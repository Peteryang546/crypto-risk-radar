#!/usr/bin/env python3
"""
API History Generator
Creates historical JSON API endpoints for programmatic access
"""

import json
import os
from datetime import datetime
from pathlib import Path

OUTPUT_DIR = Path(r'F:\stepclaw\agents\blockchain-analyst\output')
API_DIR = OUTPUT_DIR / 'api' / 'history'


def generate_api_index():
    """Generate API index with all available endpoints"""
    
    # Find all history files
    history_files = sorted(API_DIR.glob('*.json')) if API_DIR.exists() else []
    
    api_index = {
        'name': 'Crypto Risk Radar API',
        'version': '1.0',
        'description': 'Historical blockchain risk data API',
        'base_url': 'https://peteryang546.github.io/crypto-risk-radar/api/',
        'endpoints': {
            'latest': '/output/latest.json',
            'history_index': '/api/index.json',
            'history_by_date': '/api/history/{YYYY-MM-DD}.json',
            'history_range': '/api/history/range?start={date}&end={date}',
        },
        'available_dates': [f.stem for f in history_files[-30:]],  # Last 30 days
        'total_reports': len(history_files),
        'last_updated': datetime.now().isoformat(),
        'documentation': 'https://peteryang546.github.io/crypto-risk-radar/api/docs.html',
    }
    
    return api_index


def save_api_index():
    """Save API index to file"""
    API_DIR.mkdir(parents=True, exist_ok=True)
    
    index = generate_api_index()
    index_path = OUTPUT_DIR / 'api' / 'index.json'
    
    with open(index_path, 'w', encoding='utf-8') as f:
        json.dump(index, f, indent=2, ensure_ascii=False)
    
    print(f"[OK] API index saved: {index_path}")
    return index_path


def copy_latest_to_history(report_data: dict, timestamp: str):
    """Copy current report to history archive"""
    API_DIR.mkdir(parents=True, exist_ok=True)
    
    # Extract date from timestamp
    date_str = timestamp[:10]  # YYYY-MM-DD
    
    # Save with date-based filename
    history_path = API_DIR / f"{date_str}.json"
    
    with open(history_path, 'w', encoding='utf-8') as f:
        json.dump(report_data, f, indent=2, ensure_ascii=False)
    
    print(f"[OK] History saved: {history_path}")
    return history_path


def generate_api_docs():
    """Generate API documentation HTML"""
    
    docs_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Crypto Risk Radar API Documentation</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; max-width: 900px; margin: 0 auto; padding: 20px; line-height: 1.6; }
        h1 { color: #1a1a2e; border-bottom: 2px solid #00d4ff; padding-bottom: 10px; }
        h2 { color: #16213e; margin-top: 30px; }
        code { background: #f4f4f4; padding: 2px 6px; border-radius: 3px; font-family: 'Courier New', monospace; }
        pre { background: #1a1a2e; color: #00d4ff; padding: 15px; border-radius: 8px; overflow-x: auto; }
        .endpoint { background: #f8f9fa; padding: 15px; margin: 15px 0; border-left: 4px solid #00d4ff; }
        .method { color: #fff; background: #00d4ff; padding: 3px 8px; border-radius: 3px; font-size: 12px; font-weight: bold; }
        .url { color: #16213e; font-weight: bold; }
    </style>
</head>
<body>
    <h1>🔴 Crypto Risk Radar API</h1>
    <p>Programmatic access to blockchain risk monitoring data. Updated every 8 hours.</p>
    
    <h2>Base URL</h2>
    <code>https://peteryang546.github.io/crypto-risk-radar/</code>
    
    <h2>Endpoints</h2>
    
    <div class="endpoint">
        <span class="method">GET</span> <span class="url">/output/latest.json</span>
        <p>Get the latest report data in JSON format.</p>
        <pre>curl https://peteryang546.github.io/crypto-risk-radar/output/latest.json</pre>
    </div>
    
    <div class="endpoint">
        <span class="method">GET</span> <span class="url">/api/index.json</span>
        <p>Get API metadata and available dates.</p>
        <pre>curl https://peteryang546.github.io/crypto-risk-radar/api/index.json</pre>
    </div>
    
    <div class="endpoint">
        <span class="method">GET</span> <span class="url">/api/history/{YYYY-MM-DD}.json</span>
        <p>Get historical report data for a specific date.</p>
        <pre>curl https://peteryang546.github.io/crypto-risk-radar/api/history/2026-04-14.json</pre>
    </div>
    
    <h2>Response Format</h2>
    <pre>{
  "timestamp": "2026-04-14T08:25:00",
  "btc_price": 74507.00,
  "btc_change_24h": 4.99,
  "eth_price": 2368.00,
  "eth_change_24h": 7.97,
  "risk_score": 35,
  "risk_level": "Low",
  "market_sentiment": "Neutral",
  "threats_detected": 2,
  "dormant_addresses": 0,
  "token_unlocks": 10,
  "high_risk_tokens": 5,
  "data_sources": [...],
  "report_url": "https://peteryang546.github.io/crypto-risk-radar/"
}</pre>
    
    <h2>Rate Limits</h2>
    <p>This is a static API hosted on GitHub Pages. Please be respectful:</p>
    <ul>
        <li>Cache responses locally</li>
        <li>Don't poll more than once per hour</li>
        <li>Use /api/index.json to check available dates</li>
    </ul>
    
    <h2>Data License</h2>
    <p>Data is provided for educational and research purposes. See <a href="https://github.com/peteryang546/crypto-risk-radar">GitHub repository</a> for license details.</p>
    
    <h2>Support</h2>
    <p>For issues or feature requests, please open an issue on <a href="https://github.com/peteryang546/crypto-risk-radar/issues">GitHub</a>.</p>
    
    <p style="margin-top: 40px; padding-top: 20px; border-top: 1px solid #eee; color: #666; font-size: 12px;">
        Last updated: 2026-04-14 | Crypto Risk Radar API v1.0
    </p>
</body>
</html>"""
    
    docs_path = OUTPUT_DIR / 'api' / 'docs.html'
    docs_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(docs_path, 'w', encoding='utf-8') as f:
        f.write(docs_html)
    
    print(f"[OK] API docs saved: {docs_path}")
    return docs_path


if __name__ == "__main__":
    print("="*70)
    print("GENERATING API HISTORY & DOCUMENTATION")
    print("="*70)
    
    # Generate API index
    save_api_index()
    
    # Generate API docs
    generate_api_docs()
    
    print("\n" + "="*70)
    print("API endpoints:")
    print("  /api/index.json - API metadata")
    print("  /api/history/YYYY-MM-DD.json - Historical data")
    print("  /api/docs.html - Documentation")
    print("="*70)
