# GitHub Actions 工作流手动配置指南

由于 API 权限限制，无法自动上传工作流文件。请按照以下步骤手动创建：

## 步骤 1: 创建目录

1. 打开浏览器，访问: https://github.com/peteryang546/crypto-risk-radar
2. 点击 "Add file" → "Create new file"
3. 在文件名输入框中输入: `.github/workflows/generate-report.yml`
4. GitHub 会自动创建目录结构

## 步骤 2: 复制以下内容

将下面的完整内容复制到文件编辑框中：

```yaml
name: Generate Crypto Risk Radar Report

on:
  schedule:
    # Run at 00:00 and 12:00 UTC (08:00 and 20:00 Beijing Time)
    - cron: '0 0,12 * * *'
  workflow_dispatch:  # Allow manual trigger

jobs:
  build:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout repository
      uses: actions/checkout@v4
      
    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.11'
        
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install requests matplotlib pandas certifi urllib3
        
    - name: Run report generation script
      env:
        COINGECKO_API_KEY: ${{ secrets.COINGECKO_API_KEY }}
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
      run: |
        python scripts/generate_full_integrated_report.py --live
        
    - name: Copy latest report to index.html
      run: |
        latest_report=$(ls -t output/full_report_*.html | head -1)
        if [ -n "$latest_report" ]; then
          cp "$latest_report" output/index.html
          echo "Copied $latest_report to output/index.html"
        fi
        
    - name: Deploy to GitHub Pages
      uses: peaceiris/actions-gh-pages@v3
      with:
        github_token: ${{ secrets.GITHUB_TOKEN }}
        publish_dir: ./output
        publish_branch: gh-pages
        
    - name: Upload artifacts
      uses: actions/upload-artifact@v4
      with:
        name: reports
        path: output/
        retention-days: 30
```

## 步骤 3: 提交文件

1. 在 "Commit new file" 部分，输入提交信息：
   - 标题: `Add GitHub Actions workflow for automated report generation`
   - 描述: `Automated daily report generation at 08:00 and 20:00 Beijing Time`

2. 选择 "Commit directly to the main branch"

3. 点击 "Commit new file"

## 步骤 4: 配置 Secrets

1. 在仓库页面，点击 "Settings" 标签
2. 左侧菜单点击 "Secrets and variables" → "Actions"
3. 点击 "New repository secret"
4. 添加以下 secrets:

### Secret 1: COINGECKO_API_KEY
- Name: `COINGECKO_API_KEY`
- Value: `CG-m57LMPhhuqyQs2QLzUJ6ozAK`

### Secret 2: GITHUB_TOKEN (通常已存在)
- 这个通常由 GitHub 自动提供，不需要手动添加

## 步骤 5: 启用 GitHub Pages

1. 在仓库页面，点击 "Settings"
2. 左侧菜单点击 "Pages"
3. Source 选择 "Deploy from a branch"
4. Branch 选择 "gh-pages" (如果还没有，先运行一次 Action)
5. 点击 "Save"

## 步骤 6: 手动触发测试

1. 点击仓库顶部的 "Actions" 标签
2. 点击 "Generate Crypto Risk Radar Report"
3. 点击 "Run workflow" → "Run workflow"
4. 等待 2-3 分钟，查看运行结果

## 步骤 7: 验证结果

1. 如果 Actions 运行成功（绿色对勾）
2. 访问: https://peteryang546.github.io/crypto-risk-radar/
3. 查看生成的报告

## 已上传的文件

以下文件已成功上传到仓库：
- ✅ `scripts/generate_full_integrated_report.py`
- ✅ `scripts/seo_geo_publisher.py`
- ✅ `modules/high_risk_watchlist.py`
- ✅ `modules/token_unlock_alert.py`
- ✅ `modules/contract_scanner.py`
- ✅ `modules/chart_generator.py`
- ✅ `modules/__init__.py`
- ✅ `GITHUB_ACTIONS_SETUP.md`

## 需要手动上传的文件

- ⏳ `.github/workflows/generate-report.yml` (按照上述步骤创建)

## 注意事项

1. 定时任务使用 UTC 时间，对应北京时间：
   - 00:00 UTC = 08:00 北京时间
   - 12:00 UTC = 20:00 北京时间

2. 首次运行可能需要 2-3 分钟安装依赖

3. 如果运行失败，查看 Actions 日志获取详细错误信息

## 完成后的效果

- 每天自动生成两次报告
- 报告自动发布到 GitHub Pages
- 可以通过网站直接访问最新报告
- 所有历史报告保留在 artifacts 中
