# Crypto Risk Radar - Methodology

**Version**: 8.7  
**Last Updated**: April 15, 2026

---

## Overview

Crypto Risk Radar uses a multi-layered approach to assess cryptocurrency risks:

1. **Real-time Data Collection** from multiple APIs
2. **Quantitative Risk Models** for statistical analysis
3. **5-Dimension Risk Scoring** for comprehensive assessment
4. **Visualization** for intuitive understanding

---

## Data Sources

| Source | API | Data Type | Update Frequency |
|--------|-----|-----------|------------------|
| CoinGecko | `/coins/markets` | Price, Volume, Market Cap | Real-time |
| Binance | `/depth` | Orderbook | Real-time |
| Etherscan | `/api?module=account` | On-chain transactions | Real-time |
| GoPlus | `/token_security` | Contract security | Real-time |
| GeckoTerminal | `/networks/{network}/pools` | DEX data | Real-time |
| Nitter | (X mirror) | Social signals | 8-hourly |

---

## Risk Models

### 1. 5-Dimension Risk Scoring (v8.7)

**Weight Distribution**:

| Dimension | Weight | Key Metrics |
|-----------|--------|-------------|
| Market Risk | 30% | Volatility, Liquidity, Market Cap |
| Security Risk | 25% | Audit Status, Exploit History |
| Financial Risk | 20% | TVL, Revenue, Treasury Health |
| Operational Risk | 15% | Team Transparency, Governance |
| Sentiment Risk | 10% | Social Signals, News Sentiment |

**Formula**:
```
Risk Score = Σ(Dimension Score × Weight)
```

**Risk Levels**:
- 0-25: Low Risk (Green)
- 26-50: Medium Risk (Yellow/Orange)
- 51-75: High Risk (Red)
- 76-100: Critical Risk (Purple)

### 2. Volatility Calculation

**Method**: EWMA (Exponentially Weighted Moving Average)

```python
σ²_t = λ × σ²_{t-1} + (1-λ) × r²_t
```

Where:
- λ = 0.94 (decay factor)
- r_t = daily return
- Annualized: σ_annual = σ_daily × √365

**Window**: 30-day realized volatility

### 3. VaR (Value at Risk)

**Method**: Parametric VaR using EWMA volatility

```python
VaR_99% = -2.33 × σ × Portfolio Value
```

**Interpretation**: Maximum expected loss at 99% confidence level over 24 hours.

### 4. Risk Matrix

**4x4 Likelihood-Impact Matrix**:

| Likelihood \ Impact | Low(1) | Medium(2) | High(3) | Critical(4) |
|---------------------|--------|-----------|---------|-------------|
| High(4) | 4 | 8 | 12 | 16 |
| Medium(3) | 3 | 6 | 9 | 12 |
| Low(2) | 2 | 4 | 6 | 8 |
| Rare(1) | 1 | 2 | 3 | 4 |

**Priority Levels**:
- 1-4: Monitor
- 5-8: Plan mitigation
- 9-12: Implement controls
- 13-16: Immediate action

### 5. DeFi Protocol Risk

**Assessment Dimensions**:

1. **Security (30%)**: Audit status, exploit history
2. **Oracle Risk (20%)**: Oracle type, diversity, TVL at risk
3. **Financial (20%)**: TVL stability, revenue sustainability
4. **Yield Sustainability (20%)**: APY vs industry average
5. **Governance (10%)**: Token concentration, timelock

**APY Risk Thresholds**:
- < 20%: Normal
- 20-50%: High risk (unsustainable)
- > 50%: Dangerous (likely ponzi)

---

## Module Details

### Module 1: Market Overview
- **Source**: CoinGecko
- **Metrics**: Price, 24h change, volume, market cap
- **Update**: Every 8 hours

### Module 2: Orderbook Structure
- **Source**: Binance
- **Metrics**: Bid depth decay, ask uniformity, spread
- **Spoofing Detection**: Ask uniformity < 0.1 + Bid decay > 20%

### Module 3: Exchange Netflow
- **Calculation**: Exchange inflow - outflow
- **Interpretation**: Positive = selling pressure, Negative = accumulation

### Module 4: Dormant Addresses
- **Definition**: Addresses inactive > 365 days
- **Monitoring**: Large transfers (> $1M) to exchanges
- **Risk**: Often precedes major sell-offs

### Module 5: Token Unlocks
- **Source**: CoinGecko
- **Tracking**: Upcoming unlock events
- **Risk**: Supply increase can cause price pressure

### Module 6: High-Risk Tokens
- **Source**: GeckoTerminal
- **Criteria**: Low liquidity, high volatility, concentrated ownership
- **Risk Score**: 0-100 based on multiple factors

### Module 7: Contract Security
- **Source**: GoPlus Security API
- **Checks**: Honeypot, mint functions, blacklist, pause functions
- **Risk Features**: Centralized control indicators

