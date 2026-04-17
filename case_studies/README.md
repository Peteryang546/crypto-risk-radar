# Crypto Risk Radar - Case Study Library

## Purpose
Structured analysis of historical crypto scams and exploits to **extract reusable risk patterns** and build a **practical risk control methodology** for ordinary investors.

### Core Philosophy
- **Pattern Recognition, Not Prediction**: We analyze historical cases to identify recurring attack patterns, not to predict future prices
- **Static Observation, Dynamic Verification**: Tools provide snapshots; patterns are used to analyze new projects, then verified through observation
- **Neutral Observer**: We present facts and patterns, not conclusions or investment advice

### Methodology
```
Historical Cases → Pattern Extraction → Detection Formulas → 
New Project Analysis → Observation Verification → Iterative Improvement
```

## Case Study Structure

Each case study follows a standardized format:

1. **Basic Information** - Date, type, loss amount, chain
2. **Attack Pattern Analysis** - Execution flow, phases
3. **Pre-Attack Indicators** - Warning signals
4. **Technical Analysis** - Code vulnerabilities
5. **Detection Framework** - How to spot similar cases
6. **Prevention Measures** - Protection strategies
7. **Similar Cases** - Pattern matching
8. **Lessons Learned** - Key takeaways

## Pattern Categories

### 1. Exit Scams (Rug Pulls)
- **Classic Liquidity Removal**: SQUID, AnubisDAO
- **Hidden Migration**: Compounder Finance, Meerkat Finance
- **Honeypot**: SQUID (sell restriction)
- **Slow Rug**: Gradual drainage over time

### 2. Technical Exploits
- **Flash Loan Attacks**: Yearn, Harvest, bZx
- **Reentrancy**: The DAO, dForce
- **Oracle Manipulation**: Various lending protocols
- **Access Control**: Parity Multisig

### 3. Infrastructure Attacks
- **Exchange Hacks**: Binance, MT.GOX
- **Bridge Exploits**: Poly Network
- **51% Attacks**: Ethereum Classic

### 4. Economic Attacks
- **Ponzi Schemes**: Bitcoin Savings & Trust
- **Pump & Dump**: Coordinated manipulation
- **Front Running**: MEV extraction

## Pattern Library

| Pattern | File | Cases | Complexity |
|---------|------|-------|------------|
| Rug Pull | `rug_pull_pattern.md` | 5+ | Low |
| Flash Loan | `flash_loan_attack_pattern.md` | 3+ | High |
| Contract Bug | `contract_vulnerability_pattern.md` | 4+ | Medium |
| Honeypot | (in rug_pull) | 2+ | Low |

## 20 Documented Cases

### 2021 (5 cases)
1. **SQUID** - Honeypot/Rug Pull - $3.38M
2. **AnubisDAO** - Liquidity Drain - $60M
3. **Poly Network** - Cross-chain Exploit - $611M
4. **Meerkat Finance** - Migration Function - $31M
5. **Yearn Finance** - Flash Loan - $11M

### 2020 (5 cases)
6. **Compounder Finance** - Hidden Migration - $10.8M
7. **Harvest Finance** - Flash Loan - $24M
8. **Eminence Finance** - Unfinished Contract - $15M
9. **dForce** - Reentrancy - $25M
10. **bZx Protocol** - Flash Loan - $1M

### 2019 (2 cases)
11. **Binance Hack** - Hot Wallet - 7K BTC
12. **ETC 51% Attack** - Blockchain Reorg

### 2018 (1 case)
13. **Beauty Chain (BEC)** - Integer Overflow

### 2017 (1 case)
14. **Parity Multisig** - Access Control - 150M+ ETH frozen

### 2016 (2 cases)
15. **The DAO** - Reentrancy - $50M
16. **ShapeShift** - Internal Breach - $230K

### 2014 (1 case)
17. **MT.GOX Collapse** - Exchange Insolvency - $450M

### 2012 (1 case)
18. **Bitcoin Savings & Trust** - Ponzi - 700K BTC

### 2011 (1 case)
19. **MT.GOX First Hack** - Database Breach - 2,643 BTC

### Template (1 case)
20. **APT Unlock** - Token Unlock - Pattern tracking

## Quick Links

### Related Resources
- [📊 Main Dashboard](https://peteryang546.github.io/crypto-risk-radar/) - Real-time risk reports
- [🎯 Prediction Log](https://peteryang546.github.io/crypto-risk-radar/prediction_log.html) - Warning accuracy tracking
- [📋 Classification](https://peteryang546.github.io/crypto-risk-radar/classification_dashboard.html) - Token categories
- [📖 Methodology](https://peteryang546.github.io/crypto-risk-radar/METHODOLOGY_ENHANCED.md) - Risk scoring framework

## Usage Guide

### For Investors
1. Review relevant pattern before investing
2. Use detection checklist
3. Apply prevention measures
4. Check [prediction log](https://peteryang546.github.io/crypto-risk-radar/prediction_log.html) for recent warnings

### For Developers
1. Study vulnerability patterns
2. Implement prevention code
3. Follow security best practices
4. Review [methodology](https://peteryang546.github.io/crypto-risk-radar/METHODOLOGY_ENHANCED.md) for risk models

### For Analysts
1. Use pattern matching for new cases
2. Contribute new case studies
3. Update detection frameworks
4. Cross-reference with [main report](https://peteryang546.github.io/crypto-risk-radar/) data

## Contributing

To add a new case study:
1. Create `[CASE_NAME]_case_analysis.md`
2. Follow the standardized format
3. Include real transaction hashes
4. Add to pattern index

## Risk Control Methodology

### For New Project Analysis
1. **Select Relevant Patterns**: Based on project type (DEX, lending, NFT, etc.)
2. **Apply Detection Formulas**: Use checklists from pattern documents
3. **Verify On-Chain**: Check contract code, liquidity, holder distribution
4. **Document Findings**: Record observations for future verification
5. **Iterate**: Update methodology based on verification results

### Pattern-to-Formula Examples

| Pattern | Detection Formula | Verification Method |
|---------|-------------------|---------------------|
| Honeypot | `sell_restriction == true AND owner_can_mint == true` | Attempt small sell transaction |
| Liquidity Rug | `lp_unlock_time < 30_days AND owner_lp_percentage > 50%` | Monitor LP removal events |
| Flash Loan Risk | `oracle_source == single_dex AND flash_loan_enabled == true` | Review oracle implementation |
| Reentrancy | `external_call_before_state_update == true` | Static analysis + code review |

## Disclaimer

All case studies are based on publicly available information. Analysis is for **educational and pattern recognition purposes only**.

- **Not Financial Advice**: We do not recommend any investments
- **Not Predictions**: Historical patterns do not guarantee future outcomes
- **Neutral Observer**: We present facts, not conclusions
- **Verify Independently**: Always conduct your own research

---

**Last Updated**: 2026-04-17
**Total Cases**: 20
**Pattern Categories**: 4
**Methodology Status**: Active Development
