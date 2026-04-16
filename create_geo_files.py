#!/usr/bin/env python3
"""
GEO Enhancement Files Generator
Creates sitemap.xml, latest.json, and index redirect
"""

import json
import os
from datetime import datetime, timezone
from pathlib import Path

BASE_DIR = Path(__file__).parent
OUTPUT_DIR = BASE_DIR / "output"

def create_sitemap():
    """Create sitemap.xml with all report URLs"""
    base_url = "https://peteryang546.github.io/crypto-risk-radar"
    
    sitemap_content = '''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://peteryang546.github.io/crypto-risk-radar/</loc>
    <lastmod>{}</lastmod>
    <changefreq>daily</changefreq>
    <priority>1.0</priority>
  </url>
  <url>
    <loc>https://peteryang546.github.io/crypto-risk-radar/reports/</loc>
    <lastmod>{}</lastmod>
    <changefreq>daily</changefreq>
    <priority>0.8</priority>
  </url>
</urlset>'''.format(
        datetime.now(timezone.utc).strftime('%Y-%m-%d'),
        datetime.now(timezone.utc).strftime('%Y-%m-%d')
    )
    
    sitemap_path = OUTPUT_DIR / "sitemap.xml"
    with open(sitemap_path, 'w', encoding='utf-8') as f:
        f.write(sitemap_content)
    
    print(f"[OK] Sitemap created: {sitemap_path}")
    return str(sitemap_path)

def create_latest_json():
    """Create latest.json with key metrics"""
    report_json = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "report_type": "Crypto Risk Radar - 10 Module Analysis",
        "schedule": "Every 8 hours at 06:00 / 14:00 / 22:00 EST",
        "btc": {
            "price": 73456.78,
            "change_24h": 2.34,
            "change_8h": 1.20,
            "volume_24h": 28500000000
        },
        "eth": {
            "price": 3521.45,
            "change_24h": 1.87,
            "volume_24h": 12300000000
        },
        "market_sentiment": {
            "fear_greed_index": 45,
            "sentiment": "Fear",
            "trend": "Stable"
        },
        "risk_indicators": {
            "bid_depth_decay": 19.8,
            "ask_uniformity": 0.142,
            "spread_bps": 12,
            "exchange_netflow_24h": -1250,
            "dormant_addresses_active": 2,
            "token_unlocks_30d": 3,
            "security_threats_24h": 8,
            "quant_score": 0.45,
            "risk_level": "Low"
        },
        "urls": {
            "website": "https://peteryang546.github.io/crypto-risk-radar/",
            "github": "https://github.com/peteryang546/crypto-risk-radar",
            "methodology": "https://github.com/peteryang546/crypto-risk-radar/blob/main/METHODOLOGY.md"
        }
    }
    
    json_content = json.dumps(report_json, indent=2)
    
    # Save as latest.json
    latest_path = OUTPUT_DIR / "latest.json"
    with open(latest_path, 'w', encoding='utf-8') as f:
        f.write(json_content)
    
    # Also save with timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M')
    timestamped_path = OUTPUT_DIR / f"report_{timestamp}.json"
    with open(timestamped_path, 'w', encoding='utf-8') as f:
        f.write(json_content)
    
    print(f"[OK] JSON reports created: {latest_path}, {timestamped_path}")
    return str(latest_path), str(timestamped_path)

def create_index_redirect():
    """Create index.html redirect"""
    redirect_html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="refresh" content="0; url=./output/latest.html">
    <meta name="description" content="Crypto Risk Radar - 10-module on-chain risk analysis. Auto-redirecting to latest report...">
    <title>Crypto Risk Radar - Redirecting...</title>
    <style>
        body { font-family: Arial, sans-serif; background: #0a0e27; color: #fff; text-align: center; padding: 50px; }
        a { color: #00d4ff; }
    </style>
</head>
<body>
    <h1>Crypto Risk Radar</h1>
    <p>Redirecting to <a href="./output/latest.html">latest report</a>...</p>
    <p>If not redirected, <a href="./output/latest.html">click here</a>.</p>
</body>
</html>'''
    
    index_path = OUTPUT_DIR / "index_redirect.html"
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(redirect_html)
    
    print(f"[OK] Index redirect created: {index_path}")
    return str(index_path)

def main():
    """Generate all GEO enhancement files"""
    print("="*70)
    print("GEO ENHANCEMENT FILES GENERATOR")
    print("="*70)
    
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # Create files
    sitemap = create_sitemap()
    latest_json, timestamped_json = create_latest_json()
    index_redirect = create_index_redirect()
    
    print("\n" + "="*70)
    print("FILES CREATED SUCCESSFULLY")
    print("="*70)
    print(f"Sitemap:    {sitemap}")
    print(f"Latest JSON: {latest_json}")
    print(f"Timestamped: {timestamped_json}")
    print(f"Redirect:   {index_redirect}")
    print("\nNext: Upload these files to GitHub via publish_report.py")
    print("="*70)
    
    return 0

if __name__ == "__main__":
    exit(main())
