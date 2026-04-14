# 🔴 Crypto Risk Radar

> **Automated 8-hourly blockchain risk monitoring and analysis**

[![Update Status](https://img.shields.io/badge/Updates-Every%208%20hours-blue)](https://peteryang546.github.io/crypto-risk-radar/)
[![Data Quality](https://img.shields.io/badge/Data%20Quality-90%25%2B%20Real-green)](https://peteryang546.github.io/crypto-risk-radar/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 🌐 Live Website

**[https://peteryang546.github.io/crypto-risk-radar/](https://peteryang546.github.io/crypto-risk-radar/)**

- 📚 [Archive](https://peteryang546.github.io/crypto-risk-radar/archive.html) - Historical reports
- 📡 [RSS Feed](https://peteryang546.github.io/crypto-risk-radar/feed.xml) - Subscribe to updates
- 📊 [JSON API](https://peteryang546.github.io/crypto-risk-radar/output/latest.json) - Machine-readable data

---

## 📊 What is This?

Crypto Risk Radar is an **automated intelligence system** that monitors blockchain risks and market anomalies every 8 hours. It aggregates data from multiple sources to provide:

- **Real-time market data** (BTC/ETH prices, volume, sentiment)
- **On-chain security analysis** (contract risks, honeypot detection)
- **Exchange flow monitoring** (accumulation vs distribution signals)
- **Token unlock alerts** (upcoming supply increases)
- **Dormant address tracking** (whale wallet reactivations)
- **High-risk token identification** (new DEX listings with risk scores)

---

## 🎯 Key Features

### 10 Core Modules

| Module | Data Source | Status |
|--------|-------------|--------|
| Market Overview | CoinGecko API | ✅ Real-time |
| Orderbook Structure | Binance API | ✅ Real-time |
| Exchange Netflow | Calculated from market data | ✅ Real-time |
| Dormant Addresses | Etherscan API | ✅ Real-time monitoring |
| Token Unlocks | CoinGecko API | ✅ Real-time |
| High-Risk Tokens | GeckoTerminal + GoPlus | ✅ Real-time |
| Contract Security | GoPlus Security API | ✅ Real-time |
| Pattern Observations | Sample data | ⚠️ Demo (labeled) |
| Self-Protection Guide | Educational content | ✅ Static |
| Market Anomaly Index | Calculated composite | ✅ Real-time |

### Automation

- ⏰ **Every 8 hours** (06:00 / 14:00 / 22:00 ET)
- 🤖 **Fully automated** data collection, analysis, and deployment
- 📤 **Auto-publishes** to GitHub Pages
- 📧 **RSS feed** for subscriptions
- 📚 **Archive page** for historical reports

### Data Quality

- **90%+ real data** from verified APIs
- **Transparent sourcing** - all data linked to Etherscan/BSCScan
- **Neutral tone** - no accusations, only facts and correlations
- **Educational focus** - includes self-protection guides

---

## 🛠️ Technical Stack

| Component | Technology |
|-----------|------------|
| Data Collection | Python + PowerShell (for SSL bypass) |
| APIs | CoinGecko, GoPlus, GeckoTerminal, Etherscan |
| Report Generation | Python (HTML generation) |
| Hosting | GitHub Pages |
| Automation | Windows Task Scheduler |
| Data Format | HTML + JSON + RSS |

---

## 📈 Data Sources

- **[CoinGecko](https://www.coingecko.com/)** - Market data, prices, volumes
- **[GoPlus Security](https://gopluslabs.io/)** - Contract security scanning
- **[GeckoTerminal](https://www.geckoterminal.com/)** - DEX trading data
- **[Etherscan](https://etherscan.io/)** - On-chain transaction monitoring
- **[Binance](https://www.binance.com/)** - Orderbook data

---

## 🚀 Getting Started

### For Users

Simply visit the live website: **[https://peteryang546.github.io/crypto-risk-radar/](https://peteryang546.github.io/crypto-risk-radar/)**

Reports update automatically every 8 hours. No registration required.

### For Developers

```bash
# Clone the repository
git clone https://github.com/peteryang546/crypto-risk-radar.git
cd crypto-risk-radar

# Install dependencies
pip install -r requirements.txt

# Set environment variables
set GITHUB_TOKEN=your_github_token_here

# Run report generation manually
python scripts/generate_enhanced_full_report.py

# Publish to GitHub Pages
python publish_report.py
```

---

## 📋 Project Status

| Metric | Value |
|--------|-------|
| **Version** | 8.2 |
| **Data Quality** | 90%+ Real |
| **Update Frequency** | Every 8 hours |
| **Total Reports** | 20+ |
| **APIs Integrated** | 5 |
| **Status** | Production Ready |

---

## 🗺️ Roadmap

### High Priority
- [ ] Mode observation real data (Nitter/LunarCrush integration)
- [ ] Independent domain (cryptoriskradar.com)
- [ ] Google Search Console optimization

### Medium Priority
- [ ] Binance Square auto-publishing
- [ ] Weekly summary reports
- [ ] GitHub Sponsors

### Low Priority
- [ ] Stablecoin supply metrics
- [ ] Gas fee monitoring
- [ ] Multi-language support
- [ ] Email subscriptions

---

## ⚠️ Disclaimer

This project is for **educational and research purposes only**. It does not constitute financial advice. Always do your own research before making investment decisions.

- Data is provided "as is" without warranties
- Risk scores are algorithmic estimates, not guarantees
- Past patterns do not predict future results
- Cryptocurrency investments carry significant risk

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

---

## 🤝 Contributing

Contributions welcome! Please open an issue or pull request.

### Ways to Contribute
- Report bugs or data inaccuracies
- Suggest new data sources or metrics
- Improve documentation
- Share the project with others

---

## 📞 Contact

- **GitHub Issues**: [Report bugs or suggestions](https://github.com/peteryang546/crypto-risk-radar/issues)
- **RSS Feed**: Subscribe for updates
- **Website**: [Live reports](https://peteryang546.github.io/crypto-risk-radar/)

---

## 🙏 Acknowledgments

- [CoinGecko](https://www.coingecko.com/) for market data API
- [GoPlus Security](https://gopluslabs.io/) for contract security API
- [GeckoTerminal](https://www.geckoterminal.com/) for DEX data
- [Etherscan](https://etherscan.io/) for blockchain data
- [GitHub Pages](https://pages.github.com/) for free hosting

---

<p align="center">
  <strong>Crypto Risk Radar</strong> — Automated blockchain intelligence<br>
  Updated every 8 hours • 90%+ real data • Neutral & educational
</p>
