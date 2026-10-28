<#
.SYNOPSIS
  Windows PowerShell Troubleshooting & Layered Reasoning Fault-Isolation Script for CORA
  (`Troubleshooting\troubleshoot_llm_WIN.ps1` — `v3.6.1`).

.DESCRIPTION
  Identifies areas of concern across the Windows host (CPU, RAM, GPU VRAM, Disk space) and isolates
  which layer or engine of the 15-Engine Neuro-Symbolic Reasoning Suite + Zero-Loss Context VM +
  10 Guardrails (including Uncapped Cross-Platform CLI Extractor & H-MDP Solver) could be causing an issue.

.EXAMPLE
  .\Troubleshooting\troubleshoot_llm_WIN.ps1
  .\Troubleshooting\troubleshoot_llm_WIN.ps1 -Fix
  .\Troubleshooting\troubleshoot_llm_WIN.ps1 -DiagnoseCmd "ping 198.51.100.10"
  .\Troubleshooting\troubleshoot_llm_WIN.ps1 -ExplainArbiter "curl exit 7 on target API endpoint"
  .\Troubleshooting\troubleshoot_llm_WIN.ps1 -Json
#>
[CmdletBinding()]
param(
    [switch]$Fix,
    [switch]$Quick,
    [string]$DiagnoseCmd = "",
    [string]$SimOutput = "",
    [int]$SimExit = 0,
    [string]$ExplainArbiter = "",
    [switch]$Json,
    [switch]$NoColor
)

$ErrorActionPreference = "Stop"
try { [Console]::OutputEncoding = [System.Text.Encoding]::UTF8 } catch {}
$TroubleshootDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$CorePy = Join-Path $TroubleshootDir "troubleshoot_core.py"

Write-Host "==============================================================================" -ForegroundColor Blue
Write-Host "  PRE-FLIGHT WINDOWS HOST, RAM, GPU & DISK DIAGNOSTICS" -ForegroundColor White
Write-Host "==============================================================================" -ForegroundColor Blue

try {
    $osInfo = Get-CimInstance Win32_OperatingSystem -ErrorAction Stop
    $cpuInfo = Get-CimInstance Win32_Processor -ErrorAction Stop | Select-Object -First 1
    $totalRamMiB = [math]::Round($osInfo.TotalVisibleMemorySize / 1024)
    $freeRamMiB  = [math]::Round($osInfo.FreePhysicalMemory / 1024)
    $usedPct     = [math]::Round((($totalRamMiB - $freeRamMiB) * 100.0) / [math]::Max(1, $totalRamMiB))

    Write-Host ("  [OK]      CPU: {0} ({1} logical threads)" -f $cpuInfo.Name.Trim(), $cpuInfo.NumberOfLogicalProcessors) -ForegroundColor Green
    if ($usedPct -ge 90) {
        Write-Host ("  [CONCERN] System RAM usage is high: {0}% used ({1} MiB free of {2} MiB)" -f $usedPct, $freeRamMiB, $totalRamMiB) -ForegroundColor Yellow
    } else {
        Write-Host ("  [OK]      System RAM healthy: {0}% used ({1} MiB free of {2} MiB)" -f $usedPct, $freeRamMiB, $totalRamMiB) -ForegroundColor Green
    }
} catch {
    Write-Warning "Could not query WMI/CIM host metrics: $($_.Exception.Message)"
}

# Check NVIDIA GPU if nvidia-smi is available
$prevEAP = $ErrorActionPreference
$ErrorActionPreference = "Continue"
if (Get-Command "nvidia-smi" -ErrorAction SilentlyContinue) {
    $gpuOut = & nvidia-smi --query-gpu=name,memory.used,memory.total,temperature.gpu --format=csv,noheader,nounits 2>$null
    if ($LASTEXITCODE -eq 0 -and $gpuOut) {
        Write-Host ("  [OK]      NVIDIA GPU Status: {0}" -f ($gpuOut | Select-Object -First 1)) -ForegroundColor Green
    }
}

# Locate Python 3.9+
$PythonCmd = $null
foreach ($cand in @("python", "py", "python3")) {
    if (Get-Command $cand -ErrorAction SilentlyContinue) {
        $verCheck = & $cand -c "import sys; print(1 if sys.version_info >= (3, 9) else 0)" 2>$null
        if ($LASTEXITCODE -eq 0 -and "$verCheck".Trim() -eq "1") {
            $PythonCmd = $cand
            break
        }
    }
}
$ErrorActionPreference = $prevEAP

if (-not $PythonCmd) {
    Write-Host "  [FAULT]   Python 3.9+ not found in PATH." -ForegroundColor Red
    exit 1
}

$PyArgs = @($CorePy)
if ($Fix)            { $PyArgs += "--fix" }
if ($Quick)          { $PyArgs += "--quick" }
if ($DiagnoseCmd)    { $PyArgs += @("--diagnose-cmd", $DiagnoseCmd) }
if ($SimOutput)      { $PyArgs += @("--sim-output", $SimOutput) }
if ($SimExit -ne 0)  { $PyArgs += @("--sim-exit", "$SimExit") }
if ($ExplainArbiter) { $PyArgs += @("--explain-arbiter", $ExplainArbiter) }
if ($Json)           { $PyArgs += "--json" }
if ($NoColor)        { $PyArgs += "--no-color" }

& $PythonCmd @PyArgs
exit $LASTEXITCODE
