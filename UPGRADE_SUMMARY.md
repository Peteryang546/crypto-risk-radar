# Crypto Risk Radar - 8-Hourly Upgrade Summary

## Overview
Upgraded from 12-hour static reports to **8-hour Deception Monitoring System**

## Key Changes

### 1. Schedule Change
| Before | After |
|--------|-------|
| 12 hours (08:00, 20:00) | 8 hours (06:00, 14:00, 22:00 UTC) |
| 2 runs/day | 3 runs/day |

**UTC Schedule** (Targeting US/EU markets):
- 06:00 UTC = 02:00 EST / 07:00 CET (EU morning)
- 14:00 UTC = 10:00 EST / 15:00 CET (US pre-market)
- 22:00 UTC = 18:00 EST / 23:00 CET (US active)

### 2. New Modules (Deception Detection)

| Module | Description | Status |
|--------|-------------|--------|
| **Orderbook Deception** | Bid depth decay, ask uniformity | ✅ Implemented |
| **Dormant Address Alert** | Whale awakening detection | 🔄 Framework ready |
| **Social Acceleration** | FOMO signal detection | 🔄 Framework ready |
| **Composite Risk Score** | 0-100 deception index | ✅ Implemented |

### 3. Technical Architecture

```
Local Deployment (Step Claw)
├── run_analysis.py (Main orchestrator)
├── config.py (Global settings)
├── scripts/
│   ├── crawlers/
│   │   └── orderbook_crawler.py (PowerShell bridge)
│   ├── analyzers/
│   │   └── deception_score.py (Risk calculation)
│   └── utils/
│       └── history.py (State persistence)
└── setup_schedule.bat (Windows task scheduler)
```

### 4. Data Flow

```
PowerShell → Binance API → Orderbook Data
     ↓
Python Analysis → Risk Score Calculation
     ↓
GitHub API → Upload Report + JSON
     ↓
GitHub Pages → Auto-update
```

### 5. File Structure

**New Files**:
- `config.py` - Global configuration
- `run_analysis.py` - Main 8-hourly runner
- `scripts/crawlers/orderbook_crawler.py` - PowerShell data fetcher
- `scripts/analyzers/deception_score.py` - Risk calculator
- `scripts/utils/history.py` - State persistence
- `setup_schedule.bat` - Windows scheduler setup

**Modified Files**:
- Existing 12 modules remain functional
- Integrated into new 8-hourly workflow

### 6. Environment Setup

**Required**:
```bash
# Set environment variables
set GITHUB_TOKEN=your_github_token
set ETHERSCAN_API_KEY=your_etherscan_key  # Optional

# Install dependencies
pip install requests

# Setup scheduled tasks (run as Admin)
setup_schedule.bat
```

### 7. Manual Run

```bash
# Run once manually
python run_analysis.py

# Or with specific options (future)
python run_analysis.py --symbol BTCUSDT --output markdown
```

### 8. Output

**Generated Files**:
- `reports/report_YYYYMMDD_HHMM.md` - Historical reports
- `current.md` - Latest report (always updated)
- `api/status.json` - Machine-readable API

## Risk Score Formula

```
Risk Score = Σ(Indicator × Weight)

Indicators:
- Bid Depth Decay (25%): Rapid removal of buy support
- Exchange Netflow (20%): Large inflows = sell pressure
- Dormant Address (30%): Whale awakening
- Social Acceleration (15%): FOMO signals
- Ask Uniformity (10%): Algorithmic walls

Thresholds:
- 0-30: 🟢 Low Risk
- 31-60: 🟡 Medium Risk
- 61-80: 🟠 High Risk
- 81-100: 🔴 Extreme Risk
```

## Next Steps

1. **Test Run**: Execute `python run_analysis.py` manually
2. **Verify Upload**: Check GitHub for uploaded reports
3. **Setup Schedule**: Run `setup_schedule.bat` as Administrator
4. **Monitor**: Check Windows Task Scheduler for task status

## Notes

- All reports are in **English** for US/EU markets
- Uses **PowerShell** to bypass Python SSL issues
- **No local Git** required (uses GitHub API)
- **Local deployment** with full control over timing
