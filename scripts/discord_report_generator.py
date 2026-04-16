#!/usr/bin/env python3
"""
区块链风险雷达 - Discord报告生成器 (同步版本)
整合12小时多维度信号分析
"""

import os
import sys
import json
import requests
from datetime import datetime, timedelta
from pathlib import Path

# 配置
BASE_DIR = Path("F:/stepclaw/agents/blockchain-analyst")
OUTPUT_DIR = BASE_DIR / "output"
DATA_DIR = OUTPUT_DIR / "data"

class BlockchainReportGenerator:
    """区块链报告生成器"""
    
    def __init__(self):
        self.etherscan_api_key = "T37QQ98EHJXE6B6YEA2ZG9KVSTXA4UGKGK"
        self.data = {}
        
    def fetch_data(self):
        """获取市场数据"""
        print("[INFO] Fetching market data...")
        
        # 1. CoinGecko 全局数据
        try:
            resp = requests.get(
                "https://api.coingecko.com/api/v3/global",
                timeout=10
            )
            if resp.status_code == 200:
                self.data['global'] = resp.json()
        except Exception as e:
            print(f"[WARN] CoinGecko error: {e}")
        
        # 2. 恐惧贪婪指数
        try:
            resp = requests.get(
                "https://api.alternative.me/fng/?limit=2",
                timeout=10
            )
            if resp.status_code == 200:
                result = resp.json()
                self.data['fear_greed'] = result.get('data', [])
        except Exception as e:
            print(f"[WARN] F&G error: {e}")
        
        # 3. BTC/ETH价格
        try:
            resp = requests.get(
                "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd&include_24hr_change=true",
                timeout=10
            )
            if resp.status_code == 200:
                self.data['prices'] = resp.json()
        except Exception as e:
            print(f"[WARN] Price error: {e}")
        
        print("[INFO] Data fetch complete")
    
    def analyze_signals(self):
        """分析信号"""
        signals = []
        
        # 1. 恐惧贪婪信号
        if 'fear_greed' in self.data and self.data['fear_greed']:
            fg = self.data['fear_greed'][0]
            value = int(fg.get('value', 50))
            label = fg.get('value_classification', 'Neutral')
            
            if value <= 20:
                signals.append({
                    'category': 'sentiment',
                    'type': 'extreme_fear',
                    'level': 'extreme',
                    'value': value,
                    'label': label,
                    'interpretation': f'Market in extreme fear ({value}/100). Historically indicates capitulation or continuation.',
                    'action': 'Wait for volume confirmation. Do NOT catch falling knives.',
                    'confidence': 85
                })
            elif value >= 75:
                signals.append({
                    'category': 'sentiment',
                    'type': 'extreme_greed',
                    'level': 'extreme',
                    'value': value,
                    'label': label,
                    'interpretation': f'Market in extreme greed ({value}/100). Distribution risk elevated.',
                    'action': 'Consider reducing exposure. High probability of correction.',
                    'confidence': 80
                })
        
        # 2. 市场结构信号
        if 'global' in self.data and 'data' in self.data['global']:
            global_data = self.data['global']['data']
            
            market_cap_change = global_data.get('market_cap_change_percentage_24h_usd', 0)
            if abs(market_cap_change) > 5:
                signals.append({
                    'category': 'market_structure',
                    'type': 'volatility_spike',
                    'level': 'high' if abs(market_cap_change) < 8 else 'extreme',
                    'value': market_cap_change,
                    'label': 'High Volatility',
                    'interpretation': f'Market cap {"surged" if market_cap_change > 0 else "dropped"} {abs(market_cap_change):.1f}% in 24h.',
                    'action': 'Watch for follow-through or reversal.',
                    'confidence': 75
                })
            
            btc_dominance = global_data.get('market_cap_percentage', {}).get('btc', 0)
            if btc_dominance > 55:
                signals.append({
                    'category': 'market_structure',
                    'type': 'btc_dominance',
                    'level': 'high',
                    'value': btc_dominance,
                    'label': 'BTC Dominance High',
                    'interpretation': f'BTC dominance at {btc_dominance:.1f}% - risk-off mode active.',
                    'action': 'Altcoin bleeding continues. Focus on BTC or stablecoins.',
                    'confidence': 80
                })
        
        # 3. 价格行为信号
        if 'prices' in self.data:
            btc = self.data['prices'].get('bitcoin', {})
            eth = self.data['prices'].get('ethereum', {})
            
            btc_change = btc.get('usd_24h_change', 0)
            eth_change = eth.get('usd_24h_change', 0)
            
            if btc_change > 2 and eth_change < btc_change - 1:
                signals.append({
                    'category': 'price_action',
                    'type': 'relative_weakness',
                    'level': 'high',
                    'value': {'btc': btc_change, 'eth': eth_change},
                    'label': 'ETH Lagging BTC',
                    'interpretation': f'BTC leading (+{btc_change:.1f}%) while ETH lagging (+{eth_change:.1f}%). Risk-off behavior.',
                    'action': 'Altcoin risk elevated. Monitor ETH/BTC ratio.',
                    'confidence': 75
                })
        
        return signals
    
    def calculate_risk_score(self, signals):
        """计算风险分数"""
        score = 0
        
        for signal in signals:
            weight = {'extreme': 2.0, 'high': 1.0, 'moderate': 0.5}.get(signal['level'], 0.5)
            confidence = signal['confidence'] / 100
            
            if signal['type'] in ['extreme_greed', 'btc_dominance']:
                score -= weight * confidence
            elif signal['type'] in ['extreme_fear']:
                score += weight * confidence * 0.5
            else:
                score -= weight * confidence * 0.3
        
        return max(-2.0, min(2.0, score))
    
    def generate_discord_report(self, signals, risk_score):
        """生成Discord报告"""
        
        now = datetime.utcnow()
        beijing_time = now + timedelta(hours=8)
        
        # 价格数据
        btc = self.data.get('prices', {}).get('bitcoin', {})
        eth = self.data.get('prices', {}).get('ethereum', {})
        
        btc_price = btc.get('usd', 0)
        btc_change = btc.get('usd_24h_change', 0)
        eth_price = eth.get('usd', 0)
        eth_change = eth.get('usd_24h_change', 0)
        
        # 恐惧贪婪
        fg_data = self.data.get('fear_greed', [{}])[0]
        fg_value = fg_data.get('value', 'N/A')
        fg_label = fg_data.get('value_classification', 'N/A')
        
        # 风险等级
        if risk_score <= -1.5:
            risk_level = '🔴 HIGH RISK'
            recommendation = 'AVOID NEW POSITIONS'
        elif risk_score <= -0.5:
            risk_level = '🟡 ELEVATED RISK'
            recommendation = 'REDUCE EXPOSURE'
        elif risk_score >= 1.0:
            risk_level = '🟢 BULLISH SETUP'
            recommendation = 'ACCUMULATE ON DIPS'
        else:
            risk_level = '⚪ NEUTRAL'
            recommendation = 'NORMAL CAUTION'
        
        # 分类信号
        sentiment = [s for s in signals if s['category'] == 'sentiment']
        market = [s for s in signals if s['category'] == 'market_structure']
        price = [s for s in signals if s['category'] == 'price_action']
        
        report = f"""# 🚨 Crypto Risk Radar – 12H Report
**{beijing_time.strftime('%Y-%m-%d %H:%M')} CST | {now.strftime('%H:%M')} UTC**

---

## 📊 Market Snapshot

| Asset | Price | 24h Change |
|-------|-------|------------|
| **BTC** | ${btc_price:,.0f} | {'🟢' if btc_change > 0 else '🔴'} {btc_change:+.2f}% |
| **ETH** | ${eth_price:,.0f} | {'🟢' if eth_change > 0 else '🔴'} {eth_change:+.2f}% |

**Fear & Greed**: {fg_value}/100 – *{fg_label}*

---

## 🎯 Multi-Dimensional Analysis

### Sentiment ({len(sentiment)} signals)
"""
        
        for s in sentiment:
            report += f"""
**{s['label']}** ({s['level'].upper()})
- {s['interpretation']}
- Action: {s['action']}
"""
        
        if not sentiment:
            report += "_No extreme sentiment readings._\n"
        
        report += f"""

### Market Structure ({len(market)} signals)
"""
        
        for s in market:
            report += f"""
**{s['label']}**
- {s['interpretation']}
- Action: {s['action']}
"""
        
        if not market:
            report += "_No significant market structure signals._\n"
        
        report += f"""

### Price Action ({len(price)} signals)
"""
        
        for s in price:
            report += f"""
**{s['label']}**
- {s['interpretation']}
- Action: {s['action']}
"""
        
        if not price:
            report += "_No significant price action signals._\n"
        
        report += f"""

---

## 🎲 Risk Assessment

**Overall Level**: {risk_level}
**Recommendation**: **{recommendation}**
**Risk Score**: {risk_score:+.1f}/2.0

---

## 📝 Bottom Line

"""
        
        if risk_score <= -1.0:
            report += """Multiple bearish signals converging. High-risk environment.

**Action Plan**:
1. DO NOT open new long positions
2. Reduce existing exposure by 20-50%
3. Keep 30%+ in stablecoins
4. Watch for capitulation volume

Risk elevated for next 12-24h."""
        elif risk_score >= 0.5:
            report += """Constructive setup with bullish signals emerging.

**Action Plan**:
1. Consider DCA entries on dips
2. Accumulate quality assets gradually
3. Avoid leverage – volatility high
4. Watch for follow-through

Setup valid for 24-48h."""
        else:
            report += """Mixed signals with no clear directional edge.

**Action Plan**:
1. Stay patient – no FOMO
2. Prepare watchlist for next move
3. Maintain balanced exposure
4. Watch for breakout/breakdown

Neutral stance for 12-24h."""
        
        report += """

---
*Risk analysis only. Not financial advice. DYOR.*
"""
        
        return report
    
    def save_report(self, report):
        """保存报告"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M')
        
        # 保存Markdown
        md_file = OUTPUT_DIR / f"discord_report_{timestamp}.md"
        with open(md_file, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"[SUCCESS] Report saved: {md_file}")
        
        # 保存JSON数据
        json_file = DATA_DIR / f"report_data_{timestamp}.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump({
                'timestamp': datetime.now().isoformat(),
                'data': self.data,
                'signals': self.signals if hasattr(self, 'signals') else []
            }, f, indent=2)
        
        return md_file

def main():
    """主函数"""
    generator = BlockchainReportGenerator()
    
    # 获取数据
    generator.fetch_data()
    
    # 分析信号
    print("[INFO] Analyzing signals...")
    signals = generator.analyze_signals()
    generator.signals = signals
    print(f"[INFO] Detected {len(signals)} signals")
    
    # 计算风险分数
    risk_score = generator.calculate_risk_score(signals)
    print(f"[INFO] Risk score: {risk_score:+.1f}")
    
    # 生成报告
    print("[INFO] Generating report...")
    report = generator.generate_discord_report(signals, risk_score)
    
    # 保存
    generator.save_report(report)
    
    # 打印预览
    print("\n" + "="*60)
    print("REPORT PREVIEW:")
    print("="*60)
    print(report[:1500])
    print("...")
    
    return report

if __name__ == '__main__':
    main()
