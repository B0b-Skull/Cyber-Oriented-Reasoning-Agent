---
title: "Trained Knowledge & Topology: PowerShell-Remoting"
category: knowledge
domain_hub: "[[knowledge/04_windows_powershell_wmi_cim_and_active_directory]]"
os_platform: windows
primary_tactic: Active_Enum
summary: "Operational architecture, decision workflows & Windows/Linux command reference for PowerShell-Remoting: PowerShell 2.0-7+ cmdlets, Get-CimInstance/Get-WmiObject/wmic queries, WinRM/PSRemoting (Invoke-Command, Enter-PSSession), Active "
when_to_apply: "Apply when working with PowerShell-Remoting (windows): Apply when automating Windows enumeration with PowerShell or WMI/CIM (`Get-CimInstance`/`wmic`), executing commands remotely via WinRM/WMI, enumerating Active Directory users/groups/computers/trusts/GPOs (`dsquery`/`nltest`/`net`), or auditing Kerberos tickets (`klist`) and SPNs (`setspn`)."
tags: [credential_access, https, lateral_movement_routing_pivot, mdp, passive_enum, powershell, protocol_chaining, text, trained, windows, wmic, get-ciminstance, winrm, invoke-command, dsquery, nltest, kerberos, klist, setspn, active_directory, ldap, powerview]
source_file: "PowerShell-Remoting"
updated: 2026-10-30
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

<!-- CORA-MAXIMIZED-COMMANDS-START -->
## Maximized Windows & Linux Command Examples for `PowerShell-Remoting`

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
