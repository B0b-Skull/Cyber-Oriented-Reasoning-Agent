<#
.SYNOPSIS
    C.O.R.A. Windows WebGUI Automated Test Runner (`Troubleshooting/test_webgui_WIN.ps1`)
.DESCRIPTION
    Executes `Troubleshooting/test_webgui_WIN.py` to systematically validate every button,
    modal, dropdown, toggle, keyboard shortcut (`Ctrl+O`), project/file action, and API
    endpoint in the Windows WebGUI (`core/webui/server.py` + `App.svelte`).
#>
$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$CoraRoot  = Split-Path -Parent $ScriptDir

Push-Location $CoraRoot
try {
    python "$ScriptDir\test_webgui_WIN.py" @args
    exit $LASTEXITCODE
} finally {
    Pop-Location
}
