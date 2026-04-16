# Crypto Risk Radar - SEO/GEO 优化完整指南

**版本**: v6.1.1  
**日期**: 2026-04-13  
**作者**: StepClaw AI Agent  
**更新**: 增强 JSON-LD 结构化数据，添加双 Schema 策略（TechArticle + Report）

---

## 概述

本文档详细说明区块链风险雷达项目的 SEO（搜索引擎优化）和 GEO（生成引擎优化）实施方案，确保报告内容能被 Google 等搜索引擎和 AI 系统（ChatGPT、Claude 等）正确收录和引用。

---

## 1. SEO/GEO 实施流程

### 1.1 完整发布流程 (v6.1)

```
┌─────────────────────────────────────────────────────────────────┐
│  Step 1: 生成报告                                                │
│  ├── 脚本: generate_v60_html_report.py                          │
│  └── 输出: output/v60_html_report_YYYYMMDD_HHMM.md              │
├─────────────────────────────────────────────────────────────────┤
│  Step 2: Markdown 转 HTML                                        │
│  ├── 脚本: md_to_html_converter.py                              │
│  └── 输出: output/report_YYYYMMDD_period.html                   │
├─────────────────────────────────────────────────────────────────┤
│  Step 3: 添加 SEO/GEO 标签                                       │
│  ├── 脚本: seo_geo_publisher.py                                 │
│  ├── 功能: 提取关键数据，生成完整 SEO 标签                      │
│  └── 输出: output/seo_report_YYYYMMDD_period.html               │
├─────────────────────────────────────────────────────────────────┤
│  Step 4: 发布到 GitHub Pages                                     │
│  ├── 脚本: github_publisher.py                                  │
│  ├── 功能: 上传报告，更新 index.html                            │
│  └── 输出: reports/report-YYYY-MM-DD-period.html                │
├─────────────────────────────────────────────────────────────────┤
│  Step 5: 更新 sitemap.xml                                        │
│  ├── 脚本: github_publisher.py (_update_sitemap)                │
│  └── 功能: 自动添加新报告 URL                                   │
└─────────────────────────────────────────────────────────────────┘
```

### 1.2 自动化工作流

**主脚本**: `scripts/auto_publish_github_workflow.py`

```python
# 执行命令
python scripts/auto_publish_github_workflow.py

# 完整流程
1. 生成报告 → 2. 转HTML → 3. 加SEO标签 → 4. 发布 → 5. 更新sitemap
```

---

## 2. SEO 标签详解

### 2.1 基础 SEO 标签

每个报告 HTML 文件包含以下基础 SEO 标签：

```html
<head>
    <!-- 字符编码和视口 -->
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    
    <!-- 缓存控制 -->
    <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
    <meta http-equiv="Pragma" content="no-cache">
    <meta http-equiv="Expires" content="0">
    
    <!-- 页面标题（包含关键词） -->
    <title>Crypto Risk Radar – 2026-04-13 | On-Chain Quant Signals</title>
    
    <!-- 页面描述（搜索引擎显示） -->
    <meta name="description" content="Quant score +0.15/2.0 (Neutral). 7d exchange netflow +11,570 BTC, whale holdings +3.5%. Scam alert: high. Fear & Greed: 16.">
    
    <!-- 关键词 -->
    <meta name="keywords" content="crypto risk radar, on-chain analysis, bitcoin quant signals, exchange netflow, whale holdings, scam detection, fear and greed index">
    
    <!-- 作者 -->
    <meta name="author" content="Crypto Risk Radar">
    
    <!-- 爬虫指令 -->
    <meta name="robots" content="index, follow">
    
    <!-- 规范 URL（防止重复内容） -->
    <link rel="canonical" href="https://peteryang546.github.io/crypto-risk-radar/reports/report-2026-04-13-morning.html">
</head>
```

### 2.2 Open Graph 标签（社交媒体）

用于 Facebook、LinkedIn 等社交媒体分享时显示预览：

```html
<!-- Open Graph -->
<meta property="og:title" content="Crypto Risk Radar – 2026-04-13">
<meta property="og:description" content="Quant +0.15 | Netflow +11,570 BTC | Fear 16">
<meta property="og:type" content="article">
<meta property="og:url" content="https://peteryang546.github.io/crypto-risk-radar/reports/report-2026-04-13-morning.html">
<meta property="og:image" content="https://peteryang546.github.io/crypto-risk-radar/og-preview.png">
<meta property="og:site_name" content="Crypto Risk Radar">
<meta property="og:locale" content="en_US">
```

