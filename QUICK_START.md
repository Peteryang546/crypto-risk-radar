# Crypto Risk Radar v9.0 - Quick Start Guide

## 系统状态 (2026-04-16 17:35 CST)

| 组件 | 状态 | 说明 |
|------|------|------|
| **PowerShell 数据获取** | ✅ 正常 | BTC: $74,820, ETH: $2,345, F&G: 23 (Extreme Fear) |
| **报告生成** | ✅ 正常 | v6.2 报告生成成功 |
| **定时任务** | ✅ 就绪 | 18:00 CST 自动运行 |
| **API Keys** | ✅ 已配置 | CoinGecko, GoPlus 已配置 |

---

## 快速开始

### 1. 查看当前数据

```bash
# 使用 PowerShell 数据获取器（推荐）
python scripts/data_fetcher_ps.py
```

### 2. 生成报告

```bash
# 生成完整报告
python scripts/generate_full_integrated_report.py

# 报告位置
# output/full_report_YYYYMMDD_HHMM.html
```

### 3. 人工研究模式（API 受限时）

```bash
# 运行交互式 CLI（需要手动输入）
python manual_research_cli.py
```

**CLI 使用步骤**:
1. 输入合约地址
2. 输入代币符号
3. 选择链（1=ETH, 56=BSC）
4. 按提示访问 GoPlus/DEX Screener/Etherscan
5. 复制数据粘贴到 CLI
6. 确认并保存报告

---

## API 配置状态

| API | Key | 状态 |
|-----|-----|------|
| **CoinGecko** | `CG-m57LMPhhuqyQs2QLzUJ6ozAK` | ✅ 已配置 |
| **GoPlus** | APP KEY: `XPPWb0UTTAumkyGXPxKd` | ✅ 已配置 |
| **DEX Screener** | 公共 API | ✅ 无需配置 |
| **Etherscan** | `T37QQ98EHJXE6B6YEA2ZG9KVSTXA4UGKGK` | ✅ 已配置 |

---

## 文件位置

| 文件 | 路径 | 用途 |
|------|------|------|
| **项目身份** | `PROJECT_IDENTITY.md` | 项目使命与原则 |
| **升级计划** | `UPGRADE_PLAN_v9.0.md` | v9.0 完整升级计划 |
| **API 注册指南** | `API_REGISTRATION_GUIDE.md` | API 配置说明 |
| **交互流程** | `INTERACTION_WORKFLOW.md` | 人机协作流程 |
| **快速开始** | `QUICK_START.md` | 本文件 |
| **CLI 工具** | `manual_research_cli.py` | 人工研究工具 |
| **数据获取** | `scripts/data_fetcher_ps.py` | PowerShell 数据获取 |
| **报告生成** | `scripts/generate_full_integrated_report.py` | 完整报告生成 |

---

## 定时任务

| 时间 (CST) | 任务 | 状态 |
|-----------|------|------|
| 02:00 | CryptoRiskRadar_14 | ✅ 启用 |
| 10:00 | CryptoRiskRadar_22 | ✅ 启用 |
| 18:00 | CryptoRiskRadar_06 | ✅ 启用 |

**下次运行**: 今天 18:00 CST

---

## 网站

**Live Website**: https://peteryang546.github.io/crypto-risk-radar/

---

## 许可证

CC BY 4.0 - https://creativecommons.org/licenses/by/4.0/
