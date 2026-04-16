# Crypto Risk Radar - Project Summary

## Project Overview

**Crypto Risk Radar** is an independent research project providing transparent, neutral on-chain market analysis. The system generates comprehensive reports every 8 hours to align with major global market sessions.

**Core Philosophy**: Education over accusation. We present on-chain data and temporal patterns, allowing readers to draw their own conclusions.

---

## Key Features

### 1. Report Schedule (US Market Hours)
- **10:00 PM EST** - Evening analysis (Asia market close)
- **6:00 AM EST** - Pre-market briefing (EU morning)
- **2:00 PM EST** - Mid-day update (US active hours)

### 2. 10-Module Comprehensive Analysis

| Module | Content | Data Sources |
|--------|---------|--------------|
| **1. Market Overview** | BTC/ETH prices, volume, Fear & Greed | Binance, Alternative.me |
| **2. Orderbook Structure** | Bid depth decay, ask uniformity, spread | Binance API |
| **3. Exchange Netflow** | 7-day inflow/outflow history | Glassnode, Whale Alert |
| **4. Dormant Addresses** | Whale addresses active after >365 days | Etherscan, BSCScan |
| **5. Token Unlock Schedule** | Upcoming unlocks with value & percentage | TokenUnlocks, CoinGecko |
| **6. High Risk Watchlist** | Low liquidity, high concentration tokens | DEX Screener |
| **7. Contract Security** | Honeypot detection, risk features | GoPlus Security |
| **8. Pattern Observations** | Temporal correlations (neutral analysis) | On-chain + Social |
| **9. Self-Protection Guide** | Verification checklist, red flags | Educational |
| **10. Market Anomaly Index** | Composite score with 7-day trend | Multi-factor model |

### 3. Update Schedule (24-Hour Format)

**3 times daily, 8 hours apart**:

| US (ET) | Beijing (CST) | Market Session |
|:-------:|:-------------:|:---------------|
| 06:00 | 18:00 | US Pre-market |
| 14:00 | 02:00 | US Mid-day |
| 22:00 | 10:00 | US Evening |

### 4. Report Archive Feature

Each report includes a **Report Archive** section with:
- 📁 Link to all historical reports on GitHub
- 📄 Link to latest text summary (current.md)
- 📊 Link to API data (JSON endpoint)

This allows users to:
- Track market changes over time
- Compare historical patterns
- Access machine-readable data
- Browse complete report history

### 3. Neutral Tone Principles

- **"Pattern Observations"** instead of "Shill Alerts"
- **"Historical Similarity"** instead of "Risk Score"
- **"Temporal Correlation"** instead of "Manipulation"
- **Explicit disclaimers**: Correlation ≠ Causation
- **False positive rates** disclosed for patterns

### 4. Data Transparency

- All on-chain data linked to Etherscan/BSCScan
- Transaction hashes provided for verification
- Historical percentiles for context (e.g., "65th percentile")
- Open-source methodology on GitHub

---

## Technical Architecture

### Core Components

```
Crypto Risk Radar/
├── run_analysis.py              # Main orchestrator (8-hourly)
├── config.py                    # Global configuration
├── scripts/
│   ├── generate_full_integrated_report.py  # 12-module report
│   ├── generate_enhanced_full_report.py    # 10-module enhanced
│   ├── crawlers/
│   │   ├── orderbook_crawler.py # PowerShell data fetcher
│   │   ├── dormant_address.py   # Whale monitoring
│   │   └── x_crawler.py         # Social media monitoring
│   ├── analyzers/
│   │   ├── deception_score.py   # Risk calculation
│   │   ├── neutral_shill_analyzer.py  # Neutral pattern analysis
│   │   └── kol_scoring.py       # KOL integrity tracking
│   └── utils/
│       └── history.py           # State persistence
├── modules/                     # Original 12 modules
│   ├── market_overview.py
│   ├── on_chain_metrics.py
│   ├── market_microstructure.py
│   ├── security_risk.py
│   ├── quant_signal.py
│   ├── historical_backtest.py
│   ├── scenario_analysis.py
│   ├── protection_advice.py
│   ├── chart_generator.py
│   ├── high_risk_watchlist.py
│   ├── token_unlock_alert.py
│   └── contract_scanner.py
├── setup_schedule.bat           # Windows task scheduler
└── output/                      # Generated reports
```

### Data Flow

```
PowerShell Bridge → External APIs (Binance, Etherscan)
       ↓
Python Analysis → Risk Calculation → Pattern Detection
       ↓
GitHub API → Upload Reports → GitHub Pages
       ↓
Public Access → https://peteryang546.github.io/crypto-risk-radar/
```