**预览图**: `og-preview.png` (1200x630 像素)

### 2.3 Twitter Card 标签

用于 Twitter 分享时显示预览：

```html
<!-- Twitter Card -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Crypto Risk Radar – 2026-04-13">
<meta name="twitter:description" content="Quant +0.15 | Netflow +11,570 BTC">
<meta name="twitter:image" content="https://peteryang546.github.io/crypto-risk-radar/og-preview.png">
```

### 2.4 JSON-LD 结构化数据（GEO 核心）

**最重要**的部分，让 AI 系统（ChatGPT、Claude、Perplexity 等）能直接理解和引用内容。

我们使用 **双 Schema 策略**，同时提供 `TechArticle` 和 `Report` 两种类型，最大化 AI 理解度：

#### 2.4.1 TechArticle Schema（主要）

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "TechArticle",
  "headline": "Crypto Risk Radar – 2026-04-13 | On-Chain Quant Signals",
  "description": "Quant score +0.15/2.0 (Neutral). 7d exchange netflow +11,570 BTC...",
  "datePublished": "2026-04-13T08:10:00+00:00",
  "dateModified": "2026-04-13T08:10:00+00:00",
  "author": {
    "@type": "Organization",
    "name": "Crypto Risk Radar",
    "url": "https://peteryang546.github.io/crypto-risk-radar/",
    "logo": {
      "@type": "ImageObject",
      "url": "https://peteryang546.github.io/crypto-risk-radar/og-preview.png"
    }
  },
  "publisher": {
    "@type": "Organization",
    "name": "Crypto Risk Radar",
    "url": "https://peteryang546.github.io/crypto-risk-radar/",
    "logo": {
      "@type": "ImageObject",
      "url": "https://peteryang546.github.io/crypto-risk-radar/og-preview.png",
      "width": 1200,
      "height": 630
    }
  },
  "mainEntityOfPage": {
    "@type": "WebPage",
    "@id": "https://peteryang546.github.io/crypto-risk-radar/reports/report-2026-04-13-morning.html"
  },
  "image": {
    "@type": "ImageObject",
    "url": "https://peteryang546.github.io/crypto-risk-radar/og-preview.png",
    "width": 1200,
    "height": 630
  },
  "keywords": "Bitcoin, Ethereum, on-chain analysis, quant signals, scam detection, crypto risk, blockchain analytics",
  "articleSection": "Cryptocurrency Risk Analysis",
  "about": {
    "@type": "Thing",
    "name": "Cryptocurrency Market Risk Assessment",
    "description": "Quantitative analysis of Bitcoin and Ethereum on-chain metrics including exchange flows, whale movements, and scam detection"
  },
  "proficiencyLevel": "Expert",
  "dependencies": "On-chain data from Glassnode, DeFi Llama, and CoinGecko APIs",
  "isAccessibleForFree": true,
  "license": "https://creativecommons.org/licenses/by-nc/4.0/",
  "inLanguage": "en-US",
  "audience": {
    "@type": "Audience",
    "audienceType": "Cryptocurrency investors, traders, and analysts"
  }
}
</script>
```

**增强的权威性标记**:
- `proficiencyLevel`: "Expert" - 标识专业水平
- `dependencies`: 说明数据来源，增强可信度
- `isAccessibleForFree`: true - 免费访问
- `license`: 知识共享许可
- `audience`: 明确定义目标受众
- `publisher.logo`: 完整的组织信息

#### 2.4.2 Report Schema（补充）

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Report",
  "name": "Crypto Risk Radar – 2026-04-13",
  "description": "Quant score +0.15/2.0 (Neutral). 7d exchange netflow +11,570 BTC...",
  "url": "https://peteryang546.github.io/crypto-risk-radar/reports/report-2026-04-13-morning.html",
  "datePublished": "2026-04-13T08:10:00+00:00",
  "author": {
    "@type": "Organization",
    "name": "Crypto Risk Radar"
  },
  "publisher": {
    "@type": "Organization",
    "name": "Crypto Risk Radar",
    "url": "https://peteryang546.github.io/crypto-risk-radar/"
  },
  "about": {
    "@type": "Thing",
    "name": "Bitcoin and Ethereum Market Analysis"
  },
  "temporalCoverage": "P12H",
  "spatialCoverage": "Global Cryptocurrency Markets",
  "variableMeasured": [
    "Exchange Netflow",
    "Whale Holdings",
    "Fear and Greed Index",
    "Scam Detection Score"
  ]
}
</script>
```

