# Crypto Risk Radar - Monitoring & Automation Guide

## 📅 更新时间表

### 美国时间 (EST) ↔ 北京时间 (CST)

| 美国时间 | 北京时间 | 市场时段 |
|----------|----------|----------|
| **10:00 PM** | **次日 10:00 AM** | 晚间分析（亚洲收盘） |
| **6:00 AM** | **次日 6:00 PM** | 盘前简报（欧洲早盘） |
| **2:00 PM** | **次日 2:00 AM** | 盘中更新（美国活跃） |

---

## ⚙️ 自动化设置

### 步骤1: 设置定时任务（需要管理员权限）

**方法A: 双击运行（推荐）**
1. 找到 `setup_schedule_us.bat`
2. 右键 → "以管理员身份运行"
3. 按提示完成设置

**方法B: 命令行**
```cmd
# 以管理员身份打开CMD，然后运行：
cd F:\stepclaw\agents\blockchain-analyst
setup_schedule_us.bat
```

### 步骤2: 验证定时任务

```cmd
# 检查任务是否存在
schtasks /query /tn "CryptoRiskRadar*"

# 或运行检查脚本
check_schedule.bat
```

### 步骤3: 测试手动运行

```cmd
# 测试一次完整流程
python run_analysis.py
```

---

## 📊 监控状态

### 检查网站更新

**网站URL**: https://peteryang546.github.io/crypto-risk-radar/

**验证方法**:
1. 查看报告顶部的日期时间
2. 应该显示美国东部时间 (ET)
3. 对比当前时间确认更新

### 检查GitHub仓库

**仓库**: https://github.com/peteryang546/crypto-risk-radar

**查看内容**:
- `index.html` - 主页面（最新报告）
- `current.md` - 文字版摘要
- `reports/` - 历史报告归档
- `api/status.json` - 机器可读数据

---

## 🔔 通知设置

### 运行结果通知

脚本运行后会输出:
```
======================================================================
COMPLETED SUCCESSFULLY
======================================================================
Risk Score: 0/100 (Low)
Next run: 10:00 PM EST (北京时间次日 10:00 AM)
======================================================================
```

### 错误处理

如果运行失败，检查:
1. **GITHUB_TOKEN** 是否设置
2. **网络连接** 是否正常
3. **PowerShell** 是否可用
4. **Python路径** 是否正确

---

## 📝 手动操作指南

### 立即生成并发布报告

```cmd
cd F:\stepclaw\agents\blockchain-analyst

# 1. 生成报告
python scripts\generate_enhanced_full_report.py

# 2. 发布到网站
python publish_report.py
```

### 仅运行分析（不上传）

```cmd
python run_analysis.py
```

### 查看本地报告

```cmd
# 报告位置
F:\stepclaw\agents\blockchain-analyst\output\

# 查看最新HTML报告
start output\enhanced_report_*.html
```

---

## 🔍 故障排除

### 常见问题

| 问题 | 解决方案 |
|------|----------|
| "GITHUB_TOKEN not set" | 设置环境变量: `set GITHUB_TOKEN=your_token` |
| "SSL Error" | 使用PowerShell桥接（已自动处理） |
| "Upload failed" | 检查网络连接和Token权限 |
| "No reports found" | 先运行 `generate_enhanced_full_report.py` |

### 日志文件

运行日志保存在控制台输出中。如需保存到文件:
```cmd
python run_analysis.py > log.txt 2>&1
```

---

## 📈 性能监控

### 检查运行历史

查看 `F:\stepclaw\agents\blockchain-analyst\data\history.json`:
- 历史风险评分
- 运行时间戳
- 指标变化趋势

### 查看GitHub提交记录

https://github.com/peteryang546/crypto-risk-radar/commits/main

---

## 🎯 维护检查清单

**每日检查**:
- [ ] 网站显示最新时间
- [ ] 报告内容完整（10个模块）
- [ ] 无错误提示

**每周检查**:
- [ ] 定时任务正常运行
- [ ] GitHub仓库有更新
- [ ] 历史报告已归档

**每月检查**:
- [ ] 更新依赖包
- [ ] 检查API密钥有效期
- [ ] 备份历史数据

---

## 📞 快速参考

| 操作 | 命令 |
|------|------|
| 手动运行 | `python run_analysis.py` |
| 生成报告 | `python scripts\generate_enhanced_full_report.py` |
| 发布网站 | `python publish_report.py` |
| 设置定时 | `setup_schedule_us.bat` (管理员) |
| 检查状态 | `schtasks /query /tn "CryptoRiskRadar*"` |
| 查看网站 | https://peteryang546.github.io/crypto-risk-radar/ |

---

*Last Updated: April 13, 2026*
*Version: 7.0*
