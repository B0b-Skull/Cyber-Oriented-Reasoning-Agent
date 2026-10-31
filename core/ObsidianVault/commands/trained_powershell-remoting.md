---
title: "Trained Command Playbook: PowerShell-Remoting"
category: commands
domain_hub: "[[knowledge/04_windows_powershell_wmi_cim_and_active_directory]]"
os_platform: windows
primary_tactic: Active_Enum
summary: "Verified Windows & Linux command playbook for PowerShell-Remoting (Active_Enum): PowerShell 2.0-7+ cmdlets, Get-CimInstance/Get-WmiObject/wmic queries, WinRM/PSRemoting (Invoke-Command, Enter-PSSession), Active Direc"
when_to_apply: "Apply when working with PowerShell-Remoting (windows): Apply when automating Windows enumeration with PowerShell or WMI/CIM (`Get-CimInstance`/`wmic`), executing commands remotely via WinRM/WMI, enumerating Active Directory users/groups/computers/trusts/GPOs (`dsquery`/`nltest`/`net`), or auditing Kerberos tickets (`klist`) and SPNs (`setspn`)."
tags: [credential_access, https, lateral_movement_routing_pivot, mdp, passive_enum, powershell, protocol_chaining, text, trained, windows, wmic, get-ciminstance, winrm, invoke-command, dsquery, nltest, kerberos, klist, setspn, active_directory, ldap, powerview]
source_file: "PowerShell-Remoting"
updated: 2026-10-30
---

