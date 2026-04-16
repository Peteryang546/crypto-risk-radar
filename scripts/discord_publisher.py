#!/usr/bin/env python3
"""
区块链风险雷达 - Discord自动发布脚本
整合12小时内容，在美国时间对应时段发布
"""

import os
import sys
import json
import asyncio
import aiohttp
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional

# 配置
BASE_DIR = Path("F:/stepclaw/agents/blockchain-analyst")
OUTPUT_DIR = BASE_DIR / "output"

# 从环境变量加载Discord配置
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL", "")
DISCORD_CHANNEL_ID = os.getenv("DISCORD_CHANNEL_ID", "")

# 验证配置
if not DISCORD_WEBHOOK_URL:
    raise ValueError("DISCORD_WEBHOOK_URL environment variable is required")

# 发布前审批开关
REQUIRE_APPROVAL = os.getenv("REQUIRE_APPROVAL_FOR_PUBLISH", "true").lower() == "true"

class BlockchainRiskAnalyzer:
    """区块链风险分析器 - 整合多维度信号"""
    
    def __init__(self):
        self.data_cache = {}
        self.signals = []
        
    async def fetch_market_data(self) -> Dict:
        """获取市场数据"""
        async with aiohttp.ClientSession() as session:
            data = {}
            
            # 1. CoinGecko 全局数据
            try:
                async with session.get(
                    "https://api.coingecko.com/api/v3/global",
                    timeout=aiohttp.ClientTimeout(total=10)
                ) as resp:
                    if resp.status == 200:
                        data['global'] = await resp.json()
            except Exception as e:
                print(f"CoinGecko error: {e}")
            
            # 2. 恐惧贪婪指数
            try:
                async with session.get(
                    "https://api.alternative.me/fng/?limit=2",
                    timeout=aiohttp.ClientTimeout(total=10)
                ) as resp:
                    if resp.status == 200:
                        result = await resp.json()
                        data['fear_greed'] = result.get('data', [])
            except Exception as e:
                print(f"F&G error: {e}")
            
            # 3. BTC价格
            try:
                async with session.get(
                    "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd&include_24hr_change=true",
                    timeout=aiohttp.ClientTimeout(total=10)
                ) as resp:
                    if resp.status == 200:
                        data['prices'] = await resp.json()
            except Exception as e:
                print(f"Price error: {e}")
            
            return data
    
    def analyze_signals(self, data: Dict) -> List[Dict]:
        """分析多维度信号"""
        signals = []
        
        # 1. 市场情绪信号
        if 'fear_greed' in data and data['fear_greed']:
            fg = data['fear_greed'][0]
            value = int(fg.get('value', 50))
            
            if value <= 20:
                signals.append({
                    'type': 'sentiment',
                    'level': 'extreme_fear',
                    'value': value,
                    'label': fg.get('value_classification', 'Extreme Fear'),
                    'interpretation': 'Market in extreme fear - potential bottom signal OR further dump',
                    'action': 'Watch for capitulation volume'
                })
            elif value >= 80:
                signals.append({
                    'type': 'sentiment',
                    'level': 'extreme_greed',
                    'value': value,
                    'label': fg.get('value_classification', 'Extreme Greed'),
                    'interpretation': 'Market in extreme greed - distribution risk high',
                    'action': 'Consider taking profits'
                })
        
        # 2. 市场结构信号
        if 'global' in data and 'data' in data['global']:
            global_data = data['global']['data']
            
            # 总市值变化
            market_cap_change = global_data.get('market_cap_change_percentage_24h_usd', 0)
            if abs(market_cap_change) > 5:
                signals.append({
                    'type': 'market_structure',
                    'level': 'high_volatility',
                    'value': market_cap_change,
                    'label': 'High Volatility Alert',
                    'interpretation': f'Market cap {"surged" if market_cap_change > 0 else "dropped"} {abs(market_cap_change):.1f}% in 24h',
                    'action': 'Check leverage flush or FOMO entry'
                })
            
            # BTC dominance
            btc_dominance = global_data.get('market_cap_percentage', {}).get('btc', 0)
            if btc_dominance > 55:
                signals.append({
                    'type': 'market_structure',
                    'level': 'btc_dominance_high',
                    'value': btc_dominance,
                    'label': 'BTC Dominance Elevated',
                    'interpretation': 'Risk-off mode: capital fleeing to BTC safety',
                    'action': 'Altcoin bleeding likely to continue'
                })
        
        # 3. 价格行为信号
        if 'prices' in data:
            btc = data['prices'].get('bitcoin', {})
            eth = data['prices'].get('ethereum', {})
            
            btc_change = btc.get('usd_24h_change', 0)
            eth_change = eth.get('usd_24h_change', 0)
            
            # ETH/BTC ratio signal
            if btc_change > 2 and eth_change < btc_change - 1:
                signals.append({
                    'type': 'price_action',
                    'level': 'btc_leading',
                    'value': {'btc': btc_change, 'eth': eth_change},
                    'label': 'BTC Leading, ETH Lagging',
                    'interpretation': 'ETH showing relative weakness - altcoin risk elevated',
                    'action': 'Monitor ETH/BTC ratio for reversal'
                })
        
        return signals
    
    def generate_risk_assessment(self, signals: List[Dict]) -> Dict:
        """生成综合风险评估"""
        
        # 计算风险分数
        risk_score = 0
        risk_factors = []
        
        for signal in signals:
            if signal['level'] in ['extreme_fear', 'high_volatility']:
                risk_score += 2
                risk_factors.append(signal['label'])
            elif signal['level'] in ['extreme_greed', 'btc_dominance_high']:
                risk_score += 1
                risk_factors.append(signal['label'])
        
        # 风险等级
        if risk_score >= 4:
            risk_level = '🔴 HIGH RISK'
            recommendation = 'AVOID NEW POSITIONS'
        elif risk_score >= 2:
            risk_level = '🟡 ELEVATED RISK'
            recommendation = 'REDUCE EXPOSURE'
        else:
            risk_level = '🟢 MODERATE RISK'
            recommendation = 'NORMAL CAUTION'
        
        return {
            'score': risk_score,
            'level': risk_level,
            'recommendation': recommendation,
            'factors': risk_factors
        }

