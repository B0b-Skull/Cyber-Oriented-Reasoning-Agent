---
title: "Trained Command Playbook: Tasklist.pdf"
tags:
  - credential_access
  - https
  - lateral_movement_routing_pivot
  - mdp
  - passive_enum
  - pdf
  - trained
source_file: Tasklist.pdf
updated: 2026-10-25 01:00:39
---

# Trained Command Playbook: `Tasklist.pdf`

- **Source Document:** `~/Projects/CORA/Training/Tasklist.pdf`
- **CEGAR Verified Commands:** `7` (`0` malformed/unsafe snippets filtered)
- **MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`):** `7`
- **Discovered IPs/Subnets:** `None`
- **Discovered Interfaces:** `None`
- **Related Knowledge Note:** [[knowledge/trained_tasklist]]

## Distilled MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`)
| Pre-State ($s$) | Tactic ($\tau$) | Technique ($k$) | Tool ($u$) | Post-State ($s'$) | Verified Command ($c$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `tasklist` | `s_credentials_or_certs_acquired` | `Tasklist` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `tasklist` | `s_passive_topology_mapped` | `tasklist /v /fi "PID gt 1000" /fo csv` |
| `s_firewall_or_acl_unlocked` | **`Lateral_Movement_Routing_Pivot`** | Remote Host Execution, L2/L3 Route Injection & Subnet Pivot | `tasklist` | `s_cross_subnet_pivot_routed` | `tasklist /s srvmain /nh` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `tasklist` | `s_passive_topology_mapped` | `tasklist /fi "USERNAME ne NT AUTHORITY\SYSTEM" /fi "STATUS eq running"` |
| `s_firewall_or_acl_unlocked` | **`Lateral_Movement_Routing_Pivot`** | Remote Host Execution, L2/L3 Route Injection & Subnet Pivot | `tasklist` | `s_cross_subnet_pivot_routed` | `tasklist /s srvmain /s srvny` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `tasklist` | `s_passive_topology_mapped` | `tasklist /v /fi "STATUS eq running"` |
| `s_firewall_or_acl_unlocked` | **`Lateral_Movement_Routing_Pivot`** | Remote Host Execution, L2/L3 Route Injection & Subnet Pivot | `tasklist` | `s_cross_subnet_pivot_routed` | `tasklist /s srvmain /u maindom\hiropln /p p@ssW23 /nh` |

## Verified Executable Commands (Grouped by Capability Layer)

### General_System (7 commands)
```bash
Tasklist
tasklist /v /fi "PID gt 1000" /fo csv
tasklist /fi "USERNAME ne NT AUTHORITY\SYSTEM" /fi "STATUS eq running"
tasklist /v /fi "STATUS eq running"
tasklist /s srvmain /nh
tasklist /s srvmain /s srvny
tasklist /s srvmain /u maindom\hiropln /p p@ssW23 /nh
```

