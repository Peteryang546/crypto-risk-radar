#!/usr/bin/env python3
"""
Crypto Risk Radar - SEO/GEO Publisher
生成带完整 SEO 标签的 HTML 报告并更新 sitemap.xml
"""

import os
import sys
import json
import re
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path

# 站点配置
SITE_URL = "https://peteryang546.github.io/crypto-risk-radar"
SITEMAP_PATH = "sitemap.xml"

def extract_data_from_report(report_content):
    """从报告内容中提取关键数据"""
    data = {
        'date': datetime.now().strftime('%Y-%m-%d'),
        'score': '0.00',
        'grade': 'Neutral',
        'netflow': '0',
        'whale': '0',
        'scam': 'None detected',
        'fear': '50'
    }
    
    # 提取日期
    date_match = re.search(r'Data as of[^:]*:\s*(\w+\s+\d+,\s*\d{4})', report_content)
    if date_match:
        date_str = date_match.group(1)
        try:
            parsed = datetime.strptime(date_str, '%B %d, %Y')
            data['date'] = parsed.strftime('%Y-%m-%d')
        except:
            pass
    
    # 提取量化得分
    score_match = re.search(r'Final Score[^:]*:\s*([+-]?\d+\.\d+)', report_content)
    if score_match:
        data['score'] = score_match.group(1)
    
    # 提取等级
    grade_match = re.search(r'Grade[^:]*:\s*\[?([^\]]+)\]?', report_content)
    if grade_match:
        data['grade'] = grade_match.group(1).strip()
    
    # 提取净流入
    netflow_match = re.search(r'On-chain netflow[^:]*:\s*([+-]?[\d,]+)\s*BTC', report_content)
    if netflow_match:
        data['netflow'] = netflow_match.group(1).replace(',', '')
    
    # 提取巨鲸持仓
    whale_match = re.search(r'Whale holdings[^:]*:\s*([+-]?\d+\.?\d*)%', report_content)
    if whale_match:
        data['whale'] = whale_match.group(1)
    
    # 提取恐惧指数
    fear_match = re.search(r'Fear[^&]*&[^:]*:\s*(\d+)', report_content)
    if fear_match:
        data['fear'] = fear_match.group(1)
    
    # 提取骗局信息
    scam_match = re.search(r'Confirmed Honeypots[^\n]*\n[^\n]*<td>([^<]+)</td>', report_content)
    if scam_match:
        data['scam'] = scam_match.group(1).strip()
    
    return data

