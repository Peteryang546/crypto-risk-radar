#!/usr/bin/env python3
"""
Upload all historical reports to GitHub Pages root directory
Ensures archive page links work correctly
"""

import sys
import base64
import requests
from pathlib import Path

sys.path.insert(0, r'F:\stepclaw\agents\blockchain-analyst')
from config import GITHUB_TOKEN

REPO_OWNER = "peteryang546"
REPO_NAME = "crypto-risk-radar"
OUTPUT_DIR = Path(r'F:\stepclaw\agents\blockchain-analyst\output')


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
    except:
        pass
    
    # Prepare upload data
    data = {
        "message": commit_msg,
        "content": base64.b64encode(content.encode('utf-8')).decode('utf-8'),
    }
    if sha:
        data["sha"] = sha
    
    # Upload
    try:
        resp = requests.put(url, headers=headers, json=data, timeout=30)
        if resp.status_code in [200, 201]:
            print(f"  [OK] Uploaded: {file_path}")
            return True
        else:
            print(f"  [FAIL] {resp.status_code}: {resp.text[:200]}")
            return False
    except Exception as e:
        print(f"  [ERROR] {e}")
        return False


def main():
    """Upload all reports to root directory"""
    print("="*70)
    print("UPLOADING ALL HISTORICAL REPORTS TO ROOT")
    print("="*70)
    
    # Get all HTML reports
    reports = list(OUTPUT_DIR.glob('enhanced_report_*.html'))
    reports.sort(key=lambda x: x.stat().st_mtime, reverse=True)
    
    print(f"\nFound {len(reports)} reports to upload")
    
    success_count = 0
    for i, report in enumerate(reports, 1):
        print(f"\n[{i}/{len(reports)}] Uploading {report.name}...")
        
        with open(report, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if upload_to_github(report.name, content, f"Archive: {report.name}"):
            success_count += 1
    
    print("\n" + "="*70)
    print(f"UPLOAD COMPLETE: {success_count}/{len(reports)} reports uploaded")
    print("="*70)
    
    return 0 if success_count == len(reports) else 1


if __name__ == "__main__":
    sys.exit(main())
