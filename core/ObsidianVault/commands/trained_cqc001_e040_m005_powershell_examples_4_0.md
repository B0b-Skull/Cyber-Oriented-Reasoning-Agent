---
title: "Trained Command Playbook: CQC001 E040 M005 PowerShell Examples 4.0"
category: commands
domain_hub: "[[knowledge/04_windows_powershell_wmi_cim_and_active_directory]]"
os_platform: windows
primary_tactic: Active_Enum
summary: "Verified Windows & Linux command playbook for CQC001 E040 M005 PowerShell Examples 4.0 (Active_Enum): PowerShell 2.0-7+ cmdlets, Get-CimInstance/Get-WmiObject/wmic queries, WinRM/PSRemoting (Invoke-Command, Enter-PSSession), Active Direc"
when_to_apply: "Apply when working with CQC001 E040 M005 PowerShell Examples 4.0 (windows): Apply when automating Windows enumeration with PowerShell or WMI/CIM (`Get-CimInstance`/`wmic`), executing commands remotely via WinRM/WMI, enumerating Active Directory users/groups/computers/trusts/GPOs (`dsquery`/`nltest`/`net`), or auditing Kerberos tickets (`klist`) and SPNs (`setspn`)."
tags: [covert_infil, enumeration, http, https, lateral_movement_routing_pivot, mdp, passive_enum, pdf, powershell, protocol_chaining, trained, windows, wmic, get-ciminstance, winrm, invoke-command, dsquery, nltest, kerberos, klist, setspn, active_directory]
source_file: "CQC001 E040 M005 PowerShell Examples 4.0"
updated: 2026-10-30
---

