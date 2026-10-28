<#
.SYNOPSIS
    Standalone & Integrated Multi-Modal Document, OCR, Diagram & Uncapped Cross-Platform CLI/MDP Training Script (v3.6.1)
.DESCRIPTION
    Reads technical documentation, PDFs, DOCX, scripts, and network diagrams (PNG/JPG/SVG)
    from Training/ (or a specified folder/file), auto-installs required Python
    modules (Pillow, pypdf, pymupdf, python-docx, beautifulsoup4, rapidocr-onnxruntime),
    rejoins multi-line wrapped PDF commands, verifies 100% of extracted cross-platform commands
    (Linux, Windows CMD/LOLBins, Sysinternals, Active Directory, PowerShell, Cloud, Mobile/Forensics,
    Red Team, Solaris, Cisco IOS) via Engine 12 (CEGAR) with zero artificial slice caps,
    deduplicates by SHA-256 content hash, and updates core/ObsidianVault/,
    core/Reasoning/data/trained_rules.json, and core/Reasoning/data/mdp_transitions.json.
.EXAMPLE
    .\Training\train_llm_WIN.ps1
    .\Training\train_llm_WIN.ps1 -Path .\Training -Force
    .\Training\train_llm_WIN.ps1 -Status
#>
[CmdletBinding()]
param(
    [Parameter(Position = 0)]
    [string]$Path = "",

    [switch]$Force,
    [switch]$NoLlm,
    [switch]$Status,
    [switch]$CheckDeps,
    [switch]$InstallDeps,
    [switch]$Json
)

$ErrorActionPreference = "Stop"
try { [Console]::OutputEncoding = [System.Text.Encoding]::UTF8 } catch {}
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$CoraRoot = Split-Path -Parent $ScriptDir
$CoreDir = Join-Path $CoraRoot "core"
$TrainPy = Join-Path $CoreDir "Reasoning\train_llm.py"
$DefaultTrainDir = $ScriptDir
$env:CORA_ROOT = $CoraRoot
$env:CORA_CORE_DIR = $CoreDir
$env:CORA_TRAINING_DIR = $DefaultTrainDir
$env:OBSIDIAN_VAULT_DIR = Join-Path $CoreDir "ObsidianVault"

if (-not (Test-Path $TrainPy)) {
    Write-Error "[ERROR] Missing training engine: $TrainPy"
    exit 1
}

if (-not (Test-Path $DefaultTrainDir)) {
    New-Item -ItemType Directory -Path $DefaultTrainDir -Force | Out-Null
}

$VenvPython = Join-Path $CoreDir "Reasoning\.venv\Scripts\python.exe"
$PythonExe = $null
if (Test-Path $VenvPython) {
    $PythonExe = $VenvPython
} else {
    $prevEAP = $ErrorActionPreference
    $ErrorActionPreference = "Continue"
    foreach ($cand in @("python", "py", "python3")) {
        if (Get-Command $cand -ErrorAction SilentlyContinue) {
            $verCheck = & $cand -c "import sys; print(1 if sys.version_info >= (3, 9) else 0)" 2>$null
            if ($LASTEXITCODE -eq 0 -and "$verCheck".Trim() -eq "1") {
                $PythonExe = $cand
                break
            }
        }
    }
    $ErrorActionPreference = $prevEAP
}
if (-not $PythonExe) {
    Write-Error "[ERROR] Python 3.9+ is required to run train_llm.py."
    exit 1
}

# Verify/auto-install Python multi-modal & OCR modules without triggering PowerShell NativeCommandError on stderr
$prevEAP = $ErrorActionPreference
$ErrorActionPreference = "Continue"
& $PythonExe -c "import sys, importlib.util; mods = ('PIL','pypdf','pymupdf','docx','bs4','rapidocr_onnxruntime'); sys.exit(0 if all(importlib.util.find_spec(m) for m in mods) else 1)" *>$null
$depsExitCode = $LASTEXITCODE
$ErrorActionPreference = $prevEAP

if ($CheckDeps -or $InstallDeps) {
    if ($depsExitCode -ne 0) {
        Write-Host "[TRAIN-DEPS] Verifying and auto-installing multi-modal extraction & CPU Neural OCR modules..." -ForegroundColor Cyan
    }
    $PyArgs = @($TrainPy, "--check-deps")
    if ($Json) { $PyArgs += "--json" }
    & $PythonExe @PyArgs
    exit $LASTEXITCODE
}

if ($depsExitCode -ne 0) {
    Write-Host "[TRAIN-DEPS] Verifying and auto-installing multi-modal extraction & CPU Neural OCR modules..." -ForegroundColor Cyan
    & $PythonExe $TrainPy --check-deps
}

$PyArgs = @($TrainPy)
if ($Path)      { $PyArgs += $Path }
if ($Force)     { $PyArgs += "--force" }
if ($NoLlm)     { $PyArgs += "--no-llm" }
if ($Status)    { $PyArgs += "--status" }
if ($Json)      { $PyArgs += "--json" }

& $PythonExe @PyArgs
exit $LASTEXITCODE
