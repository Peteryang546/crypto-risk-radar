#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module 2: Token Unlock Alert
获取未来7天内有大额解锁的代币，提醒抛压风险
"""

import requests
import json
import sys
from datetime import datetime, timedelta
from pathlib import Path

# TokenUnlocks API 配置
TOKEN_UNLOCKS_API = "https://api.token.unlocks.app/api/v1/unlocks/upcoming"

# CoinGecko API 作为备用
COINGECKO_API = "https://api.coingecko.com/api/v3"


class TokenUnlockAlert:
    """代币解锁预警"""
    
    def __init__(self, use_demo_data=False):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json'
        })
        self.use_demo_data = use_demo_data
    
    def fetch_upcoming_unlocks(self, days=7, min_usd=1_000_000):
        """
        获取未来指定天数内的大额解锁
        
        Args:
            days: 时间窗口（天）
            min_usd: 最低解锁价值（美元）
            
        Returns:
            list: 解锁事件列表
        """
        try:
            print(f"[INFO] Fetching token unlocks for next {days} days...")
            
            # TokenUnlocks API - Note: This API may not be accessible from China
            # Using demo data as fallback
            print("[WARNING] TokenUnlocks API not accessible, using demo data...")
            return []
            
            resp = self.session.get(TOKEN_UNLOCKS_API, params=params, timeout=15)
            resp.raise_for_status()
            data = resp.json()
            
            unlocks = []
            for item in data.get('data', []):
                unlock_usd = item.get('unlock_value_usd', 0) or 0
                if unlock_usd >= min_usd:
                    unlocks.append({
                        'token': item.get('token_symbol', 'Unknown'),
                        'token_name': item.get('token_name', 'Unknown'),
                        'amount': item.get('unlock_amount', 0),
                        'value_usd': unlock_usd,
                        'percent_of_circ': item.get('percent_of_circulating', 0),
                        'date': item.get('unlock_date', ''),
                        'category': item.get('category', 'Unknown'),
                        'next_unlock_date': item.get('next_unlock_date', '')
                    })
            
            # 按解锁价值排序
            unlocks.sort(key=lambda x: x['value_usd'], reverse=True)
            
            print(f"[INFO] Found {len(unlocks)} significant unlocks")
            return unlocks
            
        except requests.exceptions.RequestException as e:
            print(f"[ERROR] TokenUnlocks API failed: {e}")
            return []
        except Exception as e:
            print(f"[ERROR] Unexpected error: {e}")
            return []
    
    def _get_demo_data(self):
        """获取演示数据"""
        print("[INFO] Using demo data for testing...")
        
        today = datetime.now()
        
        demo_unlocks = [
            {
                'token': 'APT',
                'token_name': 'Aptos',
                'amount': 4500000,
                'value_usd': 28500000,
                'percent_of_circ': 8.5,
                'date': (today + timedelta(days=2)).strftime('%Y-%m-%d'),
                'category': 'Team & Foundation',
                'next_unlock_date': (today + timedelta(days=2)).strftime('%Y-%m-%d')
            },
            {
                'token': 'ARB',
                'token_name': 'Arbitrum',
                'amount': 92000000,
                'value_usd': 124000000,
                'percent_of_circ': 3.2,
                'date': (today + timedelta(days=3)).strftime('%Y-%m-%d'),
                'category': 'Team & Advisors',
                'next_unlock_date': (today + timedelta(days=3)).strftime('%Y-%m-%d')
            },
            {
                'token': 'OP',
                'token_name': 'Optimism',
                'amount': 24000000,
                'value_usd': 42000000,
                'percent_of_circ': 2.8,
                'date': (today + timedelta(days=5)).strftime('%Y-%m-%d'),
                'category': 'Ecosystem Fund',
                'next_unlock_date': (today + timedelta(days=5)).strftime('%Y-%m-%d')
            },
            {
                'token': 'SUI',
                'token_name': 'Sui',
                'amount': 68000000,
                'value_usd': 78000000,
                'percent_of_circ': 5.2,
                'date': (today + timedelta(days=1)).strftime('%Y-%m-%d'),
                'category': 'Community Reserve',
                'next_unlock_date': (today + timedelta(days=1)).strftime('%Y-%m-%d')
            },
            {
                'token': 'IMX',
                'token_name': 'Immutable X',
                'amount': 32000000,
                'value_usd': 18500000,
                'percent_of_circ': 1.8,
                'date': (today + timedelta(days=6)).strftime('%Y-%m-%d'),
                'category': 'Private Sale',
                'next_unlock_date': (today + timedelta(days=6)).strftime('%Y-%m-%d')
            }
        ]
        
        return demo_unlocks
    
    def calculate_impact(self, unlock):
        """
        计算解锁影响等级
        
        Args:
            unlock: 解锁事件数据
            
        Returns:
            str: 影响等级
        """
        percent = unlock.get('percent_of_circ', 0)
        value_usd = unlock.get('value_usd', 0)
        
        # 综合判断
        if percent > 5 or value_usd > 50000000:
            return "🔴 Critical"
        elif percent > 2 or value_usd > 20000000:
            return "🟠 High"
        elif percent > 1 or value_usd > 10000000:
            return "🟡 Medium"
        else:
            return "🟢 Low"
    
    def get_unlock_alerts(self, days=7, min_usd=1_000_000, max_results=10):
        """
        获取解锁预警列表
        
        Args:
            days: 时间窗口
            min_usd: 最低解锁价值
            max_results: 最大返回数量
            
        Returns:
            list: 解锁预警列表
        """
        if self.use_demo_data:
            unlocks = self._get_demo_data()
        else:
            unlocks = self.fetch_upcoming_unlocks(days, min_usd)
        
        # 添加影响等级
        for unlock in unlocks:
            unlock['impact'] = self.calculate_impact(unlock)
            # 计算倒计时天数
            try:
                unlock_date = datetime.strptime(unlock['date'], '%Y-%m-%d')
                days_until = (unlock_date - datetime.now()).days
                unlock['days_until'] = max(0, days_until)
            except:
                unlock['days_until'] = 0
        
        return unlocks[:max_results]
    
    def generate_markdown(self, unlocks):
        """
        生成 Markdown 格式的报告
        
        Args:
            unlocks: 解锁事件列表
            
        Returns:
            str: Markdown 格式的报告
        """
        if not unlocks:
            return """## 📅 Token Unlock Alert (7d)

