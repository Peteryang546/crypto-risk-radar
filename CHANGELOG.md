# Changelog

All notable changes to the Crypto Risk Radar project.

## [9.0.0] - 2026-04-17

### Added
- **Module 11: Quantum Computing Threat Monitor**
  - Long-term cryptographic risk assessment
  - 2025-2040 threat timeline projection
  - Key developments tracking (IBM, Google, BIP-360/361)
  - Threat level indicators for Bitcoin, Ethereum, and post-quantum preparation

- **Module 14: On-Chain Anomaly Fact Sheet**
  - 4 historical scam case studies ($FAKEAI, $RUGPULL, $PONZI, $HONEYPOT)
  - Detection rules documentation (Extreme/High/Medium Risk criteria)
  - Risk classification guide
  - Current monitoring cycle status

- **Historical Cases Database**
  - `data/anomaly_historical_cases.json` with structured case data
  - Loss amounts, red flags, and verification sources

### Fixed
- **Module 6: High-Risk Token Watchlist**
  - Fixed criteria display: "Risk Score >70" → "Risk Score ≥40"
  - Now matches actual filtering logic in code

- **Module 7: Contract Security Scanner**
  - Added yellow notification box for mainstream assets (USDT, USDC, WBTC)
  - Clarifies that high risk scores reflect centralized control, not fraud

- **Module 8: Pattern Observations**
  - Added intelligent status messages based on detection count
  - Shows "0 signals", "1 market signal", or "N patterns detected"

- **Module 12: Risk Heatmap**
  - Added data source note explaining volatility and risk score calculations

- **Meta Description**
  - Fixed: "13-module" → "14-module"

### Changed
- **Pattern Observations Data Source**
  - Upgraded from demo data to real on-chain signal monitoring
  - Added default information mode when no extreme patterns detected

- **README Documentation**
  - Updated module list to include all 14 modules
  - Added v9.0 feature descriptions

### Data Quality
- **90%+ Real Data** from verified APIs (CoinGecko, GoPlus, GeckoTerminal, Etherscan)
- All market prices, token unlocks, and security scans use live data
- Historical cases provide educational context even when no new threats detected

---

## [8.7.0] - 2026-04-13

### Added
- **5-Dimension Risk Scoring Model**
  - Market Risk (30%): Volatility, liquidity, market cap
  - Security Risk (25%): Audit status, exploit history
  - Financial Risk (20%): TVL, revenue, treasury
  - Operational Risk (15%): Team transparency, governance
  - Sentiment Risk (10%): Social signals, news sentiment

- **Interactive Risk Heatmap**
  - SVG visualization of risk-volatility-capitalization distribution
  - Color-coded risk levels

- **Risk Matrix Assessment**
  - 4x4 likelihood-impact matrix
  - Crypto-specific risk scenarios

- **DeFi Protocol Analysis**
  - APY sustainability assessment
  - Oracle risk evaluation
  - Governance mechanism review

---

## [6.2.0] - 2026-04-10

### Added
- **Initial 8-Module Release**
  - Market Overview
  - Orderbook Structure
  - Exchange Netflow
  - Dormant Address Activity
  - Token Unlock Schedule
  - High-Risk Token Watchlist
  - Contract Security Scanner
  - Self-Protection Guide

- **GitHub Actions Automation**
  - Every 8 hours (3x daily)
  - Auto-deployment to GitHub Pages

---

## Version Naming

- **v9.0**: Five Vulnerabilities Detection + Token Research Framework
- **v8.7**: 5-Dimension Risk Scoring + Heatmap/Matrix
- **v6.2**: Initial 8-Module Release

---

*For detailed methodology, see [METHODOLOGY.md](METHODOLOGY.md)*
