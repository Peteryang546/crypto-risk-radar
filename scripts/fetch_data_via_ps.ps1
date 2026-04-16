# Fetch crypto data via PowerShell (bypasses Python SSL issues)
param(
    [string]$OutputFile = "data_ps.json"
)

$OutputPath = Join-Path "F:\stepclaw\agents\blockchain-analyst\output" $OutputFile

Write-Host "==============================================" -ForegroundColor Cyan
Write-Host "FETCHING CRYPTO DATA VIA POWERSHELL" -ForegroundColor Cyan
Write-Host "==============================================" -ForegroundColor Cyan

$data = @{}

# API Keys
$CoinGeckoApiKey = "CG-m57LMPhhuqyQs2QLzUJ6ozAK"

# 1. CoinGecko - Global data (with API key)
try {
    Write-Host "`n[1/4] Fetching CoinGecko global data..." -ForegroundColor Yellow
    $headers = @{ "x-cg-pro-api-key" = $CoinGeckoApiKey }
    $cgGlobal = Invoke-RestMethod -Uri "https://api.coingecko.com/api/v3/global" -Headers $headers -TimeoutSec 30
    $data['coingecko_global'] = $cgGlobal.data
    Write-Host "  [OK] Market cap: $($cgGlobal.data.total_market_cap.usd)" -ForegroundColor Green
} catch {
    Write-Host "  [FAIL] $($_.Exception.Message)" -ForegroundColor Red
}

# 2. CoinGecko - BTC price (with API key)
try {
    Write-Host "`n[2/4] Fetching BTC price..." -ForegroundColor Yellow
    $headers = @{ "x-cg-pro-api-key" = $CoinGeckoApiKey }
    $cgBtc = Invoke-RestMethod -Uri "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd&include_24hr_change=true" -Headers $headers -TimeoutSec 30
    $data['btc_price'] = @{ 'price' = $cgBtc.bitcoin.usd; 'change_24h' = $cgBtc.bitcoin.usd_24h_change }
    $data['eth_price'] = @{ 'price' = $cgBtc.ethereum.usd; 'change_24h' = $cgBtc.ethereum.usd_24h_change }
    Write-Host "  [OK] BTC: $($cgBtc.bitcoin.usd)" -ForegroundColor Green
} catch {
    Write-Host "  [FAIL] $($_.Exception.Message)" -ForegroundColor Red
}

# 3. Fear & Greed Index
try {
    Write-Host "`n[3/4] Fetching Fear & Greed Index..." -ForegroundColor Yellow
    $fng = Invoke-RestMethod -Uri "https://api.alternative.me/fng/?limit=1" -TimeoutSec 30
    $data['fear_greed'] = @{ 'value' = [int]$fng.data[0].value; 'label' = $fng.data[0].value_classification }
    Write-Host "  [OK] F&G: $($fng.data[0].value) - $($fng.data[0].value_classification)" -ForegroundColor Green
} catch {
    Write-Host "  [FAIL] $($_.Exception.Message)" -ForegroundColor Red
}

# 4. DEX Screener - Trending pairs
try {
    Write-Host "`n[4/4] Fetching DEX Screener trending..." -ForegroundColor Yellow
    $dex = Invoke-RestMethod -Uri "https://api.dexscreener.com/latest/dex/tokens/0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2" -TimeoutSec 30
    $pairs = $dex.pairs | Select-Object -First 5
    $data['dex_trending'] = $pairs | ForEach-Object { 
        @{
            symbol = $_.baseToken.symbol
            price = $_.priceUsd
            volume24h = $_.volume.h24
            liquidity = $_.liquidity.usd
        }
    }
    Write-Host "  [OK] Found $($pairs.Count) pairs" -ForegroundColor Green
} catch {
    Write-Host "  [FAIL] $($_.Exception.Message)" -ForegroundColor Red
}

# Save to JSON
$data | ConvertTo-Json -Depth 10 | Out-File -FilePath $OutputPath -Encoding UTF8

Write-Host "`n==============================================" -ForegroundColor Cyan
Write-Host "DATA SAVED TO: $OutputPath" -ForegroundColor Cyan
Write-Host "==============================================" -ForegroundColor Cyan
