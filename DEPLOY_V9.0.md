# V9.0 部署指南

> 部署时间: 2026-04-17 01:00 CST
> 目标: GitHub Actions自动发布 (02:00 CST)
> 版本: V9.0 Final (2058)

---

## 部署文件清单

### 核心文件 (必须推送)

| 文件 | 路径 | 变更 |
|------|------|------|
| `generate_enhanced_full_report.py` | `scripts/` | 大量修改 (所有修复) |
| `fetch_pattern_real.py` | 根目录 | 添加默认模式 |
| `anomaly_historical_cases.json` | `data/` | 新增历史案例数据 |

### GitHub Actions配置

| 文件 | 路径 | 变更 |
|------|------|------|
| `generate-report-v9.yml` | `.github/workflows/` | 新增V9.0工作流 |

---

## 部署步骤

### 步骤1: 推送代码到GitHub

```bash
# 进入项目目录
cd F:\stepclaw\agents\blockchain-analyst

# 添加所有变更
git add .

# 提交
git commit -m "V9.0 Final: 14-module complete release

- Add Module 11: Quantum Computing Threat Monitor with timeline
- Fix Module 6: Risk score criteria unified to ≥40
- Fix Module 7: Add USDT/WBTC centralized risk note
- Fix Module 8: Add Pattern Observations status messages
- Fix Module 12: Add heatmap data source note
- Fix Module 14: Add 4 historical scam cases
- Fix meta description: 13 → 14 modules
- Add historical cases data file
- All 14 modules production-ready"

# 推送
git push origin main
```

### 步骤2: 验证GitHub Actions

1. 访问: `https://github.com/peteryang546/crypto-risk-radar/actions`
2. 检查是否有新的workflow: "Generate Crypto Risk Radar Report V9.0"
3. 等待02:00 CST自动触发，或手动触发

### 步骤3: 验证报告生成

1. 等待Actions完成 (约5-10分钟)
2. 检查输出: `reports/enhanced_report_YYYYMMDD_HHMM.html`
3. 验证GitHub Pages更新: `https://peteryang546.github.io/crypto-risk-radar/`

---

## 验证清单

### 报告内容验证

| 检查项 | 期望结果 |
|--------|----------|
| 模块数量 | 14个模块全部显示 |
| Module 6 | 标题显示 "Risk Score ≥40" |
| Module 7 | USDT/WBTC有黄色注释框 |
| Module 8 | 显示状态说明文字 |
| Module 11 | 量子计算威胁+时间轴 |
| Module 12 | 热力图有数据说明注释 |
| Module 14 | 4个历史案例表格 |
| Meta | description显示"14-module" |

### 数据验证

| 检查项 | 期望结果 |
|--------|----------|
| BTC价格 | 实时数据 (~$74,000) |
| ETH价格 | 实时数据 (~$2,300) |
| 代币解锁 | 10个事件 |
| 安全威胁 | 2个检测 |
| 高风险代币 | 5个 |

---

## 自动发布时间表

GitHub Actions将在以下时间自动运行:

| CST | UTC | 说明 |
|-----|-----|------|
| 02:00 | 18:00 | 第一次运行 (今日) |
| 10:00 | 02:00 | 第二次运行 |
| 18:00 | 10:00 | 第三次运行 |

**今日首次运行**: 2026-04-17 02:00 CST

---

## 回滚方案

如果部署出现问题:

```bash
# 回滚到V6.2
git revert HEAD
git push origin main

# 或切换到V6.2 workflow
git checkout .github/workflows/generate-report.yml
git rm .github/workflows/generate-report-v9.yml
git commit -m "Rollback to V6.2"
git push origin main
```

---

## 更新日志 (V9.0)

### 新增模块
- **Module 11**: Quantum Computing Threat Monitor
  - 威胁评估表格
  - 2025-2040时间轴
  - 关键发展监控

### 修复问题
- **Module 6**: 筛选条件标题统一 (≥40)
- **Module 7**: USDT/WBTC中心化风险注释
- **Module 8**: Pattern Observations状态说明
- **Module 12**: 热力图数据来源注释
- **Module 14**: 4个历史骗局案例

### 数据文件
- `data/anomaly_historical_cases.json` (4个案例)

---

## 联系与反馈

- GitHub Issues: `https://github.com/peteryang546/crypto-risk-radar/issues`
- 反馈邮箱: crypto-risk-radar@protonmail.com

---

*部署时间: 2026-04-17 01:00 CST*
*版本: V9.0 Final (2058)*
*状态: 等待02:00自动发布*
