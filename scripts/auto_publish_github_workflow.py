#!/usr/bin/env python3
"""
区块链风险雷达 - GitHub Pages 自动化发布流程 v6.0
生成HTML报告 → 清理 → 发布到GitHub Pages
12小时统计周期，8个模块
"""

import os
import sys
import json
import subprocess
from datetime import datetime
from pathlib import Path

# 添加lib路径
sys.path.insert(0, r'F:\stepclaw\workspace\lib')

# 路径配置
BASE_DIR = Path(__file__).parent.parent
OUTPUT_DIR = BASE_DIR / "output"
LOGS_DIR = BASE_DIR / "logs"

# 确保目录存在
for dir_path in [OUTPUT_DIR, LOGS_DIR]:
    dir_path.mkdir(parents=True, exist_ok=True)

class AutoPublishWorkflow:
    """自动化发布工作流"""
    
    def __init__(self):
        self.log_file = LOGS_DIR / f"publish_log_{datetime.now().strftime('%Y%m%d')}.json"
        self.logs = self._load_logs()
    
    def _load_logs(self):
        """加载历史日志"""
        if self.log_file.exists():
            try:
                with open(self.log_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def _save_log(self, entry):
        """保存日志条目"""
        self.logs.append(entry)
        with open(self.log_file, 'w', encoding='utf-8') as f:
            json.dump(self.logs, f, indent=2)
    
    def run_command(self, cmd, cwd=None):
        """运行命令"""
        try:
            # 使用完整的Python路径
            python_path = r'C:\Users\Administrator\AppData\Local\Programs\Python\Python311\python.exe'
            if cmd.startswith('python '):
                cmd = cmd.replace('python ', f'"{python_path}" ')
            
            result = subprocess.run(
                cmd,
                shell=True,
                cwd=cwd or BASE_DIR,
                capture_output=True,
                text=True,
                encoding='utf-8'
            )
            return result.returncode == 0, result.stdout, result.stderr
        except Exception as e:
            return False, "", str(e)
    
    def step_1_generate_report(self):
        """步骤1: 生成HTML报告"""
        print("\n" + "="*70)
        print("STEP 1: Generating HTML Report (v6.0)")
        print("="*70)
        
        success, stdout, stderr = self.run_command(
            "python scripts\\generate_v60_html_report.py"
        )
        
        if success:
            print("[SUCCESS] Report generated")
            # 提取生成的文件名
            for line in stdout.split('\n'):
                if 'Report saved:' in line:
                    report_file = line.split('Report saved:')[1].strip()
                    return True, report_file
            return True, None
        else:
            print(f"[ERROR] Report generation failed: {stderr}")
            return False, None
    
    def step_2_convert_to_html(self, report_file):
        """步骤2: Markdown转HTML"""
        print("\n" + "="*70)
        print("STEP 2: Converting Markdown to HTML")
        print("="*70)
        
        success, stdout, stderr = self.run_command(
            f"python scripts\\md_to_html_converter.py \"{report_file}\""
        )
        
        if success:
            print("[SUCCESS] Report converted to HTML")
            # 提取生成的文件名
            for line in stdout.split('\n'):
                if 'Converted to HTML:' in line:
                    html_file = line.split('Converted to HTML:')[1].strip()
                    return True, html_file
            # 默认路径
            report_path = Path(report_file)
            html_file = str(report_path.parent / f"{report_path.stem}.html")
            return True, html_file
        else:
            print(f"[ERROR] HTML conversion failed: {stderr}")
            return False, None
    
    def step_3_add_seo_geo(self, html_file):
        """步骤3: 添加SEO/GEO标签"""
        print("\n" + "="*70)
        print("STEP 3: Adding SEO/GEO Tags")
        print("="*70)
        
        # 生成SEO增强版HTML
        seo_file = str(Path(html_file).parent / f"seo_{Path(html_file).name}")
        
        success, stdout, stderr = self.run_command(
            f"python scripts\\seo_geo_publisher.py --input \"{html_file}\" --output \"{seo_file}\""
        )
        
        if success:
            print("[SUCCESS] SEO/GEO tags added")
            return True, seo_file
        else:
            print(f"[WARNING] SEO/GEO processing failed: {stderr}")
            # 如果失败，使用原始HTML文件
            return True, html_file
    
    def step_4_publish_to_github(self, seo_file):
        """步骤4: 发布到GitHub Pages"""
        print("\n" + "="*70)
        print("STEP 4: Publishing to GitHub Pages")
        print("="*70)
        
        # 生成标题
        now = datetime.now()
        et_time = now.strftime('%B %d, %Y')
        period = "Evening" if now.hour >= 12 else "Morning"
        title = f"Crypto Risk Radar - 12H {period} Report | {et_time}"
        
        success, stdout, stderr = self.run_command(
            f"python scripts\\github_publisher.py --file \"{seo_file}\" --title \"{title}\""
        )
        
        if success:
            print("[SUCCESS] Published to GitHub Pages")
            # 提取发布URL
            site_url = None
            report_url = None
            for line in stdout.split('\n'):
                if 'Site URL:' in line:
                    site_url = line.split('Site URL:')[1].strip()
                if 'Report URL:' in line:
                    report_url = line.split('Report URL:')[1].strip()
            return True, {"site_url": site_url, "report_url": report_url}
        else:
            print(f"[ERROR] Publishing failed: {stderr}")
            print(f"Stdout: {stdout}")
            return False, None
    
    def run_full_workflow(self):
        """运行完整工作流"""
        print("="*70)
        print("CRYPTO RISK RADAR - GitHub Pages Auto Publish Workflow v6.1 (SEO/GEO)")
        print("="*70)
        print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        entry = {
            "timestamp": datetime.now().isoformat(),
            "status": "running",
            "platform": "github_pages"
        }
        
        # Step 1: 生成报告
        success, report_file = self.step_1_generate_report()
        if not success:
            entry["status"] = "failed"
            entry["step"] = "generate"
            self._save_log(entry)
            return False
        entry["report_file"] = report_file
        
        # Step 2: Markdown转HTML
        success, html_file = self.step_2_convert_to_html(report_file)
        if not success:
            entry["status"] = "failed"
            entry["step"] = "convert"
            self._save_log(entry)
            return False
        entry["html_file"] = html_file
        
        # Step 3: 添加SEO/GEO标签
        success, seo_file = self.step_3_add_seo_geo(html_file)
        if not success:
            entry["status"] = "failed"
            entry["step"] = "seo_geo"
            self._save_log(entry)
            return False
        entry["seo_file"] = seo_file
        
        # Step 4: 发布
        success, urls = self.step_4_publish_to_github(seo_file)
        if not success:
            entry["status"] = "failed"
            entry["step"] = "publish"
            self._save_log(entry)
            return False
        
        entry["status"] = "success"
        entry["urls"] = urls
        self._save_log(entry)
        
        print("\n" + "="*70)
        print("WORKFLOW COMPLETED SUCCESSFULLY")
        print("="*70)
        print(f"Site URL: {urls.get('site_url', 'N/A')}")
        print(f"Report URL: {urls.get('report_url', 'N/A')}")
        print(f"Log saved: {self.log_file}")
        
        return True

def main():
    workflow = AutoPublishWorkflow()
    success = workflow.run_full_workflow()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
