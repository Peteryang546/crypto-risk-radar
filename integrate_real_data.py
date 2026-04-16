#!/usr/bin/env python3
"""
Real Data Integration Module
Integrates real data crawlers into the report generation pipeline
"""

import sys
import json
from datetime import datetime
from pathlib import Path

sys.path.insert(0, r'F:\stepclaw\agents\blockchain-analyst')
sys.path.insert(0, r'F:\stepclaw\agents\blockchain-analyst\modules')
sys.path.insert(0, r'F:\stepclaw\agents\blockchain-analyst\scripts\crawlers')

from config import USE_MOCK_DATA, ETHERSCAN_API_KEY

class RealDataIntegrator:
    """Integrates real data sources into report generation"""
    
    def __init__(self, use_demo_data=False):
        self.use_demo_data = use_demo_data
        self.data = {}
        
    def fetch_high_risk_tokens(self):
        """Fetch real high-risk tokens from DEX Screener"""
        try:
            from high_risk_watchlist import HighRiskWatchlist
            watchlist = HighRiskWatchlist(use_demo_data=self.use_demo_data)
            pairs = watchlist.fetch_new_pairs(hours=24, limit=50)
            
            # Convert pairs to risk token format
            tokens = []
            for pair in pairs:
                risk_score, risk_factors = watchlist.calculate_risk_score(pair)
                if risk_score >= 70:  # Only high risk tokens
                    base = pair.get('baseToken', {})
                    tokens.append({
                        'token': base.get('symbol', 'UNKNOWN'),
                        'name': base.get('name', 'Unknown'),
                        'price': float(pair.get('priceUsd', 0)),
                        'liquidity': pair.get('liquidity', {}).get('usd', 0),
                        'holders': pair.get('txns', {}).get('h24', {}).get('buys', 0) + pair.get('txns', {}).get('h24', {}).get('sells', 0),
                        'owner_percent': 0,  # Not available from DEX Screener
                        'risk_score': risk_score,
                        'risk_factors': risk_factors,
                        'chain': pair.get('chainId', 'unknown'),
                        'dex': pair.get('dexId', 'unknown')
                    })
            
            if tokens and len(tokens) > 0:
                print(f"[OK] Fetched {len(tokens)} high-risk tokens from DEX Screener")
                return tokens[:10]  # Limit to top 10
            else:
                print("[INFO] No high-risk tokens found, using fallback")
                return self._fallback_high_risk_tokens()
        except Exception as e:
            print(f"[WARNING] High-risk token fetch failed: {e}")
            return self._fallback_high_risk_tokens()
    
    def fetch_contract_security(self):
        """Fetch real contract security data from GoPlus"""
        try:
            from contract_scanner import ContractScanner
            scanner = ContractScanner(use_demo_data=self.use_demo_data)
            
            # Scan a few known addresses for demonstration
            test_addresses = [
                ("0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb5", 1),  # Ethereum
                ("0x8ba1fb1c8b2c0b8f1a2c3d4e5f6a7b8c9d0e1f2a", 56),  # BSC
            ]
            
            threats = []
            for addr, chain in test_addresses:
                result = scanner.scan_contract(addr, chain)
                if result and result.get('is_honeypot'):
                    threats.append({
                        'token': result.get('token_name', 'Unknown'),
                        'contract': addr,
                        'discovered': datetime.now().strftime('%Y-%m-%d'),
                        'risk_features': result.get('risk_features', []),
                        'status': 'High Risk'
                    })
            
            print(f"[OK] Scanned {len(test_addresses)} contracts, found {len(threats)} threats")
            return threats
        except Exception as e:
            print(f"[WARNING] Contract security fetch failed: {e}")
            return []
    
    def fetch_token_unlocks(self):
        """Fetch real token unlock data"""
        try:
            from token_unlock_alert import TokenUnlockAlert
            alert = TokenUnlockAlert(use_demo_data=self.use_demo_data)
            unlocks = alert.fetch_unlocks(days=7)
            
            # Convert to standard format
            formatted_unlocks = []
            for u in unlocks:
                formatted_unlocks.append({
                    'token': u.get('token_symbol', 'UNKNOWN'),
                    'name': u.get('token_name', 'Unknown'),
                    'unlock_date': u.get('unlock_date', 'N/A'),
                    'amount': u.get('unlock_amount', 0),
                    'value_usd': u.get('unlock_value_usd', 0),
                    'circulating_supply': u.get('circulating_supply', 0),
                    'unlock_percent': u.get('unlock_percent', 0),
                    'category': u.get('category', 'Unknown'),
                    'risk_level': u.get('risk_level', 'Medium')
                })
            
            if formatted_unlocks and len(formatted_unlocks) > 0:
                print(f"[OK] Fetched {len(formatted_unlocks)} token unlock events")
                return formatted_unlocks
            else:
                print("[INFO] No unlock events found, using fallback")
                return self._fallback_token_unlocks()
        except Exception as e:
            print(f"[WARNING] Token unlock fetch failed: {e}")
            return self._fallback_token_unlocks()
    
    def fetch_dormant_addresses(self):
        """Fetch real dormant address activity"""
        try:
            from dormant_address import DormantAddressMonitor
            monitor = DormantAddressMonitor()
            
            # Check a few known whale addresses
            whale_addresses = [
                "0x3f5CE5FBFe3E9af3971dD833D26bA9b5C936f0b",
                "0xdAC17F958D2ee523a2206206994597C13D831ec7",
            ]
            
            active_addresses = []
            for addr in whale_addresses:
                if ETHERSCAN_API_KEY:
                    result = monitor.check_address(addr)
                    if result and result.get('is_active'):
                        active_addresses.append(result)
            
            print(f"[OK] Checked {len(whale_addresses)} addresses, found {len(active_addresses)} active")
            return active_addresses
        except Exception as e:
            print(f"[WARNING] Dormant address fetch failed: {e}")
            return []
    
    def _fallback_high_risk_tokens(self):
        """Fallback data when API fails"""
        return [
            {
                'token': 'API_ERROR',
                'name': 'Data Unavailable',
                'price': 0,
                'liquidity': 0,
                'holders': 0,
                'owner_percent': 0,
                'risk_score': 0,
                'note': 'API temporarily unavailable - check back later'
            }
        ]
    
    def _fallback_token_unlocks(self):
        """Fallback unlock data"""
        return [
            {
                'token': 'API',
                'name': 'Data Unavailable',
                'unlock_date': 'N/A',
                'amount': 0,
                'value_usd': 0,
                'note': 'Token unlock API temporarily unavailable'
            }
        ]
    
    def fetch_all_real_data(self):
        """Fetch all real data sources"""
        print("\n" + "="*70)
        print("FETCHING REAL DATA FROM APIs")
        print("="*70)
        
        self.data = {
            'high_risk_tokens': self.fetch_high_risk_tokens(),
            'security_threats': self.fetch_contract_security(),
            'token_unlocks': self.fetch_token_unlocks(),
            'dormant_addresses': self.fetch_dormant_addresses(),
            'fetch_timestamp': datetime.now().isoformat(),
            'data_quality': 'real' if not self.use_demo_data else 'demo'
        }
        
        print("\n" + "="*70)
        print("REAL DATA FETCH SUMMARY")
        print("="*70)
        print(f"High-risk tokens: {len(self.data['high_risk_tokens'])}")
        print(f"Security threats: {len(self.data['security_threats'])}")
        print(f"Token unlocks: {len(self.data['token_unlocks'])}")
        print(f"Dormant addresses: {len(self.data['dormant_addresses'])}")
        print(f"Timestamp: {self.data['fetch_timestamp']}")
        print("="*70)
        
        return self.data


def test_integration():
    """Test the real data integration"""
    print("Testing Real Data Integration...")
    integrator = RealDataIntegrator(use_demo_data=False)
    data = integrator.fetch_all_real_data()
    
    # Save test results
    output_dir = Path(r'F:\stepclaw\agents\blockchain-analyst\output')
    output_dir.mkdir(exist_ok=True)
    
    with open(output_dir / 'real_data_test.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"\n[OK] Test results saved to: {output_dir / 'real_data_test.json'}")
    return data


if __name__ == "__main__":
    test_integration()
