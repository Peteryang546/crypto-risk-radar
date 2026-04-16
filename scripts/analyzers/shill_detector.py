#!/usr/bin/env python3
"""
Shill-to-Dump Detector
Analyzes on-chain evidence for KOL shill events
"""

import json
import sys
from datetime import datetime, timedelta
from typing import Dict, List, Any
from collections import defaultdict

sys.path.insert(0, r'F:\stepclaw\agents\blockchain-analyst')
from config import USE_MOCK_DATA, ETHERSCAN_API_KEY


class ShillDetector:
    """Detect pump-and-dump patterns around KOL shills"""
    
    def __init__(self, use_mock_data=False):
        self.use_mock_data = use_mock_data
        self.suspicious_patterns = []
    
    def analyze_shill_event(self, shill: Dict) -> Dict:
        """
        Analyze a shill event for pump-and-dump evidence
        Returns evidence summary
        """
        token = shill.get("tokens", [""])[0] if shill.get("tokens") else ""
        shill_time = shill.get("time", datetime.now().isoformat())
        
        evidence = {
            "shill": shill,
            "token": token,
            "pre_shill_wallets": [],
            "post_shill_transfers": [],
            "price_action": {},
            "risk_score": 0,
            "conclusion": ""
        }
        
        if self.use_mock_data:
            # Generate mock evidence
            evidence["pre_shill_wallets"] = [
                {
                    "wallet": "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb5",
                    "type": "new",
                    "age_days": 3,
                    "buy_amount_usd": 25000,
                    "time_before_shill_hours": 2
                },
                {
                    "wallet": "0x8ba1fb1c8b2c0b8f1a2c3d4e5f6a7b8c9d0e1f2a",
                    "type": "dormant",
                    "age_days": 450,
                    "buy_amount_usd": 40000,
                    "time_before_shill_hours": 4
                }
            ]
            evidence["post_shill_transfers"] = [
                {
                    "wallet": "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb5",
                    "to_exchange": "Binance",
                    "amount_usd": 20000,
                    "time_after_shill_hours": 1
                }
            ]
            evidence["price_action"] = {
                "change_30min": 22,
                "change_1h": 18,
                "change_6h": -8,
                "change_24h": -25,
                "peak_price": 0.045,
                "current_price": 0.029
            }
            evidence["risk_score"] = 94
            evidence["conclusion"] = "Clear insider buying before shill, followed by rapid transfer to exchange. Classic pump and dump."
        else:
            # Real implementation would query Etherscan API
            # For now, return empty evidence
            evidence["conclusion"] = "On-chain analysis requires token contract address and Etherscan API integration."
        
        return evidence
    
    def calculate_risk_score(self, evidence: Dict) -> int:
        """Calculate risk score (0-100) for a shill event"""
        score = 0
        
        # Pre-shill suspicious wallets (40%)
        pre_wallets = evidence.get("pre_shill_wallets", [])
        if len(pre_wallets) > 0:
            score += 20
            for w in pre_wallets:
                if w.get("type") == "dormant":
                    score += 10
                if w.get("buy_amount_usd", 0) > 30000:
                    score += 10
        
        # Post-shill transfers to exchanges (30%)
        post_transfers = evidence.get("post_shill_transfers", [])
        if len(post_transfers) > 0:
            score += 30
        
        # Price action (30%)
        price = evidence.get("price_action", {})
        if price.get("change_30min", 0) > 20:
            score += 10
        if price.get("change_24h", 0) < -20:
            score += 20
        
        return min(score, 100)
    
    def generate_evidence_report(self, evidence: Dict) -> str:
        """Generate detailed markdown report for a shill event"""
        shill = evidence.get("shill", {})
        token = evidence.get("token", "UNKNOWN")
        risk_score = evidence.get("risk_score", 0)
        
        # Risk level emoji
        if risk_score >= 80:
            risk_emoji = "🔴"
            risk_level = "Extreme"
        elif risk_score >= 60:
            risk_emoji = "🟠"
            risk_level = "High"
        elif risk_score >= 40:
            risk_emoji = "🟡"
            risk_level = "Medium"
        else:
            risk_emoji = "🟢"
            risk_level = "Low"
        
        md = f"""## {risk_emoji} SHILL ALERT: ${token} by @{shill.get('username', 'Unknown')}

**Shill Time**: {shill.get('time', 'Unknown')[:16]} UTC  
**KOL Followers**: {shill.get('followers', 'Unknown')}  
**Shill Text**: "{shill.get('text', 'N/A')[:100]}..."  
**Original Post**: [{shill.get('link', 'Link')}]({shill.get('link', '#')})

### On-Chain Evidence
"""
        
        # Pre-shill wallets
        pre_wallets = evidence.get("pre_shill_wallets", [])
        if pre_wallets:
            md += """
| Time | Event | Wallet | Amount | Type |
|------|-------|--------|--------|------|
"""
            for w in pre_wallets:
                wallet_short = w['wallet'][:20] + "..."
                md += f"| {w['time_before_shill_hours']}h before | Buy | `{wallet_short}` | ${w['buy_amount_usd']:,} | {w['type']} ({w['age_days']}d) |\n"
        else:
            md += "\n*No suspicious pre-shill wallet activity detected.*\n"
        
        # Post-shill transfers
        post_transfers = evidence.get("post_shill_transfers", [])
        if post_transfers:
            md += """
### Post-Shill Transfers
| Time | From | To | Amount |
|------|------|-----|--------|
"""
            for t in post_transfers:
                wallet_short = t['wallet'][:20] + "..."
                md += f"| {t['time_after_shill_hours']}h after | `{wallet_short}` | {t['to_exchange']} | ${t['amount_usd']:,} |\n"
        
        # Price action
        price = evidence.get("price_action", {})
        if price:
            md += f"""
### Price Action
| Period | Change | Status |
|--------|--------|--------|
| +30min | {price.get('change_30min', 0):+.0f}% | {'🚀 Pump' if price.get('change_30min', 0) > 10 else 'Normal'} |
| +1h | {price.get('change_1h', 0):+.0f}% | {'🚀 Pump' if price.get('change_1h', 0) > 10 else 'Normal'} |
| +6h | {price.get('change_6h', 0):+.0f}% | {'📉 Dump' if price.get('change_6h', 0) < -5 else 'Normal'} |
| +24h | {price.get('change_24h', 0):+.0f}% | {'📉 Dump' if price.get('change_24h', 0) < -10 else 'Normal'} |

**Peak Price**: ${price.get('peak_price', 0):.4f}  
**Current Price**: ${price.get('current_price', 0):.4f}
"""
        
        # Conclusion
        md += f"""
### Risk Assessment
**Score**: {risk_score}/100 ({risk_level})  
**Conclusion**: {evidence.get('conclusion', 'No conclusion available.')}

**Recommendation**: {'🚨 AVOID - Clear pump and dump pattern' if risk_score >= 80 else '⚠️ CAUTION - Suspicious activity detected' if risk_score >= 60 else '✅ No significant red flags'}

---
*Methodology: [How we detect shills](https://github.com/peteryang546/crypto-risk-radar/blob/main/METHODOLOGY.md)*
"""
        
        return md
    
    def analyze_all_shills(self, shills: List[Dict]) -> List[Dict]:
        """Analyze all shill events"""
        results = []
        for shill in shills:
            evidence = self.analyze_shill_event(shill)
            evidence["risk_score"] = self.calculate_risk_score(evidence)
            results.append(evidence)
        return results


def main():
    """Test the detector"""
    print("="*70)
    print("SHILL-TO-DUMP DETECTOR")
    print("="*70)
    
    # Mock shill event
    mock_shill = {
        "username": "CryptoGuru",
        "text": "Just found the next 100x gem! $MOON token is going to explode!",
        "time": datetime.now().isoformat(),
        "tokens": ["MOON"],
        "followers": 520000
    }
    
    detector = ShillDetector(use_mock_data=True)
    evidence = detector.analyze_shill_event(mock_shill)
    
    print(detector.generate_evidence_report(evidence))


if __name__ == "__main__":
    main()
