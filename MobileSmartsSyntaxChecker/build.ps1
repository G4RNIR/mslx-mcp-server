$ErrorActionPreference = "Stop"

$projectDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$outDir = Join-Path $projectDir "bin"
$csc = "C:\Windows\Microsoft.NET\Framework64\v4.0.30319\csc.exe"

if (-not (Test-Path -LiteralPath $csc)) {
    $csc = "C:\Windows\Microsoft.NET\Framework\v4.0.30319\csc.exe"
}

if (-not (Test-Path -LiteralPath $csc)) {
    throw "csc.exe for .NET Framework v4.0 was not found."
}

New-Item -ItemType Directory -Force -Path $outDir | Out-Null

$exePath = Join-Path $outDir "MobileSmartsSyntaxChecker.exe"
$sourcePath = Join-Path $projectDir "Program.cs"

& $csc `
    "/nologo" `
    "/target:exe" `
    "/platform:anycpu" `
    "/out:$exePath" `
    "/reference:System.Web.Extensions.dll" `
    "$sourcePath"

if ($LASTEXITCODE -ne 0) {
    throw "csc.exe failed with exit code $LASTEXITCODE."
}

Write-Host "Built $outDir\MobileSmartsSyntaxChecker.exe"