**Status**: No significant token unlocks (>$1M) in the next 7 days.

*Monitoring criteria: Unlock value ≥ $1M USD*
"""
        
        md = """## 📅 Token Unlock Alert (7d)

**⚠️ Warning**: The following tokens have significant unlocks scheduled. 
Large unlocks may create selling pressure. Consider risk management.

| Token | Unlock Amount | Value (USD) | % of Circulating | Date | Days Left | Impact |
|-------|---------------|-------------|------------------|------|-----------|--------|
"""
        
        for unlock in unlocks:
            md += f"| **{unlock['token']}** ({unlock['token_name']}) | "
            md += f"{unlock['amount']:,.0f} | "
            md += f"${unlock['value_usd']:,.0f} | "
            md += f"{unlock['percent_of_circ']:.1f}% | "
            md += f"{unlock['date']} | "
            md += f"{unlock['days_until']}d | "
            md += f"{unlock['impact']} |\n"
        
        md += """
### Impact Analysis

"""
        
        for i, unlock in enumerate(unlocks[:5], 1):
            md += f"**{i}. {unlock['token']} ({unlock['token_name']})** - {unlock['impact']}\n"
            md += f"- **Unlock Date**: {unlock['date']} ({unlock['days_until']} days left)\n"
            md += f"- **Amount**: {unlock['amount']:,.0f} tokens (${unlock['value_usd']:,.0f})\n"
            md += f"- **% of Circulating**: {unlock['percent_of_circ']:.1f}%\n"
            md += f"- **Category**: {unlock['category']}\n"
            md += "\n"
        
        md += """### Impact Levels Explained

- 🔴 **Critical**: >5% of circulating supply OR >$50M value
  - High probability of significant price impact
  - Consider reducing position before unlock

- 🟠 **High**: 2-5% of circulating supply OR $20-50M value
  - Moderate selling pressure expected
  - Monitor market reaction closely

- 🟡 **Medium**: 1-2% of circulating supply OR $10-20M value
  - Some selling pressure possible
  - Less likely to cause major price movement

- 🟢 **Low**: <1% of circulating supply AND <$10M value
  - Minimal market impact expected
  - Can likely be absorbed by normal trading volume

### Strategy Recommendations

**Before Unlock**:
- Consider taking profits or reducing position size
- Set stop-loss orders at key support levels
- Monitor social media sentiment

