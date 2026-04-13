#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module 4: On-Chain Data Visualization
生成交易所净流入/流出、价格趋势等可视化图表
"""

import json
import base64
import io
from datetime import datetime, timedelta
from pathlib import Path

# 尝试导入 matplotlib
try:
    import matplotlib
    matplotlib.use('Agg')  # 无图形界面后端
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    print("[WARNING] matplotlib not available, using fallback mode")
    MATPLOTLIB_AVAILABLE = False


class ChartGenerator:
    """图表生成器"""
    
    def __init__(self, use_demo_data=True):
        self.use_demo_data = use_demo_data
        self.style_config = {
            'background_color': '#0a0e27',
            'figure_color': '#1a1f3a',
            'text_color': '#ffffff',
            'accent_color': '#00d4ff',
            'positive_color': '#00d4ff',  # 青色
            'negative_color': '#ff6b6b',  # 红色
            'grid_color': '#2a3f5f',
            'line_color': '#00d4ff'
        }
    
    def _get_demo_netflow_data(self):
        """获取演示数据 - 交易所净流入"""
        dates = []
        values = []
        
        # 生成过去7天的数据
        for i in range(7, 0, -1):
            date = datetime.now() - timedelta(days=i)
            dates.append(date.strftime('%m/%d'))
        
        # 模拟净流入数据（正值=流入，负值=流出）
        values = [1200, -800, 3500, 2800, -1200, 5200, 6800]
        
        return dates, values
    
    def _get_demo_price_data(self):
        """获取演示数据 - 价格走势"""
        dates = []
        prices = []
        volumes = []
        
        base_price = 65000
        for i in range(30, 0, -1):
            date = datetime.now() - timedelta(days=i)
            dates.append(date.strftime('%m/%d'))
            
            # 模拟价格波动
            change = (i % 7 - 3) * 500 + (i % 3) * 200
            prices.append(base_price + change)
            
            # 模拟交易量
            volumes.append(20000 + (i % 5) * 5000)
        
        return dates, prices, volumes
    
    def _get_demo_fear_greed_data(self):
        """获取演示数据 - 恐惧贪婪指数"""
        dates = []
        values = []
        
        for i in range(30, 0, -1):
            date = datetime.now() - timedelta(days=i)
            dates.append(date.strftime('%m/%d'))
            
            # 模拟恐惧贪婪指数（0-100）
            base = 45
            change = (i % 10 - 5) * 3
            values.append(max(0, min(100, base + change)))
        
        return dates, values
    
    def _setup_matplotlib_style(self):
        """设置 matplotlib 样式"""
        if not MATPLOTLIB_AVAILABLE:
            return
        
        plt.rcParams['figure.facecolor'] = self.style_config['background_color']
        plt.rcParams['axes.facecolor'] = self.style_config['figure_color']
        plt.rcParams['axes.edgecolor'] = self.style_config['grid_color']
        plt.rcParams['axes.labelcolor'] = self.style_config['text_color']
        plt.rcParams['text.color'] = self.style_config['text_color']
        plt.rcParams['xtick.color'] = self.style_config['text_color']
        plt.rcParams['ytick.color'] = self.style_config['text_color']
        plt.rcParams['grid.color'] = self.style_config['grid_color']
        plt.rcParams['grid.alpha'] = 0.3
    
    def generate_netflow_chart(self, dates=None, values=None, title="Exchange Netflow (7d)"):
        """
        生成交易所净流入/流出图表
        
        Args:
            dates: 日期列表
            values: 净流入值列表（正值=流入，负值=流出）
            title: 图表标题
            
        Returns:
            str: base64 编码的图片或 HTML 表格
        """
        if dates is None or values is None:
            dates, values = self._get_demo_netflow_data()
        
        if MATPLOTLIB_AVAILABLE:
            return self._generate_netflow_chart_matplotlib(dates, values, title)
        else:
            return self._generate_netflow_chart_html(dates, values, title)
    
    def _generate_netflow_chart_matplotlib(self, dates, values, title):
        """使用 matplotlib 生成图表"""
        self._setup_matplotlib_style()
        
        fig, ax = plt.subplots(figsize=(10, 5))
        
        # 根据正负值设置颜色
        colors = [self.style_config['negative_color'] if v > 0 else self.style_config['positive_color'] 
                  for v in values]
        
        # 绘制柱状图
        bars = ax.bar(dates, values, color=colors, alpha=0.8, edgecolor='none')
        
        # 添加零线
        ax.axhline(y=0, color=self.style_config['text_color'], linestyle='-', linewidth=1)
        
        # 设置标题和标签
        ax.set_title(title, fontsize=14, fontweight='bold', color=self.style_config['accent_color'])
        ax.set_ylabel('Netflow (BTC)', fontsize=11)
        ax.set_xlabel('Date', fontsize=11)
        
        # 添加网格
        ax.grid(axis='y', linestyle='--', alpha=0.3)
        ax.set_axisbelow(True)
        
        # 添加数值标签
        for bar, val in zip(bars, values):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2, 
                   height + (100 if height > 0 else -300),
                   f'{val:+,}',
                   ha='center', va='bottom' if height > 0 else 'top',
                   fontsize=9, color=self.style_config['text_color'])
        
        # 添加图例
        from matplotlib.patches import Patch
        legend_elements = [
            Patch(facecolor=self.style_config['negative_color'], label='Inflow (Risk+)'),
            Patch(facecolor=self.style_config['positive_color'], label='Outflow (Risk-)')
        ]
        ax.legend(handles=legend_elements, loc='upper left', 
                 facecolor=self.style_config['figure_color'],
                 edgecolor=self.style_config['grid_color'])
        
        plt.tight_layout()
        
        # 转换为 base64
        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight', 
                   facecolor=self.style_config['background_color'])
        buf.seek(0)
        img_base64 = base64.b64encode(buf.read()).decode('utf-8')
        plt.close()
        
        return f'<img src="data:image/png;base64,{img_base64}" alt="{title}" style="max-width:100%;" />'
    
    def _generate_netflow_chart_html(self, dates, values, title):
        """使用 HTML 表格作为回退"""
        html = f"""<div class="chart-container">
