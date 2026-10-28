---
title: "Trained Command Playbook: Using Netsh.pdf"
tags:
  - enumeration
  - https
  - mdp
  - netsh
  - passive_enum
  - pdf
  - trained
source_file: Using Netsh.pdf
updated: 2026-10-24 01:01:10
---

# Trained Command Playbook: `Using Netsh.pdf`

- **Source Document:** `~/Projects/CORA/Training/Using Netsh.pdf`
- **CEGAR Verified Commands:** `12` (`0` malformed/unsafe snippets filtered)
- **MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`):** `12`
- **Discovered IPs/Subnets:** `10.0.0.1, 10.0.0.9, 255.0.0.0`
- **Discovered Interfaces:** `None`
- **Related Knowledge Note:** [[knowledge/trained_using_netsh]]

## Distilled MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`)
| Pre-State ($s$) | Tactic ($\tau$) | Technique ($k$) | Tool ($u$) | Post-State ($s'$) | Verified Command ($c$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `netsh` | `s_active_services_enumerated` | `Netsh contexts` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `prompt` | `s_passive_topology_mapped` | `prompt (that is, netsh>). To run these Netsh commands on a remote Windows 2000 Server, you must first use` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `netsh` | `s_active_services_enumerated` | `Netsh interacts with other operating system components using dynamic­link library (DLL) files. Each Netsh` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `netsh` | `s_active_services_enumerated` | `Netsh commands for AAAA` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `netsh` | `s_active_services_enumerated` | `Netsh commands for DHCP` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `netsh` | `s_active_services_enumerated` | `Netsh diagnostic (diag) commands` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `netsh` | `s_active_services_enumerated` | `Netsh commands for Interface IP` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `netsh` | `s_active_services_enumerated` | `Netsh commands for RAS` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `netsh` | `s_active_services_enumerated` | `Netsh commands for Routing` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `netsh` | `s_active_services_enumerated` | `Netsh commands for WINS` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `netsh` | `s_active_services_enumerated` | `netsh [­a AliasFile] [­c Context] [­r RemoteComputer] [{NetshCommand\|­f ScriptFile}]` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `netsh` | `s_active_services_enumerated` | `netsh interface ip>` |

## Verified Executable Commands (Grouped by Capability Layer)

### General_System (1 commands)
```bash
prompt (that is, netsh>). To run these Netsh commands on a remote Windows 2000 Server, you must first use
```

### L3_Routing_NAT (11 commands)
```bash
Netsh contexts
Netsh interacts with other operating system components using dynamic­link library (DLL) files. Each Netsh
Netsh commands for AAAA
Netsh commands for DHCP
Netsh diagnostic (diag) commands
Netsh commands for Interface IP
Netsh commands for RAS
Netsh commands for Routing
Netsh commands for WINS
netsh [­a AliasFile] [­c Context] [­r RemoteComputer] [{NetshCommand|­f ScriptFile}]
netsh interface ip>
```

