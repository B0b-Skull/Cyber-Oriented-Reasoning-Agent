---
title: "Trained Command Playbook: CQC001_E010_M010_Network_Traffic_Monitoring.pdf"
tags:
  - https
  - mdp
  - passive_enum
  - pdf
  - trained
source_file: CQC001_E010_M010_Network_Traffic_Monitoring.pdf
updated: 2026-10-25 00:57:12
---

# Trained Command Playbook: `CQC001_E010_M010_Network_Traffic_Monitoring.pdf`

- **Source Document:** `~/Projects/CORA/Training/CQC001_E010_M010_Network_Traffic_Monitoring.pdf`
- **CEGAR Verified Commands:** `1` (`0` malformed/unsafe snippets filtered)
- **MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`):** `1`
- **Discovered IPs/Subnets:** `172.16.1.84, 172.16.1.85, 172.16.1.86, 172.16.10.2`
- **Discovered Interfaces:** `None`
- **Related Knowledge Note:** [[knowledge/trained_cqc001_e010_m010_network_traffic_monitoring]]

## Distilled MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`)
| Pre-State ($s$) | Tactic ($\tau$) | Technique ($k$) | Tool ($u$) | Post-State ($s'$) | Verified Command ($c$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `ip` | `s_passive_topology_mapped` | `ip flow-top-talkers` |

## Verified Executable Commands (Grouped by Capability Layer)

### L3_Routing_NAT (1 commands)
```bash
ip flow-top-talkers
```

