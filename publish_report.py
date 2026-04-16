#!/usr/bin/env python3
"""
Crypto Risk Radar - Manual Report Publisher
Uploads the latest enhanced report to GitHub Pages
"""

import os
import sys
import json
import base64
import requests
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, r'F:\stepclaw\agents\blockchain-analyst')

from config import GITHUB_TOKEN

REPO_OWNER = "peteryang546"
REPO_NAME = "crypto-risk-radar"
BASE_DIR = Path(__file__).parent
OUTPUT_DIR = BASE_DIR / "output"


def upload_to_github(file_path: str, content: str, commit_msg: str) -> bool:
    """Upload file to GitHub via API"""
    if not GITHUB_TOKEN:
        print("[ERROR] GITHUB_TOKEN not set")
        return False
    
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{file_path}"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    # Get existing file SHA if it exists
    sha = None
    try:
        resp = requests.get(url, headers=headers, timeout=30)
        if resp.status_code == 200:
            sha = resp.json().get('sha')
            print(f"  [INFO] File exists, SHA: {sha[:8]}...")
    except Exception as e:
        print(f"  [INFO] New file: {file_path}")
    
    # Prepare upload data
    data = {
        "message": commit_msg,
        "content": base64.b64encode(content.encode('utf-8')).decode('utf-8'),
        "branch": "main"
    }
    if sha:
        data["sha"] = sha
    
    try:
        resp = requests.put(url, headers=headers, json=data, timeout=60)
        if resp.status_code in [200, 201]:
            print(f"  [OK] Uploaded {file_path}")
            return True
        else:
            print(f"  [FAIL] Upload failed: {resp.status_code}")
            print(f"  [FAIL] Response: {resp.text[:300]}")
            return False
    except Exception as e:
        print(f"  [ERROR] Upload exception: {e}")
        return False


