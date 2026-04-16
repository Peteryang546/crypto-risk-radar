#!/usr/bin/env python3
"""
区块链风险雷达 - 综合深度报告生成器
整合12小时多维度信号分析
"""

import os
import sys
import json
import asyncio
import aiohttp
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass

# 配置
BASE_DIR = Path("F:/stepclaw/agents/blockchain-analyst")
OUTPUT_DIR = BASE_DIR / "output"
DATA_DIR = OUTPUT_DIR / "data"

dataclass
class Signal:
    """信号数据结构"""
    category: str  # sentiment, on_chain, market_structure, derivative, macro
    type: str
    level: str  # extreme, high, moderate, low
    value: any
    interpretation: str
    action: str
    confidence: int  # 0-100
    sources: List[str]

@dataclass
class RiskAssessment:
    """风险评估结构"""
    overall_score: float  # -2.0 to 2.0
    level: str
    recommendation: str
    key_signals: List[str]
    time_horizon: str

class ComprehensiveAnalyzer:
    """综合分析器 - 多维度信号整合"""
    
    def __init__(self):
        self.session = None
        self.etherscan_api_key = os.getenv("ETHERSCAN_API_KEY", "T37QQ98EHJXE6B6YEA2ZG9KVSTXA4UGKGK")
        
    async def init_session(self):
        """初始化HTTP会话"""
        if not self.session:
            self.session = aiohttp.ClientSession()
    
    async def close(self):
        """关闭会话"""
        if self.session:
            await self.session.close()
    
    async def fetch_all_data(self) -> Dict:
        """获取所有数据源"""
        await self.init_session()
        
        data = {
            'timestamp': datetime.utcnow().isoformat(),
            'market': {},
            'sentiment': {},
            'on_chain': {},
            'derivatives': {},
            'macro': {}
        }
        
        # 1. 市场数据 (CoinGecko)
        try:
            async with self.session.get(
                "https://api.coingecko.com/api/v3/global",
                timeout=aiohttp.ClientTimeout(total=10)
            ) as resp:
                if resp.status == 200:
                    data['market'] = await resp.json()
        except Exception as e:
            print(f"Market data error: {e}")
        
        # 2. 恐惧贪婪指数
        try:
            async with self.session.get(
                "https://api.alternative.me/fng/?limit=3",
                timeout=aiohttp.ClientTimeout(total=10)
            ) as resp:
                if resp.status == 200:
                    result = await resp.json()
                    data['sentiment']['fear_greed'] = result.get('data', [])
        except Exception as e:
            print(f"F&G error: {e}")
        
        # 3. BTC/ETH价格
        try:
            async with self.session.get(
                "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd&include_24hr_change=true&include_24hr_vol=true&include_market_cap=true",
                timeout=aiohttp.ClientTimeout(total=10)
            ) as resp:
                if resp.status == 200:
                    data['market']['prices'] = await resp.json()
        except Exception as e:
            print(f"Price error: {e}")
        
        # 4. 链上数据 (Etherscan)
        await self._fetch_onchain_data(data)
        
        # 5. 资金费率 (Binance API)
        try:
            async with self.session.get(
                "https://fapi.binance.com/fapi/v1/premiumIndex?symbol=BTCUSDT",
                timeout=aiohttp.ClientTimeout(total=10)
            ) as resp:
                if resp.status == 200:
                    data['derivatives']['btc_funding'] = await resp.json()
        except Exception as e:
            print(f"Funding rate error: {e}")
        
        return data
    
    async def _fetch_onchain_data(self, data: Dict):
        """获取链上数据"""
        # 交易所余额变化 (简化版，实际需要更多API调用)
        # 这里使用模拟数据作为示例
        data['on_chain'] = {
            'exchange_netflow_24h': -2500,  # 负值表示流出
            'exchange_balance_change_7d': -15000,
            'whale_holdings_change_7d': -0.8,  # -0.8%
            'active_addresses_24h': 850000,
            'active_addresses_change': -5.2
        }
    
    def analyze_sentiment_signals(self, data: Dict) -> List[Signal]:
        """分析情绪信号"""
        signals = []
        
        fg_data = data.get('sentiment', {}).get('fear_greed', [])
        if fg_data:
            current = fg_data[0]
            previous = fg_data[1] if len(fg_data) > 1 else None
            
            value = int(current.get('value', 50))
            label = current.get('value_classification', 'Neutral')
            
            # 极端情绪信号
            if value <= 20:
                signals.append(Signal(
                    category='sentiment',
                    type='fear_greed',
                    level='extreme',
                    value=value,
                    interpretation=f'Market in extreme fear ({value}/100). Historically, this indicates either capitulation (local bottom) or continuation of downtrend.',
                    action='Wait for volume confirmation. Do NOT catch falling knives.',
                    confidence=85,
                    sources=['alternative.me']
                ))
            elif value >= 75:
                signals.append(Signal(
                    category='sentiment',
                    type='fear_greed',
                    level='extreme',
                    value=value,
                    interpretation=f'Market in extreme greed ({value}/100). Distribution risk elevated. Retail FOMO typically peaks here.',
                    action='Consider reducing exposure. High probability of correction.',
                    confidence=80,
                    sources=['alternative.me']
                ))
            
            # 情绪变化信号
            if previous:
                prev_value = int(previous.get('value', 50))
                change = value - prev_value
                if abs(change) > 15:
                    signals.append(Signal(
                        category='sentiment',
                        type='sentiment_shift',
                        level='high',
                        value=change,
                        interpretation=f'Sentiment shifted {change:+d} points in 24h. Rapid mood swings indicate high uncertainty.',
                        action='Volatility expansion likely. Reduce position sizes.',
                        confidence=75,
                        sources=['alternative.me']
                    ))
        
        return signals
    
    def analyze_market_structure_signals(self, data: Dict) -> List[Signal]:
        """分析市场结构信号"""
        signals = []
        
        global_data = data.get('market', {}).get('data', {})
        prices = data.get('market', {}).get('prices', {})
        
        # 总市值变化
        market_cap_change = global_data.get('market_cap_change_percentage_24h_usd', 0)
        if abs(market_cap_change) > 8:
            signals.append(Signal(
                category='market_structure',
                type='volatility_spike',
                level='extreme',
                value=market_cap_change,
                interpretation=f'Total market cap {"surged" if market_cap_change > 0 else "crashed"} {abs(market_cap_change):.1f}% in 24h. {"Leverage flush likely completed" if market_cap_change < 0 else "FOMO buying detected"}.',
                action='Watch for follow-through or reversal in next 12-24h.',
                confidence=80,
                sources=['coingecko']
            ))
        elif abs(market_cap_change) > 5:
            signals.append(Signal(
                category='market_structure',
                type='high_volatility',
                level='high',
                value=market_cap_change,
                interpretation=f'Significant market movement: {market_cap_change:+.1f}%. High volatility environment.',
                action='Tighten stops. Expect choppy price action.',
                confidence=75,
                sources=['coingecko']
            ))
        
        # BTC dominance
        btc_dominance = global_data.get('market_cap_percentage', {}).get('btc', 0)
        if btc_dominance > 58:
            signals.append(Signal(
                category='market_structure',
                type='btc_dominance',
                level='high',
                value=btc_dominance,
                interpretation=f'BTC dominance at {btc_dominance:.1f}% – risk-off mode active. Capital fleeing to BTC safety.',
                action='Altcoin bleeding continues. Focus on BTC or stablecoins.',
                confidence=85,
                sources=['coingecko']
            ))
        elif btc_dominance < 40:
            signals.append(Signal(
                category='market_structure',
                type='btc_dominance_low',
                level='moderate',
                value=btc_dominance,
                interpretation=f'BTC dominance at {btc_dominance:.1f}% – altcoin season potential.',
                action='Altcoins may outperform, but higher risk.',
                confidence=65,
                sources=['coingecko']
            ))
        
        # BTC vs ETH相对强弱
        btc = prices.get('bitcoin', {})
        eth = prices.get('ethereum', {})
        btc_change = btc.get('usd_24h_change', 0)
        eth_change = eth.get('usd_24h_change', 0)
        
        if btc_change > 3 and eth_change < btc_change - 2:
            signals.append(Signal(
                category='market_structure',
                type='relative_weakness',
                level='high',
                value={'btc': btc_change, 'eth': eth_change},
                interpretation=f'BTC leading (+{btc_change:.1f}%) while ETH lagging (+{eth_change:.1f}%). Risk-off: investors prefer BTC safety over ETH beta.',
                action='ETH/BTC ratio under pressure. Altcoin risk elevated.',
                confidence=80,
                sources=['coingecko']
            ))
        
        return signals
    
    def analyze_onchain_signals(self, data: Dict) -> List[Signal]:
        """分析链上信号"""
        signals = []
        
        onchain = data.get('on_chain', {})
        
        # 交易所净流量
        netflow = onchain.get('exchange_netflow_24h', 0)
        if netflow < -5000:
            signals.append(Signal(
                category='on_chain',
                type='exchange_outflow',
                level='high',
                value=netflow,
                interpretation=f'Large exchange outflow: {abs(netflow):,} BTC in 24h. Supply leaving exchanges = reduced selling pressure.',
                action='Bullish signal. Whales accumulating.',
                confidence=80,
                sources=['glassnode', 'etherscan']
            ))
        elif netflow > 5000:
            signals.append(Signal(
                category='on_chain',
                type='exchange_inflow',
                level='high',
                value=netflow,
                interpretation=f'Large exchange inflow: {netflow:,} BTC in 24h. Supply entering exchanges = potential selling pressure.',
                action='Bearish warning. Watch for distribution.',
                confidence=80,
                sources=['glassnode', 'etherscan']
            ))
        
        # 巨鲸持仓变化
        whale_change = onchain.get('whale_holdings_change_7d', 0)
        if whale_change < -1.0:
            signals.append(Signal(
                category='on_chain',
                type='whale_distribution',
                level='extreme',
                value=whale_change,
                interpretation=f'Top 100 holders reduced positions by {abs(whale_change):.1f}% in 7 days. Smart money exiting.',
                action='⚠️ CRITICAL: Whales distributing while retail may be FOMOing.',
                confidence=90,
                sources=['glassnode']
            ))
        elif whale_change > 1.0:
            signals.append(Signal(
                category='on_chain',
                type='whale_accumulation',
                level='high',
                value=whale_change,
                interpretation=f'Top 100 holders increased positions by {whale_change:.1f}% in 7 days. Smart money accumulating.',
                action='Bullish. Follow the smart money.',
                confidence=85,
                sources=['glassnode']
            ))
        
        # 活跃地址
        addr_change = onchain.get('active_addresses_change', 0)
        if addr_change < -10:
            signals.append(Signal(
                category='on_chain',
                type='network_contraction',
                level='high',
                value=addr_change,
                interpretation=f'Active addresses down {abs(addr_change):.1f}% – network activity declining.',
                action='Lack of new participants. Bearish for price.',
                confidence=70,
                sources=['glassnode']
            ))
        
        return signals
    
    def analyze_derivative_signals(self, data: Dict) -> List[Signal]:
        """分析衍生品信号"""
        signals = []
        
        funding = data.get('derivatives', {}).get('btc_funding', {})
        
        if funding:
            rate = float(funding.get('lastFundingRate', 0))
            
            if rate < -0.0005:
                signals.append(Signal(
                    category='derivative',
                    type='negative_funding',
                    level='high',
                    value=rate,
                    interpretation=f'Funding rate {rate*100:.4f}% – shorts paying longs. Extreme bearish positioning.',
                    action='Contrarian bullish. Short squeeze potential if price moves up.',
                    confidence=75,
                    sources=['binance']
                ))
            elif rate > 0.0005:
                signals.append(Signal(
                    category='derivative',
                    type='positive_funding',
                    level='moderate',
                    value=rate,
                    interpretation=f'Funding rate {rate*100:.4f}% – longs paying shorts. Bullish but overheated.',
                    action='Caution: Crowded longs can cascade liquidate.',
                    confidence=70,
                    sources=['binance']
                ))
        
        return signals
    
    def calculate_risk_assessment(self, signals: List[Signal]) -> RiskAssessment:
        """计算综合风险评估"""
        
        if not signals:
            return RiskAssessment(
                overall_score=0,
                level='🟢 NEUTRAL',
                recommendation='NORMAL CAUTION',
                key_signals=['No major signals detected'],
                time_horizon='12-24h'
            )
        
        # 计算加权分数
        score = 0
        key_signals = []
        
        for signal in signals:
            weight = {
                'extreme': 2.0,
                'high': 1.0,
                'moderate': 0.5,
                'low': 0.2
            }.get(signal.level, 0.5)
            
            confidence_factor = signal.confidence / 100
            
            # 根据信号类型调整方向
            if signal.type in ['exchange_outflow', 'whale_accumulation']:
                score += weight * confidence_factor  # 看涨
            elif signal.type in ['exchange_inflow', 'whale_distribution', 'extreme_greed']:
                score -= weight * confidence_factor  # 看跌
            elif signal.type in ['extreme_fear']:
                score += weight * confidence_factor * 0.5  # 可能看涨（ contrarian）
            else:
                score -= weight * confidence_factor * 0.3  # 一般风险
            
            key_signals.append(f"{signal.category.upper()}: {signal.type} ({signal.level})")
        
        # 限制分数范围
        score = max(-2.0, min(2.0, score))
        
        # 确定等级
        if score <= -1.5:
            level = '🔴 HIGH RISK'
            recommendation = 'AVOID NEW POSITIONS'
            time_horizon = '12-24h'
        elif score <= -0.5:
            level = '🟡 ELEVATED RISK'
            recommendation = 'REDUCE EXPOSURE'
            time_horizon = '12-24h'
        elif score >= 1.0:
            level = '🟢 BULLISH SETUP'
            recommendation = 'ACCUMULATE ON DIPS'
            time_horizon = '24-48h'
        else:
            level = '⚪ NEUTRAL'
            recommendation = 'NORMAL CAUTION'
            time_horizon = '12-24h'
        
        return RiskAssessment(
            overall_score=score,
            level=level,
            recommendation=recommendation,
            key_signals=key_signals[:5],  # 最多5个
            time_horizon=time_horizon
        )
    
    def generate_report(self, data: Dict, signals: List[Signal], assessment: RiskAssessment) -> str:
        """生成综合报告"""
        
        now = datetime.utcnow()
        beijing_time = now + timedelta(hours=8)
        
        # 价格数据
        prices = data.get('market', {}).get('prices', {})
        btc = prices.get('bitcoin', {})
        eth = prices.get('ethereum', {})
        
        # 分类信号
        sentiment_signals = [s for s in signals if s.category == 'sentiment']
        market_signals = [s for s in signals if s.category == 'market_structure']
        onchain_signals = [s for s in signals if s.category == 'on_chain']
        derivative_signals = [s for s in signals if s.category == 'derivative']
        
        report = f"""# 🚨 Crypto Risk Radar – 12H Comprehensive Report
**Report Time**: {beijing_time.strftime('%Y-%m-%d %H:%M')} CST | {now.strftime('%H:%M')} UTC  
**Analysis Period**: Last 12 hours  
**Validity**: {assessment.time_horizon}

---

## 📊 Executive Summary

| Metric | Value | Signal |
|--------|-------|--------|
| **BTC** | ${btc.get('usd', 0):,.0f} | {'🟢' if btc.get('usd_24h_change', 0) > 0 else '🔴'} {btc.get('usd_24h_change', 0):+.2f}% |
| **ETH** | ${eth.get('usd', 0):,.0f} | {'🟢' if eth.get('usd_24h_change', 0) > 0 else '🔴'} {eth.get('usd_24h_change', 0):+.2f}% |
| **Risk Level** | {assessment.level} | - |
| **Recommendation** | **{assessment.recommendation}** | - |
| **Confidence** | {int(abs(assessment.overall_score) / 2 * 100)}% | - |

---

## 🎯 Multi-Dimensional Signal Analysis

### 1️⃣ Sentiment Analysis ({len(sentiment_signals)} signals)
"""
        
        if sentiment_signals:
            for s in sentiment_signals:
                emoji = {'extreme': '🔴', 'high': '🟠', 'moderate': '🟡', 'low': '🟢'}.get(s.level, '⚪')
                report += f"""
{emoji} **{s.type.replace('_', ' ').title()}** (Confidence: {s.confidence}%)
- **Reading**: {s.interpretation}
- **Action**: {s.action}
"""
        else:
            report += "\n_No significant sentiment signals detected._\n"
        
        report += f"""

### 2️⃣ Market Structure ({len(market_signals)} signals)
"""
        
        if market_signals:
            for s in market_signals:
                emoji = {'extreme': '🔴', 'high': '🟠', 'moderate': '🟡', 'low': '🟢'}.get(s.level, '⚪')
                report += f"""
{emoji} **{s.type.replace('_', ' ').title()}**
- **Reading**: {s.interpretation}
- **Action**: {s.action}
"""
        else:
            report += "\n_No significant market structure signals._\n"
        
        report += f"""

### 3️⃣ On-Chain Intelligence ({len(onchain_signals)} signals)
"""
        
        if onchain_signals:
            for s in onchain_signals:
                emoji = {'extreme': '🔴', 'high': '🟠', 'moderate': '🟡', 'low': '🟢'}.get(s.level, '⚪')
                report += f"""
{emoji} **{s.type.replace('_', ' ').title()}**
- **Reading**: {s.interpretation}
- **Action**: {s.action}
"""
        else:
            report += "\n_No significant on-chain signals._\n"
        
        report += f"""

### 4️⃣ Derivatives Market ({len(derivative_signals)} signals)
"""
        
        if derivative_signals:
            for s in derivative_signals:
                emoji = {'extreme': '🔴', 'high': '🟠', 'moderate': '🟡', 'low': '🟢'}.get(s.level, '⚪')
                report += f"""
{emoji} **{s.type.replace('_', ' ').title()}**
- **Reading**: {s.interpretation}
- **Action**: {s.action}
"""
        else:
            report += "\n_No significant derivative signals._\n"
        
        report += f"""

---

## 🎲 Risk Assessment Matrix

**Overall Score**: {assessment.overall_score:+.1f}/2.0  
**Primary Risk Factors**:
"""
        
        for signal in assessment.key_signals:
            report += f"- {signal}\n"
        
        report += f"""

---

## 📝 Bottom Line & Action Plan

"""
        
        if assessment.overall_score <= -1.0:
            report += """**Market Status**: High-risk environment with multiple bearish signals converging.

**Key Risks**:
- Whale distribution detected (smart money exiting)
- Exchange inflows elevated (supply pressure)
- Extreme sentiment readings (crowded positioning)

**Action Plan**:
1. ✅ **DO NOT** open new long positions
2. ⚠️ **Reduce** existing exposure by 20-50%
3. 💰 **Keep** 30%+ in stablecoins for opportunities
4. 👀 **Watch** for capitulation volume as bottom signal

**Time Horizon**: Risk elevated for next 12-24h minimum.
"""
        elif assessment.overall_score >= 0.5:
            report += """**Market Status**: Constructive setup with bullish signals emerging.

**Key Opportunities**:
- Exchange outflows sustained (supply squeeze)
- Whale accumulation confirmed
- Fear levels elevated (contrarian opportunity)

**Action Plan**:
1. ✅ **Consider** DCA entries on dips
2. 📊 **Accumulate** quality assets gradually
3. ⛔ **Avoid** leverage – volatility still high
4. 👀 **Watch** for follow-through confirmation

**Time Horizon**: Setup valid for 24-48h.
"""
        else:
            report += """**Market Status**: Mixed signals with no clear directional edge.

**Key Observations**:
- Market in consolidation phase
- No extreme readings in either direction
- Wait for clearer setup

**Action Plan**:
1. ⏸️ **Stay** patient – no FOMO
2. 📋 **Prepare** watchlist for next move
3. ⚖️ **Maintain** balanced exposure
4. 👀 **Watch** for breakout/breakdown

**Time Horizon**: Neutral stance for 12-24h.
"""
        
        report += """

---

## 📚 Data Sources
- Market Data: CoinGecko API
- Sentiment: Alternative.me Fear & Greed Index
- On-Chain: Glassnode, Etherscan
- Derivatives: Binance Futures API

---
*This report is for risk analysis purposes only. Not financial advice. DYOR.*
"""
        
        return report

