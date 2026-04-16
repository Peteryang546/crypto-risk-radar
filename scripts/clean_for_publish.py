#!/usr/bin/env python3
"""
清理报告用于Hashnode发布
- 使用美东时间(ET)
- 移除AI不友好的表格
- 移除中文
- 简化SEO
- 移除About部分
"""

import re
import sys
from datetime import datetime
from pathlib import Path

def convert_to_et(utc_time_str):
    """将UTC时间转换为美东时间"""
    try:
        dt = datetime.strptime(utc_time_str, '%Y-%m-%d %H:%M UTC')
        # ET = UTC - 4 (夏令时) 或 -5 (标准时间)
        # 简化处理，使用-4小时
        from datetime import timedelta
        et_dt = dt - timedelta(hours=4)
        return et_dt.strftime('%Y-%m-%d %H:%M ET')
    except:
        return utc_time_str

def clean_report(input_file, output_file=None):
    """清理报告用于发布"""
    
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. 转换时间为美东时间 (ET)
    def replace_time(match):
        utc_str = match.group(1)
        try:
            dt = datetime.strptime(utc_str, '%Y-%m-%d %H:%M UTC')
            from datetime import timedelta
            et_dt = dt - timedelta(hours=4)  # ET = UTC - 4
            return f"**Data as of**: {et_dt.strftime('%Y-%m-%d %H:%M ET')}"
        except:
            return match.group(0)
    
    content = re.sub(
        r'\*\*Data as of\*\*:\s*(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}\s+UTC)',
        replace_time,
        content
    )
    
    # 2. 移除历史回测表格，改为段落描述
    historical_section = re.search(
        r'## 5️⃣ HISTORICAL BACKTEST.*?\n\*\*Similar signal definition\*\*:.*?\n\*\*Matched events\*\*.*?\n\|[^|]+\|[^|]+\|[^|]+\|[^|]+\|[^|]+\|[^|]+\|\n((?:\|[^|]+\|[^|]+\|[^|]+\|[^|]+\|[^|]+\|[^|]+\|\n)+)',
        content,
        re.DOTALL
    )
    
    if historical_section:
        table_text = historical_section.group(1)
        # 解析表格数据
        rows = []
        for line in table_text.strip().split('\n'):
            parts = [p.strip() for p in line.split('|')[1:-1]]
            if len(parts) >= 6:
                rows.append({
                    'date': parts[0],
                    'score': parts[1],
                    'netflow': parts[2],
                    'funding': parts[3],
                    'return_1w': parts[4],
                    'return_2w': parts[5]
                })
        
        # 生成段落描述
        if rows:
            narrative = "**Historical matches found**: " + str(len(rows)) + " similar signals.\n\n"
            for i, row in enumerate(rows[:3], 1):
                narrative += f"**Match {i}** ({row['date']}): Score {row['score']}, netflow {row['netflow']}, funding {row['funding']}. Result: {row['return_1w']} after 1W, {row['return_2w']} after 2W.\n\n"
            
            # 替换表格为段落
            content = re.sub(
                r'(## 5️⃣ HISTORICAL BACKTEST.*?\n\*\*Similar signal definition\*\*:.*?\n)\*\*Matched events\*\*.*?\n\|[^|]+\|[^|]+\|[^|]+\|[^|]+\|[^|]+\|[^|]+\|\n(?:\|[^|]+\|[^|]+\|[^|]+\|[^|]+\|[^|]+\|[^|]+\|\n)+',
                r'\1' + narrative,
                content,
                flags=re.DOTALL
            )
    
    # 3. 简化Scenario Analysis表格为段落
    scenario_section = re.search(
        r'\*\*Scenario Analysis\*\*:.*?\n\|[^|]+\|[^|]+\|[^|]+\|[^|]+\|[^|]+\|\n((?:\|[^|]+\|[^|]+\|[^|]+\|[^|]+\|[^|]+\|\n)+)',
        content,
        re.DOTALL
    )
    
    if scenario_section:
        table_text = scenario_section.group(1)
        scenarios = []
        for line in table_text.strip().split('\n'):
            parts = [p.strip() for p in line.split('|')[1:-1]]
            if len(parts) >= 5:
                scenarios.append({
                    'name': parts[0],
                    'prob': parts[1],
                    'trigger': parts[2],
                    'action': parts[3],
                    'target': parts[4]
                })
        
        if scenarios:
            narrative = "\n"
            for s in scenarios:
                target_str = f" Target: {s['target']}." if s['target'] != '-' else ""
                narrative += f"- **{s['name']}** ({s['prob']} probability): If {s['trigger']}, then {s['action']}.{target_str}\n"
            narrative += "\n"
            
            content = re.sub(
                r'(\*\*Scenario Analysis\*\*:.*?)\n\|[^|]+\|[^|]+\|[^|]+\|[^|]+\|[^|]+\|\n(?:\|[^|]+\|[^|]+\|[^|]+\|[^|]+\|[^|]+\|\n)+',
                r'\1' + narrative,
                content,
                flags=re.DOTALL
            )
    
    # 4. 移除中文内容（保留基本标点）
    content = re.sub(r'Note: DXY[^\n]*?滞后[^\n]*', 'Note: DXY impact on BTC typically has 24-48 hour lag.', content)
    # 只移除中文字符，保留英文和基本标点
    content = re.sub(r'[\u4e00-\u9fff]+', '', content)
    
    # 5. 简化SEO部分
    content = re.sub(
        r'## SEO Keywords.*?(?=##|$)',
        '',
        content,
        flags=re.DOTALL
    )
    
    # 6. 移除About部分
    content = re.sub(
        r'## About Crypto Risk Radar.*?(?=---|$)',
        '',
        content,
        flags=re.DOTALL
    )
    
    # 7. 简化JSON-LD
    content = re.sub(
        r'<script type="application/ld\+json">.*?</script>',
        '',
        content,
        flags=re.DOTALL
    )
    
    # 8. 恢复emoji为简单符号
    content = content.replace('🔴', '[RED]').replace('🟡', '[YELLOW]').replace('🟢', '[GREEN]').replace('⚪', '[WHITE]').replace('🔵', '[BLUE]')
    content = content.replace('🚨', '##').replace('1️⃣', '1.').replace('2️⃣', '2.').replace('3️⃣', '3.').replace('4️⃣', '4.').replace('5️⃣', '5.').replace('6️⃣', '6.').replace('7️⃣', '7.')
    
    # 9. 清理多余空行
    content = re.sub(r'\n{3,}', '\n\n', content)
    
    # 保存
    if output_file is None:
        input_path = Path(input_file)
        output_file = input_path.parent / f"publish_{input_path.name}"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"[SUCCESS] Cleaned for publish: {output_file}")
    return str(output_file)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python clean_for_publish.py <input_file> [output_file]")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    clean_report(input_file, output_file)
