#!/usr/bin/env python3
"""
Real Market Data Fetcher
Uses CoinGecko API for reliable real-time data
"""

import subprocess
import json
from datetime import datetime


def fetch_coin_gecko_data():
    """Fetch real market data from CoinGecko"""
    ps_code = '''
    try {
        # CoinGecko API - 获取市场数据
        $url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=100&page=1&sparkline=false&price_change_percentage=24h"
        $resp = Invoke-RestMethod -Uri $url -TimeoutSec 30
        
        # 转换为简化格式
        $coins = $resp | ForEach-Object {
            @{
                id = $_.id
                symbol = $_.symbol.ToUpper()
                name = $_.name
                current_price = $_.current_price
                market_cap = $_.market_cap
                total_volume = $_.total_volume
                price_change_24h = $_.price_change_percentage_24h
                circulating_supply = $_.circulating_supply
                last_updated = $_.last_updated
            }
        }
        
        @{ status = "success"; data = $coins } | ConvertTo-Json -Depth 10
    } catch {
        @{ status = "error"; message = $_.Exception.Message } | ConvertTo-Json
    }
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
        print(f"[ERROR] CoinGecko fetch failed: {e}")
    
    return []


def identify_high_risk_tokens(coins):
    """Identify high-risk tokens from market data"""
    high_risk = []
    
    for coin in coins:
        risk_score = 0
        risk_factors = []
        
        # Low market cap (< $100M - more lenient for top 100)
        market_cap = coin.get('market_cap', 0) or 0
        if market_cap < 100000000:
            risk_score += 20
            risk_factors.append("Low market cap")
        
        # High volatility (> 20% change - more sensitive)
        price_change = coin.get('price_change_24h', 0) or 0
        if abs(price_change) > 20:
            risk_score += 25
            risk_factors.append("High volatility")
        
        # Low volume relative to market cap
        volume = coin.get('total_volume', 0) or 0
        if market_cap > 0 and volume / market_cap < 0.03:
            risk_score += 20
            risk_factors.append("Low liquidity")
        
        # New/unknown tokens (check symbol patterns)
        symbol = coin.get('symbol', '')
        if any(x in symbol.lower() for x in ['moon', 'safe', 'elon', 'doge', 'shib', 'pepe', 'inu', 'cat', 'frog']):
            risk_score += 15
            risk_factors.append("Meme token pattern")
        
        # Negative price change
        if price_change < -10:
            risk_score += 10
            risk_factors.append("Price declining")
        
        if risk_score >= 40:
            high_risk.append({
                'token': symbol,
                'name': coin.get('name', 'Unknown'),
                'price': coin.get('current_price', 0),
                'market_cap': market_cap,
                'volume_24h': volume,
                'price_change_24h': price_change,
                'risk_score': min(risk_score, 100),
                'risk_factors': risk_factors
            })
    
    # Sort by risk score
    high_risk.sort(key=lambda x: x['risk_score'], reverse=True)
    return high_risk[:10]


def generate_market_summary(coins):
    """Generate market summary"""
    if not coins:
        return {}
    
    btc = next((c for c in coins if c['symbol'] == 'BTC'), {})
    eth = next((c for c in coins if c['symbol'] == 'ETH'), {})
    
    # Count gainers vs losers
    gainers = sum(1 for c in coins if (c.get('price_change_24h') or 0) > 0)
    losers = len(coins) - gainers
    
    return {
        'btc_price': btc.get('current_price', 0),
        'btc_change_24h': btc.get('price_change_24h', 0),
        'eth_price': eth.get('current_price', 0),
        'eth_change_24h': eth.get('price_change_24h', 0),
        'total_coins_analyzed': len(coins),
        'gainers': gainers,
        'losers': losers,
        'timestamp': datetime.now().isoformat()
    }


def main():
    """Fetch and process real market data"""
    print("="*70)
    print("FETCHING REAL MARKET DATA FROM COINGECKO")
    print("="*70)
    
    coins = fetch_coin_gecko_data()
    
    if not coins:
        print("[ERROR] Failed to fetch market data")
        return None
    
    print(f"[OK] Fetched {len(coins)} coins from CoinGecko")
    
    high_risk = identify_high_risk_tokens(coins)
    print(f"[OK] Identified {len(high_risk)} high-risk tokens")
    
    summary = generate_market_summary(coins)
    
    result = {
        'market_summary': summary,
        'high_risk_tokens': high_risk,
        'all_coins': coins[:20],  # Top 20 for reference
        'data_source': 'CoinGecko API',
        'timestamp': datetime.now().isoformat()
    }
    
    # Save to file
    with open('real_market_data.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    
    print("\n" + "="*70)
    print("MARKET SUMMARY")
    print("="*70)
    print(f"BTC: ${summary.get('btc_price', 0):,.2f} ({summary.get('btc_change_24h', 0):+.2f}%)")
    print(f"ETH: ${summary.get('eth_price', 0):,.2f} ({summary.get('eth_change_24h', 0):+.2f}%)")
    print(f"Gainers: {summary.get('gainers', 0)} | Losers: {summary.get('losers', 0)}")
    
    print("\n" + "="*70)
    print("TOP HIGH-RISK TOKENS")
    print("="*70)
    for token in high_risk[:5]:
        print(f"{token['token']}: Risk={token['risk_score']}/100, Price=${token['price']:.6f}, Change={token['price_change_24h']:+.1f}%")
        print(f"  Factors: {', '.join(token['risk_factors'])}")
    
    print("\n[OK] Data saved to real_market_data.json")
    return result


if __name__ == "__main__":
    main()
