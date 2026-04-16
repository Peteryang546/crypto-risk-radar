#!/usr/bin/env python3
"""
区块链风险雷达 - 清理后发布版本生成器
移除所有内部技术注释，生成面向读者的干净版本
"""

import os
import sys
import re
from datetime import datetime
from pathlib import Path

# 配置
BASE_DIR = Path(__file__).parent.parent
OUTPUT_DIR = BASE_DIR / "output"
PUBLISH_DIR = BASE_DIR / "publish"

def clean_report(input_content):
    """清理报告内容，移除内部技术注释"""
    
    lines = input_content.split('\n')
    cleaned_lines = []
    skip_section = False
    skip_until_next_header = False
    in_table = False
    prev_line_empty = False
    
    for i, line in enumerate(lines):
        # 检测表格开始/结束
        if '|' in line and '---' in line:
            in_table = True
        elif in_table and not line.strip().startswith('|'):
            in_table = False
        
        # 检测并跳过内部章节标题
        if any(marker in line for marker in [
            '## Data Sources & Methodology',
            '## Quality Check Summary',
            '### Missing Data',
            '### Data Limitations',
            '### Signal Contradiction Analysis',
            '### Market Structure Analysis',
            '### Available Metrics',  # 这个章节通常是技术性的
        ]):
            skip_section = True
            skip_until_next_header = True
            continue
        
        # 检测新的大章节开始（## 开头），重置跳过状态
        if re.match(r'^## [^#]', line):
            skip_section = False
            skip_until_next_header = False
        
        # 如果在跳过模式下，跳过所有行直到下一个章节
        if skip_until_next_header and not line.startswith('##'):
            continue
        
        if skip_section:
            continue
        
        # 跳过包含特定模式的行
        skip_patterns = [
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
            'Checklist item',
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
        
        if any(pattern in line for pattern in skip_patterns):
            continue
        
        # 清理行内技术注释
        cleaned_line = line
        
        # 移除各种技术注释 (但保留表格结构)
        if not in_table:
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
        else:
            # 表格行：清理单元格内容
            cleaned_line = re.sub(r'No data available', '-', cleaned_line)
            cleaned_line = re.sub(r'N/A - [^|]*', 'N/A', cleaned_line)
            cleaned_line = re.sub(r'data unavailable', '-', cleaned_line, flags=re.IGNORECASE)
        
        # 跳过只包含 "-" 或 "N/A" 的列表项（这些是空数据标记）
        stripped = cleaned_line.strip()
        if stripped in ['- **Miner Activity**: -', '- **Exchange Netflow**: -']:
            continue
        if stripped == '### Estimated Scam Loss':
            continue
        
        # 跳过连续的 "N/A" 列表项块
        if re.match(r'^- \*\*[^*]+\*\*:\s*N/A$', stripped):
            continue
        
        # 合并连续空行
        if stripped == '':
            if prev_line_empty:
                continue
            prev_line_empty = True
        else:
            prev_line_empty = False
        
        cleaned_lines.append(cleaned_line)
    
    # 后处理
    result = '\n'.join(cleaned_lines)
    
    # 移除连续空行
    result = re.sub(r'\n{4,}', '\n\n\n', result)
    
    # 移除章节末尾的空列表
    result = re.sub(r'### [^\n]+\n\n(?=##)', '', result)
    
    # 修复重复的 ---
    result = re.sub(r'---\n+---', '---', result)
    
    return result

def extract_publish_version(input_file):
    """从原始报告提取发布版本"""
    
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 清理内容
    cleaned = clean_report(content)
    
    # 添加简洁的数据来源说明（读者版）
    footer = """
---

*Data: CoinGecko, Alternative.me | Report: Blockchain Risk Radar v5.2*
*Disclaimer: For informational purposes only. Not financial advice.*
"""
    
    return cleaned + footer

def main():
    """主函数"""
    
    # 确保发布目录存在
    PUBLISH_DIR.mkdir(parents=True, exist_ok=True)
    
    # 查找最新的报告文件
    report_files = sorted(OUTPUT_DIR.glob('v52_report_*.md'), reverse=True)
    
    if not report_files:
        print("[ERROR] No report files found in output/")
        return
    
    latest_report = report_files[0]
    print(f"[INFO] Processing: {latest_report.name}")
    
    # 生成清理版本
    publish_content = extract_publish_version(latest_report)
    
    # 保存发布版本
    timestamp = datetime.now().strftime('%Y%m%d_%H%M')
    publish_file = PUBLISH_DIR / f"publish_v52_{timestamp}.md"
    
    with open(publish_file, 'w', encoding='utf-8') as f:
        f.write(publish_content)
    
    original_size = len(open(latest_report, 'r', encoding='utf-8').read())
    clean_size = len(publish_content)
    
    print(f"[INFO] Clean version saved: {publish_file}")
    print(f"[INFO] Original size: {original_size} chars")
    print(f"[INFO] Clean size: {clean_size} chars")
    print(f"[INFO] Removed: {original_size - clean_size} chars ({(original_size - clean_size) / original_size * 100:.1f}%)")
    
    return publish_file

if __name__ == '__main__':
    main()
