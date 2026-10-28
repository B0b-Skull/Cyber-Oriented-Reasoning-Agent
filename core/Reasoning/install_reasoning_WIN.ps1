<#
.SYNOPSIS
  Windows PowerShell Installer, Hardware-Adaptive Profiler & Maintenance Script for CORA
  15-Engine Neuro-Symbolic, Somatic, Forecasting, Continual, Meta-Learning, Trajectory RL &
  Spectral PCA/K-Means++ Suite + 80/20 Pareto Gating (v4.5.0-15Engine-Core, 0 MB GPU VRAM).

.DESCRIPTION
  Analyzes Windows hardware compatibility (CPU threads, physical/available RAM, disk space,
  Python 3.9+ version, and GPU VRAM isolation), computes Hardware-Adaptive Reasoning Limits,
  and sets up all 15 CPU-based Reasoning Engines + 10 Guardrails + Uncapped CLI Extractor.

.EXAMPLE
  .\core\Reasoning\install_reasoning_WIN.ps1
  .\core\Reasoning\install_reasoning_WIN.ps1 -CheckCompat
  .\core\Reasoning\install_reasoning_WIN.ps1 -Status
  .\core\Reasoning\install_reasoning_WIN.ps1 -Test
  .\core\Reasoning\install_reasoning_WIN.ps1 -Seed
  .\core\Reasoning\install_reasoning_WIN.ps1 -SaveWheels
  .\core\Reasoning\install_reasoning_WIN.ps1 -Offline
#>
[CmdletBinding()]
param(
    [switch]$All,
    [switch]$CheckCompat,
    [switch]$InstallDeps,
    [switch]$Status,
    [switch]$Test,
    [switch]$Seed,
    [switch]$Offline,
    [Alias("DownloadWheels")]
    [switch]$SaveWheels
)

$ErrorActionPreference = "Stop"
try { [Console]::OutputEncoding = [System.Text.Encoding]::UTF8 } catch {}
$_ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$ReasoningDir = $_ScriptDir
$CoraCoreDir = Split-Path -Parent $ReasoningDir
$LogDir = Join-Path $CoraCoreDir "Log"
if (-not (Test-Path $LogDir)) {
    New-Item -ItemType Directory -Path $LogDir -Force | Out-Null
}
$PosturePs1 = Join-Path $CoraCoreDir "Network_Isolation\ConsolePostureDetection_WIN.ps1"
if (Test-Path $PosturePs1) {
    try { & $PosturePs1 -Detect -Quiet } catch {}
}
$InstallerPy = Join-Path $ReasoningDir "install_reasoning.py"

try {
    if (-not (Test-Path $InstallerPy)) {
        throw "Installer script not found at $InstallerPy"
    }

    Write-Host "=== Windows Host Pre-Flight Resource Verification (15-Engine Suite v4.5.0-15Engine-Core) ===" -ForegroundColor Cyan
    try {
        $osInfo = Get-CimInstance Win32_OperatingSystem -ErrorAction Stop
        $cpuInfo = Get-CimInstance Win32_Processor -ErrorAction Stop | Select-Object -First 1
        $totalRamMiB = [math]::Round($osInfo.TotalVisibleMemorySize / 1024)
        $freeRamMiB  = [math]::Round($osInfo.FreePhysicalMemory / 1024)
        $driveLetter = (Get-Item $ReasoningDir).PSDrive.Name
        $driveInfo   = Get-PSDrive $driveLetter -ErrorAction SilentlyContinue
        $freeDiskMiB = if ($driveInfo) { [math]::Round($driveInfo.Free / 1MB) } else { 10240 }

        Write-Host ("  CPU:       {0} ({1} threads)" -f $cpuInfo.Name.Trim(), $cpuInfo.NumberOfLogicalProcessors)
        Write-Host ("  RAM:       {0} MiB total, {1} MiB free" -f $totalRamMiB, $freeRamMiB)
        Write-Host ("  Disk Free: {0} MiB on drive {1}:" -f $freeDiskMiB, $driveLetter)

        if ($totalRamMiB -lt 2048 -or $freeRamMiB -lt 512) {
            throw "Insufficient system RAM ($freeRamMiB MiB free). At least 512 MiB free RAM required."
        }
        if ($freeDiskMiB -lt 250) {
            throw "Insufficient free disk space ($freeDiskMiB MiB free). At least 250 MiB required."
        }
    } catch {
        Write-Warning "WMI/CIM pre-flight check warning: $($_.Exception.Message) (Delegating to Python resource analyzer)"
    }

    $PythonCmd = $null
    $prevEAP = $ErrorActionPreference
    $ErrorActionPreference = "Continue"
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
        throw "Python 3.9+ was not found in PATH. Install Python via 'winget install Python.Python.3.12' or https://python.org."
    }

    $PyArgs = @($InstallerPy)
    if ($CheckCompat)    { $PyArgs += "--check-compat" }
    elseif ($InstallDeps){ $PyArgs += "--install-deps" }
    elseif ($Status)     { $PyArgs += "--status" }
    elseif ($Test)       { $PyArgs += "--test" }
    elseif ($Seed)       { $PyArgs += "--seed" }
    elseif ($SaveWheels) { $PyArgs += "--download-wheels" }
    elseif ($Offline)    { $PyArgs += @("--check-compat", "--install-deps", "--offline", "--seed", "--test") }
    else                 { $PyArgs += "--all" }

    & $PythonCmd @PyArgs
    if ($LASTEXITCODE -ne 0) {
        throw "install_reasoning.py exited with non-zero code $LASTEXITCODE"
    }
    exit 0
} catch {
    Write-Host "`n[FATAL ERROR] $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}
