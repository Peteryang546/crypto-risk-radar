"""
Risk Heatmap Generator v8.7
Interactive Risk Visualization Module
Based on Crypto Report Enhanced Methodology
"""

import json
import math
from datetime import datetime
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum

class RiskLevel(Enum):
    SAFE = "Safe"
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"

@dataclass
class AssetRiskData:
    """Risk data for a single asset"""
    symbol: str
    price: float
    market_cap: float
    volatility: float  # 30-day annualized
    risk_score: float  # 0-100
    risk_level: RiskLevel
    var_99: float  # 99% VaR
    tvl: float = 0.0  # For DeFi protocols
    apy: float = 0.0

class RiskHeatmapGenerator:
    """
    Risk Heatmap Generator
    
    Creates interactive HTML heatmap showing:
    - X-axis: Market Cap (log scale)
    - Y-axis: Volatility
    - Color: Risk Score
    - Size: TVL or Volume
    """
    
    # Color scheme for risk levels (RGB)
    COLOR_SCHEME = {
        RiskLevel.SAFE: (46, 204, 113),      # Green
        RiskLevel.LOW: (241, 196, 15),       # Yellow
        RiskLevel.MEDIUM: (230, 126, 34),    # Orange
        RiskLevel.HIGH: (231, 76, 60),       # Red
        RiskLevel.CRITICAL: (142, 68, 173),  # Purple
    }
    
    def __init__(self, width: int = 800, height: int = 600):
        self.width = width
        self.height = height
        self.assets: List[AssetRiskData] = []
    
    def add_asset(self, asset: AssetRiskData):
        """Add asset to heatmap"""
        self.assets.append(asset)
    
    def get_risk_level(self, score: float) -> RiskLevel:
        """Determine risk level from score"""
        if score <= 20:
            return RiskLevel.SAFE
        elif score <= 40:
            return RiskLevel.LOW
        elif score <= 60:
            return RiskLevel.MEDIUM
        elif score <= 80:
            return RiskLevel.HIGH
        else:
            return RiskLevel.CRITICAL
    
    def get_color(self, risk_level: RiskLevel, alpha: float = 0.8) -> str:
        """Get RGBA color string for risk level"""
        r, g, b = self.COLOR_SCHEME[risk_level]
        return f"rgba({r}, {g}, {b}, {alpha})"
    
    def calculate_position(self, asset: AssetRiskData, 
                          min_cap: float, max_cap: float,
                          min_vol: float, max_vol: float) -> Tuple[int, int]:
        """
        Calculate position on heatmap
        
        X: log(market_cap) mapped to width
        Y: volatility mapped to height (inverted)
        """
        # X position (log scale for market cap)
        if min_cap > 0 and max_cap > min_cap:
            log_min = math.log10(min_cap)
            log_max = math.log10(max_cap)
            log_cap = math.log10(max(asset.market_cap, min_cap))
            x_norm = (log_cap - log_min) / (log_max - log_min)
        else:
            x_norm = 0.5
        
        x = int(50 + x_norm * (self.width - 100))  # 50px padding
        
        # Y position (volatility, inverted)
        if max_vol > min_vol:
            y_norm = (asset.volatility - min_vol) / (max_vol - min_vol)
        else:
            y_norm = 0.5
        
        y = int(self.height - 50 - y_norm * (self.height - 100))  # Inverted
        
        return x, y
    
    def calculate_size(self, asset: AssetRiskData, min_tvl: float, max_tvl: float) -> int:
        """Calculate bubble size based on TVL"""
        if max_tvl > min_tvl:
            size_norm = (asset.tvl - min_tvl) / (max_tvl - min_tvl)
        else:
            size_norm = 0.5
        
        # Size between 10 and 40 pixels
        return int(10 + size_norm * 30)
    
    def generate_svg_heatmap(self) -> str:
        """Generate SVG heatmap"""
        if not self.assets:
            return "<p>No data available</p>"
        
        # Calculate ranges
        caps = [a.market_cap for a in self.assets if a.market_cap > 0]
        vols = [a.volatility for a in self.assets]
        tvls = [a.tvl for a in self.assets]
        
        min_cap, max_cap = min(caps), max(caps)
        min_vol, max_vol = min(vols), max(vols)
        min_tvl, max_tvl = (min(tvls), max(tvls)) if tvls else (0, 1)
        
        # SVG header
        svg_parts = [
            f'<svg width="{self.width}" height="{self.height}" xmlns="http://www.w3.org/2000/svg">',
            '<defs>',
            '  <filter id="shadow" x="-20%" y="-20%" width="140%" height="140%">',
            '    <feDropShadow dx="1" dy="1" stdDeviation="2" flood-opacity="0.3"/>',
            '  </filter>',
            '</defs>',
            '<style>',
            '  .axis { stroke: #666; stroke-width: 1; }',
            '  .grid { stroke: #ddd; stroke-width: 0.5; stroke-dasharray: 5,5; }',
            '  .label { font-family: Arial, sans-serif; font-size: 12px; fill: #666; }',
            '  .title { font-family: Arial, sans-serif; font-size: 16px; font-weight: bold; fill: #333; }',
            '  .tooltip { font-family: Arial, sans-serif; font-size: 11px; }',
            '  .asset-circle { cursor: pointer; filter: url(#shadow); }',
            '  .asset-circle:hover { stroke: #333; stroke-width: 2; }',
            '</style>',
            '',
            # Background
            f'<rect width="{self.width}" height="{self.height}" fill="#fafafa"/>',
            '',
            # Title
            f'<text x="{self.width/2}" y="25" text-anchor="middle" class="title">Crypto Risk Heatmap</text>',
            f'<text x="{self.width/2}" y="45" text-anchor="middle" class="label">Market Cap vs Volatility (colored by Risk Score)</text>',
            '',
            # Grid lines
        ]
        
        # Add grid lines
        for i in range(5):
            x = 50 + i * (self.width - 100) / 4
            y = 50 + i * (self.height - 100) / 4
            svg_parts.append(f'<line x1="{x}" y1="50" x2="{x}" y2="{self.height-50}" class="grid"/>')
            svg_parts.append(f'<line x1="50" y1="{y}" x2="{self.width-50}" y2="{y}" class="grid"/>')
        
        # Axes
        svg_parts.extend([
            f'<line x1="50" y1="{self.height-50}" x2="{self.width-50}" y2="{self.height-50}" class="axis"/>',
            f'<line x1="50" y1="50" x2="50" y2="{self.height-50}" class="axis"/>',
            '',
            # Axis labels
            f'<text x="{self.width/2}" y="{self.height-15}" text-anchor="middle" class="label">Market Cap (log scale)</text>',
            f'<text x="15" y="{self.height/2}" text-anchor="middle" transform="rotate(-90, 15, {self.height/2})" class="label">Volatility (%)</text>',
            '',
        ])
        
        # Add axis tick labels
        for i in range(5):
            # X-axis (market cap)
            x = 50 + i * (self.width - 100) / 4
            if min_cap > 0 and max_cap > min_cap:
                log_val = math.log10(min_cap) + i * (math.log10(max_cap) - math.log10(min_cap)) / 4
                cap_val = 10 ** log_val
                if cap_val >= 1e9:
                    label = f"${cap_val/1e9:.0f}B"
                elif cap_val >= 1e6:
                    label = f"${cap_val/1e6:.0f}M"
                else:
                    label = f"${cap_val:.0f}"
            else:
                label = ""
            svg_parts.append(f'<text x="{x}" y="{self.height-35}" text-anchor="middle" class="label">{label}</text>')
            
            # Y-axis (volatility)
            y = self.height - 50 - i * (self.height - 100) / 4
            vol_val = min_vol + i * (max_vol - min_vol) / 4
            svg_parts.append(f'<text x="35" y="{y+4}" text-anchor="end" class="label">{vol_val:.0%}</text>')
        
        svg_parts.append('')
        
        # Add asset circles
        for asset in self.assets:
            x, y = self.calculate_position(asset, min_cap, max_cap, min_vol, max_vol)
            size = self.calculate_size(asset, min_tvl, max_tvl)
            color = self.get_color(asset.risk_level)
            
            # Tooltip content
            tooltip = f"{asset.symbol}: Risk {asset.risk_score:.0f}/100, Vol {asset.volatility:.1%}, Cap ${asset.market_cap/1e9:.1f}B"
            
            svg_parts.append(f'  <circle cx="{x}" cy="{y}" r="{size/2}" fill="{color}" stroke="white" stroke-width="1" class="asset-circle">')
            svg_parts.append(f'    <title>{tooltip}</title>')
            svg_parts.append(f'  </circle>')
            
            # Label for larger assets
            if asset.market_cap > 1e10:  # > $10B
                svg_parts.append(f'  <text x="{x}" y="{y+4}" text-anchor="middle" class="label" font-size="10" fill="white" pointer-events="none">{asset.symbol}</text>')
        
        # Legend
        legend_x = self.width - 150
        legend_y = 70
        svg_parts.extend([
            '',
            f'<rect x="{legend_x-10}" y="{legend_y-20}" width="140" height="140" fill="white" stroke="#ddd" rx="5"/>',
            f'<text x="{legend_x}" y="{legend_y}" class="label" font-weight="bold">Risk Level</text>',
        ])
        
        for i, level in enumerate(RiskLevel):
            y = legend_y + 20 + i * 20
            color = self.get_color(level)
            svg_parts.append(f'<circle cx="{legend_x+10}" cy="{y}" r="8" fill="{color}"/>')
            svg_parts.append(f'<text x="{legend_x+25}" y="{y+4}" class="label">{level.value}</text>')
        
        svg_parts.append('</svg>')
        
        return '\n'.join(svg_parts)
    
    def generate_html_report(self, title: str = "Risk Heatmap Report") -> str:
        """Generate complete HTML report with heatmap"""
        svg_content = self.generate_svg_heatmap()
        
        # Generate asset table
        table_rows = []
        sorted_assets = sorted(self.assets, key=lambda a: a.risk_score, reverse=True)
        
        for asset in sorted_assets[:10]:  # Top 10 by risk
            risk_color = self.get_color(asset.risk_level)
            table_rows.append(f"""
            <tr>
                <td><strong>{asset.symbol}</strong></td>
                <td>${asset.price:,.2f}</td>
                <td>${asset.market_cap/1e9:.2f}B</td>
                <td>{asset.volatility:.1%}</td>
                <td><span style="color: {risk_color}">{asset.risk_score:.0f}/100</span></td>
                <td>{asset.risk_level.value}</td>
                <td>{asset.var_99:.2%}</td>
            </tr>
            """)
        
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background: #f5f5f5;
        }}
        .container {{
            background: white;
            border-radius: 8px;
            padding: 30px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #333;
            border-bottom: 2px solid #3498db;
            padding-bottom: 10px;
        }}
        .heatmap-container {{
            text-align: center;
            margin: 30px 0;
            padding: 20px;
            background: #fafafa;
            border-radius: 8px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }}
        th, td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }}
        th {{
            background: #3498db;
            color: white;
            font-weight: 600;
        }}
        tr:hover {{
            background: #f5f5f5;
        }}
        .timestamp {{
            color: #666;
            font-size: 14px;
            margin-top: 20px;
        }}
        .disclaimer {{
            background: #fff3cd;
            border-left: 4px solid #ffc107;
            padding: 15px;
            margin-top: 20px;
            font-size: 14px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>{title}</h1>
        <p class="timestamp">Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        
        <div class="heatmap-container">
            {svg_content}
        </div>
        
        <h2>Top Risk Assets</h2>
        <table>
            <thead>
                <tr>
                    <th>Asset</th>
                    <th>Price</th>
                    <th>Market Cap</th>
                    <th>Volatility</th>
                    <th>Risk Score</th>
                    <th>Risk Level</th>
                    <th>99% VaR</th>
                </tr>
            </thead>
            <tbody>
                {''.join(table_rows)}
            </tbody>
        </table>
        
        <div class="disclaimer">
            <strong>Disclaimer:</strong> This risk assessment is for educational purposes only. 
            Risk scores are algorithmic estimates based on available data. 
            Past performance does not guarantee future results. 
            Always conduct your own research before making investment decisions.
        </div>
    </div>
</body>
</html>"""
        
        return html
    
    def save_html(self, filename: str, title: str = "Risk Heatmap Report"):
        """Save HTML report to file"""
        html = self.generate_html_report(title)
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"Heatmap saved to: {filename}")


def main():
    """Test the heatmap generator"""
    generator = RiskHeatmapGenerator(width=900, height=600)
    
    # Add test assets
    test_assets = [
        AssetRiskData("BTC", 72000, 1.4e12, 0.35, 33, RiskLevel.MEDIUM, -0.0131, 0, 0),
        AssetRiskData("ETH", 3600, 4.3e11, 0.42, 38, RiskLevel.MEDIUM, -0.0193, 5e10, 0),
        AssetRiskData("SOL", 145, 6.5e10, 0.65, 52, RiskLevel.MEDIUM, -0.028, 4e9, 0),
        AssetRiskData("DOGE", 0.15, 2.1e10, 0.78, 61, RiskLevel.HIGH, -0.035, 0, 0),
        AssetRiskData("SHIB", 0.00002, 1.1e10, 0.85, 68, RiskLevel.HIGH, -0.042, 0, 0),
        AssetRiskData("RISKY", 0.001, 5e5, 0.95, 85, RiskLevel.CRITICAL, -0.055, 5e5, 1.20),
        AssetRiskData("SAFEPROTO", 10, 5e8, 0.25, 22, RiskLevel.LOW, -0.008, 2e8, 0.05),
        AssetRiskData("MIDCAP", 5, 5e9, 0.55, 48, RiskLevel.MEDIUM, -0.025, 1e9, 0),
    ]
    
    for asset in test_assets:
        generator.add_asset(asset)
    
    # Generate and save HTML
    generator.save_html("risk_heatmap_test.html", "Crypto Risk Heatmap v8.7")
    
    print("\nHeatmap generation complete!")
    print(f"Assets plotted: {len(generator.assets)}")
    
    # Print summary
    risk_counts = {}
    for asset in generator.assets:
        level = asset.risk_level.value
        risk_counts[level] = risk_counts.get(level, 0) + 1
    
    print("\nRisk Distribution:")
    for level, count in sorted(risk_counts.items()):
        print(f"  {level}: {count}")


if __name__ == "__main__":
    main()
