#!/usr/bin/env python3
"""
SEO + GEO 优化脚本 - 区块链风险雷达
为Hashnode内容添加SEO和GEO优化
"""

import json
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any

class SEOGEOOptimizer:
    """SEO和GEO优化器"""
    
    def __init__(self):
        self.target_keywords = [
            # 主要关键词
            "crypto risk analysis",
            "bitcoin on-chain data",
            "blockchain risk radar",
            "crypto scam detection",
            "on-chain analysis",
            
            # 长尾关键词
            "how to identify crypto scams",
            "what is rug pull crypto",
            "crypto wallet address poisoning",
            "bitcoin exchange netflow analysis",
            "crypto fear and greed index explained",
            "on-chain analysis for beginners",
            "blockchain data analysis",
            "crypto market risk assessment",
            "how to avoid crypto scams",
            "bitcoin whale movements",
            
            # 教育类
            "crypto risk management",
            "blockchain education",
            "crypto due diligence",
            "defi risk analysis"
        ]
    
    def extract_content_summary(self, content: str) -> Dict[str, Any]:
        """提取内容摘要"""
        # 提取TL;DR
        tldr_match = re.search(r'\*\*TL;DR\*\*:\s*(.+?)(?=\n\n|\Z)', content, re.DOTALL)
        tldr = tldr_match.group(1).strip() if tldr_match else ""
        
        # 提取量化得分
        score_match = re.search(r'\*\*Final Score\*\*:\s*([\+\-]?\d+\.?\d*)', content)
        quant_score = score_match.group(1) if score_match else ""
        
        # 提取等级
        grade_match = re.search(r'\*\*Grade\*\*:\s*([🔴🟡⚪🟢🔵])\s*(.+?)(?=\n)', content)
        grade = grade_match.group(2).strip() if grade_match else ""
        
        # 提取主要发现
        findings = []
        for line in content.split('\n'):
            if 'net outflow' in line.lower() or 'accumulation' in line.lower():
                findings.append(line.strip())
            if 'funding' in line.lower() and 'percentile' in line.lower():
                findings.append(line.strip())
        
        return {
            'tldr': tldr[:200],
            'quant_score': quant_score,
            'grade': grade,
            'key_findings': findings[:3]
        }
    
    def generate_meta_description(self, content: str) -> str:
        """生成meta描述（用于SEO）"""
        summary = self.extract_content_summary(content)
        
        desc = f"Crypto Risk Radar: {summary['grade']} signal ({summary['quant_score']}/2.0). "
        desc += f"{summary['tldr'][:100]}... "
        desc += "Data-driven blockchain risk analysis for long-term investors."
        
        return desc[:160]  # Google通常显示前160字符
    
    def generate_keywords(self, content: str) -> List[str]:
        """生成关键词列表"""
        keywords = []
        content_lower = content.lower()
        
        # 根据内容匹配关键词
        keyword_mapping = {
            'bitcoin': ['bitcoin', 'btc', 'bitcoin analysis'],
            'ethereum': ['ethereum', 'eth', 'ethereum analysis'],
            'scam': ['crypto scam', 'rug pull', 'crypto risk'],
            'on-chain': ['on-chain analysis', 'blockchain data'],
            'whale': ['bitcoin whale', 'whale movements'],
            'funding': ['funding rate', 'crypto derivatives'],
            'fear': ['fear and greed', 'crypto sentiment'],
            'exchange': ['exchange netflow', 'exchange reserves']
        }
        
        for key, words in keyword_mapping.items():
            if key in content_lower:
                keywords.extend(words)
        
        # 添加默认关键词
        default = [
            "crypto risk radar",
            "blockchain analysis",
            "crypto market analysis",
            "risk management",
            "crypto education"
        ]
        keywords.extend(default)
        
        # 去重并限制数量
        return list(set(keywords))[:10]
    
    def generate_json_ld(self, title: str, content: str, url: str, date: str) -> Dict:
        """生成JSON-LD结构化数据"""
        summary = self.extract_content_summary(content)
        keywords = self.generate_keywords(content)
        
        return {
            "@context": "https://schema.org",
            "@type": "TechArticle",
            "headline": title,
            "description": summary['tldr'][:150],
            "keywords": ", ".join(keywords),
            "author": {
                "@type": "Organization",
                "name": "Crypto Risk Radar",
                "url": "https://cryptoriskradar.hashnode.dev/"
            },
            "publisher": {
                "@type": "Organization",
                "name": "Crypto Risk Radar",
                "logo": {
                    "@type": "ImageObject",
                    "url": "https://cryptoriskradar.hashnode.dev/logo.png"
                }
            },
            "datePublished": date,
            "dateModified": date,
            "mainEntityOfPage": {
                "@type": "WebPage",
                "@id": url
            },
            "articleSection": "Blockchain Analysis",
            "about": {
                "@type": "Thing",
                "name": "Cryptocurrency Risk Analysis"
            }
        }
    
    def generate_faq_section(self, content: str) -> str:
        """生成FAQ部分（用于GEO）"""
        faqs = []
        
        # 基于内容生成FAQ
        if "quant score" in content.lower():
            faqs.append({
                "question": "What is the Quant Score in Crypto Risk Radar?",
                "answer": "The Quant Score is a composite signal calculated from 7 weighted factors including on-chain behavior, market microstructure, sentiment, and risk indicators. It ranges from -2.0 (Strong Avoid) to +2.0 (Strong Positive)."
            })
        
        if "on-chain" in content.lower():
            faqs.append({
                "question": "What on-chain metrics does the report track?",
                "answer": "The report tracks exchange netflow (24h/7d), whale holdings (Top 100), long-term holder supply changes, MVRV Z-score, and miner position index (MPI)."
            })
        
        if "scam" in content.lower():
            faqs.append({
                "question": "How does the report detect potential scams?",
                "answer": "The report analyzes liquidity lock percentages, top 10 holder concentrations, contract verification status, and trading patterns to identify high-risk tokens and potential rug pulls."
            })
        
        # 默认FAQ
        faqs.extend([
            {
                "question": "Who is Crypto Risk Radar for?",
                "answer": "Crypto Risk Radar is designed for long-term investors, risk-averse traders, and beginners who want data-driven insights to avoid common crypto pitfalls and make informed decisions."
            },
            {
                "question": "How often is the report published?",
                "answer": "The report is published twice daily at 08:10 and 20:10 CST (China Standard Time), providing 12-hour market coverage."
            }
        ])
        
        # 生成FAQ markdown
        faq_md = "\n## Frequently Asked Questions\n\n"
        for i, faq in enumerate(faqs, 1):
            faq_md += f"**Q{i}: {faq['question']}\n\n"
            faq_md += f"A: {faq['answer']}\n\n"
        
        return faq_md
    
    def optimize_content(self, content: str, title: str, url: str) -> str:
        """优化内容以提升SEO和GEO"""
        date = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
        
        # 生成JSON-LD
        json_ld = self.generate_json_ld(title, content, url, date)
        
        # 生成关键词
        keywords = self.generate_keywords(content)
        
        # 生成FAQ
        faq_section = self.generate_faq_section(content)
        
        # 构建优化后的内容
        optimized = content + f"""

---

## SEO Keywords

**Primary**: {', '.join(keywords[:3])}

**Secondary**: {', '.join(keywords[3:7])}

**Long-tail**: {', '.join(keywords[7:])}

{faq_section}

---

## About Crypto Risk Radar

**Crypto Risk Radar** provides systematic, data-driven blockchain risk analysis for long-term investors. Our 7-module framework delivers transparent, actionable insights to help you navigate the crypto market with confidence.

- **Quantitative Signals**: 7-factor weighted scoring system
- **On-Chain Analysis**: Exchange flows, whale movements, holder behavior
- **Risk Detection**: Scam identification and anomaly alerts
- **Historical Backtest**: Pattern matching and probability analysis
- **Actionable Insights**: Specific recommendations, not vague advice

**Data Sources**: Binance, CoinGecko, DEX Screener, DeFi Llama, Alternative.me

**Publication Schedule**: Daily at 08:10 & 20:10 CST

---

<script type="application/ld+json">
{json.dumps(json_ld, indent=2)}
</script>
"""
        
        return optimized
    
    def generate_social_meta(self, title: str, content: str, url: str) -> Dict:
        """生成社交媒体元数据"""
        summary = self.extract_content_summary(content)
        
        return {
            "twitter": {
                "card": "summary_large_image",
                "title": title[:70],
                "description": summary['tldr'][:200],
                "url": url,
                "image": "https://cryptoriskradar.hashnode.dev/og-image.png"
            },
            "open_graph": {
                "type": "article",
                "title": title,
                "description": summary['tldr'][:200],
                "url": url,
                "image": "https://cryptoriskradar.hashnode.dev/og-image.png",
                "site_name": "Crypto Risk Radar"
            }
        }

