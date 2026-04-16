#!/usr/bin/env python3
"""
区块链风险雷达 - GitHub Pages 自动化发布流程 v6.2 (Enhanced)
集成新模块：高风险代币观察列表、代币解锁预警、合约安全检测、链上数据可视化
"""

import os
import sys
import json
import subprocess
from datetime import datetime
from pathlib import Path

# 添加项目路径
sys.path.insert(0, r'F:\stepclaw\agents\blockchain-analyst')

# 导入增强版报告生成器
try:
    from scripts.generate_enhanced_report import (
        generate_enhanced_report, 
        generate_combined_markdown,
        generate_combined_html
    )
    ENHANCED_AVAILABLE = True
except ImportError as e:
    print(f"[WARNING] Enhanced report generator not available: {e}")
    ENHANCED_AVAILABLE = False

# 路径配置
BASE_DIR = Path(__file__).parent.parent
OUTPUT_DIR = BASE_DIR / "output"
LOGS_DIR = BASE_DIR / "logs"

# 确保目录存在
for dir_path in [OUTPUT_DIR, LOGS_DIR]:
    dir_path.mkdir(parents=True, exist_ok=True)


class EnhancedAutoPublishWorkflow:
    """增强版自动化发布工作流"""
    
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
    
    def step_1_generate_base_report(self):
        """步骤1: 生成基础报告"""
        print("\n" + "="*70)
        print("STEP 1: Generating Base Report (v6.0)")
        print("="*70)
        
        success, stdout, stderr = self.run_command(
            "python scripts\\generate_v60_html_report.py"
        )
        
        if success:
            print("[SUCCESS] Base report generated")
            # 查找生成的文件
            for line in stdout.split('\n'):
                if 'Report saved:' in line:
                    report_file = line.split('Report saved:')[1].strip()
                    return True, report_file
            # 默认路径
            return True, str(OUTPUT_DIR / f"v60_html_report_{datetime.now().strftime('%Y%m%d')}.md")
        else:
            print(f"[ERROR] Base report generation failed: {stderr}")
            return False, None
    
    def step_2_generate_enhanced_modules(self, use_demo_data=False):
        """步骤2: 生成增强模块"""
        print("\n" + "="*70)
        print("STEP 2: Generating Enhanced Modules (v6.2)")
        print("="*70)
        
        if not ENHANCED_AVAILABLE:
            print("[WARNING] Enhanced modules not available, skipping")
            return False, None
        
        try:
            # 生成增强版报告数据
            report_data = generate_enhanced_report(use_demo_data=use_demo_data)
            
            # 生成合并报告
            md_content = generate_combined_markdown(report_data)
            html_content = generate_combined_html(report_data)
            
            # 保存文件
            timestamp = datetime.now().strftime('%Y%m%d_%H%M')
            md_file = OUTPUT_DIR / f"enhanced_report_{timestamp}.md"
            html_file = OUTPUT_DIR / f"enhanced_report_{timestamp}.html"
            
            with open(md_file, 'w', encoding='utf-8') as f:
                f.write(md_content)
            
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            print(f"[SUCCESS] Enhanced report generated")
            print(f"  Markdown: {md_file}")
            print(f"  HTML: {html_file}")
            
            return True, {
                'md_file': str(md_file),
                'html_file': str(html_file),
                'data': report_data
            }
            
        except Exception as e:
            print(f"[ERROR] Enhanced modules failed: {e}")
            return False, None
    
    def step_3_convert_to_html(self, report_file):
        """步骤3: Markdown转HTML"""
        print("\n" + "="*70)
        print("STEP 3: Converting Markdown to HTML")
        print("="*70)
        
        success, stdout, stderr = self.run_command(
            f"python scripts\\md_to_html_converter.py \"{report_file}\""
        )
        
        if success:
            print("[SUCCESS] Report converted to HTML")
            return True
        else:
            print(f"[WARNING] HTML conversion failed: {stderr}")
            return False
    
    def step_4_add_seo_geo(self, html_file):
        """步骤4: 添加SEO/GEO标签"""
        print("\n" + "="*70)
        print("STEP 4: Adding SEO/GEO Tags")
        print("="*70)
        
        seo_file = str(Path(html_file).parent / f"seo_{Path(html_file).name}")
        
        success, stdout, stderr = self.run_command(
            f"python scripts\\seo_geo_publisher.py --input \"{html_file}\" --output \"{seo_file}\""
        )
        
        if success:
            print("[SUCCESS] SEO/GEO tags added")
            return True, seo_file
        else:
            print(f"[WARNING] SEO/GEO processing failed: {stderr}")
            return True, html_file
    
    def step_5_publish_to_github(self, seo_file):
        """步骤5: 发布到GitHub Pages"""
        print("\n" + "="*70)
        print("STEP 5: Publishing to GitHub Pages")
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
            return False, None
    
    def run_full_workflow(self, use_demo_data=False, publish=True):
        """
        运行完整工作流
        
        Args:
            use_demo_data: 是否使用演示数据
            publish: 是否发布到 GitHub Pages
        """
        print("="*70)
        print("CRYPTO RISK RADAR - Enhanced Auto Publish Workflow v6.2")
        print("="*70)
        print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Mode: {'Demo Data' if use_demo_data else 'Live Data'}")
        print(f"Publish: {'Yes' if publish else '