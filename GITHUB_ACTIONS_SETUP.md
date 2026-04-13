# GitHub Actions 自动发布配置

## 概述

由于本地网络环境存在 SSL/TLS 连接问题，无法直接访问 DEX Screener、CoinGecko 等 API，我们将报告生成任务迁移到 GitHub Actions 云端执行。

## 优势

- ✅ **免费**: GitHub Actions 每月 2000 分钟免费额度
- ✅ **稳定**: 云端网络环境正常，API 可访问
- ✅ **自动化**: 定时任务，无需手动操作
- ✅ **可靠**: 不再依赖本地网络环境

## 配置步骤

### 1. 上传代码到 GitHub

```bash
git add .
git commit -m "Add GitHub Actions workflow for automated report generation"
git push origin main
```

### 2. 配置 GitHub Secrets (可选)

如果需要使用 CoinGecko API Key:

1. 访问仓库 Settings → Secrets and variables → Actions
2. 点击 "New repository secret"
3. 名称: `COINGECKO_API_KEY`
4. 值: `CG-m57LMPhhuqyQs2QLzUJ6ozAK`
5. 点击 "Add secret"

### 3. 启用 GitHub Pages

1. 访问仓库 Settings → Pages
2. Source 选择 "Deploy from a branch"
3. Branch 选择 "gh-pages" / "/ (root)"
4. 点击 "Save"

### 4. 首次手动触发

1. 访问仓库 Actions 页面
2. 点击 "Generate Crypto Risk Radar Report"
3. 点击 "Run workflow"
4. 观察日志输出

## 定时任务

已配置每天运行两次：
- 00:00 UTC = 08:00 北京时间
- 12:00 UTC = 20:00 北京时间

## 文件结构

```
.github/
└── workflows/
    └── generate-report.yml    # GitHub Actions 工作流配置

scripts/
├── generate_full_integrated_report.py  # 报告生成脚本
└── test_github_actions.py              # API 测试脚本

output/                              # 生成的报告目录
├── full_report_YYYYMMDD_HHMM.html   # 完整报告
└── index.html                       # 最新报告副本
```

## 本地开发

在本地开发时，使用演示数据模式：

```bash
python scripts/generate_full_integrated_report.py --demo
```

生产环境（GitHub Actions）使用真实数据：

```bash
python scripts/generate_full_integrated_report.py --live
```

## 故障排除

### 问题: Actions 运行失败

**检查项**:
1. 确认 Python 版本正确 (3.11)
2. 确认依赖安装成功
3. 检查 API 调用日志

### 问题: GitHub Pages 未更新

**检查项**:
1. 确认 gh-pages 分支存在
2. 确认 Pages 设置正确
3. 检查 Actions 日志中的部署步骤

### 问题: API 调用失败

**在 Actions 环境中**:
- 检查 API 密钥是否正确设置
- 检查 API 速率限制
- 查看详细错误日志

## 监控

- Actions 运行状态: https://github.com/peteryang546/crypto-risk-radar/actions
- 生成的报告: https://peteryang546.github.io/crypto-risk-radar/

## 更新日志

- 2026-04-13: 初始配置完成
