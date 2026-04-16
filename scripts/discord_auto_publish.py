#!/usr/bin/env python3
"""
区块链风险雷达 - Discord自动发布脚本
定时发布12H综合报告到Discord
"""

import os
import sys
import json
import requests
from datetime import datetime, timedelta
from pathlib import Path
from dotenv import load_dotenv

# 加载环境变量
from dotenv import load_dotenv
env_path = Path(__file__).parent.parent / '.env'
if env_path.exists():
    load_dotenv(env_path)

# 配置
BASE_DIR = Path(__file__).parent.parent
OUTPUT_DIR = BASE_DIR / "output"
DATA_DIR = OUTPUT_DIR / "data"

# 从环境变量加载配置
DISCORD_WEBHOOK_URL = os.getenv('DISCORD_WEBHOOK_URL', '')
REQUIRE_APPROVAL = os.getenv('REQUIRE_APPROVAL_FOR_PUBLISH', 'true').lower() == 'true'

# 验证配置
if not DISCORD_WEBHOOK_URL:
    raise ValueError("DISCORD_WEBHOOK_URL environment variable is required")

class DiscordPublisher:
    """Discord发布器"""
    
    def __init__(self):
        self.webhook_url = DISCORD_WEBHOOK_URL
        if not self.webhook_url:
            raise ValueError("DISCORD_WEBHOOK_URL not configured")
    
    def fetch_market_data(self):
        """获取市场数据"""
        data = {}
        
        try:
            # CoinGecko 全局数据
            resp = requests.get(
                "https://api.coingecko.com/api/v3/global",
                timeout=10
            )
            if resp.status_code == 200:
                data['global'] = resp.json()
        except Exception as e:
            print(f"[WARN] Global data error: {e}")
        
        try:
            # 恐惧贪婪指数
            resp = requests.get(
                "https://api.alternative.me/fng/?limit=2",
                timeout=10
            )
            if resp.status_code == 200:
                result = resp.json()
                data['fear_greed'] = result.get('data', [])
        except Exception as e:
            print(f"[WARN] F&G error: {e}")
        
        try:
            # BTC/ETH价格
            resp = requests.get(
                "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd&include_24hr_change=true",
                timeout=10
            )
            if resp.status_code == 200:
                data['prices'] = resp.json()
        except Exception as e:
            print(f"[WARN] Price error: {e}")
        
        return data
    
    def analyze_signals(self, data):
        """分析信号"""
        signals = []
        
        # 恐惧贪婪信号
        if 'fear_greed' in data and data['fear_greed']:
            fg = data['fear_greed'][0]
            value = int(fg.get('value', 50))
            label = fg.get('value_classification', 'Neutral')
            
            if value <= 20:
                signals.append({
                    'emoji': '🔴',
                    'name': 'Extreme Fear',
                    'level': 'EXTREME',
                    'value': f'{value}/100',
                    'desc': f'Market in extreme fear ({value}/100). Historically indicates capitulation or continuation.',
                    'action': 'Wait for volume confirmation. Do NOT catch falling knives.'
                })
            elif value >= 75:
                signals.append({
                    'emoji': '🟢',
                    'name': 'Extreme Greed',
                    'level': 'EXTREME',
                    'value': f'{value}/100',
                    'desc': f'Market in extreme greed ({value}/100). Distribution risk elevated.',
                    'action': 'Consider taking profits. High probability of correction.'
                })
        
        # 市场结构信号
        if 'global' in data and 'data' in data['global']:
            global_data = data['global']['data']
            market_cap_change = global_data.get('market_cap_change_percentage_24h_usd', 0)
            
            if abs(market_cap_change) > 5:
                emoji = '🔴' if market_cap_change < 0 else '🟢'
                signals.append({
                    'emoji': emoji,
                    'name': 'High Volatility',
                    'level': 'HIGH',
                    'value': f'{market_cap_change:+.1f}%',
                    'desc': f'Market cap {"crashed" if market_cap_change < 0 else "surged"} {abs(market_cap_change):.1f}% in 24h.',
                    'action': 'Watch for follow-through or reversal.'
                })
            
            btc_dominance = global_data.get('market_cap_percentage', {}).get('btc', 0)
            if btc_dominance > 55:
                signals.append({
                    'emoji': '🟡',
                    'name': 'BTC Dominance High',
                    'level': 'HIGH',
                    'value': f'{btc_dominance:.1f}%',
                    'desc': f'BTC dominance at {btc_dominance:.1f}% - risk-off mode active.',
                    'action': 'Altcoin bleeding continues. Focus on BTC or stablecoins.'
                })
        
        # 价格行为信号
        if 'prices' in data:
            btc = data['prices'].get('bitcoin', {})
            eth = data['prices'].get('ethereum', {})
            btc_change = btc.get('usd_24h_change', 0)
            eth_change = eth.get('usd_24h_change', 0)
            
            if btc_change > 3 and eth_change < btc_change - 1:
                signals.append({
                    'emoji': '🟡',
                    'name': 'ETH Lagging BTC',
                    'level': 'MODERATE',
                    'value': f'BTC +{btc_change:.1f}%, ETH +{eth_change:.1f}%',
                    'desc': 'BTC leading while ETH lagging. Risk-off behavior.',
                    'action': 'Altcoin risk elevated. Monitor ETH/BTC ratio.'
                })
        
        return signals
    
    def calculate_risk_level(self, signals):
        """计算风险等级"""
        score = 0
        for s in signals:
            if s['level'] == 'EXTREME':
                score += 2 if 'Fear' in s['name'] else -2
            elif s['level'] == 'HIGH':
                score += 1 if 'Fear' in s['name'] else -1
        
        if score <= -2:
            return '🔴 HIGH RISK', 'AVOID NEW POSITIONS', score
        elif score <= -1:
            return '🟡 ELEVATED RISK', 'REDUCE EXPOSURE', score
        elif score >= 2:
            return '🟢 BULLISH SETUP', 'ACCUMULATE ON DIPS', score
        else:
            return '⚪ NEUTRAL', 'NORMAL CAUTION', score
    
    def generate_report(self, data, signals):
        """生成Discord报告"""
        
        now = datetime.utcnow()
        beijing_time = now + timedelta(hours=8)
        
        # 价格数据
        btc = data.get('prices', {}).get('bitcoin', {})
        eth = data.get('prices', {}).get('ethereum', {})
        
        btc_price = btc.get('usd', 0)
        btc_change = btc.get('usd_24h_change', 0)
        eth_price = eth.get('usd', 0)
        eth_change = eth.get('usd_24h_change', 0)
        
        # 恐惧贪婪
        fg_data = data.get('fear_greed', [{}])[0]
        fg_value = fg_data.get('value', 'N/A')
        fg_label = fg_data.get('value_classification', 'N/A')
        
        # 风险等级
        risk_level, recommendation, risk_score = self.calculate_risk_level(signals)
        
        # 构建报告
        report = f"""🚨 **Crypto Risk Radar - 12H Report**
📅 {beijing_time.strftime('%Y-%m-%d %H:%M')} CST | {now.strftime('%H:%M')} UTC

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 **Market Snapshot**
```
BTC: ${btc_price:,.0f} ({'+' if btc_change > 0 else ''}{btc_change:.2f}%)
ETH: ${eth_price:,.0f} ({'+' if eth_change > 0 else ''}{eth_change:.2f}%)
Fear & Greed: {fg_value}/100 - {fg_label}
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 **Key Signals Detected ({len(signals)})**
"""
        
        for s in signals:
            report += f"""
{s['emoji']} **{s['name']}** ({s['level']})
└ {s['desc']}
└ Action: {s['action']}
"""
        
        if not signals:
            report += "\n_No significant signals detected._\n"
        
        report += f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎲 **Risk Assessment**
