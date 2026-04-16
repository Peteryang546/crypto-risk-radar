#!/usr/bin/env python3
"""
区块链分析师输出评估脚本
评分标准：满分100分，≥80分通过
"""

import sys
import re
from pathlib import Path

def check_fear_greed_index(content):
    """检查恐惧贪婪指数"""
    patterns = [
        r'恐惧贪婪指数[:：]\s*\d+',
        r'Fear.*Greed.*Index[:：]?\s*\d+',
        r'贪婪指数[:：]\s*\d+',
        r'恐惧指数[:：]\s*\d+'
    ]
    for pattern in patterns:
        if re.search(pattern, content, re.IGNORECASE):
            return True, 20
    return False, 0

def check_top10_performance(content):
    """检查Top10表现"""
    patterns = [
        r'Top\s*10',
        r'前十',
        r'排名前十',
        r'涨幅.*前.*10',
        r'跌幅.*前.*10'
    ]
    for pattern in patterns:
        if re.search(pattern, content, re.IGNORECASE):
            return True, 20
    return False, 0

def check_quant_factors(content):
    """检查量化因子摘要"""
    patterns = [
        r'量化因子',
        r'综合信号',
        r'多因子模型',
        r'因子类别',
        r'价量因子|链上行为|市场微观|宏观情绪|风险特化'
    ]
    score = 0
    for pattern in patterns:
        if re.search(pattern, content, re.IGNORECASE):
            score += 4
    return score >= 12, min(score, 20)

def check_fraud_detection(content):
    """检查骗局匹配预警"""
    patterns = [
        r'骗局匹配',
        r'风险预警',
        r'AI深度伪造|地址投毒|Rug\s*Pull|虚假交易|三无.*代币',
        r'骗局类型',
        r'匹配度'
    ]
    score = 0
    for pattern in patterns:
        if re.search(pattern, content, re.IGNORECASE):
            score += 5
    return score >= 10, min(score, 20)

def check_data_sources(content):
    """检查数据来源标注"""
    patterns = [
        r'数据来源[:：]',
        r'Source[:：]',
        r'CoinGecko',
        r'Etherscan',
        r'Glassnode',
        r'DEX\s*Screener',
        r'Alternative\.me'
    ]
    score = 0
    for pattern in patterns:
        if re.search(pattern, content, re.IGNORECASE):
            score += 4
    return score >= 8, min(score, 20)

def check_forbidden_words(content):
    """检查禁止词汇"""
    forbidden = ['买入', '卖出', '抄底', '梭哈', '上车', '建议买', '建议卖', '必涨', '必跌']
    found = []
    for word in forbidden:
        if word in content:
            found.append(word)
    return len(found) == 0, found

def evaluate_report(file_path):
    """评估报告"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        return {
            'success': False,
            'score': 0,
            'error': f'无法读取文件: {e}',
            'details': {}
        }
    
    # 检查各项
    checks = {
        '恐惧贪婪指数': check_fear_greed_index(content),
        'Top10表现': check_top10_performance(content),
        '量化因子摘要': check_quant_factors(content),
        '骗局匹配预警': check_fraud_detection(content),
        '数据来源标注': check_data_sources(content)
    }
    
    # 检查禁止词汇
    no_forbidden, forbidden_found = check_forbidden_words(content)
    
    # 计算总分
    total_score = sum(score for _, score in checks.values())
    
    # 如果有禁止词汇，扣50分
    if not no_forbidden:
        total_score -= 50
    
    # 确保分数在0-100之间
    total_score = max(0, min(100, total_score))
    
    return {
        'success': total_score >= 80 and no_forbidden,
        'score': total_score,
        'forbidden_words': forbidden_found if not no_forbidden else [],
        'details': {name: passed for name, (passed, _) in checks.items()},
        'scores': {name: score for name, (_, score) in checks.items()}
    }

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("用法: python score_blockchain.py <报告文件路径>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    result = evaluate_report(file_path)
    
    print(f"评估结果: {'通过' if result['success'] else '未通过'}")
    print(f"总分: {result['score']}/100")
    print()
    
    if result.get('forbidden_words'):
        print(f"⚠️ 发现禁止词汇: {', '.join(result['forbidden_words'])}")
        print("扣除50分")
        print()
    
    print("详细评分:")
    for name, score in result['scores'].items():
        status = '✅' if result['details'][name] else '❌'
        print(f"  {status} {name}: {score}/20")
    
    sys.exit(0 if result['success'] else 1)
