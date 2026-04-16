#!/usr/bin/env python3
"""
契约验证脚本
验证 Agent 输出是否符合 IDENTITY.md 中的显式契约
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Tuple

class ContractValidator:
    """契约验证器"""
    
    # 禁止词汇列表
    FORBIDDEN_WORDS = [
        "买入", "卖出", "抄底", "梭哈", "上车",
        "建议买", "建议卖", "必涨", "必跌",
        "投资建议", "推荐购买"
    ]
    
    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self.identity_path = Path(f"F:/stepclaw/agents/{agent_id}/IDENTITY.md")
        self.errors = []
        self.warnings = []
    
    def validate_output(self, output_path: Path) -> Tuple[bool, Dict]:
        """
        验证输出文件
        
        Returns:
            (是否通过, 详细报告)
        """
        
        self.errors = []
        self.warnings = []
        
        # 读取输出内容
        content = output_path.read_text(encoding='utf-8')
        
        # 1. 检查禁止词汇
        self._check_forbidden_words(content)
        
        # 2. 检查输出格式
        self._check_output_format(content)
        
        # 3. 检查数据来源标注
        self._check_data_sources(content)
        
        # 4. 检查质量阈值
        score = self._calculate_quality_score(content)
        
        # 生成报告
        report = {
            "agent_id": self.agent_id,
            "output_file": str(output_path),
            "passed": len(self.errors) == 0 and score >= 80,
            "score": score,
            "errors": self.errors,
            "warnings": self.warnings,
            "checks": {
                "forbidden_words": len(self.errors) == 0,
                "format_valid": len([e for e in self.errors if "格式" in e]) == 0,
                "data_sources": len([e for e in self.errors if "来源" in e]) == 0,
                "quality_threshold": score >= 80
            }
        }
        
        return report["passed"], report
    
    def _check_forbidden_words(self, content: str):
        """检查禁止词汇"""
        for word in self.FORBIDDEN_WORDS:
            if word in content:
                self.errors.append(f"发现禁止词汇: '{word}'")
    
    def _check_output_format(self, content: str):
        """检查输出格式"""
        # 根据 Agent 类型检查特定格式
        if self.agent_id == "blockchain-analyst":
            # 检查 Reels 脚本格式
            if "## 视频信息" not in content:
                self.errors.append("缺少 '## 视频信息' 部分")
            if "## 分镜脚本" not in content:
                self.errors.append("缺少 '## 分镜脚本' 部分")
        
        elif self.agent_id == "ai-market-analyst":
            # 检查文章8模块
            required_sections = [
                "## 标题", "## 痛点", "## 解决方案",
                "## 实战演示", "## 商业收益", "## 案例", "## CTA"
            ]
            for section in required_sections:
                if section not in content:
                    self.warnings.append(f"可能缺少 '{section}' 部分")
        
        elif self.agent_id == "trade-market-analyst":
            # 检查日报格式
            if "## 执行摘要" not in content:
                self.errors.append("缺少 '## 执行摘要'")
            if "## 数据抓取状态" not in content:
                self.errors.append("缺少 '## 数据抓取状态'")
    
    def _check_data_sources(self, content: str):
        """检查数据来源标注"""
        # 检查是否有数据来源标注
        if "来源" not in content and "Source" not in content:
            self.warnings.append("未明确标注数据来源")
    
    def _calculate_quality_score(self, content: str) -> int:
        """计算质量评分"""
        score = 100
        
        # 根据错误和警告扣分
        score -= len(self.errors) * 10
        score -= len(self.warnings) * 5
        
        # 根据内容完整性加分
        if len(content) > 1000:
            score += 5
        
        return max(0, min(100, score))
    
    def generate_validation_report(self, output_path: Path) -> Path:
        """生成验证报告"""
        passed, report = self.validate_output(output_path)
        
        report_path = output_path.parent / f"{output_path.stem}_validation.json"
        report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding='utf-8')
        
        return report_path


# 快捷函数
def validate_agent_output(agent_id: str, output_path: str) -> Tuple[bool, Dict]:
    """验证指定Agent的输出"""
    validator = ContractValidator(agent_id)
    return validator.validate_output(Path(output_path))


# 示例用法
if __name__ == "__main__":
    # 测试验证
    test_output = Path("F:/stepclaw/workspace/blockchain-analyst/output/test.md")
    if test_output.exists():
        passed, report = validate_agent_output("blockchain-analyst", str(test_output))
        print(f"验证结果: {'通过' if passed else '失败'}")
        print(f"评分: {report['score']}/100")
        if report['errors']:
            print(f"错误: {report['errors']}")
