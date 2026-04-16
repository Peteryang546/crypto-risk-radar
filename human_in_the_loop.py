#!/usr/bin/env python3
"""
Human-in-the-Loop CLI Interface
人机合作命令行界面

交互流程:
1. 显示待办列表
2. 用户选择操作
3. 执行操作
4. 更新列表
5. 循环直到完成
"""

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional

sys.path.insert(0, r'F:\stepclaw\agents\blockchain-analyst')

from token_research_framework import TokenResearcher, TokenResearchReport


class TodoItem:
    """待办事项"""
    def __init__(self, token_data: Dict):
        self.address = token_data.get("address", "")
        self.symbol = token_data.get("symbol", "UNKNOWN")
        self.chain = token_data.get("chain", "")
        self.risk_score = token_data.get("risk_score", 0)
        self.risk_level = token_data.get("risk_level", "🟡 中")
        self.liquidity_usd = token_data.get("liquidity_usd", 0)
        self.volume_24h = token_data.get("volume_24h", 0)
        
        # 状态: pending / researching / classified / skipped
        self.status = "pending"
        self.classification = None  # 最终分类
        self.notes = ""  # 用户备注
        self.research_report = None  # 研究报告
    
    def to_dict(self) -> Dict:
        return {
            "address": self.address,
            "symbol": self.symbol,
            "chain": self.chain,
            "risk_score": self.risk_score,
            "risk_level": self.risk_level,
            "liquidity_usd": self.liquidity_usd,
            "volume_24h": self.volume_24h,
            "status": self.status,
            "classification": self.classification,
            "notes": self.notes,
            "research_report": self.research_report.to_dict() if self.research_report else None
        }


