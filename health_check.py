#!/usr/bin/env python3
"""
Health Check & Monitoring System
Monitors data sources and reports status
"""

import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, r'F:\stepclaw\agents\blockchain-analyst')

from config import GITHUB_TOKEN

OUTPUT_DIR = Path(r'F:\stepclaw\agents\blockchain-analyst\output')


class HealthChecker:
    """Monitor API health and data quality"""
    
    def __init__(self):
        self.checks = []
        self.status = 'healthy'
    
    def check_api(self, name: str, test_func) -> dict:
        """Check an API endpoint"""
        try:
            result = test_func()
            return {
                'name': name,
                'status': 'ok',
                'message': result.get('message', 'Working'),
                'latency_ms': result.get('latency', 0),
                'data_count': result.get('count', 0)
            }
        except Exception as e:
            self.status = 'degraded'
            return {
                'name': name,
                'status': 'error',
                'message': str(e)[:100],
                'latency_ms': 0,
                'data_count': 0
            }
    
    def test_coingecko(self):
        """Test CoinGecko API"""
        import requests
        start = datetime.now()
        resp = requests.get('https://api.coingecko.com/api/v3/ping', timeout=10)
        latency = (datetime.now() - start).total_seconds() * 1000
        
        if resp.status_code == 200:
            return {'message': 'API responding', 'latency': latency, 'count': 1}
        raise Exception(f'Status {resp.status_code}')
    
    def test_goplus(self):
        """Test GoPlus API"""
        import requests
        start = datetime.now()
        # Test with a known address
        url = 'https://api.gopluslabs.io/api/v1/token_security/1?contract_addresses=0xdac17f958d2ee523a2206206994597c13d831ec7'
        resp = requests.get(url, timeout=10)
        latency = (datetime.now() - start).total_seconds() * 1000
        
        if resp.status_code == 200:
            data = resp.json()
            return {'message': 'API responding', 'latency': latency, 'count': 1}
        raise Exception(f'Status {resp.status_code}')
    
    def test_github_pages(self):
        """Test GitHub Pages"""
        import requests
        start = datetime.now()
        resp = requests.get('https://peteryang546.github.io/crypto-risk-radar/', timeout=10)
        latency = (datetime.now() - start).total_seconds() * 1000
        
        if resp.status_code == 200:
            return {'message': 'Site accessible', 'latency': latency, 'count': 1}
        raise Exception(f'Status {resp.status_code}')
    
    def test_latest_json(self):
        """Test latest.json API"""
        import requests
        start = datetime.now()
        resp = requests.get('https://peteryang546.github.io/crypto-risk-radar/output/latest.json', timeout=10)
        latency = (datetime.now() - start).total_seconds() * 1000
        
        if resp.status_code == 200:
            data = resp.json()
            return {
                'message': f"Data from {data.get('timestamp', 'unknown')}",
                'latency': latency,
                'count': 1
            }
        raise Exception(f'Status {resp.status_code}')
    
    def run_all_checks(self):
        """Run all health checks"""
        print("[INFO] Running health checks...")
        
        self.checks = [
            self.check_api('CoinGecko', self.test_coingecko),
            self.check_api('GoPlus Security', self.test_goplus),
            self.check_api('GitHub Pages', self.test_github_pages),
            self.check_api('JSON API', self.test_latest_json),
        ]
        
        # Determine overall status
        errors = sum(1 for c in self.checks if c['status'] == 'error')
        if errors == 0:
            self.status = 'healthy'
        elif errors <= 2:
            self.status = 'degraded'
        else:
            self.status = 'critical'
        
        return self.checks
    
    def generate_report(self) -> dict:
        """Generate health report"""
        return {
            'timestamp': datetime.now().isoformat(),
            'status': self.status,
            'checks': self.checks,
            'summary': {
                'total': len(self.checks),
                'healthy': sum(1 for c in self.checks if c['status'] == 'ok'),
                'errors': sum(1 for c in self.checks if c['status'] == 'error'),
                'avg_latency_ms': sum(c['latency_ms'] for c in self.checks) / len(self.checks) if self.checks else 0
            }
        }
    
    def save_report(self):
        """Save health report to file"""
        report = self.generate_report()
        
        # Save to output directory
        health_path = OUTPUT_DIR / 'health.json'
        with open(health_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2)
        
        print(f"[OK] Health report saved: {health_path}")
        return health_path
    
    def print_summary(self):
        """Print summary to console"""
        print("\n" + "="*70)
        print("HEALTH CHECK SUMMARY")
        print("="*70)
        
        status_emoji = {
            'healthy': '[OK]',
            'degraded': '[WARN]',
            'critical': '[CRIT]'
        }
        
        print(f"\nOverall Status: {status_emoji.get(self.status, '[UNK]')} {self.status.upper()}")
        print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        print("\nAPI Checks:")
        for check in self.checks:
            emoji = '[OK]' if check['status'] == 'ok' else '[ERR]'
            print(f"  {emoji} {check['name']}: {check['message']} ({check['latency_ms']:.0f}ms)")
        
        summary = self.generate_report()['summary']
        print(f"\nSummary: {summary['healthy']}/{summary['total']} healthy")
        print(f"Average latency: {summary['avg_latency_ms']:.0f}ms")
        
        print("="*70)
        
        # Return exit code
        return 0 if self.status == 'healthy' else 1


def main():
    """Main health check routine"""
    checker = HealthChecker()
    checker.run_all_checks()
    checker.save_report()
    exit_code = checker.print_summary()
    
    # If degraded/critical, could send alert here
    if checker.status != 'healthy':
        print("\n[ALERT] System status is not healthy. Check logs for details.")
        # TODO: Send notification (email, webhook, etc.)
    
    return exit_code


if __name__ == "__main__":
    exit(main())
