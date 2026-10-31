---
title: "Trained Command Playbook: CQC001 E040 M005 WMI QR PowerShell 4.0"
category: commands
domain_hub: "[[knowledge/04_windows_powershell_wmi_cim_and_active_directory]]"
os_platform: windows
primary_tactic: Active_Enum
summary: "Verified Windows & Linux command playbook for CQC001 E040 M005 WMI QR PowerShell 4.0 (Active_Enum): PowerShell 2.0-7+ cmdlets, Get-CimInstance/Get-WmiObject/wmic queries, WinRM/PSRemoting (Invoke-Command, Enter-PSSession), Active Direc"
when_to_apply: "Apply when working with CQC001 E040 M005 WMI QR PowerShell 4.0 (windows): Apply when automating Windows enumeration with PowerShell or WMI/CIM (`Get-CimInstance`/`wmic`), executing commands remotely via WinRM/WMI, enumerating Active Directory users/groups/computers/trusts/GPOs (`dsquery`/`nltest`/`net`), or auditing Kerberos tickets (`klist`) and SPNs (`setspn`)."
tags: [enumeration, http, lateral_movement_routing_pivot, mdp, out-of-band_access, passive_enum, pdf, powershell, reconnaissance, trained, windows, wmic, get-ciminstance, winrm, invoke-command, dsquery, nltest, kerberos, klist, setspn, active_directory, ldap]
source_file: "CQC001 E040 M005 WMI QR PowerShell 4.0"
updated: 2026-10-30
---