def optimize_report_for_publish(input_file: str, output_file: str = None) -> str:
    """优化报告用于发布"""
    input_path = Path(input_file)
    
    if not input_path.exists():
        print(f"[ERROR] File not found: {input_path}")
        return None
    
    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 提取标题
    title_match = re.search(r'^#\s+(.+?)$', content, re.MULTILINE)
    title = title_match.group(1) if title_match else "Crypto Risk Radar Report"
    
    # 生成URL
    date_slug = datetime.now().strftime('%Y-%m-%d')
    url = f"https://cryptoriskradar.hashnode.dev/crypto-risk-radar-{date_slug}"
    
    # 优化内容
    optimizer = SEOGEOOptimizer()
    optimized = optimizer.optimize_content(content, title, url)
    
    # 保存
    if output_file is None:
        output_path = input_path.parent / f"optimized_{input_path.name}"
    else:
        output_path = Path(output_file)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(optimized)
    
    print(f"[SUCCESS] Optimized content saved: {output_path}")
    
    # 输出SEO信息
    meta_desc = optimizer.generate_meta_description(content)
    keywords = optimizer.generate_keywords(content)
    
    print(f"\n[SEO Info]")
    print(f"  Title: {title[:60]}")
    print(f"  Meta Description: {meta_desc[:100]}...")
    print(f"  Keywords: {', '.join(keywords[:5])}")
    
    return str(output_path)

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python seo_geo_optimizer.py <input_file> [output_file]")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    optimize_report_for_publish(input_file, output_file)
