#!/usr/bin/env python3
"""
Test API connections with configured keys
测试配置好的 API 连接
"""

import sys
import requests
import json
from datetime import datetime

sys.path.insert(0, r'F:\stepclaw\agents\blockchain-analyst')

from config import COINGECKO_API_KEY
from token_research_framework import TokenResearcher

print("="*70)
print("API CONNECTION TEST WITH CONFIGURED KEYS")
print("="*70)
print(f"Test Time: {datetime.now().isoformat()}")
print()

# Test 1: CoinGecko API
print("-"*70)
print("[TEST 1] CoinGecko API")
print("-"*70)
try:
    headers = {"x-cg-pro-api-key": COINGECKO_API_KEY}
    response = requests.get(
        "https://api.coingecko.com/api/v3/simple/price",
        headers=headers,
        params={
            "ids": "bitcoin,ethereum",
            "vs_currencies": "usd",
            "include_24hr_change": "true"
        },
        timeout=30
    )
    if response.status_code == 200:
        data = response.json()
        btc_price = data.get('bitcoin', {}).get('usd', 'N/A')
        eth_price = data.get('ethereum', {}).get('usd', 'N/A')
        print(f"[OK] Connected successfully")
        print(f"     BTC: ${btc_price}")
        print(f"     ETH: ${eth_price}")
    else:
        print(f"[ERR] Status code: {response.status_code}")
        print(f"      Response: {response.text[:200]}")
except Exception as e:
    print(f"[ERR] {e}")

print()

# Test 2: DEX Screener API
print("-"*70)
print("[TEST 2] DEX Screener API")
print("-"*70)
try:
    response = requests.get(
        "https://api.dexscreener.com/latest/dex/tokens/0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
        timeout=30
    )
    if response.status_code == 200:
        data = response.json()
        pairs = data.get('pairs', [])
        print(f"[OK] Connected successfully")
        print(f"     Found {len(pairs)} pairs")
        if pairs:
            first = pairs[0]
            print(f"     First pair: {first.get('baseToken', {}).get('symbol', 'N/A')}")
            print(f"     Price: ${first.get('priceUsd', 'N/A')}")
    else:
        print(f"[ERR] Status code: {response.status_code}")
except Exception as e:
    print(f"[ERR] {e}")

print()

# Test 3: GoPlus Security API
print("-"*70)
print("[TEST 3] GoPlus Security API")
print("-"*70)
try:
    researcher = TokenResearcher()  # Uses configured key
    # Test with a known token (UNI)
    test_address = "0x1f9840a85d5af5bf1d1762f925bdaddc4201f984"
    
    # Direct API test
    url = f"https://api.gopluslabs.io/api/v1/token_security/1/{test_address}"
    headers = {}
    if researcher.goplus_api_key:
        headers["Authorization"] = f"Bearer {researcher.goplus_api_key}"
    
    response = requests.get(url, headers=headers, timeout=30)
    print(f"[INFO] Status code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        if data.get('code') == 1:
            result = data.get('result', {})
            print(f"[OK] Connected successfully")
            print(f"     Token: {result.get('token_name', 'N/A')}")
            print(f"     Honeypot: {result.get('is_honeypot', 'N/A')}")
        else:
            print(f"[WARN] API returned code: {data.get('code')}")
            print(f"       Message: {data.get('message', 'N/A')}")
    else:
        print(f"[ERR] Status code: {response.status_code}")
        print(f"      Response: {response.text[:200]}")
except Exception as e:
    print(f"[ERR] {e}")

print()

# Test 4: Fear & Greed Index
print("-"*70)
print("[TEST 4] Fear & Greed Index API")
print("-"*70)
try:
    response = requests.get(
        "https://api.alternative.me/fng/?limit=1",
        timeout=30
    )
    if response.status_code == 200:
        data = response.json()
        fng_data = data.get('data', [{}])[0]
        print(f"[OK] Connected successfully")
        print(f"     Value: {fng_data.get('value', 'N/A')}")
        print(f"     Classification: {fng_data.get('value_classification', 'N/A')}")
    else:
        print(f"[ERR] Status code: {response.status_code}")
except Exception as e:
    print(f"[ERR] {e}")

print()
print("="*70)
print("TEST COMPLETE")
print("="*70)
