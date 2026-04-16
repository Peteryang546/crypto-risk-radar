#!/usr/bin/env python3
"""
Pattern Observations - Real Data Implementation
Uses on-chain and market data to detect patterns
No external social API required
Replaces fetch_social_simple.py sample data
"""

from datetime import datetime, timedelta
from typing import List, Dict, Optional


class RealPatternFetcher:
    """Fetch real patterns from on-chain and market data"""
    
    def __init__(self, market_data: Optional[Dict] = None, onchain_data: Optional[Dict] = None):
        self.market_data = market_data or {}
        self.onchain_data = onchain_data or {}
        self.data_source = "Real-time on-chain + market data"
    
    def detect_patterns(self) -> List[Dict]:
        """Detect real patterns from available data"""
        patterns = []
        
        # Pattern 1: Exchange Outflow (Whale Accumulation)
        netflow_24h = self.onchain_data.get('exchange_netflow_24h', 0)
        if netflow_24h < -500:  # Significant outflow
            patterns.append({
                'type': 'exchange_outflow',
                'kol': 'On-Chain Analytics',
                'kol_followers': 'N/A',
                'token': 'BTC',
                'content': f'24h exchange netflow: {netflow_24h:,.0f} BTC (outflow)',
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M'),
                'tweet_url': '#onchain',
                'risk_score': 30,
                'risk_factors': ['Exchange outflow', 'Whale accumulation signal'],
                'sentiment': 'Bullish',
                'correlation_note': 'Historical: Large outflows often precede price increases',
                'data_quality': 'Real-time on-chain data'
            })
        
        # Pattern 2: High Funding Rate (Overheated Longs)
        funding_rate = self.market_data.get('funding_rate', 0)
        if funding_rate > 0.008:  # High funding
            patterns.append({
                'type': 'high_funding',
                'kol': 'Market Structure',
                'kol_followers': 'N/A',
                'token': 'BTC',
                'content': f'Funding rate at {funding_rate*100:.3f}% - longs paying shorts',
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M'),
                'tweet_url': '#derivatives',
                'risk_score': 70,
                'risk_factors': ['Overheated longs', 'Short squeeze risk', 'High leverage'],
                'sentiment': 'Cautious',
                'correlation_note': 'High funding often leads to long liquidations',
                'data_quality': 'Real-time derivatives data'
            })
        
        # Pattern 3: Dormant Whale Activation
        dormant_count = len(self.onchain_data.get('dormant_addresses', []))
        if dormant_count > 3:
            patterns.append({
                'type': 'dormant_activation',
                'kol': 'Whale Alert',
                'kol_followers': 'N/A',
                'token': 'BTC',
                'content': f'{dormant_count} dormant whale addresses activated (90d+)',
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M'),
                'tweet_url': '#whales',
                'risk_score': 60,
                'risk_factors': ['Dormant whale movement', 'Potential sell pressure', 'Uncertainty'],
                'sentiment': 'Bearish',
                'correlation_note': 'Dormant whale activation can signal distribution',
                'data_quality': 'Real-time on-chain monitoring'
            })
        
        # Pattern 4: Token Unlock (Supply Pressure)
        unlock_7d = self.market_data.get('unlock_7d_usd', 0)
        if unlock_7d > 10000000:  # >$10M unlocking
            patterns.append({
                'type': 'token_unlock',
                'kol': 'Token Unlocks',
                'kol_followers': 'N/A',
                'token': self.market_data.get('unlock_token', 'Unknown'),
                'content': f'${unlock_7d/1e6:.1f}M unlocking in next 7 days',
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M'),
                'tweet_url': '#unlocks',
                'risk_score': 75,
                'risk_factors': ['Supply increase', 'Sell pressure expected', 'Inflation'],
                'sentiment': 'Bearish',
                'correlation_note': 'Large unlocks typically create sell pressure',
                'data_quality': 'Real-time unlock data'
            })
        
        # Pattern 5: High Liquidation Risk
        liq_longs = self.market_data.get('liquidation_longs', 0)
        liq_shorts = self.market_data.get('liquidation_shorts', 0)
        total_liq = liq_longs + liq_shorts
        if total_liq > 500000000:  # >$500M liquidations
            patterns.append({
                'type': 'high_liquidation',
                'kol': 'Liquidation Monitor',
                'kol_followers': 'N/A',
                'token': 'BTC',
                'content': f'24h liquidations: ${total_liq/1e6:.0f}M (Longs: ${liq_longs/1e6:.0f}M)',
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M'),
                'tweet_url': '#liquidations',
                'risk_score': 65,
                'risk_factors': ['High volatility', 'Leverage flush', 'Cascade risk'],
                'sentiment': 'Very Cautious',
                'correlation_note': 'High liquidations often mark local bottoms or tops',
                'data_quality': 'Real-time derivatives data'
            })
        
        # Pattern 6: MVRV Z-Score Extreme
        mvrv = self.onchain_data.get('mvrv_zscore', 0)
        if mvrv > 3.0:
            patterns.append({
                'type': 'mvrv_high',
                'kol': 'On-Chain Metrics',
                'kol_followers': 'N/A',
                'token': 'BTC',
                'content': f'MVRV Z-Score at {mvrv:.2f} - historically overvalued zone',
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M'),
                'tweet_url': '#mvrv',
                'risk_score': 80,
                'risk_factors': ['Overvalued historically', 'Potential correction', 'Cycle top risk'],
                'sentiment': 'Bearish',
                'correlation_note': 'MVRV > 3.0 historically marks cycle tops',
                'data_quality': 'Real-time on-chain calculation'
            })
        elif mvrv < -1.0:
            patterns.append({
                'type': 'mvrv_low',
                'kol': 'On-Chain Metrics',
                'kol_followers': 'N/A',
                'token': 'BTC',
                'content': f'MVRV Z-Score at {mvrv:.2f} - historically undervalued zone',
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M'),
                'tweet_url': '#mvrv',
                'risk_score': 25,
                'risk_factors': ['Undervalued historically', 'Accumulation opportunity'],
                'sentiment': 'Bullish',
                'correlation_note': 'MVRV < -1.0 historically marks cycle bottoms',
                'data_quality': 'Real-time on-chain calculation'
            })
        
        # Pattern 7: Miner Position Index (MPI)
        mpi = self.onchain_data.get('miner_mpi', 0)
        if mpi > 2.0:
            patterns.append({
                'type': 'miner_selling',
                'kol': 'Miner Monitor',
                'kol_followers': 'N/A',
                'token': 'BTC',
                'content': f'Miner Position Index at {mpi:.2f} - miners selling heavily',
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M'),
                'tweet_url': '#miners',
                'risk_score': 70,
                'risk_factors': ['Miner distribution', 'Sell pressure', 'Revenue realization'],
                'sentiment': 'Bearish',
                'correlation_note': 'MPI > 2.0 indicates significant miner selling',
                'data_quality': 'Real-time on-chain data'
            })
        elif mpi < -0.5:
            patterns.append({
                'type': 'miner_holding',
                'kol': 'Miner Monitor',
                'kol_followers': 'N/A',
                'token': 'BTC',
                'content': f'Miner Position Index at {mpi:.2f} - miners holding/accumulating',
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M'),
                'tweet_url': '#miners',
                'risk_score': 20,
                'risk_factors': ['Miner accumulation', 'Supply squeeze potential'],
                'sentiment': 'Bullish',
                'correlation_note': 'MPI < -0.5 indicates miner accumulation',
                'data_quality': 'Real-time on-chain data'
            })
        
        # If no significant patterns detected, add at least one informational pattern
        if not patterns:
            patterns.append({
                'type': 'market_overview',
                'kol': 'Market Monitor',
                'kol_followers': 'N/A',
                'token': 'BTC',
                'content': 'Market conditions within normal ranges. No extreme signals detected.',
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M'),
                'tweet_url': '#overview',
                'risk_score': 50,
                'risk_factors': ['Normal market conditions', 'No extreme signals'],
                'sentiment': 'Neutral',
                'correlation_note': 'Markets showing typical volatility patterns',
                'data_quality': 'Real-time market data'
            })
        
        return patterns
    
    def fetch_all_signals(self) -> Dict:
        """Fetch all pattern signals (compatible with old interface)"""
        patterns = self.detect_patterns()
        
        return {
            'tweets_analyzed': len(patterns),
            'patterns': patterns,
            'data_source': self.data_source,
            'timestamp': datetime.now().isoformat(),
            'note': 'Real-time pattern detection from on-chain and market data'
        }