**为什么使用双 Schema**:
- `TechArticle`: 强调技术专业性，适合技术类 AI 查询
- `Report`: 强调报告属性，适合数据类 AI 查询
- 覆盖更多 AI 系统的理解模式
- 增强内容权威性和可信度

**为什么重要**:
- AI 系统在回答问题时优先抓取结构化数据
- 包含关键指标（量化得分、净流入、恐惧指数）
- 明确标识文章类型和主题
- **权威性标记**帮助 AI 判断内容可信度

---

## 3. 数据提取逻辑

### 3.1 自动提取关键数据

`seo_geo_publisher.py` 自动从报告内容中提取：

| 数据项 | 提取规则 | 示例 |
|--------|----------|------|
| 日期 | `Data as of: Month DD, YYYY` | 2026-04-13 |
| 量化得分 | `Final Score: +X.XX` | +0.15 |
| 等级 | `Grade: [XXX]` | Neutral |
| 净流入 | `On-chain netflow: +X,XXX BTC` | +11,570 |
| 巨鲸持仓 | `Whale holdings: +X.X%` | +3.5 |
| 恐惧指数 | `Fear & Greed: XX` | 16 |
| 骗局信息 | `Confirmed Honeypots` 表格第一行 | high |

### 3.2 生成描述文本

基于提取的数据，自动生成 SEO 描述：

```python
description = f"Quant score {score}/2.0 ({grade}). " \
              f"7d exchange netflow {netflow} BTC, " \
              f"whale holdings {whale}%. " \
              f"Scam alert: {scam}. " \
              f"Fear & Greed: {fear}."
```

**输出示例**:
> Quant score +0.15/2.0 (Neutral). 7d exchange netflow +11,570 BTC, whale holdings +3.5%. Scam alert: high. Fear & Greed: 16.

---

## 4. Sitemap 管理

### 4.1 sitemap.xml 结构

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <!-- 主页 -->
  <url>
    <loc>https://peteryang546.github.io/crypto-risk-radar/</loc>
    <lastmod>2026-04-13</lastmod>
    <changefreq>daily</changefreq>
    <priority>1.0</priority>
  </url>
  
  <!-- 最新报告（每次发布插入到最前面） -->
  <url>
    <loc>https://peteryang546.github.io/crypto-risk-radar/reports/report-2026-04-13-morning.html</loc>
    <lastmod>2026-04-13</lastmod>
    <changefreq>never</changefreq>
    <priority>0.8</priority>
  </url>
  
  <!-- 历史报告（保留所有） -->
  <url>
    <loc>https://peteryang546.github.io/crypto-risk-radar/reports/report-2026-04-12-evening.html</loc>
    <lastmod>2026-04-12</lastmod>
    <changefreq>never</changefreq>
    <priority>0.8</priority>
  </url>
  <!-- ... 更多历史报告 -->
</urlset>
```

### 4.2 自动更新逻辑

```python
def _update_sitemap(self, date_str, file_name):
    """更新 sitemap.xml"""
    # 1. 获取现有 sitemap
    # 2. 创建新的 <url> 元素
    # 3. 插入到最前面
    # 4. 保留所有历史 URL
    # 5. 上传更新后的文件
```

---

## 5. Google Search Console 配置

### 5.1 验证步骤

1. **访问**: https://search.google.com/search-console
2. **添加资源**: `https://peteryang546.github.io/crypto-risk-radar/`
3. **选择验证方式**: HTML 文件
4. **下载验证文件**: `google88d3d6e1e5c9c00c.html`
5. **上传到仓库根目录**
6. **点击验证**

### 5.2 提交 Sitemap

验证成功后：
1. 左侧菜单点击 "Sitemaps"
2. 输入: `sitemap.xml`
3. 点击 "提交"

### 5.3 监控指标

- **收录状态**: 哪些页面被 Google 收录
- **搜索查询**: 用户通过哪些关键词找到网站
- **点击率**: 搜索结果中的点击比例
- **排名**: 关键词在搜索结果中的位置

---

## 6. 文件清单

### 6.1 SEO/GEO 相关脚本

| 文件 | 功能 |
|------|------|
| `seo_geo_publisher.py` | 生成 SEO/GEO 标签 |
| `generate_og_image.py` | 生成社交媒体预览图 |
| `github_publisher.py` | 发布并更新 sitemap |
| `auto_publish_github_workflow.py` | 完整自动化流程 |

### 6.2 生成的文件