<h3>{title}</h3>
<table class="chart-table">
<thead>
<tr>
<th>Date</th>
<th>Netflow (BTC)</th>
<th>Trend</th>
</tr>
</thead>
<tbody>
"""
        for date, val in zip(dates, values):
            trend = "📈 Inflow" if val > 0 else "📉 Outflow"
            color = "#ff6b6b" if val > 0 else "#00d4ff"
            html += f"""<tr>
<td>{date}</td>
<td style="color:{color}">{val:+,}</td>
<td>{trend}</td>
</tr>
"""
        
        html += """</tbody>
</table>
<p><em>Exchange netflow data: Positive = Inflow (selling pressure), Negative = Outflow (accumulation)</em></p>
</div>"""
        
        return html
    
    def generate_fear_greed_gauge(self, value=None):
        """
        生成恐惧贪婪指数仪表盘
        
        Args:
            value: 当前恐惧贪婪指数值 (0-100)
            
        Returns:
            str: HTML 格式的仪表盘
        """
        if value is None:
            value = 45  # 默认值
        
        # 确定等级
        if value <= 20:
            level = "Extreme Fear"
            color = "#ff0000"
            emoji = "😱"
        elif value <= 40:
            level = "Fear"
            color = "#ff6b6b"
            emoji = "😰"
        elif value <= 60:
            level = "Neutral"
            color = "#ffd93d"
            emoji = "😐"
        elif value <= 80:
            level = "Greed"
            color = "#6bcf7f"
            emoji = "😏"
        else:
            level = "Extreme Greed"
            color = "#00ff00"
            emoji = "🤑"
        
        # 计算进度条位置
        percentage = value
        
        html = f"""<div class="fear-greed-gauge">
<h3>Fear & Greed Index {emoji}</h3>
<div class="gauge-container" style="background: linear-gradient(to right, #ff0000 0%, #ff6b6b 20%, #ffd93d 40%, #6bcf7f 80%, #00ff00 100%); height: 30px; border-radius: 15px; position: relative; margin: 20px 0;">
<div class="gauge-marker" style="position: absolute; left: {percentage}%; transform: translateX(-50%); top: -10px; width: 4px; height: 50px; background: #ffffff; border-radius: 2px; box-shadow: 0 0 10px rgba(255,255,255,0.5);"></div>
</div>
<div class="gauge-labels" style="display: flex; justify-content: space-between; font-size: 12px; color: #8b9dc3;">
<span>Extreme Fear</span>
<span>Fear</span>
<span>Neutral</span>
<span>Greed</span>
<span>Extreme Greed</span>
</div>
<div class="gauge-value" style="text-align: center; margin-top: 15px;">
<span style="font-size: 48px; font-weight: bold; color: {color};">{value}</span>
<p style="font-size: 18px; color: {color}; margin-top: 5px;">{level}</p>
</div>
</div>"""
        
        return html
    
    def generate_market_overview_html(self, data=None):
        """
        生成市场概览 HTML
        
        Args:
            data: 市场数据字典
            
        Returns:
            str: HTML 格式的市场概览
        """
        if data is None:
            data = {
                'btc_price': 67500,
                'btc_change_24h': 2.5,
                'eth_price': 3450,
                'eth_change_24h': -1.2,
                'total_market_cap': 2.45,
                'market_cap_change': 1.8,
                'fear_greed': 45,
                'btc_dominance': 52.3
            }
        
        html = """<div class="market-overview">
