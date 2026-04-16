#!/usr/bin/env python3
"""
区块链风险雷达 - 集成版自动发布流程 v6.2
包含所有新模块：高风险代币、解锁预警、合约检测、数据可视化
"""

import os
import sys
import json
import subprocess
from datetime import datetime
from pathlib import Path

# 添加项目路径
sys.path.insert(0, r'F:\stepclaw\agents\blockchain-analyst')

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

# 路径配置
BASE_DIR = Path(__file__).parent.parent
OUTPUT_DIR = BASE_DIR / "output"
LOGS_DIR = BASE_DIR / "logs"
REPORTS_DIR = BASE_DIR / "reports"

# 确保目录存在
for dir_path in [OUTPUT_DIR, LOGS_DIR, REPORTS_DIR]:
    dir_path.mkdir(parents=True, exist_ok=True)


class IntegratedPublishWorkflow:
    """集成版自动发布工作流"""
    
    def __init__(self, use_demo_data=False):
        self.use_demo_data = use_demo_data
        self.log_file = LOGS_DIR / f"publish_log_{datetime.now().strftime('%Y%m%d')}.json"
        self.logs = self._load_logs()
        self.report_data = {
            'timestamp': datetime.now().isoformat(),
            'version': '6.2',
            'modules': {}
        }
    
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
        print("STEP 1: Generating Base Report")
        print("="*70)
        
        success, stdout, stderr = self.run_command(
            "python scripts\\generate_v60_html_report.py"
        )
        
        if success:
            print("[SUCCESS] Base report generated")
            # 查找生成的报告文件
            report_files = list(OUTPUT_DIR.glob("v60_html_report_*.md"))
            if report_files:
                latest = max(report_files, key=lambda p: p.stat().st_mtime)
                return True, str(latest)
            return True, None
        else:
            print(f"[ERROR] Base report generation failed: {stderr}")
            return False, None
    
    def step_2_high_risk_watchlist(self):
        """步骤2: 高风险代币观察列表"""
        print("\n" + "="*70)
        print("STEP 2: High-Risk Token Watchlist")
        print("="*70)
        
        if not MODULES_AVAILABLE:
            print("[WARNING] Modules not available, skipping")
            return False
        
        try:
            watchlist = HighRiskWatchlist(use_demo_data=self.use_demo_data)
            risk_tokens = watchlist.scan_high_risk_tokens(min_score=50, max_results=10)
            
            self.report_data['modules']['high_risk_watchlist'] = {
                'status': 'success',
                'count': len(risk_tokens),
                'markdown': watchlist.generate_markdown(risk_tokens),
                'html': watchlist.generate_html(risk_tokens),
                'data': risk_tokens
            }
            
            print(f"[SUCCESS] Found {len(risk_tokens)} high-risk tokens")
            return True
            
        except Exception as e:
            print(f"[ERROR] High-risk watchlist failed: {e}")
            self.report_data['modules']['high_risk_watchlist'] = {
                'status': 'error',
                'error': str(e)
            }
            return False
    
    def step_3_token_unlock_alert(self):
        """步骤3: 代币解锁预警"""
        print("\n" + "="*70)
        print("STEP 3: Token Unlock Alert")
        print("="*70)
        
        if not MODULES_AVAILABLE:
            print("[WARNING] Modules not available, skipping")
            return False
        
        try:
            unlock_alert = TokenUnlockAlert(use_demo_data=self.use_demo_data)
            unlocks = unlock_alert.get_unlock_alerts(days=7, min_usd=1_000_000, max_results=10)
            
            self.report_data['modules']['token_unlock_alert'] = {
                'status': 'success',
                'count': len(unlocks),
                'markdown': unlock_alert.generate_markdown(unlocks),
                'html': unlock_alert.generate_html(unlocks),
                'data': unlocks
            }
            
            print(f"[SUCCESS] Found {len(unlocks)} token unlocks")
            return True
            
        except Exception as e:
            print(f"[ERROR] Token unlock alert failed: {e}")
            self.report_data['modules']['token_unlock_alert'] = {
                'status': 'error',
                'error': str(e)
            }
            return False
    
    def step_4_contract_scanner(self):
        """步骤4: 合约安全检测"""
        print("\n" + "="*70)
        print("STEP 4: Contract Security Scanner")
        print("="*70)
        
        if not MODULES_AVAILABLE:
            print("[WARNING] Modules not available, skipping")
            return False
        
        try:
            scanner = ContractScanner(use_demo_data=self.use_demo_data)
            
            # 可以从高风险列表中获取合约地址进行扫描
            test_contracts = [
                ('0x1234567890abcdef1234567890abcdef12345678', 'ethereum'),
                ('0xabcdef1234567890abcdef1234567890abcdef12', 'bsc'),
            ]
            
            scan_results = scanner.scan_multiple(test_contracts)
            
            self.report_data['modules']['contract_scanner'] = {
                'status': 'success',
                'count': len(scan_results),
                'markdown': scanner.generate_markdown(scan_results),
                'html': scanner.generate_html(scan_results),
                'data': scan_results
            }
            
            print(f"[SUCCESS] Scanned {len(scan_results)} contracts")
            return True
            
        except Exception as e:
            print(f"[ERROR] Contract scanner failed: {e}")
            self.report_data['modules']['contract_scanner'] = {
                'status': 'error',
                'error': str(e)
            }
            return False
    
    def step_5_chart_generator(self):
        """步骤5: 数据可视化"""
        print("\n" + "="*70)
        print("STEP 5: Chart Generator")
        print("="*70)
        
        if not MODULES_AVAILABLE:
            print("[WARNING] Modules not available, skipping")
            return False
        
        try:
            chart_gen = ChartGenerator(use_demo_data=self.use_demo_data)
            charts = chart_gen.generate_all_charts()
            
            self.report_data['modules']['chart_generator'] = {
                'status': 'success',
                'charts': list(charts.keys()),
                'html': charts
            }
            
            print(f"[SUCCESS] Generated {len(charts)} charts")
            return True
            
        except Exception as e:
            print(f"[ERROR] Chart generator failed: {e}")
            self.report_data['modules']['chart_generator'] = {
                'status': 'error',
                'error': str(e)
            }
            return False
    
    def step_6_generate_integrated_report(self):
        """步骤6: 生成集成报告"""
        print("\n" + "="*70)
        print("STEP 6: Generating Integrated Report")
        print("="*70)
        
        try:
            # 保存 JSON 数据
            json_file = OUTPUT_DIR / f"integrated_report_{datetime.now().strftime('%Y%m%d_%H%M')}.json"
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(self.report_data, f, indent=2, ensure_ascii=False)
            
            # 生成 HTML 报告
            html_content = self._generate_html_report()
            html_file = OUTPUT_DIR / f"integrated_report_{datetime.now().strftime('%Y%m%d_%H%M')}.html"
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            print(f"[SUCCESS] Integrated report generated")
            print(f"  JSON: {json_file}")
            print(f"  HTML: {html_file}")
            
            return True, str(html_file)
            
        except Exception as e:
            print(f"[ERROR] Report generation failed: {e}")
            return False, None
    
    def _generate_tldr_summary(self):
        """生成 TL;DR 摘要"""
        tldr_parts = []
        
        # 高风险代币数量
        hr_module = self.report_data['modules'].get('high_risk_watchlist', {})
        if hr_module.get('status') == 'success':
            count = hr_module.get('count', 0)
            if count > 0:
                tldr_parts.append(f"发现 <strong>{count} 个高风险代币</strong>")
        
        # 代币解锁
        unlock_module = self.report_data['modules'].get('token_unlock_alert', {})
        if unlock_module.get('status') == 'success':
            count = unlock_module.get('count', 0)
            if count > 0:
                tldr_parts.append(f"<strong>{count} 个代币</strong>未来7天有大额解锁")
        
        # 合约风险
        contract_module = self.report_data['modules'].get('contract_scanner', {})
        if contract_module.get('status') == 'success':
            data = contract_module.get('data', [])
            critical = len([d for d in data if 'Critical' in d.get('risk_level', '')])
            if critical > 0:
                tldr_parts.append(f"<strong>{critical} 个合约</strong>存在严重安全风险")
        
        if not tldr_parts:
            return "<p>今日市场相对平稳，未发现重大风险信号。</p>"
        
        return f"<p>{'；'.join(tldr_parts)}。建议仔细阅读详细分析，做好风险管理。</p>"
    
    def _generate_html_report(self):
        """生成完整的 HTML 报告"""
        now = datetime.now()
        
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
    <title>Crypto Risk Radar - Integrated Report v6.2</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background-color: #0a0e27;
            color: #ffffff;
            line-height: 1.6;
            padding: 20px;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}
        header {{
            text-align: center;
            padding: 30px 0;
            border-bottom: 2px solid #2a3f5f;
            margin-bottom: 30px;
        }}
        h1 {{
            color: #00d4ff;
            font-size: 2.5em;
            margin-bottom: 10px;
        }}
        .meta {{
            color: #8b9dc3;
            font-size: 14px;
        }}
        .section {{
            background-color: #1a1f3a;
            border-radius: 12px;
            padding: 25px;
            margin-bottom: 25px;
            border: 1px solid #2a3f5f;
        }}
        h2 {{
            color: #00d4ff;
            margin-bottom: 15px;
            padding-bottom: 10px;
            border-bottom: 1px solid #2a3f5f;
        }}
        h3 {{
            color: #00d4ff;
            margin: 20px 0 10px 0;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 15px 0;
            background-color: #0a0e27;
        }}
        th {{
            background-color: #1a1f3a;
            color: #00d4ff;
            padding: 12px;
            text-align: left;
            border: 1px solid #2a3f5f;
        }}
        td {{
            color: #ffffff;
            padding: 12px;
            border: 1px solid #2a3f5f;
        }}
        tr:hover {{
            background-color: #0f1429;
        }}
        code {{
            background-color: #0a0e27;
            padding: 2px 6px;
            border-radius: 4px;
            font-family: monospace;
            color: #00d4ff;
        }}
        a {{
            color: #00d4ff;
            text-decoration: none;
        }}
        a:hover {{
            text-decoration: underline;
        }}
        ul {{
            margin: 10px 0 10px 20px;
        }}
        li {{
            margin: 5px 0;
        }}
        .risk-item, .unlock-item, .contract-item {{
            background-color: #0f1429;
            padding: 15px;
            border-radius: 8px;
            margin: 10px 0;
            border-left: 3px solid #00d4ff;
        }}
        .status-success {{
            color: #00d4ff;
        }}
        .status-error {{
            color: #ff6b6b;
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>Crypto Risk Radar</h1>
            <p class="meta">Integrated Report v6.2 | Generated: {now.strftime('%Y-%m-%d %H:%M UTC')}</p>
        </header>
        
        <!-- TL;DR 摘要 -->
        <div class="section" style="background: linear-gradient(135deg, #1a1f3a 0%, #0f1429 100%); border-left: 4px solid #00d4ff;">
            <h2 style="margin-top: 0;">📋 TL;DR - 今日要点</h2>
            {self._generate_tldr_summary()}
            <p style="color: #8b9dc3; font-size: 12px; margin-top: 10px;">
                <strong>免责声明</strong>: 本报告仅供信息参考，不构成投资建议。加密货币投资有风险，请做好自己的研究（DYOR）。
            </p>
        </div>
"""
        
        # 添加图表模块
        if self.report_data['modules'].get('chart_generator', {}).get('status') == 'success':
            charts = self.report_data['modules']['chart_generator']['html']
            if 'overview' in charts:
                html += f'<div class="section">{charts["overview"]}</div>'
            if 'netflow' in charts:
                html += f'<div class="section">{charts["netflow"]}</div>'
        
        # 添加高风险代币观察列表
        if self.report_data['modules'].get('high_risk_watchlist', {}).get('status') == 'success':
            html += self.report_data['modules']['high_risk_watchlist']['html']
        
        # 添加代币解锁预警
        if self.report_data['modules'].get('token_unlock_alert', {}).get('status') == 'success':
            html += self.report_data['modules']['token_unlock_alert']['html']
        
        # 添加合约安全检测
        if self.report_data['modules'].get('contract_scanner', {}).get('status') == 'success':
            html += self.report_data['modules']['contract_scanner']['html']
        
        html += """
        <footer style="text-align: center; padding: 20px; color: #8b9dc3; border-top: 1px solid #2a3f5f; margin-top: 30px;">
            <p>Crypto Risk Radar v6.2 | Data sources: DEX Screener, TokenUnlocks, GoPlus, CoinGecko</p>
            <p><em>This report is for informational purposes only. Always DYOR.</em></p>
        </footer>
    </div>
</body>
</html>
"""
        
        return html
    
    def run_full_workflow(self):
        """运行完整工作流"""
        print("="*70)
        print("CRYPTO RISK RADAR - Integrated Auto Publish Workflow v6.2")
        print("="*70)
        print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Mode: {'Demo Data' if self.use_demo_data else 'Live Data'}")
        
        entry = {
            "timestamp": datetime.now().isoformat(),
            "status": "running",
            "version": "6.2",
            "mode": "demo" if self.use_demo_data else "live"
        }
        
        # 步骤1: 生成基础报告
        success, base_report = self.step_1_generate_base_report()
        if not success:
            entry["status"] = "failed"
            entry["step"] = "base_report"
            self._save_log(entry)
            return False
        entry["base_report"] = base_report
        
        # 步骤2-5: 运行各模块
        self.step_2_high_risk_watchlist()
        self.step_3_token_unlock_alert()
        self.step_4_contract_scanner()
        self.step_5_chart_generator()
        
        # 步骤6: 生成集成报告
        success, integrated_report = self.step_6_generate_integrated_report()
        if not success:
            entry["status"] = "failed"
            entry["step"] = "integrated_report"
            self._save_log(entry)
            return False
        
        entry["status"] = "success"
        entry["integrated_report"] = integrated_report
        self._save_log(entry)
        
        print("\n" + "="*70)
        print("WORKFLOW COMPLETED SUCCESSFULLY")
        print("="*70)
        print(f"Report: {integrated_report}")
        
        return True


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Crypto Risk Radar - Integrated Publisher')
    parser.add_argument('--demo', action='store_true', help='Use demo data')
    parser.add_argument('--local-only', action='store_true', help='Generate local report only, do not publish')
    args = parser.parse_args()
    
    workflow = IntegratedPublishWorkflow(use_demo_data=args.demo)
    success = workflow.run_full_workflow()
    
    if success:
        print("\n✅ All tasks completed successfully!")
        sys.exit(0)
    else:
        print("\n❌ Workflow failed")
        sys.exit(1)


if __name__ == "__main__":
    main()
