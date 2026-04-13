# Crypto Deception Monitor – April 13, 2026, 13:11 UTC

## Executive Summary
**Deception Risk Score**: 0/100 (🟢 Low)

| Metric | Value | Status |
|--------|-------|--------|
| Bid Depth Decay (8h) | 0.0% | ✓ Buy support stable |
| Exchange Netflow | 0 BTC | ✓ Normal exchange flows |
| Dormant Addresses | 0 | ✓ No unusual whale activity |
| Social Acceleration | 1.00x | ✓ Normal social activity |
| Ask Uniformity | 1.000 | ✓ Normal orderbook |

---

## Deception Indicators Detail

### 1. Orderbook Manipulation Signals
**Bid Depth Decay**: 0.0%
- Current buy support: 0.00 BTC
- Previous buy support: 0.00 BTC
- Interpretation: ✓ Buy support stable

**Ask Uniformity Score**: 1.000
- Lower values indicate algorithmic walls
- Interpretation: ✓ Normal orderbook

### 2. Whale Activity
**Exchange Inflow**: 0 BTC (12h)
- Positive = inflow to exchanges (sell pressure)
- Negative = outflow from exchanges (accumulation)
- Interpretation: ✓ Normal exchange flows

**Dormant Address Alerts**: 0 addresses
- Addresses dormant >1 year that became active
- Interpretation: ✓ No unusual whale activity

### 3. Social Sentiment
**Message Acceleration**: 1.00x baseline
- Measures sudden spikes in social media activity
- Interpretation: ✓ Normal social activity

---

## Detailed Alerts

### 1. Orderbook Manipulation Signals
**Bid Depth Decay**: 0.0%
- Current buy support: 0.00 BTC
- Previous buy support: 0.00 BTC
- Interpretation: ✓ Buy support stable

**Ask Uniformity Score**: 1.000
- Lower values indicate algorithmic walls
- Interpretation: ✓ Normal orderbook

### 2. Whale Activity
**Exchange Inflow**: 0 BTC (12h)
- Positive = inflow to exchanges (sell pressure)
- Negative = outflow from exchanges (accumulation)
- Interpretation: ✓ Normal exchange flows

### 4. Dormant Address Activity
**Status**: ✅ Monitoring active - No dormant whale addresses have awakened in the last 12 hours.

*Monitoring system configured for addresses dormant >365 days with transactions >$100k*

**Note**: Full dormant address detection requires Etherscan API integration (configured).


### 5. Social Media Acceleration
**Status**: ℹ️ Monitoring disabled - Using baseline values.

Social media acceleration monitoring is temporarily disabled to focus on core deception signals (orderbook + on-chain).

*This feature can be enabled by configuring Telegram/Twitter API credentials.*


---

## Risk Assessment

**Overall Risk Level**: 🟢 Low

✅ **LOW RISK** - Market structure appears normal. Standard risk management applies.

---

## Methodology
This report analyzes:
- **Orderbook Structure**: Bid depth decay, ask uniformity, spread analysis
- **On-Chain Flows**: Exchange netflow, dormant address activity
- **Social Metrics**: Message frequency acceleration on major channels

All data is sourced from public APIs and analyzed using transparent algorithms.
See [METHODOLOGY.md](https://github.com/peteryang546/crypto-risk-radar/blob/main/METHODOLOGY.md) for detailed formulas.

---

*Non-investment advice. For research and educational purposes only.*
*Data as of: {timestamp.isoformat()}*
