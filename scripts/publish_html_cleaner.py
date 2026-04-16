#!/usr/bin/env python3
"""
HTML报告清理器 - 转换为Hashnode友好的格式
"""

import re
from datetime import datetime, timedelta
from pathlib import Path

def clean_html_report(input_file, output_file=None):
    """清理HTML报告用于发布"""
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. 转换时间 UTC -> ET
    content = re.sub(
        r'\*\*Data as of\*\*: (\d{4}-\d{2}-\d{2}) (\d{2}:\d{2}) UTC',
        lambda m: f"**Data as of**: {convert_utc_to_et(m.group(1), m.group(2))}",
        content
    )
    
    # 2. 替换emoji为标签
    emoji_map = {
        '🚨': '##',
        '🔴': '[HIGH RISK]',
        '🟡': '[MEDIUM RISK]',
        '🟢': '[LOW RISK]',
        '⚪': '[NEUTRAL]',
        '🔵': '[STRONG]',
        '✓': '✅',
        '⚠': '⚠️',
    }
    for emoji, replacement in emoji_map.items():
        content = content.replace(emoji, replacement)
    
    # 3. 移除数字emoji
    content = content.replace('1️⃣', '1.').replace('2️⃣', '2.').replace('3️⃣', '3.')
    content = content.replace('4️⃣', '4.').replace('5️⃣', '5.').replace('6️⃣', '6.')
    content = content.replace('7️⃣', '7.').replace('8️⃣', '8.')
    
    # 4. 移除中文（如果有）
    # 检测并移除中文字符
    content = re.sub(r'[\u4e00-\u9fff]+', '', content)
    
    # 5. 移除生成时间戳行
    content = re.sub(r'\*Not financial advice\. Generated at[^\n]+', '', content)
    content = re.sub(r'Not financial advice\. Generated at[^\n]+', '', content)
    
    # 6. 清理多余空行
    content = re.sub(r'\n{3,}', '\n\n', content)
    
    # 7. 确保HTML表格格式正确（Hashnode支持HTML）
    # 检查HTML标签是否完整
    if '<table' in content and '</table>' not in content:
        content += '\n</table>'
    
    # 保存
    if output_file is None:
        input_path = Path(input_file)
        output_file = input_path.parent / f"publish_{input_path.name}"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"[SUCCESS] Cleaned HTML report: {output_file}")
    return output_file

def convert_utc_to_et(date_str, time_str):
    """转换UTC时间为美东时间"""
    try:
        utc_dt = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
        et_dt = utc_dt - timedelta(hours=4)
        return et_dt.strftime("%B %d, %Y %H:%M ET")
    except:
        return f"{date_str} {time_str} ET"

def main():
    import sys
    if len(sys.argv) < 2:
        print("Usage: python publish_html_cleaner.py <input_file>")
        return
    
    input_file = sys.argv[1]
    clean_html_report(input_file)

if __name__ == "__main__":
    main()
