#!/usr/bin/env python3
"""
Orderbook Crawler - Fetches orderbook data via PowerShell (bypasses Python SSL issues)
"""

import subprocess
import json
import time
from typing import Dict, Any
import sys
sys.path.insert(0, r'F:\stepclaw\agents\blockchain-analyst')
from config import USE_MOCK_DATA


def fetch_orderbook(symbol: str = "BTCUSDT") -> Dict[str, Any]:
    """
    Fetch orderbook snapshot using PowerShell to bypass Python SSL issues
    Returns bids, asks, and timestamp
    """
    if USE_MOCK_DATA:
        return {
            "bids": [[50000, 1.2], [49990, 2.5], [49980, 3.0]],
            "asks": [[50010, 0.8], [50020, 1.0], [50030, 1.5]],
            "timestamp": int(time.time() * 1000)
        }
    
    # PowerShell script to fetch Binance orderbook
    ps_code = f'''
    try {{
        $resp = Invoke-RestMethod -Uri "https://api.binance.com/api/v3/depth?symbol={symbol}&limit=20" -TimeoutSec 30
        $resp | ConvertTo-Json -Depth 10
    }} catch {{
        Write-Output "{{`"error`": `"$($_.Exception.Message)`"}}"
    }}
    '''
    
    try:
        result = subprocess.run(
            ["powershell", "-Command", ps_code],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if result.returncode == 0 and result.stdout.strip():
            data = json.loads(result.stdout)
            if "error" in data:
                print(f"[ERROR] PowerShell error: {data['error']}")
                return {"bids": [], "asks": [], "timestamp": 0}
            
            return {
                "bids": [[float(x[0]), float(x[1])] for x in data.get("bids", [])],
                "asks": [[float(x[0]), float(x[1])] for x in data.get("asks", [])],
                "timestamp": data.get("lastUpdateId", int(time.time() * 1000))
            }
    except Exception as e:
        print(f"[ERROR] Failed to fetch orderbook: {e}")
    
    return {"bids": [], "asks": [], "timestamp": 0}


def compute_metrics(ob: Dict) -> Dict[str, Any]:
    """
    Compute metrics from orderbook:
    - total_bid_depth: Sum of all bid quantities
    - ask_uniformity: Coefficient of variation of ask volumes (lower = more suspicious)
    """
    bids = ob.get("bids", [])
    asks = ob.get("asks", [])
    
    # Total bid depth
    total_bid_depth = sum(b[1] for b in bids) if bids else 0
    
    # Ask uniformity: coefficient of variation of top 10 ask volumes
    ask_volumes = [a[1] for a in asks[:10]] if asks else []
    
    if ask_volumes and sum(ask_volumes) > 0:
        mean_vol = sum(ask_volumes) / len(ask_volumes)
        variance = sum((v - mean_vol) ** 2 for v in ask_volumes) / len(ask_volumes)
        ask_uniformity = (variance ** 0.5) / mean_vol if mean_vol > 0 else 1.0
    else:
        ask_uniformity = 1.0
    
    return {
        "total_bid_depth": total_bid_depth,
        "ask_uniformity": ask_uniformity,
        "best_bid": bids[0][0] if bids else 0,
        "best_ask": asks[0][0] if asks else 0,
        "spread": (asks[0][0] - bids[0][0]) if bids and asks else 0
    }


if __name__ == "__main__":
    print("Testing orderbook crawler...")
    ob = fetch_orderbook("BTCUSDT")
    metrics = compute_metrics(ob)
    print(f"Bid depth: {metrics['total_bid_depth']:.2f} BTC")
    print(f"Ask uniformity: {metrics['ask_uniformity']:.3f}")
    print(f"Spread: ${metrics['spread']:.2f}")
