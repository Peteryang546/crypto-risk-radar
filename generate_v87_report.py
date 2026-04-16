"""
Crypto Risk Radar v8.7 Report Generator
Integrated with new risk modules:
- 5-Dimension Risk Scoring
- DeFi Protocol Risk Analysis
- Contract Vulnerability Scanning
- Risk Matrix Assessment
- Risk Heatmap Visualization
"""

import os
import sys
import json
from datetime import datetime
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

# Import new risk modules
try:
    from risk_scoring_engine import RiskScoringEngine, RiskMetrics, RiskLevel
    from defi_risk_analyzer import DeFiRiskAnalyzer, DeFiProtocol
    from contract_vulnerability_scanner import ContractVulnerabilityScanner
    from risk_matrix_calculator import RiskMatrixCalculator
    from generate_heatmap import RiskHeatmapGenerator, AssetRiskData
    RISK_MODULES_AVAILABLE = True
except ImportError as e:
    print(f"[WARNING] Risk modules not available: {e}")
    RISK_MODULES_AVAILABLE = False

# Import existing modules
try:
    from risk_math_models import RiskMathModels
    RISK_MATH_AVAILABLE = True
except ImportError:
    RISK_MATH_AVAILABLE = False


class V87ReportGenerator:
    """
    v8.7 Report Generator with integrated risk modules
    """
    
    def __init__(self):
        self.timestamp = datetime.now()
        self.risk_engine = RiskScoringEngine() if RISK_MODULES_AVAILABLE else None
        self.defi_analyzer = DeFiRiskAnalyzer() if RISK_MODULES_AVAILABLE else None
        self.contract_scanner = ContractVulnerabilityScanner() if RISK_MODULES_AVAILABLE else None
        self.matrix_calc = RiskMatrixCalculator() if RISK_MODULES_AVAILABLE else None
        self.heatmap_gen = RiskHeatmapGenerator() if RISK_MODULES_AVAILABLE else None
        
        self.assets_data = []
        self.defi_protocols = []
        self.risk_assessments = []
        
    def add_asset(self, symbol: str, price: float, market_cap: float, 
                  volume_24h: float, volatility_30d: float,
                  audited: bool = False, tvl: float = 0):
        """Add asset for risk analysis"""
        if not RISK_MODULES_AVAILABLE:
            return
            
        metrics = RiskMetrics(
            symbol=symbol,
            price=price,
            market_cap=market_cap,
            volume_24h=volume_24h,
            volatility_30d=volatility_30d,
            audited=audited,
            tvl=tvl
        )
        
        score = self.risk_engine.calculate_overall_score(metrics)
        self.assets_data.append((metrics, score))
        
        # Add to heatmap
        if self.heatmap_gen:
            from generate_heatmap import RiskLevel as HeatmapRiskLevel
            if score.overall_score <= 25:
                risk_level = HeatmapRiskLevel.LOW
            elif score.overall_score <= 50:
                risk_level = HeatmapRiskLevel.MEDIUM
            elif score.overall_score <= 75:
                risk_level = HeatmapRiskLevel.HIGH
            else:
                risk_level = HeatmapRiskLevel.CRITICAL
            
            asset_data = AssetRiskData(
                symbol=symbol,
                price=price,
                market_cap=market_cap,
                volatility=volatility_30d,
                risk_score=score.overall_score,
                risk_level=risk_level,
                var_99=0,  # Would calculate from risk_math_models
                tvl=tvl
            )
            self.heatmap_gen.add_asset(asset_data)
    
    def add_defi_protocol(self, protocol):
        """Add DeFi protocol for risk analysis"""
        if not RISK_MODULES_AVAILABLE or not self.defi_analyzer:
            return
            
        score = self.defi_analyzer.assess_protocol(protocol)
        self.defi_protocols.append((protocol, score))
    
    def generate_module_12_defi_risk(self) -> str:
        """Generate Module 12: DeFi Protocol Risk"""
        if not self.defi_protocols:
            return """
            <div class="section">
                <h2>12. DeFi Protocol Risk</h2>
                <p>No DeFi protocols analyzed in this report cycle.</p>
            </div>
            """
        
        # Sort by risk score (highest first)
        sorted_protocols = sorted(
            self.defi_protocols,
            key=lambda x: x[1].overall_risk_score,
            reverse=True
        )
        
        # High risk protocols table
        high_risk_rows = []
        for protocol, score in sorted_protocols[:5]:
            risk_color = "#ff6b6b" if score.risk_level.value in ["Dangerous", "High Risk"] else "#ffa500"
            high_risk_rows.append(f"""
                <tr>
                    <td><strong>{protocol.name}</strong></td>
                    <td>${protocol.tvl/1e6:.1f}M</td>
                    <td>{protocol.apy:.1%}</td>
                    <td style="color: {risk_color}">{score.overall_risk_score:.0f}/100</td>
                    <td>{score.risk_level.value}</td>
                    <td>{', '.join(score.red_flags[:2]) if score.red_flags else 'None'}</td>
                </tr>
            """)
        
        # Summary statistics
        dangerous = sum(1 for _, s in sorted_protocols if s.risk_level.value == "Dangerous")
        high = sum(1 for _, s in sorted_protocols if s.risk_level.value == "High Risk")
        medium = sum(1 for _, s in sorted_protocols if s.risk_level.value == "Medium Risk")
        
        # APY warnings
        high_apy_protocols = [(p, s) for p, s in sorted_protocols if p.apy > 0.50]
        apy_warnings = ""
        if high_apy_protocols:
            apy_list = ", ".join([p.name for p, _ in high_apy_protocols[:3]])
            apy_warnings = f"""
            <div style="background-color: #fff3cd; border-left: 4px solid #ffc107; padding: 15px; margin: 15px 0;">
                <strong>High APY Warning</strong>: {len(high_apy_protocols)} protocols offer APY > 50%. 
                These include: {apy_list}. 
                Extremely high yields are typically unsustainable and may indicate ponzi-like structures.
            </div>
            """
        
        html = f"""
        <div class="section">
            <h2>12. DeFi Protocol Risk</h2>
            <p><strong>Protocols Analyzed</strong>: {len(self.defi_protocols)}</p>
            <p><strong>Risk Distribution</strong>: Dangerous: {dangerous} | High: {high} | Medium: {medium}</p>
            
            {apy_warnings}
            
            <h3>High-Risk Protocols</h3>
            <table class="data-table">
                <thead>
                    <tr>
                        <th>Protocol</th>
                        <th>TVL</th>
                        <th>APY</th>
                        <th>Risk Score</th>
                        <th>Level</th>
                        <th>Red Flags</th>
                    </tr>
                </thead>
                <tbody>
                    {''.join(high_risk_rows)}
                </tbody>
            </table>
            
            <h3>Risk Assessment Methodology</h3>
            <p>DeFi protocols are assessed across 5 dimensions:</p>
            <ul>
                <li><strong>Security (30%)</strong>: Audit status, exploit history, bug bounties</li>
                <li><strong>Oracle Risk (20%)</strong>: Oracle type, diversity, TVL at risk</li>
                <li><strong>Financial (20%)</strong>: TVL stability, revenue sustainability</li>
                <li><strong>Yield Sustainability (20%)</strong>: APY vs industry average, reward ratio</li>
                <li><strong>Governance (10%)</strong>: Token concentration, timelock, multi-sig</li>
            </ul>
            
            <p style="color: #8b9dc3; font-size: 12px; margin-top: 15px;">
                <em>Note: APY > 20% without clear revenue source is considered high risk. 
                APY > 50% is considered dangerous and likely unsustainable.</em>
            </p>
        </div>
        """
        
        return html
    
    def generate_module_13_risk_heatmap(self) -> str:
        """Generate Module 13: Risk Heatmap Visualization"""
        if not self.heatmap_gen or not self.assets_data:
            return """
            <div class="section">
                <h2>13. Risk Heatmap</h2>
                <p>No asset data available for heatmap generation.</p>
            </div>
            """
        
        # Generate SVG heatmap
        svg_content = self.heatmap_gen.generate_svg_heatmap()
        
        # Generate top risk assets table
        sorted_assets = sorted(self.assets_data, key=lambda x: x[1].overall_score, reverse=True)
        
        table_rows = []
        for metrics, score in sorted_assets[:10]:
            risk_color = "#ff6b6b" if score.risk_level.value == "Critical" else \
                        "#ffa500" if score.risk_level.value == "High" else \
                        "#f1c40f" if score.risk_level.value == "Medium" else "#2ecc71"
            
            table_rows.append(f"""
                <tr>
                    <td><strong>{metrics.symbol}</strong></td>
                    <td>${metrics.price:,.2f}</td>
                    <td>${metrics.market_cap/1e9:.2f}B</td>
                    <td>{metrics.volatility_30d:.1%}</td>
                    <td style="color: {risk_color}">{score.overall_score:.0f}/100</td>
                    <td>{score.risk_level.value}</td>
                    <td>{len(score.red_flags)}</td>
                </tr>
            """)
        
        html = f"""
        <div class="section">
            <h2>13. Risk Heatmap Visualization</h2>
            <p>Interactive visualization of asset risk profiles. X-axis: Market Cap (log scale), Y-axis: Volatility, Color: Risk Score.</p>
            
            <div class="heatmap-container" style="text-align: center; margin: 20px 0; padding: 20px; background: #0f1429; border-radius: 8px;">
                {svg_content}
            </div>
            
            <h3>Top Risk Assets</h3>
            <table class="data-table">
                <thead>
                    <tr>
                        <th>Asset</th>
                        <th>Price</th>
                        <th>Market Cap</th>
                        <th>Volatility</th>
                        <th>Risk Score</th>
                        <th>Level</th>
                        <th>Red Flags</th>
                    </tr>
                </thead>
                <tbody>
                    {''.join(table_rows)}
                </tbody>
            </table>
            
            <h3>5-Dimension Risk Model</h3>
            <p>Each asset is scored across 5 dimensions with the following weights:</p>
            <ul>
                <li><strong>Market Risk (30%)</strong>: Volatility, liquidity, market cap</li>
                <li><strong>Security Risk (25%)</strong>: Audit status, exploit history</li>
                <li><strong>Financial Risk (20%)</strong>: TVL, revenue, treasury</li>
                <li><strong>Operational Risk (15%)</strong>: Team transparency, governance</li>
                <li><strong>Sentiment Risk (10%)</strong>: Social signals, news sentiment</li>
            </ul>
        </div>
        """
        
        return html
    
    def generate_risk_matrix_section(self) -> str:
        """Generate Risk Matrix Assessment section"""
        if not self.matrix_calc:
            return ""
        
        # Get predefined crypto risks
        risk_items = self.matrix_calc.get_crypto_risk_items()
        assessments = self.matrix_calc.assess_multiple(risk_items)
        
        # Sort by priority
        sorted_assessments = sorted(assessments, key=lambda x: x.risk_score, reverse=True)
        
        # Generate table rows
        table_rows = []
        for assessment in sorted_assessments[:8]:
            item = assessment.item
            priority_color = {
                "Critical": "#ff6b6b",
                "High": "#ffa500",
                "Medium": "#f1c40f",
                "Low": "#2ecc71"
            }.get(assessment.priority.value, "#888")
            
            table_rows.append(f"""
                <tr>
                    <td><strong>{item.name}</strong></td>
                    <td>{item.category}</td>
                    <td>{item.likelihood.name}</td>
                    <td>{item.impact.name}</td>
                    <td style="color: {priority_color}">{assessment.risk_score}/16</td>
                    <td>{assessment.priority.value}</td>
                </tr>
            """)
        
        # Risk matrix ASCII table
        matrix_table = self.matrix_calc.generate_risk_matrix_table()
        
        html = f"""
        <div class="section">
            <h2>Risk Matrix Assessment</h2>
            <p>Standardized risk assessment using 4x4 likelihood-impact matrix.</p>
            
            <pre style="background: #0f1429; padding: 15px; border-radius: 8px; font-size: 12px; overflow-x: auto;">
{matrix_table}
            </pre>
            
            <h3>Crypto-Specific Risk Assessment</h3>
            <table class="data-table">
                <thead>
                    <tr>
                        <th>Risk</th>
                        <th>Category</th>
                        <th>Likelihood</th>
                        <th>Impact</th>
                        <th>Score</th>
                        <th>Priority</th>
                    </tr>
                </thead>
                <tbody>
                    {''.join(table_rows)}
                </tbody>
            </table>
        </div>
        """
        
        return html
    
    def generate_integrated_report(self, output_file: str = None) -> str:
        """Generate complete v8.7 integrated report"""
        
        # Generate all modules
        module_12 = self.generate_module_12_defi_risk()
        module_13 = self.generate_module_13_risk_heatmap()
        risk_matrix = self.generate_risk_matrix_section()
        
        # Build complete HTML
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Crypto Risk Radar v8.7 - Integrated Risk Report</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #0a0e1a;
            color: #e0e6ed;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            line-height: 1.6;
        }}
        .header {{
            background: linear-gradient(135deg, #1a1f35 0%, #0f1429 100%);
            padding: 30px;
            border-radius: 12px;
            margin-bottom: 20px;
            border: 1px solid #2a3f5f;
        }}
        .header h1 {{
            margin: 0;
            color: #00d4ff;
            font-size: 28px;
        }}
        .header .meta {{
            color: #8b9dc3;
            margin-top: 10px;
        }}
        .section {{
            background: #0f1429;
            padding: 25px;
            margin-bottom: 20px;
            border-radius: 8px;
            border: 1px solid #1a2a45;
        }}
        .section h2 {{
            color: #00d4ff;
            border-bottom: 2px solid #2a3f5f;
            padding-bottom: 10px;
            margin-top: 0;
        }}
        .section h3 {{
            color: #5dade2;
            margin-top: 20px;
        }}
        .data-table {{
            width: 100%;
            border-collapse: collapse;
            margin: 15px 0;
            font-size: 14px;
        }}
        .data-table th {{
            background: #1a2a45;
            padding: 12px;
            text-align: left;
            color: #00d4ff;
            font-weight: 600;
        }}
        .data-table td {{
            padding: 10px 12px;
            border-bottom: 1px solid #1a2a45;
        }}
        .data-table tr:hover {{
            background: #1a1f35;
        }}
        .heatmap-container {{
            background: #0a0e1a;
            border-radius: 8px;
            padding: 20px;
        }}
        .disclaimer {{
            background: #1a1f35;
            border-left: 4px solid #ffc107;
            padding: 20px;
            margin-top: 30px;
            font-size: 13px;
            color: #8b9dc3;
        }}
        .badge {{
            display: inline-block;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 12px;
            font-weight: 600;
        }}
        .badge-safe {{ background: #2ecc71; color: #000; }}
        .badge-low {{ background: #f1c40f; color: #000; }}
        .badge-medium {{ background: #e67e22; color: #fff; }}
        .badge-high {{ background: #e74c3c; color: #fff; }}
        .badge-critical {{ background: #9b59b6; color: #fff; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>Crypto Risk Radar v8.7</h1>
        <div class="meta">
            Integrated Risk Intelligence Report | Generated: {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}<br>
            New: 5-Dimension Risk Scoring | DeFi Protocol Analysis | Risk Heatmap Visualization
        </div>
    </div>
    
    {module_12}
    
    {module_13}
    
    {risk_matrix}
    
    <div class="disclaimer">
        <h3>Important Disclaimers</h3>
        <p><strong>Not Financial Advice</strong>: This report is for educational and risk awareness purposes only. 
        It does not constitute investment advice, trading recommendations, or solicitation to buy/sell any asset.</p>
        
        <p><strong>Risk Scoring Limitations</strong>: Risk scores are algorithmic estimates based on available data 
        and historical patterns. They do not predict future performance or guarantee safety. Past security does not 
        ensure future security.</p>
        
        <p><strong>Data Accuracy</strong>: While we strive for accuracy, on-chain data may have delays or errors. 
        Always verify critical information through multiple sources.</p>
        
        <p><strong>DeFi Risks</strong>: DeFi protocols carry unique risks including smart contract bugs, oracle failures, 
        and governance attacks. High APY often indicates unsustainable economics or hidden risks.</p>
        
        <p><strong>Do Your Own Research</strong>: This report is a starting point for risk assessment, not a substitute 
        for independent due diligence. Never invest more than you can afford to lose.</p>
    </div>
</body>
</html>"""
        
        # Save to file
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(html)
            print(f"v8.7 report saved to: {output_file}")
        
        return html


def main():
    """Test the v8.7 report generator"""
    print("=" * 60)
    print("Crypto Risk Radar v8.7 - Integrated Report Generator")
    print("=" * 60)
    
    if not RISK_MODULES_AVAILABLE:
        print("\n[ERROR] Risk modules not available. Please ensure all modules are installed:")
        print("  - risk_scoring_engine.py")
        print("  - defi_risk_analyzer.py")
        print("  - contract_vulnerability_scanner.py")
        print("  - risk_matrix_calculator.py")
        print("  - generate_heatmap.py")
        return
    
    generator = V87ReportGenerator()
    
    # Add test assets
    print("\n[1/4] Adding assets for risk analysis...")
    test_assets = [
        ("BTC", 72000, 1.4e12, 3.5e10, 0.35, True, 0),
        ("ETH", 3600, 4.3e11, 1.5e10, 0.42, True, 5e10),
        ("SOL", 145, 6.5e10, 2.5e9, 0.65, True, 4e9),
        ("DOGE", 0.15, 2.1e10, 8e8, 0.78, False, 0),
        ("SHIB", 0.00002, 1.1e10, 4e8, 0.85, False, 0),
        ("RISKY", 0.001, 5e5, 1e4, 0.95, False, 5e5),
    ]
    
    for symbol, price, mcap, vol, volatility, audited, tvl in test_assets:
        generator.add_asset(symbol, price, mcap, vol, volatility, audited, tvl)
    
    print(f"  Added {len(test_assets)} assets")
    
    # Add test DeFi protocols
    print("\n[2/4] Adding DeFi protocols...")
    from defi_risk_analyzer import DeFiProtocol
    test_protocols = [
        DeFiProtocol(
            name="SafeYield",
            chain="ethereum",
            tvl=5e8,
            apy=0.05,
            apy_base=0.05,
            apy_reward=0.0,
            audited=True,
            auditor="Trail of Bits",
            audit_date="2024-06",
            oracle_type="chainlink",
            oracle_count=3,
            governance_token="SAFE",
            governance_tvl=2e8,
            tvl_change_24h=0.01,
            tvl_change_7d=0.05,
            revenue_24h=100000
        ),
        DeFiProtocol(
            name="RiskyFarm",
            chain="bsc",
            tvl=1e6,
            apy=1.20,  # 120% APY!
            apy_base=0.02,
            apy_reward=1.18,
            audited=False,
            auditor="",
            audit_date=None,
            oracle_type="custom",
            oracle_count=1,
            governance_token="RISKY",
            governance_tvl=5e5,
            tvl_change_24h=-0.30,
            tvl_change_7d=-0.50,
            revenue_24h=100
        ),
    ]
    
    for protocol in test_protocols:
        generator.add_defi_protocol(protocol)
    
    print(f"  Added {len(test_protocols)} protocols")
    
    # Generate report
    print("\n[3/4] Generating integrated report...")
    output_file = f"v87_integrated_report_{datetime.now().strftime('%Y%m%d_%H%M')}.html"
    html = generator.generate_integrated_report(output_file)
    
    # Print summary
    print("\n[4/4] Report Summary:")
    print(f"  Assets analyzed: {len(generator.assets_data)}")
    print(f"  DeFi protocols: {len(generator.defi_protocols)}")
    
    if generator.assets_data:
        risk_scores = [s.overall_score for _, s in generator.assets_data]
        print(f"  Avg risk score: {sum(risk_scores)/len(risk_scores):.1f}/100")
        print(f"  Highest risk: {max(generator.assets_data, key=lambda x: x[1].overall_score)[0].symbol}")
    
    print(f"\n  Output file: {output_file}")
    print(f"  File size: {len(html):,} bytes")
    
    print("\n" + "=" * 60)
    print("v8.7 report generation complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
