#!/usr/bin/env python3
"""
v9.0 Demo - 真实数据测试演示
使用模拟数据展示完整人机合作流程
"""

import json
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, r'F:\stepclaw\agents\blockchain-analyst')

from token_research_framework import TokenResearcher, TokenResearchReport
from human_in_the_loop import HumanInTheLoop, TodoItem


def create_demo_candidates():
    """创建演示候选代币（基于真实市场模式）"""
    return [
        {
            "address": "0x742d35Cc6634C0532925a3b844Bc9e7595f8dEe",
            "chain": "1",
            "symbol": "FAKEAI",
            "name": "Fake AI Token",
            "liquidity_usd": 45000,
            "volume_24h": 320000,
            "price_usd": 0.0001,
            "price_change_24h": 450,
            "risk_score": 85,
            "risk_level": "[CRIT] Extreme"
        },
        {
            "address": "0x8ba1fb10955d9e5b2e6a7e7e6e6e6e6e6e6e6e6e",
            "chain": "1",
            "symbol": "RUGPULL",
            "name": "Rug Pull Coin",
            "liquidity_usd": 28000,
            "volume_24h": 150000,
            "price_usd": 0.00005,
            "price_change_24h": -60,
            "risk_score": 92,
            "risk_level": "[CRIT] Extreme"
        },
        {
            "address": "0x1f9840a85d5af5bf1d1762f925bdaddc4201f984",
            "chain": "1",
            "symbol": "SUSPECT",
            "name": "Suspicious Finance",
            "liquidity_usd": 120000,
            "volume_24h": 85000,
            "price_usd": 0.001,
            "price_change_24h": 25,
            "risk_score": 65,
            "risk_level": "[HIGH] High"
        },
        {
            "address": "0x6b175474e89094c44da98b954eedeac495271d0f",
            "chain": "1",
            "symbol": "OBSERVE",
            "name": "Observe Token",
            "liquidity_usd": 250000,
            "volume_24h": 45000,
            "price_usd": 0.01,
            "price_change_24h": 5,
            "risk_score": 45,
            "risk_level": "[MED] Medium"
        },
        {
            "address": "0xa0b86a33e6c16f5a1c8d1c3e5f8a9b2c4d6e7f8a",
            "chain": "1",
            "symbol": "STUDY",
            "name": "Study Coin",
            "liquidity_usd": 500000,
            "volume_24h": 120000,
            "price_usd": 0.1,
            "price_change_24h": 2,
            "risk_score": 25,
            "risk_level": "[LOW] Low"
        }
    ]


def demo_research_fakedai():
    """演示 FAKEAI 代币的完整研究"""
    print("\n" + "="*70)
    print("[RESEARCH] FAKEAI Token Deep Analysis")
    print("="*70)
    
    from token_research_framework import ContractRisk, HolderDistribution, LiquidityManagement, DeveloperAssociation, MarketingNarrative
    
    # 模拟研究报告（基于真实风险模式）
    contract_risk = ContractRisk(
        is_honeypot=True,
        sell_tax=15.0,
        buy_tax=0.0,
        has_hidden_owner=True,
        is_open_source=False,
        is_mintable=True,
        can_take_back_ownership=True,
        owner_address="0x742d..."
    )
    
    holder_dist = HolderDistribution(
        top10_percentage=78.5,
        top50_percentage=95.2,
        total_holders=156,
        new_wallets_24h=89
    )
    
    liquidity = LiquidityManagement(
        liquidity_locked=False,
        lock_duration_days=0,
        liquidity_usd=45000,
        lp_holder_count=3
    )
    
    dev_assoc = DeveloperAssociation(
        team_doxxed=False,
        has_website=True,
        has_whitepaper=False,
        social_media_count=1,
        developer_wallet_activity="suspicious"
    )
    
    marketing = MarketingNarrative(
        promises_high_returns=True,
        uses_viral_marketing=True,
        has_celebrity_endorsement=False,
        narrative_consistency="contradictory"
    )
    
    report = TokenResearchReport(
        token_symbol="FAKEAI",
        contract_address="0x742d35Cc6634C0532925a3b844Bc9e7595f8dEe",
        chain="1",
        timestamp=datetime.now().isoformat(),
        contract_risk=contract_risk,
        holder_distribution=holder_dist,
        liquidity_management=liquidity,
        developer_association=dev_assoc,
        marketing_narrative=marketing
    )
    
    # 计算综合风险
    report.calculate_overall_risk()
    
    # 显示完整报告
    print(report.generate_fact_sheet())
    
    return report


