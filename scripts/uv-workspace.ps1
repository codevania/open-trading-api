param(
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]] $UvArgs
)

$ErrorActionPreference = "Stop"

if (-not $UvArgs -or $UvArgs.Count -eq 0) {
    Write-Error "Usage: .\scripts\uv-workspace.ps1 run python <args>"
}

$repoRoot = Split-Path -Parent $PSScriptRoot
$cacheDir = Join-Path $repoRoot ".uv-cache"

& uv --cache-dir $cacheDir @UvArgs
exit $LASTEXITCODE