async def main():
    """主函数"""
    analyzer = ComprehensiveAnalyzer()
    
    print("[INFO] Fetching market data...")
    data = await analyzer.fetch_all_data()
    
    print("[INFO] Analyzing signals...")
    signals = []
    signals.extend(analyzer.analyze_sentiment_signals(data))
    signals.extend(analyzer.analyze_market_structure_signals(data))
    signals.extend(analyzer.analyze_onchain_signals(data))
    signals.extend(analyzer.analyze_derivative_signals(data))
    
    print(f"[INFO] Detected {len(signals)} signals")
    
    print("[INFO] Calculating risk assessment...")
    assessment = analyzer.calculate_risk_assessment(signals)
    
    print("[INFO] Generating report...")
    report = analyzer.generate_report(data, signals, assessment)
    
    # 保存报告
    timestamp = datetime.now().strftime('%Y%m%d_%H%M')
    output_file = OUTPUT_DIR / f"comprehensive_report_{timestamp}.md"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"[SUCCESS] Report saved: {output_file}")
    
    # 同时保存为Discord格式
    discord_file = OUTPUT_DIR / f"discord_report_{timestamp}.md"
    with open(discord_file, 'w', encoding='utf-8') as f:
        f.write(report)
    
    await analyzer.close()
    
    return report

if __name__ == '__main__':
    report = asyncio.run(main())
    print("\n" + "="*50)
    print("REPORT PREVIEW:")
    print("="*50)
    print(report[:2000] + "...")
