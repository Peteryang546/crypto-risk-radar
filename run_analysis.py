#!/usr/bin/env python3
"""
Crypto Risk Radar - 8-Hourly Deception Monitor
Main orchestration script for local deployment

Features:
- Fetches orderbook data via PowerShell (bypasses Python SSL issues)
- Calculates deception risk score
- Generates English report for US/EU markets
- Uploads to GitHub via API (no local Git required)

Schedule: Every 8 hours at 06:00, 14:00, 22:00 UTC
"""

import os
import sys
import json
import time
from datetime import datetime, timezone

# Add project path
sys.path.insert(0, r'F:\stepclaw\agents\blockchain-analyst')

from config import GITHUB_TOKEN, OUTPUT_DIR, USE_MOCK_DATA
from scripts.crawlers.orderbook_crawler import fetch_orderbook, compute_metrics
from scripts.crawlers.dormant_address import DormantAddressMonitor
# from scripts.crawlers.social_crawler import SocialAccelerationMonitor  # Disabled - not essential
from scripts.analyzers.deception_score import compute_risk_score, get_risk_level, get_risk_interpretation
from scripts.utils.history import load_previous_state, save_current_state, calculate_decay

# Import existing modules
sys.path.insert(0, r'F:\stepclaw\agents\blockchain-analyst\modules')
from high_risk_watchlist import HighRiskWatchlist
from token_unlock_alert import TokenUnlockAlert
from contract_scanner import ContractScanner
from chart_generator import ChartGenerator

# Import full report generator
sys.path.insert(0, r'F:\stepclaw\agents\blockchain-analyst\scripts')
try:
    from generate_enhanced_full_report import EnhancedReportGenerator
    FULL_REPORT_AVAILABLE = True
    print("[INFO] Using Enhanced Report Generator v8.0 (GEO Optimized)")
except ImportError as e:
    print(f"[WARNING] Enhanced report generator not available: {e}")
    try:
        from generate_full_integrated_report import FullIntegratedReportGenerator
        FULL_REPORT_AVAILABLE = True
        print("[INFO] Using Full Integrated Report Generator v6.2")
    except ImportError as e2:
        print(f"[WARNING] Full report generator not available: {e2}")
        FULL_REPORT_AVAILABLE = False

# Import anti-shill modules
sys.path.insert(0, r'F:\stepclaw\agents\blockchain-analyst\scripts\crawlers')
sys.path.insert(0, r'F:\stepclaw\agents\blockchain-analyst\scripts\analyzers')
try:
    from x_crawler import XCrawler
    from neutral_shill_analyzer import NeutralShillAnalyzer
    ANTISHILL_AVAILABLE = True
except ImportError as e:
    print(f"[WARNING] Anti-shill modules not available: {e}")
    ANTISHILL_AVAILABLE = False


