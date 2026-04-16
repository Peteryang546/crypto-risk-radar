# Crypto Risk Radar v9.0 Update Summary

**Release Date**: April 16, 2026  
**Status**: ✅ Released  
**License**: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)

**Last Updated**: 2026-04-16 18:06 CST  
**API Status**: CoinGecko, GoPlus Security Configured  
**Auto-Run Status**: 18:00 CST task completed successfully, next run at 02:00 CST

---

## Overview

v9.0 introduces the **Five Vulnerabilities Detection Framework** - a systematic approach to identify high-risk tokens through on-chain fact analysis. This upgrade transforms the project from a "daily risk report" into a "scalable on-chain anomaly fact sheet system."

---

## New Features

### 1. Five Vulnerabilities Detection

| Vulnerability | Weight | Key Signals |
|--------------|--------|-------------|
| **Contract Code** | 35% | Honeypot, Tax Rate, Hidden Owner, Verified Status |
| **Holder Distribution** | 20% | Top 10/50 Concentration, Total Holders |
| **Liquidity Management** | 25% | LP Locked, Lock Duration, Liquidity Size |
| **Developer Association** | 10% | Team Doxxed, Website, Whitepaper, Social Media |
| **Marketing Narrative** | 10% | Unrealistic Returns, Viral Marketing, Consistency |

### 2. Token Research Framework

**Workflow**:
```
[Auto Discover] → [Auto Scan] → [Human-in-the-Loop] → [Classify] → [Publish]
```

**Components**:
- `token_discovery.py` - Daily scan for new high-risk tokens
- `token_research_framework.py` - Five vulnerabilities analysis
- `human_in_the_loop.py` - CLI interface for human review
- `case_study_manager.py` - Case database with public/private separation

### 3. Risk Classification System

| Score | Level | Action | Description |
|-------|-------|--------|-------------|
| >= 70 | [CRIT] Extreme Risk | IGNORE DIRECTLY | Clear fraudulent characteristics (honeypot, unlocked liquidity) |
| 50-69 | [HIGH] High Risk | STAY AWAY | Multiple suspicious signals (anonymous team, concentrated holdings) |
| 30-49 | [MED] Medium Risk | OBSERVE ONLY | Risk signals present but not confirmed. Do not participate |
| < 30 | [LOW] Low Risk | STUDY & RESEARCH | Lower risk, can be used for learning. Not investment advice |

### 4. Report Template

**Standard Format**:
- Risk Scoring Methodology (thresholds table)
- Five Vulnerabilities Analysis (each with detection items, results, risk signals)
- Project Claims vs On-Chain Facts (comparison table)
- Comprehensive Assessment (weighted calculation)
- Historical Similar Patterns (case matching)
- Data Verification Links (GoPlus, Etherscan, DEX Screener)
- CC BY 4.0 License

### 5. Case Study Database

**Public Summary** (Visible to all):
- Token symbol, risk level, key signals
- Summary description
- Claims vs Facts comparison
- Historical similar patterns

**Private Report** (Internal only):
- Full contract address
- Transaction hashes
- Wallet addresses
- Internal investigation notes

---

## Core Principles

1. **Fact-Based Only**: Only present on-chain verifiable facts
2. **No Investment Advice**: No "buy/sell/hold" recommendations
3. **Educational Purpose**: Help users learn to identify risks
4. **Open License**: CC BY 4.0 - free to use with attribution
5. **Human-in-the-Loop**: Automated discovery + human review + classification

---

## Technical Implementation

### Scoring Algorithm

```python
# Weights
WEIGHTS = {
    'contract_code': 0.35,
    'holder_distribution': 0.20,
    'liquidity_management': 0.25,
    'developer_association': 0.10,
    'marketing_narrative': 0.10
}

# Calculate overall score
overall_score = sum(score * weight for score, weight in zip(scores, weights))
```

### Data Sources

- **GoPlus Security API**: Contract security analysis
- **DEX Screener**: Liquidity, holder distribution, trading data
- **Etherscan**: On-chain transaction verification

### File Structure

```
F:/stepclaw/agents/blockchain-analyst/
├── token_research_framework.py    # Five vulnerabilities detection
├── token_discovery.py              # New token discovery
├── human_in_the_loop.py            # CLI interface
├── case_study_manager.py           # Case database
├── narratives/                     # Generated reports
│   └── 2026-04-16-FAKEAI.md
├── case_studies/
│   ├── public/                     # Public summaries
│   └── private/                    # Detailed analysis
└── METHODOLOGY.md                  # Updated methodology
```

---

## Usage

### CLI Interface

```bash
python human_in_the_loop.py
```

**Commands**:
- `[1-5]` - Select token for deep research
- `[C]` - Quick classify based on auto-detection
- `[D]` - Discover new tokens
- `[S]` - View statistics
- `[Q]` - Save and exit

### Report Generation

```bash
python scripts/generate_enhanced_full_report.py
```

Generates 14-module report including:
- Module 14: On-Chain Anomaly Fact Sheet (v9.0)
- Comments section (GitHub Issues)
- CC BY 4.0 License

---

## Schedule

- **Every 8 hours**: 06:00 / 14:00 / 22:00 ET
- **Next run**: Today 18:00 CST (includes v9.0 modules)

---

## Files Added/Modified

### New Files
- `PROJECT_IDENTITY.md` - Project identity and mission
- `UPGRADE_PLAN_v9.0.md` - Detailed upgrade plan
- `token_research_framework.py` - Five vulnerabilities detection
- `token_discovery.py` - Token auto-discovery
- `human_in_the_loop.py` - CLI interface
- `case_study_manager.py` - Case database
- `test_demo.py` - Demo script
- `narratives/2026-04-16-FAKEAI.md` - Sample report

### Modified Files
- `README.md` - Updated to v9.0, added 14th module
- `METHODOLOGY.md` - Added Five Vulneracies Detection section
- `scripts/generate_enhanced_full_report.py` - Added Module 14, comments, license

---

## Example Report

**Sample**: `narratives/2026-04-16-FAKEAI.md`

**Key Metrics**:
- Overall Score: 73/100
- Risk Level: [CRIT] Extreme Risk
- Recommended Action: IGNORE DIRECTLY

**Five Vulnerabilities Scores**:
- Contract Code: 100/100 (Honeypot + 15% sell tax + hidden owner)
- Holder Distribution: 50/100 (Top 10: 78.5%, Total: 156 holders)
- Liquidity Management: 65/100 (Unlocked, $45k, 3 LP holders)
- Developer Association: 45/100 (Anonymous, no whitepaper)
- Marketing Narrative: 70/100 (Unrealistic returns, contradictory)

---

## Feedback

- **GitHub Issues**: [Submit feedback](https://github.com/peteryang546/crypto-risk-radar/issues)
- **License**: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)

---

*Crypto Risk Radar v9.0 - Five Vulnerabilities Detection Framework*  
*Standing by the pit, holding a lamp.*
