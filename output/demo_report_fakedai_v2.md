# FAKEAI - On-Chain Anomaly Fact Sheet

**Contract Address**: `0x742d35Cc6634C0532925a3b844Bc9e7595f8dEe`  
**Chain**: ETH  
**Detection Time**: 2026-04-16  
**Overall Risk Score**: 73/100  
**Risk Level**: [CRIT] Extreme Risk  

---

## Risk Scoring Methodology

| Risk Level | Score Range | Recommended Action |
|------------|-------------|-------------------|
| [CRIT] Extreme Risk | >= 70 | IGNORE DIRECTLY |
| [HIGH] High Risk | 50-69 | STAY AWAY |
| [MED] Medium Risk | 30-49 | OBSERVE ONLY |
| [LOW] Low Risk | < 30 | STUDY & RESEARCH |

**Scoring Weights**: Contract Code (35%) / Holder Distribution (20%) / Liquidity Management (25%) / Developer Association (10%) / Marketing Narrative (10%)

---

## 1. Contract Code Risk

| Detection Item | Result | Risk Signal |
|----------------|--------|-------------|
| Honeypot | [WARN] YES | [!!] Investors cannot sell |
| Sell Tax | 15.0% | [!!] High sell tax |
| Buy Tax | 0.0% | [OK] Normal |
| Hidden Owner | [WARN] YES | [!!] Hidden controller exists |
| Contract Verified | [WARN] NO | [!!] Code not verified, cannot audit |
| Mintable | [WARN] YES | [!!] Team can mint anytime |
| Owner Can Take Back | [WARN] YES | [!!] Ownership can be reclaimed |
| Owner Address | 0x742d... | - |
| **Risk Score** | **100/100** | |

**Key Findings**:
- Contract detected as **HONEYPOT** - investors can buy but cannot sell
- Sell tax as high as **15.0%**, severely exploitative
- Contract not verified, code cannot be audited
- Hidden owner exists, contract can be modified anytime

---

## 2. Holder Distribution

| Detection Item | Result | Risk Signal |
|----------------|--------|-------------|
| Top 10 Holders | 78.5% | [!!] Highly concentrated |
| Top 50 Holders | 95.2% | [!!] Extremely concentrated |
| Total Holders | 156 | [!!] Very few participants |
| New Wallets (24h) | 89 | [!!] Suspicious growth |
| **Risk Score** | **50/100** | |

**Key Findings**:
- Top 10 addresses control **78.5%** of tokens
- Top 50 addresses control **95.2%** of tokens
- Only **156** total holders, extremely poor liquidity

---

## 3. Liquidity Management

| Detection Item | Result | Risk Signal |
|----------------|--------|-------------|
| LP Locked | [WARN] NO | [!!] Liquidity can be withdrawn anytime (Rug Pull risk) |
| Lock Duration | 0 days | [!!] Not locked |
| Liquidity Size | $45,000 | [!!] Extremely low, easily manipulated |
| LP Holders | 3 | [!!] Very few control liquidity |
| **Risk Score** | **65/100** | |

**Key Findings**:
- **Liquidity not locked**, can be withdrawn anytime (Rug Pull risk)
- Liquidity only **$45,000**, extremely easy to manipulate
- Only **3** LP holders, highly concentrated

---

## 4. Developer Association

| Detection Item | Result | Risk Signal |
|----------------|--------|-------------|
| Team Doxxed | [WARN] NO | [!!] Anonymous team, cannot trace |
| Website | [OK] YES | [OK] Has website |
| Whitepaper | [WARN] NO | [!!] No technical documentation |
| Social Media | 1 | [!!] Only 1 social account |
| **Risk Score** | **45/100** | |

**Key Findings**:
- Team is completely **anonymous**, cannot be traced
- No whitepaper, lacks technical documentation

---

## 5. Marketing Narrative

| Detection Item | Result | Risk Signal |
|----------------|--------|-------------|
| Promises High Returns | [WARN] YES | [!!] Promises unrealistic returns |
| Viral Marketing | [WARN] YES | [!!] Uses viral marketing tactics |
| Celebrity Endorsement | [OK] NO | [OK] No false endorsement |
| Narrative Consistency | contradictory | [!!] Contradictory claims |
| **Risk Score** | **70/100** | |

**Key Findings**:
- Promises **unrealistic returns** to attract investors
- Uses **viral marketing** tactics
- Marketing claims **contradict** on-chain data

---

## Project Claims vs On-Chain Facts

| Dimension | Project/KOL Claims | On-Chain Facts |
|-----------|-------------------|----------------|
| **Technology** | "AI-driven next-gen blockchain" | Contract has honeypot, investors cannot sell |
| **Listing** | "Listing on Binance soon" | No evidence, liquidity only $45k |
| **Returns** | "Early investors get 100x returns" | 15% sell tax, team can mint anytime |
| **Team** | "Top AI experts" | Completely anonymous, cannot verify |
| **Security** | "Audited secure contract" | Not verified, hidden owner exists |

---

## Comprehensive Assessment

### Risk Calculation

| Vulnerability | Weight | Score | Weighted |
|--------------|--------|-------|----------|
| Contract Code | 35% | 100 | 35.0 |
| Holder Distribution | 20% | 50 | 10.0 |
| Liquidity Management | 25% | 65 | 16.25 |
| Developer Association | 10% | 45 | 4.5 |
| Marketing Narrative | 10% | 70 | 7.0 |
| **Total** | **100%** | - | **72.75** |

### Classification Result

- **Risk Level**: [CRIT] Extreme Risk
- **Overall Score**: 73/100
- **Recommended Action**: IGNORE DIRECTLY - The token exhibits clear fraudulent characteristics (honeypot, unlocked liquidity, etc.). Participation risk is extremely high. Recommended to completely disregard.

---

## Historical Similar Patterns

- Similar to case [RUGAI_2024](./RUGAI_2024.md) - Same honeypot + high sell tax pattern, collapsed after 48 hours
- Similar to case [FAKEMEME_2025](./FAKEMEME_2025.md) - Anonymous team, viral marketing, 95% top 50 concentration

---

## Key Signal Summary

1. [!!] **HONEYPOT DETECTED** - Investors cannot sell after buying
2. [!!] **15% SELL TAX** - Highly exploitative tax rate
3. [!!] **LIQUIDITY NOT LOCKED** - Can be withdrawn anytime (Rug Pull risk)
4. [!!] **ANONYMOUS TEAM** - Cannot trace responsibility
5. [!!] **CONTRADICTORY NARRATIVE** - Marketing claims contradict on-chain data

---

## Data Verification Links

- [View on GoPlus Security](https://gopluslabs.io/token-security/1/0x742d35Cc6634C0532925a3b844Bc9e7595f8dEe)
- [View on Etherscan](https://etherscan.io/token/0x742d35Cc6634C0532925a3b844Bc9e7595f8dEe)
- [View on DEX Screener](https://dexscreener.com/ethereum/0x742d35Cc6634C0532925a3b844Bc9e7595f8dEe)

---

*This fact sheet only presents on-chain verifiable facts and does not constitute investment advice.*

*Detection Time: 2026-04-16*

*Data Sources: GoPlus Security API, DEX Screener, Etherscan*

*License: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)*