powershell -NoProfile -Command "Get-CimInstance Win32_ComputerSystem | Select-Object Name,Domain,Manufacturer,Model,UserName,TotalPhysicalMemory"
# Trained Command Playbook: `CQC001_E040_M005_WMI_QR_PowerShell_4.0.pdf`
powershell -NoProfile -Command "Get-CimInstance Win32_ComputerSystem | Select-Object Name,Domain,Manufacturer,Model,UserName,TotalPhysicalMemory"
- **Source Document:** `~/Projects/CORA/Training/CQC001_E040_M005_WMI_QR_PowerShell_4.0.pdf`
- **CEGAR Verified Commands:** `39` (`0` malformed/unsafe snippets filtered)
- **MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`):** `39`
- **Discovered IPs/Subnets:** `127.0.0.1`
- **Discovered Interfaces:** `None`
- **Related Knowledge Note:** [[knowledge/trained_cqc001_e040_m005_wmi_qr_powershell_4_0]]
powershell -NoProfile -Command "Get-CimInstance Win32_ComputerSystem | Select-Object Name,Domain,Manufacturer,Model,UserName,TotalPhysicalMemory"
## Distilled MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`)
| Pre-State ($s$) | Tactic ($\tau$) | Technique ($k$) | Tool ($u$) | Post-State ($s'$) | Verified Command ($c$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `get-ciminstance` | `s_passive_topology_mapped` | `Get-CimInstance -Namespace <Tab>  #Finding top level namespaces` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `get-cimclass` | `s_active_services_enumerated` | `Get-CimClass #All classes in root/cimv2` |
| `s_init_unknown` | **`Reconnaissance`** | Domain, DNS, OSINT & Target Footprint Reconnaissance | `register-cimindicationevent` | `s_passive_topology_mapped` | `Register-CimIndicationEvent -Query $filter  -SourceIdentifier "Timer"` |
| `s_firewall_or_acl_unlocked` | **`Lateral_Movement_Routing_Pivot`** | Remote Host Execution, L2/L3 Route Injection & Subnet Pivot | `get-ciminstance` | `s_cross_subnet_pivot_routed` | `Get-CimInstance Win32_Service -ComputerName Server1` |
| `s_l2_l3_verified` | **`Out-of-Band_Access`** | UART/Serial Console Out-of-Band Enumeration & Control | `new-cimsession` | `s_oob_serial_enumerated` | `$s = New-CimSession -CN server1` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `get-ciminstance` | `s_passive_topology_mapped` | `Get-CimInstance -ClassName *Bios<Tab>` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `get-cimassociatedinstance` | `s_active_services_enumerated` | `Get-CimAssociatedInstance -CimInstance $disk1` |
| `s_init_unknown` | **`Reconnaissance`** | Domain, DNS, OSINT & Target Footprint Reconnaissance | `get-event` | `s_passive_topology_mapped` | `Get-Event -SourceIdentifier Timer` |
| `s_l2_l3_verified` | **`Out-of-Band_Access`** | UART/Serial Console Out-of-Band Enumeration & Control | `new-cimsession` | `s_oob_serial_enumerated` | `$s = New-CimSession -CN server1 -SessionOption $so` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `get-ciminstance` | `s_passive_topology_mapped` | `Get-CimInstance -Namespace root/Microsoft/Windows/smb -ClassName <tab>` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `get-cimassociatedinstance` | `s_active_services_enumerated` | `Get-CimAssociatedInstance -CimInstance $disk1 -ResultClassName Win32_DiskPartition` |
| `s_init_unknown` | **`Reconnaissance`** | Domain, DNS, OSINT & Target Footprint Reconnaissance | `unregister-event` | `s_passive_topology_mapped` | `Unregister-Event -SourceIdentifier "Timer"` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `get-cimclass` | `s_passive_topology_mapped` | `Get-CimClass -MethodName Stop* #Find classes that have a method like Stop*` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `get-cimassociatedinstance` | `s_active_services_enumerated` | `Get-CimAssociatedInstance -InputObject $service -Association Win32_DependentService` |
| `s_init_unknown` | **`Reconnaissance`** | Domain, DNS, OSINT & Target Footprint Reconnaissance | `register-cimindicationevent` | `s_passive_topology_mapped` | `Register-CimIndicationEvent -ClassName Win32_ProcessStartTrace   -Action $Action -SourceIdentifier` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `get-cimclass` | `s_passive_topology_mapped` | `Get-CimClass -PropertyName Handle #Find classes that have a property name handle` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `get-cimclass` | `s_active_services_enumerated` | `$c = Get-CimClass Win32_Process` |
| `s_init_unknown` | **`Reconnaissance`** | Domain, DNS, OSINT & Target Footprint Reconnaissance | `unregister-event` | `s_passive_topology_mapped` | `Unregister-Event -SourceIdentifier "ProcessWatch"` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `get-cimclass` | `s_passive_topology_mapped` | `Get-CimClass -ClassName *Partition -QualifierName Association #Find Association classes` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `new-ciminstance` | `s_active_services_enumerated` | `New-CimInstance -Class Win32_Environment -Property @{Name="testvar"; VariableValue="testvalue";` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `get-cimclass` | `s_passive_topology_mapped` | `Get-CimClass -Namespace root/Microsoft/Windows/smb -class *Smb* -QualifierName Indication` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `set-ciminstance` | `s_active_services_enumerated` | `Set-CimInstance -InputObject $a -Property @{VariableValue="ChangedValue"} -PassThru` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `get-ciminstance` | `s_passive_topology_mapped` | `Get-CimInstance -ClassName Win32_Service  #Find instances of Win32_Service class` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `set-ciminstance` | `s_active_services_enumerated` | `Set-CimInstance -InputObject $a -PassThru` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `get-ciminstance` | `s_passive_topology_mapped` | `Get-CimInstance -Query "Select * from Win32_Service Where Name like 'app%'"` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `remove-ciminstance` | `s_active_services_enumerated` | `Remove-CimInstance -InputObject $a` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `get-ciminstance` | `s_passive_topology_mapped` | `Get-CimInstance -ClassName Win32_Service -KeyOnly` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `new-cimsessionoption` | `s_active_services_enumerated` | `$so = New-CimSessionOption -Protocol DCOM` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `get-ciminstance` | `s_passive_topology_mapped` | `Get-CimInstance -ClassName Win32_Service -Property Name, Status` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `get-ciminstance` | `s_passive_topology_mapped` | `$a = Get-CimInstance -ClassName Win32_Process` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `get-ciminstance` | `s_passive_topology_mapped` | `Get-CimInstance -InputObject $a[0] #Note object passed as input object is not changed` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `get-ciminstance` | `s_passive_topology_mapped` | `$service = Get-CimInstance Win32_Service -Filter 'Name Like "winrm%"'` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `get-command` | `s_passive_topology_mapped` | `Get-Command -Module CimCmdlets` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `get-ciminstance` | `s_passive_topology_mapped` | `$a = Get-CimInstance Win32_Process -Filter "Name Like 'PowerShell%'"` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `get-ciminstance` | `s_passive_topology_mapped` | `$a = Get-CimInstance -Class Win32_Environment -Filter "Name='testvar'" #; VariableValue="testvalue";` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `gcim` | `s_passive_topology_mapped` | `gcim Win32_Service -CimSession $s` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `get-ciminstance` | `s_passive_topology_mapped` | `Get-CimInstance Win32_Service -CimSession $s` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `gcim` | `s_passive_topology_mapped` | `gcim Win32_Process -CN server1,server2 \| Select Name, PsComputerName` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `gcim` | `s_passive_topology_mapped` | `gcim Win32_Process -CN server1,server2 \| icim -MethodName GetOwner` |
powershell -NoProfile -Command "Get-CimInstance Win32_ComputerSystem | Select-Object Name,Domain,Manufacturer,Model,UserName,TotalPhysicalMemory"
## Verified Executable Commands (Grouped by Capability Layer)
powershell -NoProfile -Command "Get-CimInstance Win32_ComputerSystem | Select-Object Name,Domain,Manufacturer,Model,UserName,TotalPhysicalMemory"
### General_System (39 commands)
```bash
Get-CimInstance -Namespace <Tab>  #Finding top level namespaces
Get-CimInstance -ClassName *Bios<Tab>
Get-CimInstance -Namespace root/Microsoft/Windows/smb -ClassName <tab>
Get-CimClass #All classes in root/cimv2
Get-CimClass -MethodName Stop* #Find classes that have a method like Stop*
Get-CimClass -PropertyName Handle #Find classes that have a property name handle
Get-CimClass -ClassName *Partition -QualifierName Association #Find Association classes
Get-CimClass -Namespace root/Microsoft/Windows/smb -class *Smb* -QualifierName Indication
Get-CimInstance -ClassName Win32_Service  #Find instances of Win32_Service class
Get-CimInstance -Query "Select * from Win32_Service Where Name like 'app%'"
Get-CimInstance -ClassName Win32_Service -KeyOnly
Get-CimInstance -ClassName Win32_Service -Property Name, Status
$a = Get-CimInstance -ClassName Win32_Process
Get-CimInstance -InputObject $a[0] #Note object passed as input object is not changed
Get-CimAssociatedInstance -CimInstance $disk1
Get-CimAssociatedInstance -CimInstance $disk1 -ResultClassName Win32_DiskPartition
$service = Get-CimInstance Win32_Service -Filter 'Name Like "winrm%"'
Get-CimAssociatedInstance -InputObject $service -Association Win32_DependentService
Get-Command -Module CimCmdlets
$c = Get-CimClass Win32_Process
$a = Get-CimInstance Win32_Process -Filter "Name Like 'PowerShell%'"
New-CimInstance -Class Win32_Environment -Property @{Name="testvar"; VariableValue="testvalue";
$a = Get-CimInstance -Class Win32_Environment -Filter "Name='testvar'" #; VariableValue="testvalue";
Set-CimInstance -InputObject $a -Property @{VariableValue="ChangedValue"} -PassThru
Set-CimInstance -InputObject $a -PassThru
Remove-CimInstance -InputObject $a
Register-CimIndicationEvent -Query $filter  -SourceIdentifier "Timer"
Get-Event -SourceIdentifier Timer
Unregister-Event -SourceIdentifier "Timer"
Register-CimIndicationEvent -ClassName Win32_ProcessStartTrace   -Action $Action -SourceIdentifier
Unregister-Event -SourceIdentifier "ProcessWatch"
Get-CimInstance Win32_Service -ComputerName Server1
$s = New-CimSession -CN server1
gcim Win32_Service -CimSession $s
$so = New-CimSessionOption -Protocol DCOM
$s = New-CimSession -CN server1 -SessionOption $so
Get-CimInstance Win32_Service -CimSession $s
gcim Win32_Process -CN server1,server2 | Select Name, PsComputerName
gcim Win32_Process -CN server1,server2 | icim -MethodName GetOwner
```
powershell -NoProfile -Command "Get-CimInstance Win32_ComputerSystem | Select-Object Name,Domain,Manufacturer,Model,UserName,TotalPhysicalMemory"

<!-- CORA-MAXIMIZED-COMMANDS-START -->
## Maximized Windows & Linux Command Examples for `CQC001 E040 M005 WMI QR PowerShell 4.0`

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
