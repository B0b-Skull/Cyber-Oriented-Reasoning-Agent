---
title: "Trained Command Playbook: us-15-Graeber-Abusing-Windows-Management-Instrumentation-WMI-To-Build-A-Persistent Asynchronous-And-Fileless-Backdoor-wp"
category: commands
domain_hub: "[[knowledge/04_windows_powershell_wmi_cim_and_active_directory]]"
os_platform: windows
primary_tactic: Active_Enum
summary: "Verified Windows & Linux command playbook for us-15-Graeber-Abusing-Windows-Management-Instrumentation-WMI-To-Build-A-Persistent Asynchronous-And-Fileless-Backdoor-wp (Active_Enum): PowerShell 2.0-7+ cmdlets, Get-CimInstance/Get-WmiObject/wmic queries, WinRM/PSRemoting (Invoke-Command, Enter-PSSession), Active Direc"
when_to_apply: "Apply when working with us-15-Graeber-Abusing-Windows-Management-Instrumentation-WMI-To-Build-A-Persistent Asynchronous-And-Fileless-Backdoor-wp (windows): Apply when automating Windows enumeration with PowerShell or WMI/CIM (`Get-CimInstance`/`wmic`), executing commands remotely via WinRM/WMI, enumerating Active Directory users/groups/computers/trusts/GPOs (`dsquery`/`nltest`/`net`), or auditing Kerberos tickets (`klist`) and SPNs (`setspn`)."
tags: [credential_access, curl, enumeration, http, https, lateral_movement_routing_pivot, mdp, out-of-band_access, passive_enum, pdf, powershell, reconnaissance, sysinternals, trained, wmic, windows, get-ciminstance, winrm, invoke-command, dsquery, nltest, kerberos]
source_file: "us-15-Graeber-Abusing-Windows-Management-Instrumentation-WMI-To-Build-A-Persistent Asynchronous-And-Fileless-Backdoor-wp"
updated: 2026-10-30
---

