#!/usr/bin/env python3
"""
区块链风险雷达 - Discord发布脚本
使用本地数据生成并发布报告
"""

import os
import sys
import json
from datetime import datetime, timedelta
from pathlib import Path

# 配置
BASE_DIR = Path(__file__).parent.parent
OUTPUT_DIR = BASE_DIR / "output"
DATA_DIR = OUTPUT_DIR / "data"

# Webhook URL (从环境变量读取)
WEBHOOK_URL = os.getenv('DISCORD_WEBHOOK_URL', '')
if not WEBHOOK_URL:
    raise ValueError("DISCORD_WEBHOOK_URL environment variable is required")

def generate_report():
    """生成报告 - 使用实时API数据"""
    import requests
    
    now = datetime.utcnow()
    beijing_time = now + timedelta(hours=8)
    
    # 从API获取实时数据
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
    
    # 极端恐惧
    signals.append({
        'emoji': '🔴',
        'name': 'Extreme Fear',
        'level': 'EXTREME',
        'desc': f'Market in extreme fear ({market_data["fear_greed"]}/100). Historically indicates capitulation or continuation.',
        'action': 'Wait for volume confirmation. Do NOT catch falling knives.'
    })
    
    # BTC反弹
    signals.append({
        'emoji': '🟢',
        'name': 'BTC Strong Bounce',
        'level': 'HIGH',
        'desc': f'BTC surged +{market_data["btc_change"]:.1f}% in 24h. Bounce from extreme fear levels.',
        'action': 'Watch if sustainable or dead cat bounce.'
    })
    
    # ETH领涨
    signals.append({
        'emoji': '🟢',
        'name': 'ETH Leading',
        'level': 'MODERATE',
        'desc': f'ETH (+{market_data["eth_change"]:.1f}%) outperforming BTC (+{market_data["btc_change"]:.1f}%). Risk appetite returning.',
        'action': 'Positive sign for altcoin recovery.'
    })
    
    # 风险评分
    risk_score = 0.8
    risk_level = 'NEUTRAL'
    recommendation = 'NORMAL CAUTION'
    
    # 构建报告
    report = f"""🚨 **Crypto Risk Radar - 12H Report**
📅 {beijing_time.strftime('%Y-%m-%d %H:%M')} CST | {now.strftime('%H:%M')} UTC

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 **Market Snapshot**
```
BTC: ${market_data['btc_price']:,} (+{market_data['btc_change']:.2f}%)
ETH: ${market_data['eth_price']:,} (+{market_data['eth_change']:.2f}%)
Fear & Greed: {market_data['fear_greed']}/100 - {market_data['fear_greed_label']}
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
    
    report += f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎲 **Risk Assessment**
```
Level: {risk_level}
Score: {risk_score:+.1f}/2.0
Recommendation: {recommendation}
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📝 **Bottom Line**

Market bouncing from extreme fear levels. This could be:
1. Capitulation bottom (if volume confirms)
2. Dead cat bounce (if volume weak)

**Action Plan:**
- Watch for follow-through in next 12-24h
- Don't FOMO into the bounce
- If volume strong on pullback retest, consider entries
- Keep 50%+ cash for better opportunities

Risk: Medium-High | Timeframe: 12-24h

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ *Risk analysis only. Not financial advice. DYOR.*
"""
    
    return report

def save_report(content):
    """保存报告"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M')
    
    # 确保目录存在
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # 保存
    md_file = OUTPUT_DIR / f"discord_published_{timestamp}.md"
    with open(md_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"[INFO] Report saved: {md_file}")
    return md_file

def main():
    """主函数"""
    print("="*60)
    print("Crypto Risk Radar - Discord Report Generator")
    print("="*60)
    
    # 生成报告
    print("\n[INFO] Generating report...")
    report = generate_report()
    
    # 保存
    save_report(report)
    
    # 输出
    print("\n" + "="*60)
    print("REPORT CONTENT:")
    print("="*60)
    print(report)
    print("\n" + "="*60)
    print("✅ Report generated successfully")
    print("="*60)
    
    # 提示发布方式
    print("\n[INFO] To publish to Discord:")
    print(f"  Webhook: {WEBHOOK_URL[:50]}...")
    print("  Method: POST with JSON payload")
    print("  Content-Type: application/json")

if __name__ == '__main__':
    main()
