try {
    $resp = Invoke-RestMethod -Uri "https://api.dexscreener.com/latest/dex/pairs/ethereum/0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2" -TimeoutSec 30
    Write-Output "Pairs found: $($resp.pairs.Count)"
    if ($resp.pairs.Count -gt 0) {
        $resp.pairs | Select-Object -First 3 | ForEach-Object {
            Write-Output "Token: $($_.baseToken.symbol), Liquidity: $($_.liquidity.usd)"
        }
    }
} catch {
    Write-Output "Error: $($_.Exception.Message)"
}
