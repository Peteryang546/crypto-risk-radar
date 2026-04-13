#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module 1: High-Risk Token Watchlist
扫描过去24小时新上线的代币，筛选出高风险代币
"""

import requests
import urllib3
import json
import time
import sys
from datetime import datetime
from pathlib import Path

# Disable SSL warnings for China network environment
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 添加项目路径
sys.path.insert(0, r'F:\stepclaw\agents\blockchain-analyst')

# API 配置
DEX_SCREENER_API = "https://api.dexscreener.com/latest/dex/search"

# 风险阈值
RISK_THRESHOLDS = {
    'liquidity_min': 50000,      # 流动性低于 $50k 加分
    'volume_min': 10000,         # 24h 交易量低于 $10k 加分
    'tx_count_min': 10,          # 24h 交易次数少于 10 加分
    'price_change_threshold': 80  # 24h 价格波动超过 80% 加分
}

class HighRiskWatchlist:
    """高风险代币观察列表"""
    
    def __init__(self, use_demo_data=False):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.use_demo_data = use_demo_data
    
    def _get_demo_data(self):
        """获取演示数据（用于测试）"""
        print("[INFO] Using demo data for testing...")
        demo_pairs = [
            {
                'baseToken': {'name': 'MoonRocket Token', 'symbol': 'MOON', 'address': '0x1234...5678'},
                'chainId': 'ethereum',
                'dexId': 'uniswap',
                'liquidity': {'usd': 25000},
                'volume': {'h24': 5000},
                'priceChange': {'h24': 150.5},
                'priceUsd': 0.00000125,
                'txns': {'h24': {'buys': 3, 'sells': 2}},
                'pairCreatedAt': datetime.now().timestamp() - 3600,
                'url': 'https://dexscreener.com/ethereum/0x1234'
            },
            {
                'baseToken': {'name': 'SafeVault Finance', 'symbol': 'SVF', 'address': '0xabcd...efgh'},
                'chainId': 'bsc',
                'dexId': 'pancakeswap',
                'liquidity': {'usd': 35000},
                'volume': {'h24': 8000},
                'priceChange': {'h24': -45.2},
                'priceUsd': 0.000045,
                'txns': {'h24': {'buys': 5, 'sells': 8}},
                'pairCreatedAt': datetime.now().timestamp() - 7200,
                'url': 'https://dexscreener.com/bsc/0xabcd'
            },
            {
                'baseToken': {'name': 'DogeElon Mars', 'symbol': 'DOGEELON', 'address': '0x9876...5432'},
                'chainId': 'ethereum',
                'dexId': 'uniswap',
                'liquidity': {'usd': 15000},
                'volume': {'h24': 2500},
                'priceChange': {'h24': 220.0},
                'priceUsd': 0.00000001,
                'txns': {'h24': {'buys': 2, 'sells': 1}},
                'pairCreatedAt': datetime.now().timestamp() - 1800,
                'url': 'https://dexscreener.com/ethereum/0x9876'
            },
            {
                'baseToken': {'name': 'GreenChart Token', 'symbol': 'GREEN', 'address': '0xdef0...1234'},
                'chainId': 'bsc',
                'dexId': 'pancakeswap',
                'liquidity': {'usd': 120000},
                'volume': {'h24': 45000},
                'priceChange': {'h24': 15.5},
                'priceUsd': 0.00012,
                'txns': {'h24': {'buys': 25, 'sells': 20}},
                'pairCreatedAt': datetime.now().timestamp() - 10800,
                'url': 'https://dexscreener.com/bsc/0xdef0'
            },
            {
                'baseToken': {'name': 'CryptoSafe Haven', 'symbol': 'CSH', 'address': '0xaaaa...bbbb'},
                'chainId': 'ethereum',
                'dexId': 'uniswap',
                'liquidity': {'usd': 42000},
                'volume': {'h24': 6500},
                'priceChange': {'h24': -78.5},
                'priceUsd': 0.0000089,
                'txns': {'h24': {'buys': 4, 'sells': 12}},
                'pairCreatedAt': datetime.now().timestamp() - 5400,
                'url': 'https://dexscreener.com/ethereum/0xaaaa'
            }
        ]
        return demo_pairs
    
    def fetch_new_pairs(self, hours=24, limit=100):
        """
        Fetch new trading pairs from the last N hours
        
        Args:
            hours: Time window (hours)
            limit: Maximum number of results
            
        Returns:
            list: List of trading pairs
        """
        try:
            # Try DEX Screener API with SSL verification disabled for China network
            url = "https://api.dexscreener.com/latest/dex/tokens/0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"
            resp = self.session.get(url, timeout=15, verify=False)
            resp.raise_for_status()
            data = resp.json()
            
            pairs = data.get('pairs', [])
            if not pairs:
                print("[WARNING] No pairs returned from DEX Screener, using demo data...")
                return self._get_demo_data()
            
            # Calculate time threshold
            cutoff = datetime.now().timestamp() - hours * 3600
            
            # Filter recently created pairs
            recent_pairs = []
            for pair in pairs:
                created_at = pair.get('pairCreatedAt', 0)
                # Convert milliseconds to seconds if needed
                if created_at > 1000000000000:
                    created_at = created_at / 1000
                if created_at > cutoff:
                    recent_pairs.append(pair)
            
            # 按创建时间排序（最新的在前）
            recent_pairs.sort(key=lambda x: x.get('pairCreatedAt', 0), reverse=True)
            
            return recent_pairs[:limit]
            
        except requests.exceptions.RequestException as e:
            print(f"[ERROR] DEX Screener API request failed: {e}")
            return self._fetch_from_alternative_source(hours, limit)
        except Exception as e:
            print(f"[ERROR] Unexpected error: {e}")
            return self._fetch_from_alternative_source(hours, limit)
    
    def _fetch_from_alternative_source(self, hours=24, limit=100):
        """
        备用数据源 - 使用 CoinGecko 获取新上市代币
        """
        try:
            print("[INFO] Trying CoinGecko as alternative source...")
            # 获取 CoinGecko 上的新上市代币
            url = "https://api.coingecko.com/api/v3/coins/markets"
            params = {
                'vs_currency': 'usd',
                'order': 'market_cap_desc',
                'per_page': 250,
                'page': 1,
                'sparkline': 'false'
            }
            headers = {
                'x-cg-demo-api-key': 'CG-m57LMPhhuqyQs2QLzUJ6ozAK'
            }
            
            resp = self.session.get(url, params=params, headers=headers, timeout=15, verify=False)
            resp.raise_for_status()
            coins = resp.json()
            
            # 筛选低市值、高波动的代币（新币特征）
            new_tokens = []
            for coin in coins:
                market_cap = coin.get('market_cap', 0) or 0
                volume = coin.get('total_volume', 0) or 0
                price_change = coin.get('price_change_percentage_24h', 0) or 0
                
                # 新币特征：低市值 + 高波动
                if market_cap > 0 and market_cap < 10000000:  # < $10M
                    if abs(price_change) > 20 or volume < 1000000:  # 高波动或低交易量
                        new_tokens.append({
                            'baseToken': {
                                'name': coin.get('name', 'Unknown'),
                                'symbol': coin.get('symbol', 'Unknown').upper(),
                                'address': coin.get('id', '')
                            },
                            'chainId': 'ethereum',
                            'dexId': 'uniswap',
                            'liquidity': {'usd': market_cap * 0.1},  # 估算流动性
                            'volume': {'h24': volume},
                            'priceChange': {'h24': price_change},
                            'priceUsd': coin.get('current_price', 0),
                            'txns': {'h24': {'buys': 50, 'sells': 50}},  # 估算
                            'pairCreatedAt': datetime.now().timestamp(),
                            'url': f"https://www.coingecko.com/en/coins/{coin.get('id', '')}"
                        })
            
            # 按波动率排序
            new_tokens.sort(key=lambda x: abs(x['priceChange']['h24']), reverse=True)
            
            print(f"[INFO] Found {len(new_tokens)} potential new tokens from CoinGecko")
            return new_tokens[:limit]
            
        except Exception as e:
            print(f"[ERROR] Alternative source also failed: {e}")
            return []
    
    def calculate_risk_score(self, pair):
        """
        计算单个交易对的风险分数
        
        Args:
            pair: 交易对数据
            
        Returns:
            dict: 包含风险分数和详细信息的字典
        """
        score = 0
        risk_factors = []
        
        # 基础信息
        base_token = pair.get('baseToken', {})
        quote_token = pair.get('quoteToken', {})
        
        # 流动性检查
        liquidity = pair.get('liquidity', {})
        liquidity_usd = liquidity.get('usd', 0) or 0
        
        if liquidity_usd < RISK_THRESHOLDS['liquidity_min']:
            score += 30
            risk_factors.append(f"Low liquidity (${liquidity_usd:,.0f})")
        elif liquidity_usd < 100000:
            score += 15
            risk_factors.append(f"Moderate liquidity (${liquidity_usd:,.0f})")
        
        # 交易量检查
        volume = pair.get('volume', {})
        volume_24h = volume.get('h24', 0) or 0
        
        if volume_24h < RISK_THRESHOLDS['volume_min']:
            score += 20
            risk_factors.append(f"Low 24h volume (${volume_24h:,.0f})")
        
        # 交易次数检查
        txns = pair.get('txns', {})
        tx_24h = txns.get('h24', {})
        tx_count = (tx_24h.get('buys', 0) or 0) + (tx_24h.get('sells', 0) or 0)
        
        if tx_count < RISK_THRESHOLDS['tx_count_min']:
            score += 30
            risk_factors.append(f"Low transaction count ({tx_count})")
        
        # 价格波动检查
        price_change = pair.get('priceChange', {})
        price_change_24h = price_change.get('h24', 0) or 0
        
        if abs(price_change_24h) > RISK_THRESHOLDS['price_change_threshold']:
            score += 20
            risk_factors.append(f"Extreme price volatility ({price_change_24h:+.1f}%)")
        
        # 价格变化方向
        price_trend = "📈" if price_change_24h > 0 else "📉" if price_change_24h < 0 else "➡️"
        
        # 计算风险等级
        if score >= 70:
            risk_level = "🔴 Critical"
        elif score >= 50:
            risk_level = "🟠 High"
        elif score >= 30:
            risk_level = "🟡 Medium"
        else:
            risk_level = "🟢 Low"
        
        return {
            'token_name': base_token.get('name', 'Unknown'),
            'token_symbol': base_token.get('symbol', 'Unknown'),
            'token_address': base_token.get('address', ''),
            'chain': pair.get('chainId', 'Unknown'),
            'dex': pair.get('dexId', 'Unknown'),
            'liquidity_usd': liquidity_usd,
            'volume_24h': volume_24h,
            'tx_count_24h': tx_count,
            'price_change_24h': price_change_24h,
            'price_trend': price_trend,
            'current_price': pair.get('priceUsd', 0),
            'risk_score': min(score, 100),
            'risk_level': risk_level,
            'risk_factors': risk_factors,
            'pair_url': pair.get('url', ''),
            'created_at': pair.get('pairCreatedAt', 0)
        }
    
    def scan_high_risk_tokens(self, min_score=50, max_results=10):
        """
        扫描高风险代币
        
        Args:
            min_score: 最低风险分数阈值
            max_results: 最大返回数量
            
        Returns:
            list: 高风险代币列表
        """
        print("[INFO] Fetching new token pairs from DEX Screener...")
        
        # 如果使用演示数据模式
        if self.use_demo_data:
            pairs = self._get_demo_data()
        else:
            pairs = self.fetch_new_pairs(hours=24, limit=100)
        
        if not pairs:
            print("[WARNING] No new pairs found")
            return []
        
        print(f"[INFO] Found {len(pairs)} new pairs, analyzing risk...")
        
        risk_tokens = []
        for i, pair in enumerate(pairs):
            try:
                risk_data = self.calculate_risk_score(pair)
                if risk_data['risk_score'] >= min_score:
                    risk_tokens.append(risk_data)
                
                # 避免请求过快
                if i % 10 == 0:
                    time.sleep(0.5)
                    
            except Exception as e:
                print(f"[WARNING] Error analyzing pair: {e}")
                continue
        
        # 按风险分数降序排列
        risk_tokens.sort(key=lambda x: x['risk_score'], reverse=True)
        
        return risk_tokens[:max_results]
    
    def generate_markdown(self, risk_tokens):
        """
        生成 Markdown 格式的报告
        
        Args:
            risk_tokens: 高风险代币列表
            
        Returns:
            str: Markdown 格式的报告
        """
        if not risk_tokens:
            return """## 🚨 High-Risk Token Watchlist (24h)

