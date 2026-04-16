#!/usr/bin/env python3
"""
API Connectivity Test - v9.0 System Validation
测试所有 API 连接和数据获取
"""

import requests
import json
import sys
from datetime import datetime

# API 端点
APIS = {
    "GoPlus Security": {
        "url": "https://api.gopluslabs.io/api/v1/token_security/1",
        "params": {"contract_addresses": "0x1f9840a85d5af5bf1d1762f925bdaddc4201f984"},  # UNI token
        "method": "GET"
    },
    "DEX Screener": {
        "url": "https://api.dexscreener.com/latest/dex/tokens/0x1f9840a85d5af5bf1d1762f925bdaddc4201f984",
        "method": "GET"
    },
    "CoinGecko": {
        "url": "https://api.coingecko.com/api/v3/coins/markets",
        "params": {"vs_currency": "usd", "ids": "bitcoin,ethereum", "per_page": 2},
        "method": "GET"
    },
    "Etherscan": {
        "url": "https://api.etherscan.io/api",
        "params": {"module": "stats", "action": "ethprice", "apikey": "YourApiKey"},
        "method": "GET"
    }
}


def test_api(name, config):
    """测试单个 API"""
    print(f"\n{'='*70}")
    print(f"[TEST] {name}")
    print(f"{'='*70}")
    print(f"URL: {config['url']}")
    
    try:
        if config['method'] == 'GET':
            resp = requests.get(
                config['url'],
                params=config.get('params', {}),
                timeout=30
            )
        
        print(f"Status: {resp.status_code}")
        
        if resp.status_code == 200:
            data = resp.json()
            print(f"[OK] API accessible")
            
            # 检查数据完整性
            if name == "GoPlus Security":
                if data.get('code') == 200:
                    print(f"[OK] Data format valid")
                    token_data = data.get('data', {}).get('0x1f9840a85d5af5bf1d1762f925bdaddc4201f984'.lower(), {})
                    print(f"  - Honeypot: {token_data.get('is_honeypot', 'N/A')}")
                    print(f"  - Sell Tax: {token_data.get('sell_tax', 'N/A')}")
                    print(f"  - Verified: {token_data.get('is_open_source', 'N/A')}")
                else:
                    print(f"[WARN] API returned error code: {data.get('code')}")
                    
            elif name == "DEX Screener":
                pairs = data.get('pairs', [])
                print(f"[OK] Found {len(pairs)} trading pairs")
                if pairs:
                    pair = pairs[0]
                    print(f"  - DEX: {pair.get('dexId', 'N/A')}")
                    print(f"  - Liquidity: ${pair.get('liquidity', {}).get('usd', 0):,.0f}")
                    print(f"  - 24h Volume: ${pair.get('volume', {}).get('h24', 0):,.0f}")
                    
            elif name == "CoinGecko":
                if isinstance(data, list) and len(data) > 0:
                    print(f"[OK] Found {len(data)} coins")
                    for coin in data[:2]:
                        print(f"  - {coin.get('symbol', 'N/A')}: ${coin.get('current_price', 0):,.2f}")
                else:
                    print(f"[WARN] Unexpected data format")
                    
            elif name == "Etherscan":
                if data.get('status') == '1':
                    print(f"[OK] API key valid")
                    result = data.get('result', {})
                    print(f"  - ETH Price: ${result.get('ethusd', 'N/A')}")
                else:
                    print(f"[WARN] API key issue or rate limit: {data.get('message', 'Unknown')}")
            
            return True
        else:
            print(f"[ERROR] HTTP {resp.status_code}")
            print(f"Response: {resp.text[:200]}")
            return False
            
    except requests.exceptions.Timeout:
        print(f"[ERROR] Timeout after 30s")
        return False
    except requests.exceptions.ConnectionError:
        print(f"[ERROR] Connection failed")
        return False
    except Exception as e:
        print(f"[ERROR] {type(e).__name__}: {str(e)}")
        return False


