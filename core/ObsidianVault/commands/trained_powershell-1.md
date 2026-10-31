---
title: "Trained Command Playbook: PowerShell-1"
category: commands
domain_hub: "[[knowledge/04_windows_powershell_wmi_cim_and_active_directory]]"
os_platform: windows
primary_tactic: Active_Enum
summary: "Verified Windows & Linux command playbook for PowerShell-1 (Active_Enum): PowerShell 2.0-7+ cmdlets, Get-CimInstance/Get-WmiObject/wmic queries, WinRM/PSRemoting (Invoke-Command, Enter-PSSession), Active Direc"
when_to_apply: "Apply when working with PowerShell-1 (windows): Apply when automating Windows enumeration with PowerShell or WMI/CIM (`Get-CimInstance`/`wmic`), executing commands remotely via WinRM/WMI, enumerating Active Directory users/groups/computers/trusts/GPOs (`dsquery`/`nltest`/`net`), or auditing Kerberos tickets (`klist`) and SPNs (`setspn`)."
tags: [credential_access, defense_evasion_firewall, enumeration, lateral_movement_routing_pivot, mdp, netsh, passive_enum, powershell, reconnaissance, text, trained, windows, wmic, get-ciminstance, winrm, invoke-command, dsquery, nltest, kerberos, klist, setspn, active_directory]
source_file: "PowerShell-1"
updated: 2026-10-30
---

