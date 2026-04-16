#!/usr/bin/env python3
"""
Deception Score Calculator
Computes comprehensive risk score (0-100) based on multiple deception indicators
"""

import sys
sys.path.insert(0, r'F:\stepclaw\agents\blockchain-analyst')
from config import THRESHOLDS, WEIGHTS


def compute_risk_score(metrics: dict) -> int:
    """
    Compute deception risk score (0-100) based on:
    - Bid depth decay (rapid removal of buy support)
    - Exchange netflow (large inflows = sell pressure)
    - Dormant address activity (whale awakening)
    - Social acceleration (FOMO signals)
    - Ask uniformity (algorithmic walls)
    """
    score = 0
    triggered_signals = []
    
    # 1. Bid depth decay (rapid removal of buy support)
    decay = metrics.get("bid_depth_decay", 0)
    if decay > THRESHOLDS["bid_depth_decay_danger"]:
        score += WEIGHTS["bid_depth_decay"] * 100
        triggered_signals.append("bid_depth_decay_danger")
    elif decay > THRESHOLDS["bid_depth_decay_warning"]:
        score += WEIGHTS["bid_depth_decay"] * 50
        triggered_signals.append("bid_depth_decay_warning")
    
    # 2. Exchange netflow (large inflows indicate sell pressure)
    netflow = metrics.get("exchange_netflow", 0)
    if netflow > THRESHOLDS["exchange_netflow_danger"]:
        score += WEIGHTS["exchange_netflow"] * 100
        triggered_signals.append("exchange_netflow_danger")
    elif netflow > THRESHOLDS["exchange_netflow_warning"]:
        score += WEIGHTS["exchange_netflow"] * 50
        triggered_signals.append("exchange_netflow_warning")
    
    # 3. Dormant address activity (whale awakening)
    dormant = metrics.get("dormant_count", 0)
    if dormant >= THRESHOLDS["dormant_address_danger"]:
        score += WEIGHTS["dormant_address"] * 100
        triggered_signals.append("dormant_address_danger")
    elif dormant >= THRESHOLDS["dormant_address_warning"]:
        score += WEIGHTS["dormant_address"] * 50
        triggered_signals.append("dormant_address_warning")
    
    # 4. Social acceleration (FOMO signals)
    social = metrics.get("social_acceleration", 1.0)
    if social > THRESHOLDS["social_acceleration_danger"]:
        score += WEIGHTS["social_acceleration"] * 100
        triggered_signals.append("social_acceleration_danger")
    elif social > THRESHOLDS["social_acceleration_warning"]:
        score += WEIGHTS["social_acceleration"] * 50
        triggered_signals.append("social_acceleration_warning")
    
    # 5. Ask uniformity (algorithmic walls, lower = more suspicious)
    uniformity = metrics.get("ask_uniformity", 1.0)
    if uniformity < THRESHOLDS["ask_uniformity_danger"]:
        score += WEIGHTS["ask_uniformity"] * 100
        triggered_signals.append("ask_uniformity_danger")
    elif uniformity < THRESHOLDS["ask_uniformity_warning"]:
        score += WEIGHTS["ask_uniformity"] * 50
        triggered_signals.append("ask_uniformity_warning")
    
    return min(int(score), 100), triggered_signals


def get_risk_level(score: int) -> str:
    """Map score to risk level with emoji"""
    if score <= 30:
        return "🟢 Low"
    elif score <= 60:
        return "🟡 Medium"
    elif score <= 80:
        return "🟠 High"
    else:
        return "🔴 Extreme"


def get_risk_interpretation(metric_name: str, value: float) -> str:
    """Get human-readable interpretation of a metric"""
    interpretations = {
        "bid_depth_decay": {
            "danger": "⚠️ Rapid support removal - possible bait-and-switch",
            "warning": "⚡ Buy support declining",
            "normal": "✓ Buy support stable"
        },
        "exchange_netflow": {
            "danger": "🚨 Massive inflow - heavy sell pressure expected",
            "warning": "📈 Elevated inflow - watch for distribution",
            "normal": "✓ Normal exchange flows"
        },
        "dormant_address": {
            "danger": "🐋 Multiple whales awakening - major move likely",
            "warning": "👁️ Dormant address active - monitor closely",
            "normal": "✓ No unusual whale activity"
        },
        "social_acceleration": {
            "danger": "🔥 FOMO peak - possible blow-off top",
            "warning": "📢 Elevated social chatter",
            "normal": "✓ Normal social activity"
        },
        "ask_uniformity": {
            "danger": "🤖 Algorithmic wall detected - manipulation likely",
            "warning": "⚡ Unusual ask pattern",
            "normal": "✓ Normal orderbook"
        }
    }
    
    if metric_name not in interpretations:
        return ""
    
    if metric_name == "bid_depth_decay":
        if value > THRESHOLDS["bid_depth_decay_danger"]:
            return interpretations[metric_name]["danger"]
        elif value > THRESHOLDS["bid_depth_decay_warning"]:
            return interpretations[metric_name]["warning"]
    elif metric_name == "exchange_netflow":
        if value > THRESHOLDS["exchange_netflow_danger"]:
            return interpretations[metric_name]["danger"]
        elif value > THRESHOLDS["exchange_netflow_warning"]:
            return interpretations[metric_name]["warning"]
    elif metric_name == "dormant_address":
        if value >= THRESHOLDS["dormant_address_danger"]:
            return interpretations[metric_name]["danger"]
        elif value >= THRESHOLDS["dormant_address_warning"]:
            return interpretations[metric_name]["warning"]
    elif metric_name == "social_acceleration":
        if value > THRESHOLDS["social_acceleration_danger"]:
            return interpretations[metric_name]["danger"]
        elif value > THRESHOLDS["social_acceleration_warning"]:
            return interpretations[metric_name]["warning"]
    elif metric_name == "ask_uniformity":
        if value < THRESHOLDS["ask_uniformity_danger"]:
            return interpretations[metric_name]["danger"]
        elif value < THRESHOLDS["ask_uniformity_warning"]:
            return interpretations[metric_name]["warning"]
    
    return interpretations[metric_name]["normal"]


if __name__ == "__main__":
    # Test
    test_metrics = {
        "bid_depth_decay": 35,
        "exchange_netflow": 3000,
        "dormant_count": 2,
        "social_acceleration": 4.5,
        "ask_uniformity": 0.08
    }
    
    score, signals = compute_risk_score(test_metrics)
    level = get_risk_level(score)
    print(f"Test Score: {score}/100 ({level})")
    print(f"Triggered: {signals}")
