#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module 3: Contract Security Scanner
使用 GoPlus API 检测代币合约安全风险
"""

import requests
import urllib3
import json
import time
from datetime import datetime
from pathlib import Path

# Disable SSL warnings for China network environment
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# GoPlus API 配置
GOPLUS_API_BASE = "https://api.gopluslabs.io/api/v1/token_security"

# 链 ID 映射
CHAIN_IDS = {
    'ethereum': 1,
    'bsc': 56,
    'polygon': 137,
    'arbitrum': 42161,
    'optimism': 10,
    'avalanche': 43114,
    'fantom': 250,
    'base': 8453
}


class ContractScanner:
    """合约安全扫描器"""
    
    def __init__(self, use_demo_data=False):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json'
        })
        self.use_demo_data = use_demo_data
    
    def scan_contract(self, contract_address, chain='ethereum'):
        """
        扫描单个合约的安全风险
        
        Args:
            contract_address: 合约地址
            chain: 链名称或链 ID
            
        Returns:
            dict: 扫描结果
        """
        if self.use_demo_data:
            return self._get_demo_result(contract_address, chain)
        
        try:
            # 获取链 ID
            if isinstance(chain, str):
                chain_id = CHAIN_IDS.get(chain.lower(), 1)
            else:
                chain_id = chain
            
            print(f"[INFO] Scanning contract {contract_address} on chain {chain_id}...")
            
            # GoPlus API 调用 - with SSL verification disabled for China network
            url = f"{GOPLUS_API_BASE}/{chain_id}"
            params = {'contract_addresses': contract_address}
            
            resp = self.session.get(url, params=params, timeout=15, verify=False)
            resp.raise_for_status()
            data = resp.json()
            
            if data.get('code') != 1:
                print(f"[WARNING] GoPlus API returned code {data.get('code')}")
                return self._parse_error_result(contract_address, chain)
            
            # 解析结果
            result_data = data.get('result', {})
            contract_data = result_data.get(contract_address.lower(), {})
            
            if not contract_data:
                print(f"[WARNING] No data returned for contract {contract_address}")
                return self._parse_error_result(contract_address, chain)
            
            return self._parse_scan_result(contract_address, chain, contract_data)
            
        except requests.exceptions.RequestException as e:
            print(f"[ERROR] GoPlus API request failed: {e}")
            return self._parse_error_result(contract_address, chain, str(e))
        except Exception as e:
            print(f"[ERROR] Unexpected error: {e}")
            return self._parse_error_result(contract_address, chain, str(e))
    
    def _parse_scan_result(self, contract_address, chain, data):
        """解析扫描结果"""
        issues = []
        warnings = []
        
        # 关键风险项
        risk_checks = {
            'is_honeypot': ('Honeypot detected', 'critical'),
            'cannot_buy': ('Cannot buy tokens', 'critical'),
            'cannot_sell_all': ('Cannot sell all tokens', 'critical'),
            'hidden_owner': ('Hidden owner (can mint unlimited)', 'critical'),
            'is_mintable': ('Contract can mint new tokens', 'high'),
            'transfer_pausable': ('Transfer can be paused by owner', 'high'),
            'trading_cooldown': ('Trading cooldown enabled', 'medium'),
            'is_anti_whale': ('Anti-whale mechanism detected', 'medium'),
            'is_blacklisted': ('Blacklist function exists', 'medium'),
            'is_whitelisted': ('Whitelist function exists', 'low'),
            'slippage_modifiable': ('Slippage can be modified', 'medium'),
            'is_proxy': ('Proxy contract (upgradeable)', 'low'),
            'owner_change_balance': ('Owner can change balance', 'critical'),
            'selfdestruct': ('Contract can self-destruct', 'critical')
        }
        
        for key, (message, level) in risk_checks.items():
            value = data.get(key, '0')
            if value == '1' or value == 1 or value == True:
                if level == 'critical':
                    issues.append({'type': 'critical', 'message': message})
                elif level == 'high':
                    issues.append({'type': 'high', 'message': message})
                elif level == 'medium':
                    warnings.append({'type': 'medium', 'message': message})
                else:
                    warnings.append({'type': 'low', 'message': message})
        
        # 计算风险分数
        risk_score = 0
        risk_score += len([i for i in issues if i['type'] == 'critical']) * 30
        risk_score += len([i for i in issues if i['type'] == 'high']) * 20
        risk_score += len([i for i in issues if i['type'] == 'medium']) * 10
        risk_score += len([i for i in issues if i['type'] == 'low']) * 5
        risk_score = min(risk_score, 100)
        
        # 确定风险等级
        if risk_score >= 70:
            risk_level = "🔴 Critical"
        elif risk_score >= 50:
            risk_level = "🟠 High"
        elif risk_score >= 30:
            risk_level = "🟡 Medium"
        elif risk_score >= 10:
            risk_level = "🟢 Low"
        else:
            risk_level = "✅ Safe"
        
        # 获取基本信息
        token_name = data.get('token_name', 'Unknown')
        token_symbol = data.get('token_symbol', 'Unknown')
        holder_count = data.get('holder_count', 'N/A')
        total_supply = data.get('total_supply', 'N/A')
        
        # 获取持有者分布
        holders = data.get('holders', [])
        top_holders = []
        for i, holder in enumerate(holders[:5]):
            top_holders.append({
                'address': holder.get('address', 'Unknown')[:20] + '...',
                'balance': holder.get('balance', '0'),
                'percent': holder.get('percent', '0%')
            })
        
        return {
            'contract_address': contract_address,
            'chain': chain,
            'token_name': token_name,
            'token_symbol': token_symbol,
            'risk_score': risk_score,
            'risk_level': risk_level,
            'issues': issues,
            'warnings': warnings,
            'holder_count': holder_count,
            'total_supply': total_supply,
            'top_holders': top_holders,
            'scan_time': datetime.now().isoformat(),
            'status': 'success'
        }
    
    def _parse_error_result(self, contract_address, chain, error_msg=None):
        """解析错误结果"""
        return {
            'contract_address': contract_address,
            'chain': chain,
            'token_name': 'Unknown',
            'token_symbol': 'Unknown',
            'risk_score': 0,
            'risk_level': "⚠️ Error",
            'issues': [],
            'warnings': [],
            'error': error_msg or 'Failed to scan contract',
            'scan_time': datetime.now().isoformat(),
            'status': 'error'
        }
    
    def _get_demo_result(self, contract_address, chain):
        """获取演示扫描结果"""
        # 根据地址生成不同的演示结果
        if '1234' in contract_address:
            return {
                'contract_address': contract_address,
                'chain': chain,
                'token_name': 'MoonRocket Token',
                'token_symbol': 'MOON',
                'risk_score': 95,
                'risk_level': "🔴 Critical",
                'issues': [
                    {'type': 'critical', 'message': 'Honeypot detected'},
                    {'type': 'critical', 'message': 'Hidden owner (can mint unlimited)'},
                    {'type': 'high', 'message': 'Transfer can be paused by owner'}
                ],
                'warnings': [
                    {'type': 'medium', 'message': 'Trading cooldown enabled'},
                    {'type': 'low', 'message': 'Proxy contract (upgradeable)'}
                ],
                'holder_count': 45,
                'total_supply': '1,000,000,000',
                'top_holders': [
                    {'address': '0x1234...5678', 'balance': '500,000,000', 'percent': '50%'},
                    {'address': '0xabcd...efgh', 'balance': '200,000,000', 'percent': '20%'},
                ],
                'scan_time': datetime.now().isoformat(),
                'status': 'success'
            }
        elif 'abcd' in contract_address:
            return {
                'contract_address': contract_address,
                'chain': chain,
                'token_name': 'SafeVault Finance',
                'token_symbol': 'SVF',
                'risk_score': 45,
                'risk_level': "🟡 Medium",
                'issues': [
                    {'type': 'high', 'message': 'Contract can mint new tokens'}
                ],
                'warnings': [
                    {'type': 'medium', 'message': 'Anti-whale mechanism detected'},
                    {'type': 'low', 'message': 'Whitelist function exists'}
                ],
                'holder_count': 1250,
                'total_supply': '10,000,000',
                'top_holders': [
                    {'address': '0x1111...2222', 'balance': '2,000,000', 'percent': '20%'},
                    {'address': '0x3333...4444', 'balance': '1,500,000', 'percent': '15%'},
                ],
                'scan_time': datetime.now().isoformat(),
                'status': 'success'
            }
        else:
            return {
                'contract_address': contract_address,
                'chain': chain,
                'token_name': 'GreenChart Token',
                'token_symbol': 'GREEN',
                'risk_score': 5,
                'risk_level': "✅ Safe",
                'issues': [],
                'warnings': [
                    {'type': 'low', 'message': 'Proxy contract (upgradeable)'}
                ],
                'holder_count': 8500,
                'total_supply': '100,000,000',
                'top_holders': [
                    {'address': '0xaaaa...bbbb', 'balance': '10,000,000', 'percent': '10%'},
                    {'address': '0xcccc...dddd', 'balance': '8,000,000', 'percent': '8%'},
                ],
                'scan_time': datetime.now().isoformat(),
                'status': 'success'
            }
    
    def scan_multiple(self, contracts):
        """
        批量扫描多个合约
        
        Args:
            contracts: 列表，每项为 (address, chain) 元组
            
        Returns:
            list: 扫描结果列表
        """
        results = []
        for i, (address, chain) in enumerate(contracts):
            result = self.scan_contract(address, chain)
            results.append(result)
            
            # 避免请求过快
            if i < len(contracts) - 1:
                time.sleep(1)
        
        return results
    
    def generate_markdown(self, results):
        """生成 Markdown 格式的报告"""
        if not results:
            return """## 🔒 Contract Security Scan