powershell -NoProfile -Command "Get-CimInstance Win32_ComputerSystem | Select-Object Name,Domain,Manufacturer,Model,UserName,TotalPhysicalMemory"
# Trained Command Playbook: `PowerShell-1.txt`
powershell -NoProfile -Command "Get-CimInstance Win32_ComputerSystem | Select-Object Name,Domain,Manufacturer,Model,UserName,TotalPhysicalMemory"
- **Source Document:** `~/Projects/CORA/Training/PowerShell-1.txt`
- **CEGAR Verified Commands:** `48` (`0` malformed/unsafe snippets filtered)
- **MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`):** `48`
- **Discovered IPs/Subnets:** `127.0.0.1, 172.17.10.71`
- **Discovered Interfaces:** `None`
- **Related Knowledge Note:** [[knowledge/trained_powershell-1]]
powershell -NoProfile -Command "Get-CimInstance Win32_ComputerSystem | Select-Object Name,Domain,Manufacturer,Model,UserName,TotalPhysicalMemory"
## Distilled MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`)
| Pre-State ($s$) | Tactic ($\tau$) | Technique ($k$) | Tool ($u$) | Post-State ($s'$) | Verified Command ($c$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `$psversiontable` | `s_passive_topology_mapped` | `$PSVersionTable` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `get-verb` | `s_active_services_enumerated` | `Get-Verb` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `get-wmiobject` | `s_credentials_or_certs_acquired` | `Get-WmiObject -Class Win32_Service -filter "StartMode = 'Auto'"` |
| `s_firewall_or_acl_unlocked` | **`Lateral_Movement_Routing_Pivot`** | Remote Host Execution, L2/L3 Route Injection & Subnet Pivot | `get-wmiobject` | `s_cross_subnet_pivot_routed` | `Get-WmiObject Win32_Service -computer 172.17.10.71 -credential $c -Filter "state='Running'"` |
| `s_init_unknown` | **`Reconnaissance`** | Domain, DNS, OSINT & Target Footprint Reconnaissance | `write-host` | `s_passive_topology_mapped` | `Write-Host "Testing" $i "coming soon to a network near you ...";` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `set-strictmode` | `s_firewall_or_acl_unlocked` | `Set-StrictMode` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `get-host` | `s_passive_topology_mapped` | `Get-Host` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `set-psdebug` | `s_active_services_enumerated` | `Set-PSDebug` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `get-credential` | `s_credentials_or_certs_acquired` | `$c = Get-Credential` |
| `s_firewall_or_acl_unlocked` | **`Lateral_Movement_Routing_Pivot`** | Remote Host Execution, L2/L3 Route Injection & Subnet Pivot | `get-wmiobject` | `s_cross_subnet_pivot_routed` | `Get-WmiObject -computername $i -class win32_process \| Select-Object name, processID, Priority, ThreadCount, PageFaults, PageFileUsage \| Where-Object {!$_.processID -eq 0} \| Sort-Object -property name \| Format-Table \| Out-File $strFile}` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `netsh` | `s_firewall_or_acl_unlocked` | `netsh advfirewall set allprofiles state on` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `get-service` | `s_passive_topology_mapped` | `Get-Service -Name "name"` |
| `s_firewall_or_acl_unlocked` | **`Lateral_Movement_Routing_Pivot`** | Remote Host Execution, L2/L3 Route Injection & Subnet Pivot | `get-wmiobject` | `s_cross_subnet_pivot_routed` | `Get-WmiObject -query "select * from Win32_SystemEnclosure" -ComputerName win7 -Credential $c \| select SerialNumber` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `netsh` | `s_firewall_or_acl_unlocked` | `netsh advfirewall show allprofiles` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `get-psprovider` | `s_passive_topology_mapped` | `Get-PSProvider` |
| `s_firewall_or_acl_unlocked` | **`Lateral_Movement_Routing_Pivot`** | Remote Host Execution, L2/L3 Route Injection & Subnet Pivot | `get-wmiobject` | `s_cross_subnet_pivot_routed` | `$appToRemove = Get-WmiObject Win32_Product -computername win7 -credential $c -Filter "Name like '%Ask'"` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `netsh` | `s_firewall_or_acl_unlocked` | `netsh advfirewall set allprofiles logging droppedconnections enable` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `get-module` | `s_passive_topology_mapped` | `Get-Module` |
| `s_firewall_or_acl_unlocked` | **`Lateral_Movement_Routing_Pivot`** | Remote Host Execution, L2/L3 Route Injection & Subnet Pivot | `get-wmiobject` | `s_cross_subnet_pivot_routed` | `(Get-WmiObject Win32_Product -computername win7 -credential $c -filter "Name like '%Ask'").Uninstall()` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `netsh` | `s_firewall_or_acl_unlocked` | `netsh advfirewall set currentprofile logging maxfilesize 1024` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `get-module` | `s_passive_topology_mapped` | `Get-Module -ListAvailable` |
| `s_firewall_or_acl_unlocked` | **`Lateral_Movement_Routing_Pivot`** | Remote Host Execution, L2/L3 Route Injection & Subnet Pivot | `get-wmiobject` | `s_cross_subnet_pivot_routed` | `Get-WmiObject Win32_Product -computername -credential $c -Filter "Name like '%Ask'"` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `netsh` | `s_firewall_or_acl_unlocked` | `netsh firewall set logging droppedpackets=enable connections=enable maxfilesize=1024` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `get-help` | `s_passive_topology_mapped` | `Get-Help Get-Command -examples` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `netsh` | `s_firewall_or_acl_unlocked` | `netsh advfirewall show allprofiles \| Select-String FileName \| select -ExpandProperty line \| Select-String "%systemroot%.+\.log" \| select -ExpandProperty matches \| select -ExpandProperty value \| sort -uniq` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `get-help` | `s_passive_topology_mapped` | `Get-Help Get-Alias -examples` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `select-string` | `s_firewall_or_acl_unlocked` | `Select-String FileName \| select -ExpandProperty line \| Select-String "%systemroot%.+\.log" \|` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `get-help` | `s_passive_topology_mapped` | `get-help set-alias -full` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `set-alias` | `s_passive_topology_mapped` | `Set-Alias gh Get-Help` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `get-alias` | `s_passive_topology_mapped` | `Get-Alias -Description <Name>` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `get-alias` | `s_passive_topology_mapped` | `Get-Alias -name gwmi` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `get-alias` | `s_passive_topology_mapped` | `Get-Alias \| select * \| Format-Table -AutoSize` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `get-executionpolicy` | `s_passive_topology_mapped` | `Get-ExecutionPolicy -List` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `get-help` | `s_passive_topology_mapped` | `Get-Help Get-Wmi*` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `get-childitem` | `s_passive_topology_mapped` | `Get-ChildItem C:\ \| select name, length, lastaccesstime \| Format-Table -AutoSize` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `get-childitem` | `s_passive_topology_mapped` | `Get-ChildItem *.zip \| Sort-Object -property @{Expression={$_.LastWriteTime - $_.CreationTime}; Ascending=$false} \| Format-Table lastWriteTime, CreationTime` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `get-service` | `s_passive_topology_mapped` | `Get-Service \| Sort-Object -Property @{Expression="Status";Descending=$True}, @{Expression="DsiplayName";Descending=$false}` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `get-command` | `s_passive_topology_mapped` | `Get-Command Get-Command \| Format-List *` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `gcm` | `s_passive_topology_mapped` | `gcm Get-Command \| Format-List *` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `gcm` | `s_passive_topology_mapped` | `(gcm Get-Command).definition` |
powershell -NoProfile -Command "Get-CimInstance Win32_ComputerSystem | Select-Object Name,Domain,Manufacturer,Model,UserName,TotalPhysicalMemory"
## Verified Executable Commands (Grouped by Capability Layer)
powershell -NoProfile -Command "Get-CimInstance Win32_ComputerSystem | Select-Object Name,Domain,Manufacturer,Model,UserName,TotalPhysicalMemory"
### General_System (42 commands)
```bash
$PSVersionTable
Get-Host
Get-Service -Name "name"
Get-PSProvider
Get-Module
Get-Module -ListAvailable
Get-Help Get-Command -examples
Get-Help Get-Alias -examples
get-help set-alias -full
Set-Alias gh Get-Help
Get-Alias -Description <Name>
Get-Alias -name gwmi
Get-Alias | select * | Format-Table -AutoSize
Get-ExecutionPolicy -List
Get-Help Get-Wmi*
Get-Verb
Get-ChildItem C:\ | select name, length, lastaccesstime | Format-Table -AutoSize
Get-ChildItem *.zip | Sort-Object -property @{Expression={$_.LastWriteTime - $_.CreationTime}; Ascending=$false} | Format-Table lastWriteTime, CreationTime
Get-Service | Sort-Object -Property @{Expression="Status";Descending=$True}, @{Expression="DsiplayName";Descending=$false}
Get-Command Get-Command | Format-List *
gcm Get-Command | Format-List *
(gcm Get-Command).definition
gcm -verb u*
gcm -noun p*
Get-Help set* | select name, category, synopsis | Format-Table -AutoSize
Get-Command -Noun PSSessionConfiguration | select Name
Get-WmiObject Win32_Processor | Format-List *
Get-WmiObject -List | ? {$_.name -Match "Win32"}
Get-WmiObject -class Win32_bios
Get-WmiObject Win32_Service -Filter "state='Running'"
Get-WmiObject -Class Win32_Service -filter "StartMode = 'Auto'"
$c = Get-Credential
Get-WmiObject Win32_Service -computer 172.17.10.71 -credential $c -Filter "state='Running'"
Write-Host "Testing" $i "coming soon to a network near you ...";
Get-WmiObject -computername $i -class win32_process | Select-Object name, processID, Priority, ThreadCount, PageFaults, PageFileUsage | Where-Object {!$_.processID -eq 0} | Sort-Object -property name | Format-Table | Out-File $strFile}
Set-PSDebug
Set-StrictMode
Select-String FileName | select -ExpandProperty line | Select-String "%systemroot%.+\.log" |
Get-WmiObject -query "select * from Win32_SystemEnclosure" -ComputerName win7 -Credential $c | select SerialNumber
$appToRemove = Get-WmiObject Win32_Product -computername win7 -credential $c -Filter "Name like '%Ask'"
(Get-WmiObject Win32_Product -computername win7 -credential $c -filter "Name like '%Ask'").Uninstall()
Get-WmiObject Win32_Product -computername -credential $c -Filter "Name like '%Ask'"
```
powershell -NoProfile -Command "Get-CimInstance Win32_ComputerSystem | Select-Object Name,Domain,Manufacturer,Model,UserName,TotalPhysicalMemory"
### L3_Routing_NAT (6 commands)
```bash
netsh advfirewall set allprofiles state on
netsh advfirewall show allprofiles
netsh advfirewall set allprofiles logging droppedconnections enable
netsh advfirewall set currentprofile logging maxfilesize 1024
netsh firewall set logging droppedpackets=enable connections=enable maxfilesize=1024
netsh advfirewall show allprofiles | Select-String FileName | select -ExpandProperty line | Select-String "%systemroot%.+\.log" | select -ExpandProperty matches | select -ExpandProperty value | sort -uniq
```
powershell -NoProfile -Command "Get-CimInstance Win32_ComputerSystem | Select-Object Name,Domain,Manufacturer,Model,UserName,TotalPhysicalMemory"

<!-- CORA-MAXIMIZED-COMMANDS-START -->
## Maximized Windows & Linux Command Examples for `PowerShell-1`

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
