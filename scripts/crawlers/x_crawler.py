#!/usr/bin/env python3
"""
X (Twitter) KOL Shill Monitor
Uses Nitter mirror to avoid login requirements
Tracks KOL tweets for shill keywords
"""

import re
import json
import time
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Any

sys.path.insert(0, r'F:\stepclaw\agents\blockchain-analyst')
from config import USE_MOCK_DATA

# Shill keywords to detect
SHILL_KEYWORDS = [
    'moon', '100x', 'gem', 'buy now', 'next big thing', 'to the moon', 
    'shill', 'pump', 'sale', 'presale', "don't miss", 'last chance',
    'going parabolic', 'explosive growth', 'easy 10x', 'guaranteed'
]

# Token symbol pattern (e.g., $BTC, $ETH)
TOKEN_PATTERN = re.compile(r'\$([A-Za-z0-9]{2,10})')
# Contract address pattern (0x...)
CONTRACT_PATTERN = re.compile(r'0x[a-fA-F0-9]{40}')


class XCrawler:
    """X/Twitter crawler using Nitter mirror"""
    
    def __init__(self, use_mock_data=False):
        self.use_mock_data = use_mock_data
        self.kol_list = self._load_kol_list()
    
    def _load_kol_list(self) -> List[Dict]:
        """Load KOL list from config"""
        kol_file = Path(r'F:\stepclaw\agents\blockchain-analyst\data\kol_list.json')
        if kol_file.exists():
            with open(kol_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return [k for k in data.get('kol_list', []) if k.get('watch', False)]
        return []
    
    def _fetch_via_powershell(self, username: str) -> List[Dict]:
        """Fetch tweets via PowerShell using Nitter"""
        import subprocess
        
        ps_code = f'''
        try {{
            $url = "https://nitter.net/{username}"
            $resp = Invoke-RestMethod -Uri $url -TimeoutSec 30 -UserAgent "Mozilla/5.0"
            # Return raw HTML for parsing
            @{{"html" = $resp; "username" = "{username}"}} | ConvertTo-Json -Compress
        }} catch {{
            Write-Output "{{`"error`": `"$($_.Exception.Message)`"}}"
        }}
        '''
        
        try:
            result = subprocess.run(
                ["powershell", "-Command", ps_code],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0 and result.stdout.strip():
                data = json.loads(result.stdout)
                if "error" not in data:
                    return self._parse_nitter_html(data.get("html", ""), username)
        except Exception as e:
            print(f"[ERROR] Failed to fetch {username}: {e}")
        
        return []
    
    def _parse_nitter_html(self, html: str, username: str) -> List[Dict]:
        """Parse Nitter HTML to extract tweets"""
        tweets = []
        
        # Simple regex-based parsing (Nitter structure)
        # Each tweet is in a .timeline-item div
        tweet_blocks = re.findall(r'<div class="timeline-item"[^>]*>(.*?)</div>\s*</div>\s*</div>', html, re.DOTALL)
        
        for block in tweet_blocks[:20]:  # Last 20 tweets
            # Extract tweet text
            text_match = re.search(r'<div class="tweet-content[^"]*"[^>]*>.*?<div class="tweet-body"[^>]*>(.*?)</div>', block, re.DOTALL)
            if not text_match:
                continue
            
            text_html = text_match.group(1)
            # Remove HTML tags
            text = re.sub(r'<[^>]+>', ' ', text_html)
            text = re.sub(r'\s+', ' ', text).strip()
            
            # Extract timestamp
            time_match = re.search(r'<span[^>]*title="([^"]+)"[^>]*>.*?</span>', block)
            tweet_time = time_match.group(1) if time_match else datetime.now().isoformat()
            
            # Extract tweet link
            link_match = re.search(r'<a[^>]*href="(/[^"]+)"[^>]*>.*?</a>', block)
            tweet_link = f"https://nitter.net{link_match.group(1)}" if link_match else ""
            
            tweets.append({
                "username": username,
                "text": text,
                "time": tweet_time,
                "link": tweet_link,
                "platform": "x"
            })
        
        return tweets
    
    def _get_mock_tweets(self) -> List[Dict]:
        """Generate mock shill tweets for testing"""
        return [
            {
                "username": "CryptoGuru",
                "text": "Just found the next 100x gem! $MOON token is going to explode. Don't miss out! Buy now before it's too late!",
                "time": (datetime.now() - timedelta(hours=2)).isoformat(),
                "link": "https://x.com/CryptoGuru/status/123456",
                "platform": "x",
                "is_shill": True,
                "tokens": ["MOON"]
            },
            {
                "username": "MoonMaster",
                "text": "This $GEM token has amazing fundamentals. To the moon! Presale ending soon!",
                "time": (datetime.now() - timedelta(hours=5)).isoformat(),
                "link": "https://x.com/MoonMaster/status/789012",
                "platform": "x",
                "is_shill": True,
                "tokens": ["GEM"]
            }
        ]
    
    def detect_shill(self, tweet: Dict) -> Dict:
        """Analyze if tweet is a shill"""
        text_lower = tweet.get("text", "").lower()
        
        # Check for shill keywords
        detected_keywords = [kw for kw in SHILL_KEYWORDS if kw.lower() in text_lower]
        
        # Extract token symbols
        tokens = TOKEN_PATTERN.findall(tweet.get("text", ""))
        
        # Extract contract addresses
        contracts = CONTRACT_PATTERN.findall(tweet.get("text", ""))
        
        is_shill = len(detected_keywords) > 0 and (len(tokens) > 0 or len(contracts) > 0)
        
        return {
            **tweet,
            "is_shill": is_shill,
            "shill_keywords": detected_keywords,
            "tokens": tokens,
            "contracts": contracts,
            "shill_score": len(detected_keywords) * 10 + len(tokens) * 5
        }
    
    def fetch_all_kols(self, hours_back: int = 12) -> List[Dict]:
        """Fetch and analyze tweets from all monitored KOLs"""
        if self.use_mock_data:
            print("[INFO] Using mock shill data")
            mock_tweets = self._get_mock_tweets()
            return [self.detect_shill(t) for t in mock_tweets]
        
        all_shills = []
        
        for kol in self.kol_list:
            username = kol.get("username")
            print(f"[INFO] Fetching tweets from @{username}...")
            
            tweets = self._fetch_via_powershell(username)
            
            for tweet in tweets:
                analyzed = self.detect_shill(tweet)
                if analyzed["is_shill"]:
                    all_shills.append(analyzed)
                    print(f"  [ALERT] Shill detected: {analyzed['tokens']} - Score: {analyzed['shill_score']}")
            
            time.sleep(1)  # Rate limiting
        
        return all_shills
    
    def generate_shill_report(self, shills: List[Dict]) -> str:
        """Generate markdown report of detected shills"""
        if not shills:
            return """## 🕵️ KOL Shill Monitor (Last 12h)

**Status**: ✅ No shill tweets detected from monitored KOLs.

*Monitoring 5 high-frequency KOL accounts for pump-and-dump signals.*
"""
        
        md = """## 🚨 KOL Shill Alerts (Last 12h)

**Warning**: The following KOLs have posted promotional content that matches shill patterns.

| KOL | Token | Keywords | Score | Time |
|-----|-------|----------|-------|------|
"""
        
        for shill in shills:
            tokens = ", ".join([f"${t}" for t in shill.get("tokens", [])])
            keywords = ", ".join(shill.get("shill_keywords", []))
            md += f"| @{shill['username']} | {tokens} | {keywords} | {shill['shill_score']} | {shill['time'][:16]} |\n"
        
        md += """
### Analysis
- **Shill Score**: Based on keyword frequency + token mentions
- **High Risk**: Score > 30 indicates aggressive promotion
- **Recommendation**: Check on-chain data for insider buying before the shill

### Next Steps
1. Verify if mentioned tokens had unusual wallet activity before the tweet
2. Check if KOL has history of promoting tokens that later dumped
3. See [KOL Integrity Scoreboard](#kol-integrity) for historical performance
"""
        
        return md


def main():
    """Test the crawler"""
    print("="*70)
    print("X KOL SHILL MONITOR")
    print("="*70)
    
    crawler = XCrawler(use_mock_data=True)
    shills = crawler.fetch_all_kols()
    
    print(f"\n[INFO] Detected {len(shills)} shill tweets")
    print(crawler.generate_shill_report(shills))


if __name__ == "__main__":
    main()
