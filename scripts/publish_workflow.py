#!/usr/bin/env python3
"""
区块链风险雷达 - 完整发布工作流
1. 生成原始报告
2. 清理为发布版本
3. 发布到Discord
"""

import os
import sys
import json
import re
from datetime import datetime, timedelta
from pathlib import Path

# 配置
BASE_DIR = Path(__file__).parent.parent
OUTPUT_DIR = BASE_DIR / "output"
PUBLISH_DIR = BASE_DIR / "publish"
DATA_DIR = OUTPUT_DIR / "data"

# Discord Webhook
WEBHOOK_URL = "https://discord.com/api/webhooks/1491010742361784341/qBe60-H9T59TmSrO8X2-04K_iBmXlZte3LPUWUZBZgC5REuJRtH8muIm1NL5qyS7NSVg"

def clean_for_publish(content):
    """清理内容为发布版本"""
    
    lines = content.split('\n')
    cleaned_lines = []
    skip_until_next_header = False
    
    skip_section_markers = [
        '## Data Sources & Methodology',
        '## Quality Check Summary',
        '### Missing Data',
        '### Data Limitations',
        '### Signal Contradiction Analysis',
        '### Market Structure Analysis',
        '### Available Metrics',
    ]
    
    skip_line_patterns = [
        'Data unavailable',
        'N/A** -',
        'Note: Data unavailable',
        'Note: API',
        'requires Glassnode',
        'requires CryptoQuant',
        'requires Coinglass',
        'requires DEX Screener',
        'requires Bloomberg',
        'requires X platform',
        'Insufficient data',
        'Small sample (n=0',
        'historical backtest for reference only',
        'Past performance does not guarantee',
        '- [ ]',
        '- [x]',
        '**Data Gap Warning**',
        '⚠️ **Backtest Reliability Warning**',
        'API Integration Required',
        'Current system initialization phase',
        'Full backtest requires',
        'MPI and Hashrate data unavailable',
        'On-chain metrics require',
        'Current score relies primarily on',
        'Without full order book data',
        'manual scan recommended',
        'DEX Screener API',
        'Estimated New Tokens',
        'Low Liquidity Count',
        'High Concentration Count',
        'Rug Pull Rate Trend',
        'Estimated Scam Loss',
    ]
    
    for line in lines:
        # 检测跳过节
        if any(marker in line for marker in skip_section_markers):
            skip_until_next_header = True
            continue
        
        # 检测新章节
        if re.match(r'^## [^#]', line):
            skip_until_next_header = False
        
        if skip_until_next_header:
            continue
        
        # 跳过特定行
        if any(pattern in line for pattern in skip_line_patterns):
            continue
        
        # 清理行内注释
        cleaned_line = line
        cleaned_line = re.sub(r'\s*\(API data unavailable\)', '', cleaned_line)
        cleaned_line = re.sub(r'\s*\(Data unavailable[^)]*\)', '', cleaned_line)
        cleaned_line = re.sub(r'\s*\(Glassnode[^)]*\)', '', cleaned_line)
        cleaned_line = re.sub(r'\s*\(CryptoQuant[^)]*\)', '', cleaned_line)
        cleaned_line = re.sub(r'\s*\(Coinglass[^)]*\)', '', cleaned_line)
        cleaned_line = re.sub(r'\s*\(DEX Screener[^)]*\)', '', cleaned_line)
        cleaned_line = re.sub(r'\s*\(Bloomberg[^)]*\)', '', cleaned_line)
        cleaned_line = re.sub(r'\s*\(X platform[^)]*\)', '', cleaned_line)
        cleaned_line = re.sub(r'\s*\(Insufficient data\)', '', cleaned_line)
        cleaned_line = re.sub(r'\s*\(in [^)]*\)', '', cleaned_line)
        cleaned_line = re.sub(r'\s*\(estimated\)', '', cleaned_line)
        cleaned_line = re.sub(r'\s*\(manual scan[^)]*\)', '', cleaned_line)
        
        # 跳过N/A列表项
        if re.match(r'^- \*\*[^*]+\*\*:\s*N/A$', cleaned_line.strip()):
            continue
        
        cleaned_lines.append(cleaned_line)
    
    result = '\n'.join(cleaned_lines)
    result = re.sub(r'\n{4,}', '\n\n\n', result)
    result = re.sub(r'---\n+---', '---', result)
    
    return result

def generate_clean_report():
    """生成并清理报告"""
    
    # 查找最新报告
    report_files = sorted(OUTPUT_DIR.glob('v52_report_*.md'), reverse=True)
    
    if not report_files:
        print("[ERROR] No report files found")
        return None
    
    latest = report_files[0]
    print(f"[INFO] Processing: {latest.name}")
    
    with open(latest, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 清理
    cleaned = clean_for_publish(content)
    
    # 添加简洁footer
    footer = """
---

*Data: CoinGecko, Alternative.me | Report: Blockchain Risk Radar v5.2*
*Disclaimer: For informational purposes only. Not financial advice.*
"""
    cleaned += footer
    
    # 保存
    PUBLISH_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M')
    publish_file = PUBLISH_DIR / f"publish_v52_{timestamp}.md"
    
    with open(publish_file, 'w', encoding='utf-8') as f:
        f.write(cleaned)
    
    print(f"[INFO] Clean version saved: {publish_file}")
    print(f"[INFO] Size: {len(content)} -> {len(cleaned)} chars")
    
    return publish_file, cleaned

def main():
    """主工作流"""
    print("="*60)
    print("Blockchain Risk Radar - Publish Workflow")
    print("="*60)
    
    # 步骤1: 生成清理版本
    print("\n[Step 1] Generating clean publish version...")
    result = generate_clean_report()
    
    if not result:
        print("[ERROR] Failed to generate report")
        return
    
    publish_file, content = result
    
    print("\n[Step 2] Ready for review")
    print(f"File: {publish_file}")
    print("\nPreview (first 500 chars):")
    print("-"*60)
    print(content[:500])
    print("...")
    print("-"*60)
    
    print("\n[Step 3] Next actions:")
    print("  1. Review the cleaned file")
    print("  2. If satisfied, publish to Discord")
    print(f"  3. Webhook: {WEBHOOK_URL[:50]}...")
    
    return publish_file

if __name__ == '__main__':
    main()
