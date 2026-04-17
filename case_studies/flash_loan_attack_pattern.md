# Flash Loan Attack Pattern Analysis

## Overview
Flash loan attacks exploit price oracle manipulation through uncollateralized loans that must be repaid within a single transaction block.

## Common Attack Vectors

### 1. Price Oracle Manipulation
```
Attack Flow:
1. Borrow flash loan (e.g., 10,000 ETH)
2. Swap large amount on DEX A (manipulate price)
3. Exploit price difference on lending protocol
4. Repay flash loan
5. Profit from price discrepancy
```

### 2. Cases Using This Pattern

#### Yearn Finance (2021-02-04)
- **Loss**: $11M
- **Mechanism**: yDAI vault price manipulation
- **Root Cause**: Single oracle source
- **Prevention**: Multi-oracle price feeds

#### Harvest Finance (2020-10-26)
- **Loss**: $24M
- **Mechanism**: Curve pool manipulation
- **Root Cause**: No slippage protection
- **Prevention**: Price deviation checks

#### bZx Protocol (2020-02-15)
- **Loss**: $1M
- **Mechanism**: First documented flash loan exploit
- **Root Cause**: No flash loan awareness
- **Prevention**: Transaction context checks

### 3. Detection Indicators

#### On-Chain Signals
| Indicator | Description | Alert Level |
|-----------|-------------|-------------|
| Large Swap | >$1M swap in single tx | High |
| Flash Loan | Aave/dYdX flash loan | Medium |
| Price Deviation | >5% from other sources | High |
| Multiple Protocols | Tx interacts with >3 protocols | Medium |

#### Prevention Patterns
```solidity
// Price deviation check
require(
    abs(currentPrice - oraclePrice) < MAX_DEVIATION,
    "Price manipulation detected"
);

// Flash loan detection
require(tx.origin == msg.sender, "No contracts");
```

### 4. Risk Assessment Matrix

| Factor | Low Risk | Medium Risk | High Risk |
|--------|----------|-------------|-----------|
| Oracle Sources | 3+ decentralized | 2 sources | Single source |
| Slippage Protection | Yes, strict | Moderate | None |
| Flash Loan Awareness | Yes | Partial | No |
| Price Update Frequency | Real-time | Hourly | Daily |

### 5. Mitigation Strategies

#### Protocol Level
1. **Multi-Oracle Aggregation** (Chainlink, Band, API3)
2. **Time-Weighted Average Price** (TWAP)
3. **Flash Loan Detection** (tx.origin checks)
4. **Slippage Limits** (max 1-2% deviation)

#### Monitoring Level
1. **Real-time Price Monitoring**
2. **Large Transaction Alerts**
3. **Flash Loan Pattern Detection**
4. **Cross-protocol Correlation**

---

**Pattern Type**: Technical Exploit
**Complexity**: High
**Prevention**: Medium (requires protocol design)
