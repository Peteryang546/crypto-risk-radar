#!/usr/bin/env python3
"""
Widget Generator
Creates embeddable risk dashboard widget
"""

from datetime import datetime
from pathlib import Path

OUTPUT_DIR = Path(r'F:\stepclaw\agents\blockchain-analyst\output')


def generate_widget_html():
    """Generate embeddable widget HTML"""
    
    widget_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Crypto Risk Radar Widget</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; }
        
        .crr-widget {
            width: 100%;
            max-width: 400px;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            border-radius: 12px;
            padding: 20px;
            color: #fff;
            box-shadow: 0 4px 20px rgba(0,0,0,0.3);
        }
        
        .crr-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 15px;
            padding-bottom: 15px;
            border-bottom: 1px solid rgba(255,255,255,0.1);
        }
        
        .crr-title {
            font-size: 16px;
            font-weight: 600;
            color: #00d4ff;
        }
        
        .crr-live {
            font-size: 11px;
            color: #4ade80;
            display: flex;
            align-items: center;
            gap: 5px;
        }
        
        .crr-live::before {
            content: '';
            width: 6px;
            height: 6px;
            background: #4ade80;
            border-radius: 50%;
            animation: pulse 2s infinite;
        }
        
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }
        
        .crr-risk-score {
            text-align: center;
            padding: 20px 0;
        }
        
        .crr-score-value {
            font-size: 48px;
            font-weight: 700;
            line-height: 1;
        }
        
        .crr-score-label {
            font-size: 14px;
            color: #8b9dc3;
            margin-top: 5px;
        }
        
        .crr-score-low { color: #4ade80; }
        .crr-score-medium { color: #fbbf24; }
        .crr-score-high { color: #f87171; }
        
        .crr-metrics {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 10px;
            margin-top: 15px;
        }
        
        .crr-metric {
            background: rgba(255,255,255,0.05);
            padding: 12px;
            border-radius: 8px;
            text-align: center;
        }
        
        .crr-metric-value {
            font-size: 18px;
            font-weight: 600;
            color: #fff;
        }
        
        .crr-metric-label {
            font-size: 11px;
            color: #8b9dc3;
            margin-top: 3px;
        }
        
        .crr-footer {
            margin-top: 15px;
            padding-top: 15px;
            border-top: 1px solid rgba(255,255,255,0.1);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .crr-timestamp {
            font-size: 11px;
            color: #8b9dc3;
        }
        
        .crr-link {
            font-size: 11px;
            color: #00d4ff;
            text-decoration: none;
        }
        
        .crr-link:hover {
            text-decoration: underline;
        }
        
        /* Token-specific styles */
        .crr-token-select {
            width: 100%;
            padding: 8px 12px;
            margin-bottom: 15px;
            background: rgba(255,255,255,0.1);
            border: 1px solid rgba(255,255,255,0.2);
            border-radius: 6px;
            color: #fff;
            font-size: 14px;
            cursor: pointer;
        }
        
        .crr-token-select option {
            background: #1a1a2e;
            color: #fff;
        }
        
        .crr-token-info {
            display: none;
        }
        
        .crr-token-info.active {
            display: block;
        }
    </style>
</head>
<body>
    <div class="crr-widget">
        <div class="crr-header">
            <span class="crr-title">🔴 Risk Radar</span>
            <span class="crr-live">LIVE</span>
        </div>
        
        <select class="crr-token-select" id="tokenSelect" onchange="updateToken()">
            <option value="market">Overall Market</option>
            <option value="BTC">Bitcoin (BTC)</option>
            <option value="ETH">Ethereum (ETH)</option>
            <option value="DOGE">Dogecoin (DOGE)</option>
        </select>
        
        <!-- Market View -->
        <div class="crr-token-info active" id="market-view">
            <div class="crr-risk-score">
                <div class="crr-score-value crr-score-low" id="marketScore">35</div>
                <div class="crr-score-label">Market Risk Score</div>
            </div>
            
            <div class="crr-metrics">
                <div class="crr-metric">
                    <div class="crr-metric-value" id="btcPrice">$74.5K</div>
                    <div class="crr-metric-label">BTC</div>
                </div>
                <div class="crr-metric">
                    <div class="crr-metric-value" id="ethPrice">$2.37K</div>
                    <div class="crr-metric-label">ETH</div>
                </div>
                <div class="crr-metric">
                    <div class="crr-metric-value" id="threats">2</div>
                    <div class="crr-metric-label">Threats</div>
                </div>
                <div class="crr-metric">
                    <div class="crr-metric-value" id="unlocks">10</div>
                    <div class="crr-metric-label">Unlocks</div>
                </div>
            </div>
        </div>
        
        <!-- BTC View -->
        <div class="crr-token-info" id="BTC-view">
            <div class="crr-risk-score">
                <div class="crr-score-value crr-score-low">25</div>
                <div class="crr-score-label">BTC Risk Score</div>
            </div>
            
            <div class="crr-metrics">
                <div class="crr-metric">
                    <div class="crr-metric-value">$74.5K</div>
                    <div class="crr-metric-label">Price</div>
                </div>
                <div class="crr-metric">
                    <div class="crr-metric-value crr-score-low">+5.0%</div>
                    <div class="crr-metric-label">24h</div>
                </div>
                <div class="crr-metric">
                    <div class="crr-metric-value">Low</div>
                    <div class="crr-metric-label">Volatility</div>
                </div>
                <div class="crr-metric">
                    <div class="crr-metric-value">0</div>
                    <div class="crr-metric-label">Alerts</div>
                </div>
            </div>
        </div>
        
        <!-- ETH View -->
        <div class="crr-token-info" id="ETH-view">
            <div class="crr-risk-score">
                <div class="crr-score-value crr-score-low">30</div>
                <div class="crr-score-label">ETH Risk Score</div>
            </div>
            
            <div class="crr-metrics">
                <div class="crr-metric">
                    <div class="crr-metric-value">$2.37K</div>
                    <div class="crr-metric-label">Price</div>
                </div>
                <div class="crr-metric">
                    <div class="crr-metric-value crr-score-low">+8.0%</div>
                    <div class="crr-metric-label">24h</div>
                </div>
                <div class="crr-metric">
                    <div class="crr-metric-value">Low</div>
                    <div class="crr-metric-label">Volatility</div>
                </div>
                <div class="crr-metric">
                    <div class="crr-metric-value">0</div>
                    <div class="crr-metric-label">Alerts</div>
                </div>
            </div>
        </div>
        
        <!-- DOGE View -->
        <div class="crr-token-info" id="DOGE-view">
            <div class="crr-risk-score">
                <div class="crr-score-value crr-score-medium">55</div>
                <div class="crr-score-label">DOGE Risk Score</div>
            </div>
            
            <div class="crr-metrics">
                <div class="crr-metric">
                    <div class="crr-metric-value">$0.16</div>
                    <div class="crr-metric-label">Price</div>
                </div>
                <div class="crr-metric">
                    <div class="crr-metric-value crr-score-medium">+3.2%</div>
                    <div class="crr-metric-label">24h</div>
                </div>
                <div class="crr-metric">
                    <div class="crr-metric-value">Med</div>
                    <div class="crr-metric-label">Social Hype</div>
                </div>
                <div class="crr-metric">
                    <div class="crr-metric-value">1</div>
                    <div class="crr-metric-label">Alerts</div>
                </div>
            </div>
        </div>
        
        <div class="crr-footer">
            <span class="crr-timestamp" id="timestamp">Updated: 2026-04-14 08:25 ET</span>
            <a href="https://peteryang546.github.io/crypto-risk-radar/" target="_blank" class="crr-link">Full Report →</a>
        </div>
    </div>
    
    <script>
        function updateToken() {
            const select = document.getElementById('tokenSelect');
            const token = select.value;
            
            // Hide all views
            document.querySelectorAll('.crr-token-info').forEach(el => {
                el.classList.remove('active');
            });
            
            // Show selected view
            const view = document.getElementById(token + '-view');
            if (view) {
                view.classList.add('active');
            }
        }
        
        // Auto-refresh every 5 minutes
        setInterval(function() {
            fetch('https://peteryang546.github.io/crypto-risk-radar/output/latest.json')
                .then(r => r.json())
                .then(data => {
                    document.getElementById('marketScore').textContent = data.risk_score;
                    document.getElementById('btcPrice').textContent = '$' + (data.btc_price / 1000).toFixed(1) + 'K';
                    document.getElementById('ethPrice').textContent = '$' + (data.eth_price / 1000).toFixed(2) + 'K';
                    document.getElementById('threats').textContent = data.threats_detected;
                    document.getElementById('unlocks').textContent = data.token_unlocks;
                    document.getElementById('timestamp').textContent = 'Updated: ' + data.timestamp;
                })
                .catch(e => console.log('Refresh failed:', e));
        }, 300000);
    </script>
</body>
</html>"""
    
    return widget_html


def generate_widget_embed_code():
    """Generate embed code for websites"""
    
    embed_code = """<!-- Crypto Risk Radar Widget -->
<iframe 
    src="https://peteryang546.github.io/crypto-risk-radar/widget.html" 
    width="400" 
    height="320" 
    frameborder="0" 
    style="border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.3);">
</iframe>

<!-- Or use JavaScript for more control -->
<div id="crr-widget-container"></div>
<script>
    (function() {
        var container = document.getElementById('crr-widget-container');
        var iframe = document.createElement('iframe');
        iframe.src = 'https://peteryang546.github.io/crypto-risk-radar/widget.html?token=BTC';
        iframe.width = '400';
        iframe.height = '320';
        iframe.frameBorder = '0';
        iframe.style.borderRadius = '12px';
        iframe.style.boxShadow = '0 4px 20px rgba(0,0,0,0.3)';
        container.appendChild(iframe);
    })();
</script>

<!-- Powered by Crypto Risk Radar -->
<p style="font-size: 11px; color: #666; margin-top: 5px;">
    Risk data by <a href="https://peteryang546.github.io/crypto-risk-radar/" target="_blank">Crypto Risk Radar</a>
</p>"""
    
    return embed_code


def save_widget():
    """Save widget files"""
    
    # Save widget HTML
    widget_path = OUTPUT_DIR / 'widget.html'
    with open(widget_path, 'w', encoding='utf-8') as f:
        f.write(generate_widget_html())
    print(f"[OK] Widget saved: {widget_path}")
    
    # Save embed code
    embed_path = OUTPUT_DIR / 'widget-embed.txt'
    with open(embed_path, 'w', encoding='utf-8') as f:
        f.write(generate_widget_embed_code())
    print(f"[OK] Embed code saved: {embed_path}")
    
    return widget_path, embed_path


if __name__ == "__main__":
    print("="*70)
    print("GENERATING WIDGET")
    print("="*70)
    
    save_widget()
    
    print("\n" + "="*70)
    print("Widget URLs:")
    print("  /widget.html - Embeddable widget")
    print("  /widget-embed.txt - Copy-paste embed code")
    print("\nEmbed in any website:")
    print("  <iframe src='https://peteryang546.github.io/crypto-risk-radar/widget.html' width='400' height='320'></iframe>")
    print("="*70)
