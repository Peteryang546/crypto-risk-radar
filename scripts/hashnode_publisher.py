#!/usr/bin/env python3
"""
Hashnode博客发布脚本 - 区块链风险雷达
自动发布报告到Hashnode平台
"""

import os
import sys
import json
import re
from datetime import datetime
from pathlib import Path

# Add local lib path for requests
sys.path.insert(0, r'F:\stepclaw\workspace\lib')

try:
    import requests
except ImportError:
    print("[ERROR] requests module not found. Please install: pip install requests")
    sys.exit(1)

# Hashnode配置
HASHNODE_API_KEY = "2a69ed2e-fb06-44e1-bc25-7b8602e0ff66"
HASHNODE_WEBHOOK_SECRET = "hn_whs_0ee29a7bbe1334e2191ed875e2e4a7869a6465de3df9273f"
BLOG_URL = "https://cryptoriskradar.hashnode.dev/"
PUBLICATION_HOST = "cryptoriskradar.hashnode.dev"

# GraphQL API endpoint
GRAPHQL_ENDPOINT = "https://gql.hashnode.com"

def get_publication_id():
    """获取Publication ID"""
    query = """
    query GetPublication {
        publication(host: "%s") {
            id
            title
            url
        }
    }
    """ % PUBLICATION_HOST
    
    headers = {
        "Authorization": HASHNODE_API_KEY,
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(
            GRAPHQL_ENDPOINT,
            json={"query": query},
            headers=headers,
            timeout=30
        )
        data = response.json()
        
        if "errors" in data:
            print(f"[ERROR] GraphQL errors: {data['errors']}")
            return None
        
        pub_id = data["data"]["publication"]["id"]
        print(f"[SUCCESS] Found publication: {data['data']['publication']['title']}")
        return pub_id
    except Exception as e:
        print(f"[ERROR] Failed to get publication: {e}")
        return None

def extract_seo_keywords(content):
    """从内容中提取SEO关键词"""
    keywords = []
    
    # 主要关键词
    if "bitcoin" in content.lower() or "btc" in content.lower():
        keywords.extend(["bitcoin", "btc", "bitcoin analysis"])
    if "ethereum" in content.lower() or "eth" in content.lower():
        keywords.extend(["ethereum", "eth", "ethereum analysis"])
    
    # 风险相关
    if "scam" in content.lower() or "rug pull" in content.lower():
        keywords.extend(["crypto scam", "rug pull", "crypto risk"])
    
    # 分析类型
    if "on-chain" in content.lower():
        keywords.extend(["on-chain analysis", "blockchain data"])
    if "quant" in content.lower():
        keywords.extend(["quantitative analysis", "crypto quant"])
    
    # 默认关键词
    default_keywords = [
        "crypto risk radar",
        "blockchain analysis",
        "crypto market analysis",
        "risk management",
        "crypto education"
    ]
    
    # 合并并去重
    all_keywords = list(set(keywords + default_keywords))
    return all_keywords[:10]  # 最多10个

def generate_json_ld(title, description, date_published, keywords):
    """生成JSON-LD结构化数据"""
    return {
        "@context": "https://schema.org",
        "@type": "TechArticle",
        "headline": title,
        "description": description,
        "keywords": ", ".join(keywords),
        "author": {
            "@type": "Organization",
            "name": "Crypto Risk Radar"
        },
        "publisher": {
            "@type": "Organization",
            "name": "Crypto Risk Radar",
            "url": BLOG_URL
        },
        "datePublished": date_published,
        "dateModified": date_published,
        "mainEntityOfPage": {
            "@type": "WebPage",
            "@id": BLOG_URL
        }
    }

def prepare_content_for_hashnode(content, title):
    """准备内容格式"""
    # 提取TL;DR作为摘要
    tldr_match = re.search(r'\*\*TL;DR\*\*:\s*(.+?)(?=\n\n|\Z)', content, re.DOTALL)
    subtitle = tldr_match.group(1).strip() if tldr_match else "Daily blockchain risk analysis report"
    
    # 提取SEO关键词
    keywords = extract_seo_keywords(content)
    
    # 生成JSON-LD
    date_published = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
    json_ld = generate_json_ld(title, subtitle[:150], date_published, keywords)
    
    # 在内容末尾添加简单的hashtag SEO
    hashtags = ' '.join([f'#{kw.replace(" ", "")}' for kw in keywords[:8]])
    content_with_schema = content + f"""

---

{hashtags}
"""
    
    return content_with_schema, subtitle[:100], keywords

def publish_to_hashnode(content, title, publication_id):
    """发布文章到Hashnode"""
    
    # 准备内容
    prepared_content, subtitle, keywords = prepare_content_for_hashnode(content, title)
    
    # GraphQL mutation
    mutation = """
    mutation PublishPost($input: PublishPostInput!) {
        publishPost(input: $input) {
            post {
                id
                title
                slug
                url
                publishedAt
            }
        }
    }
    """
    
    variables = {
        "input": {
            "publicationId": publication_id,
            "title": title,
            "subtitle": subtitle,
            "contentMarkdown": prepared_content,
            "tags": [{"name": kw, "slug": kw.replace(" ", "-")} for kw in keywords[:5]],
            "settings": {
                "enableTableOfContent": True,
                "delisted": False
            }
        }
    }
    
    headers = {
        "Authorization": HASHNODE_API_KEY,
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(
            GRAPHQL_ENDPOINT,
            json={"query": mutation, "variables": variables},
            headers=headers,
            timeout=60
        )
        
        data = response.json()
        
        if "errors" in data:
            print(f"[ERROR] Publish failed: {data['errors']}")
            return None
        
        post = data["data"]["publishPost"]["post"]
        print(f"[SUCCESS] Published: {post['title']}")
        print(f"  URL: {post['url']}")
        print(f"  Slug: {post['slug']}")
        return post
        
    except Exception as e:
        print(f"[ERROR] Failed to publish: {e}")
        return None

def update_post(post_id, new_content, new_title):
    """更新已发布的文章"""
    
    mutation = """
    mutation UpdatePost($input: UpdatePostInput!) {
        updatePost(input: $input) {
            post {
                id
                title
                url
                updatedAt
            }
        }
    }
    """
    
    prepared_content, subtitle, keywords = prepare_content_for_hashnode(new_content, new_title)
    
    variables = {
        "input": {
            "id": post_id,
            "title": new_title,
            "subtitle": subtitle,
            "contentMarkdown": prepared_content
        }
    }
    
    headers = {
        "Authorization": HASHNODE_API_KEY,
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(
            GRAPHQL_ENDPOINT,
            json={"query": mutation, "variables": variables},
            headers=headers,
            timeout=60
        )
        
        data = response.json()
        
        if "errors" in data:
            print(f"[ERROR] Update failed: {data['errors']}")
            return None
        
        post = data["data"]["updatePost"]["post"]
        print(f"[SUCCESS] Updated: {post['title']}")
        return post
        
    except Exception as e:
        print(f"[ERROR] Failed to update: {e}")
        return None

def delete_post(post_id):
    """删除文章"""
    
    mutation = """
    mutation DeletePost($input: DeletePostInput!) {
        deletePost(input: $input) {
            post {
                id
                title
            }
        }
    }
    """
    
    variables = {
        "input": {
            "id": post_id
        }
    }
    
    headers = {
        "Authorization": HASHNODE_API_KEY,
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(
            GRAPHQL_ENDPOINT,
            json={"query": mutation, "variables": variables},
            headers=headers,
            timeout=30
        )
        
        data = response.json()
        
        if "errors" in data:
            print(f"[ERROR] Delete failed: {data['errors']}")
            return False
        
        post = data["data"]["deletePost"]["post"]
        print(f"[SUCCESS] Deleted: {post['title']}")
        return True
        
    except Exception as e:
        print(f"[ERROR] Failed to delete: {e}")
        return False

def list_posts(publication_id, first=10):
    """列出已发布的文章"""
    
    query = """
    query GetPosts($host: String!, $first: Int!) {
        publication(host: $host) {
            posts(first: $first) {
                edges {
                    node {
                        id
                        title
                        slug
                        url
                        publishedAt
                        views
                    }
                }
            }
        }
    }
    """
    
    variables = {
        "host": PUBLICATION_HOST,
        "first": first
    }
    
    headers = {
        "Authorization": HASHNODE_API_KEY,
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(
            GRAPHQL_ENDPOINT,
            json={"query": query, "variables": variables},
            headers=headers,
            timeout=30
        )
        
        data = response.json()
        
        if "errors" in data:
            print(f"[ERROR] List failed: {data['errors']}")
            return []
        
        posts = data["data"]["publication"]["posts"]["edges"]
        return [post["node"] for post in posts]
        
    except Exception as e:
        print(f"[ERROR] Failed to list posts: {e}")
        return []

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Hashnode Publisher for Crypto Risk Radar')
    parser.add_argument('action', choices=['publish', 'update', 'delete', 'list'], help='Action to perform')
    parser.add_argument('--file', '-f', help='Markdown file to publish')
    parser.add_argument('--title', '-t', help='Post title')
    parser.add_argument('--post-id', '-p', help='Post ID for update/delete')
    
    args = parser.parse_args()
    
    print("="*70)
    print("HASHNODE PUBLISHER - Crypto Risk Radar")
    print("="*70)
    print(f"Blog: {BLOG_URL}")
    print()
    
    # Get publication ID
    publication_id = get_publication_id()
    if not publication_id:
        print("[ERROR] Cannot get publication ID. Check your API key and blog URL.")
        sys.exit(1)
    
    if args.action == 'publish':
        if not args.file:
            print("[ERROR] --file required for publish action")
            sys.exit(1)
        
        file_path = Path(args.file)
        if not file_path.exists():
            print(f"[ERROR] File not found: {file_path}")
            sys.exit(1)
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        title = args.title or f"Crypto Risk Radar – 12H Report ({datetime.now().strftime('%Y-%m-%d %H:%M')})"
        
        result = publish_to_hashnode(content, title, publication_id)
        if result:
            # Save post info
            info_file = file_path.parent / f"hashnode_{file_path.stem}.json"
            with open(info_file, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2)
            print(f"[INFO] Post info saved: {info_file}")
    
    elif args.action == 'update':
        if not args.post_id or not args.file:
            print("[ERROR] --post-id and --file required for update action")
            sys.exit(1)
        
        file_path = Path(args.file)
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        title = args.title or f"Updated: Crypto Risk Radar ({datetime.now().strftime('%Y-%m-%d %H:%M')})"
        
        update_post(args.post_id, content, title)
    
    elif args.action == 'delete':
        if not args.post_id:
            print("[ERROR] --post-id required for delete action")
            sys.exit(1)
        
        delete_post(args.post_id)
    
    elif args.action == 'list':
        posts = list_posts(publication_id)
        print(f"\nFound {len(posts)} posts:")
        for post in posts:
            print(f"  - {post['title']}")
            print(f"    URL: {post['url']}")
            print(f"    Views: {post.get('views', 'N/A')}")
            print()

if __name__ == '__main__':
    main()
