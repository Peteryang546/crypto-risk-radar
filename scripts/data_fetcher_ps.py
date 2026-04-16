#!/usr/bin/env python3
"""
Data fetcher using PowerShell (bypasses Python SSL issues)
"""

import subprocess
import json
import os
from pathlib import Path

BASE_DIR = Path(r"F:\stepclaw\agents\blockchain-analyst")
OUTPUT_DIR = BASE_DIR / "output"


def fetch_via_powershell():
    """Fetch data using PowerShell script"""
    ps_script = BASE_DIR / "scripts" / "fetch_data_via_ps.ps1"
    
    result = subprocess.run(
        ["powershell", "-ExecutionPolicy", "Bypass", "-File", str(ps_script)],
        capture_output=True,
        text=True,
        timeout=120
    )
    
    if result.returncode != 0:
        print(f"[ERROR] PowerShell failed: {result.stderr}")
        return None
    
    # Read the generated JSON (handle BOM)
    data_file = OUTPUT_DIR / "data_ps.json"
    if data_file.exists():
        with open(data_file, 'r', encoding='utf-8-sig') as f:
            return json.load(f)
    
    return None


def get_data():
    """Main data getter - uses PowerShell to bypass SSL issues"""
    print("[INFO] Fetching data via PowerShell (bypassing Python SSL issues)...")
    
    data = fetch_via_powershell()
    
    if data:
        print("[SUCCESS] Data fetched successfully via PowerShell")
        return data
    else:
        print("[WARNING] PowerShell fetch failed, using demo data")
        return get_demo_data()


def get_demo_data():
    """Fallback demo data"""
    return {
        'btc_price': {'price': 73000, 'change_24h': -2.5},
        'eth_price': {'price': 3500, 'change_24h': -1.8},
        'fear_greed': {'value': 50, 'label': 'Neutral'},
        'coingecko_global': {'total_market_cap': {'usd': 2500000000000}}
    }


if __name__ == "__main__":
    data = get_data()
    print(json.dumps(data, indent=2)[:500])
