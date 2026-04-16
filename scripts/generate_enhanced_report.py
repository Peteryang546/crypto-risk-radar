#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
增强版报告生成器 v6.2
集成新模块：高风险代币观察列表、代币解锁预警
"""

import os
import sys
import json
from datetime import datetime
from pathlib import Path

# 添加项目路径
sys.path.insert(0, r'F:\stepclaw\agents\blockchain-analyst')

# 导入模块
try:
    from modules.high_risk_watchlist import HighRiskWatchlist
    from modules.token_unlock_alert import TokenUnlockAlert
    from modules.contract_scanner import ContractScanner
    from modules.chart_generator import ChartGenerator
    MODULES_AVAILABLE = True
except ImportError as e:
    print(f"[WARNING] Modules not available: {e}")
    MODULES_AVAILABLE = False

# 路径配置
BASE_DIR = Path(__file__).parent.parent
OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def generate_enhanced_report(use_demo_data=True):
    """
    生成增强版报告，包含新模块
    
    Args:
        use_demo_data: 是否使用演示数据
        
    Returns:
        dict: 包含各模块内容的字典
    """
    print("=" * 70)
    print("ENHANCED REPORT GENERATOR v6.2")
    print("=" * 70)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    report_data = {
        'timestamp': datetime.now().isoformat(),
        'modules': {}
    }
    
    if not MODULES_AVAILABLE:
        print("[ERROR] Required modules not available")
        return report_data
    
    # Module 1: 高风险代币观察列表
    print("\n" + "-" * 70)
    print("MODULE 1: High-Risk Token Watchlist")
    print("-" * 70)
    
    try:
        watchlist = HighRiskWatchlist(use_demo_data=use_demo_data)
        risk_tokens = watchlist.scan_high_risk_tokens(min_score=50, max_results=10)
        
        report_data['modules']['high_risk_watchlist'] = {
            'status': 'success',
            'count': len(risk_tokens),
            'markdown': watchlist.generate_markdown(risk_tokens),
            'html': watchlist.generate_html(risk_tokens),
            'data': risk_tokens
        }
        
        print(f"[SUCCESS] Found {len(risk_tokens)} high-risk tokens")
        
    except Exception as e:
        print(f"[ERROR] High-risk watchlist failed: {e}")
        report_data['modules']['high_risk_watchlist'] = {
            'status': 'error',
            'error': str(e)
        }
    
    # Module 2: 代币解锁预警
    print("\n" + "-" * 70)
    print("MODULE 2: Token Unlock Alert")
    print("-" * 70)
    
    try:
        unlock_alert = TokenUnlockAlert(use_demo_data=use_demo_data)
        unlocks = unlock_alert.get_unlock_alerts(days=7, min_usd=1_000_000, max_results=10)
        
        report_data['modules']['token_unlock_alert'] = {
            'status': 'success',
            'count': len(unlocks),
            'markdown': unlock_alert.generate_markdown(unlocks),
            'html': unlock_alert.generate_html(unlocks),
            'data': unlocks
        }
        
        print(f"[SUCCESS] Found {len(unlocks)} token unlocks")
        
    except Exception as e:
        print(f"[ERROR] Token unlock alert failed: {e}")
        report_data['modules']['token_unlock_alert'] = {
            'status': 'error',
            'error': str(e)
        }
    
    # Module 3: 合约安全检测
    print("\n" + "-" * 70)
    print("MODULE 3: Contract Security Scanner")
    print("-" * 70)
    
    try:
        scanner = ContractScanner(use_demo_data=use_demo_data)
        
        # 扫描一些示例合约（实际使用时可以从高风险列表中获取）
        test_contracts = [
            ('0x1234567890abcdef1234567890abcdef12345678', 'ethereum'),
            ('0xabcdef1234567890abcdef1234567890abcdef12', 'bsc'),
            ('0x9876543210fedcba9876543210fedcba98765432', 'ethereum')
        ]
        
        scan_results = scanner.scan_multiple(test_contracts)
        
        report_data['modules']['contract_scanner'] = {
            'status': 'success',
            'count': len(scan_results),
            'markdown': scanner.generate_markdown(scan_results),
            'html': scanner.generate_html(scan_results),
            'data': scan_results
        }
        
        print(f"[SUCCESS] Scanned {len(scan_results)} contracts")
        
    except Exception as e:
        print(f"[ERROR] Contract scanner failed: {e}")
        report_data['modules']['contract_scanner'] = {
            'status': 'error',
            'error': str(e)
        }
    
    # Module 4: 链上数据可视化
    print("\n" + "-" * 70)
    print("MODULE 4: Chart Generator")
    print("-" * 70)
    
    try:
        chart_gen = ChartGenerator(use_demo_data=use_demo_data)
        charts = chart_gen.generate_all_charts()
        
        report_data['modules']['chart_generator'] = {
            'status': 'success',
            'charts': list(charts.keys()),
            'html': charts
        }
        
        print(f"[SUCCESS] Generated {len(charts)} charts")
        
    except Exception as e:
        print(f"[ERROR] Chart generator failed: {e}")
        report_data['modules']['chart_generator'] = {
            'status': 'error',
            'error': str(e)
        }
    
    # 保存报告数据
    output_file = OUTPUT_DIR / f"enhanced_report_{datetime.now().strftime('%Y%m%d_%H%M')}.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(report_data, f, indent=2, ensure_ascii=False)
    
    print("\n" + "=" * 70)
    print("REPORT GENERATION COMPLETE")
    print("=" * 70)
    print(f"Output file: {output_file}")
    
    return report_data


def generate_combined_markdown(report_data):
    """
    生成合并的 Markdown 报告
    
    Args:
        report_data: 报告数据字典
        
    Returns:
        str: 合并的 Markdown 报告
    """
    md = f"""# Crypto Risk Radar - Enhanced Report

