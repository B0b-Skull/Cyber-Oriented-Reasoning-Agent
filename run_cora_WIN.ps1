<#
.SYNOPSIS
    run_cora_WIN.ps1 -- Windows Service, Hardware Auto-Tuner & Agent CLI Manager for CORA (llama.cpp CUDA/CPU + Custom CORA WebUI + 15-Engine Reasoning)

.DESCRIPTION
    Manages the CORA server (core\bin\llama-server.exe) + Custom CORA WebUI (Svelte/FastAPI) + CORA Agent CLI on Windows.
    Supports switching between:
      - qwen3.8 (DEFAULT):  Qwen3.8-27B-Uncensored-Q3_K_M.gguf (~12.4 GiB)
      - qwen3.5 (FAST):     Qwen3.5-9B-Uncensored-Q4_K_M.gguf (~5.2 GiB, HauhauCS-Aggressive)
      - turbo   (MTP-Q4):   Qwen3.8-27B-Turbo-MTP-Q4_K_M.gguf (~17.2 GiB, Multiple Token Prediction)
      - turbo-q6 (MTP-Q6):  Qwen3.8-27B-Turbo-MTP-Q6_K.gguf (~22.4 GiB, Multiple Token Prediction)
      - turbo-q8 (MTP-Q8):  Qwen3.8-27B-Turbo-MTP-Q8_0.gguf (~28.2 GiB, Multiple Token Prediction)
    Dynamically auto-detects CPU topology (physical/logical cores), system RAM, and NVIDIA GPU VRAM
    to configure llama-server.exe and agent-cli.py for peak efficiency.

.EXAMPLE
    .\run_cora_WIN.ps1 start
    .\run_cora_WIN.ps1 start -m 3.5
    .\run_cora_WIN.ps1 start -m turbo
    .\run_cora_WIN.ps1 cli -m 3.5 --dangerously-skip-permissions
    .\run_cora_WIN.ps1 cli -m 3.8 --dangerously-skip-permissions
    .\run_cora_WIN.ps1 cli -m turbo --dangerously-skip-permissions
    .\run_cora_WIN.ps1 cli -m turbo-q6 --dangerously-skip-permissions
    .\run_cora_WIN.ps1 cli -m turbo-q8 --dangerously-skip-permissions
    .\run_cora_WIN.ps1 download -m all-turbo
    .\run_cora_WIN.ps1 models
    .\run_cora_WIN.ps1 tune
    .\run_cora_WIN.ps1 -train Training
#>

$ErrorActionPreference = "Stop"
try { [Console]::OutputEncoding = [System.Text.Encoding]::UTF8 } catch {}

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$CoraRoot = if ((Split-Path -Leaf $ScriptDir) -ieq "core") { Split-Path -Parent $ScriptDir } else { $ScriptDir }
$BaseDir = if (Test-Path (Join-Path $CoraRoot "core")) { Join-Path $CoraRoot "core" } else { $CoraRoot }
$BinDir = Join-Path $BaseDir "bin"
$ModelsDir = if ($env:CORA_MODELS_DIR) { $env:CORA_MODELS_DIR } else { Join-Path $CoraRoot "models" }
$LogDir = Join-Path $BaseDir "Log"
$ProjectsDir = if ($env:CORA_PROJECTS_DIR) { $env:CORA_PROJECTS_DIR } else { Join-Path $CoraRoot "Projects" }
$TrainingDir = if ($env:CORA_TRAINING_DIR) { $env:CORA_TRAINING_DIR } else { Join-Path $CoraRoot "Training" }
$env:CORA_ROOT = $CoraRoot
$env:CORA_CORE_DIR = $BaseDir
$env:CORA_MODELS_DIR = $ModelsDir
$env:CORA_PROJECTS_DIR = $ProjectsDir
$env:CORA_TRAINING_DIR = $TrainingDir
$env:OBSIDIAN_VAULT_DIR = Join-Path $BaseDir "ObsidianVault"
foreach ($d in @($LogDir, $ProjectsDir, $ModelsDir, $TrainingDir)) {
    if (-not (Test-Path $d)) {
        New-Item -ItemType Directory -Path $d -Force | Out-Null
    }
}
# Ensure every existing project in Projects\ has a Files\ subdirectory
if (Test-Path $ProjectsDir) {
    Get-ChildItem -Path $ProjectsDir -Directory -ErrorAction SilentlyContinue | Where-Object { -not $_.Name.StartsWith(".") } | ForEach-Object {
        $fSub = Join-Path $_.FullName "Files"
        if (-not (Test-Path $fSub)) { New-Item -ItemType Directory -Path $fSub -Force | Out-Null }
    }
}

# Automatically migrate any legacy root-level pid/model/log files into Log\
foreach ($legacy in @("llama-server.pid", "llama-server.model", "llama-server.log")) {
    $src = Join-Path $BaseDir $legacy
    $dst = Join-Path $LogDir $legacy
    if ((Test-Path $src) -and (-not (Test-Path $dst))) {
        Move-Item -Path $src -Destination $dst -Force -ErrorAction SilentlyContinue
    }
}

$PidFile = Join-Path $LogDir "llama-server.pid"
$ActiveModelFile = Join-Path $LogDir "llama-server.model"
$LogFile = Join-Path $LogDir "llama-server.log"
$StdoutFile = Join-Path $LogDir "llama-server.stdout.log"
$WebuiPidFile = Join-Path $LogDir "webui.pid"
$WebuiLogFile = Join-Path $LogDir "webui.log"

$BindHost = if ($env:HOST) { $env:HOST } else { "127.0.0.1" }
$LlamaPort = if ($env:LLAMA_PORT) { $env:LLAMA_PORT } else { "8080" }
$WebuiPort = if ($env:WEBUI_PORT) { $env:WEBUI_PORT } else { "1337" }

$Qwen38Url             = "https://huggingface.co/0bserverx/Qwen3.8-27B-Heretic-Abliterated-Uncensored-GGUF/resolve/main/RVN-Q3_K_M-multilingual.gguf"
$Qwen38File            = "Qwen3.8-27B-Uncensored-Q3_K_M.gguf"
$Qwen38MinBytes        = 13000000000L

$Qwen35Url             = "https://huggingface.co/HauhauCS/Qwen3.5-9B-Uncensored-HauhauCS-Aggressive/resolve/main/Qwen3.5-9B-Uncensored-HauhauCS-Aggressive-Q4_K_M.gguf"
$Qwen35File            = "Qwen3.5-9B-Uncensored-Q4_K_M.gguf"
$Qwen35AltFile         = "Qwen3.5-9B-Uncensored-HauhauCS-Aggressive-Q4_K_M.gguf"
$Qwen35MinBytes        = 5500000000L

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

$ModelSelect = if ($env:MODEL) { $env:MODEL } else { "qwen3.8" }
$AgentMode = if ($env:AGENT_MODE) { $env:AGENT_MODE } else { "on" }
$SpecType = if ($env:SPEC_TYPE) { $env:SPEC_TYPE } else { "none" }
$ReasoningMode = if ($env:REASONING) { $env:REASONING } else { "off" }
$SkipPermissions = if ($env:SKIP_PERMISSIONS) { $env:SKIP_PERMISSIONS } else { "0" }
$NetisoConfigFile = Join-Path $BaseDir "Network_Isolation\network_isolation.conf"
$NetisoLevel = if ($env:LLM_ISOLATION_MODE) { $env:LLM_ISOLATION_MODE } else { "" }
$NetisoIfaces = if ($env:LLM_ALLOWED_IFACES) { $env:LLM_ALLOWED_IFACES } else { "" }
$ContinueSession = if ($env:LLM_CONTINUE_SESSION) { $env:LLM_CONTINUE_SESSION } else { "0" }

