<#
.SYNOPSIS
    C.O.R.A. Windows CLI Automated Test Runner (`Troubleshooting/test_cli_WIN.ps1`)
.DESCRIPTION
    Executes `Troubleshooting/test_cli_WIN.py` to systematically validate every startup
    switch, PowerShell launcher subcommand, interactive project/mode menu, keyboard
    shortcut (`Ctrl+O` / `/ctrl-o`), session personality mode (`Default`, `Analyst`,
    `Berserker`, `Ninja`), network isolation posture (`Red`, `White`, `Blue`), project
    `Files/` operation, and slash command in the Windows CLI (`core/agent-cli.py` + `run_cora_WIN.ps1`).
#>
$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$CoraRoot  = Split-Path -Parent $ScriptDir

Push-Location $CoraRoot
try {
    python "$ScriptDir\test_cli_WIN.py" @args
    exit $LASTEXITCODE
} finally {
    Pop-Location
}
