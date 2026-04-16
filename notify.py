#!/usr/bin/env python3
"""
Notification System
Sends notifications after each run
"""

import json
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, r'F:\stepclaw\agents\blockchain-analyst')

OUTPUT_DIR = Path(r'F:\stepclaw\agents\blockchain-analyst\output')
LOG_FILE = OUTPUT_DIR / 'last_run.json'


def send_notification():
    """Send notification based on last run status"""
    
    if not LOG_FILE.exists():
        print("[ERROR] No run log found")
        return False
    
    with open(LOG_FILE, 'r', encoding='utf-8') as f:
        log = json.load(f)
    
    status = log.get('status', 'unknown')
    ts = log.get('timestamp', 'unknown')[:19]
    details = log.get('details', {})
    
    # Build notification message
    if status == 'success':
        duration = details.get('duration_seconds', 0)
        website = details.get('website', 'https://peteryang546.github.io/crypto-risk-radar/')
        
        # Find latest report
        reports = sorted(OUTPUT_DIR.glob('enhanced_report_*.html'), 
                        key=lambda x: x.stat().st_mtime, reverse=True)
        report_name = reports[0].name if reports else 'N/A'
        
        message = f"""
CRYPTO RISK RADAR - RUN COMPLETE [OK]

Status: SUCCESS
Time: {ts}
Duration: {duration:.1f} seconds
Report: {report_name}

Website: {website}

Next run: See schedule
"""
    else:
        error = details.get('error', 'Unknown error')
        
        message = f"""
CRYPTO RISK RADAR - RUN FAILED [ERR]

Status: FAILED
Time: {ts}
Error: {error}

Please check the system.
Log: output/last_run.json
"""
    
    # Print notification (will be captured by OpenClaw)
    print("="*70)
    print("NOTIFICATION")
    print("="*70)
    print(message)
    print("="*70)
    
    # Also save to notification file for reference
    notify_file = OUTPUT_DIR / 'last_notification.txt'
    with open(notify_file, 'w', encoding='utf-8') as f:
        f.write(message)
    
    return True


if __name__ == "__main__":
    send_notification()
