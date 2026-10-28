---
title: "Trained Command Playbook: BFP-Fexible Packet Filtering.pdf"
tags:
  - http
  - iptables
  - mdp
  - passive_enum
  - pdf
  - ssh
  - trained
source_file: BFP-Fexible Packet Filtering.pdf
updated: 2026-10-24 00:57:01
---

# Trained Command Playbook: `BFP-Fexible Packet Filtering.pdf`

- **Source Document:** `~/Projects/CORA/Training/BFP-Fexible Packet Filtering.pdf`
- **CEGAR Verified Commands:** `1` (`0` malformed/unsafe snippets filtered)
- **MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`):** `1`
- **Discovered IPs/Subnets:** `172.24.1.10, 172.24.1.15`
- **Discovered Interfaces:** `lo`
- **Related Knowledge Note:** [[knowledge/trained_bfp-fexible_packet_filtering]]

## Distilled MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`)
| Pre-State ($s$) | Tactic ($\tau$) | Technique ($k$) | Tool ($u$) | Post-State ($s'$) | Verified Command ($c$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `ip` | `s_passive_topology_mapped` | `IP address for which the connection request was origi-` |

## Verified Executable Commands (Grouped by Capability Layer)

### L3_Routing_NAT (1 commands)
```bash
IP address for which the connection request was origi-
```