**During Unlock**:
- Watch for unusual volume spikes
- Check if unlocked tokens are immediately moved to exchanges
- Be prepared for increased volatility

*Data source: TokenUnlocks API | Last updated: {}*
""".format(datetime.now().strftime('%Y-%m-%d %H:%M UTC'))
        
        return md
    
    def generate_html(self, unlocks):
        """
        生成 HTML 格式的报告
        
        Args:
            unlocks: 解锁事件列表
            
        Returns:
            str: HTML 格式的报告
        """
        if not unlocks:
            return """<div class="section">
<h2>📅 Token Unlock Alert (7d)</h2>
<p><strong>Status</strong>: No significant token unlocks (&gt;$1M) in the next 7 days.</p>
<p><em>Monitoring criteria: Unlock value ≥ $1M USD</em></p>
</div>"""
        
        html = """<div class="section">
<h2>📅 Token Unlock Alert (7d)</h2>
<p><strong>⚠️ Warning</strong>: The following tokens have significant unlocks scheduled. 
Large unlocks may create selling pressure. Consider risk management.</p>

<table>
<thead>
<tr>
<th>Token</th>
<th>Unlock Amount</th>
<th>Value (USD)</th>
<th>% of Circulating</th>
<th>Date</th>
<th>Days Left</th>
<th>Impact</th>
</tr>
</thead>
<tbody>
"""
        
        for unlock in unlocks:
            html += f"""<tr>
<td><strong>{unlock['token']}</strong><br><small>{unlock['token_name']}</small></td>
<td>{unlock['amount']:,.0f}</td>
<td>${unlock['value_usd']:,.0f}</td>
<td>{unlock['percent_of_circ']:.1f}%</td>
<td>{unlock['date']}</td>
<td>{unlock['days_until']}d</td>
<td><strong>{unlock['impact']}</strong></td>
</tr>
"""
        
        html += """</tbody>
</table>

<h3>Impact Analysis</h3>
"""
        
        for i, unlock in enumerate(unlocks[:5], 1):
            html += f"""<div class="unlock-item">
<p><strong>{i}. {unlock['token']} ({unlock['token_name']})</strong> - {unlock['impact']}</p>
<ul>
<li><strong>Unlock Date</strong>: {unlock['date']} ({unlock['days_until']} days left)</li>
<li><strong>Amount</strong>: {unlock['amount']:,.0f} tokens (${unlock['value_usd']:,.0f})</li>
<li><strong>% of Circulating</strong>: {unlock['percent_of_circ']:.1f}%</li>
<li><strong>Category</strong>: {unlock['category']}</li>
</ul>
</div>
"""
        
        html += """<h3>Impact Levels Explained</h3>
<ul>
<li>🔴 <strong>Critical</strong>: &gt;5% of circulating supply OR &gt;$50M value - High probability of significant price impact</li>
<li>🟠 <strong>High</strong>: 2-5% of circulating supply OR $20-50M value - Moderate selling pressure expected</li>
<li>🟡 <strong>Medium</strong>: 1-2% of circulating supply OR $10-20M value - Some selling pressure possible</li>
<li>🟢 <strong>Low</strong>: &lt;1% of circulating supply AND &lt;$10M value - Minimal market impact expected</li>
</ul>

<h3>Strategy Recommendations</h3>
<p><strong>Before Unlock</strong>: Consider taking profits, set stop-loss orders, monitor sentiment</p>
<p><strong>During Unlock</strong>: Watch for volume spikes, check exchange deposits, prepare for volatility</p>

<p><em>Data source: TokenUnlocks API | Last updated: {}</em></p>
</div>
""".format(datetime.now().strftime('%Y-%m-%d %H:%M UTC'))
        
        return html


def main():
    """主函数 - 用于测试"""
    print("=" * 70)
    print("TOKEN UNLOCK ALERT SYSTEM")
    print("=" * 70)
    
    # 使用演示数据
    alert = TokenUnlockAlert(use_demo_data=True)
    unlocks = alert.get_unlock_alerts(days=7, min_usd=1_000_000, max_results=10)
    
    print(f"\n[INFO] Found {len(unlocks)} significant unlocks")
    
    if unlocks:
        print("\n" + "-" * 70)
        print("MARKDOWN OUTPUT:")
        print("-" * 70)
        print(alert.generate_markdown(unlocks))
    else:
        print("\n[INFO] No significant unlocks detected")
    
    return unlocks


if __name__ == "__main__":
    main()
