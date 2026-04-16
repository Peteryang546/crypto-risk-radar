#!/usr/bin/env python3
"""
区块链风险雷达 - PowerShell数据源
使用PowerShell Invoke-RestMethod获取数据（支持系统代理）
"""

import subprocess
import json
from datetime import datetime
from typing import Dict, Any, Optional

class PowerShellDataSources:
    """使用PowerShell获取数据（支持系统代理）"""
    
    def run_ps_command(self, command: str) -> Optional[Dict]:
        """运行PowerShell命令并返回JSON结果"""
        try:
            # 使用PowerShell执行命令
            ps_cmd = f"""
            $ProgressPreference = 'SilentlyContinue'
            try {{
                {command}
            }} catch {{
                Write-Output '{{"error": "$($_.Exception.Message)"}}'
            }}
            """
            
            result = subprocess.run(
                ["powershell", "-Command", ps_cmd],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0 and result.stdout.strip():
                try:
                    return json.loads(result.stdout.strip())
                except:
                    return {"raw": result.stdout.strip()}
            
            return None
        except Exception as e:
            print(f"[WARN] PowerShell error: {e}")
            return None
    
    def get_btc_price(self) -> Optional[Dict]:
        """获取BTC价格"""
        cmd = """
        $data = Invoke-RestMethod -Uri "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd&include_24hr_change=true" -Method GET -TimeoutSec 15
        $result = @{
            price = $data.bitcoin.usd
            change_24h = $data.bitcoin.usd_24h_change
            source = "CoinGecko"
            timestamp = (Get-Date -Format "yyyy-MM-ddTHH:mm:ss")
        }
        $result | ConvertTo-Json -Compress
        """
        return self.run_ps_command(cmd)
    
    def get_eth_price(self) -> Optional[Dict]:
        """获取ETH价格"""
        cmd = """
        $data = Invoke-RestMethod -Uri "https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd&include_24hr_change=true" -Method GET -TimeoutSec 15
        $result = @{
            price = $data.ethereum.usd
            change_24h = $data.ethereum.usd_24h_change
            source = "CoinGecko"
            timestamp = (Get-Date -Format "yyyy-MM-ddTHH:mm:ss")
        }
        $result | ConvertTo-Json -Compress
        """
        return self.run_ps_command(cmd)
    
    def get_fear_greed(self) -> Optional[Dict]:
        """获取恐惧贪婪指数"""
        cmd = """
        $data = Invoke-RestMethod -Uri "https://api.alternative.me/fng/?limit=1" -Method GET -TimeoutSec 10
        $item = $data.data[0]
        $result = @{
            value = [int]$item.value
            label = $item.value_classification
            timestamp = (Get-Date -Format "yyyy-MM-ddTHH:mm:ss")
            source = "Alternative.me"
        }
        $result | ConvertTo-Json -Compress
        """
        return self.run_ps_command(cmd)
    
    def get_global_data(self) -> Optional[Dict]:
        """获取全局市场数据"""
        cmd = """
        $data = Invoke-RestMethod -Uri "https://api.coingecko.com/api/v3/global" -Method GET -TimeoutSec 15
        $result = @{
            total_market_cap = $data.data.total_market_cap.usd
            total_volume = $data.data.total_volume.usd
            market_cap_change_24h = $data.data.market_cap_change_percentage_24h_usd
            btc_dominance = $data.data.market_cap_percentage.btc
            eth_dominance = $data.data.market_cap_percentage.eth
            source = "CoinGecko Global"
            timestamp = (Get-Date -Format "yyyy-MM-ddTHH:mm:ss")
        }
        $result | ConvertTo-Json -Compress
        """
        return self.run_ps_command(cmd)
    
    def fetch_all(self) -> Dict[str, Any]:
        """获取所有数据"""
        print("[INFO] Fetching data via PowerShell...")
        
        data = {
            'btc_price': self.get_btc_price(),
            'eth_price': self.get_eth_price(),
            'fear_greed': self.get_fear_greed(),
            'global': self.get_global_data(),
            'timestamp': datetime.now().isoformat()
        }
        
        success = sum(1 for v in data.values() if v is not None and isinstance(v, dict) and 'error' not in v)
        total = len([k for k in data.keys() if k != 'timestamp'])
        print(f"[INFO] Data fetch complete: {success}/{total} sources successful")
        
        return data

def get_data() -> Dict[str, Any]:
    """获取数据（主入口）"""
    sources = PowerShellDataSources()
    return sources.fetch_all()

if __name__ == '__main__':
    print("="*70)
    print("POWERSHELL DATA SOURCES TEST")
    print("="*70)
    
    data = get_data()
    
    print("\n" + "="*70)
    print("RESULTS")
    print("="*70)
    
    for key, value in data.items():
        if key == 'timestamp':
            continue
        if value and isinstance(value, dict) and 'error' not in value:
            print(f"[OK] {key}: {value.get('price', value.get('value', 'OK'))}")
        else:
            print(f"[FAIL] {key}: Failed")