### Key Technical Decisions

| Challenge | Solution |
|-----------|----------|
| Python SSL issues | PowerShell bridge for API calls |
| No local Git | GitHub API for file uploads |
| Windows deployment | Batch script for Task Scheduler |
| Mock data testing | `USE_MOCK_DATA` toggle in config |

---

## Report Examples

### Sample: Pattern Observation Section

```markdown
## 8. On-Chain Pattern Observations

**Note**: Correlation does not imply causation. Cross-check with other indicators.

### $MOON - Temporal Activity Pattern
**Source**: @CryptoGuru at 2026-04-13 12:00:00 UTC

**Pre-Mention Activity**:
- -2h: Large buy - $25,000 (Wallet age: 3 days) [View Tx]

**Post-Mention Activity**:
- +1h: Transfer to Binance - $20,000 [View Tx]

**Price Movement**: 30min: +22% | 1h: +18% | 6h: -8% | 24h: -25%

**Historical Similarity**: 94% (compared to historical patterns)

*Statistical note: 12% false positive rate in backtesting*
```

### Sample: Data Verification

All addresses link to Etherscan:
- `0x742d35Cc...` → [View on Etherscan](https://etherscan.io/address/0x742d35Cc...)
- Transaction hashes link to specific txs
- Token contracts link to token pages

---

## Deployment

### Requirements
- Windows with PowerShell
- Python 3.11+
- GitHub token (for uploads)

### Setup

```bash
# 1. Set environment variables
set GITHUB_TOKEN=your_github_token
set ETHERSCAN_API_KEY=your_etherscan_key  # Optional

# 2. Install dependencies
pip install requests

# 3. Test run
python run_analysis.py

# 4. Setup automatic scheduling (run as Admin)
setup_schedule.bat
```

### Manual Run

```bash
# Generate full report
python scripts/generate_enhanced_full_report.py

# Run complete analysis
python run_analysis.py
```

---

## Output Files

| File | Description | URL |
|------|-------------|-----|
| `current.md` | Latest report | GitHub repo root |
| `current_deception.md` | Deception-only report | GitHub repo root |
| `api/status.json` | Machine-readable data | `/api/status.json` |
| `reports/report_*.md` | Historical reports | `/reports/` |
| `enhanced_report_*.html` | Full HTML reports | `/output/` (local) |

**Public URL**: https://peteryang546.github.io/crypto-risk-radar/

---

## Methodology

### Market Anomaly Index Calculation

```
Score = Σ(Indicator × Weight)

Indicators:
- Bid Depth Decay (25%)
- Exchange Netflow (20%)
- Dormant Address Activity (30%)
- Social Acceleration (15%)
- Ask Uniformity (10%)

Scale: -2.0 to +2.0
Grade: Strong Avoid → Negative → Neutral → Positive → Strong Positive
```

### Pattern Detection

- Compare current patterns to 12-month historical database
- Calculate similarity percentage
- Report false positive rates
- Never claim causation

---

## Important Disclaimers

### Data Limitations
- Public data only (Etherscan, Binance, etc.)
- Correlation ≠ Causation
- Patterns may be coincidental
- Independent verification required

### Not Financial Advice
- Educational purposes only
- No investment recommendations
- Researchers hold no positions in mentioned tokens
- Past patterns don't predict future results

### Transparency
- All code open-source on GitHub
- Methodology documented in METHODOLOGY.md
- Raw data available for verification
- No commercial relationships with projects/KOLs

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 6.0 | 2026-04-12 | Original 12-module system |
| 6.1 | 2026-04-13 | Added GitHub Pages deployment |
| 6.2 | 2026-04-13 | Integrated deception detection |
| 7.0 | 2026-04-13 | Neutral tone, enhanced data density, US time format |
| 7.1 | 2026-04-13 | Added Report Archive section, historical report links |
| 7.2 | 2026-04-14 | Fixed ET timezone, 24-hour format, 8-hour schedule |
| 7.3 | 2026-04-14 | Windows scheduled tasks automation enabled |
| 8.0 | 2026-04-14 | GEO optimization: JSON-LD, sitemap, glossary, Quick Summary |

---

## Contact & Resources

- **GitHub**: https://github.com/peteryang546/crypto-risk-radar
- **Website**: https://peteryang546.github.io/crypto-risk-radar/
- **Methodology**: See METHODOLOGY.md in repo

---

*Last Updated: April 14, 2026*
*Version: 8.1.1*
 See METHODOLOGY.md in repo

---

*Last Updated: April 14, 2026*
*Version: 8.0*