powershell -NoProfile -Command "Get-CimInstance Win32_ComputerSystem | Select-Object Name,Domain,Manufacturer,Model,UserName,TotalPhysicalMemory"
# Trained Command Playbook: `us-15-Graeber-Abusing-Windows-Management-Instrumentation-WMI-To-Build-A-Persistent Asynchronous-And-Fileless-Backdoor-wp.pdf`
powershell -NoProfile -Command "Get-CimInstance Win32_ComputerSystem | Select-Object Name,Domain,Manufacturer,Model,UserName,TotalPhysicalMemory"
- **Source Document:** `~/Projects/CORA/Training/us-15-Graeber-Abusing-Windows-Management-Instrumentation-WMI-To-Build-A-Persistent Asynchronous-And-Fileless-Backdoor-wp.pdf`
- **CEGAR Verified Commands:** `47` (`0` malformed/unsafe snippets filtered)
- **MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`):** `47`
- **Discovered IPs/Subnets:** `172.24.72.131, 172.24.72.134, 172.24.72.135`
- **Discovered Interfaces:** `None`
- **Related Knowledge Note:** [[knowledge/trained_us-15-graeber-abusing-windows-management-instrumentation-wmi-to-]]
powershell -NoProfile -Command "Get-CimInstance Win32_ComputerSystem | Select-Object Name,Domain,Manufacturer,Model,UserName,TotalPhysicalMemory"
## Distilled MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`)
| Pre-State ($s$) | Tactic ($\tau$) | Technique ($k$) | Tool ($u$) | Post-State ($s'$) | Verified Command ($c$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `get-wmiobject` | `s_passive_topology_mapped` | `Get-WmiObject -Namespace $Namespace -Class __NAMESPACE \| ForEach-Object {` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `get-wminamespace` | `s_active_services_enumerated` | `Get-WmiNamespace -Namespace $ns` |
| `s_l2_l3_verified` | **`Out-of-Band_Access`** | UART/Serial Console Out-of-Band Enumeration & Control | `new-ciminstance` | `s_oob_serial_enumerated` | `New-CimInstance` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `wmic` | `s_credentials_or_certs_acquired` | `wmic and wmis-pth for Linux` |
| `s_init_unknown` | **`Reconnaissance`** | Domain, DNS, OSINT & Target Footprint Reconnaissance | `ls` | `s_passive_topology_mapped` | `ls WSMan:\localhost` |
| `s_firewall_or_acl_unlocked` | **`Lateral_Movement_Routing_Pivot`** | Remote Host Execution, L2/L3 Route Injection & Subnet Pivot | `test-wsman` | `s_cross_subnet_pivot_routed` | `Test-WSMan -ComputerName 172.24.72.134` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `get-wmiobject` | `s_passive_topology_mapped` | `Get-WmiObject -Namespace $Namespace -List \| ForEach-Object { $_.Path.Path }` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `get-wminamespace` | `s_active_services_enumerated` | `$WmiClasses = Get-WmiNamespace \| ForEach-Object {` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `get-wmiobject` | `s_credentials_or_certs_acquired` | `Get-WmiObject -Class Win32_Process -ComputerName` |
| `s_firewall_or_acl_unlocked` | **`Lateral_Movement_Routing_Pivot`** | Remote Host Execution, L2/L3 Route Injection & Subnet Pivot | `new-cimsession` | `s_cross_subnet_pivot_routed` | `$CimSession = New-CimSession -ComputerName 172.24.72.134 -Credential 'WIN-B85AAA7ST4U\Administrator' -Authentic` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `get-wmiobject` | `s_passive_topology_mapped` | `Get-WmiObject` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `get-cimassociatedinstance` | `s_active_services_enumerated` | `Get-CimAssociatedInstance` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `get-ciminstance` | `s_credentials_or_certs_acquired` | `Get-CimInstance -CimSession $CimSession -ClassName` |
| `s_firewall_or_acl_unlocked` | **`Lateral_Movement_Routing_Pivot`** | Remote Host Execution, L2/L3 Route Injection & Subnet Pivot | `get-wmiobject` | `s_cross_subnet_pivot_routed` | `$VMBios = Get-WmiObject Win32_BIOS -Filter 'SerialNumber LIKE "%VMware%"'` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `get-ciminstance` | `s_passive_topology_mapped` | `Get-CimInstance` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `get-cimclass` | `s_active_services_enumerated` | `Get-CimClass` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `new-object` | `s_credentials_or_certs_acquired` | `$Options = New-Object Management.ConnectionOptions` |
| `s_firewall_or_acl_unlocked` | **`Lateral_Movement_Routing_Pivot`** | Remote Host Execution, L2/L3 Route Injection & Subnet Pivot | `get-wmiobject` | `s_cross_subnet_pivot_routed` | `$VMToolsRunning = Get-WmiObject Win32_Process -Filter 'Name="vmtoolsd.exe"'` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `get-wmiobject` | `s_passive_topology_mapped` | `Get-WmiObject -Namespace root\SecurityCenter2 -Class AntiVirusProduct` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `get-cimsession` | `s_active_services_enumerated` | `Get-CimSession` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `new-object` | `s_credentials_or_certs_acquired` | `$Connection = New-Object Management.ManagementScope` |
| `s_firewall_or_acl_unlocked` | **`Lateral_Movement_Routing_Pivot`** | Remote Host Execution, L2/L3 Route Injection & Subnet Pivot | `invoke-wmimethod` | `s_cross_subnet_pivot_routed` | `Invoke-WmiMethod -Class Win32_Process -Name Create -ArgumentList 'notepad.exe' -ComputerName 172.24.72.134 -Cre` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `invoke-wmimethod` | `s_passive_topology_mapped` | `Invoke-WmiMethod @CommonArgs -Class Win32_Process -Name Create -ArgumentList` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `set-wmiinstance` | `s_active_services_enumerated` | `Set-WmiInstance` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `get-credential` | `s_credentials_or_certs_acquired` | `$Credential = Get-Credential 'WIN-B85AAA7ST4U\Administrator'` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `get-wmiobject` | `s_passive_topology_mapped` | `Get-WmiObject @CommonArgs -Class CIM_DataFile -Filter 'Name = "C:\\fighter_jet_specs.png"'` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `set-ciminstance` | `s_active_services_enumerated` | `Set-CimInstance` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `get-ciminstance` | `s_passive_topology_mapped` | `Get-CimInstance -Namespace root\cimv2 -ClassName` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `invoke-wmimethod` | `s_active_services_enumerated` | `Invoke-WmiMethod` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `get-wmiobject` | `s_passive_topology_mapped` | `Get-WmiObject -Class __FilterToConsumerBinding @Arguments` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `invoke-cimmethod` | `s_active_services_enumerated` | `Invoke-CimMethod` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `get-wmiobject` | `s_passive_topology_mapped` | `Get-WmiObject -Class __EventFilter @Arguments` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `new-cimsession` | `s_active_services_enumerated` | `New-CimSession` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `get-wmiobject` | `s_passive_topology_mapped` | `Get-WmiObject -Class __EventConsumer @Arguments` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `new-cimsessionoption` | `s_active_services_enumerated` | `New-CimSessionOption` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `register-cimindicationevent` | `s_active_services_enumerated` | `Register-CimIndicationEvent` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `register-wmievent` | `s_active_services_enumerated` | `Register-WmiEvent` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `remove-ciminstance` | `s_active_services_enumerated` | `Remove-CimInstance` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `remove-wmiobject` | `s_active_services_enumerated` | `Remove-WmiObject` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `remove-cimsession` | `s_active_services_enumerated` | `Remove-CimSession` |
powershell -NoProfile -Command "Get-CimInstance Win32_ComputerSystem | Select-Object Name,Domain,Manufacturer,Model,UserName,TotalPhysicalMemory"
## Verified Executable Commands (Grouped by Capability Layer)
powershell -NoProfile -Command "Get-CimInstance Win32_ComputerSystem | Select-Object Name,Domain,Manufacturer,Model,UserName,TotalPhysicalMemory"
### General_System (47 commands)
```bash
Get-WmiObject -Namespace $Namespace -Class __NAMESPACE | ForEach-Object {
Get-WmiNamespace -Namespace $ns
$WmiClasses = Get-WmiNamespace | ForEach-Object {
Get-WmiObject -Namespace $Namespace -List | ForEach-Object { $_.Path.Path }
Get-WmiObject
Get-CimAssociatedInstance
Get-CimClass
Get-CimInstance
Get-CimSession
Set-WmiInstance
Set-CimInstance
Invoke-WmiMethod
Invoke-CimMethod
New-CimInstance
New-CimSession
New-CimSessionOption
Register-CimIndicationEvent
Register-WmiEvent
Remove-CimInstance
Remove-WmiObject
Remove-CimSession
wmic and wmis-pth for Linux
Get-WmiObject -Class Win32_Process -ComputerName
ls WSMan:\localhost
Test-WSMan -ComputerName 172.24.72.134
$CimSession = New-CimSession -ComputerName 172.24.72.134 -Credential 'WIN-B85AAA7ST4U\Administrator' -Authentic
Get-CimInstance -CimSession $CimSession -ClassName
$WMIEventConsumer = Set-WmiInstance -Class
Set-WmiInstance -Class __FilterToConsumerBinding -Namespace
Get-WmiObject -Namespace root\SecurityCenter2 -Class AntiVirusProduct
$VMBios = Get-WmiObject Win32_BIOS -Filter 'SerialNumber LIKE "%VMware%"'
$VMToolsRunning = Get-WmiObject Win32_Process -Filter 'Name="vmtoolsd.exe"'
Invoke-WmiMethod -Class Win32_Process -Name Create -ArgumentList 'notepad.exe' -ComputerName 172.24.72.134 -Cre
$StaticClass = New-Object
$Options = New-Object Management.ConnectionOptions
$Connection = New-Object Management.ManagementScope
$Credential = Get-Credential 'WIN-B85AAA7ST4U\Administrator'
Invoke-WmiMethod @CommonArgs -Class Win32_Process -Name Create -ArgumentList
Get-WmiObject @CommonArgs -Class CIM_DataFile -Filter 'Name = "C:\\fighter_jet_specs.png"'
Invoke-WmiMethod @CommonArgs -Class StdRegProv -Name CreateKey -ArgumentList
Invoke-WmiMethod @CommonArgs -Class StdRegProv -Name DeleteValue -ArgumentList
Set-ItemProperty -Path HKLM:\SOFTWARE\EvilKey -Name Result -Value $Encoded
$RemoteOutput = Invoke-WmiMethod @CommonArgs -Class StdRegProv -Name
Get-CimInstance -Namespace root\cimv2 -ClassName
Get-WmiObject -Class __FilterToConsumerBinding @Arguments
Get-WmiObject -Class __EventFilter @Arguments
Get-WmiObject -Class __EventConsumer @Arguments
```
powershell -NoProfile -Command "Get-CimInstance Win32_ComputerSystem | Select-Object Name,Domain,Manufacturer,Model,UserName,TotalPhysicalMemory"

<!-- CORA-MAXIMIZED-COMMANDS-START -->
## Maximized Windows & Linux Command Examples for `us-15-Graeber-Abusing-Windows-Management-Instrumentation-WMI-To-Build-A-Persistent Asynchronous-And-Fileless-Backdoor-wp`

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
