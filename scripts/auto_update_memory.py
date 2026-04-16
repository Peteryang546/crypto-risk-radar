#!/usr/bin/env python3
"""
自动更新 MEMORY.md 脚本
在每次 Agent 执行后调用
"""

import json
import re
from datetime import datetime
from pathlib import Path

def update_memory(agent_id: str, execution_record: dict):
    """
    自动更新 Agent 的 MEMORY.md
    
    Args:
        agent_id: Agent ID (如 'blockchain-analyst')
        execution_record: 执行记录字典
    """
    
    memory_path = Path(f"F:/stepclaw/agents/{agent_id}/MEMORY.md")
    
    if not memory_path.exists():
        print(f"错误: 找不到 {memory_path}")
        return False
    
    # 读取现有内容
    content = memory_path.read_text(encoding='utf-8')
    
    # 更新 "最后更新" 字段
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    content = re.sub(
        r'\*\*最后更新\*\*: .*',
        f'**最后更新**: {now}',
        content
    )
    
    # 生成运行记录条目
    record_entry = f"""### {execution_record['datetime']}
- **任务**: {execution_record['task']}
- **状态**: {'✅ 成功' if execution_record['success'] else '❌ 失败'}
- **评分**: {execution_record.get('score', 'N/A')}/100
- **数据源**: {', '.join(execution_record.get('data_sources', []))}
- **输出文件**: {execution_record.get('output_file', 'N/A')}
- **备注**: {execution_record.get('notes', '无')}

"""
    
    # 插入到运行记录部分
    if "## 运行记录" in content:
        # 在 "## 运行记录" 后插入新记录
        content = re.sub(
            r'(## 运行记录\n+)',
            r'\1' + record_entry,
            content
        )
    
    # 更新数据源状态时间戳
    for source in execution_record.get('data_sources', []):
        # 查找并更新对应数据源的 "最后检查" 时间
        pattern = rf'(\| {re.escape(source)} \| .*? \| )\d{{4}}-\d{{2}}-\d{{2}}( \|)'
        replacement = rf'\g<1>{now[:10]}\g<2>'
        content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
    
    # 写回文件
    memory_path.write_text(content, encoding='utf-8')
    print(f"✅ 已更新 {agent_id}/MEMORY.md")
    return True


def update_price_trend(agent_id: str, product: str, price_data: dict):
    """
    更新价格趋势表
    
    Args:
        agent_id: Agent ID
        product: 产品名称
        price_data: 价格数据 {date, price, change, reason}
    """
    
    memory_path = Path(f"F:/stepclaw/agents/{agent_id}/MEMORY.md")
    content = memory_path.read_text(encoding='utf-8')
    
    # 查找产品价格趋势表
    pattern = rf"(### {re.escape(product)}\n\| 日期 \| 价格 \| 变动 \| 原因 \|\n\|------\|------\|------\|------\|)"
    
    new_row = f"\n| {price_data['date']} | {price_data['price']} | {price_data['change']} | {price_data['reason']} |"
    
    content = re.sub(pattern, rf'\1{new_row}', content)
    
    memory_path.write_text(content, encoding='utf-8')
    print(f"✅ 已更新 {product} 价格趋势")


def update_policy_history(agent_id: str, policy_data: dict):
    """
    更新政策历史追踪表
    
    Args:
        agent_id: Agent ID
        policy_data: 政策数据 {date, policy, impact, status}
    """
    
    memory_path = Path(f"F:/stepclaw/agents/{agent_id}/MEMORY.md")
    content = memory_path.read_text(encoding='utf-8')
    
    # 查找政策历史表
    pattern = r"(## 政策历史追踪\n\n\| 日期 \| 政策 \| 影响 \| 状态 \|\n\|------\|------\|------\|------\|)"
    
    new_row = f"\n| {policy_data['date']} | {policy_data['policy']} | {policy_data['impact']} | {policy_data['status']} |"
    
    content = re.sub(pattern, rf'\1{new_row}', content)
    
    memory_path.write_text(content, encoding='utf-8')
    print(f"✅ 已更新政策历史")


def update_user_feedback(agent_id: str, feedback: dict):
    """
    更新用户反馈修正表
    
    Args:
        agent_id: Agent ID
        feedback: 反馈数据 {date, content, action, status}
    """
    
    memory_path = Path(f"F:/stepclaw/agents/{agent_id}/MEMORY.md")
    content = memory_path.read_text(encoding='utf-8')
    
    # 查找用户反馈表
    pattern = r"(## 用户反馈修正\n\n\| 日期 \| 反馈内容 \| 修正措施 \| 状态 \|\n\|------\|----------\|----------\|------\|)"
    
    new_row = f"\n| {feedback['date']} | {feedback['content']} | {feedback['action']} | {feedback['status']} |"
    
    content = re.sub(pattern, rf'\1{new_row}', content)
    
    memory_path.write_text(content, encoding='utf-8')
    print(f"✅ 已更新用户反馈")


# 示例用法
if __name__ == "__main__":
    # 测试更新 blockchain-analyst
    test_record = {
        "datetime": "2026-04-06 20:00",
        "task": "生成Reels脚本",
        "success": True,
        "score": 85,
        "data_sources": ["CoinGecko", "Alternative.me F&G"],
        "output_file": "reels_2026-04-06.md",
        "notes": "新币检测: 无新币"
    }
    
    update_memory("blockchain-analyst", test_record)