| 文件 | 位置 | 说明 |
|------|------|------|
| `og-preview.png` | 仓库根目录 | 社交媒体预览图 |
| `sitemap.xml` | 仓库根目录 | 站点地图 |
| `google88d3d6e1e5c9c00c.html` | 仓库根目录 | GSC 验证文件 |
| `report-YYYY-MM-DD-period.html` | `reports/` | 报告文件 |
| `index.html` | 仓库根目录 | 主页（嵌入最新报告） |

---

## 7. 样式规范

### 7.1 颜色方案

```css
/* 背景 */
body { background-color: #0a0e27; }  /* 深蓝 */
.report-content { background-color: #1a1f3a; }  /* 稍浅的深蓝 */

/* 文字 */
body { color: #ffffff; }  /* 白色 */
h1, h2, h3 { color: #00d4ff; }  /* 青色标题 */
strong { color: #00d4ff; }  /* 青色强调 */

/* 表格 */
table { background-color: #0a0e27; color: #ffffff; }
th { background-color: #1a1f3a; color: #00d4ff; }
td { color: #ffffff !important; }
```

### 7.2 布局结构

```
┌─────────────────────────────────────┐
│  <head>                             │
│  ├── SEO 标签                        │
│  ├── Open Graph                      │
│  ├── Twitter Card                    │
│  ├── JSON-LD                         │
│  └── CSS 样式                        │
├─────────────────────────────────────┤
│  <body>                             │
│  ├── 报告内容                        │
│  │   ├── 标题                        │
│  │   ├── 8个模块                     │
│  │   └── 表格                        │
│  ├── Report History                 │
│  └── Footer                         │
└─────────────────────────────────────┘
```

---

## 8. 验证清单

### 8.1 发布前检查

- [ ] 报告内容完整（8个模块）
- [ ] 表格样式正确（白色文字，深蓝背景）
- [ ] SEO 标签已生成
- [ ] JSON-LD 结构化数据正确
- [ ] sitemap.xml 已更新

### 8.2 发布后检查

- [ ] 报告可正常访问
- [ ] index.html 显示最新报告
- [ ] sitemap.xml 包含新 URL
- [ ] 无 404 错误

### 8.3 SEO 效果检查

- [ ] Google Search Console 验证通过
- [ ] sitemap.xml 已提交
- [ ] 页面被 Google 收录（等待 1-7 天）
- [ ] 搜索关键词带来流量

---

## 9. 故障排除

### 9.1 验证文件问题

**问题**: Google 验证失败  
**解决**:
1. 确认文件名与 Google 提供的一致
2. 确认文件内容只有一行：`google-site-verification: <filename>`
3. 确认文件上传到仓库根目录
4. 等待 GitHub Pages 部署（1-5 分钟）

### 9.2 样式问题

**问题**: 表格文字看不见  
**解决**:
1. 检查是否移除了所有内联样式
2. 确认 CSS 中 `td { color: #ffffff !important; }`
3. 确认 `background-color: transparent !important`

### 9.3 sitemap 问题

**问题**: sitemap.xml 未更新  
**解决**:
1. 检查 GitHub API Token 权限
2. 检查仓库是否有写入权限
3. 手动检查 sitemap.xml 内容

---

## 10. 更新记录

| 日期 | 版本 | 变更 |
|------|------|------|
| 2026-04-12 | v6.0 | 初始版本（Hashnode） |
| 2026-04-12 | v6.0-GitHub | 迁移到 GitHub Pages |
| 2026-04-13 | v6.1 | 添加完整 SEO/GEO 支持 |
| 2026-04-13 | v6.1 | 添加 sitemap 自动更新 |
| 2026-04-13 | v6.1 | 添加 GSC 验证 |
| 2026-04-13 | v6.1.1 | 增强 JSON-LD 结构化数据 |
| 2026-04-13 | v6.1.1 | 添加双 Schema 策略（TechArticle + Report） |
| 2026-04-13 | v6.1.1 | 添加权威性标记（proficiencyLevel, license等） |

---

## 附录

### A. 参考链接

- [GitHub Pages 文档](https://docs.github.com/en/pages)
- [Google Search Console](https://search.google.com/search-console)
- [Schema.org TechArticle](https://schema.org/TechArticle)
- [Open Graph 协议](https://ogp.me/)

### B. 相关文件

- `CHANGELOG_2026-04-12.md` - 变更日志
- `memory/2026-04-13.md` - 工作日志
- `D:/战略对话/区块链分析师SEO & geo优化内容.txt` - 原始方案

---

**最后更新**: 2026-04-13 09:24 CST  
**状态**: ✅ 生产就绪
