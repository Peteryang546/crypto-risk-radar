#!/usr/bin/env python3
"""
Risk Math Models
Implements quantitative risk metrics based on academic research
- EWMA-VaR for tail risk estimation
- GARCH-inspired volatility regime detection
"""

import numpy as np
import subprocess
import json
from datetime import datetime, timedelta


class RiskMathModels:
    """Quantitative risk models for crypto assets"""
    
    def __init__(self):
        self.lambda_ewma = 0.94  # RiskMetrics standard
        self.var_confidence = 0.99  # 99% VaR
    
    def fetch_price_history(self, coin_id='bitcoin', days=90):
        """Fetch historical price data from CoinGecko"""
        ps_code = f'''
        try {{
            $url = "https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart?vs_currency=usd&days={days}"
            $resp = Invoke-RestMethod -Uri $url -TimeoutSec 30
            
            $prices = $resp.prices | ForEach-Object {{ $_[1] }}
            
            @{{ status = "success"; prices = $prices }} | ConvertTo-Json -Depth 10
        }} catch {{
            @{{ status = "error"; message = $_.Exception.Message }} | ConvertTo-Json
        }}
        '''
        
        try:
            result = subprocess.run(
                ["powershell", "-Command", ps_code],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0:
                data = json.loads(result.stdout)
                if data.get('status') == 'success':
                    return data.get('prices', [])
        except Exception as e:
            print(f"[WARNING] Price history fetch failed: {e}")
        
        return []
    
    def calculate_returns(self, prices):
        """Calculate daily returns from price series"""
        if len(prices) < 2:
            return []
        
        prices = np.array(prices)
        returns = np.diff(prices) / prices[:-1]
        return returns
    
    def ewma_volatility(self, returns, annualize=True):
        """
        Calculate EWMA volatility
        Based on RiskMetrics standard (lambda = 0.94)
        """
        if len(returns) < 2:
            return 0, []
        
        returns = np.array(returns)
        
        # Initialize with sample variance
        var = np.var(returns)
        ewma_var = [var]
        
        # EWMA recursion
        for ret in returns[1:]:
            var = self.lambda_ewma * var + (1 - self.lambda_ewma) * ret**2
            ewma_var.append(var)
        
        current_vol = np.sqrt(ewma_var[-1])
        
        if annualize:
            current_vol = current_vol * np.sqrt(365)
        
        return current_vol, ewma_var
    
    def calculate_var(self, returns, confidence=0.99, method='historical'):
        """
        Calculate Value at Risk
        
        Methods:
        - 'historical': Historical simulation (non-parametric)
        - 'parametric': Parametric (normal distribution)
        """
        if len(returns) < 30:
            return None
        
        returns = np.array(returns)
        
        if method == 'historical':
            # Historical simulation
            var = np.percentile(returns, (1 - confidence) * 100)
        else:
            # Parametric (normal) - using standard normal quantile
            # Z-score for 99% confidence is approximately 2.326
            z_score = 2.32634787404084  # norm.ppf(0.99)
            mean = np.mean(returns)
            std = np.std(returns)
            var = mean - z_score * std
        
        return var
    
    def calculate_var_ewma(self, returns, confidence=0.99):
        """
        Calculate VaR using EWMA volatility
        This is the recommended method for crypto (non-stationary volatility)
        """
        if len(returns) < 30:
            return None
        
        # Get current EWMA volatility (daily)
        current_vol_daily, _ = self.ewma_volatility(returns, annualize=False)
        
        # VaR = -Z * sigma (Z-score for 99% confidence ≈ 2.326)
        z_score = 2.32634787404084  # norm.ppf(0.99)
        var = -z_score * current_vol_daily
        
        return var
    
    def volatility_regime(self, returns, lookback_days=30):
        """
        Determine volatility regime and percentile
        """
        if len(returns) < lookback_days * 2:
            return None
        
        # Current volatility (EWMA, annualized)
        current_vol, _ = self.ewma_volatility(returns, annualize=True)
        
        # Historical rolling volatility for comparison
        rolling_vols = []
        for i in range(lookback_days, len(returns)):
            window = returns[i-lookback_days:i]
            vol = np.std(window) * np.sqrt(365)
            rolling_vols.append(vol)
        
        if not rolling_vols:
            return None
        
        # Calculate percentile manually
        sorted_vols = sorted(rolling_vols)
        n = len(sorted_vols)
        
        # Find position
        pos = 0
        for i, vol in enumerate(sorted_vols):
            if vol >= current_vol:
                pos = i
                break
        else:
            pos = n
        
        percentile = (pos / n) * 100
        
        # Determine regime
        if percentile >= 80:
            regime = 'High'
        elif percentile >= 50:
            regime = 'Moderate'
        else:
            regime = 'Low'
        
        return {
            'current_vol': current_vol,
            'percentile': percentile,
            'regime': regime,
            'historical_median': np.median(rolling_vols)
        }
    
    def get_btc_eth_risk_metrics(self):
        """
        Get comprehensive risk metrics for BTC and ETH
        Returns dict with VaR and volatility data
        """
        results = {}
        
        for coin_id, symbol in [('bitcoin', 'BTC'), ('ethereum', 'ETH')]:
            print(f"[INFO] Calculating risk metrics for {symbol}...")
            
            # Fetch 90 days of price history
            prices = self.fetch_price_history(coin_id, days=90)
            
            if len(prices) < 30:
                print(f"[WARNING] Insufficient data for {symbol}")
                results[symbol] = None
                continue
            
            # Calculate returns
            returns = self.calculate_returns(prices)
            
            # Calculate metrics
            var_99 = self.calculate_var_ewma(returns, confidence=0.99)
            vol_regime = self.volatility_regime(returns)
            
            results[symbol] = {
                'var_99_daily': var_99,
                'var_99_pct': var_99 * 100 if var_99 else None,
                'volatility_regime': vol_regime,
                'data_points': len(returns)
            }
            
            if var_99:
                print(f"[OK] {symbol} 99% VaR: {var_99*100:.2f}%")
            if vol_regime:
                print(f"[OK] {symbol} Vol: {vol_regime['current_vol']*100:.1f}% ({vol_regime['percentile']:.0f}th percentile)")
        
        return results


def test_risk_models():
    """Test risk math models"""
    print("="*70)
    print("TESTING RISK MATH MODELS")
    print("="*70)
    
    models = RiskMathModels()
    results = models.get_btc_eth_risk_metrics()
    
    print("\n" + "="*70)
    print("RESULTS")
    print("="*70)
    
    for symbol, data in results.items():
        if data:
            print(f"\n{symbol}:")
            print(f"  99% VaR (daily): {data['var_99_pct']:.2f}%")
            if data['volatility_regime']:
                vr = data['volatility_regime']
                print(f"  Volatility: {vr['current_vol']*100:.1f}% (annualized)")
                print(f"  Percentile: {vr['percentile']:.0f}th")
                print(f"  Regime: {vr['regime']}")
    
    print("="*70)


if __name__ == "__main__":
    test_risk_models()
