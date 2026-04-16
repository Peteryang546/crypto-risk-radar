#!/usr/bin/env python3
"""
Run Analysis with Detailed Logging
Enhanced version with comprehensive feedback
"""

import subprocess
import sys
import json
import traceback
from datetime import datetime
from pathlib import Path

OUTPUT_DIR = Path(r'F:\stepclaw\agents\blockchain-analyst\output')
LOG_FILE = OUTPUT_DIR / 'last_run.json'


def log_run(status, details):
    """Log run results"""
    log_entry = {
        'timestamp': datetime.now().isoformat(),
        'status': status,
        'details': details
    }
    
    with open(LOG_FILE, 'w', encoding='utf-8') as f:
        json.dump(log_entry, f, indent=2)
    
    return log_entry


def run_pipeline():
    """Run the full pipeline"""
    start_time = datetime.now()
    steps = []
    
    try:
        # Step 1: Generate report
        print("[1/3] Generating report...")
        result1 = subprocess.run(
            [r'C:\Users\Administrator\AppData\Local\Programs\Python\Python311\python.exe',
             r'F:\stepclaw\agents\blockchain-analyst\scripts\generate_enhanced_full_report.py'],
            capture_output=True,
            text=True,
            timeout=300
        )
        
        step1_success = result1.returncode == 0
        steps.append({
            'name': 'Generate Report',
            'success': step1_success,
            'output': result1.stdout[-300:] if result1.stdout else '',
            'error': result1.stderr[:300] if result1.stderr else ''
        })
        
        if not step1_success:
            raise Exception(f"Report generation failed: {result1.stderr}")
        
        # Step 2: Publish
        print("[2/3] Publishing to GitHub...")
        result2 = subprocess.run(
            [r'C:\Users\Administrator\AppData\Local\Programs\Python\Python311\python.exe',
             r'F:\stepclaw\agents\blockchain-analyst\publish_report.py'],
            capture_output=True,
            text=True,
            timeout=300
        )
        
        step2_success = result2.returncode == 0
        steps.append({
            'name': 'Publish',
            'success': step2_success,
            'output': result2.stdout[-300:] if result2.stdout else '',
            'error': result2.stderr[:300] if result2.stderr else ''
        })
        
        if not step2_success:
            raise Exception(f"Publishing failed: {result2.stderr}")
        
        # Step 3: Health check
        print("[3/3] Running health check...")
        result3 = subprocess.run(
            [r'C:\Users\Administrator\AppData\Local\Programs\Python\Python311\python.exe',
             r'F:\stepclaw\agents\blockchain-analyst\health_check.py'],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        steps.append({
            'name': 'Health Check',
            'success': result3.returncode == 0,
            'output': result3.stdout[-200:] if result3.stdout else '',
            'error': ''
        })
        
        # Calculate duration
        duration = (datetime.now() - start_time).total_seconds()
        
        # Success
        details = {
            'duration_seconds': duration,
            'steps': steps,
            'timestamp_et': datetime.now().strftime('%Y-%m-%d %H:%M') + ' ET',
            'website': 'https://peteryang546.github.io/crypto-risk-radar/'
        }
        
        log_run('success', details)
        
        print(f"\n[OK] Run completed successfully in {duration:.1f} seconds")
        print(f"[OK] Website updated: {details['website']}")
        
        return 0
        
    except Exception as e:
        duration = (datetime.now() - start_time).total_seconds()
        
        details = {
            'duration_seconds': duration,
            'steps': steps,
            'error': str(e),
            'traceback': traceback.format_exc()
        }
        
        log_run('error', details)
        
        print(f"\n[ERROR] Run failed after {duration:.1f} seconds")
        print(f"[ERROR] {e}")
        
        return 1


if __name__ == "__main__":
    print("="*70)
    print("CRYPTO RISK RADAR - AUTOMATED RUN")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70)
    
    exit_code = run_pipeline()
    
    # Print status summary
    print("\n" + "="*70)
    print("RUN STATUS SUMMARY")
    print("="*70)
    
    if LOG_FILE.exists():
        with open(LOG_FILE, 'r') as f:
            log = json.load(f)
        
        status = log.get('status', 'unknown')
        ts = log.get('timestamp', 'unknown')[:19]
        
        if status == 'success':
            print(f"[OK] Last run: {ts}")
            print(f"[OK] Status: SUCCESS")
            print(f"[OK] Duration: {log['details'].get('duration_seconds', 0):.1f}s")
            print(f"[OK] Website: {log['details'].get('website', 'N/A')}")
        else:
            print(f"[ERR] Last run: {ts}")
            print(f"[ERR] Status: FAILED")
            print(f"[ERR] Error: {log['details'].get('error', 'Unknown')}")
    
    print("="*70)
    
    # Send notification
    print("\n[SENDING NOTIFICATION...]")
    try:
        subprocess.run(
            [r'C:\Users\Administrator\AppData\Local\Programs\Python\Python311\python.exe',
             r'F:\stepclaw\agents\blockchain-analyst\notify.py'],
            capture_output=False,
            timeout=10
        )
    except Exception as e:
        print(f"[WARNING] Notification failed: {e}")
    
    sys.exit(exit_code)