def test_token_research_framework():
    """测试 Token Research Framework"""
    print(f"\n{'='*70}")
    print(f"[TEST] Token Research Framework")
    print(f"{'='*70}")
    
    sys.path.insert(0, r'F:\stepclaw\agents\blockchain-analyst')
    
    try:
        from token_research_framework import (
            TokenResearcher, TokenResearchReport,
            ContractRisk, HolderDistribution, LiquidityManagement,
            DeveloperAssociation, MarketingNarrative
        )
        
        print("[OK] All modules imported successfully")
        
        # 测试数据类创建
        contract = ContractRisk(
            is_honeypot=True,
            sell_tax=15.0,
            has_hidden_owner=True,
            is_open_source=False
        )
        print(f"[OK] ContractRisk created: score={contract.risk_score()}")
        
        holder = HolderDistribution(top10_percentage=78.5, total_holders=156)
        print(f"[OK] HolderDistribution created: score={holder.risk_score()}")
        
        liquidity = LiquidityManagement(liquidity_locked=False, liquidity_usd=45000)
        print(f"[OK] LiquidityManagement created: score={liquidity.risk_score()}")
        
        dev = DeveloperAssociation(team_doxxed=False, has_whitepaper=False)
        print(f"[OK] DeveloperAssociation created: score={dev.risk_score()}")
        
        marketing = MarketingNarrative(promises_high_returns=True)
        print(f"[OK] MarketingNarrative created: score={marketing.risk_score()}")
        
        # 测试完整报告
        report = TokenResearchReport(
            token_symbol="TEST",
            contract_address="0x1234...",
            chain="1",
            timestamp=datetime.now().isoformat(),
            contract_risk=contract,
            holder_distribution=holder,
            liquidity_management=liquidity,
            developer_association=dev,
            marketing_narrative=marketing
        )
        report.calculate_overall_risk()
        print(f"[OK] Full report generated: score={report.overall_risk_score}, level={report.risk_level}")
        
        return True
        
    except Exception as e:
        print(f"[ERROR] {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_case_study_manager():
    """测试 Case Study Manager"""
    print(f"\n{'='*70}")
    print(f"[TEST] Case Study Manager")
    print(f"{'='*70}")
    
    sys.path.insert(0, r'F:\stepclaw\agents\blockchain-analyst')
    
    try:
        from case_study_manager import CaseStudyManager
        
        manager = CaseStudyManager()
        print("[OK] CaseStudyManager initialized")
        
        # 测试添加案例
        case_id = manager.add_case(
            token_symbol="TEST",
            contract_address="0x1234567890abcdef",
            chain="ETH",
            risk_level="[CRIT] Extreme Risk",
            classification="Ignore Directly",
            key_signals=["honeypot", "high tax"],
            summary="Test case",
            claimed="Test claim",
            reality="Test reality"
        )
        print(f"[OK] Test case added: {case_id}")
        
        return True
        
    except Exception as e:
        print(f"[ERROR] {type(e).__name__}: {str(e)}")
        return False


def generate_test_report():
    """生成测试报告"""
    print(f"\n{'='*70}")
    print(f"[TEST] Generate Sample Report")
    print(f"{'='*70}")
    
    sys.path.insert(0, r'F:\stepclaw\agents\blockchain-analyst')
    
    try:
        from token_research_framework import (
            TokenResearchReport, ContractRisk, HolderDistribution,
            LiquidityManagement, DeveloperAssociation, MarketingNarrative
        )
        from datetime import datetime
        
        report = TokenResearchReport(
            token_symbol="TESTAPI",
            contract_address="0xTestAddress",
            chain="1",
            timestamp=datetime.now().isoformat(),
            contract_risk=ContractRisk(is_honeypot=True, sell_tax=15.0),
            holder_distribution=HolderDistribution(top10_percentage=70.0),
            liquidity_management=LiquidityManagement(liquidity_locked=False),
            developer_association=DeveloperAssociation(team_doxxed=False),
            marketing_narrative=MarketingNarrative(promises_high_returns=True)
        )
        report.calculate_overall_risk()
        
        # 保存报告
        output_path = r"F:\stepclaw\agents\blockchain-analyst\output\test_report_api.md"
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(report.generate_fact_sheet())
        
        print(f"[OK] Test report saved: {output_path}")
        print(f"  - Score: {report.overall_risk_score}/100")
        print(f"  - Level: {report.risk_level}")
        
        return True
        
    except Exception as e:
        print(f"[ERROR] {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """主测试函数"""
    print("\n" + "="*70)
    print("Crypto Risk Radar v9.0 - API Connectivity Test")
    print("="*70)
    print(f"Time: {datetime.now().isoformat()}")
    print()
    
    results = {}
    
    # 测试 API 连接
    print("\n[PHASE 1] Testing API Connectivity")
    for name, config in APIS.items():
        results[name] = test_api(name, config)
    
    # 测试框架
    print("\n[PHASE 2] Testing Token Research Framework")
    results["Framework"] = test_token_research_framework()
    
    # 测试案例管理
    print("\n[PHASE 3] Testing Case Study Manager")
    results["Case Manager"] = test_case_study_manager()
    
    # 生成测试报告
    print("\n[PHASE 4] Generating Sample Report")
    results["Report Gen"] = generate_test_report()
    
    # 汇总结果
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for name, status in results.items():
        status_str = "[OK] PASS" if status else "[ERR] FAIL"
        print(f"  {status_str}: {name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n[OK] All systems operational!")
    else:
        print(f"\n[WARN] {total - passed} test(s) failed. Check details above.")
    
    print("="*70)


if __name__ == "__main__":
    main()