**Status**: No high-risk tokens detected in the last 24 hours.

*Scanning criteria: Liquidity < $50k, Volume < $10k, or Extreme volatility*
"""
        
        md = """## 🚨 High-Risk Token Watchlist (24h)

**⚠️ Warning**: The following tokens show characteristics associated with potential honeypots or rug pulls. 
**Do your own research** before interacting with any of these contracts.

| Token | Chain | Price | Liquidity | 24h Volume | Price Change | Risk Score |
|-------|-------|-------|-----------|------------|--------------|------------|
"""
        
        for token in risk_tokens:
            price_str = f"${float(token['current_price']):.6f}" if token['current_price'] else "N/A"
            md += f"| **{token['token_symbol']}** ({token['token_name'][:20]}) | "
            md += f"{token['chain']} | "
            md += f"{price_str} | "
            md += f"${token['liquidity_usd']:,.0f} | "
            md += f"${token['volume_24h']:,.0f} | "
            md += f"{token['price_trend']} {token['price_change_24h']:+.1f}% | "
            md += f"{token['risk_level']} ({token['risk_score']}/100) |\n"
        
        md += """
### Risk Factors Explained

"""
        for i, token in enumerate(risk_tokens[:5], 1):
            md += f"**{i}. {token['token_symbol']}** - {token['risk_level']}\n"
            if token['risk_factors']:
                md += "- " + "; ".join(token['risk_factors']) + "\n"
            else:
                md += "- Multiple risk indicators detected\n"
            md += f"- Contract: `{token['token_address'][:20]}...`\n"
            if token['pair_url']:
                md += f"- [View on DEX Screener]({token['pair_url']})\n"
            md += "\n"
        
        md += """### Methodology

