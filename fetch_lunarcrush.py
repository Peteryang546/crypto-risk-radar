#!/usr/bin/env python3
"""
LunarCrush API Integration
Real social data without X account
"""

import sys
sys.path.insert(0, r'C:\Users\Administrator\AppData\Local\Programs\Python\Python311\Lib\site-packages')

import requests
import json
from datetime import datetime
from typing import List, Dict, Optional


class LunarCrushFetcher:
    """Fetch real social signals from LunarCrush API"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.lunarcrush.com/v2"
    
    def fetch_coin_data(self, symbol: str = "BTC") -> Optional[Dict]:
        """Fetch social data for a specific coin"""
        try:
            url = f"{self.base_url}/assets"
            params = {
                'key': self.api_key,
                'symbol': symbol,
                'data_points': 1
            }
            
            response = requests.get(url, params=params, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                if 'data' in data and len(data['data']) > 0:
                    asset = data['data'][0]
                    return {
                        'symbol': symbol,
                        'name': asset.get('name', symbol),
                        'price': asset.get('price', 0),
                        'social_volume': asset.get('social_volume', 0),
                        'social_contributors': asset.get('social_contributors', 0),
                        'social_dominance': asset.get('social_dominance', 0),
                        'average_sentiment': asset.get('average_sentiment', 0),
                        'sentiment_absolute': asset.get('sentiment_absolute', 0),
                        'social_score': asset.get('social_score', 0),
                        'galaxy_score': asset.get('galaxy_score', 0),
                        'alt_rank': asset.get('alt_rank', 0),
                        'market_cap': asset.get('market_cap', 0),
                        'volume_24h': asset.get('volume_24h', 0),
                        'percent_change_24h': asset.get('percent_change_24h', 0),
                        'timestamp': datetime.now().isoformat()
                    }
                else:
                    print(f"[WARNING] No data returned for {symbol}")
                    return None
            else:
                print(f"[ERROR] LunarCrush API error: {response.status_code}")
                print(f"[ERROR] Response: {response.text[:200]}")
                return None
                
        except Exception as e:
            print(f"[ERROR] Failed to fetch LunarCrush data: {e}")
            return None
    
    def fetch_multiple_coins(self, symbols: List[str] = None) -> List[Dict]:
        """Fetch social data for multiple coins"""
        if symbols is None:
            symbols = ['BTC', 'ETH', 'DOGE', 'SHIB', 'PEPE']
        
        results = []
        for symbol in symbols:
            data = self.fetch_coin_data(symbol)
            if data:
                results.append(data)
        
        return results
    
    def detect_social_patterns(self) -> List[Dict]:
        """Detect patterns from LunarCrush social data"""
        patterns = []
        
        # Fetch data for major coins
        coins = self.fetch_multiple_coins(['BTC', 'ETH', 'DOGE', 'SHIB', 'PEPE'])
        
        for coin in coins:
            symbol = coin['symbol']
            
            # Pattern 1: Social Volume Spike
            if coin['social_volume'] > 50000:
                patterns.append({
                    'type': 'social_volume_spike',
                    'kol': 'LunarCrush Social',
                    'kol_followers': 'N/A',
                    'token': symbol,
                    'content': f"24h social volume: {coin['social_volume']:,} mentions",
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M'),
                    'tweet_url': f'https://lunarcrush.com/coins/{symbol.lower()}',
                    'risk_score': 40,
                    'risk_factors': ['High social attention', 'Increased volatility risk'],
                    'sentiment': 'Bullish' if coin['average_sentiment'] > 0.6 else 'Neutral',
                    'correlation_note': f"Social dominance: {coin['social_dominance']:.2f}%",
                    'data_quality': 'Real-time LunarCrush API'
                })
            
            # Pattern 2: Extreme Sentiment
            if coin['average_sentiment'] > 0.8:
                patterns.append({
                    'type': 'extreme_positive_sentiment',
                    'kol': 'LunarCrush Sentiment',
                    'kol_followers': 'N/A',
                    'token': symbol,
                    'content': f"Extreme positive sentiment: {coin['average_sentiment']:.2f}/1.0",
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M'),
                    'tweet_url': f'https://lunarcrush.com/coins/{symbol.lower()}',
                    'risk_score': 60,
                    'risk_factors': ['Extreme optimism', 'Potential reversal risk', 'FOMO indicator'],
                    'sentiment': 'Very Bullish',
                    'correlation_note': 'Extreme sentiment often precedes corrections',
                    'data_quality': 'Real-time LunarCrush API'
                })
            elif coin['average_sentiment'] < 0.2:
                patterns.append({
                    'type': 'extreme_negative_sentiment',
                    'kol': 'LunarCrush Sentiment',
                    'kol_followers': 'N/A',
                    'token': symbol,
                    'content': f"Extreme negative sentiment: {coin['average_sentiment']:.2f}/1.0",
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M'),
                    'tweet_url': f'https://lunarcrush.com/coins/{symbol.lower()}',
                    'risk_score': 35,
                    'risk_factors': ['Extreme fear', 'Potential bottom', 'Contrarian opportunity'],
                    'sentiment': 'Very Bearish',
                    'correlation_note': 'Extreme fear often marks local bottoms',
                    'data_quality': 'Real-time LunarCrush API'
                })
            
            # Pattern 3: Galaxy Score Spike
            if coin['galaxy_score'] > 80:
                patterns.append({
                    'type': 'galaxy_score_spike',
                    'kol': 'LunarCrush Galaxy',
                    'kol_followers': 'N/A',
                    'token': symbol,
                    'content': f"Galaxy Score: {coin['galaxy_score']}/100 - strong fundamentals",
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M'),
                    'tweet_url': f'https://lunarcrush.com/coins/{symbol.lower()}',
                    'risk_score': 30,
                    'risk_factors': ['Strong social metrics', 'Positive momentum'],
                    'sentiment': 'Bullish',
                    'correlation_note': 'High galaxy score indicates strong community engagement',
                    'data_quality': 'Real-time LunarCrush API'
                })
            
            # Pattern 4: Alt Rank Drop (improving)
            if coin['alt_rank'] < 50:
                patterns.append({
                    'type': 'alt_rank_improving',
                    'kol': 'LunarCrush Rank',
                    'kol_followers': 'N/A',
                    'token': symbol,
                    'content': f"AltRank: #{coin['alt_rank']} - outperforming alts",
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M'),
                    'tweet_url': f'https://lunarcrush.com/coins/{symbol.lower()}',
                    'risk_score': 35,
                    'risk_factors': ['Outperforming market', 'Strong relative strength'],
                    'sentiment': 'Bullish',
                    'correlation_note': 'Low AltRank indicates strong performance vs other alts',
                    'data_quality': 'Real-time LunarCrush API'
                })
        
        return patterns
    
    def fetch_all_signals(self) -> Dict:
        """Fetch all social signals (compatible interface)"""
        patterns = self.detect_social_patterns()
        
        return {
            'tweets_analyzed': len(patterns) * 100,  # Estimated
            'patterns': patterns,
            'data_source': 'LunarCrush API - Real-time social data',
            'timestamp': datetime.now().isoformat(),
            'note': 'Real social data from LunarCrush API - no X account required'
        }


def test_lunarcrush():
    """Test LunarCrush API"""
    print("="*70)
    print("TESTING LUNARCRUSH API")
    print("="*70)
    
    # API Key
    API_KEY = "wn71tjsxcee77td3qmxs7th5mtmo1p6d9twocwwd9"
    
    fetcher = LunarCrushFetcher(API_KEY)
    
    # Test single coin
    print("\n[Test 1] Fetching BTC data...")
    btc_data = fetcher.fetch_coin_data('BTC')
    if btc_data:
        print(f"✅ BTC Price: ${btc_data['price']:,.2f}")
        print(f"✅ Social Volume: {btc_data['social_volume']:,}")
        print(f"✅ Sentiment: {btc_data['average_sentiment']:.2f}")
        print(f"✅ Galaxy Score: {btc_data['galaxy_score']}")
    else:
        print("❌ Failed to fetch BTC data")
    
    # Test pattern detection
    print("\n[Test 2] Detecting social patterns...")
    patterns = fetcher.detect_social_patterns()
    print(f"✅ Patterns detected: {len(patterns)}")
    
    for i, p in enumerate(patterns[:3], 1):
        print(f"\n{i}. {p['type']} | {p['token']}")
        print(f"   Risk: {p['risk_score']}/100 | Sentiment: {p['sentiment']}")
        print(f"   Content: {p['content'][:60]}...")
    
    print("\n" + "="*70)


if __name__ == "__main__":
    test_lunarcrush()
