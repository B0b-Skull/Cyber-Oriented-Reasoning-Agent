<#
.SYNOPSIS
    setup_cora_WIN.ps1 -- Master Windows Setup Script for CORA (llama.cpp CUDA/CPU + Qwen 3.8/3.5 GGUF Models + 15-Engine Hardware-Adaptive Reasoning + Two-Tier Projects/Vault Memory Isolation + Multi-Modal/OCR Training + Console Posture Detection, v4.5.0-15Engine-Core)

.DESCRIPTION
    Full Windows equivalent of setup_cora_NIX.sh. Configures the entire CORA stack on Windows:
      1. Auto-detects CPU physical cores/threads, NUMA topology, System RAM, and NVIDIA GPU VRAM to select optimal defaults and hardware tier (`ULTRA_SERVER_DATACENTER`, `EXTREME_WORKSTATION`, `HIGH_PERFORMANCE`, `PORTABLE_CONSERVATIVE`).
      2. Initializes all workspace directories (`core\Log\`, `core\bin\`, `models\`, `Projects\`, `core\ObsidianVault\`, `core\Reasoning\`, `core\Network_Isolation\`, `Troubleshooting\`, `Training\`, `core\Explained\`) and `00_MEMORY_INDEX.md`.
      3. Downloads & verifies prebuilt Windows `llama.cpp` (`b11802`) CUDA 12.4 x64 binaries + CUDA runtime DLLs into `core\bin\` (with automatic CPU x64 fallback).
      4. Downloads & verifies the GGUF LLM models into `models\` with automatic resume (`curl.exe -C -`):
           - `Qwen3.5-9B-Uncensored-Q4_K_M.gguf` (~5.24 GiB, >= 5.5 GB verified)
           - `Qwen3.8-27B-Uncensored-Q3_K_M.gguf` (~12.40 GiB, >= 13.0 GB verified; auto-selected when RAM >= 15 GiB or `-AllModels` / `-Only38`)
           - `Qwen3.8-27B-Turbo-MTP-Q4_K_M.gguf` (~17.23 GiB Multiple Token Prediction; auto-selected when RAM >= 24 GiB or VRAM >= 16 GiB, or `-Turbo` / `-OnlyTurboQ4` / `-AllTurbo` / `-AllModels`)
           - `Qwen3.8-27B-Turbo-MTP-Q6_K.gguf` (~22.38 GiB Multiple Token Prediction; auto-selected when RAM >= 48 GiB or VRAM >= 24 GiB, or `-OnlyTurboQ6` / `-AllTurbo` / `-AllModels`)
           - `Qwen3.8-27B-Turbo-MTP-Q8_0.gguf` (~28.16 GiB Multiple Token Prediction; auto-selected when RAM >= 64 GiB or VRAM >= 32 GiB, or `-OnlyTurboQ8` / `-AllTurbo` / `-AllModels`)
      5. Runs `core\Network_Isolation\ConsolePostureDetection_WIN.ps1 -Detect` to detect active network security posture.
      6. Runs `core\Reasoning\install_reasoning_WIN.ps1` to profile the target hardware, compute hardware-adaptive scaling parameters for all 15 CPU Neuro-Symbolic Reasoning Engines (0 MB GPU VRAM), and seed/test all 15 engines.
      7. Runs `Training\train_llm_WIN.ps1 -CheckDeps` to verify/install Multi-Modal (PDF/DOCX/HTML/SVG) & CPU Neural OCR dependencies.
      8. Runs `Troubleshooting\troubleshoot_llm_WIN.ps1 -Quick` to verify all 8 Layers (A-H), 15 Engines, and 10 Guardrails (0 Faults, 0 Concerns).
      9. Displays `.\run_cora_WIN.ps1 models`, `.\run_cora_WIN.ps1 tune`, and Quick Start commands.

.EXAMPLE
    .\setup_cora_WIN.ps1
    .\setup_cora_WIN.ps1 -AllModels
    .\setup_cora_WIN.ps1 -AllTurbo
    .\setup_cora_WIN.ps1 -Turbo
    .\setup_cora_WIN.ps1 -OnlyTurboQ6
    .\setup_cora_WIN.ps1 -OnlyTurboQ8
    .\setup_cora_WIN.ps1 -Only35
    .\setup_cora_WIN.ps1 -Only38
    .\setup_cora_WIN.ps1 -SkipModels
    .\setup_cora_WIN.ps1 -Offline
#>
[CmdletBinding()]
param(
    [switch]$AllModels,
    [switch]$AllTurbo,
    [switch]$Turbo,
    [switch]$OnlyTurboQ4,
    [switch]$OnlyTurboQ6,
    [switch]$OnlyTurboQ8,
    [switch]$Only35,
    [switch]$Only38,
    [switch]$SkipModels,
    [switch]$SkipReasoning,
    [switch]$Offline,
    [switch]$SkipTests,
    [string]$Dir = "",
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$RemainingArgs = @()
)

$ErrorActionPreference = "Stop"
try { [Console]::OutputEncoding = [System.Text.Encoding]::UTF8 } catch {}

# Support Linux-style double-dash flags if passed on the command line
for ($i = 0; $i -lt $RemainingArgs.Count; $i++) {
    $a = $RemainingArgs[$i].ToLowerInvariant()
    switch ($a) {
        "--all-models" { $AllModels = $true }
        "--all-turbo" { $AllTurbo = $true }
        "--turbo" { $Turbo = $true }
        "--only-turbo-q4" { $OnlyTurboQ4 = $true }
        "--only-turbo-q6" { $OnlyTurboQ6 = $true }
        "--only-turbo-q8" { $OnlyTurboQ8 = $true }
        "--only-3.5" { $Only35 = $true }
        "--only-3.8" { $Only38 = $true }
        "--skip-models" { $SkipModels = $true }
        "--skip-reasoning" { $SkipReasoning = $true }
        "--offline" { $Offline = $true }
        "--skip-tests" { $SkipTests = $true }
        "--dir" {
            if (($i + 1) -lt $RemainingArgs.Count) {
                $Dir = $RemainingArgs[$i + 1]
                $i++
            }
        }
        { $_ -in @("-h", "--help", "help") } {
            Get-Help $MyInvocation.MyCommand.Path -Detailed
            exit 0
        }
    }
}

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$CoraRoot = if (-not [string]::IsNullOrWhiteSpace($Dir)) {
    if (-not (Test-Path $Dir)) { New-Item -ItemType Directory -Path $Dir -Force | Out-Null }
    (Resolve-Path $Dir).Path
} elseif ((Split-Path -Leaf $ScriptDir) -ieq "core") {
    Split-Path -Parent $ScriptDir
} else {
    $ScriptDir
}
$BaseDir = Join-Path $CoraRoot "core"

# Constants matching setup_cora_NIX.sh
$LlamaBuildTag = "b11802"
$WinCudaBinUrl = "https://github.com/ggml-org/llama.cpp/releases/download/$LlamaBuildTag/llama-$LlamaBuildTag-bin-win-cuda-12.4-x64.zip"
$WinCudaRtUrl  = "https://github.com/ggml-org/llama.cpp/releases/download/$LlamaBuildTag/cudart-llama-bin-win-cuda-12.4-x64.zip"
$WinCpuBinUrl  = "https://github.com/ggml-org/llama.cpp/releases/download/$LlamaBuildTag/llama-$LlamaBuildTag-bin-win-cpu-x64.zip"

$Qwen38Url      = "https://huggingface.co/0bserverx/Qwen3.8-27B-Heretic-Abliterated-Uncensored-GGUF/resolve/main/RVN-Q3_K_M-multilingual.gguf"
$Qwen38File     = "Qwen3.8-27B-Uncensored-Q3_K_M.gguf"
$Qwen38MinBytes = 13000000000L

$Qwen35Url      = "https://huggingface.co/HauhauCS/Qwen3.5-9B-Uncensored-HauhauCS-Aggressive/resolve/main/Qwen3.5-9B-Uncensored-HauhauCS-Aggressive-Q4_K_M.gguf"
$Qwen35File     = "Qwen3.5-9B-Uncensored-Q4_K_M.gguf"
$Qwen35AltFile  = "Qwen3.5-9B-Uncensored-HauhauCS-Aggressive-Q4_K_M.gguf"
$Qwen35MinBytes = 5500000000L

$Qwen38TurboHfBase     = "https://huggingface.co/DavidAU/Qwen3.8-27B-TURBO-Fable-Cold-Fusion-735-882-Heretic-Uncensored-NEO-CODER-MAX-MTP-GGUF/resolve/main"
$Qwen38TurboQ4Url      = "$Qwen38TurboHfBase/Qwen3.8-27B-TurboFCFusion-735-882-Here-Uncen-NEO-CODER-MAX-MTP-Q4_K_M.gguf"
$Qwen38TurboQ4File     = "Qwen3.8-27B-Turbo-MTP-Q4_K_M.gguf"
$Qwen38TurboQ4HfFile   = "Qwen3.8-27B-TurboFCFusion-735-882-Here-Uncen-NEO-CODER-MAX-MTP-Q4_K_M.gguf"
$Qwen38TurboQ4MinBytes = 18000000000L

$Qwen38TurboQ6Url      = "$Qwen38TurboHfBase/Qwen3.8-27B-TurboFCFusion-735-882-Here-Uncen-NEO-CODER-MAX-MTP-Q6_K.gguf"
$Qwen38TurboQ6File     = "Qwen3.8-27B-Turbo-MTP-Q6_K.gguf"
$Qwen38TurboQ6HfFile   = "Qwen3.8-27B-TurboFCFusion-735-882-Here-Uncen-NEO-CODER-MAX-MTP-Q6_K.gguf"
$Qwen38TurboQ6MinBytes = 23500000000L

$Qwen38TurboQ8Url      = "$Qwen38TurboHfBase/Qwen3.8-27B-TurboFCFusion-735-882-Here-Uncen-NEO-CODER-MAX-MTP-Q8_0.gguf"
$Qwen38TurboQ8File     = "Qwen3.8-27B-Turbo-MTP-Q8_0.gguf"
$Qwen38TurboQ8HfFile   = "Qwen3.8-27B-TurboFCFusion-735-882-Here-Uncen-NEO-CODER-MAX-MTP-Q8_0.gguf"
$Qwen38TurboQ8MinBytes = 29500000000L

Write-Host "==============================================================================" -ForegroundColor Cyan
Write-Host "  CORA Windows Master Setup + GGUF Models + 15-Engine Suite (v4.5.0-15Engine-Core)" -ForegroundColor Cyan
Write-Host "==============================================================================" -ForegroundColor Cyan

# ------------------------------------------------------------------------------
# 0. Hardware Discovery & Model Selection
# ------------------------------------------------------------------------------
$TotalRamMib = 8192
$PhysCores = 4
$LogicalThreads = [Environment]::ProcessorCount
$CpuSockets = 1
try {
    $osInfo = Get-CimInstance Win32_OperatingSystem -ErrorAction SilentlyContinue
    if ($osInfo) {
        $TotalRamMib = [int][Math]::Round($osInfo.TotalVisibleMemorySize / 1024)
    }
    $cpuInfos = @(Get-CimInstance Win32_Processor -ErrorAction SilentlyContinue)
    if ($cpuInfos.Count -gt 0) {
        $CpuSockets = $cpuInfos.Count
        $PhysCores = [int](($cpuInfos | Measure-Object -Property NumberOfCores -Sum).Sum)
        $LogicalThreads = [int](($cpuInfos | Measure-Object -Property NumberOfLogicalProcessors -Sum).Sum)
    }
} catch {}

$HasNvidiaGpu = $false
$GpuCount = 0
$TotalVramMib = 0
$GpuSummary = "None detected (CPU mode)"
$nvidiaSmi = Get-Command nvidia-smi -ErrorAction SilentlyContinue
if ($nvidiaSmi) {
    $oldEap = $ErrorActionPreference
    $ErrorActionPreference = "Continue"
    try {
        $gpuOut = & $nvidiaSmi.Source --query-gpu=name,memory.total --format=csv,noheader,nounits 2>$null
        if ($LASTEXITCODE -eq 0 -and $gpuOut) {
            $HasNvidiaGpu = $true
            $gpuLines = @($gpuOut -split "`r?`n" | Where-Object { -not [string]::IsNullOrWhiteSpace($_) })
            $GpuCount = $gpuLines.Count
            foreach ($line in $gpuLines) {
                $parts = $line -split ","
                if ($parts.Count -ge 2) {
                    $vramVal = 0
                    if ([int]::TryParse($parts[-1].Trim(), [ref]$vramVal)) {
                        $TotalVramMib += $vramVal
                    }
                }
            }
            $GpuSummary = "$($gpuLines[0].Trim()) MiB (GPUs: $GpuCount, Total VRAM: $TotalVramMib MiB)"
        }
    } catch {} finally {
        $ErrorActionPreference = $oldEap
    }
}

$HwTier = if (($TotalVramMib -ge 40000) -or ($TotalRamMib -ge 120000) -or ($PhysCores -ge 32)) {
    "ULTRA_SERVER_DATACENTER"
} elseif (($TotalVramMib -ge 20000) -or ($TotalRamMib -ge 60000) -or ($PhysCores -ge 16)) {
    "EXTREME_WORKSTATION"
} elseif (($TotalVramMib -ge 10000) -or ($TotalRamMib -ge 28000) -or ($PhysCores -ge 8)) {
    "HIGH_PERFORMANCE"
} else {
    "PORTABLE_CONSERVATIVE"
}

$Download35 = $false
$Download38 = $false
$DownloadTurboQ4 = $false
$DownloadTurboQ6 = $false
$DownloadTurboQ8 = $false

if ($Only35) {
    $Download35 = $true
} elseif ($Only38) {
    $Download38 = $true
} elseif ($OnlyTurboQ4 -or $Turbo) {
    $DownloadTurboQ4 = $true
} elseif ($OnlyTurboQ6) {
    $DownloadTurboQ6 = $true
} elseif ($OnlyTurboQ8) {
    $DownloadTurboQ8 = $true
} elseif ($AllTurbo) {
    $DownloadTurboQ4 = $true
    $DownloadTurboQ6 = $true
    $DownloadTurboQ8 = $true
} elseif ($AllModels) {
    $Download35 = $true
    $Download38 = $true
    $DownloadTurboQ4 = $true
    $DownloadTurboQ6 = $true
    $DownloadTurboQ8 = $true
} else {
    $Download35 = $true
    if ($TotalRamMib -ge 15000) {
        $Download38 = $true
    } else {
        Write-Host "[WARN] System has $TotalRamMib MiB RAM (<15 GB); defaulting to Qwen3.5-9B only (pass -AllModels to force Qwen3.8-27B)." -ForegroundColor Yellow
    }
    # Auto-select Qwen3.8-27B Turbo MTP models where practical for the host RAM / GPU VRAM
    if (($TotalRamMib -ge 24000) -or ($TotalVramMib -ge 16000)) {
        $DownloadTurboQ4 = $true
    }
    if (($TotalRamMib -ge 48000) -or ($TotalVramMib -ge 24000)) {
        $DownloadTurboQ6 = $true
    }
    if (($TotalRamMib -ge 64000) -or ($TotalVramMib -ge 32000)) {
        $DownloadTurboQ8 = $true
    }
}
if ($SkipModels -or $Offline) {
    $Download35 = $false
    $Download38 = $false
    $DownloadTurboQ4 = $false
    $DownloadTurboQ6 = $false
    $DownloadTurboQ8 = $false
}

Write-Host "  Target Directory : $BaseDir"
Write-Host "  Hardware Tier    : $HwTier (Cores: $PhysCores physical / $LogicalThreads threads, Sockets/NUMA: $CpuSockets)"
Write-Host "  Detected RAM     : $TotalRamMib MiB"
Write-Host "  Detected GPU     : $GpuSummary"
Write-Host "  Models to Ensure : Qwen3.5-9B=$Download35 | Qwen3.8-27B=$Download38 | Turbo-MTP-Q4=$DownloadTurboQ4 | Turbo-MTP-Q6=$DownloadTurboQ6 | Turbo-MTP-Q8=$DownloadTurboQ8"

# ------------------------------------------------------------------------------
# 1. Workspace Directories & Obsidian Vault Initialization
# ------------------------------------------------------------------------------
Write-Host "`n[Step 1/7] Creating CORA directory structure & initializing Obsidian Knowledge Vault..." -ForegroundColor Yellow
foreach ($rootSub in @("models", "Projects", "Training", "Troubleshooting", "core")) {
    $rPath = Join-Path $CoraRoot $rootSub
    if (-not (Test-Path $rPath)) {
        New-Item -ItemType Directory -Path $rPath -Force | Out-Null
    }
}
$SubDirs = @(
    "Log",
    "bin",
    "open-webui-data",
    "ObsidianVault\.obsidian",
    "ObsidianVault\targets",
    "ObsidianVault\commands",
    "ObsidianVault\projects",
    "ObsidianVault\knowledge",
    "ObsidianVault\reasoning",
    "Reasoning",
    "Network_Isolation",
    "Explained\assets"
)
foreach ($sub in $SubDirs) {
    $dirPath = Join-Path $BaseDir $sub
    if (-not (Test-Path $dirPath)) {
        New-Item -ItemType Directory -Path $dirPath -Force | Out-Null
    }
}

# Migrate any legacy root-level logs into Log\
$LogDir = Join-Path $BaseDir "Log"
foreach ($legacyFile in @("llama-server.log", "llama-server.pid", "llama-server.model")) {
    $srcPath = Join-Path $BaseDir $legacyFile
    $dstPath = Join-Path $LogDir $legacyFile
    if ((Test-Path $srcPath) -and (-not (Test-Path $dstPath))) {
        Move-Item -Path $srcPath -Destination $dstPath -Force
    }
}

# Initialize ObsidianVault\.obsidian\app.json and 00_MEMORY_INDEX.md if missing
$VaultAppJson = Join-Path $BaseDir "ObsidianVault\.obsidian\app.json"
if (-not (Test-Path $VaultAppJson)) {
    $appJsonContent = @{
        alwaysUpdateLinks = $true
        newFileLocation = "folder"
        newFileFolderPath = "knowledge"
        showUnsupportedFiles = $false
        strictLineBreaks = $false
        readableLineLength = $true
    } | ConvertTo-Json -Depth 4
    Set-Content -Path $VaultAppJson -Value $appJsonContent -Encoding UTF8
}

$VaultIndexMd = Join-Path $BaseDir "ObsidianVault\00_MEMORY_INDEX.md"
if (-not (Test-Path $VaultIndexMd)) {
    $indexContent = @"
# CORA Knowledge & Memory Index (``00_MEMORY_INDEX``)

> **Tier-1 Hot Memory:** Automatically loaded into Qwen 3.8 / 3.5 on every session.

## Core Facts & Environment
- CORA Base Path: ``$BaseDir``
- Obsidian Vault Path: ``$(Join-Path $BaseDir 'ObsidianVault')``
- Always use ``scan_target`` before crafting ``curl`` requests against an unfamiliar URL or host.
- Save verified working ``curl`` commands, endpoints, and solutions using ``vault_save_note``.

## Indexed Vault Notes
<!-- AUTO-INDEX-START -->
<!-- AUTO-INDEX-END -->
"@
    Set-Content -Path $VaultIndexMd -Value $indexContent -Encoding UTF8
}

# ------------------------------------------------------------------------------
# 2. Download & Extract Windows llama.cpp Binaries (b11802 CUDA 12.4 / CPU x64)
# ------------------------------------------------------------------------------
$BinDir = Join-Path $BaseDir "bin"
$LlamaServerExe = Join-Path $BinDir "llama-server.exe"

function Test-LlamaServerBinary([string]$ExePath) {
    if (-not (Test-Path $ExePath)) { return $false }
    $oldEap = $ErrorActionPreference
    $ErrorActionPreference = "Continue"
    try {
        $env:PATH = "$BinDir;$env:PATH"
        $null = & $ExePath --version 2>$null
        return ($LASTEXITCODE -eq 0)
    } catch {
        return $false
    } finally {
        $ErrorActionPreference = $oldEap
    }
}

function Invoke-ResumableDownload([string]$Url, [string]$DestPath, [string]$Label) {
    $curlCmd = Get-Command curl.exe -ErrorAction SilentlyContinue
    if ($curlCmd) {
        Write-Host "  -> Downloading $Label via curl.exe (resumable)..." -ForegroundColor Cyan
        & $curlCmd.Source -fL --retry 5 --retry-delay 3 -C - -o $DestPath $Url
        if ($LASTEXITCODE -ne 0) {
            # If -C - fails on a completed or incompatible range, retry fresh without -C -
            & $curlCmd.Source -fL --retry 5 --retry-delay 3 -o $DestPath $Url
            if ($LASTEXITCODE -ne 0) {
                throw "Failed to download $Label from $Url (curl exit code $LASTEXITCODE)"
            }
        }
    } else {
        Write-Host "  -> Downloading $Label via Invoke-WebRequest..." -ForegroundColor Cyan
        Invoke-WebRequest -Uri $Url -OutFile $DestPath -UseBasicParsing
    }
}

function Expand-ZipFlatToBin([string]$ZipPath, [string]$TargetBinDir) {
    $tempExtract = Join-Path ([System.IO.Path]::GetTempPath()) ("llama_extract_" + [Guid]::NewGuid().ToString("N"))
    New-Item -ItemType Directory -Path $tempExtract -Force | Out-Null
    try {
        Expand-Archive -Path $ZipPath -DestinationPath $tempExtract -Force
        Get-ChildItem -Path $tempExtract -File -Recurse | ForEach-Object {
            Copy-Item -Path $_.FullName -Destination (Join-Path $TargetBinDir $_.Name) -Force
        }
    } finally {
        Remove-Item -Path $tempExtract -Recurse -Force -ErrorAction SilentlyContinue
    }
}

Write-Host "`n[Step 2/7] Checking Windows llama.cpp binaries (build $LlamaBuildTag)..." -ForegroundColor Yellow
if (Test-LlamaServerBinary $LlamaServerExe) {
    Write-Host "[OK] Working llama-server.exe already installed in $BinDir" -ForegroundColor Green
} elseif ($Offline) {
    Write-Host "[WARN] Offline mode active and llama-server.exe is not present in $BinDir." -ForegroundColor Yellow
} else {
    $installedLlama = $false
    if ($HasNvidiaGpu) {
        Write-Host "NVIDIA GPU detected ($GpuSummary) -- downloading llama.cpp $LlamaBuildTag CUDA 12.4 x64 binaries..." -ForegroundColor Cyan
        $cudaZip = Join-Path $BinDir "llama-$LlamaBuildTag-win-cuda.zip"
        $cudartZip = Join-Path $BinDir "cudart-$LlamaBuildTag-win-cuda.zip"
        try {
            Invoke-ResumableDownload -Url $WinCudaBinUrl -DestPath $cudaZip -Label "llama-$LlamaBuildTag-bin-win-cuda-12.4-x64.zip"
            Invoke-ResumableDownload -Url $WinCudaRtUrl -DestPath $cudartZip -Label "cudart-llama-bin-win-cuda-12.4-x64.zip"
            Expand-ZipFlatToBin -ZipPath $cudaZip -TargetBinDir $BinDir
            Expand-ZipFlatToBin -ZipPath $cudartZip -TargetBinDir $BinDir
            Remove-Item -Path $cudaZip, $cudartZip -Force -ErrorAction SilentlyContinue
            if (Test-LlamaServerBinary $LlamaServerExe) {
                Write-Host "[OK] Installed CUDA-accelerated llama-server.exe ($LlamaBuildTag) in $BinDir" -ForegroundColor Green
                $installedLlama = $true
            } else {
                Write-Host "[WARN] CUDA binary verification failed; falling back to CPU x64 build..." -ForegroundColor Yellow
            }
        } catch {
            Write-Host "[WARN] CUDA binary download/extraction failed ($($_.Exception.Message)); falling back to CPU x64 build..." -ForegroundColor Yellow
            Remove-Item -Path $cudaZip, $cudartZip -Force -ErrorAction SilentlyContinue
        }
    }

    if (-not $installedLlama) {
        Write-Host "Downloading llama.cpp $LlamaBuildTag Windows CPU x64 binaries..." -ForegroundColor Cyan
        $cpuZip = Join-Path $BinDir "llama-$LlamaBuildTag-win-cpu.zip"
        Invoke-ResumableDownload -Url $WinCpuBinUrl -DestPath $cpuZip -Label "llama-$LlamaBuildTag-bin-win-cpu-x64.zip"
        Expand-ZipFlatToBin -ZipPath $cpuZip -TargetBinDir $BinDir
        Remove-Item -Path $cpuZip -Force -ErrorAction SilentlyContinue
        if (-not (Test-LlamaServerBinary $LlamaServerExe)) {
            throw "llama-server.exe failed verification after extraction in $BinDir."
        }
        Write-Host "[OK] Installed CPU x64 llama-server.exe ($LlamaBuildTag) in $BinDir" -ForegroundColor Green
    }
}

# ------------------------------------------------------------------------------
# 3. Download & Verify GGUF LLM Models (Qwen3.5-9B & Qwen3.8-27B)
# ------------------------------------------------------------------------------
$ModelsDir = Join-Path $CoraRoot "models"

function Ensure-GgufModel([string]$Url, [string]$DestPath, [long]$MinBytes, [string]$Label) {
    if (Test-Path $DestPath) {
        $existingBytes = (Get-Item $DestPath).Length
        if ($existingBytes -ge $MinBytes) {
            $gib = "{0:N2}" -f ($existingBytes / 1GB)
            Write-Host "[OK] $Label already downloaded and verified ($gib GiB)" -ForegroundColor Green
            return
        }
        Write-Host "[WARN] Partial download detected for $Label ($existingBytes bytes < $MinBytes bytes); resuming..." -ForegroundColor Yellow
    } else {
        Write-Host "Downloading $Label -> $DestPath ..." -ForegroundColor Cyan
    }

    Invoke-ResumableDownload -Url $Url -DestPath $DestPath -Label $Label
    if (-not (Test-Path $DestPath)) {
        throw "Model download failed: $DestPath does not exist."
    }
    $finalBytes = (Get-Item $DestPath).Length
    if ($finalBytes -lt $MinBytes) {
        throw "Downloaded file $DestPath is too small ($finalBytes bytes, expected >= $MinBytes bytes). Re-run .\setup_cora_WIN.ps1 to resume."
    }
    $finalGib = "{0:N2}" -f ($finalBytes / 1GB)
    Write-Host "[OK] Verified $Label ($finalGib GiB / $finalBytes bytes)" -ForegroundColor Green
}

Write-Host "`n[Step 3/7] Ensuring GGUF CORA Models in $ModelsDir..." -ForegroundColor Yellow
if ($SkipModels -or $Offline) {
    Write-Host "[INFO] Skipping GGUF model downloads ($(if ($Offline) { '-Offline' } else { '-SkipModels' }) specified)." -ForegroundColor Cyan
} else {
    if ($Download35) {
        $q35Dest = Join-Path $ModelsDir $Qwen35File
        $q35AltDest = Join-Path $ModelsDir $Qwen35AltFile
        # If the HauhauCS-named file already exists and is complete, link/copy it to Qwen3.5-9B-Uncensored-Q4_K_M.gguf
        if ((-not (Test-Path $q35Dest)) -and (Test-Path $q35AltDest) -and ((Get-Item $q35AltDest).Length -ge $Qwen35MinBytes)) {
            New-Item -ItemType HardLink -Path $q35Dest -Target $q35AltDest -Force -ErrorAction SilentlyContinue | Out-Null
        }
        Ensure-GgufModel -Url $Qwen35Url -DestPath $q35Dest -MinBytes $Qwen35MinBytes -Label "Qwen3.5-9B-Uncensored-Q4_K_M.gguf (Fast 5.2 GiB)"
        if ((Test-Path $q35Dest) -and (-not (Test-Path $q35AltDest))) {
            try {
                New-Item -ItemType HardLink -Path $q35AltDest -Target $q35Dest -Force -ErrorAction Stop | Out-Null
            } catch {
                # Ignore if filesystem does not support hardlinks
            }
        }
    }

    if ($Download38) {
        $q38Dest = Join-Path $ModelsDir $Qwen38File
        Ensure-GgufModel -Url $Qwen38Url -DestPath $q38Dest -MinBytes $Qwen38MinBytes -Label "Qwen3.8-27B-Uncensored-Q3_K_M.gguf (Default 12.4 GiB)"
    }

    if ($DownloadTurboQ4) {
        $turboQ4Dest = Join-Path $ModelsDir $Qwen38TurboQ4File
        $turboQ4AltDest = Join-Path $ModelsDir $Qwen38TurboQ4HfFile
        Ensure-GgufModel -Url $Qwen38TurboQ4Url -DestPath $turboQ4Dest -MinBytes $Qwen38TurboQ4MinBytes -Label "Qwen3.8-27B-Turbo-MTP-Q4_K_M.gguf (MTP 17.2 GiB)"
        if ((Test-Path $turboQ4Dest) -and (-not (Test-Path $turboQ4AltDest))) {
            try { New-Item -ItemType HardLink -Path $turboQ4AltDest -Target $turboQ4Dest -Force -ErrorAction Stop | Out-Null } catch {}
        }
    }

    if ($DownloadTurboQ6) {
        $turboQ6Dest = Join-Path $ModelsDir $Qwen38TurboQ6File
        $turboQ6AltDest = Join-Path $ModelsDir $Qwen38TurboQ6HfFile
        Ensure-GgufModel -Url $Qwen38TurboQ6Url -DestPath $turboQ6Dest -MinBytes $Qwen38TurboQ6MinBytes -Label "Qwen3.8-27B-Turbo-MTP-Q6_K.gguf (MTP 22.4 GiB)"
        if ((Test-Path $turboQ6Dest) -and (-not (Test-Path $turboQ6AltDest))) {
            try { New-Item -ItemType HardLink -Path $turboQ6AltDest -Target $turboQ6Dest -Force -ErrorAction Stop | Out-Null } catch {}
        }
    }

    if ($DownloadTurboQ8) {
        $turboQ8Dest = Join-Path $ModelsDir $Qwen38TurboQ8File
        $turboQ8AltDest = Join-Path $ModelsDir $Qwen38TurboQ8HfFile
        Ensure-GgufModel -Url $Qwen38TurboQ8Url -DestPath $turboQ8Dest -MinBytes $Qwen38TurboQ8MinBytes -Label "Qwen3.8-27B-Turbo-MTP-Q8_0.gguf (MTP 28.2 GiB)"
        if ((Test-Path $turboQ8Dest) -and (-not (Test-Path $turboQ8AltDest))) {
            try { New-Item -ItemType HardLink -Path $turboQ8AltDest -Target $turboQ8Dest -Force -ErrorAction Stop | Out-Null } catch {}
        }
    }
}

# ------------------------------------------------------------------------------
# 4. Run ConsolePostureDetection_WIN.ps1
# ------------------------------------------------------------------------------
$PostureScript = Join-Path $BaseDir "Network_Isolation\ConsolePostureDetection_WIN.ps1"
if (Test-Path $PostureScript) {
    Write-Host "`n[Step 4/7] Running Windows Console Posture Detection..." -ForegroundColor Yellow
    & $PostureScript -Detect
}

# ------------------------------------------------------------------------------
# 5. Run 15-Engine Neuro-Symbolic Reasoning Suite Installer
# ------------------------------------------------------------------------------
$ReasoningInstaller = Join-Path $BaseDir "Reasoning\install_reasoning_WIN.ps1"
if ((-not $SkipReasoning) -and (Test-Path $ReasoningInstaller)) {
    Write-Host "`n[Step 5/7] Running 15-Engine Neuro-Symbolic, RL & PCA/K-Means++ Reasoning Installer (v4.5.0-15Engine-Core)..." -ForegroundColor Yellow
    if ($Offline) {
        & $ReasoningInstaller -Offline
    } else {
        & $ReasoningInstaller -All
    }
    if ($LASTEXITCODE -ne 0) {
        throw "core\Reasoning\install_reasoning_WIN.ps1 exited with code $LASTEXITCODE"
    }
}

# ------------------------------------------------------------------------------
# 6. Verify Multi-Modal Training, CPU Neural OCR & Uncapped Cross-Platform CLI Extractor
# ------------------------------------------------------------------------------
$TrainScript = Join-Path $CoraRoot "Training\train_llm_WIN.ps1"
if ((-not $Offline) -and (Test-Path $TrainScript)) {
    Write-Host "`n[Step 6/7] Verifying Uncapped Multi-Modal (PDF/DOCX/HTML/SVG), Cross-Platform CLI & CPU Neural OCR Training Modules..." -ForegroundColor Yellow
    & $TrainScript -CheckDeps
    if ($LASTEXITCODE -ne 0) {
        throw "Training\train_llm_WIN.ps1 -CheckDeps exited with code $LASTEXITCODE"
    }
}

# ------------------------------------------------------------------------------
# 7. Run Quick Troubleshooting Verification (8 Layers, 15 Engines & 10 Guardrails)
# ------------------------------------------------------------------------------
$TroubleshootScript = Join-Path $CoraRoot "Troubleshooting\troubleshoot_llm_WIN.ps1"
if ((-not $SkipTests) -and (Test-Path $TroubleshootScript)) {
    Write-Host "`n[Step 7/7] Verifying All 8 Layers, 15 Engines & 10 Guardrails (Including Uncapped CLI/MDP Extractor & RL/PCA)..." -ForegroundColor Yellow
    & $TroubleshootScript -Quick
    if ($LASTEXITCODE -ne 0) {
        throw "Troubleshooting\troubleshoot_llm_WIN.ps1 -Quick exited with code $LASTEXITCODE"
    }
}

# ------------------------------------------------------------------------------
# Final Summary & Hardware Profile Output
# ------------------------------------------------------------------------------
$ManagePs1 = Join-Path $CoraRoot "run_cora_WIN.ps1"
if (Test-Path $ManagePs1) {
    Write-Host ""
    & $ManagePs1 models
    Write-Host ""
    & $ManagePs1 tune
}

Write-Host "`n==============================================================================" -ForegroundColor Green
Write-Host "  [COMPLETE] C.O.R.A. Windows Setup Finished Successfully!" -ForegroundColor Green
Write-Host "==============================================================================" -ForegroundColor Green
Write-Host "  Quick Start Commands (PowerShell in $CoraRoot):"
Write-Host "    .\run_cora_WIN.ps1 cli                                         # Launch interactive C.O.R.A. CLI (Default 3.8 27B)"
Write-Host "    .\run_cora_WIN.ps1 cli -m 3.5 --dangerously-skip-permissions   # Launch fast Qwen3.5-9B Agent CLI"
Write-Host "    .\run_cora_WIN.ps1 start                                       # Start background llama-server + Open WebUI"
Write-Host "    .\run_cora_WIN.ps1 -train                                      # Distill & OCR .\Training\"
Write-Host "    .\run_cora_WIN.ps1 status                                      # Check server & GPU VRAM status"
Write-Host "==============================================================================" -ForegroundColor Green