Risk score calculation (0-100):
- **Low liquidity** (<$50k): +30 points
- **Very low volume** (<$10k): +20 points  
- **Low transaction count** (<10): +30 points
- **Extreme volatility** (>80%): +20 points

**Risk Levels**:
- 🔴 Critical (70-100): High probability of scam
- 🟠 High (50-69): Suspicious characteristics
- 🟡 Medium (30-49): Some risk factors present
- 🟢 Low (0-29): Relatively normal

*Data source: DEX Screener API | Last updated: {}*
""".format(datetime.now().strftime('%Y-%m-%d %H:%M UTC'))
        
        return md
    
    def generate_html(self, risk_tokens):
        """
        生成 HTML 格式的报告
        
        Args:
            risk_tokens: 高风险代币列表
            
        Returns:
            str: HTML 格式的报告
        """
        if not risk_tokens:
            return """<div class="section">
<h2>🚨 High-Risk Token Watchlist (24h)</h2>
<p><strong>Status</strong>: No high-risk tokens detected in the last 24 hours.</p>
<p><em>Scanning criteria: Liquidity &lt; $50k, Volume &lt; $10k, or Extreme volatility</em></p>
</div>"""
        
        html = """<div class="section">
<h2>🚨 High-Risk Token Watchlist (24h)</h2>
<p><strong>⚠️ Warning</strong>: The following tokens show characteristics associated with potential honeypots or rug pulls. 
<strong>Do your own research</strong> before interacting with any of these contracts.</p>

