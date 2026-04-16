# Crypto Risk Radar - Setup Checklist

## ✅ 已完成

### 1. 核心框架
- [x] 8小时调度系统 (`run_analysis.py`)
- [x] 配置文件 (`config.py`)
- [x] 欺骗风险评分算法 (`deception_score.py`)
- [x] 历史数据存储 (`history.py`)
- [x] Windows定时任务脚本 (`setup_schedule.bat`)

### 2. 数据采集模块
- [x] 订单簿爬虫 (`orderbook_crawler.py`) - PowerShell桥接
- [x] 休眠地址监控 (`dormant_address.py`) - Etherscan API
- [x] 社交媒体监控 v1 (`social_crawler.py`) - 基础框架
- [x] 社交媒体监控 v2 (`social_crawler_v2.py`) - twikit + telethon

### 3. 依赖安装
- [x] telethon (Telegram API)
- [x] twikit (Twitter 无需API Key)
- [x] ntscraper (Nitter桥接)

### 4. API Keys 配置
- [x] Etherscan API Key: `T37QQ98EHJXE6B6YEA2ZG9KVSTXA4UGKGK`

---

## ⏳ 待配置

### 1. GitHub Token (必需)
**用途**: 上传报告到 GitHub

**设置方法**:
```bash
# Windows Command Prompt
set GITHUB_TOKEN=your_github_personal_access_token

# 或者 PowerShell
$env:GITHUB_TOKEN="your_github_personal_access_token"

# 永久设置 (系统环境变量)
# 控制面板 → 系统 → 高级系统设置 → 环境变量
```

**获取方式**:
1. 访问 https://github.com/settings/tokens
2. 点击 "Generate new token (classic)"
3. 勾选 `repo` 权限
4. 复制生成的 token

---

### 2. Telegram API (可选，用于真实数据)
**用途**: 获取 Telegram 频道消息

**设置方法**:
```bash
set TELEGRAM_API_ID=your_api_id
set TELEGRAM_API_HASH=your_api_hash
```

**获取方式**:
1. 访问 https://my.telegram.org/apps
2. 使用手机号登录
3. 创建新应用
4. 记录 `api_id` 和 `api_hash`

**首次使用需要授权**:
```bash
python -c "from telethon import TelegramClient; client = TelegramClient('session', API_ID, API_HASH); client.start()"
# 输入手机号和验证码
```

---

### 3. Twitter 登录 (可选，twikit 无需 API Key)
**用途**: 获取 Twitter 数据

**说明**: twikit 不需要 API Key，但需要登录一次获取 cookies

**设置方法**:
```bash
set TWITTER_USERNAME=your_username
set TWITTER_EMAIL=your_email
set TWITTER_PASSWORD=your_password
```

**首次使用需要登录**:
```python
from twikit import Client
client = Client('en-US')
client.login(TWITTER_USERNAME, TWITTER_EMAIL, TWITTER_PASSWORD)
client.save_cookies('twitter_cookies.json')
```

---

### 4. CoinGecko API Key (可选)
**用途**: 获取价格数据

**说明**: 免费版有速率限制，付费版更稳定

**获取方式**: https://www.coingecko.com/en/api/pricing

---

## 🧪 测试步骤

### 1. 基础测试
```bash
# 测试订单簿爬虫
python scripts/crawlers/orderbook_crawler.py

# 测试休眠地址监控
python scripts/crawlers/dormant_address.py

# 测试社交媒体监控 (演示模式)
python scripts/crawlers/social_crawler.py
```

### 2. 完整流程测试
```bash
# 设置环境变量
set GITHUB_TOKEN=your_token

# 运行完整分析 (演示模式)
python run_analysis.py

# 检查输出
ls output/
```

### 3. 定时任务设置
```bash
# 以管理员身份运行
setup_schedule.bat

# 验证任务
schtasks /query /tn "CryptoRiskRadar*"
```

---

## 📋 优先级清单

### P0 - 必需 (无法运行)
1. [ ] GitHub Token - 用于上传报告

### P1 - 重要 (影响数据质量)
2. [ ] Telegram API - 获取真实社交数据
3. [ ] Twitter 登录 - 获取真实社交数据

### P2 - 可选 (增强功能)
4. [ ] CoinGecko API Key - 更稳定的价格数据
5. [ ] 自定义监控地址列表 - 添加到 `dormant_address.py`
6. [ ] 自定义 Telegram 频道 - 修改 `social_crawler_v2.py`

---

## 🔧 故障排除

### 问题: "GITHUB_TOKEN not set"
**解决**: 设置环境变量 `GITHUB_TOKEN`

### 问题: "Telegram not authorized"
**解决**: 运行授权脚本，输入手机号和验证码

### 问题: "Twitter login failed"
**解决**: 检查用户名/邮箱/密码，或手动登录保存 cookies

### 问题: "SSL Error"
**解决**: 已使用 PowerShell 桥接，不应出现此问题

---

## 📊 运行状态检查

### 检查定时任务
```bash
schtasks /query /tn "CryptoRiskRadar*" /fo list /v
```

### 检查最近报告
```bash
ls output/report_*.md | sort | tail -5
```

### 检查 GitHub 上传
访问: https://github.com/peteryang546/crypto-risk-radar/tree/main/reports

---

## 📝 配置完成后的下一步

1. **手动运行测试**: `python run_analysis.py`
2. **验证 GitHub 上传**: 检查仓库是否有新报告
3. **启用定时任务**: 运行 `setup_schedule.bat`
4. **监控首次自动运行**: 等待到 14:00, 22:00, 或 06:00
5. **验证网站更新**: https://peteryang546.github.io/crypto-risk-radar/

---

**最后更新**: 2026-04-13 20:55 CST
