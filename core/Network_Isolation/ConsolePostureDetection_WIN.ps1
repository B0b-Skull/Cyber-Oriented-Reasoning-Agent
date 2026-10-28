<#
.SYNOPSIS
    ConsolePostureDetection_WIN.ps1 — Windows PowerShell Console Posture Detection & Theme Controller

.DESCRIPTION
    Automatically detects the active network isolation posture on Windows (or WSL) and tints
    the current PowerShell / Windows Terminal window in-place (without spawning a new window):
      1. RED / UNRESTRICTED (`.\run_cora_WIN.ps1 cli -netiso red` or default)
         - Background: Deep Tactical Crimson (#1C0A0D / DarkRed) | Font: #FFE8E8 (White)
         - Badge:      NET:RED(FULL-ACCESS)
      2. WHITE / AIR_GAPPED_NETNS (`.\run_cora_WIN.ps1 cli -netiso white`)
         - Background: Deep Tactical Slate (#141820 / Black) | Font: #FFFFFF (White)
         - Badge:      NET:WHITE-NETNS(lo-only)
      3. BLUE / ISOLATED_LAN_USB (`.\run_cora_WIN.ps1 cli -netiso blue [ifaces]`)
         - Background: Deep Cyber Navy Blue (#081426 / DarkBlue) | Font: #E0F4FF (Cyan)
         - Badge:      NET:BLUE(<allowed_ifaces>)

.EXAMPLE
    .\core\Network_Isolation\ConsolePostureDetection_WIN.ps1
    .\core\Network_Isolation\ConsolePostureDetection_WIN.ps1 -Apply blue
    .\core\Network_Isolation\ConsolePostureDetection_WIN.ps1 -Apply white
    .\core\Network_Isolation\ConsolePostureDetection_WIN.ps1 -Apply red
    .\core\Network_Isolation\ConsolePostureDetection_WIN.ps1 -Demo
    .\core\Network_Isolation\ConsolePostureDetection_WIN.ps1 -Reset
#>
[CmdletBinding()]
param(
    [string]$Apply = "",
    [switch]$Detect,
    [switch]$Reset,
    [switch]$Demo,
    [switch]$Json,
    [switch]$Quiet
)

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
if ((Split-Path -Leaf $ScriptDir) -eq "Network_Isolation") {
    $BaseDir = Split-Path -Parent $ScriptDir
} else {
    $BaseDir = $ScriptDir
}

$LogDir = Join-Path $BaseDir "Log"
if (-not (Test-Path $LogDir)) {
    New-Item -ItemType Directory -Path $LogDir -Force | Out-Null
}

$VenvPython = Join-Path $BaseDir "Reasoning\.venv\Scripts\python.exe"
$PythonBin = if (Test-Path $VenvPython) { $VenvPython } elseif (Get-Command python -ErrorAction SilentlyContinue) { "python" } else { "python3" }
$PosturePy = Join-Path $BaseDir "Network_Isolation\console_posture.py"

if ($Reset) {
    & $PythonBin $PosturePy --reset --force-osc
    try {
        $Host.UI.RawUI.BackgroundColor = "Black"
        $Host.UI.RawUI.ForegroundColor = "Gray"
    } catch {}
    exit 0
}

$PyArgs = @("--force-osc")
if ($Demo) { $PyArgs += "--demo" }
elseif ($Json) { $PyArgs += "--json" }
elseif ($Apply -ne "") { $PyArgs += @("--apply", $Apply) }
else { $PyArgs += "--detect" }
if ($Quiet) { $PyArgs += "--quiet" }

# Also set legacy Windows Console RawUI fallback colors alongside Windows Terminal OSC 11/10 hex colors
try {
    $InfoJson = & $PythonBin $PosturePy --json $(if ($Apply -ne "") { @("--apply", $Apply) } else { @() }) | ConvertFrom-Json
    if ($InfoJson.ps_bg -and $InfoJson.ps_fg) {
        $Host.UI.RawUI.BackgroundColor = $InfoJson.ps_bg
        $Host.UI.RawUI.ForegroundColor = $InfoJson.ps_fg
        $Host.UI.RawUI.WindowTitle = $InfoJson.window_title
    }
} catch {}

& $PythonBin $PosturePy @PyArgs
