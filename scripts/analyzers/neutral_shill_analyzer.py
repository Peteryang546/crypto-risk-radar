#!/usr/bin/env python3
"""
Neutral Shill Pattern Analyzer
Presents on-chain observations without moral judgment
Focuses on "what happened" rather than "who is guilty"
"""

import json
import sys
from datetime import datetime, timedelta
from typing import Dict, List, Any

sys.path.insert(0, r'F:\stepclaw\agents\blockchain-analyst')
from config import USE_MOCK_DATA


class NeutralShillAnalyzer:
    """Analyze patterns neutrally - observation, not accusation"""
    
    def __init__(self, use_mock_data=False):
        self.use_mock_data = use_mock_data
    
    def analyze_pattern(self, event: Dict) -> Dict:
        """
        Analyze token activity patterns after social media mentions
        Returns neutral observation data
        """
        token = event.get("token", "UNKNOWN")
        mention_time = event.get("mention_time", datetime.now().isoformat())
        source = event.get("source", "Unknown")
        
        observation = {
            "token": token,
            "mention_source": source,
            "mention_time": mention_time,
            "on_chain_activity": [],
            "price_pattern": {},
            "historical_similarity": 0,
            "observation_notes": ""
        }
        
        if self.use_mock_data:
            # Generate neutral observation data
            observation["on_chain_activity"] = [
                {
                    "time_offset": "-2h",
                    "event": "Large buy order",
                    "wallet_age": "3 days",
                    "amount_usd": 25000,
                    "tx_hash": "0xabc...123"
                },
                {
                    "time_offset": "+1h",
                    "event": "Transfer to exchange",
                    "destination": "Binance",
                    "amount_usd": 20000,
                    "tx_hash": "0xdef...456"
                }
            ]
            
            observation["price_pattern"] = {
                "change_30min": 22,
                "change_1h": 18,
                "change_6h": -8,
                "change_24h": -25,
                "peak_time": "+30min",
                "pattern_type": "Rapid rise followed by decline"
            }
            
            observation["historical_similarity"] = 94  # Similarity to historical patterns
            observation["observation_notes"] = "Pattern observed: Significant on-chain activity preceded social media mention, followed by price volatility."
        
        return observation
    
    def generate_neutral_report(self, observations: List[Dict]) -> str:
        """Generate neutral, observation-focused report"""
        if not observations:
            return """### On-Chain Pattern Observations

**Status**: No significant token activity patterns detected in the last 12 hours.

*This section monitors for correlations between social media mentions and subsequent on-chain activity.*
"""
        
        md = """### On-Chain Pattern Observations

**Note**: The following observations document sequences of events. Correlation does not imply causation. Always conduct independent verification.

"""
        
        for obs in observations:
            token = obs.get("token", "UNKNOWN")
            similarity = obs.get("historical_similarity", 0)
            source = obs.get("mention_source", "Unknown")
            
            md += f"""#### {token} - Temporal Activity Pattern

**Social Media Mention**: @{source} at {obs.get('mention_time', 'N/A')[:16]} UTC

**On-Chain Activity Timeline**:
| Time | Event | Details |
|------|-------|---------|
"""
            
            for activity in obs.get("on_chain_activity", []):
                details = f"${activity.get('amount_usd', 0):,}"
                if activity.get('wallet_age'):
                    details += f" (Wallet age: {activity['wallet_age']})"
                if activity.get('destination'):
                    details += f" → {activity['destination']}"
                md += f"| {activity.get('time_offset', 'N/A')} | {activity.get('event', 'N/A')} | {details} |\n"
            
            price = obs.get("price_pattern", {})
            md += f"""
**Price Movement**:
- 30 minutes: {price.get('change_30min', 0):+.1f}%
- 1 hour: {price.get('change_1h', 0):+.1f}%
- 6 hours: {price.get('change_6h', 0):+.1f}%
- 24 hours: {price.get('change_24h', 0):+.1f}%

**Pattern Similarity**: {similarity}% (compared to historical post-promotion patterns)

**Observation**: {obs.get('observation_notes', 'N/A')}

**Data Sources**: 
- On-chain: Etherscan, BSCScan
- Price: Binance API
- Time reference: UTC

---
"""
        
        return md
    
    def generate_correlation_table(self, sources: List[Dict]) -> str:
        """Generate correlation analysis table"""
        md = """### Social Media - On-Chain Activity Correlation Analysis

**Methodology**: This analysis measures the temporal correlation between social media mentions of tokens and subsequent on-chain transactions. A high correlation score indicates that similar patterns have been observed historically, not that manipulation has occurred.

| Source | Mentions (30d) | Avg Price Change (24h) | Correlation Score | Pattern Type |
|--------|----------------|------------------------|-------------------|--------------|
"""
        
        for source in sources:
            change = source.get("avg_24h_change", 0)
            change_emoji = "📉" if change < -10 else "📈" if change > 5 else "➡️"
            md += f"| @{source.get('username', 'N/A')} | {source.get('mentions', 0)} | {change_emoji} {change:+.1f}% | {source.get('correlation', 0)}% | {source.get('pattern', 'N/A')} |\n"
        
        md += """
**Interpretation**:
- **Correlation Score**: Percentage of mentions followed by similar price patterns within 24 hours
- **Pattern Type**: Description of observed price movement sequence
- **Note**: High correlation does not prove causation. Markets are influenced by many factors.

**Limitations**:
- Analysis is based on publicly available data
- Cannot account for all market variables
- Patterns may occur due to normal market activity
- Always verify independently before making decisions
"""
        
        return md
    
    def generate_self_protection_guide(self) -> str:
        """Generate neutral self-protection guide"""
        return """## Self-Protection Guide: How to Verify Token Promotions

**Purpose**: This guide provides steps to independently verify information before making investment decisions. It is educational content, not financial advice.

### Step 1: Check On-Chain Data
- [ ] Verify token contract on Etherscan or BSCScan
- [ ] Check if liquidity is locked (look for LP tokens burned or time-locked)
- [ ] Review holder distribution (avoid tokens where top 5 wallets hold >50%)

### Step 2: Analyze Timing
- [ ] Check if there were large transactions before the promotion
- [ ] Look for wallet age: new wallets making large buys may indicate coordinated activity
- [ ] Review transaction patterns in the 24 hours before and after mentions

### Step 3: Price Action Verification
- [ ] Wait 24 hours after a promotional tweet before considering entry
- [ ] Set stop-losses at -10% to -15% if you do enter
- [ ] Take partial profits quickly if price rises rapidly

### Step 4: Contract Safety
- [ ] Use honeypot detection tools before interacting with new contracts
- [ ] Check if contract is verified and open-source
- [ ] Look for functions like "blacklist" or "mint" that could be abused

### Step 5: General Risk Management
- [ ] Never invest more than you can afford to lose completely
- [ ] Diversify across multiple tokens, not just one "opportunity"
- [ ] Keep records of your research process for future reference

### Red Flags Checklist
**Not definitive proof, but worth extra caution**:
- [ ] Token has no locked liquidity
- [ ] Top wallet holds >20% of supply
- [ ] Contract is not verified
- [ ] Large buys from wallets created within 7 days
- [ ] Immediate transfers to exchanges after price rise
- [ ] No clear project documentation or team information

### Remember
- **DYOR**: Do Your Own Research
- **Correlation ≠ Causation**: Patterns don't prove manipulation
- **Markets are Complex**: Many factors influence prices
- **No Guarantees**: Even careful analysis can be wrong

---

*This guide is for educational purposes. Not financial advice.*
"""


def main():
    """Test neutral analyzer"""
    print("="*70)
    print("NEUTRAL SHILL PATTERN ANALYZER")
    print("="*70)
    
    analyzer = NeutralShillAnalyzer(use_mock_data=True)
    
    mock_event = {
        "token": "MOON",
        "mention_source": "CryptoGuru",
        "mention_time": datetime.now().isoformat()
    }
    
    obs = analyzer.analyze_pattern(mock_event)
    print(analyzer.generate_neutral_report([obs]))
    print("\n" + analyzer.generate_self_protection_guide())


if __name__ == "__main__":
    main()
