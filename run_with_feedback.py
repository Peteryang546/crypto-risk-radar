#!/usr/bin/env python3
"""
Run Analysis with Feedback
Runs the full pipeline and provides detailed feedback
"""

import subprocess
import sys
import traceback
from datetime import datetime
from pathlib import Path

sys.path.insert(0, r'F:\stepclaw\agents\blockchain-analyst')

from monitor import RunMonitor


def run_command(cmd, description):
    """Run a command and return success status"""
    print(f"\n{'='*70}")
    print(f"STEP: {description}")
    print(f"{'='*70}")
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=300,
            shell=True
        )
        
        if result.returncode == 0:
            print(f"[OK] {description} completed successfully")
            if result.stdout:
                print(result.stdout[-500:] if len(result.stdout) > 500 else result.stdout)
            return True, "Success"
        else:
            print(f"[ERROR] {description} failed with code {result.returncode}")
            if result.stderr:
                print(f"Error: {result.stderr[:500]}")
            return False, f"Exit code {result.returncode}"
            
    except subprocess.TimeoutExpired:
        print(f"[ERROR] {description} timed out after 5 minutes")
        return False, "Timeout"
    except Exception as e:
        print(f"[ERROR] {description} failed: {e}")
        return False, str(e)


def main():
    """Main execution with feedback"""
    monitor = RunMonitor()
    start_time = datetime.now()
    
    print("="*70)
    print("CRYPTO RISK RADAR - AUTOMATED RUN")
    print(f"Started: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70)
    
    steps = [
        (r"C:\Users\Administrator\AppData\Local\Programs\Python\Python311\python.exe scripts\generate_enhanced_full_report.py",
         "Generate Report"),
        (r"C:\Users\Administrator\AppData\Local\Programs\Python\Python311\python.exe publish_report.py",
         "Publish to GitHub"),
        (r"C:\Users\Administrator\AppData\Local\Programs\Python\Python311\python.exe health_check.py",
         "Health Check"),
    ]
    
    results = []
    all_success = True
    
    for cmd, desc in steps:
        success, message = run_command(cmd, desc)
        results.append({'step': desc, 'success': success, 'message': message})
        if not success:
            all_success = False
    
    # Calculate duration
    duration = (datetime.now() - start_time).total_seconds()
    
    # Print summary
    print("\n" + "="*70)
    print("RUN SUMMARY")
    print("="*70)
    
    for r in results:
        status = "[OK]" if r['success'] else "[ERR]"
        print(f"{status} {r['step']}: {r['message']}")
    
    print(f"\nDuration: {duration:.1f} seconds")
    print(f"Status: {'SUCCESS' if all_success else 'FAILED'}")
    
    # Record in monitor
    if all_success:
        monitor.record_run('success', f'All steps completed in {duration:.0f}s')
    else:
        failed = [r['step'] for r in results if not r['success']]
        monitor.record_run('error', f"Failed: {', '.join(failed)}")
    
    # Print final feedback
    print("\n" + "="*70)
    monitor.print_feedback()
    
    return 0 if all_success else 1


if __name__ == "__main__":
    exit(main())
