#!/usr/bin/env python3
"""
区块链风险雷达 - 完整发布流程
生成报告 → 清理 → 审核 → 输出发布版本
"""

import os
import sys
import subprocess
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
OUTPUT_DIR = BASE_DIR / "output"
PUBLISH_DIR = BASE_DIR / "publish"
PUBLISH_DIR.mkdir(parents=True, exist_ok=True)

def run_command(cmd, cwd=None):
    """运行命令并返回结果"""
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

def generate_report():
    """生成报告"""
    print("="*70)
    print("STEP 1: Generating Report")
    print("="*70)
    
    # 运行生成脚本
    success, stdout, stderr = run_command("python scripts/generate_v52_report.py")
    
    if not success:
        print(f"[ERROR] Report generation failed: {stderr}")
        return None
    
    # 解析输出来找到生成的文件
    for line in stdout.split('\n'):
        if 'Report saved:' in line:
            report_file = line.split('Report saved:')[1].strip()
            print(f"[SUCCESS] Report generated: {report_file}")
            return Path(report_file)
    
    # 如果解析失败，找最新的文件
    reports = sorted(OUTPUT_DIR.glob("v52_report_*.md"), key=lambda x: x.stat().st_mtime, reverse=True)
    if reports:
        print(f"[SUCCESS] Report generated: {reports[0]}")
        return reports[0]
    
    print("[ERROR] Could not find generated report")
    return None

def clean_report(input_file):
    """清理报告生成发布版本"""
    print("\n" + "="*70)
    print("STEP 2: Cleaning Report for Publishing")
    print("="*70)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M')
    publish_file = PUBLISH_DIR / f"publish_v52_{timestamp}.md"
    
    success, stdout, stderr = run_command(
        f"python scripts/clean_report.py {input_file} {publish_file}"
    )
    
    if not success:
        print(f"[ERROR] Report cleaning failed: {stderr}")
        return None
    
    print(f"[SUCCESS] Cleaned report saved: {publish_file}")
    return publish_file

def review_report(publish_file):
    """审核报告"""
    print("\n" + "="*70)
    print("STEP 3: Reviewing Report")
    print("="*70)
    
    # 运行审核脚本
    review_script = Path("../social-media-manager/scripts/review_blockchain_report.py")
    if not review_script.exists():
        # 尝试绝对路径
        review_script = BASE_DIR.parent / "social-media-manager/scripts/review_blockchain_report.py"
    
    success, stdout, stderr = run_command(
        f"python {review_script} {publish_file}",
        cwd=BASE_DIR.parent / "social-media-manager" if review_script.exists() else None
    )
    
    print(stdout)
    
    if stderr:
        print(f"[WARN] Review stderr: {stderr}")
    
    # 检查审核结果
    if "APPROVED" in stdout or "Result: APPROVED" in stdout:
        print("[SUCCESS] Report approved for publishing")
        return True
    else:
        print("[FAIL] Report rejected, needs fixes")
        return False

def output_for_discord(publish_file):
    """输出发不到Discord的内容"""
    print("\n" + "="*70)
    print("STEP 4: Output for Discord")
    print("="*70)
    
    try:
        with open(publish_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print("\n" + "="*70)
        print("DISCORD PUBLISH CONTENT")
        print("="*70)
        print(content)
        print("\n" + "="*70)
        print("END OF CONTENT")
        print("="*70)
        
        return True
    except Exception as e:
        print(f"[ERROR] Could not read publish file: {e}")
        return False

def main():
    print("="*70)
    print("BLOCKCHAIN RISK RADAR - COMPLETE PUBLISH WORKFLOW")
    print("="*70)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Step 1: Generate report
    report_file = generate_report()
    if not report_file:
        print("\n[FAIL] Workflow failed at Step 1")
        sys.exit(1)
    
    # Step 2: Clean report
    publish_file = clean_report(report_file)
    if not publish_file:
        print("\n[FAIL] Workflow failed at Step 2")
        sys.exit(1)
    
    # Step 3: Review report
    approved = review_report(publish_file)
    if not approved:
        print("\n[FAIL] Workflow failed at Step 3 - Report needs fixes")
        print("\nPlease fix the issues and re-run.")
        sys.exit(1)
    
    # Step 4: Output for Discord
    success = output_for_discord(publish_file)
    if not success:
        print("\n[FAIL] Workflow failed at Step 4")
        sys.exit(1)
    
    print("\n" + "="*70)
    print("WORKFLOW COMPLETED SUCCESSFULLY")
    print("="*70)
    print(f"Report ready for Discord publishing")
    print(f"Publish file: {publish_file}")
    print(f"Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == '__main__':
    main()