powershell -NoProfile -Command "Get-CimInstance Win32_ComputerSystem | Select-Object Name,Domain,Manufacturer,Model,UserName,TotalPhysicalMemory"
# Trained Command Playbook: `CQC001_E040_M005_PowerShell_Examples_4.0.pdf`
powershell -NoProfile -Command "Get-CimInstance Win32_ComputerSystem | Select-Object Name,Domain,Manufacturer,Model,UserName,TotalPhysicalMemory"
- **Source Document:** `~/Projects/CORA/Training/CQC001_E040_M005_PowerShell_Examples_4.0.pdf`
- **CEGAR Verified Commands:** `20` (`0` malformed/unsafe snippets filtered)
- **MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`):** `20`
- **Discovered IPs/Subnets:** `None`
- **Discovered Interfaces:** `None`
- **Related Knowledge Note:** [[knowledge/trained_cqc001_e040_m005_powershell_examples_4_0]]
powershell -NoProfile -Command "Get-CimInstance Win32_ComputerSystem | Select-Object Name,Domain,Manufacturer,Model,UserName,TotalPhysicalMemory"
## Distilled MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`)
| Pre-State ($s$) | Tactic ($\tau$) | Technique ($k$) | Tool ($u$) | Post-State ($s'$) | Verified Command ($c$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `new-jobtrigger` | `s_active_services_enumerated` | `$trigger = New-JobTrigger -Daily -At 3am` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `get-childitem` | `s_passive_topology_mapped` | `Get-ChildItem *.ps1 -pv a \| Get-Acl \| foreach {"{0} size is {1}" -f $a.Name, $a.length}` |
| `s_firewall_or_acl_unlocked` | **`Lateral_Movement_Routing_Pivot`** | Remote Host Execution, L2/L3 Route Injection & Subnet Pivot | `test-netconnection` | `s_cross_subnet_pivot_routed` | `Test-NetConnection -ComputerName microsoft.com -InformationLevel Detailed` |
| `s_protocol_chain_established` | **`Covert_Infil`** | Staged Artifact / Encapsulated Ingress Delivery | `get-filehash` | `s_covert_infil_channel_ready` | `Get-FileHash C:\downloads\WindowsOS.iso -Algorithm SHA384` |
| `s_credentials_or_certs_acquired` | **`Protocol_Chaining`** | Multi-Protocol Handshake & Tunnel Relay Chaining | `invoke-command` | `s_protocol_chain_established` | `$m = Invoke-Command -ComputerName RemoteServer -ScriptBlock { Get Module  -` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `register-scheduledjob` | `s_active_services_enumerated` | `Register-ScheduledJob -Name DailyBackup -Trigger $trigger -ScriptBlock {Copy-Item` |
| `s_firewall_or_acl_unlocked` | **`Lateral_Movement_Routing_Pivot`** | Remote Host Execution, L2/L3 Route Injection & Subnet Pivot | `test-netconnection` | `s_cross_subnet_pivot_routed` | `Test-NetConnection -ComputerName microsoft.com -Port 80 -InformationLevel Quiet` |
| `s_protocol_chain_established` | **`Covert_Infil`** | Staged Artifact / Encapsulated Ingress Delivery | `invoke-webrequest` | `s_covert_infil_channel_ready` | `$iwr = Invoke-WebRequest http://blogs.msdn.com/b/powershell` |
| `s_credentials_or_certs_acquired` | **`Protocol_Chaining`** | Multi-Protocol Handshake & Tunnel Relay Chaining | `new-pssession` | `s_protocol_chain_established` | `$s = New-PSSession -ComputerName RemoteServer` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `get-job` | `s_active_services_enumerated` | `Get-Job -Name DailyBackup \| Receive-Job` |
| `s_protocol_chain_established` | **`Covert_Infil`** | Staged Artifact / Encapsulated Ingress Delivery | `invoke-restmethod` | `s_covert_infil_channel_ready` | `$irm = Invoke-RestMethod blogs.msdn.com/b/powershell/rss.aspx` |
| `s_credentials_or_certs_acquired` | **`Protocol_Chaining`** | Multi-Protocol Handshake & Tunnel Relay Chaining | `get-module` | `s_protocol_chain_established` | `$m = Get-Module -PSSession $s -Name DhcpServer -ListAvailable` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `start-job` | `s_active_services_enumerated` | `Start-Job -DefinitionName DailyBackup` |
| `s_credentials_or_certs_acquired` | **`Protocol_Chaining`** | Multi-Protocol Handshake & Tunnel Relay Chaining | `new-cimsession` | `s_protocol_chain_established` | `$c = New-CimSession -ComputerName RemoteServer` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `register-scheduledjob` | `s_active_services_enumerated` | `Register-ScheduledJob -Name Backup -ScriptBlock {Copy-Item c:\ImportantFiles d: Backup$((Get-Date).ToFileTime()) -Recurse -Force -PassThru} -RunNow` |
| `s_credentials_or_certs_acquired` | **`Protocol_Chaining`** | Multi-Protocol Handshake & Tunnel Relay Chaining | `get-module` | `s_protocol_chain_established` | `$m = Get-Module -CimSession $c -Name DhcpServer -ListAvailable` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `invoke-restmethod` | `s_active_services_enumerated` | `$sessions = Invoke-RestMethod https://odata.eventpointdata.com/tena2014/` |
| `s_credentials_or_certs_acquired` | **`Protocol_Chaining`** | Multi-Protocol Handshake & Tunnel Relay Chaining | `invoke-command` | `s_protocol_chain_established` | `Invoke-Command -ComputerName Server 1 { param($localVar) echo $localVar } -ArgumentList $localVar` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `invoke-item` | `s_active_services_enumerated` | `Invoke-Item $env:TEMP\sessions.csv` |
| `s_credentials_or_certs_acquired` | **`Protocol_Chaining`** | Multi-Protocol Handshake & Tunnel Relay Chaining | `invoke-command` | `s_protocol_chain_established` | `Invoke-Command -ComputerName Server1 { echo $using:localVar }` |
powershell -NoProfile -Command "Get-CimInstance Win32_ComputerSystem | Select-Object Name,Domain,Manufacturer,Model,UserName,TotalPhysicalMemory"
## Verified Executable Commands (Grouped by Capability Layer)
powershell -NoProfile -Command "Get-CimInstance Win32_ComputerSystem | Select-Object Name,Domain,Manufacturer,Model,UserName,TotalPhysicalMemory"
### General_System (18 commands)
```bash
$trigger = New-JobTrigger -Daily -At 3am
Register-ScheduledJob -Name DailyBackup -Trigger $trigger -ScriptBlock {Copy-Item
Get-Job -Name DailyBackup | Receive-Job
Start-Job -DefinitionName DailyBackup
Register-ScheduledJob -Name Backup -ScriptBlock {Copy-Item c:\ImportantFiles d: Backup$((Get-Date).ToFileTime()) -Recurse -Force -PassThru} -RunNow
Get-ChildItem *.ps1 -pv a | Get-Acl | foreach {"{0} size is {1}" -f $a.Name, $a.length}
Test-NetConnection -ComputerName microsoft.com -InformationLevel Detailed
Test-NetConnection -ComputerName microsoft.com -Port 80 -InformationLevel Quiet
Get-FileHash C:\downloads\WindowsOS.iso -Algorithm SHA384
$irm = Invoke-RestMethod blogs.msdn.com/b/powershell/rss.aspx
Invoke-Item $env:TEMP\sessions.csv
$m = Invoke-Command -ComputerName RemoteServer -ScriptBlock { Get Module  -
$s = New-PSSession -ComputerName RemoteServer
$m = Get-Module -PSSession $s -Name DhcpServer -ListAvailable
$c = New-CimSession -ComputerName RemoteServer
$m = Get-Module -CimSession $c -Name DhcpServer -ListAvailable
Invoke-Command -ComputerName Server 1 { param($localVar) echo $localVar } -ArgumentList $localVar
Invoke-Command -ComputerName Server1 { echo $using:localVar }
```
powershell -NoProfile -Command "Get-CimInstance Win32_ComputerSystem | Select-Object Name,Domain,Manufacturer,Model,UserName,TotalPhysicalMemory"
### L7_HTTP_Web (2 commands)
```bash
$iwr = Invoke-WebRequest http://blogs.msdn.com/b/powershell
$sessions = Invoke-RestMethod https://odata.eventpointdata.com/tena2014/
```
powershell -NoProfile -Command "Get-CimInstance Win32_ComputerSystem | Select-Object Name,Domain,Manufacturer,Model,UserName,TotalPhysicalMemory"

<!-- CORA-MAXIMIZED-COMMANDS-START -->
## Maximized Windows & Linux Command Examples for `CQC001 E040 M005 PowerShell Examples 4.0`

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