<h3>📊 Market Overview</h3>
<div class="overview-grid" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin: 20px 0;">
"""
        
        # BTC
        btc_color = "#00d4ff" if data['btc_change_24h'] >= 0 else "#ff6b6b"
        btc_arrow = "▲" if data['btc_change_24h'] >= 0 else "▼"
        html += f"""<div class="overview-card" style="background: #0f1429; padding: 15px; border-radius: 8px; border: 1px solid #2a3f5f;">
<h4 style="color: #8b9dc3; margin-bottom: 8px;">Bitcoin</h4>
<p style="font-size: 24px; font-weight: bold; margin: 5px 0;">${data['btc_price']:,}</p>
<p style="color: {btc_color}; font-size: 14px;">{btc_arrow} {abs(data['btc_change_24h']):.1f}% (24h)</p>
</div>
"""
        
        # ETH
        eth_color = "#00d4ff" if data['eth_change_24h'] >= 0 else "#ff6b6b"
        eth_arrow = "▲" if data['eth_change_24h'] >= 0 else "▼"
        html += f"""<div class="overview-card" style="background: #0f1429; padding: 15px; border-radius: 8px; border: 1px solid #2a3f5f;">
<h4 style="color: #8b9dc3; margin-bottom: 8px;">Ethereum</h4>
<p style="font-size: 24px; font-weight: bold; margin: 5px 0;">${data['eth_price']:,}</p>
<p style="color: {eth_color}; font-size: 14px;">{eth_arrow} {abs(data['eth_change_24h']):.1f}% (24h)</p>
</div>
"""
        
        # Market Cap
        mc_color = "#00d4ff" if data['market_cap_change'] >= 0 else "#ff6b6b"
        mc_arrow = "▲" if data['market_cap_change'] >= 0 else "▼"
        html += f"""<div class="overview-card" style="background: #0f1429; padding: 15px; border-radius: 8px; border: 1px solid #2a3f5f;">
<h4 style="color: #8b9dc3; margin-bottom: 8px;">Total Market Cap</h4>
<p style="font-size: 24px; font-weight: bold; margin: 5px 0;">${data['total_market_cap']:.2f}T</p>
<p style="color: {mc_color}; font-size: 14px;">{mc_arrow} {abs(data['market_cap_change']):.1f}% (24h)</p>
</div>
"""
        
        # BTC Dominance
        html += f"""<div class="overview-card" style="background: #0f1429; padding: 15px; border-radius: 8px; border: 1px solid #2a3f5f;">
<h4 style="color: #8b9dc3; margin-bottom: 8px;">BTC Dominance</h4>
<p style="font-size: 24px; font-weight: bold; margin: 5px 0;">{data['btc_dominance']:.1f}%</p>
<p style="color: #8b9dc3; font-size: 14px;">Market Share</p>
</div>
"""
        
        html += """</div>
</div>"""
        
        # 添加恐惧贪婪指数
        html += self.generate_fear_greed_gauge(data.get('fear_greed', 45))
        
        return html
    
    def generate_all_charts(self):
        """生成所有图表"""
        charts = {}
        
        # 交易所净流入图表
        charts['netflow'] = self.generate_netflow_chart()
        
        # 市场概览
        charts['overview'] = self.generate_market_overview_html()
        
        return charts


def main():
    """主函数 - 用于测试"""
    print("=" * 70)
    print("CHART GENERATOR")
    print("=" * 70)
    
    generator = ChartGenerator(use_demo_data=True)
    
    # 生成交易所净流入图表
    print("\n[1] Generating Exchange Netflow Chart...")
    netflow_chart = generator.generate_netflow_chart()
    print(f"    Generated (length: {len(netflow_chart)} chars)")
    
    # 生成市场概览
    print("\n[2] Generating Market Overview...")
    overview = generator.generate_market_overview_html()
    print(f"    Generated (length: {len(overview)} chars)")
    
    # 生成恐惧贪婪指数
    print("\n[3] Generating Fear & Greed Gauge...")
    fear_greed = generator.generate_fear_greed_gauge(45)
    print(f"    Generated (length: {len(fear_greed)} chars)")
    
    print("\n" + "=" * 70)
    print("ALL CHARTS GENERATED")
    print("=" * 70)
    
    # 显示预览
    print("\n[Preview] Fear & Greed Gauge HTML:")
    print(fear_greed[:500] + "...")


if __name__ == "__main__":
    main()
