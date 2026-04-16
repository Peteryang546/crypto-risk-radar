#!/usr/bin/env python3
"""
Social Signals Fetcher
Fetches KOL tweets and correlates with on-chain activity
Uses Nitter (X mirror) and LunarCrush APIs
"""

import subprocess
import json
import re
from datetime import datetime, timedelta
from typing import List, Dict
from urllib.parse import quote


# Key KOLs to monitor
MONITORED_KOLS = {
    'elonmusk': {'name': 'Elon Musk', 'category': 'Influencer', 'risk_weight': 0.9},
    'cz_binance': {'name': 'CZ', 'category': 'Exchange CEO', 'risk_weight': 0.8},
    'saylor': {'name': 'Michael Saylor', 'category': 'Institutional', 'risk_weight': 0.7},
    'VitalikButerin': {'name': 'Vitalik Buterin', 'category': 'Founder', 'risk_weight': 0.85},
    'SatoshiLite': {'name': 'Charlie Lee', 'category': 'Founder', 'risk_weight': 0.6},
}

# Token symbols to watch
WATCHED_TOKENS = ['BTC', 'ETH', 'DOGE', 'SHIB', 'PEPE', 'FLOKI', 'BONK', 'WOJAK']


class SocialSignalFetcher:
    """Fetch and analyze social signals from crypto KOLs"""
    
    def __init__(self):
        self.nitter_instances = [
            'https://nitter.net',
            'https://nitter.it',
            'https://nitter.cz',
        ]
    
    def _fetch_via_powershell(self, url: str) -> str:
        """Use PowerShell to fetch data"""
        ps_code = f'''
        try {{
            $resp = Invoke-RestMethod -Uri "{url}" -TimeoutSec 30 -MaximumRedirection 0
            $resp
        }} catch {{
            ""
        }}
        '''
        
        try:
            result = subprocess.run(
                ["powershell", "-Command", ps_code],
                capture_output=True,
                text=True,
                timeout=60
            )
            return result.stdout
        except Exception as e:
            print(f"[ERROR] PowerShell fetch failed: {e}")
        
        return ""
    
    def fetch_nitter_tweets(self, username: str, limit: int = 5) -> List[Dict]:
        """Fetch tweets from Nitter (X mirror)"""
        tweets = []
        
        for instance in self.nitter_instances:
            try:
                # Nitter RSS feed
                url = f"{instance}/{username}/rss"
                content = self._fetch_via_powershell(url)
                
                if content and '<item>' in content:
                    # Parse RSS items
                    items = content.split('<item>')[1:limit+1]
                    
                    for item in items:
                        # Extract title
                        title_match = re.search(r'<title>(.*?)</title>', item, re.DOTALL)
                        title = title_match.group(1) if title_match else ""
                        
                        # Extract pubDate
                        date_match = re.search(r'<pubDate>(.*?)</pubDate>', item)
                        pub_date = date_match.group(1) if date_match else ""
                        
                        # Extract link
                        link_match = re.search(r'<link>(.*?)</link>', item)
                        link = link_match.group(1) if link_match else ""
                        
                        # Check if mentions crypto
                        mentions_tokens = [t for t in WATCHED_TOKENS if t.lower() in title.lower()]
                        
                        if mentions_tokens:
                            tweets.append({
                                'username': username,
                                'text': title[:200] + '...' if len(title) > 200 else title,
                                'date': pub_date,
                                'url': link.replace('nitter.net', 'x.com').replace('nitter.it', 'x.com').replace('nitter.cz', 'x.com'),
                                'mentions': mentions_tokens,
                                'sentiment': self._analyze_sentiment(title),
                            })
                    
                    if tweets:
                        break  # Success, no need to try other instances
                        
            except Exception as e:
                print(f"[WARNING] Nitter fetch failed for {instance}: {e}")
                continue
        
        return tweets
    
    def _analyze_sentiment(self, text: str) -> str:
        """Simple sentiment analysis"""
        text_lower = text.lower()
        
        positive_words = ['moon', 'pump', 'bull', 'buy', 'hold', 'long', 'up', 'rise', 'gain', 'profit']
        negative_words = ['dump', 'bear', 'sell', 'short', 'down', 'fall', 'loss', 'crash', 'scam', 'rug']
        
        pos_count = sum(1 for w in positive_words if w in text_lower)
        neg_count = sum(1 for w in negative_words if w in text_lower)
        
        if pos_count > neg_count:
            return 'Bullish'
        elif neg_count > pos_count:
            return 'Bearish'
        else:
            return 'Neutral'
    
    def fetch_lunarcrush_data(self, symbol: str) -> Dict:
        """Fetch social data from LunarCrush (requires API key)"""
        # Note: LunarCrush requires API key for full access
        # This is a placeholder for when API key is available
        return {
            'symbol': symbol,
            'social_volume': 0,
            'social_score': 0,
            'galaxy_score': 0,
            'alt_rank': 0,
        }
    
    def detect_patterns(self, tweets: List[Dict]) -> List[Dict]:
        """Detect suspicious patterns in tweets"""
        patterns = []
        
        for tweet in tweets:
            risk_factors = []
            risk_score = 0
            
            # Check for excessive hype
            hype_words = ['moon', '100x', '1000x', 'guaranteed', "can't lose", 'sure thing']
            if any(w in tweet['text'].lower() for w in hype_words):
                risk_factors.append("Excessive hype language")
                risk_score += 30
            
            # Check for urgency
            urgency_words = ['now', 'hurry', 'last chance', "don't miss", 'act fast', 'limited time']
            if any(w in tweet['text'].lower() for w in urgency_words):
                risk_factors.append("Urgency tactics")
                risk_score += 25
            
            # Check for specific token mentions with price targets
            if re.search(r'\$[\d,]+|target.*\d+|price.*\d+', tweet['text'], re.IGNORECASE):
                risk_factors.append("Specific price targets")
                risk_score += 20
            
            # Check for referral/promotional content
            promo_words = ['link in bio', 'dm me', 'join my', 'exclusive', 'premium']
            if any(w in tweet['text'].lower() for w in promo_words):
                risk_factors.append("Promotional content")
                risk_score += 15
            
            # High follower count + risky content = higher risk
            kol_info = MONITORED_KOLS.get(tweet['username'], {})
            if kol_info:
                risk_score = min(100, risk_score + int(kol_info.get('risk_weight', 0.5) * 20))
            
            if risk_score >= 30:
                patterns.append({
                    'kol': f"@{tweet['username']}",
                    'kol_name': kol_info.get('name', tweet['username']),
                    'token': ', '.join(tweet['mentions']),
                    'content': tweet['text'][:100] + '...',
                    'timestamp': tweet['date'],
                    'tweet_url': tweet['url'],
                    'risk_score': risk_score,
                    'risk_factors': risk_factors,
                    'sentiment': tweet['sentiment'],
                    'correlation_note': 'Tweet mentions token; monitor for unusual on-chain activity'
                })
        
        # Sort by risk score
        patterns.sort(key=lambda x: x['risk_score'], reverse=True)
        return patterns[:10]
    
    def fetch_all_signals(self) -> Dict:
        """Fetch all social signals"""
        print("[INFO] Fetching social signals from Nitter...")
        
        all_tweets = []
        for username in MONITORED_KOLS.keys():
            print(f"  Checking @{username}...")
            tweets = self.fetch_nitter_tweets(username, limit=3)
            all_tweets.extend(tweets)
        
        print(f"[OK] Fetched {len(all_tweets)} tweets mentioning watched tokens")
        
        # Detect patterns
        patterns = self.detect_patterns(all_tweets)
        print(f"[OK] Detected {len(patterns)} suspicious patterns")
        
        return {
            'tweets_analyzed': len(all_tweets),
            'patterns': patterns,
            'data_source': 'Nitter (X mirror)',
            'timestamp': datetime.now().isoformat(),
        }
    
    def get_sample_patterns(self) -> List[Dict]:
        """Return sample patterns for demonstration"""
        return [
            {
                'kol': '@CryptoGuru',
                'kol_name': 'Crypto Guru',
                'token': '$MOON',
                'content': 'This token is going to moon! Buy now before it\'s too late! Not financial advice...',
                'timestamp': '2 hours ago',
                'tweet_url': 'https://x.com/CryptoGuru/status/1234567890',
                'risk_score': 75,
                'risk_factors': ['Excessive hype language', 'Urgency tactics'],
                'sentiment': 'Bullish',
                'correlation_note': 'Tweet posted 15 minutes before 500% price spike'
            }
        ]


def test_social_fetcher():
    """Test social signal fetching"""
    print("="*70)
    print("TESTING SOCIAL SIGNAL FETCHER")
    print("="*70)
    
    fetcher = SocialSignalFetcher()
    
    # Test Nitter fetch
    print("\n[1/2] Fetching tweets from Nitter...")
    signals = fetcher.fetch_all_signals()
    
    print(f"\nTweets analyzed: {signals['tweets_analyzed']}")
    print(f"Patterns detected: {len(signals['patterns'])}")
    
    if signals['patterns']:
        print("\nDetected patterns:")
        for p in signals['patterns'][:3]:
            print(f"  {p['kol']}: {p['token']} - Risk {p['risk_score']}/100")
            print(f"    Factors: {', '.join(p['risk_factors'])}")
    
    # Show sample
    print("\n[2/2] Sample pattern:")
    sample = fetcher.get_sample_patterns()[0]
    print(f"  KOL: {sample['kol']}")
    print(f"  Token: {sample['token']}")
    print(f"  Risk: {sample['risk_score']}/100")
    
    print("\n" + "="*70)


if __name__ == "__main__":
    test_social_fetcher()
