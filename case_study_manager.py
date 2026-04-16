#!/usr/bin/env python3
"""
Case Study Manager - 案例库管理系统

摘要公开模式：
- 公开：基本信息、风险等级、关键信号
- 私有：详细交易哈希、具体地址、完整分析
"""

import json
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict


@dataclass
class CaseStudy:
    """案例研究"""
    # 公开信息
    case_id: str
    token_symbol: str
    chain: str
    discovery_date: str
    risk_level: str  # 🔴极高 / 🟠高 / 🟡中 / 🟢低
    classification: str
    
    # 关键信号（公开）
    key_signals: List[str]  # 如：["honeypot检测阳性", "流动性未锁", "团队匿名"]
    
    # 摘要描述（公开）
    summary: str  # 100字以内的摘要
    
    # 项目方声称 vs 事实（公开）
    claimed: str
    reality: str
    
    # 历史相似案例（公开）
    similar_cases: List[str]  # 案例ID列表
    
    # 私有信息（不公开）
    contract_address: str = ""  # 完整地址不公开
    detailed_analysis: str = ""  # 详细分析
    transaction_hashes: List[str] = None  # 交易哈希
    wallet_addresses: List[str] = None  # 相关钱包
    internal_notes: str = ""  # 内部备注
    
    def __post_init__(self):
        if self.transaction_hashes is None:
            self.transaction_hashes = []
        if self.wallet_addresses is None:
            self.wallet_addresses = []
    
    def generate_public_summary(self) -> str:
        """生成公开摘要（Markdown格式）"""
        lines = [
            f"## 案例 #{self.case_id}: {self.token_symbol}",
            f"",
            f"**风险等级**: {self.risk_level}",
            f"**发现日期**: {self.discovery_date}",
            f"**链**: {self.chain}",
            f"",
            f"### 关键信号",
        ]
        
        for signal in self.key_signals:
            lines.append(f"- {signal}")
        
        lines.extend([
            f"",
            f"### Case Summary",
            f"{self.summary}",
            f"",
            f"### Claims vs Facts",
            f"**Project/KOL Claims**: {self.claimed}",
            f"",
            f"**On-Chain Facts**: {self.reality}",
            f"",
        ])
        
        # 添加历史相似模式
        if self.similar_cases:
            lines.extend([
                f"### Historical Similar Patterns",
                f"",
            ])
            for case_id in self.similar_cases[:3]:
                lines.append(f"- Similar to case [{case_id}](./{case_id}.md)")
            lines.append(f"")
        
        lines.extend([
            f"---",
            f"",
            f"*This case study only presents publicly verifiable on-chain facts and does not constitute investment advice.*",
            f"",
            f"*License: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)*",
            f""
        ])
        
        return "\n".join(lines)
    
    def generate_private_report(self) -> str:
        """生成完整私有报告（仅内部使用）"""
        lines = [
            f"# 案例 #{self.case_id}: {self.token_symbol} - 完整报告",
            f"",
            f"## 基本信息",
            f"- 代币: {self.token_symbol}",
            f"- 合约: {self.contract_address}",
            f"- 链: {self.chain}",
            f"- 发现日期: {self.discovery_date}",
            f"- 风险等级: {self.risk_level}",
            f"",
            f"## 详细分析",
            f"{self.detailed_analysis}",
            f"",
            f"## 相关交易",
        ]
        
        for tx in self.transaction_hashes:
            lines.append(f"- {tx}")
        
        lines.extend([
            f"",
            f"## 相关钱包",
        ])
        
        for wallet in self.wallet_addresses:
            lines.append(f"- {wallet}")
        
        lines.extend([
            f"",
            f"## 内部备注",
            f"{self.internal_notes}",
            f"",
            f"---",
            f"*内部资料，请勿外传*",
        ])
        
        return "\n".join(lines)
    
    def to_public_dict(self) -> Dict:
        """转换为公开字典"""
        return {
            "case_id": self.case_id,
            "token_symbol": self.token_symbol,
            "chain": self.chain,
            "discovery_date": self.discovery_date,
            "risk_level": self.risk_level,
            "classification": self.classification,
            "key_signals": self.key_signals,
            "summary": self.summary,
            "claimed": self.claimed,
            "reality": self.reality,
            "similar_cases": self.similar_cases
        }
    
    def to_private_dict(self) -> Dict:
        """转换为完整字典（包含私有信息）"""
        data = self.to_public_dict()
        data.update({
            "contract_address": self.contract_address,
            "detailed_analysis": self.detailed_analysis,
            "transaction_hashes": self.transaction_hashes,
            "wallet_addresses": self.wallet_addresses,
            "internal_notes": self.internal_notes
        })
        return data


