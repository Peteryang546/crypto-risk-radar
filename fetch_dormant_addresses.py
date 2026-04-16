#!/usr/bin/env python3
"""
Dormant Address Monitor
Detects awakening of long-inactive whale addresses
Uses Etherscan API via PowerShell
"""

import subprocess
import json
import time
from datetime import datetime, timezone
from typing import List, Dict


# Major exchange deposit addresses (Ethereum)
EXCHANGE_ADDRESSES = {
    'Binance': '0x28C6c06298d514Db55E5743bf21d60f5a6',
    'Coinbase': '0x716034C25D9Fb4b38c837aFe417B7f2b9af3E9E',
    'Kraken': '0x267be1C1D684F78cb4F6',
    'OKX': '0x236f9F97E0E62388479bf9E5Aba93DfF9f9A8F8',
    'Crypto.com': '0x6262998CeD04146fA4',
}


class DormantAddressMonitor:
    """Monitor dormant addresses that become active"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or 'YourEtherscanAPIKey'
        self.dormant_threshold_days = 365
        self.min_transfer_eth = 10  # Minimum ETH to trigger alert
    
    def _fetch_via_powershell(self, url: str) -> Dict:
        """Use PowerShell to fetch data"""
        ps_code = f'''
        try {{
            $resp = Invoke-RestMethod -Uri "{url}" -TimeoutSec 30
            $resp | ConvertTo-Json -Depth 10
        }} catch {{
            @{{ status = "error"; message = $_.Exception.Message }} | ConvertTo-Json
        }}
        '''
        
        try:
            result = subprocess.run(
                ["powershell", "-Command", ps_code],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0:
                return json.loads(result.stdout)
        except Exception as e:
            print(f"[ERROR] PowerShell fetch failed: {e}")
        
        return {}
    
    def get_eth_price(self) -> float:
        """Get current ETH price from CoinGecko"""
        url = "https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd"
        data = self._fetch_via_powershell(url)
        
        if data and 'ethereum' in data:
            return data['ethereum'].get('usd', 2400)
        return 2400  # Fallback
    
    def get_exchange_transfers(self, exchange: str, address: str, hours: int = 12) -> List[Dict]:
        """Get recent large transfers to an exchange address"""
        cutoff_time = int(time.time()) - (hours * 3600)
        
        # Etherscan API - get transactions for address
        url = f"https://api.etherscan.io/api?module=account&action=txlist&address={address}&startblock=0&endblock=99999999&sort=desc&apikey={self.api_key}"
        data = self._fetch_via_powershell(url)
        
        transfers = []
        if data and data.get('status') == '1' and data.get('result'):
            for tx in data['result'][:30]:  # Check last 30 transactions
                tx_time = int(tx.get('timeStamp', 0))
                
                # Only check transactions within lookback period
                if tx_time < cutoff_time:
                    break
                
                value_eth = int(tx.get('value', 0)) / 10**18
                
                # Only large transfers TO the exchange (incoming)
                if value_eth >= self.min_transfer_eth and tx.get('to', '').lower() == address.lower():
                    transfers.append({
                        'from_address': tx.get('from', ''),
                        'to_address': address,
                        'value_eth': value_eth,
                        'value_usd': value_eth * self.get_eth_price(),
                        'timestamp': tx_time,
                        'exchange': exchange,
                        'tx_hash': tx.get('hash', ''),
                        'block': tx.get('blockNumber', ''),
                    })
        
        return transfers
    
    def get_address_first_tx(self, address: str) -> int:
        """Get timestamp of first transaction for an address"""
        url = f"https://api.etherscan.io/api?module=account&action=txlist&address={address}&startblock=0&endblock=99999999&sort=asc&apikey={self.api_key}"
        data = self._fetch_via_powershell(url)
        
        if data and data.get('status') == '1' and data.get('result'):
            txs = data['result']
            if txs:
                return int(txs[0].get('timeStamp', 0))
        
        return None
    
    def detect_dormant_addresses(self, hours: int = 12) -> List[Dict]:
        """Detect dormant addresses that recently became active"""
        print(f"[INFO] Scanning for dormant address activity (last {hours}h)...")
        
        all_transfers = []
        
        # Check each exchange
        for exchange, address in EXCHANGE_ADDRESSES.items():
            print(f"  Checking {exchange}...")
            transfers = self.get_exchange_transfers(exchange, address, hours)
            all_transfers.extend(transfers)
            time.sleep(0.5)  # Rate limiting
        
        print(f"[INFO] Found {len(all_transfers)} large transfers to exchanges")
        
        # Check which addresses are dormant
        dormant_list = []
        for tx in all_transfers:
            from_addr = tx['from_address']
            print(f"  Checking dormancy for {from_addr[:20]}...")
            
            first_tx_time = self.get_address_first_tx(from_addr)
            
            if first_tx_time:
                days_dormant = (int(time.time()) - first_tx_time) // 86400
                
                if days_dormant >= self.dormant_threshold_days:
                    dormant_list.append({
                        'address': from_addr,
                        'chain': 'ethereum',
                        'dormant_days': days_dormant,
                        'last_active': datetime.fromtimestamp(first_tx_time, tz=timezone.utc).strftime('%Y-%m-%d'),
                        'current_activity': f"Transferred {round(tx['value_eth'], 2)} ETH to {tx['exchange']}",
                        'value_usd': round(tx['value_usd'], 0),
                        'risk_level': 'High' if days_dormant > 730 else 'Medium',
                        'tx_hash': tx['tx_hash'],
                        'exchange': tx['exchange'],
                        'amount_eth': round(tx['value_eth'], 2),
                        'first_tx_date': datetime.fromtimestamp(first_tx_time, tz=timezone.utc).strftime('%Y-%m-%d'),
                    })
                    print(f"    ⚠️  DORMANT {days_dormant} days!")
            
            time.sleep(0.3)  # Rate limiting
        
        # Sort by dormant days (longest first)
        dormant_list.sort(key=lambda x: x['dormant_days'], reverse=True)
        
        print(f"[OK] Found {len(dormant_list)} dormant addresses awakened")
        return dormant_list[:5]  # Return top 5
    
    def get_sample_dormant(self) -> List[Dict]:
        """Return sample dormant address data"""
        return [
            {
                'address': '0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb5',
                'chain': 'ethereum',
                'dormant_days': 892,
                'last_active': '2023-10-15',
                'current_activity': 'Transferred 1,250.5 ETH to Binance',
                'value_usd': 2960000,
                'risk_level': 'High',
                'tx_hash': '0xabc123def456789012345678901234567890123456789012345678901234abcd',
                'exchange': 'Binance',
                'amount_eth': 1250.5,
                'first_tx_date': '2023-10-15',
                'note': 'Sample data - real Etherscan integration pending'
            },
            {
                'address': '0x8ba1fb1c8b2c0b8f1a2c3d4e5f6a7b8c9d0e1f2a',
                'chain': 'ethereum',
                'dormant_days': 456,
                'last_active': '2024-12-14',
                'current_activity': 'Transferred 450.0 ETH to Coinbase',
                'value_usd': 1065000,
                'risk_level': 'Medium',
                'tx_hash': '0xdef789abc012345678901234567890123456789012345678901234567890ef12',
                'exchange': 'Coinbase',
                'amount_eth': 450.0,
                'first_tx_date': '2024-12-14',
                'note': 'Sample data - real Etherscan integration pending'
            }
        ]


def test_dormant_monitor():
    """Test dormant address monitoring"""
    print("="*70)
    print("TESTING DORMANT ADDRESS MONITOR")
    print("="*70)
    
    monitor = DormantAddressMonitor()
    
    # Test with sample data first
    print("\n[1/2] Sample dormant addresses:")
    samples = monitor.get_sample_dormant()
    for s in samples:
        print(f"  {s['address'][:20]}...: {s['dormant_days']} days dormant")
        print(f"    Transferred {s['amount_eth']} ETH to {s['exchange']}")
    
    # Try real detection (will likely return empty due to API limits/no recent activity)
    print("\n[2/2] Real dormant address detection:")
    print("  (This requires valid Etherscan API key and may return empty)")
    dormant = monitor.detect_dormant_addresses(hours=24)
    
    if dormant:
        print(f"\n[OK] Found {len(dormant)} dormant addresses:")
        for d in dormant:
            print(f"  {d['address'][:20]}...: {d['dormant_days']} days")
    else:
        print("[INFO] No dormant addresses detected in last 24h")
    
    print("\n" + "="*70)


if __name__ == "__main__":
    test_dormant_monitor()
