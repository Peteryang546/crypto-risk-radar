#!/usr/bin/env python3
"""
Token Discovery Script for Crypto Risk Radar
Scans DEX Screener for new tokens and adds to research queue
"""

import requests
import json
import pandas as pd
from datetime import datetime
import os

EXCEL_PATH = "F:\\stepclaw\\agents\\blockchain-analyst\\token_research_queue.xlsx"

def fetch_new_tokens():
    """
    Fetch recently created tokens from DEX Screener API
    Criteria: Created within last 24h, liquidity > $10k, volume > $5k
    """
    try:
        # DEX Screener API endpoint for new pairs
        url = "https://api.dexscreener.com/latest/dex/search?q=ETH"
        response = requests.get(url, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            pairs = data.get('pairs', [])
            
            candidates = []
            for pair in pairs[:20]:  # Check top 20
                try:
                    # Basic filters
                    liquidity = float(pair.get('liquidity', {}).get('usd', 0) or 0)
                    volume_24h = float(pair.get('volume', {}).get('h24', 0) or 0)
                    
                    if liquidity >= 10000 and volume_24h >= 5000:
                        token = {
                            'name': pair.get('baseToken', {}).get('name', 'Unknown'),
                            'symbol': pair.get('baseToken', {}).get('symbol', 'Unknown'),
                            'address': pair.get('baseToken', {}).get('address', ''),
                            'chain': pair.get('chainId', 'unknown'),
                            'liquidity': liquidity,
                            'volume_24h': volume_24h,
                            'pair_address': pair.get('pairAddress', '')
                        }
                        candidates.append(token)
                except (ValueError, TypeError):
                    continue
            
            return candidates
        else:
            print(f"API Error: {response.status_code}")
            return []
            
    except Exception as e:
        print(f"Error fetching tokens: {e}")
        return []

def load_existing_queue():
    """Load existing Excel queue"""
    if os.path.exists(EXCEL_PATH):
        return pd.read_excel(EXCEL_PATH)
    else:
        return pd.DataFrame(columns=[
            'Token Name', 'Contract Address', 'Chain', 'Discovery Date',
            'Category', 'Status', 'Notes', 'Research URL'
        ])

def add_to_queue(tokens):
    """Add new tokens to Excel queue"""
    df = load_existing_queue()
    existing_addresses = set(df['Contract Address'].dropna().str.lower())
    
    new_entries = []
    for token in tokens:
        if token['address'].lower() not in existing_addresses:
            new_entries.append({
                'Token Name': f"{token['name']} (${token['symbol']})",
                'Contract Address': token['address'],
                'Chain': token['chain'],
                'Discovery Date': datetime.now().strftime('%Y-%m-%d'),
                'Category': 'Pending',
                'Status': '待分析',
                'Notes': f"Liquidity: ${token['liquidity']:,.0f}, Volume 24h: ${token['volume_24h']:,.0f}",
                'Research URL': ''
            })
    
    if new_entries:
        new_df = pd.DataFrame(new_entries)
        df = pd.concat([df, new_df], ignore_index=True)
        df.to_excel(EXCEL_PATH, index=False)
        print(f"Added {len(new_entries)} new tokens to queue")
        return new_entries
    else:
        print("No new tokens found")
        return []

def main():
    """Main discovery loop"""
    print(f"[{datetime.now()}] Starting token discovery...")
    
    tokens = fetch_new_tokens()
    if tokens:
        new_tokens = add_to_queue(tokens)
        print(f"Discovery complete. Found {len(new_tokens)} new candidates.")
    else:
        print("No tokens discovered this run.")

if __name__ == "__main__":
    main()
