# 区块链风险雷达 - SKILL.md (v6.0 HTML版)

**版本**: 6.0  
**状态**: 生产就绪  
**最后更新**: 2026-04-12  
**发布周期**: 12小时  

---

## 核心使命

> "Don't report data. Deliver judgment."

提供可执行的风险判断，12小时更新周期，8个完整模块。

---

## 强制输出结构 (8模块)

每个报告必须包含以下8个模块：

### 1. QUANT SIGNAL (量化综合信号)
- Final Score: -2.0 到 +2.0
- Grade: [HIGH RISK] / [MEDIUM RISK] / [NEUTRAL] / [LOW RISK] / [STRONG]
- Signal Consistency Index
- HTML表格展示7个因子计算

### 2. ON-CHAIN BEHAVIOR (链上行为)
- Accumulation/Distribution Score
- Exchange netflow (24h/7d)
- Whale holdings
- Long-term holder supply
- MVRV Z-score
- Miner Activity

### 3. MARKET MICROSTRUCTURE (市场微观结构)
- Short Squeeze Probability
- Funding rate
- Futures premium
- Open interest change
- 24h Liquidations

### 4. SCAM & ANOMALY ALERT (骗局与异常检测)
- Alert Level
- New token alerts
- High-risk flagged
- Risk Indicators

### 5. HISTORICAL BACKTEST (历史回测)
- **HTML表格**展示历史匹配事件
- 包含: Date, Signal Score, BTC Price, 2W Return, Condition, Result

### 6. SCENARIO ANALYSIS (情景分析)
- **HTML表格**展示Bull/Base/Bear三种情景
- 包含: Scenario, Probability, Trigger, Action, Target, R:R
- Position Sizing Guidance

### 7. MACRO & MARKET CONTEXT (宏观与市场背景)
- DXY, S&P 500, US 10Y Yield
- BTC Spot ETF Flow
- Put/Call Ratio
- Stablecoin Supply
- Exchange Reserves
- Bitcoin Dominance

### 8. SECURITY ALERTS (安全预警)
- **HTML表格**展示Confirmed Honeypots
- **HTML表格**展示High Risk Tokens
- Daily Threat Summary
- Protection Advice

---

## 表格格式规范

### 使用HTML表格
所有表格必须使用HTML格式，而非Markdown表格：

```html
<div style="overflow-x: auto; margin: 15px 0;">
<table style="border-collapse: collapse; width: 100%; font-family: Arial, sans-serif; font-size: 14px;">
  <thead>
    <tr style="background-color: #4472C4; color: white;">
      <th style="padding: 10px; border: 1px solid #ddd; text-align: left;">Header</th>
    </tr>
  </thead>
  <tbody>
    <tr style="background-color: #f9f9f9;">
      <td style="padding: 8px; border: 1px solid #ddd;">Data</td>
    </tr>
  </tbody>
</table>
</div>
```

### 表格样式要求
- 表头背景: `#4472C4` (蓝色)
- 表头文字: 白色
- 交替行背景: `#f9f9f9` 和 `white`
- 边框: `1px solid #ddd`
- 响应式: `overflow-x: auto`

---

## 发布标准

| 项目 | 标准 |
|------|------|
| 时间格式 | ET (美东时间) |
| 表格格式 | HTML表格 |
| 历史回测 | HTML表格 |
| Scenario | HTML表格 |
| Security | HTML表格 |
| 语言 | 全英文 |
| Emoji | 替换为标签 [HIGH RISK] 等 |
| SEO | 简单hashtag |
| 结尾 | 无生成时间戳 |
| **Report ID** | **禁止在发布内容中显示** |

---

## 生成脚本

### 主脚本
```bash
python scripts\generate_v60_html_report.py
```

### 清理脚本
```bash
python scripts\publish_html_cleaner.py output\v60_html_report_YYYYMMDD_HHMM.md
```

### 自动发布
```bash
python scripts\auto_publish_v60_workflow.py
```

---

## 输出文件

```
output/
├── v60_html_report_YYYYMMDD_HHMM.md      # 原始HTML报告
├── publish_v60_html_report_YYYYMMDD_HHMM.md  # 清理版本
└── logs/
    └── publish_log_YYYYMMDD.json         # 发布日志
```

---

**版本**: 6.0  
**更新日期**: 2026-04-12
