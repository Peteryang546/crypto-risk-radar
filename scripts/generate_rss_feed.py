#!/usr/bin/env python3
"""
Generate RSS Feed
Creates RSS feed for report updates
"""

import os
import json
from datetime import datetime
from pathlib import Path


def generate_rss_feed(reports_dir: str = r'F:\stepclaw\agents\blockchain-analyst\output', 
                      output_path: str = r'F:\stepclaw\agents\blockchain-analyst\output\feed.xml',
                      base_url: str = 'https://peteryang546.github.io/crypto-risk-radar'):
    """Generate RSS feed for reports"""
    
    # Get all HTML reports
    reports_path = Path(reports_dir)
    html_files = sorted(reports_path.glob('enhanced_report_*.html'), reverse=True)[:20]  # Last 20
    
    # RSS Header
    rss_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
<channel>
    <title>Crypto Risk Radar</title>
    <link>{base_url}/</link>
    <description>Automated 8-hourly blockchain risk monitoring and analysis</description>
    <language>en</language>
    <lastBuildDate>{datetime.now().strftime('%a, %d %b %Y %H:%M:%S +0000')}</lastBuildDate>
    <atom:link href="{base_url}/feed.xml" rel="self" type="application/rss+xml" />
    <image>
        <url>{base_url}/logo.png</url>
        <title>Crypto Risk Radar</title>
        <link>{base_url}/</link>
    </image>
'''
    
    # Add items
    for f in html_files:
        # Extract date from filename
        parts = f.stem.split('_')
        if len(parts) >= 4:
            date_str = parts[2]  # YYYYMMDD
            time_str = parts[3]  # HHMM
            
            year = date_str[:4]
            month = date_str[4:6]
            day = date_str[6:8]
            hour = time_str[:2]
            minute = time_str[2:]
            
            pub_date = datetime(int(year), int(month), int(day), int(hour), int(minute))
            pub_date_rss = pub_date.strftime('%a, %d %b %Y %H:%M:%S +0000')
            
            report_url = f"{base_url}/reports/{f.name}"
            
            # Try to extract summary from report
            summary = "New risk monitoring report available."
            try:
                content = f.read_text(encoding='utf-8', errors='ignore')
                # Extract risk score from content
                if 'Risk Score' in content:
                    summary = "Updated risk analysis with latest market data and security scans."
            except:
                pass
            
            rss_content += f'''
    <item>
        <title>Crypto Risk Radar - {year}-{month}-{day} {hour}:{minute} ET</title>
        <link>{report_url}</link>
        <guid isPermaLink="true">{report_url}</guid>
        <pubDate>{pub_date_rss}</pubDate>
        <description><![CDATA[
            <p>Automated blockchain risk monitoring report for {year}-{month}-{day}.</p>
            <p>{summary}</p>
            <p><a href="{report_url}">View Full Report</a></p>
        ]]></description>
        <category>Blockchain</category>
        <category>Crypto</category>
        <category>Risk Analysis</category>
    </item>
'''
    
    # RSS Footer
    rss_content += '''
</channel>
</rss>
'''
    
    # Write file
    output_file = Path(output_path)
    output_file.write_text(rss_content, encoding='utf-8')
    
    print(f"[OK] RSS feed generated: {output_path}")
    print(f"[INFO] Feed URL: {base_url}/feed.xml")
    print(f"[INFO] Items: {len(html_files)}")
    
    return output_path


if __name__ == "__main__":
    generate_rss_feed()