```
Level: {risk_level}
Score: {risk_score}/10
Recommendation: {recommendation}
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📝 **Bottom Line**
"""
        
        if risk_score <= -1:
            report += """Multiple bearish signals converging. High-risk environment.

**Action Plan:**
1. ⛔ DO NOT open new long positions
2. 📉 Reduce exposure by 20-50%
3. 💰 Keep 30%+ in stablecoins
4. 👀 Watch for capitulation volume

_Risk elevated for next 12-24h_"""
        elif risk_score >= 1:
            report += """Constructive setup with bullish signals emerging.

**Action Plan:**
1. ✅ Consider DCA entries on dips
2. 📈 Accumulate quality assets
3. ⚠️ Avoid leverage
4. 👀 Watch for follow-through

_Setup valid for 24-48h_"""
        else:
            report += """Mixed signals with no clear directional edge.

**Action Plan:**
1. ⏸️ Stay patient - no FOMO
2. 📋 Prepare watchlist
3. ⚖️ Maintain balanced exposure
4. 👀 Watch for breakout/breakdown

_Neutral stance for 12-24h_"""
        
        report += """

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
_⚠️ Risk analysis only. Not financial advice. DYOR._
"""
        
        return report
    
    def publish_to_discord(self, content):
        """发布到Discord"""
        
        payload = {
            "content": content,
            "username": "Crypto Risk Radar"
        }
        
        try:
            resp = requests.post(
                self.webhook_url,
                json=payload,
                timeout=30
            )
            
            if resp.status_code == 204:
                print("[SUCCESS] Published to Discord")
                return True
            else:
                print(f"[ERROR] Failed to publish: {resp.status_code}")
                print(f"[ERROR] Response: {resp.text}")
                return False
                
        except Exception as e:
            print(f"[ERROR] Publish error: {e}")
            return False
    
    def save_report(self, content):
        """保存报告到本地"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M')
        
        # 保存Markdown
        md_file = OUTPUT_DIR / f"published_{timestamp}.md"
        with open(md_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"[INFO] Report saved: {md_file}")
        return md_file
    
    def run(self):
        """执行完整流程"""
        print("="*60)
        print("Crypto Risk Radar - Discord Publisher")
        print("="*60)
        
        # 1. 获取数据
        print("\n[1/4] Fetching market data...")
        data = self.fetch_market_data()
        
        # 2. 分析信号
        print("[2/4] Analyzing signals...")
        signals = self.analyze_signals(data)
        print(f"       Found {len(signals)} signals")
        
        # 3. 生成报告
        print("[3/4] Generating report...")
        report = self.generate_report(data, signals)
        
        # 4. 发布
        print("[4/4] Publishing to Discord...")
        success = self.publish_to_discord(report)
        
        # 保存本地副本
        self.save_report(report)
        
        print("\n" + "="*60)
        if success:
            print("✅ PUBLISH COMPLETE")
        else:
            print("❌ PUBLISH FAILED")
        print("="*60)
        
        return success

def main():
    """主函数"""
    try:
        publisher = DiscordPublisher()
        publisher.run()
    except Exception as e:
        print(f"[FATAL ERROR] {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
