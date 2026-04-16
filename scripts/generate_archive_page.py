#!/usr/bin/env python3
"""
Generate Archive Page
Creates a historical report listing page
"""

import os
import json
from datetime import datetime
from pathlib import Path


def generate_archive_html(reports_dir: str = r'F:\stepclaw\agents\blockchain-analyst\output', output_path: str = r'F:\stepclaw\agents\blockchain-analyst\output\archive.html'):
    """Generate archive page with all historical reports"""
    
    # Get all HTML reports
    reports_path = Path(reports_dir)
    html_files = sorted(reports_path.glob('enhanced_report_*.html'), reverse=True)
    
    # Group by month
    reports_by_month = {}
    for f in html_files:
        # Extract date from filename: enhanced_report_YYYYMMDD_HHMM.html
        date_str = f.stem.split('_')[2]  # YYYYMMDD
        year = date_str[:4]
        month = date_str[4:6]
        day = date_str[6:8]
        
        month_key = f"{year}-{month}"
        if month_key not in reports_by_month:
            reports_by_month[month_key] = []
        
        reports_by_month[month_key].append({
            'filename': f.name,
            'date': f"{year}-{month}-{day}",
            'time': f.stem.split('_')[3] if len(f.stem.split('_')) > 3 else '0000',
            'url': f'./{f.name}'
        })
    
    # Generate HTML
    html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Crypto Risk Radar - Archive</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 100%);
            color: #ffffff;
            min-height: 100vh;
            padding: 40px 20px;
        }}
        .container {{
            max-width: 900px;
            margin: 0 auto;
        }}
        h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
            background: linear-gradient(90deg, #00d4ff, #8b9dc3);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        .subtitle {{
            color: #8b9dc3;
            margin-bottom: 40px;
            font-size: 1.1em;
        }}
        .month-section {{
            margin-bottom: 40px;
        }}
        .month-title {{
            font-size: 1.5em;
            color: #00d4ff;
            margin-bottom: 15px;
            padding-bottom: 10px;
            border-bottom: 1px solid rgba(0, 212, 255, 0.3);
        }}
        .report-list {{
            list-style: none;
        }}
        .report-item {{
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 8px;
            padding: 15px 20px;
            margin-bottom: 10px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            transition: all 0.3s ease;
        }}
        .report-item:hover {{
            background: rgba(0, 212, 255, 0.1);
            border-color: rgba(0, 212, 255, 0.3);
        }}
        .report-date {{
            font-weight: 600;
            color: #ffffff;
        }}
        .report-time {{
            color: #8b9dc3;
            font-size: 0.9em;
        }}
        .report-link {{
            color: #00d4ff;
            text-decoration: none;
            font-weight: 500;
            padding: 8px 16px;
            border: 1px solid #00d4ff;
            border-radius: 4px;
            transition: all 0.3s ease;
        }}
        .report-link:hover {{
            background: #00d4ff;
            color: #0a0e27;
        }}
        .back-link {{
            display: inline-block;
            margin-bottom: 30px;
            color: #8b9dc3;
            text-decoration: none;
        }}
        .back-link:hover {{
            color: #00d4ff;
        }}
        .stats {{
            background: rgba(0, 212, 255, 0.1);
            border: 1px solid rgba(0, 212, 255, 0.3);
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 40px;
        }}
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 20px;
        }}
        .stat-item {{
            text-align: center;
        }}
        .stat-value {{
            font-size: 2em;
            font-weight: bold;
            color: #00d4ff;
        }}
        .stat-label {{
            color: #8b9dc3;
            font-size: 0.9em;
        }}
        footer {{
            margin-top: 60px;
            padding-top: 30px;
            border-top: 1px solid rgba(255, 255, 255, 0.1);
            text-align: center;
            color: #8b9dc3;
            font-size: 0.9em;
        }}
    </style>
</head>
<body>
    <div class="container">
        <a href="./index.html" class="back-link">← Back to Current Report</a>
        
        <h1>📚 Report Archive</h1>
        <p class="subtitle">Historical Crypto Risk Radar reports</p>
        
        <div class="stats">
            <div class="stats-grid">
                <div class="stat-item">
                    <div class="stat-value">{len(html_files)}</div>
                    <div class="stat-label">Total Reports</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value">{len(reports_by_month)}</div>
                    <div class="stat-label">Months</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value">8h</div>
                    <div class="stat-label">Update Frequency</div>
                </div>
            </div>
        </div>
'''
    
    # Add reports by month
    for month_key in sorted(reports_by_month.keys(), reverse=True):
        reports = reports_by_month[month_key]
        month_name = datetime.strptime(month_key, '%Y-%m').strftime('%B %Y')
        
        html_content += f'''
        <div class="month-section">
            <h2 class="month-title">{month_name}</h2>
            <ul class="report-list">
'''
        
        for report in reports:
            time_formatted = f"{report['time'][:2]}:{report['time'][2:]}"
            html_content += f'''
                <li class="report-item">
                    <div>
                        <span class="report-date">{report['date']}</span>
                        <span class="report-time"> at {time_formatted} ET</span>
                    </div>
                    <a href="{report['url']}" class="report-link">View Report</a>
                </li>
'''
        
        html_content += '''
            </ul>
        </div>
'''
    
    html_content += f'''
        <footer>
            <p>Crypto Risk Radar - Automated 8-hourly blockchain risk monitoring</p>
            <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}</p>
        </footer>
    </div>
</body>
</html>
'''
    
    # Write file
    output_file = Path(output_path)
    output_file.write_text(html_content, encoding='utf-8')
    
    print(f"[OK] Archive page generated: {output_path}")
    print(f"[INFO] Total reports: {len(html_files)}")
    print(f"[INFO] Months covered: {len(reports_by_month)}")
    
    return output_path


if __name__ == "__main__":
    generate_archive_html()
