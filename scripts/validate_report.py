#!/usr/bin/env python3
"""
区块链风险雷达 - 报告验证模块
确保输出符合7模块强制要求
"""

import re
from pathlib import Path

REQUIRED_SECTIONS = [
    "QUANT SIGNAL",
    "ON-CHAIN BEHAVIOR", 
    "RISK DETECTION",
    "SCAM & ANOMALY ALERT",
    "MACRO & DERIVATIVES",
    "STABLECOIN FLOW",
    "SCENARIO ANALYSIS"
]

def validate_report(report_path: str) -> dict:
    """验证报告是否包含所有必需模块"""
    result = {
        'valid': False,
        'missing_sections': [],
        'errors': []
    }
    
    try:
        content = Path(report_path).read_text(encoding='utf-8')
    except Exception as e:
        result['errors'].append(f"无法读取文件: {e}")
        return result
    
    # 检查必需模块
    for section in REQUIRED_SECTIONS:
        if section not in content:
            result['missing_sections'].append(section)
    
    # 检查敏感信息泄露
    sensitive_patterns = [
        r'DISCORD_API_KEY[=:]\s*\w+',
        r'ETHERSCAN_API_KEY[=:]\s*\w+',
        r'webhooks/\d+/[\w-]+',  # Discord webhook URL
    ]
    
    for pattern in sensitive_patterns:
        if re.search(pattern, content, re.IGNORECASE):
            result['errors'].append(f"检测到敏感信息泄露: {pattern}")
    
    # 检查硬编码数据
    if 'btc_price': 69898 in content or 'btc_price': 0 in content:
        result['errors'].append("检测到硬编码或零值价格数据，请确保使用实时API")
    
    result['valid'] = len(result['missing_sections']) == 0 and len(result['errors']) == 0
    return result

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("用法: python validate_report.py <report_path>")
        sys.exit(1)
    
    result = validate_report(sys.argv[1])
    print(f"验证结果: {'通过' if result['valid'] else '失败'}")
    
    if result['missing_sections']:
        print(f"\n缺失模块: {', '.join(result['missing_sections'])}")
    
    if result['errors']:
        print(f"\n错误: {', '.join(result['errors'])}")
    
    sys.exit(0 if result['valid'] else 1)
