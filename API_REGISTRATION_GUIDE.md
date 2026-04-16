# API Registration Guide - Crypto Risk Radar
# API 注册指南

## 概述

当前系统使用以下 API 获取数据。部分 API 需要注册获取 API Key。

---

## 已配置的 API

### 1. Etherscan API ✅ 已配置

**状态**: 已配置（使用现有 key）
**用途**: 获取以太坊链上数据（交易历史、持仓分布）
**当前 Key**: `T37QQ98EHJXE6B6YEA2ZG9KVSTXA4UGKGK`

**注册链接**: https://etherscan.io/apis
**免费额度**: 5 calls/second

---

### 2. CoinGecko API ✅ 已配置

**状态**: ✅ 已配置（2026-04-16 17:30 CST）
**用途**: 获取价格、市值、交易量数据
**当前 Key**: `CG-m57LMPhhuqyQs2QLzUJ6ozAK`

**注册链接**: https://www.coingecko.com/en/api
**免费额度**: Demo plan 10-30 calls/minute

**配置位置**:
- `config.py`: `COINGECKO_API_KEY`
- `scripts/fetch_data_via_ps.ps1`: `$CoinGeckoApiKey`

---

### 3. GoPlus Security API ✅ 已配置

**状态**: ✅ 已配置（2026-04-16 17:30 CST）
**用途**: 合约安全检测（Honeypot、税率、隐藏所有者等）
**当前 Key**: 
- APP KEY: `XPPWb0UTTAumkyGXPxKd`
- APP Secret: `DJMyH3wA0caqv0zmWpGkazasKGz1y3As`

**注意**: GoPlus API 返回 code=4012（签名验证失败），可能需要使用不同的认证方式或联系 GoPlus 支持。

**注册链接**: https://gopluslabs.io/
**文档**: https://docs.gopluslabs.io/

**配置位置**:
- `token_research_framework.py`: `TokenResearcher.__init__`

---

### 4. DEX Screener API ✅ 公共 API

**状态**: ✅ 公共 API，无需注册
**用途**: 获取 DEX 流动性、交易量数据
**问题**: 当前存在 SSL 连接问题（Python 环境）

**文档**: https://docs.dexscreener.com/

**注意**: DEX Screener 连接问题可能是本地 Python SSL 配置问题，非 API Key 问题。使用 PowerShell 数据获取器可绕过此问题。

---

### 4. DEX Screener API ❌ 无需注册

**状态**: 免费公共 API，但当前连接失败
**用途**: 获取 DEX 流动性、交易量数据
**问题**: 可能是网络/SSL 问题，非 API Key 问题

**注意**: DEX Screener 提供公共 API，无需 API Key
**文档**: https://docs.dexscreener.com/

---

## 优先级建议

| 优先级 | API | 原因 |
|--------|-----|------|
| 🔴 高 | CoinGecko | 核心价格数据源，免费版限制严格 |
| 🟡 中 | GoPlus | 合约安全检测，v9.0 五大软肋核心 |
| 🟢 低 | DEX Screener | 公共 API，问题可能是网络配置 |

---

## 当前数据获取路径（网络不畅时）

根据 `.github/workflows/generate-report.yml` 和 `scripts/data_fetcher_ps.py`：

### GitHub Actions 环境
```
GitHub Actions (Ubuntu)
    ↓
PowerShell Script (fetch_data_via_ps.ps1)
    ↓
Invoke-RestMethod (绕过 Python SSL 问题)
    ↓
CoinGecko API → Fear & Greed API → DEX Screener API
```

### 本地 Windows 环境
```
Python Script
    ↓
data_fetcher_ps.py
    ↓
PowerShell Execution
    ↓
Invoke-RestMethod
    ↓
API Endpoints
```

### 人工研究模式（API 完全不可用时）
```
用户发现代币
    ↓
manual_research_cli.py
    ↓
用户提供数据（从网站手动复制）
    ↓
AI 处理 → 生成报告 → 保存案例库
```

---

## 快速修复方案

### 方案 1: 使用 PowerShell 数据获取器（推荐）

已配置的 `data_fetcher_ps.py` 使用 PowerShell 绕过 Python SSL 问题：

```bash
# 测试 PowerShell 数据获取
cd F:\stepclaw\agents\blockchain-analyst
python scripts\data_fetcher_ps.py
```

### 方案 2: 使用人工研究 CLI

当所有 API 都不可用时，使用人工模式：

```bash
python manual_research_cli.py
```

---

## 注册后配置步骤

### 1. CoinGecko API Key

```bash
# 1. 注册并获取 API Key
# 2. 添加到 GitHub Secrets（GitHub Actions 使用）
#    Repository → Settings → Secrets → New repository secret
#    Name: COINGECKO_API_KEY
#    Value: your_api_key

# 3. 本地测试时修改 config.py
COINGECKO_API_KEY = "your_api_key_here"
```

### 2. GoPlus Security API Key

```bash
# 1. 注册并获取 API Key
# 2. 修改 token_research_framework.py

class TokenResearcher:
    def __init__(self, goplus_api_key: Optional[str] = "your_api_key"):
        self.goplus_api_key = goplus_api_key
```

---

## 测试 API 连接

```bash
# 运行 API 测试脚本
cd F:\stepclaw\agents\blockchain-analyst
python test_api_connectivity.py
```

---

## 总结

| API | 当前状态 | 需要操作 |
|-----|---------|---------|
| Etherscan | ✅ 已配置 | 无需操作 |
| CoinGecko | ⚠️ 免费版 | **推荐注册** API Key |
| GoPlus | ⚠️ 可能受限 | **推荐注册** API Key |
| DEX Screener | ❌ 连接失败 | 检查网络/SSL，无需注册 |

**建议**: 优先注册 CoinGecko API Key，可显著提升数据获取稳定性。
