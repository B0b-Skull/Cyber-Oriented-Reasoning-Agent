---
title: "Trained Knowledge & Topology: PowerShell-Remoting.txt"
tags:
  - credential_access
  - https
  - lateral_movement_routing_pivot
  - mdp
  - passive_enum
  - powershell
  - protocol_chaining
  - text
  - trained
source_file: PowerShell-Remoting.txt
doc_type: text
updated: 2026-10-25 01:00:07
---

# Trained Knowledge & Architecture: `PowerShell-Remoting.txt`

- **Source Path:** `~/Projects/CORA/Training/PowerShell-Remoting.txt` (`text`)
- **Extracted Technical Entities:** `https, powershell`
- **Extracted IPs / Subnets:** `None`
- **Extracted Interfaces:** `None`
- **Linked Command Playbook:** [[commands/trained_powershell-remoting]] (`28` CEGAR-verified commands | `28` MDP transitions)

## Command & Tactic Coverage Summary
- **Total CEGAR-Verified Commands:** `28` (full executable list in [[commands/trained_powershell-remoting]])
- **Tactic Distribution:** `Protocol_Chaining` (15), `Passive_Enum` (6), `Credential_Access` (4), `Lateral_Movement_Routing_Pivot` (3)
- **Top Extracted CLI Tools:** `get-childitem` (4), `get-hotfix` (3), `get-module` (3), `invoke-command` (3), `new-pssession` (3), `get-variable` (2), `enable-psremoting` (1), `enter-pssession` (1), `exit-pssession` (1), `get-credential` (1), `get-process` (1), `get-pssession` (1), `get-service` (1), `get-winevent` (1), `reg` (1), `remove-pssession` (1)

## Extracted Reference Excerpt
Enable-PSRemoting			:Configures PC via PS for remote commands, runs the Set-WSManQuickConfig cmdlet | https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.core/enable-psremoting?view=powershell-5.1
winrm quickconfig -q		:Enables Winrm

$SecurePassword = Read-Host -Prompt "Rubb13" -AsSecureString 
========================================================================================
Get-Hotfix -ComputerName Win10 -credential barney
Get-Hotfix -ComputerName Win10 -credential $c												:Autoloads credentials assigned to variable $c
get-hotfix -computername win10 -credential $c | where {$_.Description -match "Security"}	:List of Hotfixes for Security
========================================================================================
$c = Get-Credential			:Asks for user name and password and stores as the variable $c.

Creates sessions:
	$session7 = New-PSSession -computername win7
	$session10 = New-PSSession -computername Win10 -credential $c
	Get-Variable session7				:Shows session info
========================================================================================
PSSession					:Lists current sessions

List Processes
	Invoke-Command -session $session7 {get-process}
	Invoke-Command -session $session7 -scriptblock {tasklist}
	Invoke-Command -session $session10 -scriptblock {tasklist /svc}

Enter session, retrieve process and services, close session:
	$session10 = new-pssession -computername Win10 -credential $close		:Creates new session
	Get-Variable $session10													:Displays variable
	Enter-PSSession -session $session10
	Get-Process
	Get-Service | Where {$_.Status -like "Running"
	Exit-PSSession

Shutdown remote sessions
	Get-PSsession
	Remove-PSsession win7,win10 or Remove-PSsession -ID SessionID#
	Get-PSsession
========================================================================================	
Get-ChildItem | Select Name, CreationTime
Get-ChildItem | Select Name, CreationTime, CreationTimeUTC
Get-ChildItem | Select Name, CreationTime, CreationTimeUTC, LastWriteTime
Get-ChildItem | Select Name, CreationTime, LastWriteTime, LastAccessTime
========================================================================================
reg query "HKLM\SOFTWARE\Wow6432Node\Policies\Microsoft\Windows\PowerShell\ModuleLogging"   :Searches HKLM for logging enabled.
Get-Module Microsoft.* | Select Name, LogPipelineExecutionDetails							:view the module logging settings of each module within PowerShell
Get-Module Microsoft.* | ForEach {$_.LogPipelineExecutionDetails = $False}					:Turns the logging FALSE yet registry still shows turned on.
Get-Module Microsoft.* | ForEach {$_.LogPipelineExecutionDetails = $True}					:Turns logging to TRUE
Get-WinEvent -FilterHashtable @{LogName='Windows PowerShell';Id ='800'} -MaxEve

