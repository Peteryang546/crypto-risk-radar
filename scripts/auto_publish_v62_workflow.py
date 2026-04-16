#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
区块链风险雷达 - 增强版自动发布流程 v6.2
集成新模块：高风险代币观察列表、代币解锁预警、合约安全检测、数据可视化
"""

import os
import sys
import json
import subprocess
from datetime import datetime
from pathlib import Path

# 添加项目路径
sys.path.insert(0, r'F:\stepclaw\agents\blockchain-analyst')

# 路径配置
BASE_DIR = Path(__file__).parent.parent
OUTPUT_DIR = BASE_DIR / "output"
LOGS_DIR = BASE_DIR / "logs"

# 确保目录存在
for dir_path in [OUTPUT_DIR, LOGS_DIR]:
    dir_path.mkdir(parents=True, exist_ok=True)

# 导入模块
try:
    from modules.high_risk_watchlist import HighRiskWatchlist
    from modules.token_unlock_alert import TokenUnlockAlert
    from modules.contract_scanner import ContractScanner
    from modules.chart_generator import ChartGenerator
    MODULES_AVAILABLE = True
except ImportError as e:
    print(f"[WARNING] Modules not available: {e}")
    MODULES_AVAILABLE = False


class AutoPublishWorkflowV62:
    """增强版自动化发布工作流 v6.2"""
    
    def __init__(self, use_demo_data=False):
        self.log_file = LOGS_DIR / f"publish_log_{datetime.now().strftime('%Y%m%d')}.json"
        self.logs = self._load_logs()
        self.use_demo_data = use_demo_data
        self.report_data = {}
    
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
                if 'Report saved:' in line or 'Saved to:' in line:
                    report_file = line.split(':')[-1].strip()
                    return True, report_file
            return True, None
        else:
            print(f"[ERROR] Base report generation failed: {stderr}")
            return False, None
    
    def step_2_run_new_modules(self):
        """步骤2: 运行新模块"""
        print("\n" + "="*70)
        print("STEP 2: Running New Analysis Modules")
        print("="*70)
        
        if not MODULES_AVAILABLE:
            print("[WARNING] Modules not available, skipping")
            return True
        
        self.report_data['modules'] = {}
        
        # Module 1: 高风险代币观察列表
        print("\n[2.1] High-Risk Token Watchlist...")
        try:
            watchlist = HighRiskWatchlist(use_demo_data=self.use_demo_data)
            risk_tokens = watchlist.scan_high_risk_tokens(min_score=50, max_results=10)
            self.report_data['modules']['high_risk_watchlist'] = {
                'status': 'success',
                'count': len(risk_tokens),
                'html': watchlist.generate_html(risk_tokens)
            }
            print(f"  [SUCCESS] Found {len(risk_tokens)} high-risk tokens")
        except Exception as e:
            print(f"  [ERROR] {e}")
            self.report_data['modules']['high_risk_watchlist'] = {'status': 'error', 'error': str(e)}
        
        # Module 2: 代币解锁预警
        print("\n[2.2] Token Unlock Alert...")
        try:
            unlock_alert = TokenUnlockAlert(use_demo_data=self.use_demo_data)
            unlocks = unlock_alert.get_unlock_alerts(days=7, min_usd=1_000_000, max_results=10)
            self.report_data['modules']['token_unlock_alert'] = {
                'status': 'success',
                'count': len(unlocks),
                'html': unlock_alert.generate_html(unlocks)
            }
            print(f"  [SUCCESS] Found {len(unlocks)} token unlocks")
        except Exception as e:
            print(f"  [ERROR] {e}")
            self.report_data['modules']['token_unlock_alert'] = {'status': 'error', 'error': str(e)}
        
        # Module 3: 合约安全检测
        print("\n[2.3] Contract Security Scanner...")
        try:
            scanner = ContractScanner(use_demo_data=self.use_demo_data)
            # 可以从高风险列表中获取合约地址
            test_contracts = [
                ('0x1234567890abcdef1234567890abcdef12345678', 'ethereum'),
                ('0xabcdef1234567890abcdef1234567890abcdef12', 'bsc')
            ]
            scan_results = scanner.scan_multiple(test_contracts)
            self.report_data['modules']['contract_scanner'] = {
                'status': 'success',
                'count': len(scan_results),
                'html': scanner.generate_html(scan_results)
            }
            print(f"  [SUCCESS] Scanned {len(scan_results)} contracts")
        except Exception as e:
            print(f"  [ERROR] {e}")
            self.report_data['modules']['contract_scanner'] = {'status': 'error', 'error': str(e)}
        
        # Module 4: 数据可视化
        print("\n[2.4] Chart Generator...")
        try:
            chart_gen = ChartGenerator(use_demo_data=self.use_demo_data)
            charts = chart_gen.generate_all_charts()
            self.report_data['modules']['chart_generator'] = {
                'status': 'success',
                'charts': list(charts.keys()),
                'html': charts
            }
            print(f"  [SUCCESS] Generated {len(charts)} charts")
        except Exception as e:
            print(f"  [ERROR] {e}")
            self.report_data['modules']['chart_generator'] = {'status': 'error', 'error': str(e)}
        
        return True
    
    def step_3_merge_reports(self):
        """步骤3: 合并报告"""
        print("\n" + "="*70)
        print("STEP 3: Merging Reports")
        print("="*70)
        
        try:
            # 保存模块数据
            modules_file = OUTPUT_DIR / f"modules_data_{datetime.now().strftime('%Y%m%d_%H%M')}.json"
            with open(modules_file, 'w', encoding='utf-8') as f:
                json.dump(self.report_data, f, indent=2, ensure_ascii=False)
            
            print(f"[SUCCESS] Modules data saved: {modules_file}")
            return True, modules_file
            
        except Exception as e:
            print(f"[ERROR] Failed to merge reports: {e}")
            return False, None
    
    def step_4_convert_and_enhance(self):
        """步骤4: 转换并增强报告"""
        print("\n" + "="*70)
        print("STEP 4: Converting and Enhancing Report")
        print("="*70)
        
        # 运行增强版报告生成器
        success, stdout, stderr = self.run_command(
            "python scripts\\generate_enhanced_report.py"
        )
        
        if success:
            print("[SUCCESS] Enhanced report generated")
            # 查找生成的文件
            for line in stdout.split('\n'):
                if 'HTML report:' in line:
                    html_file = line.split(':')[-1].strip()
                    return True, html_file
            return True, None
        else:
            print(f"[ERROR] Report enhancement failed: {stderr}")
            return False, None
    
    def step_5_add_seo_geo(self, html_file):
        """步骤5: 添加SEO/GEO标签"""
        print("\n" + "="*70)
        print("STEP 5: Adding SEO/GEO Tags")
        print("="*70)
        
        if not html_file:
            print("[WARNING] No HTML file to enhance")
            return True, html_file
        
        # 运行SEO/GEO生成器
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
    
    def step_6_publish_to_github(self, seo_file):
        """步骤6: 发布到GitHub Pages"""
        print("\n" + "="*70)
        print("STEP 6: Publishing to GitHub Pages")
        print("="*70)
        
        # 生成标题
        now = datetime.now()
        et_time = now.strftime('%B %d, %Y')
        period = "Evening" if now.hour >= 12 else "Morning"
        title = f"Crypto Risk Radar - Enhanced 12H {period} Report | {et_time}"
        
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
    
    def run_full_workflow(self, publish=True):
        """运行完整工作流"""
        print("="*70)
        print("CRYPTO RISK RADAR - Enhanced Auto Publish Workflow v6.2")
        print("="*70)
        print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Mode: {'Demo Data' if self.use_demo_data else 'Live Data'}")
        
        entry = {
            "timestamp": datetime.now().isoformat(),
            "status": "running",
            "platform": "github_pages",
            "version": "6.2"
        }
        
        # Step 1: 生成基础报告
        success, base_report = self.step_1_generate_base_report()
        if not success:
            entry["status"] = "failed"
            entry["step"] = "generate_base"
            self._save_log(entry)
            return False
        entry["base_report"] = base_report
        
        # Step 2: 运行新模块
        success = self.step_2_run_new_modules()
        if not success:
            entry["status"] = "failed"
            entry["step"] = "new_modules"
            self._save_log(entry)
            return False
        
        # Step 3: 合并报告
        success, modules_file = self.step_3_merge_reports()
        if not success:
            entry["status"] = "failed"
            entry["step"] = "merge"
            self._save_log(entry)
            return False
        entry["modules_file"] = str(modules_file)
        
        # Step 4: 转换并增强报告
        success, html_file = self.step_4_convert_and_enhance()
        if not success:
            entry["status"] = "failed"
            entry["step"] = "enhance"
            self._save_log(entry)
            return False
        entry["html_file"] = html_file
        
        # Step 5: 添加SEO/GEO标签
        success, seo_file = self.step_5_add_seo_geo(html_file)
        if not success:
            entry["status"] = "failed"
            entry["step"] = "seo_geo"
            self._save_log(entry)
            return False
        entry["seo_file"] = seo_file
        
        # Step 6: 发布（可选）
        if publish:
            success, urls = self.step_6_publish_to_github(seo_file)
            if not success:
                entry["status"] = "failed"
                entry["step"] = "publish"
                self._save_log(entry)
                return False
            entry["urls"] = urls
        else:
            print("\n[SKIP] Publishing to GitHub Pages (local mode)")
            entry["urls"] = {"local_file": seo_file}
        
        entry["status"] = "success"
        self._save_log(entry)
        
        print("\n" + "="*70)
        print("WORKFLOW COMPLETED SUCCESSFULLY")
        print("="*70)
        
        if publish and entry.get("urls", {}).get("report_url"):
            print(f"Report URL: {entry['urls']['report_url']}")
        else:
            print(f"Local Report: {seo_file}")
        
        return True


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Enhanced Auto Publish Workflow v6.2')
    parser.add_argument('--demo', action='store_true', help='Use demo data')
    parser.add_argument('--local', action='store_true', help='Local mode (do not publish)')
    
    args = parser.parse_args()
    
    workflow = AutoPublishWorkflowV62(use_demo_data=args.demo)
    workflow.run_full_workflow(publish=not args.local)


if __name__ == "__main__":
    main()
