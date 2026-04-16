# 区块链风险雷达 - v6.0 变更日志

**版本**: 6.0  
**发布日期**: 2026-04-12  
**状态**: 生产就绪

---

## 核心变更

### 1. 模块扩展 (7 → 8)

新增 **Security Alerts（安全预警）** 模块，包含：
- 8.1 Daily Threat Summary（每日威胁摘要）
- 8.2 Confirmed Honeypots（确认的Honeypot）
- 8.3 High Risk Tokens（高风险代币）
- 8.4 Protection Advice（防护建议）

### 2. 表格格式变更 (Markdown → HTML)

所有表格改用HTML格式，提升可读性和视觉效果：

| 模块 | 旧格式 | 新格式 |
|------|--------|--------|
| QUANT SIGNAL | Markdown表格 | HTML表格 |
| HISTORICAL BACKTEST | Markdown表格 | HTML表格 |
| SCENARIO ANALYSIS | Markdown表格 | HTML表格 |
| SECURITY ALERTS | 无 | HTML表格 |

**HTML表格样式规范**:
- 表头背景: `#4472C4` (蓝色)
- 表头文字: 白色
- 交替行背景: `#f9f9f9` 和 `white`
- 边框: `1px solid #ddd`
- 响应式: `overflow-x: auto`

### 3. 发布标准更新

| 项目 | v5.2 | v6.0 |
|------|------|------|
| Report ID | 显示在报告头部 | **禁止显示** |
| 时间格式 | ET | ET (保持) |
| 语言 | 英文 | 英文 (保持) |
| Emoji | 保留 | 替换为标签 [HIGH RISK] 等 |

**重要**: 从v6.0开始，发布内容中**不再显示Report ID**，仅在内部文件命名中使用。

### 4. 脚本更新

#### 新增脚本
- `generate_v60_html_report.py` - 生成HTML格式报告
- `publish_html_cleaner.py` - 清理HTML报告用于发布
- `auto_publish_v60_workflow.py` - 完整自动化发布流程

#### 废弃脚本
- `generate_v52_report.py` - 旧版Markdown报告
- `clean_report.py` - 旧版清理脚本
- `publish_cleaner.py` - 旧版发布清理

### 5. Cron任务更新

```json
// 旧配置 (v5.2)
{
  "id": "blockchain-discord-morning-810",
  "schedule": "10 8 * * *"
}

// 新配置 (v6.0)
{
  "id": "blockchain-v60-morning-810",
  "schedule": "10 8 * * *",
  "payload": {
    "text": "【Crypto Risk Radar v6.0】Generate 12H report with 8 modules, HTML tables..."
  }
}
```

---

## 发布记录

### 首次发布 (v6.0)
- **时间**: 2026-04-12 08:19:27
- **URL**: https://cryptoriskradar.hashnode.dev/crypto-risk-radar-12h-report-april-12-2026
- **状态**: ✅ 成功
- **模块**: 8个模块完整
- **表格**: HTML格式

---

## 技术细节

### HTML表格生成函数
```python
def html_table(self, headers, rows, caption=None):
    """生成HTML表格"""
    html = '<div style="overflow-x: auto; margin: 15px 0;">\n'
    if caption:
        html += f'<div style="font-weight: bold; margin-bottom: 8px;">{caption}</div>\n'
    html += '<table style="border-collapse: collapse; width: 100%; font-family: Arial, sans-serif; font-size: 14px;">\n'
    # ... thead, tbody
    return html
```

### 清理规则更新
```python
# 移除Report ID
content = re.sub(r'\*\*Report ID\*\*: .*?\n', '', content)

# 替换emoji
emoji_map = {
    '🔴': '[HIGH RISK]',
    '🟡': '[MEDIUM RISK]',
    '🟢': '[LOW RISK]',
    # ...
}
```

---

## 文件结构

```
agents/blockchain-analyst/
├── scripts/
│   ├── generate_v60_html_report.py    ✅ 新版
│   ├── publish_html_cleaner.py        ✅ 新版
│   ├── auto_publish_v60_workflow.py   ✅ 新版
│   └── hashnode_publisher.py          ✅ 保持
├── output/
│   ├── v60_html_report_YYYYMMDD_HHMM.md
│   └── publish_v60_html_report_YYYYMMDD_HHMM.md
├── logs/
│   └── publish_log_YYYYMMDD.json
├── SKILL.md                           ✅ 已更新
├── MEMORY.md                          ✅ 已更新
└── CHANGELOG_v6.0.md                  ✅ 本文档
```

---

## 后续计划

- [ ] 监控首次发布的读者反馈
- [ ] 优化Security Alerts数据源
- [ ] 考虑添加更多可视化元素

---

**更新日期**: 2026-04-12  
**更新者**: StepClaw Agent  
**审核状态**: ✅ 已审核