def demo_todo_list():
    """演示待办列表"""
    print("\n" + "="*70)
    print("[TODO] Token Analysis Todo List")
    print("="*70)
    
    candidates = create_demo_candidates()
    
    print(f"\nFound {len(candidates)} candidate tokens, sorted by risk level:\n")
    
    for i, token in enumerate(candidates, 1):
        print(f"{i}. {token['symbol']} - {token['risk_level']}")
        print(f"   Liquidity: ${token['liquidity_usd']:,.0f} | 24h Volume: ${token['volume_24h']:,.0f}")
        print(f"   24h Price Change: {token['price_change_24h']:+.1f}%")
        print(f"   Risk Score: {token['risk_score']}/100")
        print()
    
    print("-"*70)
    print("Action Options:")
    print("  [1-5] Select token for deep research")
    print("  [C]   Quick classify (based on auto-detection)")
    print("  [S]   View statistics")
    print("  [Q]   Save and exit")
    print("-"*70)


def demo_case_study():
    """演示案例库"""
    print("\n" + "="*70)
    print("[CASE] Case Study Database (Public Summary Mode)")
    print("="*70)
    
    from case_study_manager import CaseStudyManager
    
    manager = CaseStudyManager()
    
    # 添加演示案例
    case_id = manager.add_case(
        token_symbol="FAKEAI",
        contract_address="0x742d35Cc6634C0532925a3b844Bc9e7595f8dEe",
        chain="ETH",
        risk_level="[CRIT] Extreme Risk",
        classification="Ignore Directly",
        key_signals=[
            "honeypot detected",
            "15% sell tax",
            "liquidity not locked",
            "anonymous team",
            "contradictory narrative"
        ],
        summary="Typical high-risk scam token with honeypot in contract, top 10 holders own 78.5%, liquidity only $45k and unlocked.",
        claimed="AI-powered next-gen blockchain, listing on Binance soon, early investors get 100x returns",
        reality="Honeypot detected - investors cannot sell; team wallets bought heavily before shilling; liquidity can be withdrawn anytime",
        detailed_analysis="Full technical analysis...",
        transaction_hashes=["0xabc123...", "0xdef456..."],
        wallet_addresses=["0x742d...", "0x9999..."],
        internal_notes="Internal investigation: Team linked to multiple Rug Pull projects"
    )
    
    print(f"\n[OK] Case {case_id} added to database")
    
    # 显示公开摘要
    case = manager.get_case(case_id)
    print("\n" + "="*70)
    print("[PUBLIC] Public Summary (Visible to All):")
    print("="*70)
    print(case.generate_public_summary())
    
    print("\n" + "="*70)
    print("[PRIVATE] Private Report (Internal Use Only):")
    print("="*70)
    print("[Contains full contract address, transaction hashes, wallet addresses]")
    print("[Not publicly disclosed to prevent bad actors from learning]")


def main():
    """主函数"""
    print("\n" + "="*70)
    print("[OK] Crypto Risk Radar v9.0 - Real Data Test")
    print("="*70)
    print("\nThis demo uses simulated data to show the human-in-the-loop workflow")
    print("In production, it connects to DEX Screener / GoPlus API for real data\n")
    
    # 1. 显示待办列表
    demo_todo_list()
    
    # 2. 演示深度研究
    report = demo_research_fakedai()
    
    # 3. 演示案例库
    demo_case_study()
    
    print("\n" + "="*70)
    print("[OK] Demo Complete!")
    print("="*70)
    print("\nHow to use:")
    print("  python human_in_the_loop.py")
    print("\nThis launches the CLI interface where you can:")
    print("  1. Discover new tokens")
    print("  2. Select tokens for deep research")
    print("  3. View 5-vulnerability analysis report")
    print("  4. Confirm classification and save to case study database")


if __name__ == "__main__":
    main()