**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}
**Version**: v6.2 (Enhanced)

---

"""
    
    # 添加高风险代币观察列表
    if report_data['modules'].get('high_risk_watchlist', {}).get('status') == 'success':
        md += report_data['modules']['high_risk_watchlist']['markdown']
        md += "\n\n---\n\n"
    
    # 添加代币解锁预警
    if report_data['modules'].get('token_unlock_alert', {}).get('status') == 'success':
        md += report_data['modules']['token_unlock_alert']['markdown']
        md += "\n\n---\n\n"
    
    # 添加合约安全检测
    if report_data['modules'].get('contract_scanner', {}).get('status') == 'success':
        md += report_data['modules']['contract_scanner']['markdown']
        md += "\n\n---\n\n"
    
    return md


def generate_combined_html(report_data):
    """
    生成合并的 HTML 报告
    
    Args:
        report_data: 报告数据字典
        
    Returns:
        str: 合并的 HTML 报告
    """
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Crypto Risk Radar - Enhanced Report</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background-color: #0a0e27;
            color: #ffffff;
            line-height: 1.6;
            padding: 20px;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}
        h1 {{
            color: #00d4ff;
            text-align: center;
            margin-bottom: 10px;
        }}
        .meta {{
            text-align: center;
            color: #8b9dc3;
            margin-bottom: 30px;
        }}
        .section {{
            background-color: #1a1f3a;
            border-radius: 12px;
            padding: 25px;
            margin-bottom: 25px;
            border: 1px solid #2a3f5f;
        }}
        h2 {{
            color: #00d4ff;
            margin-bottom: 15px;
            padding-bottom: 10px;
            border-bottom: 1px solid #2a3f5f;
        }}
        h3 {{
            color: #00d4ff;
            margin: 20px 0 10px 0;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 15px 0;
            background-color: #0a0e27;
        }}
        th {{
            background-color: #1a1f3a;
            color: #00d4ff;
            padding: 12px;
            text-align: left;
            border: 1px solid #2a3f5f;
        }}
        td {{
            color: #ffffff;
            padding: 12px;
            border: 1px solid #2a3f5f;
        }}
        tr:hover {{
            background-color: #0f1429;
        }}
        code {{
            background-color: #0a0e27;
            padding: 2px 6px;
            border-radius: 4px;
            font-family: monospace;
            color: #00d4ff;
        }}
        a {{
            color: #00d4ff;
            text-decoration: none;
        }}
        a:hover {{
            text-decoration: underline;
        }}
        ul {{
            margin: 10px 0 10px 20px;
        }}
        li {{
            margin: 5px 0;
        }}
        .risk-item, .unlock-item {{
            background-color: #0f1429;
            padding: 15px;
            border-radius: 8px;
            margin: 10px 0;
            border-left: 3px solid #00d4ff;
        }}
        hr {{
            border: none;
            border-top: 1px solid #2a3f5f;
            margin: 30px 0;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 Crypto Risk Radar - Enhanced Report</h1>
        <p class="meta">Generated: {datetime.now().strftime('%Y-%m-%d %H:%M UTC')} | Version: v6.2</p>
        
        <hr>
"""
    
    # 添加图表生成器（市场概览）
    if report_data['modules'].get('chart_generator', {}).get('status') == 'success':
        charts = report_data['modules']['chart_generator']['html']
        if 'overview' in charts:
            html += charts['overview']
        if 'netflow' in charts:
            html += f'<div class="section">{charts["netflow"]}</div>'
    
    # 添加高风险代币观察列表
    if report_data['modules'].get('high_risk_watchlist', {}).get('status') == 'success':
        html += report_data['modules']['high_risk_watchlist']['html']
    
    # 添加代币解锁预警
    if report_data['modules'].get('token_unlock_alert', {}).get('status') == 'success':
        html += report_data['modules']['token_unlock_alert']['html']
    
    # 添加合约安全检测
    if report_data['modules'].get('contract_scanner', {}).get('status') == 'success':
        html += report_data['modules']['contract_scanner']['html']
    
    html += """
    </div>
</body>
</html>
"""
    
    return html


def main():
    """主函数"""
    # 生成增强版报告
    report_data = generate_enhanced_report(use_demo_data=True)
    
    # 生成合并报告
    print("\n" + "-" * 70)
    print("Generating combined reports...")
    print("-" * 70)
    
    # Markdown
    md_content = generate_combined_markdown(report_data)
    md_file = OUTPUT_DIR / f"enhanced_report_{datetime.now().strftime('%Y%m%d_%H%M')}.md"
    with open(md_file, 'w', encoding='utf-8') as f:
        f.write(md_content)
    print(f"[SUCCESS] Markdown report: {md_file}")
    
    # HTML
    html_content = generate_combined_html(report_data)
    html_file = OUTPUT_DIR / f"enhanced_report_{datetime.now().strftime('%Y%m%d_%H%M')}.html"
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"[SUCCESS] HTML report: {html_file}")
    
    print("\n" + "=" * 70)
    print("ALL REPORTS GENERATED SUCCESSFULLY")
    print("=" * 70)
    
    return report_data


if __name__ == "__main__":
    main()
