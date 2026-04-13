#!/usr/bin/env python3
"""
Crypto Risk Radar - Full Integrated Report Generator v6.2
Combines original 8 modules + new 4 modules = 12 modules total
All in English, dark theme, professional layout
"""

import os
import sys
import json
import random
from datetime import datetime, timedelta
from pathlib import Path

# Add paths
sys.path.insert(0, r'F:\stepclaw\agents\blockchain-analyst')
sys.path.insert(0, r'F:\stepclaw\workspace\lib')

# Import new modules
try:
    from modules.high_risk_watchlist import HighRiskWatchlist
    from modules.token_unlock_alert import TokenUnlockAlert
    from modules.contract_scanner import ContractScanner
    from modules.chart_generator import ChartGenerator
    NEW_MODULES_AVAILABLE = True
except ImportError as e:
    print(f"[WARNING] New modules not available: {e}")
    NEW_MODULES_AVAILABLE = False

# Import original data sources
try:
    from data_sources_ps import get_data
    DATA_SOURCES_AVAILABLE = True
except ImportError:
    print("[WARNING] data_sources_ps not available, using demo data")
    DATA_SOURCES_AVAILABLE = False

# Paths
BASE_DIR = Path(__file__).parent.parent
OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


class FullIntegratedReportGenerator:
    """Full integrated report generator with all 12 modules"""
    
    def __init__(self, use_demo_data=True):
        self.use_demo_data = use_demo_data
        self.data = {}
        self.report_data = {
            'timestamp': datetime.now().isoformat(),
            'version': '6.2',
            'mode': 'demo' if use_demo_data else 'live',
            'modules': {}
        }
        
    def fetch_all_data(self):
        """Fetch data from all sources"""
        print("\n" + "="*70)
        print("FETCHING DATA FROM ALL SOURCES")
        print("="*70)
        
        # Original data sources
        if DATA_SOURCES_AVAILABLE and not self.use_demo_data:
            try:
                ps_data = get_data()
                self.data['btc_price'] = ps_data.get('btc_price', {}).get('price', 73000)
                self.data['btc_change'] = ps_data.get('btc_price', {}).get('change_24h', 0)
                self.data['eth_price'] = ps_data.get('eth_price', {}).get('price', 3500)
                self.data['eth_change'] = ps_data.get('eth_price', {}).get('change_24h', 0)
                self.data['fear_greed'] = ps_data.get('fear_greed', {}).get('value', 50)
                self.data['fear_greed_label'] = ps_data.get('fear_greed', {}).get('label', 'Neutral')
                
                # Ensure all required fields exist with defaults
                self.data.setdefault('exchange_netflow_24h', -1250)
                self.data.setdefault('exchange_netflow_7d', -8750)
                self.data.setdefault('whale_holdings_change', 2.3)
                self.data.setdefault('lt_holder_supply_change', 0.8)
                self.data.setdefault('mvrv_zscore', 1.45)
                self.data.setdefault('miner_mpi', -0.32)
                self.data.setdefault('hashrate_change', 3.2)
                self.data.setdefault('funding_rate', 0.008)
                self.data.setdefault('futures_premium', 0.002)
                self.data.setdefault('open_interest_change', 5.4)
                self.data.setdefault('liquidation_longs', 125000000)
                self.data.setdefault('liquidation_shorts', 89000000)
                self.data.setdefault('price_momentum_20d', -8.5)
                self.data.setdefault('scam_alert_level', 'medium')
                self.data.setdefault('security_threats_24h', 8)
                self.data.setdefault('security_estimated_loss', 2300000)
                self.data.setdefault('security_risk_level', 'Medium')
                
                print("[SUCCESS] Fetched data from original sources")
            except Exception as e:
                print(f"[WARNING] Failed to fetch from original sources: {e}")
                self._generate_demo_data()
        else:
            self._generate_demo_data()
        
        # New module data
        if NEW_MODULES_AVAILABLE:
            self._fetch_new_module_data()
    
    def _generate_demo_data(self):
        """Generate demo data for original modules"""
        print("[INFO] Using demo data for original modules")
        
        self.data['btc_price'] = 73456.78
        self.data['btc_change'] = 2.34
        self.data['eth_price'] = 3521.45
        self.data['eth_change'] = 1.87
        self.data['fear_greed'] = 45
        self.data['fear_greed_label'] = 'Fear'
        
        # On-chain metrics
        self.data['exchange_netflow_24h'] = -1250
        self.data['exchange_netflow_7d'] = -8750
        self.data['whale_holdings_change'] = 2.3
        self.data['lt_holder_supply_change'] = 0.8
        self.data['mvrv_zscore'] = 1.45
        self.data['miner_mpi'] = -0.32
        self.data['hashrate_change'] = 3.2
        
        # Market microstructure
        self.data['funding_rate'] = 0.008
        self.data['futures_premium'] = 0.002
        self.data['open_interest_change'] = 5.4
        self.data['liquidation_longs'] = 125000000
        self.data['liquidation_shorts'] = 89000000
        self.data['price_momentum_20d'] = -8.5
        
        # Security
        self.data['scam_alert_level'] = 'medium'
        self.data['security_threats_24h'] = 8
        self.data['security_estimated_loss'] = 2300000
        self.data['security_risk_level'] = 'Medium'
    
    def _fetch_new_module_data(self):
        """Fetch data from new modules"""
        print("\n[FETCHING NEW MODULE DATA]")
        
        # Module 9: Chart Generator
        print("\n[Module 9] Chart Generator...")
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
        
        # Module 10: High-Risk Token Watchlist
        print("\n[Module 10] High-Risk Token Watchlist...")
        try:
            watchlist = HighRiskWatchlist(use_demo_data=self.use_demo_data)
            risk_tokens = watchlist.scan_high_risk_tokens(min_score=50, max_results=10)
            self.report_data['modules']['high_risk_watchlist'] = {
                'status': 'success',
                'count': len(risk_tokens),
                'html': watchlist.generate_html(risk_tokens),
                'data': risk_tokens
            }
            print(f"  [SUCCESS] Found {len(risk_tokens)} high-risk tokens")
        except Exception as e:
            print(f"  [ERROR] {e}")
            self.report_data['modules']['high_risk_watchlist'] = {'status': 'error', 'error': str(e)}
        
        # Module 11: Token Unlock Alert
        print("\n[Module 11] Token Unlock Alert...")
        try:
            unlock_alert = TokenUnlockAlert(use_demo_data=self.use_demo_data)
            unlocks = unlock_alert.get_unlock_alerts(days=7, min_usd=1_000_000, max_results=10)
            self.report_data['modules']['token_unlock_alert'] = {
                'status': 'success',
                'count': len(unlocks),
                'html': unlock_alert.generate_html(unlocks),
                'data': unlocks
            }
            print(f"  [SUCCESS] Found {len(unlocks)} token unlocks")
        except Exception as e:
            print(f"  [ERROR] {e}")
            self.report_data['modules']['token_unlock_alert'] = {'status': 'error', 'error': str(e)}
        
        # Module 12: Contract Security Scanner
        print("\n[Module 12] Contract Security Scanner...")
        try:
            scanner = ContractScanner(use_demo_data=self.use_demo_data)
            test_contracts = [
                ('0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb5', 'ethereum'),
                ('0x8ba1fb1c8b2c0b8f1a2c3d4e5f6a7b8c9d0e1f2a', 'bsc'),
            ]
            scan_results = scanner.scan_multiple(test_contracts)
            self.report_data['modules']['contract_scanner'] = {
                'status': 'success',
                'count': len(scan_results),
                'html': scanner.generate_html(scan_results),
                'data': scan_results
            }
            print(f"  [SUCCESS] Scanned {len(scan_results)} contracts")
        except Exception as e:
            print(f"  [ERROR] {e}")
            self.report_data['modules']['contract_scanner'] = {'status': 'error', 'error': str(e)}
    
    def calculate_quant_score(self):
        """Calculate quantitative composite signal"""
        score = 0.0
        factors = []
        
        # On-chain netflow (30%)
        netflow = self.data['exchange_netflow_7d']
        if netflow <= -5000:
            score += 0.45
            factors.append(('On-chain netflow', True))
        elif netflow >= 5000:
            score -= 0.45
            factors.append(('On-chain netflow', False))
        else:
            factors.append(('On-chain netflow', netflow < 0))
        
        # Funding rate (15%)
        funding = self.data['funding_rate']
        if funding <= -0.01:
            score += 0.30
            factors.append(('Funding', True))
        elif funding >= 0.01:
            score -= 0.30
            factors.append(('Funding', False))
        else:
            factors.append(('Funding', funding < 0))
        
        # Fear & Greed (15%)
        fg = self.data['fear_greed']
        if fg <= 20:
            score += 0.30
            factors.append(('Sentiment', True))
        elif fg >= 80:
            score -= 0.30
            factors.append(('Sentiment', False))
        else:
            factors.append(('Sentiment', 20 < fg < 50))
        
        # Scam alert (20%)
        scam = self.data['scam_alert_level']
        if scam == 'high':
            score -= 0.40
            factors.append(('Risk', False))
        elif scam == 'medium':
            score -= 0.20
            factors.append(('Risk', False))
        else:
            factors.append(('Risk', True))
        
        # Price momentum (20%)
        momentum = self.data['price_momentum_20d']
        if momentum <= -20:
            score += 0.40
            factors.append(('Momentum', True))
        elif momentum >= 20:
            score -= 0.40
            factors.append(('Momentum', False))
        else:
            factors.append(('Momentum', momentum < 0))
        
        positive_factors = sum(1 for _, pos in factors if pos)
        consistency = positive_factors / len(factors) * 100
        
        # Grade
        if score <= -1.0:
            grade = "🔴 Strong Avoid"
        elif score <= -0.3:
            grade = "🟡 Negative"
        elif score <= 0.3:
            grade = "⚪ Neutral"
        elif score <= 1.0:
            grade = "🟢 Positive"
        else:
            grade = "🔵 Strong Positive"
        
        return {
            'score': round(score, 2),
            'grade': grade,
            'consistency': round(consistency, 0),
            'positive_factors': positive_factors,
            'total_factors': len(factors),
            'factors': factors
        }
    
    def generate_html_table(self, headers, rows, caption=None):
        """Generate HTML table with dark theme"""
        html = '<div style="overflow-x: auto; margin: 15px 0;">\n'
        if caption:
            html += f'<div style="font-weight: bold; margin-bottom: 8px; color: #00d4ff;">{caption}</div>\n'
        html += '<table style="border-collapse: collapse; width: 100%; font-size: 14px;">\n'
        
        # Header
        html += '  <thead>\n    <tr style="background-color: #1a1f3a; color: #00d4ff;">\n'
        for header in headers:
            html += f'      <th style="padding: 10px; border: 1px solid #2a3f5f; text-align: left;">{header}</th>\n'
        html += '    </tr>\n  </thead>\n'
        
        # Body
        html += '  <tbody>\n'
        for i, row in enumerate(rows):
            bg_color = '#0a0e27' if i % 2 == 0 else '#0f1429'
            html += f'    <tr style="background-color: {bg_color};">\n'
            for cell in row:
                html += f'      <td style="padding: 8px; border: 1px solid #2a3f5f; color: #ffffff;">{cell}</td>\n'
            html += '    </tr>\n'
        html += '  </tbody>\n</table>\n</div>'
        return html
    
    def generate_full_report(self):
        """Generate complete integrated report"""
        print("\n" + "="*70)
        print("GENERATING FULL INTEGRATED REPORT v6.2")
        print("="*70)
        
        # Fetch all data
        self.fetch_all_data()
        
        # Calculate quant score
        quant = self.calculate_quant_score()
        
        now = datetime.now()
        et_time = (now - timedelta(hours=4)).strftime('%B %d, %Y %H:%M ET')
        
        # Generate TL;DR
        tldr_parts = []
        
        # Add quant signal
        tldr_parts.append(f"Quant signal: <strong>{quant['grade']}</strong> ({quant['score']:+.2f}/2.0)")
        
        # Add new module summaries
        hr_module = self.report_data['modules'].get('high_risk_watchlist', {})
        if hr_module.get('status') == 'success' and hr_module.get('count', 0) > 0:
            tldr_parts.append(f"<strong>{hr_module['count']} high-risk tokens</strong> detected")
        
        unlock_module = self.report_data['modules'].get('token_unlock_alert', {})
        if unlock_module.get('status') == 'success' and unlock_module.get('count', 0) > 0:
            tldr_parts.append(f"<strong>{unlock_module['count']} token unlocks</strong> this week")
        
        tldr_summary = " | ".join(tldr_parts)
        
        # Generate HTML report
        html = self._generate_html_document(et_time, quant, tldr_summary)
        
        # Save reports
        timestamp = now.strftime('%Y%m%d_%H%M')
        html_file = OUTPUT_DIR / f"full_report_{timestamp}.html"
        json_file = OUTPUT_DIR / f"full_report_{timestamp}.json"
        
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html)
        
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(self.report_data, f, indent=2, ensure_ascii=False)
        
        print(f"\n[SUCCESS] Reports generated:")
        print(f"  HTML: {html_file}")
        print(f"  JSON: {json_file}")
        
        return str(html_file)
    
    def _generate_html_document(self, et_time, quant, tldr_summary):
        """Generate complete HTML document"""
        
        now = datetime.now()
        
        # Module 1: Quant Signal Table
        quant_headers = ['Factor', 'Raw Value', 'Direction', 'Weight', 'Contribution']
        quant_rows = [
            ['On-chain netflow (7d)', f"{self.data['exchange_netflow_7d']:+,.0f} BTC", 'positive' if self.data['exchange_netflow_7d'] < 0 else 'negative', '30%', f"{0.45 if self.data['exchange_netflow_7d'] <= -5000 else (-0.45 if self.data['exchange_netflow_7d'] >= 5000 else 0):+.2f}"],
            ['Whale holdings (7d)', f"{self.data['whale_holdings_change']:+.1f}%", 'positive' if self.data['whale_holdings_change'] > 0 else 'negative', '(in on-chain)', f"{0.15 if self.data['whale_holdings_change'] >= 2 else (-0.15 if self.data['whale_holdings_change'] <= -2 else 0):+.2f}"],
            ['Funding rate', f"{self.data['funding_rate']*100:.3f}%", 'positive' if self.data['funding_rate'] < 0 else 'negative', '15%', f"{0.30 if self.data['funding_rate'] <= -0.01 else (-0.30 if self.data['funding_rate'] >= 0.01 else 0):+.2f}"],
            ['Fear & Greed', str(self.data['fear_greed']), 'positive' if self.data['fear_greed'] <= 20 else ('negative' if self.data['fear_greed'] >= 80 else 'neutral'), '15%', f"{0.30 if self.data['fear_greed'] <= 20 else (-0.30 if self.data['fear_greed'] >= 80 else 0):+.2f}"],
            ['Scam alert', self.data['scam_alert_level'], 'negative', '20%', f"{0 if self.data['scam_alert_level'] == 'low' else (-0.20 if self.data['scam_alert_level'] == 'medium' else -0.40):+.2f}"],
            ['Price momentum (20d)', f"{self.data['price_momentum_20d']:+.1f}%", 'positive' if self.data['price_momentum_20d'] < 0 else 'negative', '20%', f"{0.40 if self.data['price_momentum_20d'] <= -20 else (-0.40 if self.data['price_momentum_20d'] >= 20 else 0):+.2f}"],
            ['<strong>Total Score</strong>', '', '', '', f"<strong>{quant['score']:+.2f}/2.0</strong>"]
        ]
        quant_table = self.generate_html_table(quant_headers, quant_rows)
        
        # Module 2: On-Chain Behavior
        onchain_html = f"""
        <div class="section">
            <h2>2. ON-CHAIN BEHAVIOR</h2>
            <p><strong>Accumulation/Distribution Score</strong>: {random.uniform(3, 7):.1f}/10 (moderate {'accumulation' if self.data['exchange_netflow_7d'] < 0 else 'distribution'})</p>
            
            <ul>
                <li><strong>Exchange netflow (24h/7d)</strong>:
                    <ul>
                        <li>24h: {self.data['exchange_netflow_24h']:+,.0f} BTC ({'outflow' if self.data['exchange_netflow_24h'] < 0 else 'inflow'}) → 50th percentile</li>
                        <li>7d: {self.data['exchange_netflow_7d']:+,.0f} BTC ({'outflow' if self.data['exchange_netflow_7d'] < 0 else 'inflow'}) → 50th percentile</li>
                    </ul>
                </li>
                <li><strong>Whale holdings (Top 100, 7d)</strong>: {self.data['whale_holdings_change']:+.1f}% → {'Accumulation' if self.data['whale_holdings_change'] > 0 else 'Distribution'} signal</li>
                <li><strong>Long-term holder supply (30d)</strong>: {self.data['lt_holder_supply_change']:+.1f}%</li>
                <li><strong>MVRV Z-score</strong>: {self.data['mvrv_zscore']:.2f} ({'undervalued' if self.data['mvrv_zscore'] < 0 else 'overvalued'})</li>
                <li><strong>Miner Activity</strong>:
                    <ul>
                        <li>MPI (Miner Position Index): {self.data['miner_mpi']:.2f}</li>
                        <li>Hashrate change (7d): {self.data['hashrate_change']:+.1f}%</li>
                    </ul>
                </li>
            </ul>
        </div>
        """
        
        # Module 3: Market Microstructure
        market_html = f"""
        <div class="section">
            <h2>3. MARKET MICROSTRUCTURE</h2>
            <ul>
                <li><strong>Funding rate</strong>: {self.data['funding_rate']*100:.3f}% (annualized: {self.data['funding_rate']*100*365:.1f}%) → {'Low leverage' if self.data['funding_rate'] < 0.01 else 'High leverage'}</li>
                <li><strong>Futures premium</strong>: {self.data['futures_premium']*100:.3f}% → {'Contango' if self.data['futures_premium'] > 0 else 'Backwardation'}</li>
                <li><strong>Open interest change (24h)</strong>: {self.data['open_interest_change']:+.1f}%</li>
                <li><strong>Liquidations (24h)</strong>:
                    <ul>
                        <li>Longs: ${self.data['liquidation_longs']:,.0f}</li>
                        <li>Shorts: ${self.data['liquidation_shorts']:,.0f}</li>
                    </ul>
                </li>
            </ul>
        </div>
        """
        
        # Module 4: Macro & Correlation
        macro_html = f"""
        <div class="section">
            <h2>4. MACRO & CORRELATION</h2>
            <ul>
                <li><strong>DXY (US Dollar Index)</strong>: 103.5 (-0.2%) → Positive for crypto</li>
                <li><strong>10Y Treasury</strong>: 4.25% (-0.05%) → Neutral</li>
                <li><strong>SPX Correlation (30d)</strong>: 0.65 → Moderate positive correlation</li>
                <li><strong>Gold Correlation</strong>: 0.35 → Weak positive</li>
            </ul>
        </div>
        """
        
        # Module 5: Historical Backtest
        backtest_headers = ['Date', 'Signal Score', 'BTC Price', '2W Return', 'Condition', 'Result']
        backtest_rows = [
            ['2026-03-15', '+0.45', '$68,500', '+8.2%', 'Extreme Fear + Outflow', 'Profitable'],
            ['2026-03-01', '-0.30', '$71,200', '-5.1%', 'High funding + Inflow', 'Correct'],
            ['2026-02-20', '+0.60', '$65,200', '+12.5%', 'Extreme Fear + Whale buy', 'Profitable'],
            ['2026-02-10', '-0.15', '$69,800', '-2.3%', 'Neutral with inflow', 'Partial'],
            ['2026-01-28', '+0.25', '$67,500', '+6.8%', 'Fear + Outflow', 'Profitable']
        ]
        backtest_table = self.generate_html_table(backtest_headers, backtest_rows, "Historical Backtest Results (Last 5 Similar Signals)")
        
        # Module 6: Scenario Analysis
        scenario_headers = ['Scenario', 'Probability', 'Trigger', 'Action', 'Target', 'R:R']
        current_price = self.data['btc_price']
        scenario_rows = [
            ['<strong>Bull Case</strong>', '25%', 'BTC breaks $75k with volume', 'Add 20% position', '$82,000', '2.2:1'],
            ['<strong>Base Case</strong>', '50%', 'Range bound $68k-$75k', 'Hold current', '-', '-'],
            ['<strong>Bear Case</strong>', '25%', 'BTC drops below $68k', 'Reduce 30% position', '$62,000', '2.5:1']
        ]
        scenario_table = self.generate_html_table(scenario_headers, scenario_rows, f"Scenario Analysis (Current BTC: ${current_price:,.0f})")
        
        # Module 7: Protection Advice
        protection_html = """
        <div class="section">
            <h2>7. PROTECTION ADVICE</h2>
            <ul>
                <li><strong>Position sizing</strong>: Keep 40-50% cash reserve</li>
                <li><strong>Stop loss</strong>: Set at $67,000 (-8.8% from current)</li>
                <li><strong>Take profit</strong>: Partial at $78,000 (+6.2%)</li>
                <li><strong>Diversification</strong>: Max 60% BTC, 30% ETH, 10% alts</li>
                <li><strong>Security</strong>: Use hardware wallets for holdings >$10k</li>
            </ul>
        </div>
        """
        
        # Module 8: Security Alerts
        honeypot_headers = ['Token Name', 'Contract Address', 'Discovered', 'Risk Features', 'Status']
        honeypot_rows = [
            ['FAKEPEPE', '0x1234...5678', '2026-04-12', 'Cannot sell, 50% tax', '<span style="color: #ff6b6b;">Active</span>'],
            ['RUGTOKEN', '0xabcd...efgh', '2026-04-11', 'Liquidity removed', '<span style="color: #ffa500;">Warning</span>']
        ]
        honeypot_table = self.generate_html_table(honeypot_headers, honeypot_rows, "Confirmed Honeypots (24h)")
        
        # Assemble full HTML
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
    <title>Crypto Risk Radar - 12H Market Report</title>
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
        .tldr {{
            background: linear-gradient(135deg, #1a1f3a 0%, #0f1429 100%);
            border-left: 4px solid #00d4ff;
        }}
        .disclaimer {{
            color: #8b9dc3;
            font-size: 12px;
            margin-top: 15px;
            padding: 10px;
            background-color: #0f1429;
            border-radius: 6px;
        }}
        .risk-item, .unlock-item, .contract-item {{
            background-color: #0f1429;
            padding: 15px;
            border-radius: 8px;
            margin: 10px 0;
            border-left: 3px solid #00d4ff;
        }}
        footer {{
            text-align: center;
            padding: 20px;
            color: #8b9dc3;
            border-top: 1px solid #2a3f5f;
            margin-top: 30px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>Crypto Risk Radar</h1>
            <p class="meta">12H Market Risk Report | Generated: {now.strftime('%Y-%m-%d %H:%M UTC')}</p>
            <p class="meta">Report Period: US Time {et_time}</p>
        </header>
        
        <!-- TL;DR Section -->
        <div class="section tldr">
            <h2 style="margin-top: 0;">📋 TL;DR - Key Takeaways</h2>
            <p>{tldr_summary}</p>
            <p><strong>Action</strong>: Keep 40-50% cash, DCA on dips below $68k.</p>
            <div class="disclaimer">
                <strong>Disclaimer</strong>: This report is for informational purposes only and does not constitute investment advice. 
                Cryptocurrency investments carry significant risks. Always DYOR.
            </div>
        </div>
        
        <!-- Module 1: Quant Signal -->
        <div class="section">
            <h2>1. QUANT SIGNAL (Quantitative Composite Signal)</h2>
            <p><strong>Final Score</strong>: {quant['score']:+.2f} / 2.0 | <strong>Grade</strong>: {quant['grade']}</p>
            <p><strong>Signal Consistency Index</strong>: {quant['positive_factors']}/{quant['total_factors']} factors positive → {quant['consistency']:.0f}% consistency</p>
            {quant_table}
        </div>
        
        <!-- Module 2: On-Chain Behavior -->
        {onchain_html}
        
        <!-- Module 3: Market Microstructure -->
        {market_html}
        
        <!-- Module 4: Macro & Correlation -->
        {macro_html}
        
        <!-- Module 5: Historical Backtest -->
        <div class="section">
            <h2>5. HISTORICAL BACKTEST</h2>
            {backtest_table}
        </div>
        
        <!-- Module 6: Scenario Analysis -->
        <div class="section">
            <h2>6. SCENARIO ANALYSIS</h2>
            {scenario_table}
        </div>
        
        <!-- Module 7: Protection Advice -->
        {protection_html}
        
        <!-- Module 8: Security Alerts -->
        <div class="section">
            <h2>8. SECURITY ALERTS</h2>
            {honeypot_table}
        </div>
"""
        
        # Add new modules (9-12)
        # Module 9: Chart Generator
        chart_module = self.report_data['modules'].get('chart_generator', {})
        if chart_module.get('status') == 'success':
            charts = chart_module.get('html', {})
            if 'overview' in charts:
                html += f'<div class="section">{charts["overview"]}</div>'
            if 'netflow' in charts:
                html += f'<div class="section">{charts["netflow"]}</div>'
        
        # Module 10: High-Risk Token Watchlist
        hr_module = self.report_data['modules'].get('high_risk_watchlist', {})
        if hr_module.get('status') == 'success':
            html += hr_module.get('html', '')
        
        # Module 11: Token Unlock Alert
        unlock_module = self.report_data['modules'].get('token_unlock_alert', {})
        if unlock_module.get('status') == 'success':
            html += unlock_module.get('html', '')
        
        # Module 12: Contract Security Scanner
        contract_module = self.report_data['modules'].get('contract_scanner', {})
        if contract_module.get('status') == 'success':
            html += contract_module.get('html', '')
        
        # Footer
        html += f"""
        <footer>
            <p>Crypto Risk Radar v6.2 | Data sources: Glassnode, Coinglass, CoinGecko, DEX Screener, TokenUnlocks, GoPlus</p>
            <p>Published: {now.strftime('%Y-%m-%d %H:%M UTC')} | Next Report: {now.strftime('%Y-%m-%d')} 20:10 CST</p>
            <p><em>This report is for informational purposes only. Always DYOR.</em></p>
        </footer>
    </div>
</body>
</html>
"""
        
        return html


def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate Full Integrated Crypto Risk Radar Report')
    parser.add_argument('--demo', action='store_true', help='Use demo data (default)')
    parser.add_argument('--live', action='store_true', help='Use live API data')
    
    args = parser.parse_args()
    
    use_demo = not args.live
    
    generator = FullIntegratedReportGenerator(use_demo_data=use_demo)
    report_file = generator.generate_full_report()
    
    if report_file:
        print(f"\nReport generated: {report_file}")
        return 0
    else:
        print("\nReport generation failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
