#!/usr/bin/env python3
"""
发布清理器 - 将报告转换为人类友好的发布格式
"""

import re
import sys
from datetime import datetime, timedelta
from pathlib import Path

def clean_for_publish(input_file, output_file=None):
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    output = []
    in_historical_table = False
    in_scenario_table = False
    table_buffer = []
    
    scenarios = []
    
    for line in lines:
        # 1. 转换时间
        if '**Data as of**:' in line and 'UTC' in line:
            match = re.search(r'(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2})\s+UTC', line)
            if match:
                utc_str = match.group(1)
                dt = datetime.strptime(utc_str, '%Y-%m-%d %H:%M')
                et_dt = dt - timedelta(hours=4)
                line = f"**Data as of**: {et_dt.strftime('%Y-%m-%d %H:%M ET')}\n"
        
        # 2. 替换emoji
        line = line.replace('🚨', '##').replace('🔴', '[HIGH]').replace('🟡', '[MED]').replace('🟢', '[LOW]').replace('⚪', '[NEUTRAL]').replace('🔵', '[STRONG]')
        line = line.replace('1️⃣', '1.').replace('2️⃣', '2.').replace('3️⃣', '3.').replace('4️⃣', '4.').replace('5️⃣', '5.').replace('6️⃣', '6.').replace('7️⃣', '7.')
        
        # 3. 检测历史回测表格开始
        if '**Matched events**' in line or (in_historical_table and line.startswith('| Date')):
            in_historical_table = True
            table_buffer = []
            continue
        
        # 4. 处理历史回测表格
        if in_historical_table:
            if line.startswith('|') and '---' not in line:
                table_buffer.append(line)
            elif not line.startswith('|') and table_buffer:
                # 表格结束，转换为段落
                output.append('\n**Historical matches found**: 3 similar signals.\n\n')
                for i, row in enumerate(table_buffer[1:4], 1):  # 跳过表头，最多3行
                    parts = [p.strip() for p in row.split('|')[1:-1]]
                    if len(parts) >= 6:
                        output.append(f"**Match {i}** ({parts[0]}): Score {parts[1]}, netflow {parts[2]}, funding {parts[3]}. Result: {parts[4]} after 1W, {parts[5]} after 2W.\n\n")
                in_historical_table = False
                table_buffer = []
            continue
        
        # 5. 检测Scenario表格
        if '**Scenario Analysis**' in line:
            in_scenario_table = True
            output.append(line)
            continue
        
        if in_scenario_table and line.startswith('|') and 'Bull case' in line:
            # 开始处理scenario表格
            scenarios = []
            scenarios.append(line)
            continue
        
        if in_scenario_table and line.startswith('|') and scenarios:
            if '---' not in line:
                scenarios.append(line)
            else:
                # 表格分隔线，跳过
                continue
        elif in_scenario_table and scenarios and not line.startswith('|'):
            # 表格结束，转换
            output.append('\n')
            for row in scenarios:
                parts = [p.strip() for p in row.split('|')[1:-1]]
                if len(parts) >= 5 and parts[0] not in ['Scenario', '----------']:
                    target = f" Target: {parts[4]}." if parts[4] != '-' else ""
                    output.append(f"- **{parts[0]}** ({parts[1]} probability): If {parts[2]}, then {parts[3]}.{target}\n")
            output.append('\n')
            in_scenario_table = False
            scenarios = []
            continue
        
        # 6. 移除中文
        if '滞后' in line:
            line = '  - *Note*: DXY impact on BTC typically has 24-48 hour lag.\n'
        
        # 7. 跳过SEO和About部分
        if '## SEO Keywords' in line or '## About Crypto Risk Radar' in line:
            break
        
        # 8. 跳过JSON-LD
        if '<script' in line:
            continue
        
        output.append(line)
    
    # 写入文件
    result = ''.join(output)
    # 移除生成时间戳行
    result = re.sub(r'\n---\n\*Not financial advice\. Generated at[^\n]+', '', result)
    result = re.sub(r'\n{3,}', '\n\n', result)
    
    if output_file is None:
        input_path = Path(input_file)
        output_file = input_path.parent / f"publish_{input_path.name}"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(result)
    
    print(f"[SUCCESS] Published version: {output_file}")
    return str(output_file)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python publish_cleaner.py <input_file> [output_file]")
        sys.exit(1)
    
    clean_for_publish(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)
