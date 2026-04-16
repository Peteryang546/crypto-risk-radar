#!/usr/bin/env python3
"""
Run Monitor & Feedback System
Monitors scheduled task execution and provides feedback
"""

import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, r'F:\stepclaw\agents\blockchain-analyst')

OUTPUT_DIR = Path(r'F:\stepclaw\agents\blockchain-analyst\output')
LOG_FILE = OUTPUT_DIR / 'run_log.json'


class RunMonitor:
    """Monitor report generation and provide feedback"""
    
    def __init__(self):
        self.runs = self._load_log()
    
    def _load_log(self):
        """Load run history"""
        if LOG_FILE.exists():
            with open(LOG_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {'runs': [], 'last_check': None}
    
    def _save_log(self):
        """Save run history"""
        with open(LOG_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.runs, f, indent=2)
    
    def check_recent_runs(self):
        """Check for recent report generation"""
        # Find latest HTML report
        reports = sorted(OUTPUT_DIR.glob('enhanced_report_*.html'), 
                        key=lambda x: x.stat().st_mtime, reverse=True)
        
        if not reports:
            return None
        
        latest = reports[0]
        mtime = datetime.fromtimestamp(latest.stat().st_mtime)
        
        return {
            'file': latest.name,
            'time': mtime.isoformat(),
            'age_minutes': (datetime.now() - mtime).total_seconds() / 60
        }
    
    def record_run(self, status, message, details=None):
        """Record a run attempt"""
        run_record = {
            'timestamp': datetime.now().isoformat(),
            'status': status,  # success, error, skipped
            'message': message,
            'details': details or {}
        }
        
        self.runs['runs'].append(run_record)
        self.runs['last_check'] = datetime.now().isoformat()
        
        # Keep only last 50 runs
        self.runs['runs'] = self.runs['runs'][-50:]
        
        self._save_log()
        return run_record
    
    def get_status_summary(self):
        """Get current status summary"""
        latest = self.check_recent_runs()
        
        if not latest:
            return {
                'status': 'error',
                'message': 'No reports found',
                'last_run': None
            }
        
        age_hours = latest['age_minutes'] / 60
        
        if age_hours < 1:
            status = 'fresh'
            message = f"Report generated {latest['age_minutes']:.0f} minutes ago"
        elif age_hours < 9:
            status = 'normal'
            message = f"Last report: {age_hours:.1f} hours ago"
        elif age_hours < 12:
            status = 'stale'
            message = f"Report is {age_hours:.1f} hours old - may be delayed"
        else:
            status = 'error'
            message = f"No recent reports! Last: {age_hours:.1f} hours ago"
        
        return {
            'status': status,
            'message': message,
            'last_run': latest,
            'next_expected': self._get_next_run_time()
        }
    
    def _get_next_run_time(self):
        """Calculate next expected run time"""
        now = datetime.now()
        et_now = now - timedelta(hours=12)  # Approximate ET conversion
        
        # Run times in ET: 06:00, 14:00, 22:00
        run_hours = [6, 14, 22]
        
        for hour in run_hours:
            if et_now.hour < hour:
                next_run = et_now.replace(hour=hour, minute=0, second=0)
                return (next_run + timedelta(hours=12)).isoformat()  # Convert back to CST
        
        # Next run is tomorrow at 06:00 ET
        next_run = (et_now + timedelta(days=1)).replace(hour=6, minute=0, second=0)
        return (next_run + timedelta(hours=12)).isoformat()
    
    def print_feedback(self):
        """Print user-friendly feedback"""
        summary = self.get_status_summary()
        
        print("="*70)
        print("CRYPTO RISK RADAR - RUN STATUS")
        print("="*70)
        
        status_emoji = {
            'fresh': '[OK]',
            'normal': '[OK]',
            'stale': '[WARN]',
            'error': '[ERR]'
        }
        
        print(f"\nStatus: {status_emoji.get(summary['status'], '[?]')} {summary['message']}")
        
        if summary['last_run']:
            lr = summary['last_run']
            print(f"Latest Report: {lr['file']}")
            print(f"Generated: {lr['time']}")
        
        print(f"\nNext Expected Run: {summary['next_expected'][:16]}")
        
        # Recent history
        if self.runs['runs']:
            print("\nRecent Activity:")
            for run in self.runs['runs'][-5:]:
                ts = run['timestamp'][:16]
                status = '[OK]' if run['status'] == 'success' else '[ERR]'
                print(f"  {status} {ts}: {run['message']}")
        
        print("="*70)
        
        return summary


def main():
    """Main monitoring function"""
    monitor = RunMonitor()
    
    # Check current status
    summary = monitor.print_feedback()
    
    # Record this check
    monitor.record_run('success', 'Status check completed', {
        'current_status': summary['status'],
        'last_report_age_hours': summary['last_run']['age_minutes'] / 60 if summary['last_run'] else None
    })
    
    return 0 if summary['status'] in ['fresh', 'normal'] else 1


if __name__ == "__main__":
    exit(main())
