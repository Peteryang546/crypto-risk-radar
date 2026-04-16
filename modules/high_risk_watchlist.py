#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module 1: High-Risk Token Watchlist
扫描过去24小时新上线的代币，筛选出高风险代币
使用 PowerShell 绕过 Python SSL 问题
"""

import subprocess
import json
import sys
import time
from datetime import datetime
from pathlib import Path

# 添加项目路径
sys.path.insert(0, r'F:\stepclaw\agents\blockchain-analyst')

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
        self.use_demo_data = use_demo_data
    
    def _fetch_via_powershell(self):
        """使用 PowerShell 获取 DEX Screener 最新交易对数据"""
        ps_code = '''
        try {
            # 方法1: 获取 Ethereum 上 WETH 的最新交易对
            $resp = Invoke-RestMethod -Uri "https://api.dexscreener.com/latest/dex/pairs/ethereum/0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2" -TimeoutSec 30
            $pairs = $resp.pairs
            
            # 方法2: 如果方法1失败，获取所有链的最新代币
            if ($pairs.Count -eq 0 -or $pairs -eq $null) {
                Write-Host "[INFO] Trying alternative API endpoint..."
                # 获取热门代币列表
                $tokens = @("0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2", "0xdAC17F958D2ee523a2206206994597C13D831ec7")
                $allPairs = @()
                foreach ($token in $tokens) {
                    try {
                        $resp2 = Invoke-RestMethod -Uri "https://api.dexscreener.com/latest/dex/tokens/$token" -TimeoutSec 15
                        if ($resp2.pairs) {
                            $allPairs += $resp2.pairs
                        }
                    } catch {}
                }
                $pairs = $allPairs
            }
            
            # 排序并限制数量
            if ($pairs -and $pairs.Count -gt 0) {
                $sorted = $pairs | Sort-Object -Property { $_.pairCreatedAt } -Descending | Select-Object -First 50
                $sorted | ConvertTo-Json -Depth 10
            } else {
                Write-Output "[]"
            }
        } catch {
            Write-Output "[]"
        }
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
                if isinstance(data, list):
                    return data
                elif isinstance(data, dict):
                    return [data]
            return []
        except Exception as e:
            print(f"[ERROR] PowerShell fetch failed: {e}")
            return []
    
    def _get_demo_data(self):
        """获取演示数据（用于测试）"""
        print("[INFO] Using demo data for testing...")
        return [
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
            }
        ]
    
    def fetch_new_pairs(self, hours=24, limit=100):
        """Fetch new trading pairs"""
        if self.use_demo_data:
            return self._get_demo_data()
        
        print("[INFO] Fetching new token pairs via PowerShell...")
        pairs = self._fetch_via_powershell()
        
        if not pairs:
            print("[WARNING] No pairs returned, using demo data...")
            return self._get_demo_data()
        
        # Calculate time threshold
        cutoff = datetime.now().timestamp() - hours * 3600
        
        # Filter recently created pairs
        recent_pairs = []
        for pair in pairs:
            created_at = pair.get('pairCreatedAt', 0)
            if created_at > 1000000000000:
                created_at = created_at / 1000
            if created_at > cutoff:
                recent_pairs.append(pair)
        
        recent_pairs.sort(key=lambda x: x.get('pairCreatedAt', 0), reverse=True)
        return recent_pairs[:limit]
    
    def calculate_risk_score(self, pair):
        """计算单个交易对的风险分数"""
        score = 0
        risk_factors = []
        
        base_token = pair.get('baseToken', {})
        
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
        
        price_trend = "Up" if price_change_24h > 0 else "Down" if price_change_24h < 0 else "Flat"
        
        if score >= 70:
            risk_level = "Critical"
        elif score >= 50:
            risk_level = "High"
        elif score >= 30:
            risk_level = "Medium"
        else:
            risk_level = "Low"
        
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
        """扫描高风险代币"""
        print("[INFO] Fetching new token pairs...")
        pairs = self.fetch_new_pairs(hours=24, limit=100)
        
        if not pairs:
            print("[WARNING] No new pairs found")
            return []
        
        print(f"[INFO] Found {len(pairs)} new pairs, analyzing risk...")
        
        risk_tokens = []
        for pair in pairs:
            try:
                risk_data = self.calculate_risk_score(pair)
                if risk_data['risk_score'] >= min_score:
                    risk_tokens.append(risk_data)
            except Exception as e:
                print(f"[WARNING] Error analyzing pair: {e}")
                continue
        
        risk_tokens.sort(key=lambda x: x['risk_score'], reverse=True)
        return risk_tokens[:max_results]
    
    def generate_markdown(self, risk_tokens):
        """生成 Markdown 格式的报告"""
        if not risk_tokens:
            return """## High-Risk Token Watchlist (24h)

**Status**: No high-risk tokens detected in the last 24 hours.
"""
        
        md = """## High-Risk Token Watchlist (24h)

**Warning**: The following tokens show characteristics associated with potential risks.

| Token | Chain | Price | Liquidity | 24h Volume | Price Change | Risk Score |
|-------|-------|-------|-----------|------------|--------------|------------|
"""
        
        for token in risk_tokens:
            price_str = f"${float(token['current_price']):.6f}" if token['current_price'] else "N/A"
            md += f"| **{token['token_symbol']}** | {token['chain']} | {price_str} | ${token['liquidity_usd']:,.0f} | ${token['volume_24h']:,.0f} | {token['price_trend']} {token['price_change_24h']:+.1f}% | {token['risk_level']} ({token['risk_score']}/100) |\n"
        
        return md
    
    def generate_html(self, risk_tokens):
        """生成 HTML 格式的报告"""
        if not risk_tokens:
            return """<div class="section">
<h2>High-Risk Token Watchlist (24h)</h2>
<p><strong>Status</strong>: No high-risk tokens detected in the last 24 hours.</p>
</div>"""
        
        html = """<div class="section">
<h2>High-Risk Token Watchlist (24h)</h2>
<p><strong>Warning</strong>: The following tokens show characteristics associated with potential risks.</p>
<table>
<thead>
<tr><th>Token</th><th>Chain</th><th>Price</th><th>Liquidity</th><th>24h Volume</th><th>Price Change</th><th>Risk Score</th></tr>
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
</tr>"""
        
        html += "</tbody></table></div>"
        return html


def main():
    """主函数 - 用于测试"""
    print("=" * 70)
    print("HIGH-RISK TOKEN WATCHLIST SCANNER")
    print("=" * 70)
    
    scanner = HighRiskWatchlist(use_demo_data=False)
    risk_tokens = scanner.scan_high_risk_tokens(min_score=50, max_results=10)
    
    print(f"\n[INFO] Found {len(risk_tokens)} high-risk tokens")
    
    if risk_tokens:
        print("\n" + scanner.generate_markdown(risk_tokens))
    else:
        print("\n[INFO] No high-risk tokens detected")
    
    return risk_tokens


if __name__ == "__main__":
    main()
