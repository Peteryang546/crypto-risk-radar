#!/usr/bin/env python3
"""
Run report generation with automatic retry (max 5 attempts)
Shows clear success/failure status
"""

import subprocess
import sys
import time
from datetime import datetime

MAX_RETRIES = 5
RETRY_DELAYS = [0, 30, 60, 120, 180]  # seconds between retries


def run_report_generation(attempt):
    """Run the report generation script"""
    print(f"\n{'='*70}")
    print(f"ATTEMPT {attempt}/{MAX_RETRIES}")
    print(f"{'='*70}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        result = subprocess.run(
            [sys.executable, "scripts/generate_full_integrated_report.py", "--live"],
            cwd=r"F:\stepclaw\agents\blockchain-analyst",
            capture_output=True,
            text=True,
            timeout=300  # 5 minutes timeout
        )
        
        # Print output
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        
        return result.returncode == 0
        
    except subprocess.TimeoutExpired:
        print(f"[ERROR] Attempt {attempt} timed out after 5 minutes")
        return False
    except Exception as e:
        print(f"[ERROR] Attempt {attempt} failed with exception: {e}")
        return False


def main():
    print("="*70)
    print("CRYPTO RISK RADAR - AUTO RETRY SYSTEM")
    print("="*70)
    print(f"Max retries: {MAX_RETRIES}")
    print(f"Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70)
    
    success = False
    last_error = None
    
    for attempt in range(1, MAX_RETRIES + 1):
        # Wait before retry (except first attempt)
        if attempt > 1:
            delay = RETRY_DELAYS[attempt - 1]
            print(f"\n[RETRY] Waiting {delay} seconds before attempt {attempt}...")
            time.sleep(delay)
        
        # Run the report generation
        if run_report_generation(attempt):
            success = True
            break
        else:
            last_error = f"Attempt {attempt} failed"
            print(f"\n[WARNING] Attempt {attempt} failed")
    
    # Final status
    print("\n" + "="*70)
    print("FINAL STATUS")
    print("="*70)
    
    if success:
        print("[SUCCESS] Report generation completed!")
        print(f"Report generated successfully after {attempt} attempt(s)")
        print(f"End time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("\nNext steps:")
        print("1. Check output/ directory for the generated report")
        print("2. Review the HTML file")
        print("3. Upload to GitHub if needed")
        return 0
    else:
        print("[FAILURE] All attempts failed!")
        print(f"All {MAX_RETRIES} attempts failed")
        print(f"Last error: {last_error}")
        print(f"End time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("\nPossible causes:")
        print("- Network connectivity issues")
        print("- API rate limits")
        print("- Data source unavailable")
        print("- Script errors")
        print("\nTroubleshooting:")
        print("1. Check internet connection")
        print("2. Verify API keys are valid")
        print("3. Check logs for specific error messages")
        print("4. Try running with --demo flag for testing")
        return 1


if __name__ == "__main__":
    sys.exit(main())
