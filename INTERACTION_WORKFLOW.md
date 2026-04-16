# Human-in-the-Loop Interaction Workflow
# 人机交互流程设计

## 概述

当自动 API 数据获取受限时，采用 **"AI 指导 + 人工查询 + AI 记录"** 的协作模式。

---

## 场景 1: 新代币分析（API 受限时）

### 流程图

```
[用户发现新代币]
    ↓
[用户提供合约地址]
    ↓
[AI 指导人工查询步骤]
    ↓
[用户访问 GoPlus/DEX Screener/Etherscan]
    ↓
[用户复制关键数据给 AI]
    ↓
[AI 自动填充五大软肋数据]
    ↓
[AI 计算风险评分]
    ↓
[AI 生成完整报告]
    ↓
[用户复核并确认分类]
    ↓
[AI 保存到案例库]
```

### 详细步骤

#### Step 1: 用户提供合约地址

**用户输入**:
```
分析这个代币: 0x742d35Cc6634C0532925a3b844Bc9e7595f8dEe
```

#### Step 2: AI 提供查询指南

**AI 回复**:
```
收到！请按以下步骤查询数据：

## 1. GoPlus Security (合约安全)
访问: https://gopluslabs.io/token-security/1/0x742d35Cc6634C0532925a3b844Bc9e7595f8dEe
请复制以下信息：
- Is Honeypot: (YES/NO)
- Sell Tax: (X%)
- Buy Tax: (X%)
- Hidden Owner: (YES/NO)
- Is Open Source: (YES/NO)
- Is Mintable: (YES/NO)

## 2. DEX Screener (流动性)
访问: https://dexscreener.com/ethereum/0x742d35Cc6634C0532925a3b844Bc9e7595f8dEe
请复制：
- Liquidity: ($X)
- 24h Volume: ($X)
- Top 10 Holders: (X%)
- LP Locked: (YES/NO)

## 3. Etherscan (持仓)
访问: https://etherscan.io/token/0x742d35Cc6634C0532925a3b844Bc9e7595f8dEe#balances
请复制：
- Total Holders: (X)
- Top 10 addresses percentage

完成后粘贴数据，我将自动生成报告。
```

#### Step 3: 用户提供数据

**用户输入**:
```
GoPlus数据:
- Is Honeypot: YES
- Sell Tax: 15%
- Buy Tax: 0%
- Hidden Owner: YES
- Is Open Source: NO
- Is Mintable: YES

DEX Screener:
- Liquidity: $45,000
- 24h Volume: $320,000
- LP Locked: NO

Etherscan:
- Total Holders: 156
- Top 10: 78.5%
```

#### Step 4: AI 自动处理

**AI 执行**:
1. 自动填充五大软肋数据类
2. 计算各维度风险评分
3. 计算综合评分
4. 生成分类建议
5. 生成完整报告

**AI 回复**:
```
[OK] 数据已录入，正在分析...

## 五大软肋评分

| 软肋 | 得分 | 关键发现 |
|------|------|----------|
| 合约代码 | 100/100 | HONEYPOT + 15%卖出税 + 未开源 |
| 持仓分布 | 50/100 | 前10持仓78.5%，仅156人 |
| 流动性管理 | 65/100 | 未锁仓，仅$45k |
| 开发者关联 | 45/100 | 匿名团队，无白皮书 |
| 营销叙事 | 待补充 | 需要您提供项目方宣传内容 |

## 当前综合评分: 65/100

请提供项目方的营销内容（官网/Twitter宣传），我将完成最后10%的评分。
```

#### Step 5: 用户补充营销信息

**用户输入**:
```
项目方声称:
- "AI驱动的下一代区块链"
- "即将上线币安"
- "早期投资者将获得100x回报"
```

#### Step 6: AI 完成分析

**AI 执行**:
- 营销叙事评分: 70/100（承诺高回报+叙事矛盾）
- 重新计算综合评分: 73/100
- 生成分类: [CRIT] Extreme Risk
- 生成完整报告

**AI 回复**:
```
## 最终分析结果

**综合评分**: 73/100
**风险等级**: [CRIT] Extreme Risk
**应对策略**: IGNORE DIRECTLY

完整报告已生成，请复核：
[报告内容...]

## 确认分类

请选择：
[1] 确认 - [CRIT] Extreme Risk → IGNORE DIRECTLY
[2] 调整 - [HIGH] High Risk → STAY AWAY
[3] 添加备注
[4] 重新分析
```

#### Step 7: 用户确认

**用户输入**:
```
1
```

#### Step 8: AI 保存到案例库

