#!/usr/bin/env python3
"""
History Manager - Stores and retrieves previous state for calculating changes
"""

import os
import json
from datetime import datetime
from pathlib import Path
import sys
sys.path.insert(0, r'F:\stepclaw\agents\blockchain-analyst')
from config import DATA_DIR

HISTORY_FILE = os.path.join(DATA_DIR, "history.json")


def load_previous_state() -> dict:
    """Load previous run state from local file"""
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"[WARNING] Failed to load history: {e}")
    return {}


def save_current_state(state: dict):
    """Save current state to local file for next run"""
    try:
        os.makedirs(os.path.dirname(HISTORY_FILE), exist_ok=True)
        
        # Add timestamp
        state["last_updated"] = datetime.now().isoformat()
        
        with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
            json.dump(state, f, indent=2)
        
        print(f"[OK] History saved to {HISTORY_FILE}")
    except Exception as e:
        print(f"[ERROR] Failed to save history: {e}")


def calculate_decay(current: float, previous: float) -> float:
    """Calculate percentage decay from previous to current"""
    if previous <= 0:
        return 0
    return ((previous - current) / previous) * 100


if __name__ == "__main__":
    # Test
    state = load_previous_state()
    print(f"Loaded state: {state}")
    
    test_state = {"total_bid_depth": 150.5, "timestamp": datetime.now().isoformat()}
    save_current_state(test_state)
