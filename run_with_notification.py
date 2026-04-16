#!/usr/bin/env python3
"""
Run Analysis with Notification
Complete pipeline with automatic notification
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


def send_notification():
    """Send notification"""
    try:
        subprocess.run(
            [r'C:\Users\Administrator\AppData\Local\Programs\Python\Python311\python.exe',
             r'F:\stepclaw\agents\blockchain-analyst\notify.py'],
            capture_output=False,
            timeout=10
        )
    except Exception as e:
        print(f"[WARNING] Notification error: {e}")


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
        steps.append({'name': 'Generate', 'success': step1_success})
        
        if not step1_success:
            raise Exception("Report generation failed")
        
        # Step 2: Publish
        print("[2/3] Publishing...")
        result2 = subprocess.run(
            [r'C:\Users\Administrator\AppData\Local\Programs\Python\Python311\python.exe',
             r'F:\stepclaw\agents\blockchain-analyst\publish_report.py'],
            capture_output=True,
            text=True,
            timeout=300
        )
        
        step2_success = result2.returncode == 0
        steps.append({'name': 'Publish', 'success': step2_success})
        
        if not step2_success:
            # Log detailed error
            error_detail = f"Publishing failed\n\nSTDOUT:\n{result2.stdout}\n\nSTDERR:\n{result2.stderr}"
            print(f"[ERROR] {error_detail}")
            raise Exception(error_detail)
        
        # Step 3: Health check
        print("[3/3] Health check...")
        result3 = subprocess.run(
            [r'C:\Users\Administrator\AppData\Local\Programs\Python\Python311\python.exe',
             r'F:\stepclaw\agents\blockchain-analyst\health_check.py'],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        steps.append({'name': 'Health', 'success': result3.returncode == 0})
        
        # Success
        duration = (datetime.now() - start_time).total_seconds()
        
        details = {
            'duration_seconds': duration,
            'steps': steps,
            'timestamp_et': datetime.now().strftime('%Y-%m-%d %H:%M') + ' ET',
            'website': 'https://peteryang546.github.io/crypto-risk-radar/'
        }
        
        log_run('success', details)
        
        print(f"\n[OK] Completed in {duration:.1f}s")
        
        # Send notifications (multiple methods)
        send_notification()  # File-based notification
        
        # Try toast notification
        try:
            subprocess.run(
                [r'C:\Users\Administrator\AppData\Local\Programs\Python\Python311\python.exe',
                 r'F:\stepclaw\agents\blockchain-analyst\notify_toast.py'],
                capture_output=True,
                timeout=10
            )
        except:
            pass
        
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
        
        print(f"\n[ERROR] Failed: {e}")
        
        # Send notifications even on failure
        send_notification()
        
        # Try toast notification
        try:
            subprocess.run(
                [r'C:\Users\Administrator\AppData\Local\Programs\Python\Python311\python.exe',
                 r'F:\stepclaw\agents\blockchain-analyst\notify_toast.py'],
                capture_output=True,
                timeout=10
            )
        except:
            pass
        
        return 1


if __name__ == "__main__":
    print("="*70)
    print("CRYPTO RISK RADAR - AUTOMATED RUN")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70)
    
    exit_code = run_pipeline()
    sys.exit(exit_code)