**Status**: No contracts scanned.
"""
        
        md = """## 🔒 Contract Security Scan

**⚠️ Important**: This scan provides automated risk assessment only. 
Always conduct additional due diligence before investing.

| Token | Chain | Risk Level | Issues | Warnings | Holders |
|-------|-------|------------|--------|----------|---------|
"""
        
        for result in results:
            token = f"**{result['token_symbol']}** ({result['token_name'][:20]})"
            chain = result['chain']
            risk = result['risk_level']
            issues = len(result.get('issues', []))
            warnings = len(result.get('warnings', []))
            holders = result.get('holder_count', 'N/A')
            
            md += f"| {token} | {chain} | {risk} | {issues} | {warnings} | {holders} |\n"
        
        md += """
### Detailed Analysis

"""
        
        for i, result in enumerate(results, 1):
            md += f"**{i}. {result['token_symbol']} ({result['token_name']})** - {result['risk_level']}\n\n"
            
            if result.get('status') == 'error':
                md += f"- ⚠️ **Error**: {result.get('error', 'Unknown error')}\n"
            else:
                md += f"- **Contract**: `{result['contract_address']}`\n"
                md += f"- **Chain**: {result['chain']}\n"
                md += f"- **Holders**: {result.get('holder_count', 'N/A')}\n"
                md += f"- **Total Supply**: {result.get('total_supply', 'N/A')}\n\n"
                
                if result.get('issues'):
                    md += "**Critical Issues:**\n"
                    for issue in result['issues']:
                        icon = "🔴" if issue['type'] == 'critical' else "🟠"
                        md += f"- {icon} {issue['message']}\n"
                    md += "\n"
                
                if result.get('warnings'):
                    md += "**Warnings:**\n"
                    for warning in result['warnings']:
                        icon = "🟡" if warning['type'] == 'medium' else "🟢"
                        md += f"- {icon} {warning['message']}\n"
                    md += "\n"
                
                if result.get('top_holders'):
                    md += "**Top Holders:**\n"
                    for holder in result['top_holders'][:3]:
                        md += f"- `{holder['address']}`: {holder['balance']} ({holder['percent']})\n"
                    md += "\n"
            
            md += "---\n\n"
        
        md += """### Risk Level Guide

