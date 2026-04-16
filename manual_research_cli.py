#!/usr/bin/env python3
"""
Manual Research CLI - Human-in-the-Loop Interface
人工查询 + AI 处理的协作模式
"""

import sys
import json
from datetime import datetime
from pathlib import Path

sys.path.insert(0, r'F:\stepclaw\agents\blockchain-analyst')

from token_research_framework import (
    TokenResearchReport, ContractRisk, HolderDistribution,
    LiquidityManagement, DeveloperAssociation, MarketingNarrative
)
from case_study_manager import CaseStudyManager


class ManualResearchCLI:
    """人工研究 CLI"""
    
    def __init__(self):
        self.case_manager = CaseStudyManager()
    
    def show_guide(self, token_address: str, chain: str = "1"):
        """显示查询指南"""
        print("\n" + "="*70)
        print("DATA COLLECTION GUIDE")
        print("="*70)
        print(f"\nToken: {token_address}")
        print(f"Chain: {chain}")
        print("\n" + "-"*70)
        print("STEP 1: GoPlus Security (Contract Safety)")
        print("-"*70)
        print(f"URL: https://gopluslabs.io/token-security/{chain}/{token_address}")
        print("\nCopy these fields:")
        print("  - Is Honeypot: (YES/NO)")
        print("  - Sell Tax: (X%)")
        print("  - Buy Tax: (X%)")
        print("  - Hidden Owner: (YES/NO)")
        print("  - Is Open Source: (YES/NO)")
        print("  - Is Mintable: (YES/NO)")
        print("  - Can Take Back Ownership: (YES/NO)")
        
        print("\n" + "-"*70)
        print("STEP 2: DEX Screener (Liquidity)")
        print("-"*70)
        chain_name = "ethereum" if chain == "1" else "bsc" if chain == "56" else "ethereum"
        print(f"URL: https://dexscreener.com/{chain_name}/{token_address}")
        print("\nCopy these fields:")
        print("  - Liquidity USD: ($X)")
        print("  - 24h Volume: ($X)")
        print("  - LP Locked: (YES/NO)")
        print("  - Lock Duration: (X days)")
        print("  - LP Holders: (X)")
        
        print("\n" + "-"*70)
        print("STEP 3: Etherscan (Holder Distribution)")
        print("-"*70)
        print(f"URL: https://etherscan.io/token/{token_address}#balances")
        print("\nCopy these fields:")
        print("  - Total Holders: (X)")
        print("  - Top 10 Holders %: (X%)")
        print("  - Top 50 Holders %: (X%)")
        
        print("\n" + "-"*70)
        print("STEP 4: Marketing Analysis (Manual)")
        print("-"*70)
        print("Visit the project's:")
        print("  - Website")
        print("  - Twitter/X")
        print("  - Telegram/Discord")
        print("\nNote:")
        print("  - Promises high returns? (YES/NO)")
        print("  - Uses viral marketing? (YES/NO)")
        print("  - Any claims vs reality contradictions?")
        
        print("\n" + "="*70)
        print("Paste the collected data below (or type 'skip' to use defaults):")
        print("="*70 + "\n")
    
    def parse_input(self, text: str) -> dict:
        """解析用户输入"""
        data = {
            'contract': {},
            'holder': {},
            'liquidity': {},
            'developer': {},
            'marketing': {}
        }
        
        lines = text.strip().split('\n')
        current_section = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # 检测章节
            if '[GoPlus]' in line or 'GoPlus' in line:
                current_section = 'contract'
                continue
            elif '[DEX]' in line or 'DEX' in line:
                current_section = 'liquidity'
                continue
            elif '[Etherscan]' in line or 'Etherscan' in line:
                current_section = 'holder'
                continue
            elif '[Marketing]' in line or 'Marketing' in line:
                current_section = 'marketing'
                continue
            elif '[Developer]' in line or 'Developer' in line:
                current_section = 'developer'
                continue
            
            # 解析键值对
            if ':' in line and current_section:
                key, value = line.split(':', 1)
                key = key.strip().lower().replace(' ', '_')
                value = value.strip()
                
                # 转换布尔值
                if value.upper() in ['YES', 'TRUE']:
                    value = True
                elif value.upper() in ['NO', 'FALSE']:
                    value = False
                else:
                    # 尝试转换为数字
                    try:
                        value = float(value.replace('%', '').replace('$', '').replace(',', ''))
                    except:
                        pass
                
                data[current_section][key] = value
        
        return data
    
    def create_report(self, token_symbol: str, token_address: str, 
                      chain: str, data: dict) -> TokenResearchReport:
        """创建研究报告"""
        
        # 合约风险
        contract = ContractRisk(
            is_honeypot=data['contract'].get('is_honeypot', False),
            sell_tax=data['contract'].get('sell_tax', 0),
            buy_tax=data['contract'].get('buy_tax', 0),
            has_hidden_owner=data['contract'].get('hidden_owner', False),
            is_open_source=data['contract'].get('is_open_source', False),
            is_mintable=data['contract'].get('is_mintable', False),
            can_take_back_ownership=data['contract'].get('can_take_back_ownership', False),
            owner_address=data['contract'].get('owner_address', '')
        )
        
        # 持仓分布
        holder = HolderDistribution(
            top10_percentage=data['holder'].get('top10_percentage', 0),
            top50_percentage=data['holder'].get('top50_percentage', 0),
            total_holders=int(data['holder'].get('total_holders', 0)),
            new_wallets_24h=int(data['holder'].get('new_wallets_24h', 0))
        )
        
        # 流动性管理
        liquidity = LiquidityManagement(
            liquidity_locked=data['liquidity'].get('lp_locked', False),
            lock_duration_days=int(data['liquidity'].get('lock_duration_days', 0)),
            liquidity_usd=data['liquidity'].get('liquidity_usd', 0),
            lp_holder_count=int(data['liquidity'].get('lp_holders', 0))
        )
        
        # 开发者关联
        developer = DeveloperAssociation(
            team_doxxed=data['developer'].get('team_doxxed', False),
            has_website=data['developer'].get('has_website', False),
            has_whitepaper=data['developer'].get('has_whitepaper', False),
            social_media_count=int(data['developer'].get('social_media_count', 0)),
            developer_wallet_activity=data['developer'].get('wallet_activity', 'unknown')
        )
        
        # 营销叙事
        marketing = MarketingNarrative(
            promises_high_returns=data['marketing'].get('promises_high_returns', False),
            uses_viral_marketing=data['marketing'].get('uses_viral_marketing', False),
            has_celebrity_endorsement=data['marketing'].get('has_celebrity_endorsement', False),
            narrative_consistency=data['marketing'].get('narrative_consistency', 'unknown')
        )
        
        # 创建报告
        report = TokenResearchReport(
            token_symbol=token_symbol,
            contract_address=token_address,
            chain=chain,
            timestamp=datetime.now().isoformat(),
            contract_risk=contract,
            holder_distribution=holder,
            liquidity_management=liquidity,
            developer_association=developer,
            marketing_narrative=marketing
        )
        
        report.calculate_overall_risk()
        return report
    
    def run(self):
        """运行交互流程"""
        print("\n" + "="*70)
        print("MANUAL TOKEN RESEARCH - v9.0")
        print("="*70)
        print("\nThis tool guides you through manual data collection")
        print("and automatically generates risk assessment reports.\n")
        
        # 获取代币信息
        token_address = input("Enter contract address: ").strip()
        token_symbol = input("Enter token symbol: ").strip().upper()
        chain = input("Enter chain (1=ETH, 56=BSC) [default: 1]: ").strip() or "1"
        
        # 显示查询指南
        self.show_guide(token_address, chain)
        
        # 收集数据
        print("Paste collected data (empty line to finish):")
        lines = []
        while True:
            try:
                line = input()
                if line.strip() == '' and lines and lines[-1].strip() == '':
                    break
                lines.append(line)
            except EOFError:
                break
        
        input_text = '\n'.join(lines)
        
        if input_text.strip().lower() == 'skip':
            print("\n[WARN] Using default values (all safe)")
            input_text = ""
        
        # 解析数据
        data = self.parse_input(input_text)
        
        # 显示解析结果
        print("\n" + "="*70)
        print("PARSED DATA")
        print("="*70)
        for section, values in data.items():
            if values:
                print(f"\n{section.upper()}:")
                for k, v in values.items():
                    print(f"  {k}: {v}")
        
        # 确认
        confirm = input("\nIs this correct? [Y/n]: ").strip().lower()
        if confirm == 'n':
            print("[INFO] Aborted. Please restart.")
            return
        
        # 生成报告
        print("\n[OK] Generating report...")
        report = self.create_report(token_symbol, token_address, chain, data)
        
        # 显示结果
        print("\n" + "="*70)
        print("📈 RISK ASSESSMENT RESULT")
        print("="*70)
        print(f"\nToken: {report.token_symbol}")
        print(f"Overall Score: {report.overall_risk_score}/100")
        print(f"Risk Level: {report.risk_level}")
        print(f"\nRecommended Action:")
        print(f"  {report.recommended_action}")
        
        print("\n" + "-"*70)
        print("Five Vulnerabilities Breakdown:")
        print("-"*70)
        print(f"  Contract Code:        {report.contract_risk.risk_score()}/100")
        print(f"  Holder Distribution:  {report.holder_distribution.risk_score()}/100")
        print(f"  Liquidity Management: {report.liquidity_management.risk_score()}/100")
        print(f"  Developer Association: {report.developer_association.risk_score()}/100")
        print(f"  Marketing Narrative:  {report.marketing_narrative.risk_score()}/100")
        
        # 保存报告
        save = input("\nSave report? [Y/n]: ").strip().lower()
        if save != 'n':
            output_dir = Path(r'F:\stepclaw\agents\blockchain-analyst\narratives')
            output_dir.mkdir(exist_ok=True)
            
            filename = f"{datetime.now().strftime('%Y-%m-%d')}-{report.token_symbol}.md"
            filepath = output_dir / filename
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(report.generate_fact_sheet())
            
            print(f"\n[OK] Report saved: {filepath}")
            
            # 添加到案例库
            add_case = input("Add to case study database? [Y/n]: ").strip().lower()
            if add_case != 'n':
                claimed = input("Project claims (what they say): ").strip()
                reality = input("On-chain reality (facts): ").strip()
                
                case_id = self.case_manager.add_case(
                    token_symbol=report.token_symbol,
                    contract_address=report.contract_address,
                    chain=report.chain,
                    risk_level=report.risk_level,
                    classification=report.recommended_action.split(' - ')[0],
                    key_signals=[
                        f"Contract: {report.contract_risk.risk_score()}/100",
                        f"Holders: {report.holder_distribution.risk_score()}/100",
                        f"Liquidity: {report.liquidity_management.risk_score()}/100"
                    ],
                    summary=f"Risk score {report.overall_risk_score}/100. {report.recommended_action}",
                    claimed=claimed,
                    reality=reality
                )
                
                print(f"\n[OK] Added to case database: {case_id}")
        
        print("\n" + "="*70)
        print("Done! Next steps:")
        print("  - [A] Analyze another token")
        print("  - [L] List pending reviews")
        print("  - [Q] Quit")
        print("="*70)


def main():
    """主函数"""
    cli = ManualResearchCLI()
    
    while True:
        try:
            cli.run()
            
            choice = input("\nChoice [A/L/Q]: ").strip().upper()
            if choice == 'Q':
                print("\n[OK] Goodbye!")
                break
            elif choice == 'L':
                print("\n[TODO] List function not implemented yet")
            elif choice != 'A':
                print("\n[ERR] Invalid choice")
                
        except KeyboardInterrupt:
            print("\n\n[OK] Interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"\n[ERR] {e}")
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    main()
