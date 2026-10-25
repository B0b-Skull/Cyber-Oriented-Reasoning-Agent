---
title: "Trained Command Playbook: CQC001_E040_M005_WMI_QR_PowerShell_4.0.pdf"
tags:
  - enumeration
  - http
  - lateral_movement_routing_pivot
  - mdp
  - out-of-band_access
  - passive_enum
  - pdf
  - powershell
  - reconnaissance
  - trained
source_file: CQC001_E040_M005_WMI_QR_PowerShell_4.0.pdf
updated: 2026-10-25 00:57:53
---

# Trained Command Playbook: `CQC001_E040_M005_WMI_QR_PowerShell_4.0.pdf`

- **Source Document:** `~/Projects/CORA/Training/CQC001_E040_M005_WMI_QR_PowerShell_4.0.pdf`
- **CEGAR Verified Commands:** `39` (`0` malformed/unsafe snippets filtered)
- **MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`):** `39`
- **Discovered IPs/Subnets:** `127.0.0.1`
- **Discovered Interfaces:** `None`
- **Related Knowledge Note:** [[knowledge/trained_cqc001_e040_m005_wmi_qr_powershell_4_0]]

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

## Verified Executable Commands (Grouped by Capability Layer)

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