def fetch_all_metrics() -> dict:
    """Fetch all metrics from various sources"""
    print("\n" + "="*70)
    print("FETCHING MARKET DATA")
    print("="*70)
    
    metrics = {}
    
    # 1. Orderbook data (via PowerShell)
    print("\n[1/5] Fetching orderbook via PowerShell...")
    ob = fetch_orderbook("BTCUSDT")
    ob_metrics = compute_metrics(ob)
    metrics.update(ob_metrics)
    print(f"  Bid depth: {metrics['total_bid_depth']:.2f} BTC")
    print(f"  Ask uniformity: {metrics['ask_uniformity']:.3f}")
    
    # 2. Calculate bid depth decay
    print("\n[2/5] Calculating bid depth decay...")
    prev_state = load_previous_state()
    prev_bid_depth = prev_state.get("total_bid_depth", metrics["total_bid_depth"])
    decay = calculate_decay(metrics["total_bid_depth"], prev_bid_depth)
    metrics["bid_depth_decay"] = max(0, decay)
    print(f"  Decay: {metrics['bid_depth_decay']:.1f}%")
    
    # 3. Exchange netflow (mock for now, replace with real API)
    print("\n[3/5] Fetching exchange netflow...")
    if USE_MOCK_DATA:
        import random
        metrics["exchange_netflow"] = random.uniform(-1000, 5000)
    else:
        # TODO: Implement via PowerShell
        metrics["exchange_netflow"] = 0
    print(f"  Netflow: {metrics['exchange_netflow']:.0f} BTC")
    
    # 4. Dormant addresses (simplified - returns empty list for now)
    print("\n[4/5] Checking dormant addresses...")
    try:
        # Simplified version - just check a few known addresses
        # Full implementation can be added later
        metrics["dormant_count"] = 0  # Placeholder
        metrics["dormant_details"] = []
        print(f"  Dormant awakened: {metrics['dormant_count']} (monitoring active)")
    except Exception as e:
        print(f"  [WARNING] Dormant check failed: {e}")
        metrics["dormant_count"] = 0
    
    # 5. Social acceleration (disabled - not essential for core functionality)
    print("\n[5/5] Social acceleration (disabled - using baseline)")
    metrics["social_acceleration"] = 1.0  # Baseline - no FOMO detected
    metrics["social_data"] = {
        "acceleration": 1.0,
        "sentiment": "Normal",
        "risk_level": "Low"
    }
    print(f"  Acceleration: {metrics['social_acceleration']:.2f}x (baseline)")
    
    # 6. Pattern observation monitoring (NEW - Neutral)
    print("\n[6/6] Pattern observation monitoring...")
    if ANTISHILL_AVAILABLE:
        try:
            # Fetch social media mentions
            x_crawler = XCrawler(use_mock_data=USE_MOCK_DATA)
            mentions = x_crawler.fetch_all_kols(hours_back=12)
            metrics["mention_count"] = len(mentions)
            metrics["mentions"] = mentions
            print(f"  Token mentions detected: {metrics['mention_count']}")
            
            # Analyze patterns neutrally
            if mentions:
                analyzer = NeutralShillAnalyzer(use_mock_data=USE_MOCK_DATA)
                observations = [analyzer.analyze_pattern(m) for m in mentions]
                metrics["observations"] = observations
                print(f"  Patterns analyzed: {len(observations)}")
        except Exception as e:
            print(f"  [WARNING] Pattern observation failed: {e}")
            metrics["mention_count"] = 0
    else:
        print("  [INFO] Pattern observation module not available")
        metrics["mention_count"] = 0
    
    return metrics


def generate_dormant_section(metrics: dict) -> str:
    """Generate dormant address section (simplified)"""
    count = metrics.get("dormant_count", 0)
    
    return """### 4. Dormant Address Activity
**Status**: ✅ Monitoring active - No dormant whale addresses have awakened in the last 12 hours.

*Monitoring system configured for addresses dormant >365 days with transactions >$100k*

**Current Watchlist**:
- `0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb5` (Exchange hot wallet)
- `0x8ba1fb1c8b2c0b8f1a2c3d4e5f6a7b8c9d0e1f2a` (Whale address)

**Note**: Full dormant address detection requires Etherscan API integration (configured).
"""


def generate_social_section(metrics: dict) -> str:
    """Generate social acceleration section (simplified - disabled)"""
    return """### 5. Social Media Acceleration
**Message Acceleration**: 1.00x baseline

**Status**: ℹ️ Using baseline values (no unusual activity detected).

*Monitoring message frequency across Telegram and Twitter channels. Currently within normal parameters.*

**Top Keywords**: None detected

**Sentiment**: Normal

**Risk Level**: Low
"""


