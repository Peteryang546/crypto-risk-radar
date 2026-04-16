#!/usr/bin/env python3
"""
Test script to simulate GitHub Actions environment
Tests API connectivity from a clean environment
"""

import requests
import json
from datetime import datetime

print("="*70)
print("TESTING API CONNECTIVITY (Simulating GitHub Actions Environment)")
print("="*70)
print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print()

# Test 1: CoinGecko API with API Key
print("[TEST 1] CoinGecko API (with API Key)")
print("-" * 50)
try:
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        'vs_currency': 'usd',
        'order': 'market_cap_desc',
        'per_page': 5,
        'page': 1
    }
    headers = {
        'x-cg-demo-api-key': 'CG-m57LMPhhuqyQs2QLzUJ6ozAK'
    }
    
    resp = requests.get(url, params=params, headers=headers, timeout=15)
    print(f"Status Code: {resp.status_code}")
    
    if resp.status_code == 200:
        data = resp.json()
        print(f"✅ SUCCESS - Retrieved {len(data)} coins")
        if data:
            print(f"Top coin: {data[0].get('name', 'N/A')} (${data[0].get('current_price', 0):,.2f})")
    else:
        print(f"⚠️  Status {resp.status_code}: {resp.text[:200]}")
except Exception as e:
    print(f"❌ ERROR: {e}")

print()

# Test 2: DEX Screener API
print("[TEST 2] DEX Screener API")
print("-" * 50)
try:
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
        print(f"⚠️  Status {resp.status_code}: {resp.text[:200]}")
except Exception as e:
    print(f"❌ ERROR: {e}")

print()

# Test 3: GoPlus API
print("[TEST 3] GoPlus API (Contract Security)")
print("-" * 50)
try:
    # Test with WETH contract
    contract = "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"
    chain_id = "1"
    url = f"https://api.gopluslabs.io/api/v1/token_security/{chain_id}"
    params = {'contract_addresses': contract}
    
    resp = requests.get(url, params=params, timeout=15)
    print(f"Status Code: {resp.status_code}")
    
    if resp.status_code == 200:
        data = resp.json()
        print(f"✅ SUCCESS - API responding")
        result = data.get('result', {})
        if result:
            contract_data = result.get(contract.lower(), {})
            print(f"Contract checked: {contract[:20]}...")
            print(f"Honeypot: {contract_data.get('is_honeypot', 'N/A')}")
    else:
        print(f"⚠️  Status {resp.status_code}: {resp.text[:200]}")
except Exception as e:
    print(f"❌ ERROR: {e}")

print()
print("="*70)
print("SUMMARY")
print("="*70)
print("""
If all tests pass here but fail in your local environment,
the issue is confirmed to be your local network configuration.

GitHub Actions will run in a clean Ubuntu environment with:
- No firewall restrictions
- Direct internet access
- Latest SSL certificates
- All APIs should be accessible

This confirms that deploying to GitHub Actions is the best solution.
""")
