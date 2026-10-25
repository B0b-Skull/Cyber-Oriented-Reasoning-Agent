---
title: "Trained Command Playbook: Metro Ethernet Training_Day_2_MPLS.pdf"
tags:
  - enumeration
  - eth0
  - eth1
  - mdp
  - passive_enum
  - pdf
  - trained
source_file: Metro Ethernet Training_Day_2_MPLS.pdf
updated: 2026-10-25 00:59:01
---

# Trained Command Playbook: `Metro Ethernet Training_Day_2_MPLS.pdf`

- **Source Document:** `~/Projects/CORA/Training/Metro Ethernet Training_Day_2_MPLS.pdf`
- **CEGAR Verified Commands:** `4` (`0` malformed/unsafe snippets filtered)
- **MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`):** `4`
- **Discovered IPs/Subnets:** `10.1.0.0/24, 10.1.2.0/24, 10.2.1.0/24, 10.2.12.0/24, 10.22.12.0/24, 10.3.0.0/16, 10.3.1.0/24, 10.3.3.0/24, 10.4.12.0/24, 134.5.1.5, 134.5.6.1, 137.204.0.0/16, 149.27.2.0/24, 149.27.2.27, 172.16.1.0, 172.26.1.0, 192.4.2.10, 197.26.15.0/24, 197.26.15.1, 197.26.15.1/32, 20.1.0.0/16, 20.2.0.0/16, 20.2.1.0/28, 20.2.1.2, 20.2.1.2/28, 200.3.2.1, 200.3.2.7, 30.0.0.2, 30.1.1.0/28, 47.1.1.1`
- **Discovered Interfaces:** `eth0, eth1`
- **Related Knowledge Note:** [[knowledge/trained_metro_ethernet_training_day_2_mpls]]

## Distilled MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`)
| Pre-State ($s$) | Tactic ($\tau$) | Technique ($k$) | Tool ($u$) | Post-State ($s'$) | Verified Command ($c$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `ip` | `s_passive_topology_mapped` | `IP address (too long, has fields)` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `new-generation` | `s_active_services_enumerated` | `NEW-GENERATION ROUTER ARCHITECTURE` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `ip` | `s_passive_topology_mapped` | `IP address lookup` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `ip` | `s_passive_topology_mapped` | `IP address lookup is usually one the most common bottlenecks in high performance` |

## Verified Executable Commands (Grouped by Capability Layer)

### General_System (1 commands)
```bash
NEW-GENERATION ROUTER ARCHITECTURE
```

### L3_Routing_NAT (3 commands)
```bash
IP address (too long, has fields)
IP address lookup
IP address lookup is usually one the most common bottlenecks in high performance
```

