#!/usr/bin/env python3
"""
DEXTools/GeckoTerminal Token Fetcher
Fetches new and trending tokens for risk analysis
"""

import subprocess
import json
from typing import List, Dict


class TokenFetcher:
    """Fetch new tokens from DEX data sources"""
    
    def fetch_from_geckoterminal(self, network: str = 'eth', limit: int = 20) -> List[Dict]:
        """Fetch new tokens from GeckoTerminal API via PowerShell"""
        ps_code = f'''
        try {{
            $url = "https://api.geckoterminal.com/api/v2/networks/{network}/pools?page=1"
            $resp = Invoke-RestMethod -Uri $url -TimeoutSec 30
            
            $tokens = $resp.data | ForEach-Object {{
                $attrs = $_.attributes
                $baseToken = $_.relationships.base_token.data.id -split '\.' | Select-Object -Last 1
                $quoteToken = $_.relationships.quote_token.data.id -split '\.' | Select-Object -Last 1
                @{{
                    address = $baseToken
                    pool_address = $attrs.address
                    name = $attrs.name
                    symbol = if ($attrs.name -match "^(\w+)/") {{ $matches[1] }} else {{ $baseToken.Substring(0, [Math]::Min(8, $baseToken.Length)) }}
                    quote_symbol = if ($attrs.name -match "/(\w+)$") {{ $matches[1] }} else {{ "ETH" }}
                    price_usd = $attrs.base_token_price_usd
                    volume_24h = $attrs.volume_usd.h24
                    liquidity = $attrs.reserve_in_usd
                    price_change_24h = $attrs.price_change_percentage.h24
                    transactions_24h = ($attrs.transactions.h24.buys + $attrs.transactions.h24.sells)
                    created_at = $attrs.pool_created_at
                    dex = $attrs.name -split ' ' | Select-Object -Last 1
                }}
            }}
            
            # Sort by creation time (newest first) and limit
            $sorted = $tokens | Sort-Object -Property {{ $_.created_at }} -Descending | Select-Object -First {limit}
            
            @{{ status = "success"; data = $sorted }} | ConvertTo-Json -Depth 10
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
                data = json.loads(result.stdout)
                if data.get('status') == 'success':
                    return data.get('data', [])
        except Exception as e:
            print(f"[ERROR] GeckoTerminal fetch failed: {e}")
        
        return []
    
    def identify_high_risk_tokens(self, tokens: List[Dict]) -> List[Dict]:
        """Identify high-risk tokens from the list"""
        high_risk = []
        
        for token in tokens:
            risk_score = 0
            risk_factors = []
            
            # Low liquidity (< $500k for DEX tokens)
            liquidity = float(token.get('liquidity', 0) or 0)
            if liquidity < 500000:
                risk_score += 25
                risk_factors.append("Low liquidity")
            elif liquidity < 100000:
                risk_score += 40
                risk_factors.append("Very low liquidity")
            
            # High volatility (> 50% change)
            price_change = float(token.get('price_change_24h', 0) or 0)
            if abs(price_change) > 50:
                risk_score += 25
                risk_factors.append("High volatility")
            
            # Low volume relative to liquidity
            volume = float(token.get('volume_24h', 0) or 0)
            if liquidity > 0 and volume / liquidity < 0.1:
                risk_score += 20
                risk_factors.append("Low volume ratio")
            
            # Few transactions
            tx_count = token.get('transactions_24h', 0) or 0
            if tx_count < 50:
                risk_score += 15
                risk_factors.append("Low transaction count")
            
            # Meme token patterns
            symbol = token.get('symbol', '')
            name = token.get('name', '')
            if any(x in (symbol + name).lower() for x in ['moon', 'safe', 'elon', 'doge', 'shib', 'pepe', 'inu', 'cat', 'frog', 'baby']):
                risk_score += 15
                risk_factors.append("Meme token pattern")
            
            # Very new token (< 24 hours)
            created_at = token.get('created_at', '')
            if created_at:
                risk_score += 10
                risk_factors.append("Very new token")
            
            if risk_score >= 30:
                high_risk.append({
                    'token': symbol,
                    'name': name,
                    'price': token.get('price_usd', 0),
                    'liquidity': liquidity,
                    'volume_24h': volume,
                    'price_change_24h': price_change,
                    'holders': tx_count,  # Using tx count as proxy
                    'risk_score': min(risk_score, 100),
                    'risk_factors': risk_factors,
                    'contract': token.get('address', ''),
                    'chain': 'ethereum'
                })
        
        # Sort by risk score
        high_risk.sort(key=lambda x: x['risk_score'], reverse=True)
        return high_risk[:10]


def test_token_fetcher():
    """Test token fetching"""
    print("="*70)
    print("TESTING TOKEN FETCHER")
    print("="*70)
    
    fetcher = TokenFetcher()
    
    # Fetch from GeckoTerminal
    print("\n[1/2] Fetching tokens from GeckoTerminal...")
    tokens = fetcher.fetch_from_geckoterminal(network='eth', limit=30)
    print(f"[OK] Fetched {len(tokens)} tokens")
    
    if tokens:
        print("\nTop 5 tokens by liquidity:")
        sorted_tokens = sorted(tokens, key=lambda x: float(x.get('liquidity', 0) or 0), reverse=True)[:5]
        for t in sorted_tokens:
            liq = float(t.get('liquidity', 0) or 0)
            change = float(t.get('price_change_24h', 0) or 0)
            print(f"  {t['symbol']} ({t.get('quote_symbol', 'ETH')}): ${liq:,.0f} liquidity, {change:+.1f}%")
            print(f"    Address: {t.get('address', 'N/A')[:20]}...")
    
    # Identify high-risk tokens
    print("\n[2/2] Identifying high-risk tokens...")
    high_risk = fetcher.identify_high_risk_tokens(tokens)
    print(f"[OK] Found {len(high_risk)} high-risk tokens")
    
    if high_risk:
        print("\nHigh-risk tokens:")
        for t in high_risk[:5]:
            print(f"  {t['token']}: Risk={t['risk_score']}/100")
            print(f"    Factors: {', '.join(t['risk_factors'])}")
    
    print("\n" + "="*70)


if __name__ == "__main__":
    test_token_fetcher()