def publish_latest_report():
    """Find and publish the latest enhanced report"""
    print("="*70)
    print("PUBLISHING LATEST REPORT TO GITHUB PAGES")
    print("="*70)
    
    # Find latest enhanced report
    reports = list(OUTPUT_DIR.glob("enhanced_report_*.html"))
    if not reports:
        print("[ERROR] No enhanced reports found in output/")
        print("[INFO] Run: python scripts/generate_enhanced_full_report.py")
        return 1
    
    # Sort by modification time (newest first)
    reports.sort(key=lambda x: x.stat().st_mtime, reverse=True)
    latest_report = reports[0]
    
    print(f"[INFO] Latest report: {latest_report.name}")
    
    # Read report content
    with open(latest_report, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    now = datetime.now()
    et_time = now - timedelta(hours=4)  # ET is UTC-4 (simplified)
    
    print(f"[INFO] Report timestamp: {et_time.strftime('%B %d, %Y %H:%M')} ET")
    
    # Upload as index.html (main page)
    print("\n[1/3] Uploading index.html (main page)...")
    success1 = upload_to_github(
        "index.html",
        html_content,
        f"Update report - {et_time.strftime('%Y-%m-%d %H:%M')} ET"
    )
    
    # Also upload to reports archive (both root and reports/ for compatibility)
    archive_name = f"reports/{latest_report.name}"
    print(f"\n[2/3] Uploading to archive: {archive_name}...")
    success2 = upload_to_github(
        archive_name,
        html_content,
        f"Archive report - {et_time.strftime('%Y-%m-%d %H:%M')}"
    )
    
    # Also upload to root for archive page links
    print(f"\n[2b/3] Uploading to root: {latest_report.name}...")
    success2b = upload_to_github(
        latest_report.name,
        html_content,
        f"Archive report (root) - {et_time.strftime('%Y-%m-%d %H:%M')}"
    )
    
    # Update current.md with summary
    summary = f"""# Crypto Risk Radar - Latest Report

**Last Updated**: {et_time.strftime('%B %d, %Y %H:%M')} ET

**View Full Report**: [Click here](https://peteryang546.github.io/crypto-risk-radar/)

## Quick Summary

This report is updated every 8 hours (10:00 PM / 6:00 AM / 2:00 PM EST).

### Report Contents
- Market Overview (BTC/ETH prices, Fear & Greed)
- Orderbook Structure (bid depth, ask uniformity)
- Exchange Netflow (7-day history)
- Dormant Address Activity
- Token Unlock Schedule
- High Risk Token Watchlist
- Contract Security Scanner
- Pattern Observations (neutral analysis)
- Self-Protection Guide
- Market Anomaly Index

### Data Sources
Etherscan, Binance, CoinGecko, DEX Screener, GoPlus Security

---

*This is an automated report. For the full interactive version, visit the link above.*

*© 2026 Crypto Risk Radar - Independent Research Project*
"""
    
    print("\n[3/3] Updating current.md...")
    success3 = upload_to_github(
        "current.md",
        summary,
        f"Update summary - {et_time.strftime('%Y-%m-%d %H:%M')} ET"
    )
    
    # Generate and upload archive page
    print("\n[4/5] Generating and uploading archive page...")
    try:
        sys.path.insert(0, str(BASE_DIR / 'scripts'))
        from generate_archive_page import generate_archive_html
        archive_path = generate_archive_html()
        archive_content = Path(archive_path).read_text(encoding='utf-8')
        success4 = upload_to_github(
            "archive.html",
            archive_content,
            f"Update archive - {et_time.strftime('%Y-%m-%d %H:%M')} ET"
        )
    except Exception as e:
        print(f"  [WARNING] Archive generation failed: {e}")
        success4 = False
    
    # Generate and upload RSS feed
    print("\n[5/5] Generating and uploading RSS feed...")
    try:
        from generate_rss_feed import generate_rss_feed
        rss_path = generate_rss_feed()
        rss_content = Path(rss_path).read_text(encoding='utf-8')
        success5 = upload_to_github(
            "feed.xml",
            rss_content,
            f"Update RSS feed - {et_time.strftime('%Y-%m-%d %H:%M')} ET"
        )
    except Exception as e:
        print(f"  [WARNING] RSS generation failed: {e}")
        success5 = False
    
    # Upload API files
    print("\n[6/8] Generating and uploading API files...")
    try:
        from generate_api_history import save_api_index, generate_api_docs
        api_index_path = save_api_index()
        api_docs_path = generate_api_docs()
        
        api_index_content = Path(api_index_path).read_text(encoding='utf-8')
        success6 = upload_to_github(
            "api/index.json",
            api_index_content,
            f"Update API index - {et_time.strftime('%Y-%m-%d %H:%M')} ET"
        )
        
        api_docs_content = Path(api_docs_path).read_text(encoding='utf-8')
        success7 = upload_to_github(
            "api/docs.html",
            api_docs_content,
            f"Update API docs - {et_time.strftime('%Y-%m-%d %H:%M')} ET"
        )
    except Exception as e:
        print(f"  [WARNING] API generation failed: {e}")
        success6 = success7 = False
    
    # Upload Widget
    print("\n[7/8] Generating and uploading widget...")
    try:
        from generate_widget import save_widget
        widget_path, embed_path = save_widget()
        
        widget_content = Path(widget_path).read_text(encoding='utf-8')
        success8 = upload_to_github(
            "widget.html",
            widget_content,
            f"Update widget - {et_time.strftime('%Y-%m-%d %H:%M')} ET"
        )
    except Exception as e:
        print(f"  [WARNING] Widget generation failed: {e}")
        success8 = False
    
    # Upload health check
    print("\n[8/8] Uploading health check...")
    try:
        health_path = OUTPUT_DIR / 'health.json'
        if health_path.exists():
            health_content = health_path.read_text(encoding='utf-8')
            success9 = upload_to_github(
                "health.json",
                health_content,
                f"Update health - {et_time.strftime('%Y-%m-%d %H:%M')} ET"
            )
        else:
            success9 = False
    except Exception as e:
        print(f"  [WARNING] Health upload failed: {e}")
        success9 = False
    
    # Print results
    print("\n" + "="*70)
    print("PUBLISH RESULTS")
    print("="*70)
    print(f"index.html:     {'[OK] SUCCESS' if success1 else '[FAIL] FAILED'}")
    print(f"Archive:        {'[OK] SUCCESS' if success2 else '[FAIL] FAILED'}")
    print(f"current.md:     {'[OK] SUCCESS' if success3 else '[FAIL] FAILED'}")
    print(f"archive.html:   {'[OK] SUCCESS' if success4 else '[FAIL] FAILED'}")
    print(f"feed.xml:       {'[OK] SUCCESS' if success5 else '[FAIL] FAILED'}")
    print(f"API index:      {'[OK] SUCCESS' if success6 else '[FAIL] FAILED'}")
    print(f"API docs:       {'[OK] SUCCESS' if success7 else '[FAIL] FAILED'}")
    print(f"Widget:         {'[OK] SUCCESS' if success8 else '[FAIL] FAILED'}")
    print(f"Health:         {'[OK] SUCCESS' if success9 else '[FAIL] FAILED'}")
    
    if success1:
        print(f"\nWebsite updated: https://peteryang546.github.io/crypto-risk-radar/")
        print(f"Archive: https://peteryang546.github.io/crypto-risk-radar/archive.html")
        print(f"RSS Feed: https://peteryang546.github.io/crypto-risk-radar/feed.xml")
        print(f"API Docs: https://peteryang546.github.io/crypto-risk-radar/api/docs.html")
        print(f"Widget: https://peteryang546.github.io/crypto-risk-radar/widget.html")
        print(f"\nSchedule (Every 8 hours, 3 times daily):")
        print(f"  ET:  06:00 / 14:00 / 22:00")
        print(f"  CST: 18:00 / 02:00 / 10:00 (北京时间)")
    
    return 0 if success1 else 1


def main():
    """Main entry point"""
    if not GITHUB_TOKEN:
        print("[ERROR] GITHUB_TOKEN environment variable not set!")
        print("[INFO] Set it with: set GITHUB_TOKEN=your_token_here")
        return 1
    
    return publish_latest_report()


if __name__ == "__main__":
    sys.exit(main())
