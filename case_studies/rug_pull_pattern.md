# Rug Pull Pattern Analysis

## Definition
Developer removes liquidity or drains funds after attracting investors, causing token value to collapse to near zero.

## Pattern Variants

### 1. Liquidity Removal (Classic)
**Examples**: SQUID, AnubisDAO, Meerkat Finance

```
Execution Pattern:
1. Create token + liquidity pool
2. Attract investors through marketing
3. Wait for sufficient liquidity
4. Remove LP tokens / drain pool
5. Disappear with funds
```

**Warning Signs**:
- LP tokens not locked
- Developer holds large LP share
- No vesting schedule
- Anonymous team

### 2. Migration Function (Hidden)
**Examples**: Compounder Finance, Meerkat Finance

```solidity
// Hidden migration function
function migrate(address newContract) external onlyOwner {
    // Transfer all funds to new contract
    // New contract controlled by attacker
}
```

**Warning Signs**:
- Unverified contract code
- Complex ownership structures
- Unnecessary migration functions
- No timelock on critical functions

### 3. Sell Restriction (Honeypot)
**Examples**: SQUID

```solidity
// Prevent selling
function _transfer(address from, address to, uint256 amount) internal {
    require(canSell[from] || from == owner(), "Selling disabled");
    super._transfer(from, to, amount);
}
```

**Warning Signs**:
- Cannot sell after buying
- Whitelist-only selling
- Dynamic sell taxes (>50%)
- Blacklist functionality

## Detection Framework

### Automated Checks
| Check | Tool | Risk Level |
|-------|------|------------|
| Honeypot Test | Honeypot.is | Critical |
| Contract Audit | MythX | High |
| LP Lock Status | Team Finance | High |
| Ownership Analysis | Etherscan | Medium |
| Sell Simulation | Tenderly | Critical |

### Manual Verification
1. **Test Sell Function**: Buy small amount, attempt sell
2. **Check LP Lock**: Verify on Team Finance / Uncx
3. **Review Contract**: Look for hidden functions
4. **Team Research**: Verify identities
5. **Community Check**: Reddit, Twitter sentiment

## Risk Scoring

### High Risk (Score 80-100)
- No LP lock
- Honeypot detected
- Anonymous team + hype marketing
- Unverified contracts

### Medium Risk (Score 50-79)
- LP locked < 6 months
- Partially verified team
- Contract has owner privileges
- High concentration

### Low Risk (Score 0-49)
- LP locked > 1 year
- Verified team
- Audited contract
- Fair launch

## Prevention Checklist

### Before Investing
- [ ] Test buy AND sell in same transaction
- [ ] Verify LP lock duration
- [ ] Check contract audit status
- [ ] Research team background
- [ ] Analyze token distribution
- [ ] Review social media sentiment

### Red Flags (Immediate Avoid)
- [ ] Cannot sell after buying
- [ ] Promises guaranteed returns
- [ ] No contract verification
- [ ] Anonymous team + celebrity endorsements
- [ ] Unrealistic APY (>1000%)

## Case Studies by Pattern

| Pattern | Cases | Detection Difficulty |
|---------|-------|---------------------|
| Classic LP Removal | SQUID, AnubisDAO | Easy |
| Hidden Migration | Compounder, Meerkat | Medium |
| Honeypot | SQUID, various memes | Easy (if tested) |
| Slow Rug | Various farm tokens | Hard |

---

**Pattern Type**: Exit Scam
**Prevalence**: Very High (especially on BSC)
**Prevention**: High (if investors verify)
