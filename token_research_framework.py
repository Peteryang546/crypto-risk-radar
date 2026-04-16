#!/usr/bin/env python3
"""
Token Research Framework - Five Vulnerabilities Detection
五大软肋检测框架

检测维度:
1. 合约代码风险 (Contract Risk)
2. 持仓分布 (Holder Distribution)
3. 流动性管理 (Liquidity Management)
4. 开发者关联 (Developer Association)
5. 营销叙事 (Marketing Narrative)
"""

import json
import requests
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import Optional, Dict, List
from pathlib import Path

# API配置
GOPLUS_API = "https://api.gopluslabs.io/api/v1/token_security/{chain}"
DEXSCREENER_API = "https://api.dexscreener.com/latest/dex/tokens/{address}"
ETHERSCAN_API = "https://api.etherscan.io/api"


@dataclass
class ContractRisk:
    """合约代码风险"""
    is_honeypot: bool = False
    sell_tax: float = 0.0
    buy_tax: float = 0.0
    has_hidden_owner: bool = False
    is_open_source: bool = False
    is_mintable: bool = False
    can_take_back_ownership: bool = False
    owner_address: str = ""
    
    def risk_score(self) -> int:
        """计算风险分数 (0-100)"""
        score = 0
        if self.is_honeypot: score += 40
        if self.sell_tax > 10: score += 20
        if self.has_hidden_owner: score += 15
        if not self.is_open_source: score += 10
        if self.is_mintable: score += 10
        if self.can_take_back_ownership: score += 5
        return min(score, 100)


@dataclass
class HolderDistribution:
    """持仓分布"""
    top10_percentage: float = 0.0
    top50_percentage: float = 0.0
    total_holders: int = 0
    new_wallets_24h: int = 0
    
    def risk_score(self) -> int:
        """计算风险分数"""
        score = 0
        if self.top10_percentage > 50: score += 30
        elif self.top10_percentage > 30: score += 15
        if self.top50_percentage > 80: score += 20
        if self.total_holders < 100: score += 20
        return min(score, 100)


@dataclass
class LiquidityManagement:
    """流动性管理"""
    liquidity_locked: bool = False
    lock_duration_days: int = 0
    liquidity_usd: float = 0.0
    lp_holder_count: int = 0
    
    def risk_score(self) -> int:
        """计算风险分数"""
        score = 0
        if not self.liquidity_locked: score += 40
        elif self.lock_duration_days < 30: score += 20
        if self.liquidity_usd < 50000: score += 25
        elif self.liquidity_usd < 100000: score += 10
        return min(score, 100)


@dataclass
class DeveloperAssociation:
    """开发者关联"""
    team_doxxed: bool = False
    has_website: bool = False
    has_whitepaper: bool = False
    social_media_count: int = 0
    developer_wallet_activity: str = "unknown"
    
    def risk_score(self) -> int:
        """计算风险分数"""
        score = 0
        if not self.team_doxxed: score += 20
        if not self.has_website: score += 15
        if not self.has_whitepaper: score += 10
        if self.social_media_count < 2: score += 15
        return min(score, 100)


@dataclass
class MarketingNarrative:
    """营销叙事"""
    promises_high_returns: bool = False
    uses_viral_marketing: bool = False
    has_celebrity_endorsement: bool = False
    narrative_consistency: str = "unknown"  # consistent, inconsistent, contradictory
    
    def risk_score(self) -> int:
        """计算风险分数"""
        score = 0
        if self.promises_high_returns: score += 30
        if self.uses_viral_marketing: score += 15
        if self.has_celebrity_endorsement: score += 10
        if self.narrative_consistency == "contradictory": score += 25
        return min(score, 100)


