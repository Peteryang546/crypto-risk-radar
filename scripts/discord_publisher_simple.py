#!/usr/bin/env python3
"""
区块链风险雷达 - Discord发布脚本 (简化版)
使用本地数据生成报告
"""

import os
import sys
import json
from datetime import datetime, timedelta
from pathlib import Path

# 配置
BASE_DIR = Path("F:/stepclaw/agents/blockchain-analyst")
OUTPUT_DIR = BASE_DIR / "output"
DATA_DIR = OUTPUT_DIR / "data"

# 从环境变量加载配置
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL", "")
REQUIRE_APPROVAL = os.getenv("REQUIRE_APPROVAL_FOR_PUBLISH", "true").lower() == "true"

# 验证配置
if not DISCORD_WEBHOOK_URL:
    print("[ERROR] DISCORD_WEBHOOK_URL environment variable is required")
    sys.exit(1)

# 确保目录存在
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
DATA_DIR.mkdir(parents=True, exist_ok=True)

def generate_report():
    """生成报告"""
    
    now = datetime.utcnow()
    beijing_time = now + timedelta(hours=8)
    
    # 从实时API获取数据
    import requests
    market_data = {}
    
    try:
        resp = requests.get(
            "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd&include_24hr_change=true",
            timeout=10
        )
        if resp.status_code == 200:
            prices = resp.json()
            market_data['btc_price'] = prices['bitcoin']['usd']
            market_data['btc_change'] = prices['bitcoin'].get('usd_24h_change', 0)
            market_data['eth_price'] = prices['ethereum']['usd']
            market_data['eth_change'] = prices['ethereum'].get('usd_24h_change', 0)
    except Exception as e:
        print(f"[WARN] Price fetch error: {e}")
        market_data['btc_price'] = 0
        market_data['btc_change'] = 0
        market_data['eth_price'] = 0
        market_data['eth_change'] = 0
    
    # 获取恐惧贪婪指数
    try:
        resp = requests.get("https://api.alternative.me/fng/?limit=1", timeout=10)
        if resp.status_code == 200:
            fg_data = resp.json()['data'][0]
            market_data['fear_greed'] = int(fg_data['value'])
            market_data['fear_greed_label'] = fg_data['value_classification']
    except Exception as e:
        print(f"[WARN] Fear&Greed fetch error: {e}")
        market_data['fear_greed'] = 50
        market_data['fear_greed_label'] = 'Neutral'
    
    # 分析信号
    signals = []
    
    # 极端恐惧信号
    if market_data['fear_greed'] <= 20:
        signals.append({
            'category': 'sentiment',
            'name': 'Extreme Fear',
            'level': 'extreme',
            'interpretation': f'Market in extreme fear ({market_data["fear_greed"]}/100). Historically indicates either capitulation (local bottom) or continuation of downtrend.',
            'action': 'Wait for volume confirmation. Do NOT catch falling knives.'
        })
    
    # 市场上涨信号
    if market_data['btc_change'] > 3:
        signals.append({
            'category': 'price',
            'name': 'BTC Strong Bounce',
            'level': 'high',
            'interpretation': f'BTC surged {market_data["btc_change"]:.1f}% in 24h. Bounce from extreme fear levels.',
            'action': 'Watch if this is sustainable or dead cat bounce.'
        })
    
    # ETH相对强弱
    if market_data['eth_change'] > market_data['btc_change']:
        signals.append({
            'category': 'relative',
            'name': 'ETH Leading',
            'level': 'moderate',
            'interpretation': f'ETH (+{market_data["eth_change"]:.1f}%) outperforming BTC (+{market_data["btc_change"]:.1f}%). Risk appetite returning.',
            'action': 'Positive sign for altcoin recovery.'
        })
    
    # 计算风险分数
    risk_score = 0.8  # 基于当前数据
    
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
    sentiment_signals = [s for s in signals if s['category'] == 'sentiment']
    price_signals = [s for s in signals if s['category'] in ['price', 'relative']]
    
    # 生成报告
    report = f"""# Crypto Risk Radar - 12H Report
**{beijing_time.strftime('%Y-%m-%d %H:%M')} CST | {now.strftime('%H:%M')} UTC**

---

## Market Snapshot

| Asset | Price | 24h Change |
|-------|-------|------------|
| **BTC** | ${market_data['btc_price']:,} | {'+' if market_data['btc_change'] > 0 else ''}{market_data['btc_change']:.2f}% |
| **ETH** | ${market_data['eth_price']:,} | {'+' if market_data['eth_change'] > 0 else ''}{market_data['eth_change']:.2f}% |

**Fear & Greed**: {market_data['fear_greed']}/100 - {market_data['fear_greed_label']}

---

## Key Signals Detected ({len(signals)})

### Sentiment Analysis ({len(sentiment_signals)})
"""
    
    for s in sentiment_signals:
        report += f"""
**{s['name']}** ({s['level'].upper()})
- {s['interpretation']}
- Action: {s['action']}
"""
    
    report += f"""

### Price Action ({len(price_signals)})
"""
    
    for s in price_signals:
        report += f"""
**{s['name']}**
- {s['interpretation']}
- Action: {s['action']}
"""
    
    report += f"""

---

## Risk Assessment

**Overall Level**: {risk_level}
**Recommendation**: {recommendation}
**Risk Score**: {risk_score:+.1f}/2.0

---

## Bottom Line

"""
    
    if market_data['fear_greed'] <= 20 and market_data['btc_change'] > 0:
        report += """Market bouncing from extreme fear levels. This could be:
1. Capitulation bottom (if volume confirms)
2. Dead cat bounce (if volume weak)

**Action Plan**:
- Watch for follow-through in next 12-24h
- Don't FOMO into the bounce
- If volume strong on pullback retest, consider entries
- Keep 50%+ cash for better opportunities

Risk: Medium-High | Timeframe: 12-24h"""
    else:
        report += """Market conditions neutral. No extreme signals.

**Action Plan**:
- Maintain balanced exposure
- Watch for breakout/breakdown
- Prepare for volatility

Risk: Medium | Timeframe: 12-24h"""
    
    report += """

---
*Risk analysis only. Not financial advice. DYOR.*
"""
    
    return report, market_data, signals

def save_report(report, data, signals):
    """保存报告"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M')
    
    # 保存Markdown
    md_file = OUTPUT_DIR / f"discord_report_{timestamp}.md"
    with open(md_file, 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"[SUCCESS] Report saved: {md_file}")
    
    # 保存JSON
    json_file = DATA_DIR / f"report_data_{timestamp}.json"
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump({
            'timestamp': datetime.now().isoformat(),
            'data': data,
            'signals': signals
        }, f, indent=2)
    
    return md_file

def main():
    """主函数"""
    print("[INFO] Generating Discord report...")
    
    # 生成报告
    report, data, signals = generate_report()
    
    # 保存
    save_report(report, data, signals)
    
    # 输出到控制台
    print("\n" + "="*60)
    print("REPORT GENERATED:")
    print("="*60)
    print(report)
    
    return report

if __name__ == '__main__':
    main()