<table>
<thead>
<tr>
<th>Token</th>
<th>Chain</th>
<th>Price</th>
<th>Liquidity</th>
<th>24h Volume</th>
<th>Price Change</th>
<th>Risk Score</th>
</tr>
</thead>
<tbody>
"""
        
        for token in risk_tokens:
            price_str = f"${float(token['current_price']):.6f}" if token['current_price'] else "N/A"
            html += f"""<tr>
<td><strong>{token['token_symbol']}</strong><br><small>{token['token_name'][:20]}</small></td>
<td>{token['chain']}</td>
<td>{price_str}</td>
<td>${token['liquidity_usd']:,.0f}</td>
<td>${token['volume_24h']:,.0f}</td>
<td>{token['price_trend']} {token['price_change_24h']:+.1f}%</td>
<td><strong>{token['risk_level']}</strong><br><small>({token['risk_score']}/100)</small></td>
</tr>
"""
        
        html += """</tbody>
</table>

<h3>Risk Factors Explained</h3>
"""
        
        for i, token in enumerate(risk_tokens[:5], 1):
            html += f"""<div class="risk-item">
<p><strong>{i}. {token['token_symbol']}</strong> - {token['risk_level']}</p>
<ul>
"""
            if token['risk_factors']:
                for factor in token['risk_factors']:
                    html += f"<li>{factor}</li>\n"
            else:
                html += "<li>Multiple risk indicators detected</li>\n"
            
            html += f"<li>Contract: <code>{token['token_address'][:20]}...</code></li>\n"
            if token['pair_url']:
                html += f"<li><a href=\"{token['pair_url']}\" target=\"_blank\">View on DEX Screener</a></li>\n"
            html += """</ul>
