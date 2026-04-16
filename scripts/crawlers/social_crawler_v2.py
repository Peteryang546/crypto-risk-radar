#!/usr/bin/env python3
"""
Social Media Acceleration Monitor v2
Uses twikit (no API key) for Twitter and Telethon for Telegram
"""

import asyncio
import json
import os
import sys
from datetime import datetime, timedelta
from typing import Dict, List, Any
from collections import defaultdict

sys.path.insert(0, r'F:\stepclaw\agents\blockchain-analyst')
from config import USE_MOCK_DATA, TELEGRAM_API_ID, TELEGRAM_API_HASH

# Try importing libraries
try:
    from twikit import Client as TwitterClient
    TWIKIT_AVAILABLE = True
except ImportError:
    TWIKIT_AVAILABLE = False
    print("[WARN] twikit not available")

try:
    from telethon import TelegramClient
    from telethon.tl.functions.messages import GetHistoryRequest
    TELETHON_AVAILABLE = True
except ImportError:
    TELETHON_AVAILABLE = False
    print("[WARN] telethon not available")


class SocialMonitorV2:
    """Monitor social media using twikit and telethon"""
    
    def __init__(self):
        self.keywords = [
            "bitcoin", "btc", "ethereum", "eth", "crypto",
            "moon", "pump", "dump", "buy", "sell",
            "bull", "bear", "fomo", "fud", "altcoin"
        ]
        self.twitter_client = None
        self.telegram_client = None
        
    async def init_twitter(self):
        """Initialize Twitter client (twikit)"""
        if not TWIKIT_AVAILABLE:
            return False
        
        try:
            self.twitter_client = TwitterClient('en-US')
            # Try to load existing cookies
            if os.path.exists('twitter_cookies.json'):
                self.twitter_client.load_cookies('twitter_cookies.json')
            else:
                print("[INFO] Twitter cookies not found, will need login")
            return True
        except Exception as e:
            print(f"[ERROR] Twitter init failed: {e}")
            return False
    
    async def init_telegram(self):
        """Initialize Telegram client (telethon)"""
        if not TELETHON_AVAILABLE:
            return False
        
        if not TELEGRAM_API_ID or not TELEGRAM_API_HASH:
            print("[WARN] Telegram API credentials not configured")
            return False
        
        try:
            self.telegram_client = TelegramClient(
                'telegram_session',
                int(TELEGRAM_API_ID),
                TELEGRAM_API_HASH
            )
            await self.telegram_client.connect()
            
            if not await self.telegram_client.is_user_authorized():
                print("[WARN] Telegram not authorized, please run auth script")
                return False
            
            return True
        except Exception as e:
            print(f"[ERROR] Telegram init failed: {e}")
            return False
    
    async def fetch_twitter(self, query: str = "bitcoin OR btc OR crypto", count: int = 50) -> List[Dict]:
        """Fetch recent tweets"""
        if not self.twitter_client:
            return []
        
        try:
            tweets = await self.twitter_client.search_tweet(query, 'Latest', count)
            messages = []
            for tweet in tweets:
                messages.append({
                    "platform": "twitter",
                    "text": tweet.text,
                    "time": tweet.created_at,
                    "author": tweet.user.name,
                    "likes": tweet.favorite_count
                })
            return messages
        except Exception as e:
            print(f"[ERROR] Twitter fetch failed: {e}")
            return []
    
    async def fetch_telegram(self, channel: str = "cryptopanic", limit: int = 50) -> List[Dict]:
        """Fetch recent Telegram messages"""
        if not self.telegram_client:
            return []
        
        try:
            entity = await self.telegram_client.get_entity(channel)
            messages = []
            
            async for message in self.telegram_client.iter_messages(entity, limit=limit):
                if message.text:
                    messages.append({
                        "platform": "telegram",
                        "text": message.text,
                        "time": message.date.isoformat() if message.date else datetime.now().isoformat(),
                        "author": str(message.sender_id) if message.sender_id else "unknown"
                    })
            
            return messages
        except Exception as e:
            print(f"[ERROR] Telegram fetch failed: {e}")
            return []
    
    def analyze_messages(self, messages: List[Dict]) -> Dict[str, Any]:
        """Analyze message frequency and keywords"""
        if not messages:
            return {"acceleration": 1.0, "baseline": 0, "current": 0}
        
        now = datetime.now()
        baseline_cutoff = now - timedelta(minutes=120)
        current_cutoff = now - timedelta(minutes=10)
        
        # Count messages
        baseline_count = sum(1 for m in messages 
                           if datetime.fromisoformat(m.get("time", "").replace('Z', '+00:00')) > baseline_cutoff)
        current_count = sum(1 for m in messages 
                          if datetime.fromisoformat(m.get("time", "").replace('Z', '+00:00')) > current_cutoff)
        
        # Calculate acceleration
        expected = baseline_count * (10 / 120) if baseline_count > 0 else 1
        acceleration = current_count / expected if expected > 0 else 1.0
        
        # Keyword analysis
        keyword_counts = defaultdict(int)
        for msg in messages:
            text = msg.get("text", "").lower()
            for kw in self.keywords:
                if kw in text:
                    keyword_counts[kw] += 1
        
        top_keywords = sorted(
            [{"word": k, "count": v} for k, v in keyword_counts.items()],
            key=lambda x: x["count"],
            reverse=True
        )[:10]
        
        # Sentiment
        if acceleration > 5:
            sentiment = "Extreme FOMO"
            risk = "High"
        elif acceleration > 3:
            sentiment = "High Excitement"
            risk = "Medium"
        elif acceleration > 1.5:
            sentiment = "Elevated Interest"
            risk = "Low"
        else:
            sentiment = "Normal"
            risk = "Low"
        
        return {
            "acceleration": round(acceleration, 2),
            "baseline": baseline_count,
            "current": current_count,
            "top_keywords": top_keywords,
            "sentiment": sentiment,
            "risk_level": risk,
            "total_messages": len(messages)
        }
    
    async def monitor(self) -> Dict[str, Any]:
        """Run full monitoring cycle"""
        if USE_MOCK_DATA:
            return self._get_mock_data()
        
        all_messages = []
        
        # Initialize clients
        await self.init_twitter()
        await self.init_telegram()
        
        # Fetch data
        if self.twitter_client:
            twitter_msgs = await self.fetch_twitter()
            all_messages.extend(twitter_msgs)
            print(f"[OK] Fetched {len(twitter_msgs)} tweets")
        
        if self.telegram_client:
            telegram_msgs = await self.fetch_telegram()
            all_messages.extend(telegram_msgs)
            print(f"[OK] Fetched {len(telegram_msgs)} telegram messages")
        
        # Analyze
        result = self.analyze_messages(all_messages)
        result["sources"] = {
            "twitter": TWIKIT_AVAILABLE and self.twitter_client is not None,
            "telegram": TELETHON_AVAILABLE and self.telegram_client is not None
        }
        
        return result
    
    def _get_mock_data(self) -> Dict[str, Any]:
        """Mock data for testing"""
        return {
            "acceleration": 4.5,
            "baseline": 45,
            "current": 28,
            "top_keywords": [
                {"word": "moon", "count": 15},
                {"word": "pump", "count": 12},
                {"word": "buy", "count": 8},
                {"word": "fomo", "count": 6}
            ],
            "sentiment": "High Excitement",
            "risk_level": "Medium",
            "total_messages": 150,
            "sources": {"twitter": False, "telegram": False}
        }


async def main():
    """Test the monitor"""
    print("="*70)
    print("SOCIAL MONITOR V2 TEST")
    print("="*70)
    
    monitor = SocialMonitorV2()
    result = await monitor.monitor()
    
    print(f"\nAcceleration: {result['acceleration']}x")
    print(f"Sentiment: {result['sentiment']}")
    print(f"Risk: {result['risk_level']}")
    print(f"Sources: {result['sources']}")


if __name__ == "__main__":
    asyncio.run(main())