### Module 8: Pattern Observations
- **Source**: Social media (Nitter)
- **Tracking**: KOL mentions, promotional patterns
- **Risk Factors**: Excessive hype, urgency tactics, vague claims

### Module 9: Self-Protection Guide
- **Static Content**: Verification checklist, red flags
- **Purpose**: Educational resource for investors

### Module 10: Market Anomaly Index
- **Components**: Orderbook + Netflow + Dormant + Social
- **Scale**: 0-2.0
- **Thresholds**: >1.0 = elevated risk

### Module 11: Risk Heatmap (v8.7)
- **Visualization**: SVG scatter plot
- **Axes**: Market Cap (log) vs Volatility
- **Color**: Risk score (5-level gradient)
- **Assets**: BTC, ETH, SOL, BNB, XRP, DOGE

### Module 12: Risk Matrix (v8.7)
- **Framework**: 4x4 Likelihood-Impact
- **Risks**: Token unlocks, exploits, rug pulls, etc.
- **Output**: Priority scores (1-16)

---

## Data Quality

### Real vs Sample Data

| Module | Data Type | Source |
|--------|-----------|--------|
| Market Overview | Real | CoinGecko API |
| Orderbook | Real | Binance API |
| Netflow | Calculated | Market data |
| Dormant | Real | Etherscan API |
| Unlocks | Real | CoinGecko API |
| High-Risk Tokens | Real | GeckoTerminal API |
| Contract Security | Real | GoPlus API |
| Social Patterns | Sample | Demo data (labeled) |
| Risk Scores | Calculated | 5-dimension model |

### Accuracy
- Price data: ±0.1%
- On-chain data: 100% (direct from blockchain)
- Risk scores: Algorithmic estimates (not predictions)

---

## Limitations

1. **Risk scores are estimates**, not guarantees
2. **Past performance** does not predict future results
3. **Social signals** may have delays or gaps
4. **Contract analysis** cannot detect all vulnerabilities
5. **DeFi protocols** may have unaudited code

---

## References

- DeFiLlama Risk Assessment Methodology
- Risk Assessment Framework (ISO 31000)
- Crypto Report Enhanced (Visualization)
- Smart Contract Security Best Practices

---

## Token Research Framework (v9.0)

### Five Vulnerabilities Detection

**Purpose**: Identify high-risk tokens through on-chain fact analysis

**Five Vulnerabilities**:

| Vulnerability | Weight | Key Signals |
|--------------|--------|-------------|
| Contract Code | 35% | Honeypot, Tax Rate, Hidden Owner, Verified Status |
| Holder Distribution | 20% | Top 10/50 Concentration, Total Holders |
| Liquidity Management | 25% | LP Locked, Lock Duration, Liquidity Size |
| Developer Association | 10% | Team Doxxed, Website, Whitepaper, Social Media |
| Marketing Narrative | 10% | Unrealistic Returns, Viral Marketing, Consistency |

### Scoring Rules

**Contract Code Risk**:
- Honeypot detected: 100 points
- Sell tax > 10%: 70 points
- Hidden owner: 60 points
- Not verified: 50 points
- Mintable: 40 points

**Holder Distribution Risk**:
- Top 10 > 80%: 100 points
- Top 10 60-80%: 50 points
- Top 10 < 60%: 0-30 points
- Total holders < 100: +20 points

**Liquidity Management Risk**:
- Not locked: 80-100 points
- Locked < 1 year: 50 points
- Locked > 1 year: 0 points
- Liquidity < $50k: +25 points

**Developer Association Risk**:
- Anonymous team: 50 points
- Partial doxxed: 25 points
- Fully doxxed: 0 points
- No whitepaper: +15 points

**Marketing Narrative Risk**:
- Promises unrealistic returns: 70 points
- Contradictory narrative: 50 points
- Viral marketing: +15 points

### Risk Classification

| Score | Level | Action |
|-------|-------|--------|
| >= 70 | [CRIT] Extreme Risk | IGNORE DIRECTLY |
| 50-69 | [HIGH] High Risk | STAY AWAY |
| 30-49 | [MED] Medium Risk | OBSERVE ONLY |
| < 30 | [LOW] Low Risk | STUDY & RESEARCH |

### Formula
```
Overall Score = Σ(Vulnerability Score × Weight)
```

### Data Sources
- GoPlus Security API (contract analysis)
- DEX Screener (liquidity, holder data)
- Etherscan (on-chain verification)

---

## Updates

- **v9.0** (Apr 2026): Added Five Vulnerabilities Detection, Token Research Framework, Case Study Database
- **v8.7** (Apr 2026): Added 5-dimension risk scoring, heatmap, risk matrix
- **v8.5** (Apr 2026): Added VaR, volatility regime, spoofing detection
- **v8.0** (Apr 2026): Major refactor with 10 modules
- **v7.0** (Mar 2026): Initial release

---

**Disclaimer**: This methodology is for educational purposes. Always conduct independent research before making investment decisions.