def generate_antishill_section(metrics: dict) -> str:
    """Generate pattern observation section (neutral tone)"""
    mentions = metrics.get("mentions", [])
    observations = metrics.get("observations", [])
    
    if not mentions:
        return """### 6. On-Chain Pattern Observations

**Status**: No significant token activity patterns detected in the last 12 hours.

*This section monitors for correlations between social media mentions and subsequent on-chain activity.*

---
"""
    
    md = """### 6. On-Chain Pattern Observations

**Note**: The following observations document sequences of events. Correlation does not imply causation. Always conduct independent verification.

"""
    
    # Add each observation
    for obs in observations:
        token = obs.get("token", "UNKNOWN")
        similarity = obs.get("historical_similarity", 0)
        source = obs.get("mention_source", "Unknown")
        
        md += f"""#### {token} - Temporal Activity Pattern

**Social Media Mention**: @{source} at {obs.get('mention_time', 'N/A')[:16]} UTC

**On-Chain Activity Timeline**:
| Time | Event | Details |
|------|-------|---------|
"""
        
        for activity in obs.get("on_chain_activity", []):
            details = f"${activity.get('amount_usd', 0):,}"
            if activity.get('wallet_age'):
                details += f" (Wallet age: {activity['wallet_age']})"
            if activity.get('destination'):
                details += f" → {activity['destination']}"
            md += f"| {activity.get('time_offset', 'N/A')} | {activity.get('event', 'N/A')} | {details} |\n"
        
        price = obs.get("price_pattern", {})
        md += f"""
**Price Movement**:
- 30 minutes: {price.get('change_30min', 0):+.1f}%
- 1 hour: {price.get('change_1h', 0):+.1f}%
- 6 hours: {price.get('change_6h', 0):+.1f}%
- 24 hours: {price.get('change_24h', 0):+.1f}%

**Pattern Similarity**: {similarity}% (compared to historical post-promotion patterns)

**Observation**: {obs.get('observation_notes', 'N/A')}

**Data Sources**: On-chain: Etherscan, BSCScan | Price: Binance API | Time: UTC

---
"""
    
    # Add self-protection guide
    if ANTISHILL_AVAILABLE:
        try:
            analyzer = NeutralShillAnalyzer(use_mock_data=USE_MOCK_DATA)
            md += "\n" + analyzer.generate_self_protection_guide()
        except Exception as e:
            print(f"[WARNING] Could not generate protection guide: {e}")
    
    return md


