---
title: "Trained Command Playbook: PS Get-CIM.txt"
tags:
  - credential_access
  - lateral_movement_routing_pivot
  - mdp
  - passive_enum
  - text
  - trained
source_file: PS Get-CIM.txt
updated: 2026-10-24 01:00:10
---

# Trained Command Playbook: `PS Get-CIM.txt`

- **Source Document:** `~/Projects/CORA/Training/PS Get-CIM.txt`
- **CEGAR Verified Commands:** `17` (`0` malformed/unsafe snippets filtered)
- **MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`):** `17`
- **Discovered IPs/Subnets:** `None`
- **Discovered Interfaces:** `None`
- **Related Knowledge Note:** [[knowledge/trained_ps_get-cim]]

## Distilled MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`)
| Pre-State ($s$) | Tactic ($\tau$) | Technique ($k$) | Tool ($u$) | Post-State ($s'$) | Verified Command ($c$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `get-ciminstance` | `s_passive_topology_mapped` | `Get-CimInstance Win32_Process` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `get-cimclass` | `s_credentials_or_certs_acquired` | `Get-CimClass \| Where {$_.CimClassName -match 'User'}` |
| `s_firewall_or_acl_unlocked` | **`Lateral_Movement_Routing_Pivot`** | Remote Host Execution, L2/L3 Route Injection & Subnet Pivot | `new-cimsession` | `s_cross_subnet_pivot_routed` | `$c = New-CimSession -ComputerName win10 -Credential fred` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `get-ciminstance` | `s_passive_topology_mapped` | `Get-CimInstance Win32_bios` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `new-cimsessionoption` | `s_credentials_or_certs_acquired` | `$dopt = New-CimSessionOption -Protocol Dcom` |
| `s_firewall_or_acl_unlocked` | **`Lateral_Movement_Routing_Pivot`** | Remote Host Execution, L2/L3 Route Injection & Subnet Pivot | `new-cimsession` | `s_cross_subnet_pivot_routed` | `$d = New-CimSession -ComputerName win7 -Credential fred -SessionOption $dopt` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `get-ciminstance` | `s_passive_topology_mapped` | `Get-CimInstance Win32_Service -Filter "State='Running'"` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `get-ciminstance` | `s_credentials_or_certs_acquired` | `Get-CimInstance -query "select * from Win32_Service where startmode='disabled'" \| select name` |
| `s_firewall_or_acl_unlocked` | **`Lateral_Movement_Routing_Pivot`** | Remote Host Execution, L2/L3 Route Injection & Subnet Pivot | `get-wmiobject` | `s_cross_subnet_pivot_routed` | `$appToRemove = Get-WmiObject Win32_Product -computername win7 -credential $c -Filter "Name like '%Helper'"` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `get-ciminstance` | `s_passive_topology_mapped` | `Get-CimInstance -ClassName Win32_Service -filter "State like 'Running'" \| select name` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `get-credential` | `s_credentials_or_certs_acquired` | `$c = Get-Credential` |
| `s_firewall_or_acl_unlocked` | **`Lateral_Movement_Routing_Pivot`** | Remote Host Execution, L2/L3 Route Injection & Subnet Pivot | `get-wmiobject` | `s_cross_subnet_pivot_routed` | `(Get-WmiObject Win32_Product -computername win7 -credential $c -filter "Name like '%Helper'").Uninstall()` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `get-ciminstance` | `s_passive_topology_mapped` | `Get-CimInstance -ClassName Win32_bios \| Get-Member` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `get-credential` | `s_credentials_or_certs_acquired` | `$p = Get-Credential` |
| `s_firewall_or_acl_unlocked` | **`Lateral_Movement_Routing_Pivot`** | Remote Host Execution, L2/L3 Route Injection & Subnet Pivot | `get-wmiobject` | `s_cross_subnet_pivot_routed` | `Get-WmiObject Win32_Product -computername Win7 -credential $c -Filter "Name like '%Helper'"` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `get-ciminstance` | `s_credentials_or_certs_acquired` | `Get-CimInstance Win32_Process -Filter "Name='Spooler'"` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `get-ciminstance` | `s_credentials_or_certs_acquired` | `$service = Get-CimInstance Win32_Process -Filter "Name='Spooler'"` |

## Verified Executable Commands (Grouped by Capability Layer)

### General_System (17 commands)
```bash
Get-CimInstance Win32_Process
Get-CimInstance Win32_bios
Get-CimInstance Win32_Service -Filter "State='Running'"
Get-CimInstance -ClassName Win32_Service -filter "State like 'Running'" | select name
Get-CimClass | Where {$_.CimClassName -match 'User'}
Get-CimInstance -ClassName Win32_bios | Get-Member
$c = New-CimSession -ComputerName win10 -Credential fred
$dopt = New-CimSessionOption -Protocol Dcom
$d = New-CimSession -ComputerName win7 -Credential fred -SessionOption $dopt
Get-CimInstance -query "select * from Win32_Service where startmode='disabled'" | select name
$c = Get-Credential
$p = Get-Credential
$appToRemove = Get-WmiObject Win32_Product -computername win7 -credential $c -Filter "Name like '%Helper'"
(Get-WmiObject Win32_Product -computername win7 -credential $c -filter "Name like '%Helper'").Uninstall()
Get-WmiObject Win32_Product -computername Win7 -credential $c -Filter "Name like '%Helper'"
Get-CimInstance Win32_Process -Filter "Name='Spooler'"
$service = Get-CimInstance Win32_Process -Filter "Name='Spooler'"
```

