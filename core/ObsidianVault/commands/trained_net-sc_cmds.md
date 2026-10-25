---
title: "Trained Command Playbook: Net-SC CMDs.txt"
tags:
  - defense_evasion_firewall
  - enumeration
  - lateral_movement_routing_pivot
  - mdp
  - passive_enum
  - privilege_escalation
  - text
  - trained
source_file: Net-SC CMDs.txt
updated: 2026-10-25 00:59:23
---

# Trained Command Playbook: `Net-SC CMDs.txt`

- **Source Document:** `~/Projects/CORA/Training/Net-SC CMDs.txt`
- **CEGAR Verified Commands:** `25` (`0` malformed/unsafe snippets filtered)
- **MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`):** `25`
- **Discovered IPs/Subnets:** `None`
- **Discovered Interfaces:** `None`
- **Related Knowledge Note:** [[knowledge/trained_net-sc_cmds]]

## Distilled MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`)
| Pre-State ($s$) | Tactic ($\tau$) | Technique ($k$) | Tool ($u$) | Post-State ($s'$) | Verified Command ($c$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `driverquery` | `s_firewall_or_acl_unlocked` | `driverquery /si \| findstr "Security Driver"` |
| `s_firewall_or_acl_unlocked` | **`Lateral_Movement_Routing_Pivot`** | Remote Host Execution, L2/L3 Route Injection & Subnet Pivot | `sc` | `s_cross_subnet_pivot_routed` | `sc \\xp.ops.local getkeyname "Windows Firewall/Internet Connection Sharing (ICS)"` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `net` | `s_passive_topology_mapped` | `net start umrdpservice` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `sc` | `s_interactive_tty_or_priv_escalated` | `sc config spooler start= disabled` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `net` | `s_active_services_enumerated` | `net stop your_service` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `driverquery` | `s_firewall_or_acl_unlocked` | `driverquery /si \| findstr "TRUE"` |
| `s_firewall_or_acl_unlocked` | **`Lateral_Movement_Routing_Pivot`** | Remote Host Execution, L2/L3 Route Injection & Subnet Pivot | `sc` | `s_cross_subnet_pivot_routed` | `sc \\xp.ops.local query state= all` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `sc` | `s_passive_topology_mapped` | `sc qc Netman` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `sc` | `s_interactive_tty_or_priv_escalated` | `sc config w32time start= auto` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `net` | `s_active_services_enumerated` | `net pause your_service` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `net` | `s_firewall_or_acl_unlocked` | `net start "Print Spooler"` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `driverquery` | `s_passive_topology_mapped` | `Driverquery` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `sc` | `s_interactive_tty_or_priv_escalated` | `sc config Netlogon start= disabled` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `net` | `s_active_services_enumerated` | `net continue your_service` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `net` | `s_firewall_or_acl_unlocked` | `net start "Remote Registry"` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `net` | `s_passive_topology_mapped` | `net start your_service` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `net` | `s_firewall_or_acl_unlocked` | `net continue telnet` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `sc` | `s_firewall_or_acl_unlocked` | `sc query \| findstr "Time"` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `sc` | `s_firewall_or_acl_unlocked` | `sc queryex type= service state= all \| find /i "Time"` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `sc` | `s_firewall_or_acl_unlocked` | `sc qc LanmanWorkstation` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `sc` | `s_firewall_or_acl_unlocked` | `sc start` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `sc` | `s_firewall_or_acl_unlocked` | `sc stop` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `sc` | `s_firewall_or_acl_unlocked` | `sc stop audiosrv` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `net` | `s_firewall_or_acl_unlocked` | `net stop audiosrv` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `sc` | `s_firewall_or_acl_unlocked` | `sc start umrdpservice` |

## Verified Executable Commands (Grouped by Capability Layer)

### General_System (25 commands)
```bash
driverquery /si | findstr "Security Driver"
driverquery /si | findstr "TRUE"
net start "Print Spooler"
net start "Remote Registry"
net continue telnet
sc \\xp.ops.local getkeyname "Windows Firewall/Internet Connection Sharing (ICS)"
sc \\xp.ops.local query state= all
sc query | findstr "Time"
sc queryex type= service state= all | find /i "Time"
sc qc LanmanWorkstation
sc start
sc stop
sc stop audiosrv
net stop audiosrv
sc start umrdpservice
net start umrdpservice
sc config spooler start= disabled
sc config w32time start= auto
sc qc Netman
sc config Netlogon start= disabled
Driverquery
net stop your_service
net start your_service
net pause your_service
net continue your_service
```

