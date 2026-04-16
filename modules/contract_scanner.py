#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module 3: Contract Security Scanner
使用 GoPlus API 扫描合约安全风险
使用 PowerShell 绕过 Python SSL 问题
"""

import subprocess
import json
import sys
from datetime import datetime

sys.path.insert(0, r'F:\stepclaw\agents\blockchain-analyst')


class ContractScanner:
    """合约安全扫描器"""
    
    def __init__(self, use_demo_data=False):
        self.use_demo_data = use_demo_data
        self.chain_names = {
            1: 'Ethereum',
            56: 'BSC',
            137: 'Polygon',
            42161: 'Arbitrum',
            10: 'Optimism',
            43114: 'Avalanche',
            250: 'Fantom',
            8453: 'Base'
        }
    
    def _scan_via_powershell(self, contract_address, chain_id):
        """使用 PowerShell 扫描合约"""
        ps_code = f'''
        try {{
            $url = "https://api.gopluslabs.io/api/v1/token_security/{chain_id}?contract_addresses={contract_address}"
            $resp = Invoke-RestMethod -Uri $url -TimeoutSec 30
            $resp | ConvertTo-Json -Depth 10
        }} catch {{
            Write-Output "{{`"result`": null, `"error`": `"$($_.Exception.Message)`"}}"
        }}
        '''
        
        try:
            result = subprocess.run(
                ["powershell", "-Command", ps_code],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0 and result.stdout.strip():
                return json.loads(result.stdout)
            return {'result': None}
        except Exception as e:
            print(f"[ERROR] PowerShell scan failed: {e}")
            return {'result': None}
    
    def _get_demo_data(self):
        """演示数据"""
        return [
            {
                'contract_address': '0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb5',
                'chain_id': 1,
                'chain_name': 'Ethereum',
                'token_name': 'Demo Token A',
                'token_symbol': 'DTA',
                'is_open_source': True,
                'is_proxy': False,
                'is_mintable': False,
                'owner_address': '0x0000...0000',
                'owner_balance': 0,
                'owner_percent': 0,
                'is_blacklist': False,
                'is_whitelist': False,
                'is_honeypot': False,
                'risk_level': 'Low',
                'risk_score': 15,
                'scan_time': datetime.now().isoformat()
            },
            {
                'contract_address': '0x8ba1fb1c8b2c0b8f1a2c3d4e5f6a7b8c9d0e1f2a',
                'chain_id': 56,
                'chain_name': 'BSC',
                'token_name': 'Demo Token B',
                'token_symbol': 'DTB',
                'is_open_source': True,
                'is_proxy': True,
                'is_mintable': True,
                'owner_address': '0x1234...5678',
                'owner_balance': 1000000,
                'owner_percent': 25,
                'is_blacklist': True,
                'is_whitelist': False,
                'is_honeypot': False,
                'risk_level': 'Medium',
                'risk_score': 55,
                'scan_time': datetime.now().isoformat()
            }
        ]
    
    def scan_contract(self, contract_address, chain_id=1):
        """扫描单个合约"""
        if self.use_demo_data:
            return None
        
        print(f"[INFO] Scanning contract {contract_address} on chain {chain_id}...")
        result = self._scan_via_powershell(contract_address, chain_id)
        
        if not result or not result.get('result'):
            print(f"[WARNING] No data returned for contract {contract_address}")
            return None
        
        # 解析 GoPlus 响应
        token_data = result['result'].get(contract_address.lower(), {})
        
        if not token_data:
            return None
        
        # 计算风险分数
        risk_score = 0
        risk_factors = []
        
        if token_data.get('is_proxy', '0') == '1':
            risk_score += 20
            risk_factors.append('Proxy contract')
        
        if token_data.get('is_mintable', '0') == '1':
            risk_score += 25
            risk_factors.append('Mintable')
        
        owner_percent = float(token_data.get('owner_percent', '0') or 0)
        if owner_percent > 50:
            risk_score += 30
            risk_factors.append(f'High owner ownership ({owner_percent:.1f}%)')
        elif owner_percent > 20:
            risk_score += 15
            risk_factors.append(f'Moderate owner ownership ({owner_percent:.1f}%)')
        
        if token_data.get('is_blacklist', '0') == '1':
            risk_score += 25
            risk_factors.append('Blacklist function')
        
        if token_data.get('is_honeypot', '0') == '1':
            risk_score += 50
            risk_factors.append('HONEYPOT DETECTED!')
        
        if risk_score >= 70:
            risk_level = 'Critical'
        elif risk_score >= 50:
            risk_level = 'High'
        elif risk_score >= 30:
            risk_level = 'Medium'
        else:
            risk_level = 'Low'
        
        return {
            'contract_address': contract_address,
            'chain_id': chain_id,
            'chain_name': self.chain_names.get(chain_id, f'Chain {chain_id}'),
            'token_name': token_data.get('token_name', 'Unknown'),
            'token_symbol': token_data.get('token_symbol', 'Unknown'),
            'is_open_source': token_data.get('is_open_source', '0') == '1',
            'is_proxy': token_data.get('is_proxy', '0') == '1',
            'is_mintable': token_data.get('is_mintable', '0') == '1',
            'owner_address': token_data.get('owner_address', 'Unknown'),
            'owner_balance': float(token_data.get('owner_balance', '0') or 0),
            'owner_percent': owner_percent,
            'is_blacklist': token_data.get('is_blacklist', '0') == '1',
            'is_whitelist': token_data.get('is_whitelist', '0') == '1',
            'is_honeypot': token_data.get('is_honeypot', '0') == '1',
            'risk_level': risk_level,
            'risk_score': min(risk_score, 100),
            'risk_factors': risk_factors,
            'scan_time': datetime.now().isoformat()
        }
    
    def scan_multiple(self, contracts):
        """扫描多个合约"""
        if self.use_demo_data:
            return self._get_demo_data()
        
        results = []
        for contract in contracts:
            result = self.scan_contract(
                contract['address'],
                contract.get('chain_id', 1)
            )
            if result:
                results.append(result)
        
        return results
    
    def generate_markdown(self, results):
        """生成 Markdown 报告"""
        if not results:
            return """## Contract Security Scanner

