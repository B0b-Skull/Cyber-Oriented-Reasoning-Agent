---
title: "Trained Command Playbook: us-15-Graeber-Abusing-Windows-Management-Instrumentation-WMI-To-Build-A-Persistent Asynchronous-And-Fileless-Backdoor-wp.pdf"
tags:
  - credential_access
  - curl
  - enumeration
  - http
  - https
  - lateral_movement_routing_pivot
  - mdp
  - out-of-band_access
  - passive_enum
  - pdf
  - powershell
  - reconnaissance
  - sysinternals
  - trained
  - wmic
source_file: us-15-Graeber-Abusing-Windows-Management-Instrumentation-WMI-To-Build-A-Persistent Asynchronous-And-Fileless-Backdoor-wp.pdf
updated: 2026-10-25 01:01:08
---

# Trained Command Playbook: `us-15-Graeber-Abusing-Windows-Management-Instrumentation-WMI-To-Build-A-Persistent Asynchronous-And-Fileless-Backdoor-wp.pdf`

- **Source Document:** `~/Projects/CORA/Training/us-15-Graeber-Abusing-Windows-Management-Instrumentation-WMI-To-Build-A-Persistent Asynchronous-And-Fileless-Backdoor-wp.pdf`
- **CEGAR Verified Commands:** `47` (`0` malformed/unsafe snippets filtered)
- **MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`):** `47`
- **Discovered IPs/Subnets:** `172.24.72.131, 172.24.72.134, 172.24.72.135`
- **Discovered Interfaces:** `None`
- **Related Knowledge Note:** [[knowledge/trained_us-15-graeber-abusing-windows-management-instrumentation-wmi-to-]]

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

## Verified Executable Commands (Grouped by Capability Layer)

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