**AI 执行**:
- 保存公开摘要到 `case_studies/public/`
- 保存完整报告到 `case_studies/private/`
- 更新索引文件
- 生成 Git commit 信息

**AI 回复**:
```
[OK] 案例已保存

**案例ID**: FAKEAI_595F8DEE
**位置**: 
- 公开: case_studies/public/FAKEAI_595F8DEE.md
- 私有: case_studies/private/FAKEAI_595F8DEE.md

**下一步**:
- [D] 发现新代币
- [L] 查看待办列表
- [S] 查看统计
- [Q] 退出
```

---

## 场景 2: 批量快速分类

### 流程

当用户有多个代币需要快速分类时：

```
[用户提供多个合约地址]
    ↓
[AI 生成批量查询清单]
    ↓
[用户逐个查询并粘贴数据]
    ↓
[AI 自动计算所有评分]
    ↓
[AI 生成待办列表]
    ↓
[用户批量确认分类]
```

### 示例

**用户输入**:
```
批量分析这3个代币:
1. 0xabc...
2. 0xdef...
3. 0xghi...
```

**AI 回复**:
```
## 批量查询清单

请按以下格式提供数据（可复制粘贴）：

### Token 1: 0xabc...
GoPlus: [honeypot: YES/NO, sell_tax: X%, ...]
DEX: [liquidity: $X, volume: $X, ...]
Etherscan: [holders: X, top10: X%]
Marketing: [项目方宣传内容]

### Token 2: 0xdef...
...

### Token 3: 0xghi...
...
```

---

## 场景 3: 案例库查询

### 查询历史案例

**用户输入**:
```
查询类似 RUGAI_2024 的案例
```

**AI 回复**:
```
## 相似案例

找到 2 个相似案例：

1. **FAKEAI_595F8DEE** (2026-04-16)
   - 相似度: 95%
   - 共同特征: Honeypot + 高卖出税 + 匿名团队
   - 结果: 已分类为 [CRIT]

2. **SCAMTOKEN_2025** (2025-11-20)
   - 相似度: 80%
   - 共同特征: 未锁仓流动性 + 病毒式营销
   - 结果: 48小时后归零

[查看详情] [返回]
```

---

## 数据输入格式

### 标准格式（推荐）

```
[GoPlus]
honeypot: YES
sell_tax: 15
buy_tax: 0
hidden_owner: YES
is_open_source: NO
is_mintable: YES

[DEX]
liquidity: 45000
volume_24h: 320000
lp_locked: NO
top10_percentage: 78.5

[Etherscan]
total_holders: 156

[Marketing]
claims: AI-powered next-gen blockchain, listing on Binance soon, 100x returns
```

### 自由格式（AI 自动解析）

用户也可以直接粘贴网页内容，AI 会自动提取关键数据。

---

## 快捷键

| 命令 | 功能 |
|------|------|
| `D` | 发现新代币 |
| `A <address>` | 分析指定地址 |
| `L` | 查看待办列表 |
| `C` | 快速分类 |
| `S` | 查看统计 |
| `F <token>` | 查找相似案例 |
| `H` | 帮助 |
| `Q` | 退出 |

---

## 错误处理

### 数据不完整时

**AI 回复**:
```
[WARN] 数据不完整，以下字段缺失：
- 买入税率
- LP锁仓时长

请补充，或使用默认值（买入税率=0, 锁仓时长=0）继续？
[Y] 使用默认值继续
[N] 补充数据
```

### 数据矛盾时

**AI 回复**:
```
[WARN] 检测到数据矛盾：
- GoPlus显示: Honeypot = NO
- 但用户反馈: 无法卖出

请确认哪个数据正确：
[1] 以GoPlus为准
[2] 以用户实测为准
[3] 标记为存疑，继续分析
```

---

## 输出文件

### 公开文件（所有人可见）

`case_studies/public/TOKEN_CASEID.md`
- 基本信息
- 风险等级
- 关键信号
- 摘要
- Claims vs Facts
- 相似案例

### 私有文件（仅内部）

`case_studies/private/TOKEN_CASEID.md`
- 完整合约地址
- 交易哈希
- 钱包地址
- 内部调查备注

---

## 总结

**核心原则**:
1. **AI 指导**: 告诉用户查什么、去哪查
2. **人工查询**: 用户访问网站、复制数据
3. **AI 处理**: 自动计算、生成报告
4. **人工确认**: 用户复核分类
5. **AI 保存**: 自动归档到案例库

**优势**:
- 绕过 API 限制
- 利用人工判断（营销叙事分析）
- 保持数据可验证性
- 建立案例积累

**效率**:
- 熟练后每个代币 5-10 分钟
- 批量处理可节省时间
- 案例库积累后可直接引用
