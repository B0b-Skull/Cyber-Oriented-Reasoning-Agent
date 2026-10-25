---
title: "Trained Command Playbook: wp-windows-management-instrumentation.pdf"
tags:
  - credential_access
  - curl
  - enumeration
  - http
  - https
  - lateral_movement_routing_pivot
  - mdp
  - passive_enum
  - pdf
  - powershell
  - sysinternals
  - trained
  - wmic
source_file: wp-windows-management-instrumentation.pdf
updated: 2026-10-25 01:01:14
---

# Trained Command Playbook: `wp-windows-management-instrumentation.pdf`

- **Source Document:** `~/Projects/CORA/Training/wp-windows-management-instrumentation.pdf`
- **CEGAR Verified Commands:** `50` (`0` malformed/unsafe snippets filtered)
- **MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`):** `50`
- **Discovered IPs/Subnets:** `1.5.0.7, 127.0.0.1, 172.24.72.131, 172.24.72.134, 172.24.72.135, 2.2.2.7, 5.9.7.6, 7.0.0.1, 7.0.3.5, 8.1.0.4, 8.4.9.8, 9.1.7.0, 9.4.2.9`
- **Discovered Interfaces:** `Lo`
- **Related Knowledge Note:** [[knowledge/trained_wp-windows-management-instrumentation]]

## Distilled MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`)
| Pre-State ($s$) | Tactic ($\tau$) | Technique ($k$) | Tool ($u$) | Post-State ($s'$) | Verified Command ($c$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `wmic` | `s_passive_topology_mapped` | `wmic and wmis-pth for Linux` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `get-wminamespace-namespace$ns` | `s_active_services_enumerated` | `Get-WmiNamespace-Namespace$ns` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `get-wmiobject` | `s_credentials_or_certs_acquired` | `Get-WmiObject -Class Win32_Process -ComputerName` |
| `s_firewall_or_acl_unlocked` | **`Lateral_Movement_Routing_Pivot`** | Remote Host Execution, L2/L3 Route Injection & Subnet Pivot | `test-wsman` | `s_cross_subnet_pivot_routed` | `Test-WSMan -ComputerName 172.24.72.134` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `get-wmiobject-namespace$namespace-class__namespace` | `s_passive_topology_mapped` | `Get-WmiObject-Namespace$Namespace-Class__NAMESPACE\|ForEach-Object {` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `get-wminamespace` | `s_active_services_enumerated` | `$WmiClasses=Get-WmiNamespace\|ForEach-Object {` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `get-ciminstance` | `s_credentials_or_certs_acquired` | `Get-CimInstance -CimSession $CimSession -ClassName Win32_Process` |
| `s_firewall_or_acl_unlocked` | **`Lateral_Movement_Routing_Pivot`** | Remote Host Execution, L2/L3 Route Injection & Subnet Pivot | `new-cimsession` | `s_cross_subnet_pivot_routed` | `$CimSession = New-CimSession -ComputerName 172.24.72.134 -Credential 'WIN-B85AAA7ST4U Administrator' -Authentic` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `get-wmiobject-namespace$namespace-list` | `s_passive_topology_mapped` | `Get-WmiObject-Namespace$Namespace-List\| ForEach-Object { $_.Path.Path }` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `get-cimassociatedinstance` | `s_active_services_enumerated` | `Get-CimAssociatedInstance` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `new-objectmanagement.connectionoptions` | `s_credentials_or_certs_acquired` | `$Options=New-ObjectManagement.ConnectionOptions` |
| `s_firewall_or_acl_unlocked` | **`Lateral_Movement_Routing_Pivot`** | Remote Host Execution, L2/L3 Route Injection & Subnet Pivot | `invoke-wmimethod` | `s_cross_subnet_pivot_routed` | `Invoke-WmiMethod -Class Win32_Process -Name Create -ArgumentList 'notepad.exe' -ComputerName 172.24.72.134 -Cre` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `get-wmiobject` | `s_passive_topology_mapped` | `Get-WmiObject` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `get-cimclass` | `s_active_services_enumerated` | `Get-CimClass` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `new-objectmanagement.managementscope` | `s_credentials_or_certs_acquired` | `$Connection=New-ObjectManagement.ManagementScope` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `get-ciminstance` | `s_passive_topology_mapped` | `Get-CimInstance` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `get-cimsession` | `s_active_services_enumerated` | `Get-CimSession` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `administrator` | `s_credentials_or_certs_acquired` | `$Credential=Get-Credential'WIN-B85AAA7ST4U\Administrator'` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `get-wmiobject` | `s_passive_topology_mapped` | `Get-WmiObject -Namespace root\SecurityCenter2 -Class AntiVirusProduct` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `set-wmiinstance` | `s_active_services_enumerated` | `Set-WmiInstance` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `get-wmiobject-class__filtertoconsumerbinding@arguments` | `s_credentials_or_certs_acquired` | `Get-WmiObject-Class__FilterToConsumerBinding@Arguments` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `get-wmiobjectwin32_bios-filter'serialnumber` | `s_passive_topology_mapped` | `$VMBios=Get-WmiObjectWin32_BIOS-Filter'SerialNumber LIKE "%VMware%"'` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `set-ciminstance` | `s_active_services_enumerated` | `Set-CimInstance` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `get-wmiobject-class__eventfilter@arguments` | `s_credentials_or_certs_acquired` | `Get-WmiObject-Class__EventFilter@Arguments` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `get-wmiobjectwin32_process-filter'name="vmtoolsd` | `s_passive_topology_mapped` | `$VMToolsRunning=Get-WmiObjectWin32_Process-Filter'Name="vmtoolsd.exe"'` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `invoke-wmimethod` | `s_active_services_enumerated` | `Invoke-WmiMethod` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `get-wmiobject-class__eventconsumer@arguments` | `s_credentials_or_certs_acquired` | `Get-WmiObject-Class__EventConsumer@Arguments` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `ver` | `s_passive_topology_mapped` | `ver file contains a single unsigned 32-bit` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `invoke-cimmethod` | `s_active_services_enumerated` | `Invoke-CimMethod` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `type` | `s_passive_topology_mapped` | `TYPE qualifier with the value uint32.` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `new-ciminstance` | `s_active_services_enumerated` | `New-CimInstance` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `new-cimsession` | `s_active_services_enumerated` | `New-CimSession` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `new-cimsessionoption` | `s_active_services_enumerated` | `New-CimSessionOption` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `register-cimindicationevent` | `s_active_services_enumerated` | `Register-CimIndicationEvent` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `register-wmievent` | `s_active_services_enumerated` | `Register-WmiEvent` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `remove-ciminstance` | `s_active_services_enumerated` | `Remove-CimInstance` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `remove-wmiobject` | `s_active_services_enumerated` | `Remove-WmiObject` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `remove-cimsession` | `s_active_services_enumerated` | `Remove-CimSession` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `ls` | `s_active_services_enumerated` | `ls WSMan:\localhost` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `set-wmiinstance-class__eventfilter-` | `s_active_services_enumerated` | `$WMIEventFilter=Set-WmiInstance-Class__EventFilter-` |

## Verified Executable Commands (Grouped by Capability Layer)

### General_System (50 commands)
```bash
wmic and wmis-pth for Linux
Get-WmiObject-Namespace$Namespace-Class__NAMESPACE|ForEach-Object {
Get-WmiNamespace-Namespace$ns
$WmiClasses=Get-WmiNamespace|ForEach-Object {
Get-WmiObject-Namespace$Namespace-List| ForEach-Object { $_.Path.Path }
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
Get-WmiObject -Class Win32_Process -ComputerName
ls WSMan:\localhost
Test-WSMan -ComputerName 172.24.72.134
$CimSession = New-CimSession -ComputerName 172.24.72.134 -Credential 'WIN-B85AAA7ST4U Administrator' -Authentic
Get-CimInstance -CimSession $CimSession -ClassName Win32_Process
$WMIEventFilter=Set-WmiInstance-Class__EventFilter-
$WMIEventConsumer=Set-WmiInstance-
Set-WmiInstance-Class__FilterToConsumerBinding-
Get-WmiObject -Namespace root\SecurityCenter2 -Class AntiVirusProduct
$VMBios=Get-WmiObjectWin32_BIOS-Filter'SerialNumber LIKE "%VMware%"'
$VMToolsRunning=Get-WmiObjectWin32_Process-Filter'Name="vmtoolsd.exe"'
Invoke-WmiMethod -Class Win32_Process -Name Create -ArgumentList 'notepad.exe' -ComputerName 172.24.72.134 -Cre
$Options=New-ObjectManagement.ConnectionOptions
$Connection=New-ObjectManagement.ManagementScope
$Credential=Get-Credential'WIN-B85AAA7ST4U\Administrator'
Invoke-WmiMethod@CommonArgs-ClassWin32_Process-NameCreate-
Invoke-WmiMethod@CommonArgs-ClassStdRegProv-NameCreateKey-
Invoke-WmiMethod@CommonArgs-ClassStdRegProv-NameDeleteValue-
Set-ItemProperty -Path HKLM:\SOFTWARE\EvilKey -Name Result -Value
$RemoteOutput=Invoke-WmiMethod@CommonArgs-ClassStdRegProv-
Get-WmiObject-Class__FilterToConsumerBinding@Arguments
Get-WmiObject-Class__EventFilter@Arguments
Get-WmiObject-Class__EventConsumer@Arguments
last time.
ver file contains a single unsigned 32-bit
locate classes and instances. For
locate its offset. The index operates
TYPE qualifier with the value uint32.
```

