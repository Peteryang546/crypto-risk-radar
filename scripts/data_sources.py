#!/usr/bin/env python3
"""
区块链风险雷达 - 免费数据源配置
完全免费的数据源替代方案
"""

import sys
sys.path.insert(0, r'F:\stepclaw\workspace\lib')

import requests
import json
from datetime import datetime
from typing import Dict, Any, Optional

class FreeDataSources:
    """免费数据源聚合器"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'CryptoRiskRadar/1.0 (Research Purpose)'
        })
    
    # ========== 1. 价格数据 ==========
    
    def get_binance_price(self, symbol: str = "BTCUSDT") -> Optional[Dict]:
        """从Binance获取实时价格 - 完全免费，无限制 (需要VPN)"""
        try:
            url = f"https://api.binance.com/api/v3/ticker/24hr?symbol={symbol}"
            response = self.session.get(url, timeout=10)
            data = response.json()
            
            return {
                'price': float(data['lastPrice']),
                'change_24h': float(data['priceChangePercent']),
                'high_24h': float(data['highPrice']),
                'low_24h': float(data['lowPrice']),
                'volume_24h': float(data['volume']),
                'quote_volume': float(data['quoteVolume']),
                'source': 'Binance',
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            print(f"[WARN] Binance price error (may need VPN): {e}")
            return None
    
    def get_coingecko_price_direct(self, coin_id: str = "bitcoin") -> Optional[Dict]:
        """从CoinGecko获取价格 - 备选方案 (无需VPN)"""
        try:
            url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=usd&include_24hr_change=true"
            response = self.session.get(url, timeout=15)
            data = response.json()
            
            if coin_id in data:
                return {
                    'price': data[coin_id]['usd'],
                    'change_24h': data[coin_id].get('usd_24h_change', 0),
                    'source': 'CoinGecko',
                    'timestamp': datetime.now().isoformat()
                }
            return None
        except Exception as e:
            print(f"[WARN] CoinGecko direct error: {e}")
            return None
    
    def get_binance_funding_rate(self, symbol: str = "BTCUSDT") -> Optional[Dict]:
        """从Binance获取资金费率 - 完全免费"""
        try:
            url = f"https://fapi.binance.com/fapi/v1/premiumIndex?symbol={symbol}"
            response = self.session.get(url, timeout=10)
            data = response.json()
            
            return {
                'funding_rate': float(data['lastFundingRate']),
                'mark_price': float(data['markPrice']),
                'index_price': float(data['indexPrice']),
                'estimated_rate': float(data.get('estimatedSettlePrice', 0)),
                'source': 'Binance Futures',
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            print(f"[WARN] Binance funding error: {e}")
            return None
    
    def get_coingecko_prices(self, ids: list = None) -> Optional[Dict]:
        """从CoinGecko获取价格 - 免费版 (50 calls/min)"""
        if ids is None:
            ids = ['bitcoin', 'ethereum']
        
        try:
            ids_str = ','.join(ids)
            url = f"https://api.coingecko.com/api/v3/simple/price?ids={ids_str}&vs_currencies=usd&include_24hr_change=true&include_market_cap=true&include_24hr_vol=true"
            response = self.session.get(url, timeout=15)
            data = response.json()
            
            result = {}
            for coin_id in ids:
                if coin_id in data:
                    result[coin_id] = {
                        'price': data[coin_id]['usd'],
                        'change_24h': data[coin_id].get('usd_24h_change', 0),
                        'market_cap': data[coin_id].get('usd_market_cap', 0),
                        'volume_24h': data[coin_id].get('usd_24h_vol', 0),
                        'source': 'CoinGecko',
                        'timestamp': datetime.now().isoformat()
                    }
            return result
        except Exception as e:
            print(f"[WARN] CoinGecko error: {e}")
            return None
    
    # ========== 2. 情绪数据 ==========
    
    def get_fear_greed_index(self) -> Optional[Dict]:
        """从Alternative.me获取恐惧贪婪指数 - 完全免费"""
        try:
            url = "https://api.alternative.me/fng/?limit=1"
            response = self.session.get(url, timeout=10)
            data = response.json()
            
            if 'data' in data and len(data['data']) > 0:
                item = data['data'][0]
                return {
                    'value': int(item['value']),
                    'label': item['value_classification'],
                    'timestamp': datetime.fromtimestamp(int(item['timestamp'])).isoformat(),
                    'source': 'Alternative.me'
                }
            return None
        except Exception as e:
            print(f"[WARN] Fear & Greed error: {e}")
            return None
    
    # ========== 3. DEX数据 ==========
    
    def get_dex_screener_trending(self, chain: str = "solana", limit: int = 10) -> Optional[list]:
        """从DEX Screener获取热门代币 - 完全免费"""
        try:
            url = f"https://api.dexscreener.com/token-profiles/latest/v1"
            response = self.session.get(url, timeout=15)
            data = response.json()
            
            tokens = []
            if 'profiles' in data:
                for profile in data['profiles'][:limit]:
                    token = {
                        'token_address': profile.get('tokenAddress', ''),
                        'chain': profile.get('chainId', ''),
                        'description': profile.get('description', ''),
                        'links': profile.get('links', []),
                        'source': 'DEX Screener',
                        'timestamp': datetime.now().isoformat()
                    }
                    tokens.append(token)
            
            return tokens
        except Exception as e:
            print(f"[WARN] DEX Screener error: {e}")
            return None
    
    def get_dex_screener_token(self, chain: str, address: str) -> Optional[Dict]:
        """获取特定代币的DEX数据"""
        try:
            url = f"https://api.dexscreener.com/tokens/v1/{chain}/{address}"
            response = self.session.get(url, timeout=10)
            data = response.json()
            
            if isinstance(data, list) and len(data) > 0:
                pair = data[0]
                return {
                    'price': float(pair.get('priceUsd', 0)),
                    'liquidity': pair.get('liquidity', {}).get('usd', 0),
                    'volume_24h': pair.get('volume', {}).get('h24', 0),
                    'price_change_24h': pair.get('priceChange', {}).get('h24', 0),
                    'buys_24h': pair.get('txns', {}).get('h24', {}).get('buys', 0),
                    'sells_24h': pair.get('txns', {}).get('h24', {}).get('sells', 0),
                    'source': 'DEX Screener',
                    'timestamp': datetime.now().isoformat()
                }
            return None
        except Exception as e:
            print(f"[WARN] DEX Screener token error: {e}")
            return None
    
    # ========== 4. DeFi数据 ==========
    
    def get_defi_llama_tvl(self, protocol: str = None) -> Optional[Dict]:
        """从DeFi Llama获取TVL数据 - 完全免费"""
        try:
            if protocol:
                url = f"https://api.llama.fi/tvl/{protocol}"
            else:
                url = "https://api.llama.fi/charts"
            
            response = self.session.get(url, timeout=15)
            data = response.json()
            
            return {
                'data': data,
                'source': 'DeFi Llama',
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            print(f"[WARN] DeFi Llama error: {e}")
            return None
    
    # ========== 5. 全局数据 ==========
    
    def get_global_data(self) -> Optional[Dict]:
        """获取全局市场数据"""
        try:
            url = "https://api.coingecko.com/api/v3/global"
            response = self.session.get(url, timeout=10)
            data = response.json()
            
            if 'data' in data:
                return {
                    'active_cryptocurrencies': data['data']['active_cryptocurrencies'],
                    'markets': data['data']['markets'],
                    'total_market_cap': data['data']['total_market_cap']['usd'],
                    'total_volume': data['data']['total_volume']['usd'],
                    'market_cap_change_24h': data['data']['market_cap_change_percentage_24h_usd'],
                    'btc_dominance': data['data']['market_cap_percentage']['btc'],
                    'eth_dominance': data['data']['market_cap_percentage']['eth'],
                    'source': 'CoinGecko Global',
                    'timestamp': datetime.now().isoformat()
                }
            return None
        except Exception as e:
            print(f"[WARN] Global data error: {e}")
            return None
    
    # ========== 6. 聚合获取 ==========
    
    def fetch_all(self) -> Dict[str, Any]:
        """获取所有可用数据 (自动使用备选源)"""
        print("[INFO] Fetching data from free sources...")
        
        # 尝试Binance，失败则使用CoinGecko
        btc_price = self.get_binance_price("BTCUSDT")
        if not btc_price:
            btc_price = self.get_coingecko_price_direct("bitcoin")
        
        eth_price = self.get_binance_price("ETHUSDT")
        if not eth_price:
            eth_price = self.get_coingecko_price_direct("ethereum")
        
        data = {
            'btc_price': btc_price,
            'eth_price': eth_price,
            'btc_funding': self.get_binance_funding_rate("BTCUSDT"),
            'fear_greed': self.get_fear_greed_index(),
            'global': self.get_global_data(),
            'dex_trending': self.get_dex_screener_trending(),
            'defi_tvl': self.get_defi_llama_tvl(),
            'timestamp': datetime.now().isoformat()
        }
        
        # 统计成功/失败
        success = sum(1 for v in data.values() if v is not None and not isinstance(v, str))
        total = len([k for k in data.keys() if k != 'timestamp'])
        print(f"[INFO] Data fetch complete: {success}/{total} sources successful")
        
        return data

# 便捷函数
def get_free_data() -> Dict[str, Any]:
    """一键获取所有免费数据"""
    sources = FreeDataSources()
    return sources.fetch_all()

if __name__ == '__main__':
    # 测试数据源
    print("="*70)
    print("FREE DATA SOURCES TEST")
    print("="*70)
    
    data = get_free_data()
    
    print("\n" + "="*70)
    print("RESULTS")
    print("="*70)
    
    for key, value in data.items():
        if key == 'timestamp':
            continue
        status = "[OK]" if value else "[FAIL]"
        print(f"{status} {key}: {'OK' if value else 'Failed'}")