- 🔴 **Critical**: Multiple severe risks detected. High probability of scam or honeypot.
- 🟠 **High**: Significant risks present. Exercise extreme caution.
- 🟡 **Medium**: Some risks detected. Additional research recommended.
- 🟢 **Low**: Minor concerns only. Relatively safer but still DYOR.
- ✅ **Safe**: No major risks detected. Standard due diligence still required.

### Common Risk Indicators

**Critical**:
- Honeypot (can buy but not sell)
- Hidden owner with minting privileges
- Owner can change balances
- Self-destruct function

**High**:
- Mintable supply
- Pausable transfers
- Modifiable slippage

**Medium**:
- Trading cooldowns
- Anti-whale mechanisms
- Blacklist functions

*Data source: GoPlus Security API | Last updated: {}*
""".format(datetime.now().strftime('%Y-%m-%d %H:%M UTC'))
        
        return md
    
    def generate_html(self, results):
        """生成 HTML 格式的报告"""
        if not results:
            return """<div class="section">
<h2>🔒 Contract Security Scan</h2>
<p><strong>Status</strong>: No contracts scanned.</p>
</div>"""
        
        html = """<div class="section">
<h2>🔒 Contract Security Scan</h2>
<p><strong>⚠️ Important</strong>: This scan provides automated risk assessment only. 
Always conduct additional due diligence before investing.</p>