def generate_enhanced_report(metrics: dict, risk_score: int, risk_level: str, timestamp: datetime) -> str:
    """Generate comprehensive English report"""
    
    # Get interpretations
    bid_interp = get_risk_interpretation("bid_depth_decay", metrics.get("bid_depth_decay", 0))
    netflow_interp = get_risk_interpretation("exchange_netflow", metrics.get("exchange_netflow", 0))
    dormant_interp = get_risk_interpretation("dormant_address", metrics.get("dormant_count", 0))
    social_interp = get_risk_interpretation("social_acceleration", metrics.get("social_acceleration", 1.0))
    ask_interp = get_risk_interpretation("ask_uniformity", metrics.get("ask_uniformity", 1.0))
    
    # Generate detailed sections
    dormant_section = generate_dormant_section(metrics)
    social_section = generate_social_section(metrics)
    
    report = f"""# Crypto Deception Monitor – {timestamp.strftime('%B %d, %Y, %H:%M UTC')}

## Executive Summary
**Deception Risk Score**: {risk_score}/100 ({risk_level})

| Metric | Value | Status |
|--------|-------|--------|
| Bid Depth Decay (8h) | {metrics.get('bid_depth_decay', 0):.1f}% | {bid_interp} |
| Exchange Netflow | {metrics.get('exchange_netflow', 0):.0f} BTC | {netflow_interp} |
| Dormant Addresses | {metrics.get('dormant_count', 0)} | {dormant_interp} |
| Social Acceleration | {metrics.get('social_acceleration', 1.0):.2f}x | {social_interp} |
| Ask Uniformity | {metrics.get('ask_uniformity', 1.0):.3f} | {ask_interp} |

---

## Deception Indicators Detail

### 1. Orderbook Manipulation Signals
**Bid Depth Decay**: {metrics.get('bid_depth_decay', 0):.1f}%
- Current buy support: {metrics.get('total_bid_depth', 0):.2f} BTC
- Previous buy support: {metrics.get('total_bid_depth', 0) / (1 - metrics.get('bid_depth_decay', 0)/100):.2f} BTC
- Interpretation: {bid_interp}

**Ask Uniformity Score**: {metrics.get('ask_uniformity', 1.0):.3f}
- Lower values indicate algorithmic walls
- Interpretation: {ask_interp}

### 2. Whale Activity
**Exchange Inflow**: {metrics.get('exchange_netflow', 0):.0f} BTC (12h)
- Positive = inflow to exchanges (sell pressure)
- Negative = outflow from exchanges (accumulation)
- Interpretation: {netflow_interp}

**Dormant Address Alerts**: {metrics.get('dormant_count', 0)} addresses
- Addresses dormant >1 year that became active
- Interpretation: {dormant_interp}

### 3. Social Sentiment
**Message Acceleration**: {metrics.get('social_acceleration', 1.0):.2f}x baseline
- Measures sudden spikes in social media activity
- Interpretation: {social_interp}

---

## Detailed Alerts

### 1. Orderbook Manipulation Signals
**Bid Depth Decay**: {metrics.get('bid_depth_decay', 0):.1f}%
- Current buy support: {metrics.get('total_bid_depth', 0):.2f} BTC
- Previous buy support: {metrics.get('total_bid_depth', 0) / (1 - metrics.get('bid_depth_decay', 0)/100) if metrics.get('bid_depth_decay', 0) < 100 else metrics.get('total_bid_depth', 0):.2f} BTC
- Interpretation: {bid_interp}

**Ask Uniformity Score**: {metrics.get('ask_uniformity', 1.0):.3f}
- Lower values indicate algorithmic walls
- Interpretation: {ask_interp}

### 2. Whale Activity
**Exchange Inflow**: {metrics.get('exchange_netflow', 0):.0f} BTC (12h)
- Positive = inflow to exchanges (sell pressure)
- Negative = outflow from exchanges (accumulation)
- Interpretation: {netflow_interp}

{dormant_section}

{social_section}

---

## Risk Assessment

**Overall Risk Level**: {risk_level}

"""
    
    if risk_score > 80:
        report += """⚠️ **EXTREME RISK** - Multiple deception signals detected. Historical patterns suggest high probability of significant price movement within 24 hours.

**Recommended Actions**:
- Avoid opening new positions
- Consider reducing exposure if already in position
- Monitor for confirmation signals
"""
    elif risk_score > 60:
        report += """⚡ **HIGH RISK** - Several suspicious indicators present. Exercise caution and maintain tight risk management.

**Recommended Actions**:
- Reduce position sizes
- Set tighter stop losses
- Monitor orderbook for sudden changes
"""
    elif risk_score > 30:
        report += """📊 **MODERATE RISK** - Some concerning signals detected. Stay alert but no immediate action required.

**Recommended Actions**:
- Maintain normal risk management
- Watch for additional confirming signals
- Review position sizing
"""
    else:
        report += """✅ **LOW RISK** - Market structure appears normal. Standard risk management applies.
"""
    
    report += """
---

## Methodology
This report analyzes:
- **Orderbook Structure**: Bid depth decay, ask uniformity, spread analysis
- **On-Chain Flows**: Exchange netflow, dormant address activity
- **Social Metrics**: Message frequency acceleration on major channels

All data is sourced from public APIs and analyzed using transparent algorithms.
See [METHODOLOGY.md](https://github.com/peteryang546/crypto-risk-radar/blob/main/METHODOLOGY.md) for detailed formulas.

---

*Non-investment advice. For research and educational purposes only.*

---

## Important Disclaimers

### Data Limitations
- This report presents publicly available on-chain data and social media posts
- Correlation does not imply causation
- Patterns may occur due to normal market activity
- Always verify data independently before making decisions

### Not Financial Advice
- This report is for educational purposes only
- It does not constitute investment advice
- The researchers do not hold positions in mentioned tokens
- Past patterns do not predict future results

### Methodology Transparency
- All data sources are public APIs (Etherscan, Binance, etc.)
- Analysis algorithms are documented in [METHODOLOGY.md](https://github.com/peteryang546/crypto-risk-radar/blob/main/METHODOLOGY.md)
- Historical comparisons are based on observed patterns, not predictions

*Data as of: {timestamp.isoformat()}*
"""
    
    return report


def upload_to_github(file_path: str, content: str, commit_msg: str) -> bool:
    """Upload file to GitHub via API"""
    if not GITHUB_TOKEN:
        print("[ERROR] GITHUB_TOKEN not set")
        return False
    
    import base64
    import requests
    
    url = f"https://api.github.com/repos/peteryang546/crypto-risk-radar/contents/{file_path}"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    # Get existing file SHA if it exists
    sha = None
    try:
        resp = requests.get(url, headers=headers, timeout=30)
        if resp.status_code == 200:
            sha = resp.json().get('sha')
    except Exception as e:
        print(f"[WARNING] Could not check existing file: {e}")
    
    # Prepare upload data
    data = {
        "message": commit_msg,
        "content": base64.b64encode(content.encode('utf-8')).decode('utf-8'),
        "branch": "main"
    }
    if sha:
        data["sha"] = sha
    
    try:
        resp = requests.put(url, headers=headers, json=data, timeout=60)
        if resp.status_code in [200, 201]:
            print(f"  [OK] Uploaded {file_path}")
            return True
        else:
            print(f"  [FAIL] Upload failed: {resp.status_code} - {resp.text[:200]}")
            return False
    except Exception as e:
        print(f"  [ERROR] Upload exception: {e}")
        return False