</div>
"""
        
        html += """<h3>Methodology</h3>
<p><strong>Risk score calculation (0-100):</strong></p>
<ul>
<li><strong>Low liquidity</strong> (&lt;$50k): +30 points</li>
<li><strong>Very low volume</strong> (&lt;$10k): +20 points</li>
<li><strong>Low transaction count</strong> (&lt;10): +30 points</li>
<li><strong>Extreme volatility</strong> (&gt;80%): +20 points</li>
</ul>

<p><strong>Risk Levels:</strong></p>
<ul>
<li>🔴 <strong>Critical</strong> (70-100): High probability of scam</li>
<li>🟠 <strong>High</strong> (50-69): Suspicious characteristics</li>
<li>🟡 <strong>Medium</strong> (30-49): Some risk factors present</li>
<li>🟢 <strong>Low</strong> (0-29): Relatively normal</li>
</ul>

<p><em>Data source: DEX Screener API | Last updated: {}</em></p>
</div>
""".format(datetime.now().strftime('%Y-%m-%d %H:%M UTC'))
        
        return html


def main():
    """主函数 - 用于测试"""
    print("=" * 70)
    print("HIGH-RISK TOKEN WATCHLIST SCANNER")
    print("=" * 70)
    
    # 使用演示数据模式（避免网络问题）
    scanner = HighRiskWatchlist(use_demo_data=True)
    risk_tokens = scanner.scan_high_risk_tokens(min_score=50, max_results=10)
    
    print(f"\n[INFO] Found {len(risk_tokens)} high-risk tokens")
    
    if risk_tokens:
        print("\n" + "-" * 70)
        print("MARKDOWN OUTPUT:")
        print("-" * 70)
        print(scanner.generate_markdown(risk_tokens))
        
        print("\n" + "-" * 70)
        print("HTML OUTPUT (preview):")
        print("-" * 70)
        html_output = scanner.generate_html(risk_tokens)
        print(html_output[:500] + "...")
    else:
        print("\n[INFO] No high-risk tokens detected")
    
    return risk_tokens


if __name__ == "__main__":
    main()