class CaseStudyManager:
    """案例库管理器"""
    
    def __init__(self, base_dir: str = r"F:\stepclaw\agents\blockchain-analyst"):
        self.base_dir = Path(base_dir)
        
        # 公开案例库
        self.public_dir = self.base_dir / "case_studies" / "public"
        self.public_dir.mkdir(parents=True, exist_ok=True)
        
        # 私有案例库
        self.private_dir = self.base_dir / "case_studies" / "private"
        self.private_dir.mkdir(parents=True, exist_ok=True)
        
        # 索引文件
        self.index_file = self.public_dir / "index.json"
        self.cases: Dict[str, CaseStudy] = {}
        
        self._load_index()
    
    def _load_index(self):
        """加载案例索引"""
        if self.index_file.exists():
            try:
                with open(self.index_file, 'r', encoding='utf-8') as f:
                    index = json.load(f)
                    for case_data in index.get("cases", []):
                        case = CaseStudy(**case_data)
                        self.cases[case.case_id] = case
                print(f"[INFO] Loaded {len(self.cases)} cases from index")
            except Exception as e:
                print(f"[WARNING] Failed to load case index: {e}")
    
    def _save_index(self):
        """保存案例索引"""
        index = {
            "updated_at": datetime.now().isoformat(),
            "total_cases": len(self.cases),
            "cases": [case.to_public_dict() for case in self.cases.values()]
        }
        
        with open(self.index_file, 'w', encoding='utf-8') as f:
            json.dump(index, f, indent=2, ensure_ascii=False)
    
    def _generate_case_id(self, token_symbol: str, contract_address: str) -> str:
        """生成案例ID"""
        # 使用代币符号 + 合约地址前8位
        addr_short = contract_address[-8:] if len(contract_address) > 8 else contract_address
        return f"{token_symbol}_{addr_short}".upper()
    
    def add_case(self, token_symbol: str, contract_address: str, chain: str,
                 risk_level: str, classification: str,
                 key_signals: List[str], summary: str,
                 claimed: str, reality: str,
                 detailed_analysis: str = "",
                 transaction_hashes: List[str] = None,
                 wallet_addresses: List[str] = None,
                 internal_notes: str = "",
                 similar_cases: List[str] = None) -> str:
        """
        添加新案例
        
        Returns:
            case_id: 案例ID
        """
        case_id = self._generate_case_id(token_symbol, contract_address)
        
        # 检查是否已存在
        if case_id in self.cases:
            print(f"[WARNING] Case {case_id} already exists, updating...")
        
        case = CaseStudy(
            case_id=case_id,
            token_symbol=token_symbol,
            chain=chain,
            discovery_date=datetime.now().strftime("%Y-%m-%d"),
            risk_level=risk_level,
            classification=classification,
            key_signals=key_signals,
            summary=summary,
            claimed=claimed,
            reality=reality,
            similar_cases=similar_cases or [],
            contract_address=contract_address,
            detailed_analysis=detailed_analysis,
            transaction_hashes=transaction_hashes or [],
            wallet_addresses=wallet_addresses or [],
            internal_notes=internal_notes
        )
        
        self.cases[case_id] = case
        
        # 保存公开版本
        public_file = self.public_dir / f"{case_id}.md"
        with open(public_file, 'w', encoding='utf-8') as f:
            f.write(case.generate_public_summary())
        
        # 保存私有版本
        private_file = self.private_dir / f"{case_id}.md"
        with open(private_file, 'w', encoding='utf-8') as f:
            f.write(case.generate_private_report())
        
        # 更新索引
        self._save_index()
        
        print(f"[INFO] Added case {case_id}")
        return case_id
    
    def get_case(self, case_id: str) -> Optional[CaseStudy]:
        """获取案例"""
        return self.cases.get(case_id)
    
    def list_cases(self, risk_level: str = None) -> List[CaseStudy]:
        """列出案例"""
        cases = list(self.cases.values())
        if risk_level:
            cases = [c for c in cases if c.risk_level == risk_level]
        return sorted(cases, key=lambda x: x.discovery_date, reverse=True)
    
    def generate_public_index_page(self) -> str:
        """生成公开索引页面（Markdown）"""
        lines = [
            "# 案例库 - 骗局警示",
            "",
            "> ⚠️ **免责声明**: 本案例库仅陈列公开可验证的链上事实，不构成投资建议。",
            "> 目的是帮助投资者识别高风险代币的典型模式。",
            "",
            f"**最后更新**: {datetime.now().strftime('%Y-%m-%d')}",
            f"**案例总数**: {len(self.cases)}",
            "",
            "## 按风险等级分类",
            "",
        ]
        
        # 按风险等级分组
        risk_levels = ["🔴 极高风险", "🟠 高风险", "🟡 中风险", "🟢 低风险"]
        
        for level in risk_levels:
            cases = self.list_cases(risk_level=level)
            if cases:
                lines.extend([
                    f"### {level}",
                    "",
                ])
                
                for case in cases[:10]:  # 每类显示前10个
                    lines.extend([
                        f"- **[{case.case_id}]({case.case_id}.md)** - {case.token_symbol}",
                        f"  - {case.summary[:80]}...",
                        f"  - 关键信号: {', '.join(case.key_signals[:3])}",
                        "",
                    ])
                
                if len(cases) > 10:
                    lines.append(f"*... 还有 {len(cases) - 10} 个案例*")
                    lines.append("")
        
        lines.extend([
            "---",
            "",
            "## 如何使用",
            "",
            "1. **识别模式**: 查看多个案例，识别共同的骗局特征",
            "2. **对比验证**: 将新发现的代币与案例对比",
            "3. **教育学习**: 了解常见的风险信号",
            "",
            "## 贡献",
            "",
            "如发现新的骗局案例，欢迎通过 [GitHub Issues](https://github.com/peteryang546/crypto-risk-radar/issues) 提交。",
            "",
            "*本案例库采用 [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) 许可。*",
        ])
        
        return "\n".join(lines)
    
    def export_public_archive(self, output_file: str = None):
        """导出公开案例库"""
        if not output_file:
            output_file = self.public_dir / "README.md"
        
        content = self.generate_public_index_page()
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"[INFO] Exported public archive to {output_file}")


# 示例用法
if __name__ == "__main__":
    manager = CaseStudyManager()
    
    # 添加示例案例
    case_id = manager.add_case(
        token_symbol="FAKEAI",
        contract_address="0x1234567890abcdef1234567890abcdef12345678",
        chain="ETH",
        risk_level="🔴 极高风险",
        classification="直接忽略",
        key_signals=["honeypot检测阳性", "卖出税率15%", "流动性未锁", "团队匿名"],
        summary="典型的高风险骗局代币，合约代码存在honeypot陷阱，投资者无法卖出。",
        claimed="AI驱动的下一代区块链，即将上线币安",
        reality="合约代码检测出honeypot，团队钱包在喊单前大量买入",
        detailed_analysis="详细技术分析内容...",
        transaction_hashes=["0xabc...", "0xdef..."],
        wallet_addresses=["0x123...", "0x456..."],
        internal_notes="内部调查备注..."
    )
    
    # 导出公开案例库
    manager.export_public_archive()
    
    print(f"\n✅ 案例 {case_id} 已添加")
