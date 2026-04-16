#!/usr/bin/env python3
"""
GoPlus Security API Integration
Fetches real contract security data
"""

import subprocess
import json
from typing import Dict, List


class GoPlusSecurityFetcher:
    """Fetch contract security data from GoPlus API"""
    
    # Chain IDs
    CHAINS = {
        'ethereum': 1,
        'bsc': 56,
        'polygon': 137,
        'arbitrum': 42161,
        'optimism': 10,
        'avalanche': 43114,
        'fantom': 250,
        'base': 8453
    }
    
    def scan_contract(self, contract_address: str, chain_id: int = 1) -> Dict:
        """Scan a contract using GoPlus API via PowerShell"""
        # Use format instead of f-string to avoid variable name conflicts
        ps_template = '''
        try {{
            $url = "https://api.gopluslabs.io/api/v1/token_security/{chain}?contract_addresses={address}"
            $resp = Invoke-RestMethod -Uri $url -TimeoutSec 30
            $resp | ConvertTo-Json -Depth 10
        }} catch {{
            Write-Output "{{`"error`": `"API call failed`"}}"
        }}
        '''
        ps_code = ps_template.format(chain=chain_id, address=contract_address)
        
        try:
            result = subprocess.run(
                ["powershell", "-Command", ps_code],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0:
                data = json.loads(result.stdout)
                return self._parse_security_result(data, contract_address, chain_id)
        except Exception as e:
            import traceback
            print(f"[ERROR] GoPlus scan failed: {e}")
            print(f"[DEBUG] Traceback: {traceback.format_exc()}")
        
        return None
    
    def _parse_security_result(self, data: Dict, address: str, chain_id: int) -> Dict:
        """Parse GoPlus API response"""
        if not data or 'result' not in data:
            return None
        
        result_data = data.get('result', {})
        if address.lower() not in result_data:
            return None
        
        token_data = result_data[address.lower()]
        
        # Extract risk features
        risk_features = []
        is_honeypot = False
        risk_score = 0
        
        # Check for honeypot
        if token_data.get('is_honeypot') == '1':
            is_honeypot = True
            risk_features.append("Honeypot detected")
            risk_score += 50
        
        # Check for anti-whale
        if token_data.get('is_anti_whale') == '1':
            risk_features.append("Anti-whale mechanism")
            risk_score += 20
        
        # Check for blacklist
        if token_data.get('is_blacklisted') == '1':
            risk_features.append("Can blacklist addresses")
            risk_score += 30
        
        # Check for mint function
        if token_data.get('is_mintable') == '1':
            risk_features.append("Owner can mint tokens")
            risk_score += 25
        
        # Check for owner can sell
        if token_data.get('owner_can_sell') == '1':
            risk_features.append("Owner can sell all tokens")
            risk_score += 35
        
        # Check for hidden owner
        if token_data.get('hidden_owner') == '1':
            risk_features.append("Hidden owner")
            risk_score += 30
        
        # Check for self-destruct
        if token_data.get('selfdestruct') == '1':
            risk_features.append("Can self-destruct")
            risk_score += 40
        
        # Check for external call
        if token_data.get('external_call') == '1':
            risk_features.append("External calls detected")
            risk_score += 15
        
        # Check for buy tax
        buy_tax = token_data.get('buy_tax', '0')
        if buy_tax and float(buy_tax) > 10:
            risk_features.append(f"High buy tax: {buy_tax}%")
            risk_score += 15
        
        # Check for sell tax
        sell_tax = token_data.get('sell_tax', '0')
        if sell_tax and float(sell_tax) > 10:
            risk_features.append(f"High sell tax: {sell_tax}%")
            risk_score += 15
        
        # Check for slippage modifiable
        if token_data.get('slippage_modifiable') == '1':
            risk_features.append("Slippage modifiable")
            risk_score += 20
        
        # Check for personal slippage
        if token_data.get('personal_slippage_modifiable') == '1':
            risk_features.append("Personal slippage modifiable")
            risk_score += 25
        
        # Check for transfer pause
        if token_data.get('transfer_pausable') == '1':
            risk_features.append("Transfers can be paused")
            risk_score += 20
        
        # Check for trading cooldown
        if token_data.get('trading_cooldown') == '1':
            risk_features.append("Trading cooldown enabled")
            risk_score += 10
        
        return {
            'token': token_data.get('token_name', 'Unknown'),
            'symbol': token_data.get('token_symbol', 'UNKNOWN'),
            'contract': address,
            'chain_id': chain_id,
            'is_honeypot': is_honeypot,
            'risk_score': min(risk_score, 100),
            'risk_features': risk_features,
            'buy_tax': buy_tax,
            'sell_tax': sell_tax,
            'holder_count': token_data.get('holder_count', 'N/A'),
            'trust_score': 'Low' if risk_score > 50 else 'Medium' if risk_score > 20 else 'High'
        }
    
    def scan_multiple(self, contracts: List[tuple]) -> List[Dict]:
        """Scan multiple contracts"""
        results = []
        print(f"[INFO] Scanning {len(contracts)} contracts with GoPlus...")
        
        for address, chain_id in contracts:
            result = self.scan_contract(address, chain_id)
            if result and result.get('risk_score', 0) > 0:
                results.append(result)
                print(f"  ⚠️ {result['symbol']}: Risk Score {result['risk_score']}/100")
        
        print(f"[OK] Found {len(results)} contracts with risk indicators")
        return results


def test_goplus():
    """Test GoPlus integration"""
    print("="*70)
    print("TESTING GOPLUS SECURITY API")
    print("="*70)
    
    goplus = GoPlusSecurityFetcher()
    
    # Test with known tokens
    test_contracts = [
        ("0xdAC17F958D2ee523a2206206994597C13D831ec7", 1),  # USDT (should be safe)
        ("0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48", 1),  # USDC (should be safe)
    ]
    
    for address, chain in test_contracts:
        print(f"\nScanning {address} on chain {chain}...")
        result = goplus.scan_contract(address, chain)
        if result:
            print(f"  Token: {result['token']} ({result['symbol']})")
            print(f"  Risk Score: {result['risk_score']}/100")
            print(f"  Is Honeypot: {result['is_honeypot']}")
            print(f"  Risk Features: {', '.join(result['risk_features']) if result['risk_features'] else 'None'}")
        else:
            print("  No data returned")
    
    print("\n" + "="*70)


if __name__ == "__main__":
    test_goplus()