function Show-Usage {
    Write-Host @"
Usage: .\run_cora_WIN.ps1 {start|stop|restart|status|webui|webgui|models|download|tune|cli|continue|reason|train|posture|troubleshoot|logs} [-m MODEL] [options...]

Commands:
  start        Start llama-server.exe (with Agent tools + auto-detected tuning) and Custom CORA WebUI (port 1337)
  stop         Stop llama-server.exe and Custom CORA WebUI
  restart      Restart both services (optionally switching models with -m)
  status       Show service status, active model, auto-detected hardware profile, and GPU VRAM usage
  webui|webgui Start & open the Custom CORA WebUI Dashboard (http://127.0.0.1:1337)
  models       List installed & available models and show which model is active / default
  download     Download/verify a specific model (-m turbo | -m turbo-q6 | -m turbo-q8 | -m all-turbo | -m all)
  tune         Display the auto-detected hardware profile and exact flags without starting
  cli          Launch the interactive CORA Agent CLI with shell & file tools
  continue     Launch CORA Agent CLI and resume directly from the last saved session (alias for `cli --continue`)
  reason       Run CPU-based Neuro-Symbolic Reasoning Engine (status|test|seed|pipeline)
  train        Distill Training\ (or custom folder/file) + OCR diagrams into ObsidianVault & Reasoning (-train / --train)
  posture      Detect & apply console security posture theme (-Detect|-Apply|-Demo|-Reset)
  troubleshoot Run the 8-Layer CORA Troubleshooting & Diagnostics Suite
  logs         Show and follow llama-server logs (stored in core\Log\llama-server.log)

Model Selection Switch (-m / --model or `$env:MODEL):
  -m qwen3.8 | 3.8 | 27b | q3              Use Qwen3.8-27B-Uncensored-Q3_K_M.gguf (~12.4 GiB) [DEFAULT]
  -m qwen3.5 | 3.5 | 9b | fast             Use Qwen3.5-9B-Uncensored-Q4_K_M.gguf (~5.2 GiB, HauhauCS-Aggressive)
  -m turbo | mtp | turbo-q4 | mtp-q4 | q4  Use Qwen3.8-27B-Turbo-MTP-Q4_K_M.gguf (~17.2 GiB, Multiple Token Prediction)
  -m turbo-q6 | mtp-q6 | 3.8-q6 | q6       Use Qwen3.8-27B-Turbo-MTP-Q6_K.gguf (~22.4 GiB, Multiple Token Prediction)
  -m turbo-q8 | mtp-q8 | 3.8-q8 | q8       Use Qwen3.8-27B-Turbo-MTP-Q8_0.gguf (~28.2 GiB, Multiple Token Prediction)
  -m C:\path\to\model.gguf                 Use a custom GGUF model file

Session Continuation Switch (Agent CLI):
  -c, --continue, --resume                 Continue from the last CLI session (restores active project, goal,
                                           attempt ledger, and conversation history)

Network Isolation Switch (--network-isolation / -netiso <Red|White|Blue> [ifaces]):
  -netiso red   | --network-isolation red             Full network stack access (RED posture; all NICs & WAN open)
  -netiso white | --network-isolation white           Isolated by network namespace / loopback (WHITE posture; `lo` only)
  -netiso blue  | --network-isolation blue            Interface-locked isolation using static `BLUE_ALLOWED_IFACES`
                                                      from `core\Network_Isolation\network_isolation.conf`
  -netiso blue eth0,eth1                              Override config file and lock CLI strictly to `eth0` and `eth1`
  Shorthand aliases: -red | -white | -blue [eth0,eth1] | -netiso blue:eth0,eth1

Reasoning / Thinking Switch:
  --no-think                       Disable internal <think> monologue for instant answers [DEFAULT]
  --think                          Enable step-by-step <think> chain-of-thought reasoning

Permissions / Confirmation & Project Switches (Agent CLI):
  --confirm                              Prompt [y/N/a] before running shell commands or file writes [DEFAULT]
  --dangerously-skip-permissions         Auto-run all shell commands and file writes without confirming
  -P, --project <doc_path_or_dir> [name] Ingest documentation file/folder, verify data with user, and create/track
                                         an isolated project workspace in Projects\<name>\ (memory.md & downloads\)

Examples:
  .\run_cora_WIN.ps1 cli -m 3.8 -c                                   # Continue from the last session with Qwen3.8-27B
  .\run_cora_WIN.ps1 cli -m 3.8 -netiso red                          # Full network stack access (Red posture)
  .\run_cora_WIN.ps1 cli -m 3.8 --network-isolation white            # Isolated loopback posture (White posture)
  .\run_cora_WIN.ps1 cli -m 3.8 -netiso blue                         # Locked to static interfaces in network_isolation.conf
  .\run_cora_WIN.ps1 cli -m 3.8 -netiso blue eth0,eth1               # Override config and lock strictly to eth0 and eth1
  .\run_cora_WIN.ps1 cli -m 3.5 --dangerously-skip-permissions       # Agent CLI with Qwen3.5-9B (auto-run all commands)
  .\run_cora_WIN.ps1 cli -m 3.8 --dangerously-skip-permissions       # Default Qwen3.8 Agent CLI (auto-run)
  .\run_cora_WIN.ps1 cli -m turbo --dangerously-skip-permissions     # Agent CLI with Qwen3.8-27B Turbo MTP Q4_K_M
  .\run_cora_WIN.ps1 download -m all-turbo                           # Download all 3 Qwen3.8-27B Turbo MTP models
  .\run_cora_WIN.ps1 -train Training                                 # Train CORA & Reasoning on Training\
  .\run_cora_WIN.ps1 models                                          # List installed & available models
"@
}

$Action = "status"
$ActionSet = $false
$ExtraArgs = New-Object System.Collections.Generic.List[string]

for ($hi = 0; $hi -lt $args.Count; $hi++) {
    $curArg = [string]$args[$hi]
    if ($curArg -match '^(.+):(-h|--help)$') {
        $pyExe = if (Get-Command python -ErrorAction SilentlyContinue) { "python" } else { "python3" }
        & $pyExe (Join-Path $BaseDir "agent-cli.py") $Matches[1] "-h"
        exit 0
    } elseif ($curArg -in @("-h", "--help", "-?")) {
        if ($hi -gt 0) {
            $pyExe = if (Get-Command python -ErrorAction SilentlyContinue) { "python" } else { "python3" }
            & $pyExe (Join-Path $BaseDir "agent-cli.py") ([string]$args[$hi - 1]) "-h"
            exit 0
        } elseif (($hi + 1) -lt $args.Count) {
            $pyExe = if (Get-Command python -ErrorAction SilentlyContinue) { "python" } else { "python3" }
            & $pyExe (Join-Path $BaseDir "agent-cli.py") ([string]$args[$hi + 1]) "-h"
            exit 0
        }
    }
}

$i = 0
while ($i -lt $args.Count) {
    $arg = [string]$args[$i]
    $argLower = $arg.ToLowerInvariant()
    switch -Regex ($argLower) {
        '^(start|stop|restart|status|webui|webgui|-webui|--webui|-webgui|--webgui|gui|-gui|--gui|ui|dashboard|-dashboard|--dashboard|models|download|pull|tune|detect|cli|continue|resume|reason|reasoning|train|-train|--train|posture|troubleshoot|diag|diagnostics|logs|-h|--help|help)$' {
            if (-not $ActionSet) {
                if ($argLower -eq "-train" -or $argLower -eq "--train") {
                    $Action = "train"
                } elseif ($argLower -in @("webui", "webgui", "-webui", "--webui", "-webgui", "--webgui", "gui", "-gui", "--gui", "ui", "dashboard", "-dashboard", "--dashboard")) {
                    $Action = "webui"
                } elseif ($argLower -eq "pull") {
                    $Action = "download"
                } elseif ($argLower -eq "continue" -or $argLower -eq "resume") {
                    $Action = "cli"
                    $ContinueSession = "1"
                    $ExtraArgs.Add("--continue")
                } else {
                    $Action = $argLower
                }
                $ActionSet = $true
            } else {
                if ($argLower -eq "continue" -or $argLower -eq "resume") {
                    $ContinueSession = "1"
                    $ExtraArgs.Add("--continue")
                } else {
                    $ExtraArgs.Add($arg)
                }
            }
            $i++
            break
        }
        '^(-c|--continue|-continue|--resume|-resume)$' {
            $ContinueSession = "1"
            $ExtraArgs.Add("--continue")
            $i++
            break
        }
        '^(-netiso|--netiso|--network-isolation|-network-isolation|-n)$' {
            if (($i + 1) -ge $args.Count) {
                Write-Error "Error: $arg requires a color level: red, white, or blue [ifaces]"
                exit 2
            }
            $NetisoLevel = [string]$args[$i + 1]
            $i += 2
            if ($NetisoLevel.ToLowerInvariant() -eq "blue" -and $i -lt $args.Count) {
                $nextTok = [string]$args[$i]
                if (-not $nextTok.StartsWith("-") -and $nextTok.ToLowerInvariant() -notin @("cli","start","stop","restart","status","models","download","tune","continue","resume")) {
                    $NetisoIfaces = $nextTok
                    $i++
                }
            }
            break
        }
        '^(-red|--red)$' {
            $NetisoLevel = "red"
            $NetisoIfaces = ""
            $i++
            break
        }
        '^(-white|--white)$' {
            $NetisoLevel = "white"
            $NetisoIfaces = "lo"
            $i++
            break
        }
        '^(-blue|--blue)$' {
            $NetisoLevel = "blue"
            $i++
            if ($i -lt $args.Count) {
                $nextTok = [string]$args[$i]
                if (-not $nextTok.StartsWith("-") -and $nextTok.ToLowerInvariant() -notin @("cli","start","stop","restart","status","models","download","tune","continue","resume")) {
                    $NetisoIfaces = $nextTok
                    $i++
                }
            }
            break
        }
        '^(-m|--model|-model)$' {
            if (($i + 1) -ge $args.Count) {
                Write-Error "Error: $arg requires a model argument (e.g. qwen3.8, qwen3.5, turbo, turbo-q6, or turbo-q8)"
                exit 2
            }
            $ModelSelect = [string]$args[$i + 1]
            $i += 2
            break
        }
        '^(?:-m|--model|-model)[:=](.+)$' {
            $ModelSelect = $Matches[1]
            $i++
            break
        }
        '^(?:-netiso|--netiso|--network-isolation|-network-isolation)[:=](.+)$' {
            $NetisoLevel = $Matches[1]
            if ($NetisoLevel -match '^blue[:=](.+)$') {
                $NetisoIfaces = $Matches[1]
                $NetisoLevel = "blue"
            }
            $i++
            break
        }
        '^(--think|-think)$' {
            $ReasoningMode = "on"
            $i++
            break
        }
        '^(--no-think|-no-think|-nothink)$' {
            $ReasoningMode = "off"
            $i++
            break
        }
        '^(--dangerously-skip-permissions|-dangerously-skip-permissions|-dangerouslyskippermissions)$' {
            $SkipPermissions = "1"
            $i++
            break
        }
        '^(--confirm|-confirm)$' {
            $SkipPermissions = "0"
            $i++
            break
        }
        default {
            $ExtraArgs.Add($arg)
            $i++
            break
        }
    }
}

if ($ContinueSession -eq "1") {
    $env:LLM_CONTINUE_SESSION = "1"
}
if (-not [string]::IsNullOrWhiteSpace($NetisoLevel)) {
    $lvlLow = $NetisoLevel.Trim().ToLowerInvariant()
    if ($lvlLow -in @("white", "netns", "namespace", "airgap")) {
        $env:LLM_ISOLATION_MODE = "WHITE"
        $env:LLM_POSTURE_OVERRIDE = "WHITE"
        $env:LLM_ALLOWED_IFACES = "lo"
        $ExtraArgs.Add("-netiso")
        $ExtraArgs.Add("white")
    } elseif ($lvlLow -in @("blue", "lan", "usb", "isolated")) {
        $env:LLM_ISOLATION_MODE = "BLUE"
        $env:LLM_POSTURE_OVERRIDE = "BLUE"
        if (-not [string]::IsNullOrWhiteSpace($NetisoIfaces)) {
            $env:LLM_ALLOWED_IFACES = $NetisoIfaces
            $ExtraArgs.Add("-netiso")
            $ExtraArgs.Add("blue")
            $ExtraArgs.Add($NetisoIfaces)
        } else {
            $ExtraArgs.Add("-netiso")
            $ExtraArgs.Add("blue")
        }
    } else {
        $env:LLM_ISOLATION_MODE = "RED"
        $env:LLM_POSTURE_OVERRIDE = "RED"
        $ExtraArgs.Add("-netiso")
        $ExtraArgs.Add("red")
    }
}

function Resolve-PythonExe {
    $oldEap = $ErrorActionPreference
    $ErrorActionPreference = "Continue"
    try {
        foreach ($cand in @("python", "python3", "py")) {
            $cmd = Get-Command $cand -ErrorAction SilentlyContinue
            if ($cmd) {
                $ver = & $cmd.Source -c "import sys; print(sys.version_info.major)" 2>$null
                if ($LASTEXITCODE -eq 0 -and "$ver".Trim() -eq "3") {
                    return $cmd.Source
                }
            }
        }
    } finally {
        $ErrorActionPreference = $oldEap
    }
    throw "Python 3 is required but was not found on PATH."
}

$script:ModelDownloadUrl = ""
$script:ModelMinBytes = 0L
$script:ModelHfAltFile = ""
$script:ModelExpectedMib = 5366

function Resolve-Model([string]$Selector = $ModelSelect) {
    $selLower = $Selector.Trim().ToLowerInvariant()
    $q38Path = Join-Path $ModelsDir $Qwen38File
    $q35Path = Join-Path $ModelsDir $Qwen35File
    $q35AltPath = Join-Path $ModelsDir $Qwen35AltFile
    $turboQ4Path = Join-Path $ModelsDir $Qwen38TurboQ4File
    $turboQ4AltPath = Join-Path $ModelsDir $Qwen38TurboQ4HfFile
    $turboQ6Path = Join-Path $ModelsDir $Qwen38TurboQ6File
    $turboQ6AltPath = Join-Path $ModelsDir $Qwen38TurboQ6HfFile
    $turboQ8Path = Join-Path $ModelsDir $Qwen38TurboQ8File
    $turboQ8AltPath = Join-Path $ModelsDir $Qwen38TurboQ8HfFile

    $script:ModelDownloadUrl = ""
    $script:ModelMinBytes = 0L
    $script:ModelHfAltFile = ""
    $script:ModelExpectedMib = 5366

    switch ($selLower) {
        { $_ -in @("qwen3.8", "3.8", "27b", "qwen38", "q3", "q3_k_m", "default", "") } {
            if ((Test-Path $q38Path) -or (-not (Test-Path $q35Path) -and -not (Test-Path $q35AltPath)) -or ($selLower -ne "")) {
                $script:ModelKey = "qwen3.8"
                $script:ModelAlias = "Qwen3.8-27B-Uncensored-Q3_K_M"
                $script:ModelPath = if ($env:MODEL_PATH_OVERRIDE) { $env:MODEL_PATH_OVERRIDE } else { $q38Path }
                $script:ModelDownloadUrl = $Qwen38Url
                $script:ModelMinBytes = $Qwen38MinBytes
                $script:ModelExpectedMib = 12689
            } else {
                $script:ModelKey = "qwen3.5"
                $script:ModelAlias = "Qwen3.5-9B-Uncensored-Q4_K_M"
                $script:ModelPath = if (Test-Path $q35Path) { $q35Path } else { $q35AltPath }
                $script:ModelDownloadUrl = $Qwen35Url
                $script:ModelMinBytes = $Qwen35MinBytes
                $script:ModelExpectedMib = 5366
            }
        }
        { $_ -in @("qwen3.5", "3.5", "9b", "qwen35", "fast", "hauhaucs") } {
            $script:ModelKey = "qwen3.5"
            $script:ModelAlias = "Qwen3.5-9B-Uncensored-Q4_K_M"
            $script:ModelDownloadUrl = $Qwen35Url
            $script:ModelMinBytes = $Qwen35MinBytes
            $script:ModelHfAltFile = $Qwen35AltFile
            $script:ModelExpectedMib = 5366
            $script:ModelPath = if (Test-Path $q35Path) { $q35Path } elseif (Test-Path $q35AltPath) { $q35AltPath } else { $q35Path }
        }
        { $_ -in @("turbo", "mtp", "turbo-q4", "mtp-q4", "q4", "q4_k_m", "3.8-turbo", "3.8-mtp", "3.8-q4", "3.8-turbo-q4", "3.8-mtp-q4", "qwen3.8-turbo", "qwen3.8-mtp", "qwen3.8-turbo-q4", "qwen3.8-mtp-q4", "27b-turbo", "27b-mtp", "27b-q4") } {
            $script:ModelKey = "turbo-q4"
            $script:ModelAlias = "Qwen3.8-27B-Turbo-MTP-Q4_K_M"
            $script:ModelDownloadUrl = $Qwen38TurboQ4Url
            $script:ModelMinBytes = $Qwen38TurboQ4MinBytes
            $script:ModelHfAltFile = $Qwen38TurboQ4HfFile
            $script:ModelExpectedMib = 17642
            $script:ModelPath = if (Test-Path $turboQ4Path) { $turboQ4Path } elseif (Test-Path $turboQ4AltPath) { $turboQ4AltPath } else { $turboQ4Path }
        }
        { $_ -in @("turbo-q6", "mtp-q6", "q6", "q6_k", "3.8-turbo-q6", "3.8-mtp-q6", "3.8-q6", "qwen3.8-turbo-q6", "qwen3.8-mtp-q6", "27b-turbo-q6", "27b-mtp-q6", "27b-q6") } {
            $script:ModelKey = "turbo-q6"
            $script:ModelAlias = "Qwen3.8-27B-Turbo-MTP-Q6_K"
            $script:ModelDownloadUrl = $Qwen38TurboQ6Url
            $script:ModelMinBytes = $Qwen38TurboQ6MinBytes
            $script:ModelHfAltFile = $Qwen38TurboQ6HfFile
            $script:ModelExpectedMib = 22920
            $script:ModelPath = if (Test-Path $turboQ6Path) { $turboQ6Path } elseif (Test-Path $turboQ6AltPath) { $turboQ6AltPath } else { $turboQ6Path }
        }
        { $_ -in @("turbo-q8", "mtp-q8", "q8", "q8_0", "3.8-turbo-q8", "3.8-mtp-q8", "3.8-q8", "qwen3.8-turbo-q8", "qwen3.8-mtp-q8", "27b-turbo-q8", "27b-mtp-q8", "27b-q8") } {
            $script:ModelKey = "turbo-q8"
            $script:ModelAlias = "Qwen3.8-27B-Turbo-MTP-Q8_0"
            $script:ModelDownloadUrl = $Qwen38TurboQ8Url
            $script:ModelMinBytes = $Qwen38TurboQ8MinBytes
            $script:ModelHfAltFile = $Qwen38TurboQ8HfFile
            $script:ModelExpectedMib = 28838
            $script:ModelPath = if (Test-Path $turboQ8Path) { $turboQ8Path } elseif (Test-Path $turboQ8AltPath) { $turboQ8AltPath } else { $turboQ8Path }
        }
        default {
            $cand1 = $Selector
            $cand2 = Join-Path $ModelsDir $Selector
            if (Test-Path $cand1) {
                $script:ModelPath = (Resolve-Path $cand1).Path
            } elseif (Test-Path $cand2) {
                $script:ModelPath = (Resolve-Path $cand2).Path
            } else {
                Write-Error "Error: Unknown model selector '$Selector'. Use -m qwen3.8 (default), -m qwen3.5, -m turbo (MTP Q4_K_M), -m turbo-q6 (MTP Q6_K), or -m turbo-q8 (MTP Q8_0)."
                exit 2
            }
            $script:ModelAlias = [System.IO.Path]::GetFileNameWithoutExtension($script:ModelPath)
            $script:ModelKey = $script:ModelAlias
        }
    }
}

function Invoke-ModelDownload([string]$Label, [string]$Url, [string]$DestPath, [long]$MinBytes, [string]$HfAltFile = "") {
    if (-not (Test-Path $ModelsDir)) {
        New-Item -ItemType Directory -Path $ModelsDir -Force | Out-Null
    }
    if (Test-Path $DestPath) {
        $existingBytes = (Get-Item $DestPath).Length
        if ($existingBytes -ge $MinBytes) {
            $gib = "{0:N2}" -f ($existingBytes / 1GB)
            Write-Host "  -> $Label already installed and verified ($gib GiB)." -ForegroundColor Green
            return
        }
        Write-Host "  -> $Label is incomplete ($existingBytes bytes < $MinBytes bytes); resuming download..." -ForegroundColor Yellow
    } else {
        Write-Host "  -> Downloading $Label from Hugging Face ..." -ForegroundColor Cyan
    }

    $curlCmd = Get-Command curl.exe -ErrorAction SilentlyContinue
    if ($curlCmd) {
        & $curlCmd.Source -fL --retry 5 --retry-delay 3 -C - -o $DestPath $Url
        if ($LASTEXITCODE -ne 0) {
            & $curlCmd.Source -fL --retry 5 --retry-delay 3 -o $DestPath $Url
            if ($LASTEXITCODE -ne 0) {
                throw "Failed to download $Label from $Url (curl exit code $LASTEXITCODE)"
            }
        }
    } else {
        Invoke-WebRequest -Uri $Url -OutFile $DestPath -UseBasicParsing
    }

    if (-not (Test-Path $DestPath)) {
        throw "Model download failed: $DestPath does not exist."
    }
    $finalBytes = (Get-Item $DestPath).Length
    if ($finalBytes -lt $MinBytes) {
        throw "Downloaded file $DestPath is smaller than expected ($finalBytes bytes < $MinBytes bytes). Re-run command to resume."
    }
    if ($HfAltFile) {
        $altDest = Join-Path $ModelsDir $HfAltFile
        if (-not (Test-Path $altDest)) {
            try {
                New-Item -ItemType HardLink -Path $altDest -Target $DestPath -Force -ErrorAction Stop | Out-Null
            } catch {}
        }
    }
    $finalGib = "{0:N2}" -f ($finalBytes / 1GB)
    Write-Host "  -> Verified $Label ($finalGib GiB)." -ForegroundColor Green
}

function Ensure-SelectedModelDownloaded {
    if (Test-Path $script:ModelPath) {
        $existingBytes = (Get-Item $script:ModelPath).Length
        if (($script:ModelMinBytes -eq 0L) -or ($existingBytes -ge $script:ModelMinBytes)) {
            return
        }
    }
    if ($script:ModelDownloadUrl -and ($env:OFFLINE -ne "1")) {
        $leaf = Split-Path -Leaf $script:ModelPath
        Write-Host "Model $($script:ModelAlias) ($leaf) is not yet present in $ModelsDir; auto-downloading now..." -ForegroundColor Cyan
        Invoke-ModelDownload -Label "$($script:ModelAlias) ($leaf)" -Url $script:ModelDownloadUrl -DestPath $script:ModelPath -MinBytes $script:ModelMinBytes -HfAltFile $script:ModelHfAltFile
    }
}

function Invoke-DownloadModelsCommand([string]$Selector = $ModelSelect) {
    $selLower = $Selector.Trim().ToLowerInvariant()
    switch ($selLower) {
        "all" {
            Invoke-ModelDownload -Label "Qwen3.5-9B-Uncensored-Q4_K_M.gguf (5.24 GiB)" -Url $Qwen35Url -DestPath (Join-Path $ModelsDir $Qwen35File) -MinBytes $Qwen35MinBytes -HfAltFile $Qwen35AltFile
            Invoke-ModelDownload -Label "Qwen3.8-27B-Uncensored-Q3_K_M.gguf (12.40 GiB)" -Url $Qwen38Url -DestPath (Join-Path $ModelsDir $Qwen38File) -MinBytes $Qwen38MinBytes
            Invoke-ModelDownload -Label "Qwen3.8-27B-Turbo-MTP-Q4_K_M.gguf (17.23 GiB MTP)" -Url $Qwen38TurboQ4Url -DestPath (Join-Path $ModelsDir $Qwen38TurboQ4File) -MinBytes $Qwen38TurboQ4MinBytes -HfAltFile $Qwen38TurboQ4HfFile
            Invoke-ModelDownload -Label "Qwen3.8-27B-Turbo-MTP-Q6_K.gguf (22.38 GiB MTP)" -Url $Qwen38TurboQ6Url -DestPath (Join-Path $ModelsDir $Qwen38TurboQ6File) -MinBytes $Qwen38TurboQ6MinBytes -HfAltFile $Qwen38TurboQ6HfFile
            Invoke-ModelDownload -Label "Qwen3.8-27B-Turbo-MTP-Q8_0.gguf (28.16 GiB MTP)" -Url $Qwen38TurboQ8Url -DestPath (Join-Path $ModelsDir $Qwen38TurboQ8File) -MinBytes $Qwen38TurboQ8MinBytes -HfAltFile $Qwen38TurboQ8HfFile
        }
        { $_ -in @("all-turbo", "turbo-all", "mtp-all", "all-mtp") } {
            Invoke-ModelDownload -Label "Qwen3.8-27B-Turbo-MTP-Q4_K_M.gguf (17.23 GiB MTP)" -Url $Qwen38TurboQ4Url -DestPath (Join-Path $ModelsDir $Qwen38TurboQ4File) -MinBytes $Qwen38TurboQ4MinBytes -HfAltFile $Qwen38TurboQ4HfFile
            Invoke-ModelDownload -Label "Qwen3.8-27B-Turbo-MTP-Q6_K.gguf (22.38 GiB MTP)" -Url $Qwen38TurboQ6Url -DestPath (Join-Path $ModelsDir $Qwen38TurboQ6File) -MinBytes $Qwen38TurboQ6MinBytes -HfAltFile $Qwen38TurboQ6HfFile
            Invoke-ModelDownload -Label "Qwen3.8-27B-Turbo-MTP-Q8_0.gguf (28.16 GiB MTP)" -Url $Qwen38TurboQ8Url -DestPath (Join-Path $ModelsDir $Qwen38TurboQ8File) -MinBytes $Qwen38TurboQ8MinBytes -HfAltFile $Qwen38TurboQ8HfFile
        }
        default {
            Resolve-Model $Selector
            if (-not $script:ModelDownloadUrl) {
                Write-Error "Error: No remote download URL configured for model selector '$Selector'."
                exit 2
            }
            $leaf = Split-Path -Leaf $script:ModelPath
            Invoke-ModelDownload -Label "$($script:ModelAlias) ($leaf)" -Url $script:ModelDownloadUrl -DestPath $script:ModelPath -MinBytes $script:ModelMinBytes -HfAltFile $script:ModelHfAltFile
        }
    }
}

function Detect-HardwareAndTune {
    Resolve-Model $ModelSelect

    $script:CpuName = "Unknown CPU"
    $script:LogicalCpus = [Environment]::ProcessorCount
    $script:PhysicalCores = [Math]::Max(1, [int]($script:LogicalCpus / 2))
    try {
        $procs = @(Get-CimInstance Win32_Processor -ErrorAction SilentlyContinue)
        if ($procs.Count -gt 0) {
            $script:CpuName = ($procs[0].Name -replace '\s+', ' ').Trim()
            $physSum = ($procs | Measure-Object -Property NumberOfCores -Sum).Sum
            $logSum = ($procs | Measure-Object -Property NumberOfLogicalProcessors -Sum).Sum
            if ($physSum -gt 0) { $script:PhysicalCores = [int]$physSum }
            if ($logSum -gt 0) { $script:LogicalCpus = [int]$logSum }
        }
    } catch {}

    $autoThreads = [Math]::Max(1, [int][Math]::Floor(($script:PhysicalCores * 4 + 4) / 5))
    $autoThreadsBatch = $script:PhysicalCores
    $script:Threads = if ($env:THREADS) { [int]$env:THREADS } else { $autoThreads }
    $script:ThreadsBatch = if ($env:THREADS_BATCH) { [int]$env:THREADS_BATCH } else { $autoThreadsBatch }

    $script:TotalRamMib = 8192
    $script:AvailRamMib = 4096
    try {
        $osInfo = Get-CimInstance Win32_OperatingSystem -ErrorAction SilentlyContinue
        if ($osInfo) {
            $script:TotalRamMib = [int][Math]::Round($osInfo.TotalVisibleMemorySize / 1024)
            $script:AvailRamMib = [int][Math]::Round($osInfo.FreePhysicalMemory / 1024)
        }
    } catch {}

    if (Test-Path $script:ModelPath) {
        $script:ModelSizeMib = [int][Math]::Floor((Get-Item $script:ModelPath).Length / 1048576)
    } else {
        $script:ModelSizeMib = if ($script:ModelExpectedMib) { $script:ModelExpectedMib } else { 5366 }
    }

    $script:GpuDetected = $false
    $script:GpuCount = 0
    $script:GpuName = "None (CPU-only mode)"
    $script:GpuTotalMib = 0
    $script:GpuFreeMib = 0

    $nvidiaSmi = Get-Command nvidia-smi -ErrorAction SilentlyContinue
    if ($nvidiaSmi) {
        $oldEap = $ErrorActionPreference
        $ErrorActionPreference = "Continue"
        try {
            $gpuOut = & $nvidiaSmi.Source --query-gpu=name,memory.total,memory.free --format=csv,noheader,nounits 2>$null
            if ($LASTEXITCODE -eq 0 -and $gpuOut) {
                $lines = @($gpuOut -split "`r?`n" | Where-Object { $_.Trim() -ne "" })
                $script:GpuCount = $lines.Count
                $firstLine = $lines[0].Trim()
                $parts = $firstLine -split ','
                if ($parts.Count -ge 3) {
                    $script:GpuDetected = $true
                    $script:GpuName = $parts[0].Trim()
                    $script:GpuTotalMib = [int][double]$parts[1].Trim()
                    $script:GpuFreeMib = [int][double]$parts[2].Trim()
                }
                if ($env:CUDA_VISIBLE_DEVICES -and ($env:CUDA_VISIBLE_DEVICES -match '^\d+$')) {
                    if ([int]$env:CUDA_VISIBLE_DEVICES -ge $script:GpuCount) {
                        $env:CUDA_VISIBLE_DEVICES = "0"
                    }
                }
            }
        } catch {} finally {
            $ErrorActionPreference = $oldEap
        }
    }

    $gpuHeadroomMib = $script:GpuTotalMib - $script:ModelSizeMib
    if ($script:GpuDetected -and $script:GpuTotalMib -ge 24000 -and $gpuHeadroomMib -ge 10000) {
        $script:KvCacheType = if ($env:KV_CACHE_TYPE) { $env:KV_CACHE_TYPE } else { "f16" }
    } else {
        $script:KvCacheType = if ($env:KV_CACHE_TYPE) { $env:KV_CACHE_TYPE } else { "q8_0" }
    }

    $script:GpuArgs = New-Object System.Collections.Generic.List[string]
    if ($script:GpuDetected -and $script:GpuTotalMib -gt 0) {
        if ($script:ModelSizeMib -le $script:GpuTotalMib) {
            $autoFitTarget = 256
        } elseif ($script:GpuTotalMib -le 8192) {
            $autoFitTarget = 384
        } elseif ($script:GpuTotalMib -le 16384) {
            $autoFitTarget = 512
        } else {
            $autoFitTarget = 768
        }
        $script:FitTarget = if ($env:FIT_TARGET) { $env:FIT_TARGET } else { "$autoFitTarget" }
        if ($script:GpuTotalMib -ge 24000) {
            $script:BatchSize = if ($env:BATCH_SIZE) { $env:BATCH_SIZE } else { "4096" }
            $script:UbatchSize = if ($env:UBATCH_SIZE) { $env:UBATCH_SIZE } else { "2048" }
        } else {
            $script:BatchSize = if ($env:BATCH_SIZE) { $env:BATCH_SIZE } else { "2048" }
            $script:UbatchSize = if ($env:UBATCH_SIZE) { $env:UBATCH_SIZE } else { "512" }
        }
        foreach ($a in @("--fit", "on", "--fit-target", $script:FitTarget, "--flash-attn", "on", "--cache-type-k", $script:KvCacheType, "--cache-type-v", $script:KvCacheType)) {
            $script:GpuArgs.Add($a)
        }
        if ($gpuHeadroomMib -ge 4096) {
            $script:GpuArgs.Add("--n-gpu-layers")
            $script:GpuArgs.Add("999")
        }
    } else {
        $script:FitTarget = "N/A"
        $script:BatchSize = if ($env:BATCH_SIZE) { $env:BATCH_SIZE } else { "1024" }
        $script:UbatchSize = if ($env:UBATCH_SIZE) { $env:UBATCH_SIZE } else { "256" }
        foreach ($a in @("--n-gpu-layers", "0", "--flash-attn", "on", "--cache-type-k", $script:KvCacheType, "--cache-type-v", $script:KvCacheType)) {
            $script:GpuArgs.Add($a)
        }
    }

    $totalPoolMib = $script:TotalRamMib + $script:GpuTotalMib
    $headroomMib = $totalPoolMib - $script:ModelSizeMib
    if ($script:GpuDetected -and $script:ModelSizeMib -le $script:GpuTotalMib) {
        if ($gpuHeadroomMib -ge 24000) {
            $autoCtxSize = 65536
        } elseif ($gpuHeadroomMib -ge 10000) {
            $autoCtxSize = 32768
        } elseif ($gpuHeadroomMib -ge 4000) {
            $autoCtxSize = 16384
        } else {
            $autoCtxSize = 8192
        }
    } elseif ($headroomMib -ge 64000) {
        $autoCtxSize = 32768
    } elseif ($headroomMib -ge 18000) {
        $autoCtxSize = 16384
    } elseif ($headroomMib -ge 10000) {
        $autoCtxSize = 8192
    } else {
        $autoCtxSize = 4096
    }
    $script:CtxSize = if ($env:CTX_SIZE) { $env:CTX_SIZE } else { "$autoCtxSize" }

    $script:FeatureArgs = New-Object System.Collections.Generic.List[string]
    if ($SpecType -ne "none" -and -not [string]::IsNullOrWhiteSpace($SpecType)) {
        $script:FeatureArgs.Add("--spec-type")
        $script:FeatureArgs.Add($SpecType)
    }
    if ($ReasoningMode -ne "auto" -and -not [string]::IsNullOrWhiteSpace($ReasoningMode)) {
        $script:FeatureArgs.Add("--reasoning")
        $script:FeatureArgs.Add($ReasoningMode)
    }

    $script:ServerAgentArgs = New-Object System.Collections.Generic.List[string]
    if ($AgentMode -in @("on", "true", "1")) {
        $script:ServerAgentArgs.Add("--agent")
        $script:ServerAgentArgs.Add("--tools")
        $script:ServerAgentArgs.Add("all")
    }

    $repeatPenalty = if ($env:REPEAT_PENALTY) { $env:REPEAT_PENALTY } else { "1.02" }
    $repeatLastN = if ($env:REPEAT_LAST_N) { $env:REPEAT_LAST_N } else { "64" }
    $script:SamplingGuardArgs = New-Object System.Collections.Generic.List[string]
    $script:SamplingGuardArgs.Add("--repeat-penalty")
    $script:SamplingGuardArgs.Add($repeatPenalty)
    $script:SamplingGuardArgs.Add("--repeat-last-n")
    $script:SamplingGuardArgs.Add($repeatLastN)
    if ($script:TotalRamMib -ge 120000 -or $script:GpuTotalMib -ge 24000 -or $script:LogicalCpus -ge 36) {
        $script:ReasoningHwTier = "ULTRA_SERVER_DATACENTER (15 Core Engines: 1,024-D VSA, 80x H-MDP, 1,200 RL eps, 32x K-Means++)"
    } elseif ($script:TotalRamMib -ge 24000 -and $script:LogicalCpus -ge 16) {
        $script:ReasoningHwTier = "EXTREME_WORKSTATION (15 Core Engines: 1,024-D VSA, 80x H-MDP, 600 RL eps, 20x K-Means++)"
    } elseif ($script:TotalRamMib -ge 12000 -and $script:LogicalCpus -ge 8) {
        $script:ReasoningHwTier = "HIGH_PERFORMANCE (15 Core Engines: 1,024-D VSA, 60x H-MDP, 400 RL eps, 12x K-Means++)"
    } else {
        $script:ReasoningHwTier = "PORTABLE_CONSERVATIVE (15 Core Engines: 1,024-D VSA, 40x H-MDP, 200 RL eps, 8x K-Means++)"
    }
}

function Show-HardwareProfile {
    Detect-HardwareAndTune
    Write-Host "=== Auto-Detected Hardware & Tuning Profile ==="
    Write-Host ("  CPU:            {0} ({1} physical cores, {2} threads)" -f $script:CpuName, $script:PhysicalCores, $script:LogicalCpus)
    Write-Host ("  System RAM:     {0} MiB total ({1} MiB available)" -f $script:TotalRamMib, $script:AvailRamMib)
    if ($script:GpuDetected) {
        Write-Host ("  GPU:            {0} ({1} MiB total, {2} MiB free, {3} GPU(s) visible)" -f $script:GpuName, $script:GpuTotalMib, $script:GpuFreeMib, $script:GpuCount)
    } else {
        Write-Host ("  GPU:            {0}" -f $script:GpuName)
    }
    Write-Host ("  15-Engine Tier: {0}" -f $script:ReasoningHwTier)
    $modelLeaf = Split-Path -Leaf $script:ModelPath
    Write-Host ("  Selected Model: {0} ({1} MiB -> {2})" -f $script:ModelAlias, $script:ModelSizeMib, $modelLeaf)
    Write-Host ("  Reasoning Mode: {0} (default: off for instant answers; pass --think to enable <think>)" -f $ReasoningMode)
    Write-Host ("  Agent Tools:    {0} (read_file, write_file, edit_file, exec_shell_command, grep_search, ...)" -f $AgentMode)
    $tunedLine = "  Tuned Settings: --ctx-size $($script:CtxSize) --reasoning $ReasoningMode --threads $($script:Threads) --threads-batch $($script:ThreadsBatch) --batch-size $($script:BatchSize) --ubatch-size $($script:UbatchSize) --spec-type $SpecType"
    if ($script:GpuDetected) {
        $tunedLine += " --fit on --fit-target $($script:FitTarget) --flash-attn on -ctk $($script:KvCacheType) -ctv $($script:KvCacheType)"
    } else {
        $tunedLine += " --n-gpu-layers 0 --flash-attn on -ctk $($script:KvCacheType) -ctv $($script:KvCacheType)"
    }
    Write-Host $tunedLine
    Write-Host "==============================================="
}

function Test-LlamaRunning {
    if (Test-Path $PidFile) {
        $rawPid = (Get-Content $PidFile -ErrorAction SilentlyContinue | Select-Object -First 1)
        if ($rawPid -and ($rawPid.Trim() -match '^\d+$')) {
            $proc = Get-Process -Id ([int]$rawPid.Trim()) -ErrorAction SilentlyContinue
            if ($proc -and (-not $proc.HasExited)) {
                return $true
            }
        }
    }
    return $false
}

function Format-FileSize([string]$Path) {
    if (-not (Test-Path $Path)) { return "Missing" }
    $bytes = (Get-Item $Path).Length
    if ($bytes -ge 1GB) {
        return ("{0:N1} GiB" -f ($bytes / 1GB))
    }
    return ("{0:N1} MiB" -f ($bytes / 1MB))
}

function Show-Models {
    Resolve-Model $ModelSelect
    $runningModel = "NONE (stopped)"
    if ((Test-LlamaRunning) -and (Test-Path $ActiveModelFile)) {
        $runningModel = (Get-Content $ActiveModelFile -ErrorAction SilentlyContinue | Select-Object -First 1).Trim()
    }
    $q38File = Join-Path $ModelsDir $Qwen38File
    $q35File = Join-Path $ModelsDir $Qwen35File
    $turboQ4File = Join-Path $ModelsDir $Qwen38TurboQ4File
    $turboQ4Alt = Join-Path $ModelsDir $Qwen38TurboQ4HfFile
    $turboQ6File = Join-Path $ModelsDir $Qwen38TurboQ6File
    $turboQ6Alt = Join-Path $ModelsDir $Qwen38TurboQ6HfFile
    $turboQ8File = Join-Path $ModelsDir $Qwen38TurboQ8File
    $turboQ8Alt = Join-Path $ModelsDir $Qwen38TurboQ8HfFile

    Write-Host "=== Installed & Available CORA Models ==="
    Write-Host "  1. [DEFAULT]  qwen3.8 (-m 3.8 | 27b | q3)            -> Qwen3.8-27B-Uncensored-Q3_K_M.gguf (~12.4 GiB)"
    if (Test-Path $q38File) {
        Write-Host ("     Status: Installed ({0})" -f (Format-FileSize $q38File))
    } else {
        Write-Host "     Status: Not downloaded yet (auto-downloads with: .\run_cora_WIN.ps1 download -m 3.8)"
    }
    Write-Host "  2. [FAST]     qwen3.5 (-m 3.5 | 9b | fast)           -> Qwen3.5-9B-Uncensored-Q4_K_M.gguf (~5.2 GiB, HauhauCS-Aggressive)"
    if (Test-Path $q35File) {
        Write-Host ("     Status: Installed ({0})" -f (Format-FileSize $q35File))
    } else {
        Write-Host "     Status: Not downloaded yet (auto-downloads with: .\run_cora_WIN.ps1 download -m 3.5)"
    }
    Write-Host "  3. [MTP-Q4]   turbo (-m turbo | mtp | turbo-q4 | q4) -> Qwen3.8-27B-Turbo-MTP-Q4_K_M.gguf (~17.2 GiB, Multiple Token Prediction)"
    if (Test-Path $turboQ4File) {
        Write-Host ("     Status: Installed ({0})" -f (Format-FileSize $turboQ4File))
    } elseif (Test-Path $turboQ4Alt) {
        Write-Host ("     Status: Installed ({0})" -f (Format-FileSize $turboQ4Alt))
    } else {
        Write-Host "     Status: Available for auto-download (.\run_cora_WIN.ps1 download -m turbo  OR  .\run_cora_WIN.ps1 cli -m turbo)"
    }
    Write-Host "  4. [MTP-Q6]   turbo-q6 (-m turbo-q6 | mtp-q6 | q6)   -> Qwen3.8-27B-Turbo-MTP-Q6_K.gguf (~22.4 GiB, Multiple Token Prediction)"
    if (Test-Path $turboQ6File) {
        Write-Host ("     Status: Installed ({0})" -f (Format-FileSize $turboQ6File))
    } elseif (Test-Path $turboQ6Alt) {
        Write-Host ("     Status: Installed ({0})" -f (Format-FileSize $turboQ6Alt))
    } else {
        Write-Host "     Status: Available for auto-download (.\run_cora_WIN.ps1 download -m turbo-q6  OR  .\run_cora_WIN.ps1 cli -m turbo-q6)"
    }
    Write-Host "  5. [MTP-Q8]   turbo-q8 (-m turbo-q8 | mtp-q8 | q8)   -> Qwen3.8-27B-Turbo-MTP-Q8_0.gguf (~28.2 GiB, Multiple Token Prediction)"
    if (Test-Path $turboQ8File) {
        Write-Host ("     Status: Installed ({0})" -f (Format-FileSize $turboQ8File))
    } elseif (Test-Path $turboQ8Alt) {
        Write-Host ("     Status: Installed ({0})" -f (Format-FileSize $turboQ8Alt))
    } else {
        Write-Host "     Status: Available for auto-download (.\run_cora_WIN.ps1 download -m turbo-q8  OR  .\run_cora_WIN.ps1 cli -m turbo-q8)"
    }
    Write-Host ""
    Write-Host "  Currently Running: $runningModel"
    Write-Host "=============================================="
}

function Get-LlamaServerBinary {
    $winExe = Join-Path $BinDir "llama-server.exe"
    if (Test-Path $winExe) { return $winExe }
    # Check subdirectories inside bin\ in case archive extracted to a subfolder
    $subExe = Get-ChildItem -Path $BinDir -Filter "llama-server.exe" -Recurse -ErrorAction SilentlyContinue | Select-Object -First 1
    if ($subExe) { return $subExe.FullName }
    throw "llama-server.exe not found in $BinDir. Run .\setup_cora_WIN.ps1 first to download the Windows llama.cpp binaries."
}

function Build-LlamaServerArgumentList([bool]$IncludeServerAgent = $true) {
    $argList = New-Object System.Collections.Generic.List[string]
    foreach ($a in @(
        "--model", $script:ModelPath,
        "--alias", $script:ModelAlias,
        "--host", $BindHost,
        "--port", $LlamaPort,
        "--ctx-size", $script:CtxSize,
        "--parallel", "1",
        "--context-shift",
        "--no-reasoning-preserve"
    )) {
        $argList.Add($a)
    }
    foreach ($a in $script:GpuArgs) { $argList.Add($a) }
    foreach ($a in $script:FeatureArgs) { $argList.Add($a) }
    if ($IncludeServerAgent) {
        foreach ($a in $script:ServerAgentArgs) { $argList.Add($a) }
    }
    foreach ($a in $script:SamplingGuardArgs) { $argList.Add($a) }
    foreach ($a in @(
        "--threads", "$($script:Threads)",
        "--threads-batch", "$($script:ThreadsBatch)",
        "--batch-size", "$($script:BatchSize)",
        "--ubatch-size", "$($script:UbatchSize)",
        "--cont-batching",
        "--no-webui"
    )) {
        $argList.Add($a)
    }
    return $argList
}

function Test-WebuiRunning {
    try {
        $resp = Invoke-WebRequest -Uri "http://${BindHost}:${WebuiPort}/api/health" -UseBasicParsing -TimeoutSec 2 -ErrorAction Stop
        if ($resp.StatusCode -eq 200 -and $resp.Content -match '"cora-webui"') {
            return $true
        }
    } catch {}
    if (Test-Path $WebuiPidFile) {
        $rawPid = (Get-Content $WebuiPidFile -ErrorAction SilentlyContinue | Select-Object -First 1)
        if ($rawPid -and ($rawPid.Trim() -match '^\d+$')) {
            $proc = Get-Process -Id ([int]$rawPid.Trim()) -ErrorAction SilentlyContinue
            if ($proc -and (-not $proc.HasExited)) {
                return $true
            }
        }
    }
    return $false
}

function Stop-CoraWebui {
    $stoppedAny = $false
    if (Test-Path $WebuiPidFile) {
        $rawPid = (Get-Content $WebuiPidFile -ErrorAction SilentlyContinue | Select-Object -First 1)
        if ($rawPid -and ($rawPid.Trim() -match '^\d+$')) {
            $wPid = [int]$rawPid.Trim()
            $proc = Get-Process -Id $wPid -ErrorAction SilentlyContinue
            if ($proc -and (-not $proc.HasExited)) {
                Write-Host "Stopping Custom CORA WebUI (PID $wPid)..."
                Stop-Process -Id $wPid -Force -ErrorAction SilentlyContinue
                $stoppedAny = $true
            }
        }
    }
    try {
        $conns = Get-NetTCPConnection -LocalPort ([int]$WebuiPort) -State Listen -ErrorAction SilentlyContinue
        foreach ($c in $conns) {
            if ($c.OwningProcess -gt 0) {
                if (-not $stoppedAny) {
                    Write-Host "Stopping Custom CORA WebUI on port $WebuiPort (PID $($c.OwningProcess))..."
                }
                Stop-Process -Id $c.OwningProcess -Force -ErrorAction SilentlyContinue
                $stoppedAny = $true
            }
        }
    } catch {}
    Remove-Item -Path $WebuiPidFile -Force -ErrorAction SilentlyContinue
}

function Start-CoraWebui([bool]$OpenBrowser = $true) {
    $webuiPy = Join-Path $BaseDir "webui\server.py"
    if (-not (Test-Path $webuiPy)) {
        Write-Host "Custom CORA WebUI server not found at $webuiPy" -ForegroundColor Yellow
        return
    }
    $noBrowser = ($ExtraArgs -contains "--no-browser") -or ($ExtraArgs -contains "-no-browser")
    $url = "http://${BindHost}:${WebuiPort}"

    if (Test-WebuiRunning) {
        $wPid = if (Test-Path $WebuiPidFile) { (Get-Content $WebuiPidFile -ErrorAction SilentlyContinue | Select-Object -First 1).Trim() } else { "active" }
        Write-Host "Custom CORA WebUI is already running (PID $wPid) -> $url" -ForegroundColor Green
        Write-Host -NoNewline "Verifying local LLM (llama-server) readiness..."
        try {
            $llmRes = Invoke-RestMethod -Uri "$url/api/models/start" -Method POST -ContentType "application/json" -Body '{"force_restart":false}' -TimeoutSec 90 -ErrorAction Stop
            if ($llmRes.ok) {
                Write-Host " ONLINE ($($llmRes.models.llama_server.active_model))" -ForegroundColor Green
            } else {
                Write-Host " Loading in background..." -ForegroundColor Yellow
            }
        } catch {
            Write-Host " Loading in background..." -ForegroundColor Yellow
        }
        if ($OpenBrowser -and (-not $noBrowser) -and [Environment]::UserInteractive) {
            try { Start-Process $url | Out-Null } catch {}
        }
        return
    }

    # Ensure no stale process is holding port 1337 before starting the single WebUI instance
    try {
        $staleConns = Get-NetTCPConnection -LocalPort ([int]$WebuiPort) -State Listen -ErrorAction SilentlyContinue
        foreach ($sc in $staleConns) {
            if ($sc.OwningProcess -gt 0) {
                Stop-Process -Id $sc.OwningProcess -Force -ErrorAction SilentlyContinue
            }
        }
    } catch {}

    $pyExe = Resolve-PythonExe
    $activeProj = if ($env:CORA_ACTIVE_PROJECT) { $env:CORA_ACTIVE_PROJECT.Trim() } else { "" }
    if ($activeProj -and ($activeProj.ToLowerInvariant() -notin @("active_session", "default"))) {
        $projFilesDir = Join-Path $ProjectsDir "$activeProj\Files"
        if (-not (Test-Path $projFilesDir)) {
            New-Item -ItemType Directory -Path $projFilesDir -Force | Out-Null
        }
    }
    try {
        & $pyExe -c "import fastapi, uvicorn, psutil, pydantic" 2>$null
        if ($LASTEXITCODE -ne 0) {
            $reqFile = Join-Path $BaseDir "webui\requirements.txt"
            if (Test-Path $reqFile) {
                Write-Host "Installing CORA WebUI Python dependencies ($reqFile)..." -ForegroundColor Cyan
                & $pyExe -m pip install -q -r $reqFile 2>$null
            }
        }
    } catch {}
    Write-Host -NoNewline "Starting Custom CORA WebUI (Svelte + FastAPI + 15-Engine Dashboard + Project Files/) on $url "
    $wProc = Start-Process -FilePath $pyExe `
        -ArgumentList @($webuiPy, "--host", $BindHost, "--port", "$WebuiPort") `
        -WorkingDirectory $BaseDir `
        -WindowStyle Hidden `
        -RedirectStandardError $WebuiLogFile `
        -RedirectStandardOutput (Join-Path $LogDir "webui.stdout.log") `
        -PassThru
    Set-Content -Path $WebuiPidFile -Value $wProc.Id -Encoding ASCII

    $ready = $false
    for ($t = 0; $t -lt 25; $t++) {
        if ($wProc.HasExited) {
            Write-Host ""
            Write-Host "Error: Custom CORA WebUI exited during startup. Log output:" -ForegroundColor Red
            if (Test-Path $WebuiLogFile) {
                Get-Content $WebuiLogFile -Tail 25 | Write-Host
            }
            return
        }
        try {
            $resp = Invoke-WebRequest -Uri "$url/api/health" -UseBasicParsing -TimeoutSec 1 -ErrorAction Stop
            if ($resp.StatusCode -eq 200 -and $resp.Content -match '"ok"') {
                $ready = $true
                break
            }
        } catch {}
        Write-Host -NoNewline "."
        Start-Sleep -Milliseconds 400
    }
    Write-Host ""
    if ($ready) {
        Write-Host "Custom CORA WebUI is LIVE (PID $($wProc.Id)) -> $url" -ForegroundColor Green
        Write-Host -NoNewline "Ensuring local LLM (llama-server) is ONLINE and ready..."
        try {
            $llmRes = Invoke-RestMethod -Uri "$url/api/models/start" -Method POST -ContentType "application/json" -Body '{"force_restart":false}' -TimeoutSec 90 -ErrorAction Stop
            if ($llmRes.ok) {
                Write-Host " ONLINE ($($llmRes.models.llama_server.active_model))" -ForegroundColor Green
            } else {
                Write-Host " Loading in background..." -ForegroundColor Yellow
            }
        } catch {
            Write-Host " Loading in background..." -ForegroundColor Yellow
        }
        if ($OpenBrowser -and (-not $noBrowser) -and [Environment]::UserInteractive) {
            Write-Host "Opening $url in your default browser..." -ForegroundColor Cyan
            try { Start-Process $url | Out-Null } catch {}
        }
    } else {
        Write-Host "Custom CORA WebUI process started (PID $($wProc.Id)) -> $url" -ForegroundColor Yellow
    }
}

function Start-Services {
    Resolve-Model $ModelSelect
    Ensure-SelectedModelDownloaded
    Detect-HardwareAndTune
    if (-not (Test-Path $script:ModelPath)) {
        Write-Error "Error: Model file not found at $($script:ModelPath). Run .\setup_cora_WIN.ps1 or .\run_cora_WIN.ps1 download -m $($script:ModelKey) to download models."
        exit 1
    }
    $actModeFile = Join-Path $BaseDir "Log\active_session_mode.env"
    if ([Environment]::UserInteractive -and (-not $env:CORA_ACTIVE_PROJECT) -and ($env:CORA_NON_INTERACTIVE -ne "1") -and ($ExtraArgs -notcontains "--no-browser")) {
        Remove-Item -Path $actModeFile -Force -ErrorAction SilentlyContinue
        $pyExe = Resolve-PythonExe
        $agentCliPy = Join-Path $BaseDir "agent-cli.py"
        & $pyExe $agentCliPy "--select-project-only"
        if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
        $actProjFile = Join-Path $BaseDir "Reasoning\data\sessions\active_project.txt"
        if (Test-Path $actProjFile) {
            $env:CORA_ACTIVE_PROJECT = (Get-Content $actProjFile -ErrorAction SilentlyContinue | Select-Object -First 1).Trim()
        }
        if (Test-Path $actModeFile) {
            foreach ($line in (Get-Content $actModeFile -ErrorAction SilentlyContinue)) {
                if ($line -match "^(?:export\s+)?([A-Za-z0-9_]+)=(.*)$") {
                    $val = $Matches[2].Trim().Trim('"', "'")
                    Set-Item -Path "Env:\$($Matches[1])" -Value $val
                }
            }
        }
    }
    $includeServerAgent = $true
    if ($env:CORA_PERSONALITY_MODE -eq "ANALYST") {
        $env:LLM_ISOLATION_MODE = "WHITE"
        $env:LLM_POSTURE_OVERRIDE = "WHITE"
        $env:LLM_ALLOWED_IFACES = "lo"
        $BindHost = "127.0.0.1"
        $includeServerAgent = $false
        Write-Host "  [ANALYST MODE ENFORCED] WebGUI / llama-server locked to WHITE isolation (127.0.0.1 loopback only; external network scanning & agent shell tools disabled)."
    }
    Show-HardwareProfile

    $srvExtraArgs = New-Object System.Collections.Generic.List[string]
    $skipNext = 0
    for ($ei = 0; $ei -lt $ExtraArgs.Count; $ei++) {
        if ($skipNext -gt 0) {
            $skipNext--
            continue
        }
        $eArg = [string]$ExtraArgs[$ei]
        if ($eArg -in @("-netiso", "--netiso", "--network-isolation", "-network-isolation")) {
            if (($ei + 1) -lt $ExtraArgs.Count -and ([string]$ExtraArgs[$ei + 1]).ToLowerInvariant() -eq "blue" -and ($ei + 2) -lt $ExtraArgs.Count -and (-not ([string]$ExtraArgs[$ei + 2]).StartsWith("-"))) {
                $skipNext = 2
            } else {
                $skipNext = 1
            }
            continue
        } elseif ($eArg -in @("-P", "--project")) {
            $skipNext = 1
            continue
        } elseif ($eArg -in @("--continue", "-c", "--no-browser", "-no-browser", "--hud", "--no-hud", "--keep-server", "--keep-alive") -or $eArg -match '^(?:-P|--project)[:=]') {
            continue
        } else {
            $srvExtraArgs.Add($eArg)
        }
    }

    if (Test-LlamaRunning) {
        $curPid = (Get-Content $PidFile -ErrorAction SilentlyContinue | Select-Object -First 1).Trim()
        $curMod = if (Test-Path $ActiveModelFile) { (Get-Content $ActiveModelFile -ErrorAction SilentlyContinue | Select-Object -First 1).Trim() } else { "unknown" }
        Write-Host "llama-server is already running (PID $curPid, Model: $curMod). Use '.\run_cora_WIN.ps1 restart -m $($script:ModelKey)' to switch models."
    } else {
        $serverExe = Get-LlamaServerBinary
        $argList = Build-LlamaServerArgumentList -IncludeServerAgent $includeServerAgent
        foreach ($extra in $srvExtraArgs) { $argList.Add($extra) }

        Write-Host "Starting llama-server ($($script:ModelAlias)) on http://${BindHost}:${LlamaPort} ..."
        $env:PATH = "$BinDir;$env:PATH"
        $proc = Start-Process -FilePath $serverExe `
            -ArgumentList $argList `
            -WorkingDirectory $BaseDir `
            -WindowStyle Hidden `
            -RedirectStandardError $LogFile `
            -RedirectStandardOutput $StdoutFile `
            -PassThru
        Set-Content -Path $PidFile -Value $proc.Id -Encoding ASCII
        $modelLeaf = Split-Path -Leaf $script:ModelPath
        Set-Content -Path $ActiveModelFile -Value "$($script:ModelAlias) ($modelLeaf)" -Encoding UTF8
        Write-Host "llama-server started (PID $($proc.Id), Model: $($script:ModelAlias)). Waiting for model load..."
    }
    Start-CoraWebui
}

function Stop-Services {
    $actModeFile = Join-Path $BaseDir "Log\active_session_mode.env"
    Remove-Item -Path $actModeFile -Force -ErrorAction SilentlyContinue
    if (Test-LlamaRunning) {
        $curPid = [int](Get-Content $PidFile -ErrorAction SilentlyContinue | Select-Object -First 1).Trim()
        Write-Host "Stopping llama-server (PID $curPid)..."
        Stop-Process -Id $curPid -Force -ErrorAction SilentlyContinue
        Remove-Item -Path $PidFile, $ActiveModelFile -Force -ErrorAction SilentlyContinue
    } else {
        Write-Host "llama-server is not running."
        Remove-Item -Path $PidFile, $ActiveModelFile -Force -ErrorAction SilentlyContinue
    }
    Stop-CoraWebui
}

function Show-Status {
    Show-HardwareProfile
    Write-Host "`nService Status:"
    if (Test-LlamaRunning) {
        $curPid = (Get-Content $PidFile -ErrorAction SilentlyContinue | Select-Object -First 1).Trim()
        $curMod = if (Test-Path $ActiveModelFile) { (Get-Content $ActiveModelFile -ErrorAction SilentlyContinue | Select-Object -First 1).Trim() } else { $script:ModelAlias }
        Write-Host "  llama-server: RUNNING (PID $curPid)"
        Write-Host "  Active Model: $curMod"
        Write-Host "  Llama API:    http://${BindHost}:${LlamaPort} (OpenAI-compatible API & llama.cpp server)"
    } else {
        Write-Host "  llama-server: STOPPED"
    }
    if (Test-WebuiRunning) {
        $wPid = if (Test-Path $WebuiPidFile) { (Get-Content $WebuiPidFile -ErrorAction SilentlyContinue | Select-Object -First 1).Trim() } else { "active" }
        Write-Host "  CORA WebUI:   RUNNING (PID $wPid) -> http://${BindHost}:$($script:WebuiPort) (Custom Svelte/FastAPI Dashboard)"
    } else {
        Write-Host "  CORA WebUI:   STOPPED (Start with: .\run_cora_WIN.ps1 webgui  or  .\run_cora_WIN.ps1 webui  or  .\run_cora_WIN.ps1 start)"
    }

    $nvidiaSmi = Get-Command nvidia-smi -ErrorAction SilentlyContinue
    if ($nvidiaSmi) {
        Write-Host "`nGPU Memory Usage:"
        $oldEap = $ErrorActionPreference
        $ErrorActionPreference = "Continue"
        try {
            & $nvidiaSmi.Source --query-gpu=name,memory.used,memory.free,memory.total,utilization.gpu --format=csv 2>$null
        } finally {
            $ErrorActionPreference = $oldEap
        }
    }
}

function Start-AgentCli {
    Resolve-Model $ModelSelect
    Ensure-SelectedModelDownloaded
    Detect-HardwareAndTune
    if (-not (Test-Path $script:ModelPath)) {
        Write-Error "Error: Model file not found at $($script:ModelPath). Run .\setup_cora_WIN.ps1 or .\run_cora_WIN.ps1 download -m $($script:ModelKey) to download models."
        exit 1
    }

    $currentActive = if (Test-Path $ActiveModelFile) { (Get-Content $ActiveModelFile -ErrorAction SilentlyContinue | Select-Object -First 1).Trim() } else { "" }
    if ((-not (Test-LlamaRunning)) -or (-not $currentActive.StartsWith($script:ModelAlias))) {
        if (Test-LlamaRunning) {
            Write-Host "Switching running llama-server to $($script:ModelAlias) ..."
            Stop-Services
            Start-Sleep -Seconds 1
        }
        Show-HardwareProfile
        $serverExe = Get-LlamaServerBinary
        $argList = Build-LlamaServerArgumentList -IncludeServerAgent $false
        Write-Host "Starting local llama-server backend ($($script:ModelAlias)) on http://${BindHost}:${LlamaPort} ..."
        $env:PATH = "$BinDir;$env:PATH"
        $proc = Start-Process -FilePath $serverExe `
            -ArgumentList $argList `
            -WorkingDirectory $BaseDir `
            -WindowStyle Hidden `
            -RedirectStandardError $LogFile `
            -RedirectStandardOutput $StdoutFile `
            -PassThru
        Set-Content -Path $PidFile -Value $proc.Id -Encoding ASCII
        $modelLeaf = Split-Path -Leaf $script:ModelPath
        Set-Content -Path $ActiveModelFile -Value "$($script:ModelAlias) ($modelLeaf)" -Encoding UTF8
    } else {
        Show-HardwareProfile
    }

    Write-Host -NoNewline "Waiting for $($script:ModelAlias) backend to become ready "
    $ready = $false
    $healthUrl = "http://${BindHost}:${LlamaPort}/health"
    for ($t = 0; $t -lt 90; $t++) {
        if (-not (Test-LlamaRunning)) {
            Write-Host ""
            Write-Host "Error: llama-server exited during startup. Last log lines:" -ForegroundColor Red
            if (Test-Path $LogFile) {
                Get-Content $LogFile -Tail 20 | Write-Host
            }
            exit 1
        }
        try {
            $resp = Invoke-WebRequest -Uri $healthUrl -UseBasicParsing -TimeoutSec 2 -ErrorAction Stop
            if ($resp.StatusCode -eq 200 -and $resp.Content -match '"ok"') {
                $ready = $true
                break
            }
        } catch {}
        Write-Host -NoNewline "."
        Start-Sleep -Seconds 1
    }
    Write-Host ""
    if (-not $ready) {
        Write-Error "Error: Timed out waiting for llama-server on http://${BindHost}:${LlamaPort}"
        exit 1
    }

    $env:LLAMA_API_URL = "http://${BindHost}:${LlamaPort}/v1/chat/completions"
    $env:MODEL_ALIAS = $script:ModelAlias
    $env:SKIP_PERMISSIONS = $SkipPermissions
    $env:REASONING_MODE = $ReasoningMode

    $keepServer = ($ExtraArgs -contains "--keep-server") -or ($ExtraArgs -contains "--keep-alive")
    $pyExe = Resolve-PythonExe
    $agentCliPy = Join-Path $BaseDir "agent-cli.py"
    $exitCode = 0
    try {
        & $pyExe $agentCliPy @ExtraArgs
        $exitCode = $LASTEXITCODE
    } finally {
        if (-not $keepServer) {
            Stop-Services
        }
    }
    exit $exitCode
}

switch ($Action) {
    "start" { Start-Services }
    "stop" { Stop-Services }
    "restart" { Stop-Services; Start-Sleep -Seconds 1; Start-Services }
    "status" { Show-Status }
    "webui" { Start-CoraWebui }
    "models" { Show-Models }
    "download" {
        $dlTarget = if ($ExtraArgs.Count -gt 0) { $ExtraArgs[0] } else { $ModelSelect }
        Invoke-DownloadModelsCommand $dlTarget
    }
    { $_ -in @("tune", "detect") } { Show-HardwareProfile }
    "cli" { Start-AgentCli }
    { $_ -in @("reason", "reasoning") } {
        $pyExe = Resolve-PythonExe
        $reasonCli = Join-Path $BaseDir "Reasoning\reasoning_cli.py"
        & $pyExe $reasonCli @ExtraArgs
        exit $LASTEXITCODE
    }
    "train" {
        $trainPs1 = Join-Path $TrainingDir "train_llm_WIN.ps1"
        & $trainPs1 @ExtraArgs
        exit $LASTEXITCODE
    }
    "posture" {
        $posturePs1 = Join-Path $BaseDir "Network_Isolation\ConsolePostureDetection_WIN.ps1"
        & $posturePs1 @ExtraArgs
        exit $LASTEXITCODE
    }
    { $_ -in @("troubleshoot", "diag", "diagnostics") } {
        $troubleshootPs1 = Join-Path $CoraRoot "Troubleshooting\troubleshoot_llm_WIN.ps1"
        & $troubleshootPs1 @ExtraArgs
        exit $LASTEXITCODE
    }
    "logs" {
        if (Test-Path $LogFile) {
            Get-Content $LogFile -Tail 50 -Wait
        } else {
            Write-Host "No log file found at $LogFile yet."
        }
    }
    { $_ -in @("-h", "--help", "help") } { Show-Usage }
    default { Show-Usage; exit 2 }
}
