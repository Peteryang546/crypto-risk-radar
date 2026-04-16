#!/usr/bin/env python3
"""
区块链风险雷达 - 完整自动化发布流程 v6.0
生成HTML报告 → 清理 → 发布到Hashnode
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
    
    def step_2_clean_report(self, report_file):
        """步骤2: 清理报告"""
        print("\n" + "="*70)
        print("STEP 2: Cleaning Report for Publishing")
        print("="*70)
        
        success, stdout, stderr = self.run_command(
            f"python scripts\\publish_html_cleaner.py \"{report_file}\""
        )
        
        if success:
            print("[SUCCESS] Report cleaned")
            # 提取清理后的文件名
            for line in stdout.split('\n'):
                if 'Cleaned HTML report:' in line:
                    cleaned_file = line.split('Cleaned HTML report:')[1].strip()
                    return True, cleaned_file
            # 默认路径
            report_path = Path(report_file)
            cleaned_file = str(report_path.parent / f"publish_{report_path.name}")
            return True, cleaned_file
        else:
            print(f"[ERROR] Report cleaning failed: {stderr}")
            return False, None
    
    def step_3_publish_to_hashnode(self, cleaned_file):
        """步骤3: 发布到Hashnode"""
        print("\n" + "="*70)
        print("STEP 3: Publishing to Hashnode")
        print("="*70)
        
        # 生成标题
        now = datetime.now()
        et_time = now.strftime('%B %d, %Y')
        title = f"Crypto Risk Radar - 12H Report | {et_time}"
        
        success, stdout, stderr = self.run_command(
            f"python scripts\\hashnode_publisher.py publish --file \"{cleaned_file}\" --title \"{title}\""
        )
        
        if success:
            print("[SUCCESS] Published to Hashnode")
            # 提取发布URL
            for line in stdout.split('\n'):
                if 'URL:' in line:
                    url = line.split('URL:')[1].strip()
                    return True, url
            return True, None
        else:
            print(f"[ERROR] Publishing failed: {stderr}")
            return False, None
    
    def run_full_workflow(self):
        """运行完整工作流"""
        print("="*70)
        print("CRYPTO RISK RADAR - Auto Publish Workflow v6.0")
        print("="*70)
        print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        entry = {
            "timestamp": datetime.now().isoformat(),
            "status": "running"
        }
        
        # Step 1: 生成报告
        success, report_file = self.step_1_generate_report()
        if not success:
            entry["status"] = "failed"
            entry["step"] = "generate"
            self._save_log(entry)
            return False
        entry["report_file"] = report_file
        
        # Step 2: 清理报告
        success, cleaned_file = self.step_2_clean_report(report_file)
        if not success:
            entry["status"] = "failed"
            entry["step"] = "clean"
            self._save_log(entry)
            return False
        entry["cleaned_file"] = cleaned_file
        
        # Step 3: 发布
        success, url = self.step_3_publish_to_hashnode(cleaned_file)
        if not success:
            entry["status"] = "failed"
            entry["step"] = "publish"
            self._save_log(entry)
            return False
        
        entry["status"] = "success"
        entry["url"] = url
        self._save_log(entry)
        
        print("\n" + "="*70)
        print("WORKFLOW COMPLETED SUCCESSFULLY")
        print("="*70)
        print(f"Report URL: {url}")
        print(f"Log saved: {self.log_file}")
        
        return True

def main():
    workflow = AutoPublishWorkflow()
    workflow.run_full_workflow()

if __name__ == "__main__":
    main()
