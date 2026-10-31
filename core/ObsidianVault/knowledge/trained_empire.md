---
title: "Trained Knowledge & Topology: Empire"
category: knowledge
domain_hub: "[[knowledge/04_windows_powershell_wmi_cim_and_active_directory]]"
os_platform: windows
primary_tactic: Active_Enum
summary: "Operational architecture, decision workflows & Windows/Linux command reference for Empire: PowerShell 2.0-7+ cmdlets, Get-CimInstance/Get-WmiObject/wmic queries, WinRM/PSRemoting (Invoke-Command, Enter-PSSession), Active "
when_to_apply: "Apply when working with Empire (windows): Apply when automating Windows enumeration with PowerShell or WMI/CIM (`Get-CimInstance`/`wmic`), executing commands remotely via WinRM/WMI, enumerating Active Directory users/groups/computers/trusts/GPOs (`dsquery`/`nltest`/`net`), or auditing Kerberos tickets (`klist`) and SPNs (`setspn`)."
tags: [credential_access, enumeration, http, https, initial_access_exploitation, ipconfig, kerberos, mdp, mimikatz, out-of-band_access, pdf, powershell, trained, windows, wmic, get-ciminstance, winrm, invoke-command, dsquery, nltest, klist, setspn]
source_file: "Empire"
updated: 2026-10-30
---

# Trained Knowledge & Architecture: `Empire.pdf`

- **Source Path:** `~/Projects/CORA/Training/Empire.pdf` (`pdf`)
- **Extracted Technical Entities:** `http, https, ipconfig, kerberos, mimikatz, powershell`
- **Extracted IPs / Subnets:** `None`
- **Extracted Interfaces:** `None`
- **Linked Command Playbook:** [[commands/trained_empire]] (`9` CEGAR-verified commands | `9` MDP transitions)

## Command & Tactic Coverage Summary
- **Total CEGAR-Verified Commands:** `9` (full executable list in [[commands/trained_empire]])
- **Tactic Distribution:** `Enumeration` (4), `Credential_Access` (2), `Initial_Access_Exploitation` (2), `Out-of-Band_Access` (1)
- **Top Extracted CLI Tools:** `empire.db` (2), `kill` (2), `agent.log` (1), `file.txt` (1), `mimikatz` (1), `sekurlsa::logonpasswords` (1), `unset` (1)

## Extracted Reference Excerpt
--- [Page 1] ---
Version 1.0. Created by Will Schroeder (@harmj0y) and Matt Nelson (@enigma0x3) and released under the Creative Commons v3 "Attribution" License. 
           Empire Cheat Sheet 
 
Getting Started 
Get Empire: # git clone 
https://github.com/PowerShellEmpire/Empire or 
download the latest release from 
https://github.com/PowerShellEmpire/Empire/releases  
Run setup: # ./setup/install.sh 
Reset your installation: # ./setup/reset.sh 
Start Empire [in debug mode]: # ./empire [--debug] 
Documentation at: http://www.PowerShellEmpire.com  
Return back to the main Empire menu at any point with 
main, exit with exit (or Ctrl+C). Go back to the previous 
menu with back. Type help at any point for a list of 
commands and their descriptions. 
You can list all agents or listeners from any menu with 
list [agents/listeners] 
To manually edit the backend db: # sqlitebrowser 
./data/empire.db 
Empire has a heavy UI focus with lots of tab-completion. 
Logging and Downloads 
If –debug specified, info in ./empire.debug 
Each agent that checks in has a complete log of 
tasking/results located in: 
./downloads/AGENTNAME/agent.log 
Downloads/other module output for each agent are also 
stored in ./downloads/ AGENTNAME /* 
(Empire: listeners) > 
Change to the listeners menu from any menu location in 
Empire with listeners. This will show the currently active 
listeners (list also shows this). Listeners are preserved in 
./data./empire.db and start back up on Empire startup. 
See the current listener config options: info/options 
Set an option: set OPTION VALUE 
Unset an option: unset OPTION 
Use a particular stager for a given listener: usestager 
[tab] STAGERNAME LISTENER 
To generate a launcher one-liner: launcher LISTENER 
Start a listener with the currently set options: execute 
Kill one (or all) listeners: kill [tab] NAME/all 
KillDate 
Date for the listener to exit 
(MM/dd/yyyy) 
Name 
Name alias to give the 
listener 
DefaultLostLimit 
Number of missed checkins 
before exiting 
Type 
native, pivot, hop, foreign, 
meter 
DefaultDelay 
Agent delay/reach back 
interval (in seconds) 
WorkingHours 
Hours for the agent to 
operate (09:00-17:00) 
Host 
http[s]://HOSTNAME:PORT 
for staging (also takes IP) 
CertPath 
Path to .pem cert to HTTPS 
DefaultJitter 
Jitter in agent reachback 
interval (0.0-1.0). 
(Empire: stager/stager_name) > 
Empire has a modular approach to generating stagers 
(the way you’re going to get code execution on a remote 
machine). You can access these from main or listeners 
with usemodule [tab] STAGER [LISTENER_NAME] 
info/options will display the current option sets, and 
set/unset works similarly to the listener menu. generate 
will generate the current stager/options. 
launcher 
Command one-liner 
launcher_bat 
Self-deleting  .bat

<!-- CORA-MAXIMIZED-COMMANDS-START -->
## Maximized Windows & Linux Command Examples for `Empire`

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
