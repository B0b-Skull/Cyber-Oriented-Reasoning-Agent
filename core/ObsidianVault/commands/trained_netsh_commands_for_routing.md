---
title: "Trained Command Playbook: Netsh commands for Routing.pdf"
tags:
  - enumeration
  - https
  - mdp
  - netsh
  - passive_enum
  - pdf
  - trained
source_file: Netsh commands for Routing.pdf
updated: 2026-10-25 00:59:23
---

# Trained Command Playbook: `Netsh commands for Routing.pdf`

- **Source Document:** `~/Projects/CORA/Training/Netsh commands for Routing.pdf`
- **CEGAR Verified Commands:** `16` (`0` malformed/unsafe snippets filtered)
- **MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`):** `16`
- **Discovered IPs/Subnets:** `0.0.0.0, 10.0.0.2, 10.10.1.100, 10.10.10.0, 10.10.10.1, 10.11.11.1, 10.11.21.154, <LOCAL_HOST_IP>, 255.255.255.0`
- **Discovered Interfaces:** `None`
- **Related Knowledge Note:** [[knowledge/trained_netsh_commands_for_routing]]

## Distilled MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`)
| Pre-State ($s$) | Tactic ($\tau$) | Technique ($k$) | Tool ($u$) | Post-State ($s'$) | Verified Command ($c$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `netsh` | `s_active_services_enumerated` | `Netsh commands for Routing` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `ip` | `s_passive_topology_mapped` | `IP address, and the second address is for the high IP address to use in building the filter.` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `netsh` | `s_active_services_enumerated` | `Netsh Routing IP IGMP commands` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `ip` | `s_passive_topology_mapped` | `IP address, and the second address is for the high IP address used in building the filter.` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `netsh` | `s_active_services_enumerated` | `Netsh Routing IP Routerdiscovery commands` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `netsh` | `s_active_services_enumerated` | `Netsh Routing IP RIP commands` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `netsh` | `s_active_services_enumerated` | `Netsh Routing IP Relay commands` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `netsh` | `s_active_services_enumerated` | `Netsh Routing IP OSPF commands` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `netsh` | `s_active_services_enumerated` | `Netsh Routing IP Autodhcp commands` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `netsh` | `s_active_services_enumerated` | `Netsh Routing IP Dnsproxy commands` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `netsh` | `s_active_services_enumerated` | `Netsh Routing IP NAT commands` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `netsh` | `s_active_services_enumerated` | `Netsh Routing IPX commands` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `netsh` | `s_active_services_enumerated` | `Netsh Routing IPX NetBIOS commands` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `netsh` | `s_active_services_enumerated` | `Netsh Routing IPX RIP commands` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `netsh` | `s_active_services_enumerated` | `Netsh Routing IPX SAP commands` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `netsh` | `s_active_services_enumerated` | `Netsh Routing example` |

## Verified Executable Commands (Grouped by Capability Layer)

### L3_Routing_NAT (16 commands)
```bash
Netsh commands for Routing
Netsh Routing IP IGMP commands
Netsh Routing IP Routerdiscovery commands
Netsh Routing IP RIP commands
IP address, and the second address is for the high IP address to use in building the filter.
IP address, and the second address is for the high IP address used in building the filter.
Netsh Routing IP Relay commands
Netsh Routing IP OSPF commands
Netsh Routing IP Autodhcp commands
Netsh Routing IP Dnsproxy commands
Netsh Routing IP NAT commands
Netsh Routing IPX commands
Netsh Routing IPX NetBIOS commands
Netsh Routing IPX RIP commands
Netsh Routing IPX SAP commands
Netsh Routing example
```

