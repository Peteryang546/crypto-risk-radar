#!/usr/bin/env python3
"""
区块链风险雷达 - 完整自动化发布流程
生成报告 → 清理 → SEO优化 → 发布到Hashnode
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
PUBLISH_DIR = BASE_DIR / "publish"
LOGS_DIR = BASE_DIR / "logs"

# 确保目录存在
for dir_path in [OUTPUT_DIR, PUBLISH_DIR, LOGS_DIR]:
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
        """步骤1: 生成报告"""
        print("\n" + "="*70)
        print("STEP 1: Generating Report")
        print("="*70)
        
        # 使用新的数据源配置
        success, stdout, stderr = self.run_command(
            "python scripts/generate_v52_report.py"
        )
        
        if not success:
            print(f"[ERROR] Report generation failed: {stderr}")
            return None
        
        # 解析生成的文件路径
        report_file = None
        for line in stdout.split('\n'):
            if 'Report saved:' in line:
                report_file = line.split('Report saved:')[1].strip()
                break
        
        if not report_file:
            # 查找最新的报告
            reports = sorted(OUTPUT_DIR.glob("v52_report_*.md"), 
                           key=lambda x: x.stat().st_mtime, reverse=True)
            if reports:
                report_file = str(reports[0])
        
        if report_file:
            print(f"[SUCCESS] Report generated: {report_file}")
            return report_file
        
        print("[ERROR] Could not find generated report")
        return None
    
    def step_2_clean_report(self, input_file):
        """步骤2: 清理报告用于发布"""
        print("\n" + "="*70)
        print("STEP 2: Cleaning Report for Publish")
        print("="*70)
        
        # 使用新的publish_cleaner脚本
        success, stdout, stderr = self.run_command(
            f"python scripts/publish_cleaner.py \"{input_file}\""
        )
        
        print(stdout)
        
        if not success:
            print(f"[WARN] Clean warning: {stderr}")
        
        # 查找清理后的文件
        cleaned_file = None
        for line in stdout.split('\n'):
            if 'Published version:' in line:
                cleaned_file = line.split('Published version:')[1].strip()
                break
        
        if not cleaned_file:
            # 在output目录查找publish_前缀的文件
            base_name = Path(input_file).name
            cleaned = OUTPUT_DIR / f"publish_{base_name}"
            if cleaned.exists():
                cleaned_file = str(cleaned)
        
        if cleaned_file:
            print(f"[SUCCESS] Cleaned report: {cleaned_file}")
            return cleaned_file
        
        # 如果没有清理版本，使用原始版本
        print("[INFO] Using original report")
        return input_file
    
    def step_3_optimize_seo(self, input_file):
        """步骤3: SEO优化"""
        print("\n" + "="*70)
        print("STEP 3: SEO & GEO Optimization")
        print("="*70)
        
        success, stdout, stderr = self.run_command(
            f"python scripts/seo_geo_optimizer.py \"{input_file}\""
        )
        
        print(stdout)
        
        if not success:
            print(f"[WARN] SEO optimization warning: {stderr}")
            return input_file
        
        # 查找优化后的文件
        optimized_file = None
        for line in stdout.split('\n'):
            if 'Optimized content saved:' in line:
                optimized_file = line.split('Optimized content saved:')[1].strip()
                break
        
        if not optimized_file:
            # 查找optimized_前缀的文件
            base_name = Path(input_file).name
            optimized = Path(input_file).parent / f"optimized_{base_name}"
            if optimized.exists():
                optimized_file = str(optimized)
        
        if optimized_file:
            print(f"[SUCCESS] Optimized report: {optimized_file}")
            return optimized_file
        
        print("[INFO] Using input file for publishing")
        return input_file
    
    def step_4_publish_to_hashnode(self, input_file):
        """步骤4: 发布到Hashnode"""
        print("\n" + "="*70)
        print("STEP 4: Publishing to Hashnode")
        print("="*70)
        
        # 生成标题
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')
        title = f"Crypto Risk Radar – 12H Report ({timestamp} UTC)"
        
        success, stdout, stderr = self.run_command(
            f'python scripts/hashnode_publisher.py publish '
            f'--file "{input_file}" '
            f'--title "{title}"'
        )
        
        print(stdout)
        
        if not success:
            print(f"[ERROR] Publish failed: {stderr}")
            return None
        
        # 解析发布结果
        post_url = None
        for line in stdout.split('\n'):
            if 'URL:' in line:
                post_url = line.split('URL:')[1].strip()
                break
        
        if post_url:
            print(f"[SUCCESS] Published to: {post_url}")
            return post_url
        
        return "published"
    
    def run_full_workflow(self):
        """运行完整工作流"""
        print("="*70)
        print("CRYPTO RISK RADAR - AUTO PUBLISH WORKFLOW")
        print("="*70)
        print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "status": "started"
        }
        
        # Step 1: Generate
        report_file = self.step_1_generate_report()
        if not report_file:
            log_entry["status"] = "failed"
            log_entry["step"] = "generate"
            self._save_log(log_entry)
            print("\n[FAIL] Workflow failed at Step 1")
            return False
        
        log_entry["report_file"] = report_file
        
        # Step 2: Clean
        cleaned_file = self.step_2_clean_report(report_file)
        log_entry["cleaned_file"] = cleaned_file
        
        # Step 3: Optimize
        optimized_file = self.step_3_optimize_seo(cleaned_file)
        log_entry["optimized_file"] = optimized_file
        
        # Step 4: Publish
        post_url = self.step_4_publish_to_hashnode(optimized_file)
        
        if post_url:
            log_entry["status"] = "success"
            log_entry["post_url"] = post_url
            self._save_log(log_entry)
            
            print("\n" + "="*70)
            print("WORKFLOW COMPLETED SUCCESSFULLY")
            print("="*70)
            print(f"Report published to Hashnode")
            print(f"URL: {post_url}")
            print(f"Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            return True
        else:
            log_entry["status"] = "failed"
            log_entry["step"] = "publish"
            self._save_log(log_entry)
            
            print("\n[FAIL] Workflow failed at Step 4")
            return False

def main():
    workflow = AutoPublishWorkflow()
    success = workflow.run_full_workflow()
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()
