#!/usr/bin/env python3
"""
GitHub Pages 发布器
使用 GitHub API 直接发布报告到仓库
"""

import os
import sys
import json
import base64
import requests
from datetime import datetime
from pathlib import Path
from urllib.parse import quote

# GitHub 配置 - 从环境变量读取
GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN', '')
GITHUB_REPO = os.environ.get('GITHUB_REPO', 'peteryang546/crypto-risk-radar')
GITHUB_BRANCH = os.environ.get('GITHUB_BRANCH', 'main')
GITHUB_API_BASE = f"https://api.github.com/repos/{GITHUB_REPO}"

# 路径配置
BASE_DIR = Path(__file__).parent.parent
OUTPUT_DIR = BASE_DIR / "output"

class GitHubPublisher:
    """GitHub Pages 发布器"""
    
    def __init__(self):
        self.headers = {
            "Authorization": f"token {GITHUB_TOKEN}",
            "Accept": "application/vnd.github.v3+json",
            "Content-Type": "application/json"
        }
    
    def _api_request(self, method, endpoint, data=None):
        """发送 GitHub API 请求"""
        url = f"{GITHUB_API_BASE}/{endpoint}"
        try:
            if method == "GET":
                response = requests.get(url, headers=self.headers, timeout=30)
            elif method == "PUT":
                response = requests.put(url, headers=self.headers, json=data, timeout=30)
            elif method == "DELETE":
                response = requests.delete(url, headers=self.headers, timeout=30)
            else:
                return False, f"Unsupported method: {method}"
            
            if response.status_code in [200, 201, 204]:
                return True, response.json() if response.text else {}
            else:
                return False, f"HTTP {response.status_code}: {response.text}"
        except Exception as e:
            return False, str(e)
    
    def get_file_sha(self, path):
        """获取文件 SHA（如果文件存在）"""
        success, result = self._api_request("GET", f"contents/{quote(path, safe='')}?ref={GITHUB_BRANCH}")
        if success and isinstance(result, dict):
            return result.get("sha")
        return None
    
    def upload_file(self, path, content, message=None):
        """上传/更新文件到 GitHub"""
        # 获取现有文件 SHA（如果存在）
        sha = self.get_file_sha(path)
        
        # 准备数据
        data = {
            "message": message or f"Update {path} - {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            "content": base64.b64encode(content.encode('utf-8')).decode('utf-8'),
            "branch": GITHUB_BRANCH
        }
        
        if sha:
            data["sha"] = sha
        
        # 发送请求
        success, result = self._api_request("PUT", f"contents/{quote(path, safe='')}", data)
        
        if success:
            if isinstance(result, dict) and "content" in result:
                return True, result["content"].get("html_url", "")
            return True, ""
        else:
            return False, result
    
    def delete_file(self, path, message=None):
        """删除 GitHub 上的文件"""
        sha = self.get_file_sha(path)
        if not sha:
            return True, "File does not exist"
        
        data = {
            "message": message or f"Delete {path}",
            "sha": sha,
            "branch": GITHUB_BRANCH
        }
        
        success, result = self._api_request("DELETE", f"contents/{quote(path, safe='')}", data)
        return success, result
    
    def publish_report(self, html_file, title=None):
        """发布报告到 GitHub Pages"""
        # 读取 HTML 文件
        with open(html_file, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # 生成文件名
        now = datetime.now()
        date_str = now.strftime('%Y-%m-%d')
        time_str = now.strftime('%H%M')
        
        # 确定是早间还是晚间报告
        period = "evening" if now.hour >= 12 else "morning"
        
        # 文件路径
        file_name = f"report-{date_str}-{period}.html"
        file_path = f"reports/{file_name}"
        
        # 上传报告
        print(f"Uploading report to {file_path}...")
        success, url = self.upload_file(
            file_path,
            html_content,
            message=f"Publish {period} report - {date_str}"
        )
        
        if not success:
            return False, f"Failed to upload report: {url}"
        
        # 同时更新 index.html（最新报告）
        print("Updating index.html...")
        index_content = self._generate_index_html(html_content, title, date_str, period, file_name)
        success, index_url = self.upload_file(
            "index.html",
            index_content,
            message=f"Update index with {period} report - {date_str}"
        )
        
        if not success:
            print(f"Warning: Failed to update index.html: {index_url}")
        
        # 更新 sitemap.xml
        print("Updating sitemap.xml...")
        sitemap_success = self._update_sitemap(date_str, file_name)
        if not sitemap_success:
            print("Warning: Failed to update sitemap.xml")
        
        # 返回访问 URL
        site_url = f"https://peteryang546.github.io/crypto-risk-radar/"
        report_url = f"{site_url}reports/{file_name}"
        
        return True, {
            "site_url": site_url,
            "report_url": report_url,
            "file_path": file_path
        }
    
    def _update_sitemap(self, date_str, file_name):
        """更新 sitemap.xml"""
        try:
            site_url = "https://peteryang546.github.io/crypto-risk-radar"
            report_url = f"{site_url}/reports/{file_name}"
            
            # 尝试获取现有的 sitemap.xml
            success, existing_content = self._get_file_content("sitemap.xml")
            
            if success and existing_content:
                # 解析现有内容
                import xml.etree.ElementTree as ET
                import re
                
                # 移除 XML 声明，解析内容
                content_without_decl = re.sub(r'<\?xml[^?]*\?>', '', existing_content)
                root = ET.fromstring(content_without_decl)
                
                # 创建新的 url 元素
                new_url = ET.Element("url")
                loc = ET.SubElement(new_url, "loc")
                loc.text = report_url
                lastmod = ET.SubElement(new_url, "lastmod")
                lastmod.text = date_str
                changefreq = ET.SubElement(new_url, "changefreq")
                changefreq.text = "never"
                priority = ET.SubElement(new_url, "priority")
                priority.text = "0.8"
                
                # 插入到最前面
                root.insert(0, new_url)
                
                # 转换回字符串
                new_content = ET.tostring(root, encoding='unicode')
                new_content = '<?xml version="1.0" encoding="UTF-8"?>\n' + new_content
                
            else:
                # 创建新的 sitemap
                new_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>{site_url}/</loc>
    <lastmod>{date_str}</lastmod>
    <changefreq>daily</changefreq>
    <priority>1.0</priority>
  </url>
  <url>
    <loc>{report_url}</loc>
    <lastmod>{date_str}</lastmod>
    <changefreq>never</changefreq>
    <priority>0.8</priority>
  </url>
</urlset>"""
            
            # 上传 sitemap.xml
            success, result = self.upload_file(
                "sitemap.xml",
                new_content,
                message=f"Update sitemap with {file_name} - {date_str}"
            )
            
            if success:
                print("[SUCCESS] sitemap.xml updated")
                return True
            else:
                print(f"[ERROR] Failed to update sitemap: {result}")
                return False
                
        except Exception as e:
            print(f"[ERROR] sitemap update failed: {e}")
            return False
    
    def _get_file_content(self, path):
        """获取文件内容"""
        try:
            success, result = self._api_request("GET", f"contents/{quote(path, safe='')}?ref={GITHUB_BRANCH}")
            if success and isinstance(result, dict) and 'content' in result:
                import base64
                content = base64.b64decode(result['content']).decode('utf-8')
                return True, content
            return False, None
        except Exception as e:
            return False, str(e)
    
    def _generate_index_html(self, report_content, title, date_str, period, file_name):
        """生成 index.html，直接嵌入报告内容"""
        # 提取报告标题
        if not title:
            title = f"Crypto Risk Radar - {date_str} {'Evening' if period == 'evening' else 'Morning'} Report"
        
        # 清理报告内容中的 HTML 和 body 标签，只保留内容
        cleaned_content = report_content
        # 移除 doctype, html, head, body 标签
        import re
        cleaned_content = re.sub(r'<!DOCTYPE[^>]*>', '', cleaned_content, flags=re.IGNORECASE)
        cleaned_content = re.sub(r'<html[^>]*>', '', cleaned_content, flags=re.IGNORECASE)
        cleaned_content = re.sub(r'</html>', '', cleaned_content, flags=re.IGNORECASE)
        cleaned_content = re.sub(r'<head>.*?</head>', '', cleaned_content, flags=re.IGNORECASE | re.DOTALL)
        cleaned_content = re.sub(r'<body[^>]*>', '', cleaned_content, flags=re.IGNORECASE)
        cleaned_content = re.sub(r'</body>', '', cleaned_content, flags=re.IGNORECASE)
        
        # 构建历史报告链接
        period_label = "Evening" if period == "evening" else "Morning"
        history_section = f"""
    <div class="history-section" style="max-width: 1200px; margin: 30px auto; background-color: #1a1f3a; border-radius: 12px; padding: 30px; border: 1px solid #2a3f5f;">
        <h2 style="color: #00d4ff; margin-bottom: 20px; font-size: 1.5em;">📊 Report History</h2>
        <ul style="list-style: none; padding: 0;">
            <li style="padding: 10px 0; border-bottom: 1px solid #2a3f5f;">
                <a href="reports/{file_name}" style="color: #ffffff; text-decoration: none; font-size: 1.1em;">
                    {date_str} - {period_label} Report
                </a>
                <span style="color: #8b9dc3; margin-left: 10px;">(Latest)</span>
            </li>
        </ul>
        <p style="color: #8b9dc3; margin-top: 15px; font-size: 0.9em;">
            View all reports in the <a href="https://github.com/peteryang546/crypto-risk-radar/tree/main/reports" style="color: #00d4ff;">reports folder</a>
        </p>
    </div>
"""
        
        # 构建完整的 index.html - 直接嵌入报告内容
        index_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
    <meta http-equiv="Pragma" content="no-cache">
    <meta http-equiv="Expires" content="0">
    <title>{title}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background-color: #0a0e27;
            color: #ffffff;
            line-height: 1.6;
            padding: 20px;
        }}
        .report-content {{
            max-width: 1200px;
            margin: 0 auto;
            background-color: #1a1f3a;
            border-radius: 12px;
            padding: 30px;
            border: 1px solid #2a3f5f;
        }}
        .report-content h1, .report-content h2, .report-content h3 {{
            color: #00d4ff;
            margin: 20px 0 15px 0;
        }}
        .report-content p {{
            color: #ffffff;
            margin-bottom: 15px;
        }}
        .report-content table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            background-color: #0a0e27;
        }}
        .report-content th, .report-content td {{
            padding: 12px;
            text-align: left;
            border: 1px solid #2a3f5f;
            color: #ffffff;
        }}
        .report-content th {{
            background-color: #1a1f3a;
            color: #00d4ff;
            font-weight: 600;
        }}
        .report-content tr:nth-child(even) {{
            background-color: #0f1429;
        }}
        .report-content tr:hover {{
            background-color: #1a2a4a;
        }}
        .history-section {{
            max-width: 1200px;
            margin: 30px auto;
            background-color: #1a1f3a;
            border-radius: 12px;
            padding: 30px;
            border: 1px solid #2a3f5f;
        }}
        .history-section h2 {{
            color: #00d4ff;
            margin-bottom: 20px;
            font-size: 1.5em;
        }}
        .history-section ul {{
            list-style: none;
            padding: 0;
        }}
        .history-section li {{
            padding: 10px 0;
            border-bottom: 1px solid #2a3f5f;
        }}
        .history-section li:last-child {{
            border-bottom: none;
        }}
        .history-section a {{
            color: #ffffff;
            text-decoration: none;
            font-size: 1.1em;
        }}
        .history-section a:hover {{
            color: #00d4ff;
        }}
        .footer {{
            text-align: center;
            padding: 40px 20px;
            color: #ffffff;
            margin-top: 40px;
            font-size: 0.9em;
        }}
        .footer a {{
            color: #00d4ff;
            text-decoration: none;
        }}
    </style>
</head>
<body>
    <div class="report-content">
        {cleaned_content}
    </div>
    
    {history_section}
    
    <div class="footer">
        <p>Generated by StepClaw AI Agent | Updated every 12 hours</p>
        <p>Data sources: Binance, CoinGecko, DeFi Llama, DEX Screener</p>
        <p><a href="https://github.com/peteryang546/crypto-risk-radar">View on GitHub</a></p>
    </div>
</body>
</html>"""
        
        return index_html

def main():
    """命令行入口"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Publish report to GitHub Pages")
    parser.add_argument("--file", required=True, help="HTML file to publish")
    parser.add_argument("--title", help="Report title")
    
    args = parser.parse_args()
    
    publisher = GitHubPublisher()
    success, result = publisher.publish_report(args.file, args.title)
    
    if success:
        print(f"\n[SUCCESS] Published successfully!")
        print(f"Site URL: {result['site_url']}")
        print(f"Report URL: {result['report_url']}")
    else:
        print(f"\n[ERROR] Publishing failed: {result}")
        sys.exit(1)

if __name__ == "__main__":
    main()