class DiscordPublisher:
    """Discord发布器"""
    
    def __init__(self, webhook_url: str = None):
        self.webhook_url = webhook_url or DISCORD_WEBHOOK_URL
        self.analyzer = BlockchainRiskAnalyzer()
    
    def format_message(self, data: Dict, signals: List[Dict], assessment: Dict, period: str = "12H") -> str:
        """格式化Discord消息"""
        
        # 获取当前时间
        now = datetime.utcnow()
        beijing_time = now + timedelta(hours=8)
        
        # 价格数据
        prices = data.get('prices', {})
        btc = prices.get('bitcoin', {})
        eth = prices.get('ethereum', {})
        
        btc_price = btc.get('usd', 0)
        btc_change = btc.get('usd_24h_change', 0)
        eth_price = eth.get('usd', 0)
        eth_change = eth.get('usd_24h_change', 0)
        
        # 恐惧贪婪
        fg_data = data.get('fear_greed', [{}])[0]
        fg_value = fg_data.get('value', 'N/A')
        fg_label = fg_data.get('value_classification', 'N/A')
        
        # 构建消息
        message = f"""# 🚨 Crypto Risk Radar – {period} Report
**{beijing_time.strftime('%Y-%m-%d %H:%M')} CST | {now.strftime('%H:%M')} UTC**

---

## 📊 Market Snapshot

| Asset | Price | 24h Change |
|-------|-------|------------|
| **BTC** | ${btc_price:,.0f} | {'🟢' if btc_change > 0 else '🔴'} {btc_change:+.2f}% |
| **ETH** | ${eth_price:,.0f} | {'🟢' if eth_change > 0 else '🔴'} {eth_change:+.2f}% |

**Fear & Greed Index**: {fg_value}/100 – *{fg_label}*

---

## ⚡ Key Signals Detected ({len(signals)})
"""
        
        # 添加信号详情
        for i, signal in enumerate(signals, 1):
            emoji = {
                'sentiment': '🎭',
                'market_structure': '📈',
                'price_action': '💰',
                'on_chain': '⛓️',
                'risk': '⚠️'
            }.get(signal['type'], '🔹')
            
            message += f"""
### {emoji} Signal {i}: {signal['label']}
**Interpretation**: {signal['interpretation']}
**Action**: {signal['action']}
"""
        
        # 添加风险评估
        message += f"""
---

## 🎯 Risk Assessment

**Overall Level**: {assessment['level']}
**Recommendation**: **{assessment['recommendation']}**
**Risk Score**: {assessment['score']}/10

**Key Risk Factors**:
"""
        
        if assessment['factors']:
            for factor in assessment['factors']:
                message += f"- {factor}\n"
        else:
            message += "- No major risk factors detected\n"
        
        # 添加结论
        message += f"""
---

## 📝 Bottom Line

"""
        
        if assessment['score'] >= 4:
            message += """Multiple risk signals are flashing. This is NOT a favorable environment for new positions. 
If you're already in positions, consider reducing exposure. If you're in cash, stay patient – better entries likely ahead."""
        elif assessment['score'] >= 2:
            message += """Market showing mixed signals with elevated risk. Proceed with caution.
Reduce position sizes and maintain tight risk management."""
        else:
            message += """Market conditions appear relatively stable. Normal caution advised.
Still watch for sudden volatility – crypto moves fast."""
        
        message += """

---
*This is risk analysis, not investment advice. DYOR.*
"""
        
        return message
    
    async def publish(self, period: str = "12H"):
        """发布到Discord"""
        
        # 获取数据
        data = await self.analyzer.fetch_market_data()
        
        # 分析信号
        signals = self.analyzer.analyze_signals(data)
        
        # 风险评估
        assessment = self.analyzer.generate_risk_assessment(signals)
        
        # 格式化消息
        message = self.format_message(data, signals, assessment, period)
        
        # 发送到Discord
        if self.webhook_url:
            async with aiohttp.ClientSession() as session:
                payload = {
                    "content": message,
                    "username": "Crypto Risk Radar"
                }
                
                try:
                    async with session.post(
                        self.webhook_url,
                        json=payload,
                        timeout=aiohttp.ClientTimeout(total=30)
                    ) as resp:
                        if resp.status == 204:
                            print(f"✅ Published {period} report to Discord")
                            return True
                        else:
                            print(f"❌ Failed to publish: {resp.status}")
                            return False
                except Exception as e:
                    print(f"❌ Publish error: {e}")
                    return False
        else:
            # 保存到文件（测试模式）
            output_file = OUTPUT_DIR / f"discord_report_{period}_{datetime.now().strftime('%Y%m%d_%H%M')}.md"
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(message)
            print(f"✅ Report saved to {output_file}")
            return True

def get_publish_times():
    """获取发布时间（对应美国时间）"""
    now = datetime.utcnow()
    
    # 美国东部时间 (UTC-4 或 UTC-5，取决于夏令时)
    # 北京时间 20:10 = UTC 12:10 = 美东 08:10 (早晨)
    # 北京时间 08:10 = UTC 00:10 = 美东 20:10 (晚上)
    
    morning_beijing = now.replace(hour=8, minute=10, second=0, microsecond=0)
    evening_beijing = now.replace(hour=20, minute=10, second=0, microsecond=0)
    
    # 如果当前时间已过，设置为明天
    if now > morning_beijing:
        morning_beijing += timedelta(days=1)
    if now > evening_beijing:
        evening_beijing += timedelta(days=1)
    
    return morning_beijing, evening_beijing

async def main():
    """主函数"""
    publisher = DiscordPublisher()
    
    # 获取发布时间
    morning_time, evening_time = get_publish_times()
    
    print(f"Next morning publish (08:10 CST): {morning_time}")
    print(f"Next evening publish (20:10 CST): {evening_time}")
    
    # 发布测试报告
    await publisher.publish("12H")

if __name__ == '__main__':
    asyncio.run(main())
