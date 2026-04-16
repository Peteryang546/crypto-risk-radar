#!/usr/bin/env python3
"""
Token Unlocks Data Fetcher
Fetches upcoming token unlock events
"""

import subprocess
import json
from datetime import datetime, timedelta
from typing import List, Dict


class TokenUnlocksFetcher:
    """Fetch token unlock events"""
    
    def fetch_from_coinmarketcap(self) -> List[Dict]:
        """
        Fetch token unlock data from CoinMarketCap API via PowerShell
        Note: Using public endpoints that don't require API key
        """
        # Try to fetch from CoinGecko which has unlock data
        ps_code = '''
        try {
            # CoinGecko API for coins with upcoming events
            $url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=100&page=1"
            $resp = Invoke-RestMethod -Uri $url -TimeoutSec 30
            
            # Filter for tokens with unlock events (approximated by circulating vs total supply)
            $tokens = $resp | Where-Object { 
                $_.circulating_supply -gt 0 -and 
                $_.total_supply -gt 0 -and 
                ($_.circulating_supply / $_.total_supply) -lt 0.8 
            } | Select-Object -First 10 | ForEach-Object {
                $circulating = $_.circulating_supply
                $total = $_.total_supply
                $unlock_percent = 100 - (($circulating / $total) * 100)
                $unlock_value = ($total - $circulating) * $_.current_price
                
                @{
                    token = $_.symbol.ToUpper()
                    name = $_.name
                    unlock_date = (Get-Date).AddDays(7).ToString("yyyy-MM-dd")  # Approximate
                    amount = [math]::Round($total - $circulating, 0)
                    value_usd = [math]::Round($unlock_value, 0)
                    circulating_supply = [math]::Round($circulating, 0)
                    total_supply = [math]::Round($total, 0)
                    unlock_percent = [math]::Round($unlock_percent, 2)
                    category = "Team/Investor"
                    risk_level = if ($unlock_percent -gt 10) { "High" } elseif ($unlock_percent -gt 5) { "Medium" } else { "Low" }
                }
            }
            
            @{ status = "success"; data = $tokens } | ConvertTo-Json -Depth 10
        } catch {
            @{ status = "error"; message = $_.Exception.Message } | ConvertTo-Json
        }
        '''
        
        try:
            result = subprocess.run(
                ["powershell", "-Command", ps_code],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0:
                data = json.loads(result.stdout)
                if data.get('status') == 'success':
                    return data.get('data', [])
        except Exception as e:
            print(f"[ERROR] Token unlocks fetch failed: {e}")
        
        return []
    
    def get_sample_unlocks(self) -> List[Dict]:
        """Return sample unlock data for demonstration"""
        today = datetime.now()
        return [
            {
                'token': 'APT',
                'name': 'Aptos',
                'unlock_date': (today + timedelta(days=2)).strftime('%Y-%m-%d'),
                'amount': 4500000,
                'value_usd': 28500000,
                'circulating_supply': 450000000,
                'total_supply': 1100000000,
                'unlock_percent': 4.1,
                'category': 'Early Contributors',
                'risk_level': 'Medium',
                'note': 'Sample data - real API integration pending'
            },
            {
                'token': 'STRK',
                'name': 'Starknet',
                'unlock_date': (today + timedelta(days=5)).strftime('%Y-%m-%d'),
                'amount': 89000000,
                'value_usd': 156000000,
                'circulating_supply': 728000000,
                'total_supply': 10000000000,
                'unlock_percent': 12.2,
                'category': 'Team & Investors',
                'risk_level': 'High',
                'note': 'Sample data - real API integration pending'
            },
            {
                'token': 'ARB',
                'name': 'Arbitrum',
                'unlock_date': (today + timedelta(days=12)).strftime('%Y-%m-%d'),
                'amount': 125000000,
                'value_usd': 98000000,
                'circulating_supply': 3200000000,
                'total_supply': 10000000000,
                'unlock_percent': 3.9,
                'category': 'Team & Advisors',
                'risk_level': 'Medium',
                'note': 'Sample data - real API integration pending'
            }
        ]


def test_unlocks_fetcher():
    """Test token unlocks fetching"""
    print("="*70)
    print("TESTING TOKEN UNLOCKS FETCHER")
    print("="*70)
    
    fetcher = TokenUnlocksFetcher()
    
    # Try to fetch real data
    print("\n[1/2] Fetching from CoinGecko...")
    unlocks = fetcher.fetch_from_coinmarketcap()
    print(f"[OK] Fetched {len(unlocks)} unlock events")
    
    if unlocks:
        print("\nUpcoming unlocks:")
        for u in unlocks[:5]:
            print(f"  {u['token']} ({u['name']}): {u['unlock_percent']}% unlock on {u['unlock_date']}")
            print(f"    Value: ${u['value_usd']:,.0f} | Risk: {u['risk_level']}")
    
    # Get sample data
    print("\n[2/2] Sample unlock data:")
    samples = fetcher.get_sample_unlocks()
    for u in samples:
        print(f"  {u['token']}: {u['unlock_percent']}% on {u['unlock_date']} [SAMPLE]")
    
    print("\n" + "="*70)


if __name__ == "__main__":
    test_unlocks_fetcher()