@dataclass
class TokenResearchReport:
    """代币研究报告"""
    token_symbol: str
    contract_address: str
    chain: str
    timestamp: str
    
    # 五大软肋
    contract_risk: ContractRisk
    holder_distribution: HolderDistribution
    liquidity_management: LiquidityManagement
    developer_association: DeveloperAssociation
    marketing_narrative: MarketingNarrative
    
    # 综合评估
    overall_risk_score: int = 0
    risk_level: str = ""  # 极高风险/高风险/中风险/低风险
    recommended_action: str = ""  # 直接忽略/远离/观察/可研究
    
    def calculate_overall_risk(self) -> int:
        """计算综合风险分数"""
        scores = [
            self.contract_risk.risk_score(),
            self.holder_distribution.risk_score(),
            self.liquidity_management.risk_score(),
            self.developer_association.risk_score(),
            self.marketing_narrative.risk_score()
        ]
        # 加权平均：合约风险权重更高
        weights = [0.35, 0.20, 0.25, 0.10, 0.10]
        self.overall_risk_score = int(sum(s * w for s, w in zip(scores, weights)))
        
        # 确定风险等级和应对策略
        # Thresholds:
        # >= 70: [CRIT] Extreme Risk - Directly ignore
        # 50-69: [HIGH] High Risk - Stay away
        # 30-49: [MED] Medium Risk - Observe only
        # < 30: [LOW] Low Risk - Study & research
        if self.overall_risk_score >= 70:
            self.risk_level = "[CRIT] Extreme Risk"
            self.recommended_action = "IGNORE DIRECTLY - The token exhibits clear fraudulent characteristics (honeypot, unlocked liquidity, etc.). Participation risk is extremely high. Recommended to completely disregard."
        elif self.overall_risk_score >= 50:
            self.risk_level = "[HIGH] High Risk"
            self.recommended_action = "STAY AWAY - Multiple suspicious signals present (anonymous team, concentrated holdings). High probability of being a scam. Not recommended for participation."
        elif self.overall_risk_score >= 30:
            self.risk_level = "[MED] Medium Risk"
            self.recommended_action = "OBSERVE ONLY - Risk signals present but not fully confirmed. Can be added to watchlist for further data. Do not participate."
        else:
            self.risk_level = "[LOW] Low Risk"
            self.recommended_action = "STUDY & RESEARCH - Lower risk profile. Can be used as a case study for learning blockchain technology. Not an investment recommendation."
        
        return self.overall_risk_score
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            "token_symbol": self.token_symbol,
            "contract_address": self.contract_address,
            "chain": self.chain,
            "timestamp": self.timestamp,
            "contract_risk": asdict(self.contract_risk),
            "holder_distribution": asdict(self.holder_distribution),
            "liquidity_management": asdict(self.liquidity_management),
            "developer_association": asdict(self.developer_association),
            "marketing_narrative": asdict(self.marketing_narrative),
            "overall_risk_score": self.overall_risk_score,
            "risk_level": self.risk_level,
            "recommended_action": self.recommended_action
        }
    
    def generate_fact_sheet(self) -> str:
        """生成事实清单（Markdown格式）"""
        lines = [
            f"# {self.token_symbol} - On-Chain Anomaly Fact Sheet",
            f"",
            f"**Contract Address**: `{self.contract_address}`",
            f"**Chain**: {self.chain}",
            f"**Detection Time**: {self.timestamp}",
            f"**Overall Risk Score**: {self.overall_risk_score}/100",
            f"**Risk Level**: {self.risk_level}",
            f"",
            f"---",
            f"",
            f"## Risk Scoring Methodology",
            f"",
            f"| Risk Level | Score Range | Recommended Action |",
            f"|------------|-------------|-------------------|",
            f"| [CRIT] Extreme Risk | >= 70 | IGNORE DIRECTLY |",
            f"| [HIGH] High Risk | 50-69 | STAY AWAY |",
            f"| [MED] Medium Risk | 30-49 | OBSERVE ONLY |",
            f"| [LOW] Low Risk | < 30 | STUDY & RESEARCH |",
            f"",
            f"**Scoring Weights**: Contract Code (35%) / Holder Distribution (20%) / Liquidity Management (25%) / Developer Association (10%) / Marketing Narrative (10%)",
            f"",
            f"---",
            f"",
            f"## 1. Contract Code Risk",
            f"",
            f"| Detection Item | Result | Risk Signal |",
            f"|----------------|--------|-------------|",
            f"| Honeypot | {'[WARN] YES' if self.contract_risk.is_honeypot else '[OK] NO'} | {'[!!] Investors cannot sell' if self.contract_risk.is_honeypot else '[OK] Normal'} |",
            f"| Sell Tax | {self.contract_risk.sell_tax}% | {'[!!] High sell tax' if self.contract_risk.sell_tax > 10 else '[OK] Normal'} |",
            f"| Buy Tax | {self.contract_risk.buy_tax}% | [OK] Normal |",
            f"| Hidden Owner | {'[WARN] YES' if self.contract_risk.has_hidden_owner else '[OK] NO'} | {'[!!] Hidden controller exists' if self.contract_risk.has_hidden_owner else '[OK] Transparent'} |",
            f"| Contract Verified | {'[OK] YES' if self.contract_risk.is_open_source else '[WARN] NO'} | {'[!!] Code not verified, cannot audit' if not self.contract_risk.is_open_source else '[OK] Verified'} |",
            f"| Mintable | {'[WARN] YES' if self.contract_risk.is_mintable else '[OK] NO'} | {'[!!] Team can mint anytime' if self.contract_risk.is_mintable else '[OK] Fixed supply'} |",
            f"| Owner Can Take Back | {'[WARN] YES' if self.contract_risk.can_take_back_ownership else '[OK] NO'} | {'[!!] Ownership can be reclaimed' if self.contract_risk.can_take_back_ownership else '[OK] Safe'} |",
            f"| Owner Address | {self.contract_risk.owner_address or 'N/A'} | - |",
            f"| **Risk Score** | **{self.contract_risk.risk_score()}/100** | |",
            f"",
            f"**Key Findings**:",
            f"- Contract detected as **HONEYPOT** - investors can buy but cannot sell",
            f"- Sell tax as high as **{self.contract_risk.sell_tax}%**, severely exploitative",
            f"- Contract {'not verified' if not self.contract_risk.is_open_source else 'verified'}, code cannot be audited" if not self.contract_risk.is_open_source else "",
            f"- Hidden owner exists, contract can be modified anytime" if self.contract_risk.has_hidden_owner else "",
            f"",
            f"---",
            f"",
            f"## 2. Holder Distribution",
            f"",
            f"| Detection Item | Result | Risk Signal |",
            f"|----------------|--------|-------------|",
            f"| Top 10 Holders | {self.holder_distribution.top10_percentage}% | {'[!!] Highly concentrated' if self.holder_distribution.top10_percentage > 50 else '[WARN] Moderately concentrated' if self.holder_distribution.top10_percentage > 30 else '[OK] Decentralized'} |",
            f"| Top 50 Holders | {self.holder_distribution.top50_percentage}% | {'[!!] Extremely concentrated' if self.holder_distribution.top50_percentage > 80 else '[OK] Normal'} |",
            f"| Total Holders | {self.holder_distribution.total_holders} | {'[!!] Very few participants' if self.holder_distribution.total_holders < 500 else '[OK] Active community'} |",
            f"| New Wallets (24h) | {self.holder_distribution.new_wallets_24h} | {'[!!] Suspicious growth' if self.holder_distribution.new_wallets_24h > 50 else '[OK] Normal'} |",
            f"| **Risk Score** | **{self.holder_distribution.risk_score()}/100** | |",
            f"",
            f"**Key Findings**:",
            f"- Top 10 addresses control **{self.holder_distribution.top10_percentage}%** of tokens",
            f"- Top 50 addresses control **{self.holder_distribution.top50_percentage}%** of tokens",
            f"- Only **{self.holder_distribution.total_holders}** total holders, extremely poor liquidity",
            f"",
            f"---",
            f"",
            f"## 3. Liquidity Management",
            f"",
            f"| Detection Item | Result | Risk Signal |",
            f"|----------------|--------|-------------|",
            f"| LP Locked | {'[OK] YES' if self.liquidity_management.liquidity_locked else '[WARN] NO'} | {'[!!] Liquidity can be withdrawn anytime (Rug Pull risk)' if not self.liquidity_management.liquidity_locked else '[OK] Locked'} |",
            f"| Lock Duration | {self.liquidity_management.lock_duration_days} days | {'[!!] Not locked' if self.liquidity_management.lock_duration_days == 0 else '[OK] Locked'} |",
            f"| Liquidity Size | ${self.liquidity_management.liquidity_usd:,.0f} | {'[!!] Extremely low, easily manipulated' if self.liquidity_management.liquidity_usd < 50000 else '[WARN] Low liquidity' if self.liquidity_management.liquidity_usd < 100000 else '[OK] Adequate'} |",
            f"| LP Holders | {self.liquidity_management.lp_holder_count} | {'[!!] Very few control liquidity' if self.liquidity_management.lp_holder_count < 5 else '[OK] Decentralized'} |",
            f"| **Risk Score** | **{self.liquidity_management.risk_score()}/100** | |",
            f"",
            f"**Key Findings**:",
            f"- **Liquidity not locked**, can be withdrawn anytime (Rug Pull risk)",
            f"- Liquidity only **${self.liquidity_management.liquidity_usd:,.0f}**, extremely easy to manipulate",
            f"- Only **{self.liquidity_management.lp_holder_count}** LP holders, highly concentrated",
            f"",
            f"---",
            f"",
            f"## 4. Developer Association",
            f"",
            f"| Detection Item | Result | Risk Signal |",
            f"|----------------|--------|-------------|",
            f"| Team Doxxed | {'[OK] YES' if self.developer_association.team_doxxed else '[WARN] NO'} | {'[!!] Anonymous team, cannot trace' if not self.developer_association.team_doxxed else '[OK] Transparent'} |",
            f"| Website | {'[OK] YES' if self.developer_association.has_website else '[WARN] NO'} | {'[OK] Has website' if self.developer_association.has_website else '[WARN] No website'} |",
            f"| Whitepaper | {'[OK] YES' if self.developer_association.has_whitepaper else '[WARN] NO'} | {'[!!] No technical documentation' if not self.developer_association.has_whitepaper else '[OK] Has whitepaper'} |",
            f"| Social Media | {self.developer_association.social_media_count} | {'[!!] Only 1 social account' if self.developer_association.social_media_count < 2 else '[OK] Multiple channels'} |",
            f"| **Risk Score** | **{self.developer_association.risk_score()}/100** | |",
            f"",
            f"**Key Findings**:",
            f"- Team is completely **anonymous**, cannot be traced",
            f"- {'No whitepaper, lacks technical documentation' if not self.developer_association.has_whitepaper else 'Has whitepaper'}",
            f"| **Risk Score** | **{self.contract_risk.risk_score()}/100** | |",
            f"",
            f"**Key Findings**:",
            f"- Contract detected as **HONEYPOT** - investors can buy but cannot sell",
            f"- Sell tax as high as **{self.contract_risk.sell_tax}%**, severely exploitative",
            f"- Contract {'not verified' if not self.contract_risk.is_open_source else 'verified'}, code cannot be audited" if not self.contract_risk.is_open_source else "",
            f"- Hidden owner exists, contract can be modified anytime" if self.contract_risk.has_hidden_owner else "",
            f"",
            f"---",
            f"",
            f"## 2. Holder Distribution",
            f"",
            f"| Detection Item | Result | Risk Signal |",
            f"|----------------|--------|-------------|",
            f"| Top 10 Holders | {self.holder_distribution.top10_percentage}% | {'⚠️ Highly concentrated' if self.holder_distribution.top10_percentage > 50 else '⚠️ Moderately concentrated' if self.holder_distribution.top10_percentage > 30 else '✓ Decentralized'} |",
            f"| Top 50 Holders | {self.holder_distribution.top50_percentage}% | {'⚠️ Extremely concentrated' if self.holder_distribution.top50_percentage > 80 else '✓ Normal'} |",
            f"| Total Holders | {self.holder_distribution.total_holders} | {'⚠️ Very few participants' if self.holder_distribution.total_holders < 500 else '✓ Active community'} |",
            f"| New Wallets (24h) | {self.holder_distribution.new_wallets_24h} | {'⚠️ Suspicious growth' if self.holder_distribution.new_wallets_24h > 50 else '✓ Normal'} |",
            f"| **Risk Score** | **{self.holder_distribution.risk_score()}/100** | |",
            f"",
            f"**Key Findings**:",
            f"- Top 10 addresses control **{self.holder_distribution.top10_percentage}%** of tokens",
            f"- Top 50 addresses control **{self.holder_distribution.top50_percentage}%** of tokens",
            f"- Only **{self.holder_distribution.total_holders}** total holders, extremely poor liquidity",
            f"",
            f"---",
            f"",
            f"## 3. Liquidity Management",
            f"",
            f"| Detection Item | Result | Risk Signal |",
            f"|----------------|--------|-------------|",
            f"| LP Locked | {'[OK] YES' if self.liquidity_management.liquidity_locked else '[WARN] NO'} | {'⚠️ Liquidity can be withdrawn anytime (Rug Pull risk)' if not self.liquidity_management.liquidity_locked else '✓ Locked'} |",
            f"| Lock Duration | {self.liquidity_management.lock_duration_days} days | {'⚠️ Not locked' if self.liquidity_management.lock_duration_days == 0 else '✓ Locked'} |",
            f"| Liquidity Size | ${self.liquidity_management.liquidity_usd:,.0f} | {'⚠️ Extremely low, easily manipulated' if self.liquidity_management.liquidity_usd < 50000 else '⚠️ Low liquidity' if self.liquidity_management.liquidity_usd < 100000 else '✓ Adequate'} |",
            f"| LP Holders | {self.liquidity_management.lp_holder_count} | {'⚠️ Very few control liquidity' if self.liquidity_management.lp_holder_count < 5 else '✓ Decentralized'} |",
            f"| **Risk Score** | **{self.liquidity_management.risk_score()}/100** | |",
            f"",
            f"**Key Findings**:",
            f"- **Liquidity not locked**, can be withdrawn anytime (Rug Pull risk)",
            f"- Liquidity only **${self.liquidity_management.liquidity_usd:,.0f}**, extremely easy to manipulate",
            f"- Only **{self.liquidity_management.lp_holder_count}** LP holders, highly concentrated",
            f"",
            f"---",
            f"",
            f"## 4. Developer Association",
            f"",
            f"| Detection Item | Result | Risk Signal |",
            f"|----------------|--------|-------------|",
            f"| Team Doxxed | {'[OK] YES' if self.developer_association.team_doxxed else '[WARN] NO'} | {'⚠️ Anonymous team, cannot trace' if not self.developer_association.team_doxxed else '✓ Transparent'} |",
            f"| Website | {'[OK] YES' if self.developer_association.has_website else '[WARN] NO'} | {'✓ Has website' if self.developer_association.has_website else '⚠️ No website'} |",
            f"| Whitepaper | {'[OK] YES' if self.developer_association.has_whitepaper else '[WARN] NO'} | {'⚠️ No technical documentation' if not self.developer_association.has_whitepaper else '✓ Has whitepaper'} |",
            f"| Social Media | {self.developer_association.social_media_count} | {'⚠️ Only 1 social account' if self.developer_association.social_media_count < 2 else '✓ Multiple channels'} |",
            f"| **Risk Score** | **{self.developer_association.risk_score()}/100** | |",
            f"",
            f"**Key Findings**:",
            f"- Team is completely **anonymous**, cannot be traced",
            f"- {'No whitepaper, lacks technical documentation' if not self.developer_association.has_whitepaper else 'Has whitepaper'}" if not self.developer_association.has_whitepaper else "",
            f"",
            f"---",
            f"",
            f"## 5. Marketing Narrative",
            f"",
            f"| Detection Item | Result | Risk Signal |",
            f"|----------------|--------|-------------|",
            f"| Promises High Returns | {'[WARN] YES' if self.marketing_narrative.promises_high_returns else '[OK] NO'} | {'⚠️ Promises unrealistic returns' if self.marketing_narrative.promises_high_returns else '✓ No exaggerated claims'} |",
            f"| Viral Marketing | {'[WARN] YES' if self.marketing_narrative.uses_viral_marketing else '[OK] NO'} | {'⚠️ Uses viral marketing tactics' if self.marketing_narrative.uses_viral_marketing else '✓ Organic growth'} |",
            f"| Celebrity Endorsement | {'[WARN] YES' if self.marketing_narrative.has_celebrity_endorsement else '[OK] NO'} | {'⚠️ Fake celebrity endorsement' if self.marketing_narrative.has_celebrity_endorsement else '✓ No false endorsement'} |",
            f"| Narrative Consistency | {self.marketing_narrative.narrative_consistency} | {'⚠️ Contradictory claims' if self.marketing_narrative.narrative_consistency == 'contradictory' else '✓ Consistent'} |",
            f"| **Risk Score** | **{self.marketing_narrative.risk_score()}/100** | |",
            f"",
            f"**Key Findings**:",
            f"- {'Promises **unrealistic returns** to attract investors' if self.marketing_narrative.promises_high_returns else 'No unrealistic return promises'}" if self.marketing_narrative.promises_high_returns else "",
            f"- Uses **viral marketing** tactics" if self.marketing_narrative.uses_viral_marketing else "",
            f"- Marketing claims **contradict** on-chain data" if self.marketing_narrative.narrative_consistency == 'contradictory' else "",
            f"",
            f"---",
            f"",
            f"## Project Claims vs On-Chain Facts",
            f"",
            f"| Dimension | Project/KOL Claims | On-Chain Facts |",
            f"|-----------|-------------------|----------------|",
            f"| **Technology** | [To be filled] | [To be filled] |",
            f"| **Listing** | [To be filled] | [To be filled] |",
            f"| **Returns** | [To be filled] | [To be filled] |",
            f"| **Team** | [To be filled] | [To be filled] |",
            f"| **Security** | [To be filled] | [To be filled] |",
            f"",
            f"---",
            f"",
            f"## Comprehensive Assessment",
            f"",
            f"### Risk Calculation",
            f"",
            f"| Vulnerability | Weight | Score | Weighted |",
            f"|--------------|--------|-------|----------|",
            f"| Contract Code | 35% | {self.contract_risk.risk_score()} | {self.contract_risk.risk_score() * 0.35:.1f} |",
            f"| Holder Distribution | 20% | {self.holder_distribution.risk_score()} | {self.holder_distribution.risk_score() * 0.20:.1f} |",
            f"| Liquidity Management | 25% | {self.liquidity_management.risk_score()} | {self.liquidity_management.risk_score() * 0.25:.1f} |",
            f"| Developer Association | 10% | {self.developer_association.risk_score()} | {self.developer_association.risk_score() * 0.10:.1f} |",
            f"| Marketing Narrative | 10% | {self.marketing_narrative.risk_score()} | {self.marketing_narrative.risk_score() * 0.10:.1f} |",
            f"| **Total** | **100%** | - | **{self.overall_risk_score:.1f}** |",
            f"",
            f"### Classification Result",
            f"",
            f"- **Risk Level**: {self.risk_level}",
            f"- **Overall Score**: {self.overall_risk_score}/100",
            f"- **Recommended Action**: {self.recommended_action}",
            f"",
            f"---",
            f"",
            f"## Data Verification Links",
            f"",
            f"- [View on GoPlus Security](https://gopluslabs.io/token-security/{self.chain}/{self.contract_address})",
            f"- [View on Etherscan](https://etherscan.io/token/{self.contract_address})",
            f"- [View on DEX Screener](https://dexscreener.com/ethereum/{self.contract_address})",
            f"",
            f"---",
            f"",
            f"*This fact sheet only presents on-chain verifiable facts and does not constitute investment advice.*",
            f"",
            f"*Detection Time: {self.timestamp}*",
            f"",
            f"*Data Sources: GoPlus Security API, DEX Screener, Etherscan*"
        ]
        return "\n".join(lines)