def generate_seo_html(report_content, data, output_path):
    """生成带完整 SEO 标签的 HTML"""
    
    date = data['date']
    score = data['score']
    grade = data['grade']
    netflow = data['netflow']
    whale = data['whale']
    scam = data['scam']
    fear = data['fear']
    
    # 构建描述
    description = f"Quant score {score}/2.0 ({grade}). 7d exchange netflow {netflow} BTC, whale holdings {whale}%. Scam alert: {scam}. Fear & Greed: {fear}."
    
    # 构建 JSON-LD - 增强权威性标记
    json_ld = {
        "@context": "https://schema.org",
        "@type": "TechArticle",
        "headline": f"Crypto Risk Radar – {date} | On-Chain Quant Signals",
        "description": description,
        "datePublished": f"{date}T08:10:00+00:00",
        "dateModified": f"{date}T08:10:00+00:00",
        "author": {
            "@type": "Organization",
            "name": "Crypto Risk Radar",
            "url": SITE_URL,
            "logo": {
                "@type": "ImageObject",
                "url": f"{SITE_URL}/og-preview.png"
            }
        },
        "publisher": {
            "@type": "Organization",
            "name": "Crypto Risk Radar",
            "url": SITE_URL,
            "logo": {
                "@type": "ImageObject",
                "url": f"{SITE_URL}/og-preview.png",
                "width": 1200,
                "height": 630
            }
        },
        "mainEntityOfPage": {
            "@type": "WebPage",
            "@id": f"{SITE_URL}/reports/{filename}"
        },
        "image": {
            "@type": "ImageObject",
            "url": f"{SITE_URL}/og-preview.png",
            "width": 1200,
            "height": 630
        },
        "keywords": "Bitcoin, Ethereum, on-chain analysis, quant signals, scam detection, crypto risk, blockchain analytics",
        "articleSection": "Cryptocurrency Risk Analysis",
        "about": {
            "@type": "Thing",
            "name": "Cryptocurrency Market Risk Assessment",
            "description": "Quantitative analysis of Bitcoin and Ethereum on-chain metrics including exchange flows, whale movements, and scam detection"
        },
        "proficiencyLevel": "Expert",
        "dependencies": "On-chain data from Glassnode, DeFi Llama, and CoinGecko APIs",
        "isAccessibleForFree": True,
        "license": "https://creativecommons.org/licenses/by-nc/4.0/",
        "inLanguage": "en-US",
        "audience": {
            "@type": "Audience",
            "audienceType": "Cryptocurrency investors, traders, and analysts"
        }
    }
    
    filename = os.path.basename(output_path)
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
    <meta http-equiv="Pragma" content="no-cache">
    <meta http-equiv="Expires" content="0">
    
    <!-- 基础 SEO -->
    <title>Crypto Risk Radar – {date} | On-Chain Quant Signals</title>
    <meta name="description" content="{description}">
    <meta name="keywords" content="crypto risk radar, on-chain analysis, bitcoin quant signals, exchange netflow, whale holdings, scam detection, fear and greed index">
    <meta name="author" content="Crypto Risk Radar">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="{SITE_URL}/reports/{filename}">
    
    <!-- Open Graph -->
    <meta property="og:title" content="Crypto Risk Radar – {date}">
    <meta property="og:description" content="Quant {score} | Netflow {netflow} BTC | Fear {fear}">
    <meta property="og:type" content="article">
    <meta property="og:url" content="{SITE_URL}/reports/{filename}">
    <meta property="og:image" content="{SITE_URL}/og-preview.png">
    <meta property="og:site_name" content="Crypto Risk Radar">
    <meta property="og:locale" content="en_US">
    
    <!-- Twitter Card -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="Crypto Risk Radar – {date}">
    <meta name="twitter:description" content="Quant {score} | Netflow {netflow} BTC">
    <meta name="twitter:image" content="{SITE_URL}/og-preview.png">
    
    <!-- Structured Data - TechArticle -->
    <script type="application/ld+json">
{json.dumps(json_ld, indent=2)}
    </script>
    
    <!-- Structured Data - Report (增强AI理解) -->
    <script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "Report",
  "name": "Crypto Risk Radar – {date}",
  "description": "{description}",
  "url": "{SITE_URL}/reports/{filename}",
  "datePublished": "{date}T08:10:00+00:00",
  "author": {{
    "@type": "Organization",
    "name": "Crypto Risk Radar"
  }},
  "publisher": {{
    "@type": "Organization",
    "name": "Crypto Risk Radar",
    "url": "{SITE_URL}"
  }},
  "about": {{
    "@type": "Thing",
    "name": "Bitcoin and Ethereum Market Analysis"
  }},
  "temporalCoverage": "P12H",
  "spatialCoverage": "Global Cryptocurrency Markets",
  "variableMeasured": [
    "Exchange Netflow",
    "Whale Holdings",
    "Fear and Greed Index",
    "Scam Detection Score"
  ]
}}
    </script>
    
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background-color: #0a0e27;
            color: #ffffff;
            line-height: 1.6;
            padding: 20px;
        }}
        .report-content {{
            max-width: 1200px;
            margin: 0 auto;
            background-color: #1a1f3a;
            border-radius: 12px;
            padding: 30px;
            border: 1px solid #2a3f5f;
        }}
        h1, h2, h3 {{
            color: #00d4ff;
            margin: 20px 0 15px 0;
        }}
        h1 {{ font-size: 2em; text-align: center; margin-bottom: 20px; }}
        h2 {{ font-size: 1.5em; border-bottom: 1px solid #2a3f5f; padding-bottom: 10px; }}
        h3 {{ font-size: 1.2em; }}
        p {{ color: #ffffff; margin-bottom: 15px; }}
        strong {{ color: #00d4ff; }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            background-color: #0a0e27;
            color: #ffffff;
        }}
        thead tr {{ background-color: #1a1f3a !important; }}
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
        tbody tr {{ background-color: #0a0e27; }}
        tbody tr:nth-child(even) {{ background-color: #0f1429; }}
        tbody tr:hover {{ background-color: #1a2a4a; }}
        ul {{ margin: 15px 0; padding-left: 30px; }}
        li {{ color: #ffffff; margin-bottom: 8px; }}
        a {{ color: #00d4ff; text-decoration: none; }}
        .history-section {{
            max-width: 1200px;
            margin: 30px auto;
            background-color: #1a1f3a;
            border-radius: 12px;
            padding: 30px;
            border: 1px solid #2a3f5f;
        }}
        .history-section h2 {{ color: #00d4ff; margin-bottom: 20px; }}
        .history-section ul {{ list-style: none; padding: 0; }}
        .history-section li {{ padding: 10px 0; border-bottom: 1px solid #2a3f5f; }}
        .history-section li:last-child {{ border-bottom: none; }}
        .history-section a {{ color: #ffffff; font-size: 1.1em; }}
        .history-section a:hover {{ color: #00d4ff; }}
        .footer {{
            text-align: center;
            padding: 40px 20px;
            color: #ffffff;
            margin-top: 40px;
            font-size: 0.9em;
        }}
    </style>
</head>
<body>
    <div class="report-content">
        {report_content}
    </div>
    
    <div class="history-section">
        <h2>📊 Report History</h2>
        <ul>
            <li><a href="{filename}">{date} - Latest Report</a></li>
        </ul>
        <p style="color: #8b9dc3; margin-top: 15px;">
            View all reports in the <a href="https://github.com/peteryang546/crypto-risk-radar/tree/main/reports">reports folder</a>
        </p>
    </div>
    
    <div class="footer">
        <p>Generated by StepClaw AI Agent | Updated every 12 hours</p>
        <p>Data sources: Binance, CoinGecko, DeFi Llama, DEX Screener</p>
        <p><a href="{SITE_URL}">View on GitHub</a></p>
    </div>
</body>
</html>"""
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"[SUCCESS] SEO HTML generated: {output_path}")
    return True

def update_sitemap(date, filename):
    """更新 sitemap.xml"""
    # sitemap 将在 GitHub 仓库根目录创建
    # 这里我们生成 sitemap 内容，由 github_publisher.py 上传
    url = f"{SITE_URL}/reports/{filename}"
    
    sitemap_entry = f"""  <url>
    <loc>{url}</loc>
    <lastmod>{date}</lastmod>
    <changefreq>never</changefreq>
    <priority>0.8</priority>
  </url>
"""
    return sitemap_entry

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate SEO-enhanced HTML report")
    parser.add_argument("--input", required=True, help="Input HTML file path")
    parser.add_argument("--output", required=True, help="Output HTML file path")
    
    args = parser.parse_args()
    
    # 读取输入文件
    with open(args.input, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 提取数据
    data = extract_data_from_report(content)
    print(f"[INFO] Extracted data: {data}")
    
    # 生成 SEO HTML
    generate_seo_html(content, data, args.output)
    
    # 生成 sitemap 条目
    sitemap_entry = update_sitemap(data['date'], os.path.basename(args.output))
    print(f"[INFO] Sitemap entry generated")
    
    # 保存 sitemap 条目到临时文件
    sitemap_temp = args.output + '.sitemap_entry.txt'
    with open(sitemap_temp, 'w', encoding='utf-8') as f:
        f.write(sitemap_entry)
    print(f"[SUCCESS] Sitemap entry saved: {sitemap_temp}")

if __name__ == "__main__":
    main()