powershell -NoProfile -Command "Get-CimInstance Win32_ComputerSystem | Select-Object Name,Domain,Manufacturer,Model,UserName,TotalPhysicalMemory"
# Trained Command Playbook: `PowerShell-Remoting.txt`
powershell -NoProfile -Command "Get-CimInstance Win32_ComputerSystem | Select-Object Name,Domain,Manufacturer,Model,UserName,TotalPhysicalMemory"
- **Source Document:** `~/Projects/CORA/Training/PowerShell-Remoting.txt`
- **CEGAR Verified Commands:** `28` (`0` malformed/unsafe snippets filtered)
- **MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`):** `28`
- **Discovered IPs/Subnets:** `None`
- **Discovered Interfaces:** `None`
- **Related Knowledge Note:** [[knowledge/trained_powershell-remoting]]
powershell -NoProfile -Command "Get-CimInstance Win32_ComputerSystem | Select-Object Name,Domain,Manufacturer,Model,UserName,TotalPhysicalMemory"
## Distilled MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`)
| Pre-State ($s$) | Tactic ($\tau$) | Technique ($k$) | Tool ($u$) | Post-State ($s'$) | Verified Command ($c$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `enable-psremoting` | `s_credentials_or_certs_acquired` | `Enable-PSRemoting` |
| `s_firewall_or_acl_unlocked` | **`Lateral_Movement_Routing_Pivot`** | Remote Host Execution, L2/L3 Route Injection & Subnet Pivot | `get-hotfix` | `s_cross_subnet_pivot_routed` | `Get-Hotfix -ComputerName Win10 -credential barney` |
| `s_credentials_or_certs_acquired` | **`Protocol_Chaining`** | Multi-Protocol Handshake & Tunnel Relay Chaining | `get-credential` | `s_protocol_chain_established` | `$c = Get-Credential` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `get-childitem` | `s_passive_topology_mapped` | `Get-ChildItem \| Select Name, CreationTime` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `get-module` | `s_credentials_or_certs_acquired` | `Get-Module Microsoft.* \| ForEach {$_.LogPipelineExecutionDetails = $False}` |
| `s_firewall_or_acl_unlocked` | **`Lateral_Movement_Routing_Pivot`** | Remote Host Execution, L2/L3 Route Injection & Subnet Pivot | `get-hotfix` | `s_cross_subnet_pivot_routed` | `Get-Hotfix -ComputerName Win10 -credential $c` |
| `s_credentials_or_certs_acquired` | **`Protocol_Chaining`** | Multi-Protocol Handshake & Tunnel Relay Chaining | `new-pssession` | `s_protocol_chain_established` | `$session7 = New-PSSession -computername win7` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `get-childitem` | `s_passive_topology_mapped` | `Get-ChildItem \| Select Name, CreationTime, CreationTimeUTC` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `get-module` | `s_credentials_or_certs_acquired` | `Get-Module Microsoft.* \| ForEach {$_.LogPipelineExecutionDetails = $True}` |
| `s_firewall_or_acl_unlocked` | **`Lateral_Movement_Routing_Pivot`** | Remote Host Execution, L2/L3 Route Injection & Subnet Pivot | `get-hotfix` | `s_cross_subnet_pivot_routed` | `get-hotfix -computername win10 -credential $c \| where {$_.Description -match "Security"}` |
| `s_credentials_or_certs_acquired` | **`Protocol_Chaining`** | Multi-Protocol Handshake & Tunnel Relay Chaining | `new-pssession` | `s_protocol_chain_established` | `$session10 = New-PSSession -computername Win10 -credential $c` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `get-childitem` | `s_passive_topology_mapped` | `Get-ChildItem \| Select Name, CreationTime, CreationTimeUTC, LastWriteTime` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `get-winevent` | `s_credentials_or_certs_acquired` | `Get-WinEvent -FilterHashtable @{LogName='Windows PowerShell';Id ='800'} -MaxEvents 1 \| Select -Expand Message` |
| `s_credentials_or_certs_acquired` | **`Protocol_Chaining`** | Multi-Protocol Handshake & Tunnel Relay Chaining | `get-variable` | `s_protocol_chain_established` | `Get-Variable session7` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `get-childitem` | `s_passive_topology_mapped` | `Get-ChildItem \| Select Name, CreationTime, LastWriteTime, LastAccessTime` |
| `s_credentials_or_certs_acquired` | **`Protocol_Chaining`** | Multi-Protocol Handshake & Tunnel Relay Chaining | `invoke-command` | `s_protocol_chain_established` | `Invoke-Command -session $session7 {get-process}` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `reg` | `s_passive_topology_mapped` | `reg query "HKLM\SOFTWARE\Wow6432Node\Policies\Microsoft\Windows\PowerShell\ModuleLogging"` |
| `s_credentials_or_certs_acquired` | **`Protocol_Chaining`** | Multi-Protocol Handshake & Tunnel Relay Chaining | `invoke-command` | `s_protocol_chain_established` | `Invoke-Command -session $session7 -scriptblock {tasklist}` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `get-module` | `s_passive_topology_mapped` | `Get-Module Microsoft.* \| Select Name, LogPipelineExecutionDetails` |
| `s_credentials_or_certs_acquired` | **`Protocol_Chaining`** | Multi-Protocol Handshake & Tunnel Relay Chaining | `invoke-command` | `s_protocol_chain_established` | `Invoke-Command -session $session10 -scriptblock {tasklist /svc}` |
| `s_credentials_or_certs_acquired` | **`Protocol_Chaining`** | Multi-Protocol Handshake & Tunnel Relay Chaining | `new-pssession` | `s_protocol_chain_established` | `$session10 = new-pssession -computername Win10 -credential $close` |
| `s_credentials_or_certs_acquired` | **`Protocol_Chaining`** | Multi-Protocol Handshake & Tunnel Relay Chaining | `get-variable` | `s_protocol_chain_established` | `Get-Variable $session10` |
| `s_credentials_or_certs_acquired` | **`Protocol_Chaining`** | Multi-Protocol Handshake & Tunnel Relay Chaining | `enter-pssession` | `s_protocol_chain_established` | `Enter-PSSession -session $session10` |
| `s_credentials_or_certs_acquired` | **`Protocol_Chaining`** | Multi-Protocol Handshake & Tunnel Relay Chaining | `get-process` | `s_protocol_chain_established` | `Get-Process` |
| `s_credentials_or_certs_acquired` | **`Protocol_Chaining`** | Multi-Protocol Handshake & Tunnel Relay Chaining | `get-service` | `s_protocol_chain_established` | `Get-Service \| Where {$_.Status -like "Running"` |
| `s_credentials_or_certs_acquired` | **`Protocol_Chaining`** | Multi-Protocol Handshake & Tunnel Relay Chaining | `exit-pssession` | `s_protocol_chain_established` | `Exit-PSSession` |
| `s_credentials_or_certs_acquired` | **`Protocol_Chaining`** | Multi-Protocol Handshake & Tunnel Relay Chaining | `get-pssession` | `s_protocol_chain_established` | `Get-PSsession` |
| `s_credentials_or_certs_acquired` | **`Protocol_Chaining`** | Multi-Protocol Handshake & Tunnel Relay Chaining | `remove-pssession` | `s_protocol_chain_established` | `Remove-PSsession win7,win10 or Remove-PSsession -ID SessionID#` |
powershell -NoProfile -Command "Get-CimInstance Win32_ComputerSystem | Select-Object Name,Domain,Manufacturer,Model,UserName,TotalPhysicalMemory"
## Verified Executable Commands (Grouped by Capability Layer)
powershell -NoProfile -Command "Get-CimInstance Win32_ComputerSystem | Select-Object Name,Domain,Manufacturer,Model,UserName,TotalPhysicalMemory"
### General_System (28 commands)
```bash
Enable-PSRemoting
Get-Hotfix -ComputerName Win10 -credential barney
Get-Hotfix -ComputerName Win10 -credential $c
get-hotfix -computername win10 -credential $c | where {$_.Description -match "Security"}
$c = Get-Credential
$session7 = New-PSSession -computername win7
$session10 = New-PSSession -computername Win10 -credential $c
Get-Variable session7
Invoke-Command -session $session7 {get-process}
Invoke-Command -session $session7 -scriptblock {tasklist}
Invoke-Command -session $session10 -scriptblock {tasklist /svc}
$session10 = new-pssession -computername Win10 -credential $close
Get-Variable $session10
Enter-PSSession -session $session10
Get-Process
Get-Service | Where {$_.Status -like "Running"
Exit-PSSession
Get-PSsession
Remove-PSsession win7,win10 or Remove-PSsession -ID SessionID#
Get-ChildItem | Select Name, CreationTime
Get-ChildItem | Select Name, CreationTime, CreationTimeUTC
Get-ChildItem | Select Name, CreationTime, CreationTimeUTC, LastWriteTime
Get-ChildItem | Select Name, CreationTime, LastWriteTime, LastAccessTime
reg query "HKLM\SOFTWARE\Wow6432Node\Policies\Microsoft\Windows\PowerShell\ModuleLogging"
Get-Module Microsoft.* | Select Name, LogPipelineExecutionDetails
Get-Module Microsoft.* | ForEach {$_.LogPipelineExecutionDetails = $False}
Get-Module Microsoft.* | ForEach {$_.LogPipelineExecutionDetails = $True}
Get-WinEvent -FilterHashtable @{LogName='Windows PowerShell';Id ='800'} -MaxEvents 1 | Select -Expand Message
```
powershell -NoProfile -Command "Get-CimInstance Win32_ComputerSystem | Select-Object Name,Domain,Manufacturer,Model,UserName,TotalPhysicalMemory"

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