class TokenResearcher:
    """代币研究员"""
    
    def __init__(self, goplus_api_key: Optional[str] = None):
        self.goplus_api_key = goplus_api_key or "XPPWb0UTTAumkyGXPxKd"
        self.goplus_secret = "DJMyH3wA0caqv0zmWpGkazasKGz1y3As"
        self.session = requests.Session()
    
    def analyze_token(self, token_address: str, chain: str = "1", 
                      token_symbol: str = "") -> TokenResearchReport:
        """
        分析代币
        
        Args:
            token_address: 合约地址
            chain: 链ID (1=ETH, 56=BSC, etc.)
            token_symbol: 代币符号
        
        Returns:
            TokenResearchReport: 研究报告
        """
        # 获取GoPlus安全数据
        contract_risk = self._fetch_contract_risk(token_address, chain)
        
        # 获取DEX Screener数据
        holder_dist, liquidity = self._fetch_dex_data(token_address)
        
        # 开发者信息（需要人工补充或从其他源获取）
        dev_assoc = DeveloperAssociation()  # 默认空值
        
        # 营销叙事（需要人工补充）
        marketing = MarketingNarrative()  # 默认空值
        
        # 创建报告
        report = TokenResearchReport(
            token_symbol=token_symbol or "UNKNOWN",
            contract_address=token_address,
            chain=chain,
            timestamp=datetime.now().isoformat(),
            contract_risk=contract_risk,
            holder_distribution=holder_dist,
            liquidity_management=liquidity,
            developer_association=dev_assoc,
            marketing_narrative=marketing
        )
        
        # 计算综合风险
        report.calculate_overall_risk()
        
        return report
    
    def _fetch_contract_risk(self, token_address: str, chain: str) -> ContractRisk:
        """获取合约风险数据"""
        try:
            url = GOPLUS_API.format(chain=chain)
            params = {"contract_addresses": token_address}
            headers = {}
            
            # GoPlus API authentication
            if self.goplus_api_key:
                # Try Authorization header first
                headers["Authorization"] = self.goplus_api_key
                # Also add as query parameter for compatibility
                params["api_key"] = self.goplus_api_key
            
            resp = self.session.get(url, params=params, headers=headers, timeout=30)
            data = resp.json()
            
            # Check for various response codes
            # code=1: success (free tier)
            # code=200: success (paid tier)
            # code=4012: signature verification failure
            if data.get("code") not in [1, 200]:
                print(f"[WARNING] GoPlus API returned code: {data.get('code')}, message: {data.get('message', 'N/A')}")
                return ContractRisk()
            
            token_data = data.get("data", {}).get(token_address.lower(), {})
            
            return ContractRisk(
                is_honeypot=token_data.get("is_honeypot", "0") == "1",
                sell_tax=float(token_data.get("sell_tax", "0")),
                buy_tax=float(token_data.get("buy_tax", "0")),
                has_hidden_owner=token_data.get("hidden_owner", "0") == "1",
                is_open_source=token_data.get("is_open_source", "0") == "1",
                is_mintable=token_data.get("is_mintable", "0") == "1",
                can_take_back_ownership=token_data.get("can_take_back_ownership", "0") == "1",
                owner_address=token_data.get("owner_address", "")
            )
        except Exception as e:
            print(f"[WARNING] Failed to fetch contract risk: {e}")
            return ContractRisk()
    
    def _fetch_dex_data(self, token_address: str) -> tuple:
        """获取DEX数据"""
        try:
            url = DEXSCREENER_API.format(address=token_address)
            resp = self.session.get(url, timeout=30)
            data = resp.json()
            
            pairs = data.get("pairs", [])
            if not pairs:
                return HolderDistribution(), LiquidityManagement()
            
            # 取流动性最高的pair
            main_pair = max(pairs, key=lambda x: float(x.get("liquidity", {}).get("usd", 0) or 0))
            
            # 持仓分布（DEX Screener不直接提供，需要估算）
            holder_dist = HolderDistribution(
                total_holders=main_pair.get("txns", {}).get("h24", {}).get("buys", 0) + 
                             main_pair.get("txns", {}).get("h24", {}).get("sells", 0)
            )
            
            # 流动性管理
            liquidity = LiquidityManagement(
                liquidity_usd=float(main_pair.get("liquidity", {}).get("usd", 0) or 0),
                lp_holder_count=main_pair.get("liquidity", {}).get("lp", {}).get("holders", 0)
            )
            
            return holder_dist, liquidity
        except Exception as e:
            print(f"[WARNING] Failed to fetch DEX data: {e}")
            return HolderDistribution(), LiquidityManagement()


# 示例用法
if __name__ == "__main__":
    researcher = TokenResearcher()
    
    # 示例：分析一个代币（使用示例地址）
    report = researcher.analyze_token(
        token_address="0x1234567890abcdef1234567890abcdef12345678",
        token_symbol="EXAMPLE"
    )
    
    print(report.generate_fact_sheet())
    
    # 保存为JSON
    with open("token_report.json", "w", encoding="utf-8") as f:
        json.dump(report.to_dict(), f, indent=2, ensure_ascii=False)
