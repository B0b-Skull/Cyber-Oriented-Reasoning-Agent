---
title: "Trained Knowledge & Topology: CQC001 E040 M005 S070 I020 ModExam X020 C010 LogScript"
category: knowledge
domain_hub: "[[knowledge/04_windows_powershell_wmi_cim_and_active_directory]]"
os_platform: windows
primary_tactic: Active_Enum
summary: "Operational architecture, decision workflows & Windows/Linux command reference for CQC001 E040 M005 S070 I020 ModExam X020 C010 LogScript: PowerShell 2.0-7+ cmdlets, Get-CimInstance/Get-WmiObject/wmic queries, WinRM/PSRemoting (Invoke-Command, Enter-PSSession), Active "
when_to_apply: "Apply when working with CQC001 E040 M005 S070 I020 ModExam X020 C010 LogScript (windows): Apply when automating Windows enumeration with PowerShell or WMI/CIM (`Get-CimInstance`/`wmic`), executing commands remotely via WinRM/WMI, enumerating Active Directory users/groups/computers/trusts/GPOs (`dsquery`/`nltest`/`net`), or auditing Kerberos tickets (`klist`) and SPNs (`setspn`)."
tags: [http, lateral_movement_routing_pivot, mdp, text, trained, windows, powershell, wmic, get-ciminstance, winrm, invoke-command, dsquery, nltest, kerberos, klist, setspn, active_directory, ldap, powerview, powerup, powersploit, empire]
source_file: "CQC001 E040 M005 S070 I020 ModExam X020 C010 LogScript"
updated: 2026-10-30
---

# Trained Knowledge & Architecture: `CQC001_E040_M005_S070_I020_ModExam_X020_C010_LogScript.txt`

- **Source Path:** `~/Projects/CORA/Training/CQC001_E040_M005_S070_I020_ModExam_X020_C010_LogScript.txt` (`text`)
- **Extracted Technical Entities:** `http`
- **Extracted IPs / Subnets:** `None`
- **Extracted Interfaces:** `None`
- **Linked Command Playbook:** [[commands/trained_cqc001_e040_m005_s070_i020_modexam_x020_c010_logscript]] (`1` CEGAR-verified commands | `1` MDP transitions)

## Command & Tactic Coverage Summary
- **Total CEGAR-Verified Commands:** `1` (full executable list in [[commands/trained_cqc001_e040_m005_s070_i020_modexam_x020_c010_logscript]])
- **Tactic Distribution:** `Lateral_Movement_Routing_Pivot` (1)
- **Top Extracted CLI Tools:** `get-wmiobject` (1)

## Document Structure & Key Topics
- Script: Query-EventLog.ps1
- Date: 30.May.2007
- Version: 1.0
- Author: Jason Fossen, Perimeter Consulting LLC (http://www.sans.org/sec505)
- Purpose: Demo how to search remote event logs with *server-side* WMI queries.
- Legal: Script provided "AS IS" without warranties or guarantees of any
- kind.  USE AT YOUR OWN RISK.  Public domain, no rights reserved.
- $query = "SELECT * FROM Win32_NTLogEvent WHERE logfile = 'Security' AND EventCode = '528' OR EventCode = '4624'"     # Successful logons.
- $query = "SELECT * FROM Win32_NTLogEvent WHERE logfile = 'Security' AND EventCode = '644'"       # Account lockout.
- $query = "SELECT * FROM Win32_NTLogEvent WHERE logfile = 'Security' AND EventCode = '624'"       # User account created.
- $query = "SELECT * FROM Win32_NTLogEvent WHERE logfile = 'Security' AND EventCode = '627'"       # Password change attempted.
- $query = "SELECT * FROM Win32_NTLogEvent WHERE logfile = 'Security' AND EventCode = '628'"       # Password change successful.
- $query = "SELECT * FROM Win32_NTLogEvent WHERE logfile = 'Security' AND EventCode = '629'"       # User account disabled.
- $query = "SELECT * FROM Win32_NTLogEvent WHERE logfile = 'Security' AND EventCode = '517'"       # Security log cleared.
- $query = "SELECT * FROM Win32_NTLogEvent WHERE logfile = 'Security' AND Type = 'audit failure'"  # Security log failed events.
- $query = "SELECT * FROM Win32_NTLogEvent WHERE logfile = 'System' AND Type = 'Error'"            # System log errors.
- $query = "SELECT * FROM Win32_NTLogEvent WHERE logfile = 'System' AND EventCode = '6008'"        # System log unexpected shutdowns.

## Extracted Reference Excerpt
##############################################################################
#  Script: Query-EventLog.ps1
#    Date: 30.May.2007
# Version: 1.0
#  Author: Jason Fossen, Perimeter Consulting LLC (http://www.sans.org/sec505)
# Purpose: Demo how to search remote event logs with *server-side* WMI queries.
#   Legal: Script provided "AS IS" without warranties or guarantees of any
#          kind.  USE AT YOUR OWN RISK.  Public domain, no rights reserved.
##############################################################################


$computer = "."     # A period indicates the local machine, the default.

$query = "SELECT * FROM Win32_NTLogEvent WHERE logfile = 'Security' AND EventCode = '529' OR EventCode = '4625'"       # Bad username/password.
# $query = "SELECT * FROM Win32_NTLogEvent WHERE logfile = 'Security' AND EventCode = '528' OR EventCode = '4624'"     # Successful logons.
# $query = "SELECT * FROM Win32_NTLogEvent WHERE logfile = 'Security' AND EventCode = '644'"       # Account lockout.
# $query = "SELECT * FROM Win32_NTLogEvent WHERE logfile = 'Security' AND EventCode = '624'"       # User account created.
# $query = "SELECT * FROM Win32_NTLogEvent WHERE logfile = 'Security' AND EventCode = '627'"       # Password change attempted.
# $query = "SELECT * FROM Win32_NTLogEvent WHERE logfile = 'Security' AND EventCode = '628'"       # Password change successful.
# $query = "SELECT * FROM Win32_NTLogEvent WHERE logfile = 'Security' AND EventCode = '629'"       # User account disabled.
# $query = "SELECT * FROM Win32_NTLogEvent WHERE logfile = 'Security' AND EventCode = '517'"       # Security log cleared.
# $query = "SELECT * FROM Win32_NTLogEvent WHERE logfile = 'Security' AND Type = 'audit failure'"  # Security log failed events.
# $query = "SELECT * FROM Win32_NTLogEvent WHERE logfile = 'System' AND Type = 'Error'"            # System log errors.
# $query = "SELECT * FROM Win32_NTLogEvent WHERE logfile = 'System' AND EventCode = '6008'"        # System log unexpected shutdowns.

get-wmiobject -query $query -computername $computer |
select-object RecordNumber,TimeGenerated,ComputerName,LogFile,User,SourceName,EventCode,Type,Message

<!-- CORA-MAXIMIZED-COMMANDS-START -->
## Maximized Windows & Linux Command Examples for `CQC001 E040 M005 S070 I020 ModExam X020 C010 LogScript`

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