<table>
<thead>
<tr>
<th>Token</th>
<th>Chain</th>
<th>Risk Level</th>
<th>Issues</th>
<th>Warnings</th>
<th>Holders</th>
</tr>
</thead>
<tbody>
"""
        
        for result in results:
            html += f"""<tr>
<td><strong>{result['token_symbol']}</strong><br><small>{result['token_name'][:20]}</small></td>
<td>{result['chain']}</td>
<td><strong>{result['risk_level']}</strong></td>
<td>{len(result.get('issues', []))}</td>
<td>{len(result.get('warnings', []))}</td>
<td>{result.get('holder_count', 'N/A')}</td>
</tr>
"""
        
        html += """</tbody>
</table>

<h3>Detailed Analysis</h3>
"""
        
        for i, result in enumerate(results, 1):
            html += f"""<div class="contract-item">
<p><strong>{i}. {result['token_symbol']} ({result['token_name']})</strong> - {result['risk_level']}</p>
"""
            
            if result.get('status') == 'error':
                html += f"<p>⚠️ <strong>Error</strong>: {result.get('error', 'Unknown error')}</p>"
            else:
                html += f"""<ul>
<li><strong>Contract</strong>: <code>{result['contract_address']}</code></li>
<li><strong>Chain</strong>: {result['chain']}</li>
<li><strong>Holders</strong>: {result.get('holder_count', 'N/A')}</li>
<li><strong>Total Supply</strong>: {result.get('total_supply', 'N/A')}</li>
</ul>
"""
                
                if result.get('issues'):
                    html += "<p><strong>Critical Issues:</strong></p><ul>"
                    for issue in result['issues']:
                        icon = "🔴" if issue['type'] == 'critical' else "🟠"
                        html += f"<li>{icon} {issue['message']}</li>"
                    html += "</ul>"
                
                if result.get('warnings'):
                    html += "<p><strong>Warnings:</strong></p><ul>"
                    for warning in result['warnings']:
                        icon = "🟡" if warning['type'] == 'medium' else "🟢"
                        html += f"<li>{icon} {warning['message']}</li>"
                    html += "</ul>"
                
                if result.get('top_holders'):
                    html += "<p><strong>Top Holders:</strong></p><ul>"
                    for holder in result['top_holders'][:3]:
                        html += f"<li><code>{holder['address']}</code>: {holder['balance']} ({holder['percent']})</li>"
                    html += "</ul>"
            
            html += "</div>"
        
        html += """<h3>Risk Level Guide</h3>
<ul>
<li>🔴 <strong>Critical</strong>: Multiple severe risks. High probability of scam.</li>
<li>🟠 <strong>High</strong>: Significant risks present. Exercise extreme caution.</li>
<li>🟡 <strong>Medium</strong>: Some risks detected. Additional research recommended.</li>
<li>🟢 <strong>Low</strong>: Minor concerns only. Relatively safer but still DYOR.</li>
<li>✅ <strong>Safe</strong>: No major risks detected. Standard due diligence required.</li>
</ul>

<p><em>Data source: GoPlus Security API | Last updated: {}</em></p>
</div>
""".format(datetime.now().strftime('%Y-%m-%d %H:%M UTC'))
        
        return html


def main():
    """主函数 - 用于测试"""
    print("=" * 70)
    print("CONTRACT SECURITY SCANNER")
    print("=" * 70)
    
    scanner = ContractScanner(use_demo_data=True)
    
    # 测试扫描多个合约
    test_contracts = [
        ('0x1234567890abcdef1234567890abcdef12345678', 'ethereum'),
        ('0xabcdef1234567890abcdef1234567890abcdef12', 'bsc'),
        ('0x9876543210fedcba9876543210fedcba98765432', 'ethereum')
    ]
    
    results = scanner.scan_multiple(test_contracts)
    
    print(f"\n[INFO] Scanned {len(results)} contracts")
    
    print("\n" + "-" * 70)
    print("MARKDOWN OUTPUT:")
    print("-" * 70)
    print(scanner.generate_markdown(results))


if __name__ == "__main__":
    main()