class HumanInTheLoop:
    """人机合作系统"""
    
    def __init__(self, output_dir: str = r"F:\stepclaw\agents\blockchain-analyst\output"):
        self.output_dir = Path(output_dir)
        self.todo_file = self.output_dir / "todo_list.json"
        self.researcher = TokenResearcher()
        self.todo_list: List[TodoItem] = []
        
        # 加载现有待办列表
        self._load_todo()
    
    def _load_todo(self):
        """加载待办列表"""
        if self.todo_file.exists():
            try:
                with open(self.todo_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for item_data in data.get("items", []):
                        item = TodoItem(item_data)
                        item.status = item_data.get("status", "pending")
                        item.classification = item_data.get("classification")
                        item.notes = item_data.get("notes", "")
                        self.todo_list.append(item)
                print(f"[INFO] Loaded {len(self.todo_list)} items from todo list")
            except Exception as e:
                print(f"[WARNING] Failed to load todo list: {e}")
    
    def _save_todo(self):
        """保存待办列表"""
        data = {
            "updated_at": datetime.now().isoformat(),
            "total_items": len(self.todo_list),
            "pending": sum(1 for i in self.todo_list if i.status == "pending"),
            "researching": sum(1 for i in self.todo_list if i.status == "researching"),
            "classified": sum(1 for i in self.todo_list if i.status == "classified"),
            "skipped": sum(1 for i in self.todo_list if i.status == "skipped"),
            "items": [item.to_dict() for item in self.todo_list]
        }
        
        with open(self.todo_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def add_candidates(self, candidates: List[Dict]):
        """添加候选代币到待办列表"""
        added = 0
        for candidate in candidates:
            # 检查是否已存在
            if not any(item.address == candidate["address"] for item in self.todo_list):
                self.todo_list.append(TodoItem(candidate))
                added += 1
        
        if added > 0:
            self._save_todo()
            print(f"[INFO] Added {added} new candidates to todo list")
        
        return added
    
    def show_todo(self):
        """显示待办列表"""
        print("\n" + "="*70)
        print("📋 代币分析待办列表")
        print("="*70)
        
        pending_items = [i for i in self.todo_list if i.status == "pending"]
        
        if not pending_items:
            print("\n✅ 所有代币已处理完毕！")
            print("\n选项:")
            print("  [D] 发现新代币")
            print("  [Q] 退出")
            return
        
        print(f"\n待处理: {len(pending_items)} 个代币\n")
        
        for i, item in enumerate(pending_items[:10], 1):  # 显示前10个
            print(f"{i}. {item.symbol} - {item.risk_level}")
            print(f"   流动性: ${item.liquidity_usd:,.0f} | 24h交易量: ${item.volume_24h:,.0f}")
            print(f"   风险评分: {item.risk_score}/100")
            print()
        
        if len(pending_items) > 10:
            print(f"... 还有 {len(pending_items) - 10} 个代币")
        
        print("-"*70)
        print("操作选项:")
        print("  [数字] 选择代币进行深入研究 (1-10)")
        print("  [C] 快速分类（跳过研究）")
        print("  [D] 发现新代币")
        print("  [S] 查看统计")
        print("  [Q] 保存并退出")
        print("-"*70)
    
    def research_token(self, index: int):
        """深入研究代币"""
        pending_items = [i for i in self.todo_list if i.status == "pending"]
        
        if index < 1 or index > len(pending_items):
            print("[ERROR] 无效的选择")
            return
        
        item = pending_items[index - 1]
        item.status = "researching"
        
        print(f"\n🔍 正在研究 {item.symbol}...")
        print(f"合约地址: {item.address}")
        print("-"*70)
        
        # 执行自动研究
        try:
            report = self.researcher.analyze_token(
                token_address=item.address,
                chain=item.chain,
                token_symbol=item.symbol
            )
            item.research_report = report
            
            # 显示研究报告
            print(report.generate_fact_sheet())
            
            # 用户确认分类
            print("\n" + "="*70)
            print("分类选择:")
            print("  [1] 🔴 极高风险 - 直接忽略")
            print("  [2] 🟠 高风险 - 远离")
            print("  [3] 🟡 中风险 - 观察，不参与")
            print("  [4] 🟢 低风险 - 可学习、可研究")
            print("  [S] 跳过，稍后处理")
            print("-"*70)
            
            choice = input("选择分类 (1-4/S): ").strip().upper()
            
            classification_map = {
                "1": ("🔴 极高风险", "直接忽略"),
                "2": ("🟠 高风险", "远离"),
                "3": ("🟡 中风险", "观察，不参与"),
                "4": ("🟢 低风险", "可学习、可研究")
            }
            
            if choice in classification_map:
                item.classification = classification_map[choice]
                item.status = "classified"
                
                # 添加备注
                notes = input("添加备注 (可选，直接回车跳过): ").strip()
                if notes:
                    item.notes = notes
                
                print(f"\n✅ 已分类: {item.symbol} -> {item.classification[0]}")
                
            elif choice == "S":
                item.status = "pending"
                print(f"\n⏸️ 已跳过: {item.symbol}")
            else:
                item.status = "pending"
                print(f"\n⚠️ 无效选择，保持待处理状态")
            
            self._save_todo()
            
        except Exception as e:
            print(f"[ERROR] 研究失败: {e}")
            item.status = "pending"
    
    def quick_classify(self):
        """快速分类（基于自动检测结果）"""
        pending_items = [i for i in self.todo_list if i.status == "pending"]
        
        if not pending_items:
            print("[INFO] 没有待处理的代币")
            return
        
        print(f"\n快速分类 {len(pending_items)} 个代币:")
        print("-"*70)
        
        for item in pending_items:
            # 根据风险分数自动建议
            if item.risk_score >= 70:
                suggestion = ("🔴 极高风险", "直接忽略")
            elif item.risk_score >= 50:
                suggestion = ("🟠 高风险", "远离")
            elif item.risk_score >= 30:
                suggestion = ("🟡 中风险", "观察，不参与")
            else:
                suggestion = ("🟢 低风险", "可学习、可研究")
            
            print(f"\n{item.symbol} - 建议: {suggestion[0]}")
            print(f"  风险评分: {item.risk_score}/100")
            print(f"  流动性: ${item.liquidity_usd:,.0f}")
            
            choice = input("  确认 [Y/N/S]: ").strip().upper()
            
            if choice == "Y":
                item.classification = suggestion
                item.status = "classified"
                print(f"  ✅ 已分类为 {suggestion[0]}")
            elif choice == "N":
                # 让用户选择其他分类
                print("  选择分类:")
                print("    [1] 🔴 极高风险")
                print("    [2] 🟠 高风险")
                print("    [3] 🟡 中风险")
                print("    [4] 🟢 低风险")
                alt = input("  选择 (1-4): ").strip()
                alt_map = {"1": ("🔴 极高风险", "直接忽略"), "2": ("🟠 高风险", "远离"),
                          "3": ("🟡 中风险", "观察，不参与"), "4": ("🟢 低风险", "可学习、可研究")}
                if alt in alt_map:
                    item.classification = alt_map[alt]
                    item.status = "classified"
                    print(f"  ✅ 已分类为 {item.classification[0]}")
            elif choice == "S":
                print("  ⏸️ 已跳过")
            else:
                print("  ⚠️ 保持待处理")
        
        self._save_todo()
        print(f"\n✅ 快速分类完成")
    
    def show_stats(self):
        """显示统计"""
        total = len(self.todo_list)
        pending = sum(1 for i in self.todo_list if i.status == "pending")
        researching = sum(1 for i in self.todo_list if i.status == "researching")
        classified = sum(1 for i in self.todo_list if i.status == "classified")
        skipped = sum(1 for i in self.todo_list if i.status == "skipped")
        
        # 分类统计
        extreme = sum(1 for i in self.todo_list if i.classification and i.classification[0] == "🔴 极高风险")
        high = sum(1 for i in self.todo_list if i.classification and i.classification[0] == "🟠 高风险")
        medium = sum(1 for i in self.todo_list if i.classification and i.classification[0] == "🟡 中风险")
        low = sum(1 for i in self.todo_list if i.classification and i.classification[0] == "🟢 低风险")
        
        print("\n" + "="*70)
        print("📊 统计信息")
        print("="*70)
        print(f"\n总代币数: {total}")
        print(f"  待处理: {pending}")
        print(f"  研究中: {researching}")
        print(f"  已分类: {classified}")
        print(f"  已跳过: {skipped}")
        print(f"\n分类分布:")
        print(f"  🔴 极高风险: {extreme}")
        print(f"  🟠 高风险: {high}")
        print(f"  🟡 中风险: {medium}")
        print(f"  🟢 低风险: {low}")
        print("="*70)
    
    def run(self):
        """运行交互循环"""
        print("\n" + "="*70)
        print("🤖 Crypto Risk Radar - 人机合作系统")
        print("="*70)
        print("输入 H 查看帮助，Q 退出\n")
        
        while True:
            self.show_todo()
            
            try:
                choice = input("\n选择操作: ").strip().upper()
                
                if choice == "Q":
                    self._save_todo()
                    print("\n✅ 已保存，再见！")
                    break
                elif choice == "H":
                    self._show_help()
                elif choice == "D":
                    self._discover_new()
                elif choice == "C":
                    self.quick_classify()
                elif choice == "S":
                    self.show_stats()
                elif choice.isdigit():
                    self.research_token(int(choice))
                else:
                    print("[ERROR] 无效的选择，输入 H 查看帮助")
                    
            except KeyboardInterrupt:
                print("\n\n⚠️ 中断保存...")
                self._save_todo()
                break
            except Exception as e:
                print(f"[ERROR] {e}")
    
    def _show_help(self):
        """显示帮助"""
        print("\n" + "="*70)
        print("📖 帮助")
        print("="*70)
        print("\n操作说明:")
        print("  [数字] 选择代币进行深入研究 (显示的前10个)")
        print("  [C]    快速分类（基于自动检测结果）")
        print("  [D]    发现新代币（从DEX Screener获取）")
        print("  [S]    查看统计信息")
        print("  [H]    显示帮助")
        print("  [Q]    保存并退出")
        print("\n分类说明:")
        print("  🔴 极高风险 - 明确欺诈特征，直接忽略")
        print("  🟠 高风险   - 高度可疑，远离")
        print("  🟡 中风险   - 经营困难，观察不参与")
        print("  🟢 低风险   - 可学习研究，不构成投资建议")
        print("="*70)
    
    def _discover_new(self):
        """发现新代币"""
        from token_discovery import TokenDiscovery
        
        print("\n🔍 正在发现新代币...")
        discovery = TokenDiscovery()
        candidates = discovery.discover_new_tokens(limit=10)
        
        if candidates:
            added = self.add_candidates(candidates)
            print(f"\n✅ 已添加 {added} 个新候选")
        else:
            print("\n[INFO] 未发现新的高风险代币")


# 示例用法
if __name__ == "__main__":
    # 创建人机合作系统
    hitl = HumanInTheLoop()
    
    # 运行交互循环
    hitl.run()