**Status**: No contracts scanned.
"""
        
        md = """## Contract Security Scanner

| Contract | Chain | Token | Open Source | Proxy | Mintable | Risk Level |
|----------|-------|-------|-------------|-------|----------|------------|
"""
        
        for r in results:
            os_status = "Yes" if r['is_open_source'] else "No"
            proxy_status = "Yes" if r['is_proxy'] else "No"
            mint_status = "Yes" if r['is_mintable'] else "No"
            md += f"| `{r['contract_address'][:20]}...` | {r['chain_name']} | {r['token_symbol']} | {os_status} | {proxy_status} | {mint_status} | {r['risk_level']} ({r['risk_score']}/100) |\n"
        
        return md
    
    def generate_html(self, results):
        """生成 HTML 报告"""
        if not results:
            return """<div class="section">
<h2>Contract Security Scanner</h2>
<p><strong>Status</strong>: No contracts scanned.</p>
</div>"""
        
        html = """<div class="section">
<h2>Contract Security Scanner</h2>
<table>
<thead>
<tr><th>Contract</th><th>Chain</th><th>Token</th><th>Open Source</th><th>Proxy</th><th>Mintable</th><th>Risk Level</th></tr>
</thead>
<tbody>
"""
        
        for r in results:
            os_status = "Yes" if r['is_open_source'] else "No"
            proxy_status = "Yes" if r['is_proxy'] else "No"
            mint_status = "Yes" if r['is_mintable'] else "No"
            html += f"""<tr>
<td><code>{r['contract_address'][:20]}...</code></td>
<td>{r['chain_name']}</td>
<td>{r['token_symbol']}</td>
<td>{os_status}</td>
<td>{proxy_status}</td>
<td>{mint_status}</td>
<td><strong>{r['risk_level']}</strong><br><small>({r['risk_score']}/100)</small></td>
</tr>"""
        
        html += "</tbody></table></div>"
        return html


def main():
    print("=" * 70)
    print("CONTRACT SECURITY SCANNER")
    print("=" * 70)
    
    scanner = ContractScanner(use_demo_data=False)
    contracts = [
        {'address': '0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb5', 'chain_id': 1},
        {'address': '0x8ba1fb1c8b2c0b8f1a2c3d4e5f6a7b8c9d0e1f2a', 'chain_id': 56}
    ]
    
    results = scanner.scan_multiple(contracts)
    print(f"\n[INFO] Scanned {len(results)} contracts")
    print(scanner.generate_markdown(results))


if __name__ == "__main__":
    main()
