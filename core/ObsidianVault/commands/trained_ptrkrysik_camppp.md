---
title: "Trained Command Playbook: ptrkrysik_camppp.pdf"
tags:
  - enumeration
  - https
  - mdp
  - pdf
  - post_exploitation_verification
  - trained
  - wireshark
source_file: ptrkrysik_camppp.pdf
updated: 2026-10-25 01:00:14
---

# Trained Command Playbook: `ptrkrysik_camppp.pdf`

- **Source Document:** `~/Projects/CORA/Training/ptrkrysik_camppp.pdf`
- **CEGAR Verified Commands:** `2` (`0` malformed/unsafe snippets filtered)
- **MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`):** `2`
- **Discovered IPs/Subnets:** `None`
- **Discovered Interfaces:** `None`
- **Related Knowledge Note:** [[knowledge/trained_ptrkrysik_camppp]]

## Distilled MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`)
| Pre-State ($s$) | Tactic ($\tau$) | Technique ($k$) | Tool ($u$) | Post-State ($s'$) | Verified Command ($c$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `s_cross_subnet_pivot_routed` | **`Post_Exploitation_Verification`** | Post-Action Host Identity, Privilege & Objective Verification | `whoami` | `s_goal_verified_complete` | `whoami` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `out-of-tree` | `s_active_services_enumerated` | `Out-of-tree GNU Radio module` |

## Verified Executable Commands (Grouped by Capability Layer)

### General_System (2 commands)
```bash
whoami
Out-of-tree GNU Radio module
```

