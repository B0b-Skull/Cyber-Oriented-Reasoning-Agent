---
title: "Trained Command Playbook: Metro Ethernet Training_Part_1.pdf"
tags:
  - arp
  - enumeration
  - http
  - https
  - mdp
  - passive_enum
  - pdf
  - ssl
  - tls
  - trained
  - vlan
source_file: Metro Ethernet Training_Part_1.pdf
updated: 2026-10-25 00:59:10
---

# Trained Command Playbook: `Metro Ethernet Training_Part_1.pdf`

- **Source Document:** `~/Projects/CORA/Training/Metro Ethernet Training_Part_1.pdf`
- **CEGAR Verified Commands:** `4` (`0` malformed/unsafe snippets filtered)
- **MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`):** `4`
- **Discovered IPs/Subnets:** `1.0.0.0, 1.1.1.2/32, 1.1.1.4/32, 10.0.0.0/30, 127.255.255.255, 128.0.0.0, 191.255.255.255, 192.0.0.0, 223.255.255.255, 224.0.0.0, 239.255.255.255, 240.0.0.0, 255.255.255.255, 6.3.1.2`
- **Discovered Interfaces:** `LO, Lo`
- **Related Knowledge Note:** [[knowledge/trained_metro_ethernet_training_part_1]]

## Distilled MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`)
| Pre-State ($s$) | Tactic ($\tau$) | Technique ($k$) | Tool ($u$) | Post-State ($s'$) | Verified Command ($c$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `locate` | `s_active_services_enumerated` | `Locate the aggregation switch close to the building entry point (e.g. fiber panel)` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `ip` | `s_passive_topology_mapped` | `IP Address` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `locate` | `s_active_services_enumerated` | `Locate edge switches close to users (e.g. one per floor)` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `out-of-band` | `s_active_services_enumerated` | `Out-of-band OAM not reflective of the data plane` |

## Verified Executable Commands (Grouped by Capability Layer)

### General_System (3 commands)
```bash
Locate the aggregation switch close to the building entry point (e.g. fiber panel)
Locate edge switches close to users (e.g. one per floor)
Out-of-band OAM not reflective of the data plane
```

### L3_Routing_NAT (1 commands)
```bash
IP Address
```

