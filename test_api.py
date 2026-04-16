#!/usr/bin/env python3
"""Test real API calls"""
import sys
sys.path.insert(0, r'F:\stepclaw\agents\blockchain-analyst')
sys.path.insert(0, r'F:\stepclaw\agents\blockchain-analyst\modules')

print("="*70)
print("TESTING REAL API CALLS")
print("="*70)

# Test 1: High Risk Watchlist
print("\n[1/4] Testing DEX Screener API...")
try:
    from high_risk_watchlist import HighRiskWatchlist
    w = HighRiskWatchlist(use_demo_data=False)
    pairs = w.fetch_new_pairs(hours=24, limit=20)
    print(f"[OK] Fetched {len(pairs)} pairs")
    if pairs:
        for p in pairs[:3]:
            base = p.get('baseToken', {})
            liq = p.get('liquidity', {}).get('usd', 0)
            print(f"  - {base.get('symbol', 'N/A')}: liquidity=${liq:,.0f}")
except Exception as e:
    print(f"[ERROR] {e}")

# Test 2: Token Unlocks
print("\n[2/4] Testing Token Unlock API...")
try:
    from token_unlock_alert import TokenUnlockAlert
    t = TokenUnlockAlert(use_demo_data=False)
    unlocks = t.fetch_unlocks(days=7)
    print(f"[OK] Fetched {len(unlocks)} unlocks")
    if unlocks:
        for u in unlocks[:3]:
            print(f"  - {u.get('token_symbol', 'N/A')}: ${u.get('unlock_value_usd', 0):,.0f}")
except Exception as e:
    print(f"[ERROR] {e}")

# Test 3: Contract Scanner
print("\n[3/4] Testing GoPlus API...")
try:
    from contract_scanner import ContractScanner
    c = ContractScanner(use_demo_data=False)
    # Test with a known token
    result = c.scan_contract("0xdAC17F958D2ee523a2206206994597C13D831ec7", 1)  # USDT
    if result:
        print(f"[OK] Scanned USDT contract")
        print(f"  - Is honeypot: {result.get('is_honeypot', 'N/A')}")
        print(f"  - Risk features: {result.get('risk_features', [])}")
    else:
        print("[WARNING] No data returned")
except Exception as e:
    print(f"[ERROR] {e}")

# Test 4: Dormant Addresses
print("\n[4/4] Testing Etherscan API...")
try:
    from dormant_address import DormantAddressMonitor
    d = DormantAddressMonitor()
    # Just check if API key is set
    from config import ETHERSCAN_API_KEY
    if ETHERSCAN_API_KEY:
        print("[OK] Etherscan API key is configured")
    else:
        print("[ERROR] Etherscan API key not set")
except Exception as e:
    print(f"[ERROR] {e}")

print("\n" + "="*70)
print("API TEST COMPLETE")
print("="*70)
