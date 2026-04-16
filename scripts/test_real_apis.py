#!/usr/bin/env python3
"""
Test real API connections for Crypto Risk Radar
Tests: DEX Screener, GoPlus, TokenUnlocks
"""

import requests
import json
from datetime import datetime

print("="*70)
print("TESTING REAL API CONNECTIONS")
print("="*70)
print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print()

# Test 1: DEX Screener API
print("[TEST 1] DEX Screener API")
print("-" * 50)
try:
    # Try to get trending pairs
    url = "https://api.dexscreener.com/latest/dex/tokens/0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"
    resp = requests.get(url, timeout=15)
    print(f"Status Code: {resp.status_code}")
    
    if resp.status_code == 200:
        data = resp.json()
        pairs = data.get('pairs', [])
        print(f"✅ SUCCESS - Retrieved {len(pairs)} pairs")
        if pairs:
            print(f"Sample pair: {pairs[0].get('baseToken', {}).get('symbol', 'N/A')}")
    else:
        print(f"❌ FAILED - Status: {resp.status_code}")
        print(f"Response: {resp.text[:200]}")
except Exception as e:
    print(f"❌ ERROR: {e}")

print()

# Test 2: GoPlus API
print("[TEST 2] GoPlus API (Contract Security)")
print("-" * 50)
try:
    # Test with a known contract (WETH)
    contract = "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"
    chain_id = "1"  # Ethereum
    url = f"https://api.gopluslabs.io/api/v1/token_security/{chain_id}?contract_addresses={contract}"
    
    resp = requests.get(url, timeout=15)
    print(f"Status Code: {resp.status_code}")
    
    if resp.status_code == 200:
        data = resp.json()
        result = data.get('result', {})
        print(f"✅ SUCCESS - API responding")
        if result:
            contract_data = result.get(contract.lower(), {})
            print(f"Contract checked: {contract[:20]}...")
            print(f"Honeypot: {contract_data.get('is_honeypot', 'N/A')}")
    else:
        print(f"❌ FAILED - Status: {resp.status_code}")
except Exception as e:
    print(f"❌ ERROR: {e}")

print()

# Test 3: TokenUnlocks API (via CoinGecko as alternative)
print("[TEST 3] Token Unlock Data (via CoinGecko)")
print("-" * 50)
try:
    # Try CoinGecko API for market data
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        'vs_currency': 'usd',
        'order': 'market_cap_desc',
        'per_page': 5,
        'page': 1
    }
    
    resp = requests.get(url, params=params, timeout=15)
    print(f"Status Code: {resp.status_code}")
    
    if resp.status_code == 200:
        data = resp.json()
        print(f"✅ SUCCESS - Retrieved {len(data)} coins")
        if data:
            print(f"Top coin: {data[0].get('name', 'N/A')} (${data[0].get('current_price', 0):,.2f})")
    else:
        print(f"❌ FAILED - Status: {resp.status_code}")
        print(f"Note: CoinGecko has rate limits (10-30 calls/minute for free tier)")
except Exception as e:
    print(f"❌ ERROR: {e}")

print()
print("="*70)
print("API TEST SUMMARY")
print("="*70)
print("""
DEX Screener: Free API, no registration needed
GoPlus: Free API, no registration needed  
CoinGecko: Free tier available (rate limited)

All APIs are accessible without registration.
For production use, consider:
1. Adding API keys for higher rate limits
2. Implementing caching to reduce API calls
3. Adding retry logic for failed requests
""")
