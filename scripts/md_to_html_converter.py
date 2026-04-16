#!/usr/bin/env python3
"""
Markdown 报告转换为完整 HTML
"""

import re
import sys
from pathlib import Path

def md_to_html(input_file, output_file=None):
    """将 Markdown 报告转换为完整 HTML"""
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 提取标题
    title_match = re.search(r'^# (.+)$', content, re.MULTILINE)
    title = title_match.group(1) if title_match else "Crypto Risk Radar Report"
    
    # 转换 Markdown 到 HTML
    html_content = content
    
    # 先处理表格 - 完全移除所有内联样式
    # 移除 table 的所有内联样式
    html_content = re.sub(r'<table\s+style="[^"]*"', r'<table', html_content, flags=re.IGNORECASE)
    # 移除 tr 的所有内联样式
    html_content = re.sub(r'<tr\s+style="[^"]*"', r'<tr', html_content, flags=re.IGNORECASE)
    # 移除 td 的所有内联样式
    html_content = re.sub(r'<td\s+style="[^"]*"', r'<td', html_content, flags=re.IGNORECASE)
    # 移除 th 的所有内联样式
    html_content = re.sub(r'<th\s+style="[^"]*"', r'<th', html_content, flags=re.IGNORECASE)
    # 移除 div 的样式（表格容器）
    html_content = re.sub(r'<div\s+style="[^"]*"[^>]*>', r'<div>', html_content, flags=re.IGNORECASE)
    # 清理空的 style 属性
    html_content = re.sub(r'\s+style="\s*"', '', html_content)
    
    # 转换标题
    html_content = re.sub(r'^###### (.+)$', r'<h6>\1</h6>', html_content, flags=re.MULTILINE)
    html_content = re.sub(r'^##### (.+)$', r'<h5>\1</h5>', html_content, flags=re.MULTILINE)
    html_content = re.sub(r'^#### (.+)$', r'<h4>\1</h4>', html_content, flags=re.MULTILINE)
    html_content = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html_content, flags=re.MULTILINE)
    html_content = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html_content, flags=re.MULTILINE)
    html_content = re.sub(r'^# (.+)$', r'<h1>\1</h1>', html_content, flags=re.MULTILINE)
    
    # 转换粗体
    html_content = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html_content)
    
    # 转换斜体
    html_content = re.sub(r'\*(.+?)\*', r'<em>\1</em>', html_content)
    
    # 转换行内代码
    html_content = re.sub(r'`(.+?)`', r'<code>\1</code>', html_content)
    
    # 转换列表项
    html_content = re.sub(r'^- (.+)$', r'<li>\1</li>', html_content, flags=re.MULTILINE)
    
    # 包裹列表
    html_content = re.sub(r'(<li>.+</li>\n)+', r'<ul>\g<0></ul>', html_content, flags=re.DOTALL)
    
    # 转换段落（非标签行）
    lines = html_content.split('\n')
    new_lines = []
    in_paragraph = False
    
    for line in lines:
        stripped = line.strip()
        # 跳过空行和标签行
        if not stripped:
            if in_paragraph:
                new_lines.append('</p>')
                in_paragraph = False
            new_lines.append('')
        elif stripped.startswith('<') and stripped.endswith('>'):
            if in_paragraph:
                new_lines.append('</p>')
                in_paragraph = False
            new_lines.append(line)
        else:
            if not in_paragraph:
                new_lines.append('<p>')
                in_paragraph = True
            new_lines.append(line)
    
    if in_paragraph:
        new_lines.append('</p>')
    
    html_content = '\n'.join(new_lines)
    
    # 构建完整 HTML
    full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background-color: #0a0e27;
            color: #ffffff;
            line-height: 1.6;
            padding: 20px;
            max-width: 1200px;
            margin: 0 auto;
        }}
        h1 {{
            color: #00d4ff;
            font-size: 2em;
            margin-bottom: 20px;
            text-align: center;
        }}
        h2 {{
            color: #00d4ff;
            font-size: 1.5em;
            margin: 30px 0 15px 0;
            border-bottom: 1px solid #2a3f5f;
            padding-bottom: 10px;
        }}
        h3 {{
            color: #00d4ff;
            font-size: 1.2em;
            margin: 20px 0 10px 0;
        }}
        h4, h5, h6 {{
            color: #00d4ff;
            margin: 15px 0 10px 0;
        }}
        p {{
            color: #ffffff;
            margin-bottom: 15px;
        }}
        strong {{
            color: #00d4ff;
            font-weight: 600;
        }}
        ul {{
            margin: 15px 0;
            padding-left: 30px;
        }}
        li {{
            color: #ffffff;
            margin-bottom: 8px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            background-color: #0a0e27;
            font-size: 0.9em;
            color: #ffffff;
        }}
        thead tr {{
            background-color: #1a1f3a !important;
        }}
        th {{
            background-color: #1a1f3a;
            color: #00d4ff;
            padding: 12px;
            text-align: left;
            border: 1px solid #2a3f5f;
            font-weight: 600;
        }}
        td {{
            color: #ffffff !important;
            padding: 12px;
            text-align: left;
            border: 1px solid #2a3f5f;
            background-color: transparent !important;
        }}
        tbody tr {{
            background-color: #0a0e27;
        }}
        tbody tr:nth-child(even) {{
            background-color: #0f1429;
        }}
        tbody tr:hover {{
            background-color: #1a2a4a;
        }}
        code {{
            background-color: #1a1f3a;
            color: #00d4ff;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
        }}
        hr {{
            border: none;
            border-top: 1px solid #2a3f5f;
            margin: 30px 0;
        }}
        em {{
            color: #8b9dc3;
        }}
    </style>
</head>
<body>
{html_content}
</body>
</html>"""
    
    # 保存
    if output_file is None:
        input_path = Path(input_file)
        output_file = input_path.parent / f"{input_path.stem}.html"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(full_html)
    
    print(f"[SUCCESS] Converted to HTML: {output_file}")
    return output_file

def main():
    if len(sys.argv) < 2:
        print("Usage: python md_to_html_converter.py <input_md_file> [output_html_file]")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    md_to_html(input_file, output_file)

if __name__ == "__main__":
    main()