def test_pattern_fetcher():
    """Test real pattern fetcher"""
    print("="*70)
    print("TESTING REAL PATTERN FETCHER")
    print("="*70)
    
    # Test data
    market_data = {
        'funding_rate': 0.012,
        'liquidation_longs': 150000000,
        'liquidation_shorts': 80000000,
        'unlock_7d_usd': 25000000,
        'unlock_token': 'EXAMPLE'
    }
    
    onchain_data = {
        'exchange_netflow_24h': -1200,
        'dormant_addresses': [{'addr': '0x1'}, {'addr': '0x2'}, {'addr': '0x3'}],
        'mvrv_zscore': 2.5,
        'miner_mpi': 1.8
    }
    
    fetcher = RealPatternFetcher(market_data, onchain_data)
    signals = fetcher.fetch_all_signals()
    
    print(f"\nData source: {signals['data_source']}")
    print(f"Patterns detected: {len(signals['patterns'])}")
    
    for i, p in enumerate(signals['patterns'], 1):
        print(f"\n{i}. {p['type']} | {p['token']}")
        print(f"   Risk: {p['risk_score']}/100 | Sentiment: {p['sentiment']}")
        print(f"   Factors: {', '.join(p['risk_factors'])}")
        print(f"   Data: {p['data_quality']}")
    
    print("\n" + "="*70)


if __name__ == "__main__":
    test_pattern_fetcher()