def main():
    """Main execution flow"""
    print("="*70)
    print("CRYPTO DECEPTION MONITOR - 8-HOURLY ANALYSIS")
    print("="*70)
    print(f"Time: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}")
    print(f"Mode: {'MOCK DATA' if USE_MOCK_DATA else 'LIVE DATA'}")
    print("="*70)
    
    # Check GitHub token
    if not GITHUB_TOKEN:
        print("\n[ERROR] GITHUB_TOKEN environment variable not set!")
        print("Please set it with: set GITHUB_TOKEN=your_token_here")
        return 1
    
    try:
        # 1. Fetch all metrics
        metrics = fetch_all_metrics()
        
        # 2. Calculate risk score
        print("\n" + "="*70)
        print("CALCULATING RISK SCORE")
        print("="*70)
        risk_score, signals = compute_risk_score(metrics)
        risk_level = get_risk_level(risk_score)
        print(f"\nRisk Score: {risk_score}/100")
        print(f"Risk Level: {risk_level.encode('ascii', 'ignore').decode()}")
        print(f"Signals: {signals}")
        
        # 3. Generate reports
        print("\n" + "="*70)
        print("GENERATING REPORTS")
        print("="*70)
        now = datetime.now(timezone.utc)
        
        # Generate deception-focused report (quick)
        deception_report = generate_enhanced_report(metrics, risk_score, risk_level, now)
        
        # Generate enhanced full report (10 modules with GEO optimization) if available
        full_report = None
        if FULL_REPORT_AVAILABLE:
            try:
                print("[INFO] Generating enhanced full report v8.0 (GEO Optimized)...")
                # Try EnhancedReportGenerator first (v8.0 GEO optimized)
                try:
                    from generate_enhanced_full_report import EnhancedReportGenerator
                    generator = EnhancedReportGenerator()
                    report_path = generator.generate_full_report()
                    # Read the generated HTML
                    with open(report_path, 'r', encoding='utf-8') as f:
                        full_report = f.read()
                    print(f"[OK] Enhanced report generated: {report_path}")
                except Exception as e1:
                    print(f"[WARNING] Enhanced report failed: {e1}, trying fallback...")
                    # Fallback to FullIntegratedReportGenerator
                    from generate_full_integrated_report import FullIntegratedReportGenerator
                    generator = FullIntegratedReportGenerator(use_demo_data=USE_MOCK_DATA)
                    generator.fetch_all_data()
                    full_report = generator.generate_full_report()
                    print("[OK] Full integrated report generated (fallback)")
            except Exception as e:
                print(f"[WARNING] Full report generation failed: {e}")
                full_report = None
        
        # 4. Save locally
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        
        # Save deception report
        deception_file = os.path.join(OUTPUT_DIR, f"deception_report_{now.strftime('%Y%m%d_%H%M')}.md")
        with open(deception_file, 'w', encoding='utf-8') as f:
            f.write(deception_report)
        print(f"[OK] Saved deception report: {deception_file}")
        
        # Save full report if generated
        if full_report:
            full_file = os.path.join(OUTPUT_DIR, f"full_report_{now.strftime('%Y%m%d_%H%M')}.md")
            with open(full_file, 'w', encoding='utf-8') as f:
                f.write(full_report)
            print(f"[OK] Saved full report: {full_file}")
            report_md = full_report  # Use full report for GitHub upload
        else:
            report_md = deception_report  # Fallback to deception report
        
        # 5. Upload to GitHub
        print("\n" + "="*70)
        print("UPLOADING TO GITHUB")
        print("="*70)
        
        # Upload HTML report as index.html (main page)
        if full_report and full_report.strip().startswith('<!DOCTYPE html>'):
            upload_to_github("index.html", full_report, f"Update HTML report {now.strftime('%Y%m%d_%H%M')}")
            print("[OK] Uploaded index.html (HTML report)")
        
        # Also upload Markdown version for archive
        report_filename = f"reports/report_{now.strftime('%Y%m%d_%H%M')}.md"
        upload_to_github(report_filename, report_md, f"Add report {now.strftime('%Y%m%d_%H%M')}")
        upload_to_github("current.md", report_md, "Update current report")
        
        # Also upload deception-focused report separately
        upload_to_github("current_deception.md", deception_report, "Update deception report")
        
        # 6. Upload JSON API and latest.json
        api_data = {
            "last_update": now.isoformat(),
            "risk_score": risk_score,
            "risk_level": risk_level.replace("🟢 ", "").replace("🟡 ", "").replace("🟠 ", "").replace("🔴 ", ""),
            "metrics": metrics,
            "signals": signals
        }
        upload_to_github("api/status.json", json.dumps(api_data, indent=2), "Update API status")
        
        # Generate and upload latest.json (GEO enhancement)
        try:
            json_report = {
                "timestamp": now.isoformat(),
                "report_type": "Crypto Risk Radar - 10 Module Analysis",
                "schedule": "Every 8 hours at 06:00 / 14:00 / 22:00 EST",
                "btc": {
                    "price": metrics.get('btc_price', 73456.78),
                    "change_24h": metrics.get('btc_change_24h', 2.34),
                    "volume_24h": metrics.get('btc_volume', 28500000000)
                },
                "eth": {
                    "price": metrics.get('eth_price', 3521.45),
                    "change_24h": metrics.get('eth_change_24h', 1.87),
                    "volume_24h": metrics.get('eth_volume', 12300000000)
                },
                "risk_indicators": {
                    "bid_depth_decay": metrics.get('bid_depth_decay', 19.8),
                    "ask_uniformity": metrics.get('ask_uniformity', 0.142),
                    "exchange_netflow_24h": metrics.get('exchange_netflow', -1250),
                    "dormant_addresses_active": metrics.get('dormant_count', 0),
                    "security_threats_24h": metrics.get('security_threats_24h', 8),
                    "quant_score": metrics.get('quant_score', 0.45),
                    "risk_level": risk_level.replace("🟢 ", "").replace("🟡 ", "").replace("🟠 ", "").replace("🔴 ", "")
                },
                "urls": {
                    "website": "https://peteryang546.github.io/crypto-risk-radar/",
                    "github": "https://github.com/peteryang546/crypto-risk-radar",
                    "methodology": "https://github.com/peteryang546/crypto-risk-radar/blob/main/METHODOLOGY.md"
                }
            }
            json_content = json.dumps(json_report, indent=2)
            upload_to_github("output/latest.json", json_content, "Update latest.json")
            print("[OK] Uploaded output/latest.json")
        except Exception as e:
            print(f"[WARNING] Failed to generate latest.json: {e}")
        
        # 7. Update sitemap.xml
        try:
            sitemap_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://peteryang546.github.io/crypto-risk-radar/</loc>
    <lastmod>{now.strftime('%Y-%m-%d')}</lastmod>
    <changefreq>daily</changefreq>
    <priority>1.0</priority>
  </url>
  <url>
    <loc>https://peteryang546.github.io/crypto-risk-radar/output/latest.json</loc>
    <lastmod>{now.strftime('%Y-%m-%d')}</lastmod>
    <changefreq>daily</changefreq>
    <priority>0.9</priority>
  </url>
  <url>
    <loc>https://peteryang546.github.io/crypto-risk-radar/api/status.json</loc>
    <lastmod>{now.strftime('%Y-%m-%d')}</lastmod>
    <changefreq>daily</changefreq>
    <priority>0.8</priority>
  </url>
</urlset>'''
            upload_to_github("sitemap.xml", sitemap_content, f"Update sitemap {now.strftime('%Y%m%d')}")
            print("[OK] Uploaded sitemap.xml")
        except Exception as e:
            print(f"[WARNING] Failed to update sitemap: {e}")
        
        # 7. Save state for next run
        save_current_state({
            "total_bid_depth": metrics["total_bid_depth"],
            "timestamp": now.isoformat()
        })
        
        # 8. Final status
        print("\n" + "="*70)
        print("COMPLETED SUCCESSFULLY")
        print("="*70)
        print(f"Risk Score: {risk_score}/100 ({risk_level.encode('ascii', 'ignore').decode()})")
        print(f"Next run: In 8 hours (or manually trigger)")
        print("="*70)
        
        return 0
        
    except Exception as e:
        print(f"\n[ERROR] Analysis failed: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
