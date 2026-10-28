---
title: "Trained Command Playbook: CQC001_E010_M060_Spanning_Tree_Protocol.pdf"
tags:
  - enumeration
  - mdp
  - pdf
  - trained
  - vlan
source_file: CQC001_E010_M060_Spanning_Tree_Protocol.pdf
updated: 2026-10-24 00:57:30
---

# Trained Command Playbook: `CQC001_E010_M060_Spanning_Tree_Protocol.pdf`

- **Source Document:** `~/Projects/CORA/Training/CQC001_E010_M060_Spanning_Tree_Protocol.pdf`
- **CEGAR Verified Commands:** `1` (`0` malformed/unsafe snippets filtered)
- **MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`):** `1`
- **Discovered IPs/Subnets:** `None`
- **Discovered Interfaces:** `None`
- **Related Knowledge Note:** [[knowledge/trained_cqc001_e010_m060_spanning_tree_protocol]]

## Distilled MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`)
| Pre-State ($s$) | Tactic ($\tau$) | Technique ($k$) | Tool ($u$) | Post-State ($s'$) | Verified Command ($c$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `interface` | `s_active_services_enumerated` | `interface FastEthernet0/1` |

## Verified Executable Commands (Grouped by Capability Layer)

### General_System (1 commands)
```bash
interface FastEthernet0/1
```

