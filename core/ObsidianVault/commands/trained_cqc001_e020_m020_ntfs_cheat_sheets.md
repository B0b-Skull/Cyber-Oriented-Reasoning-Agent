---
title: "Trained Command Playbook: CQC001_E020_M020_NTFS_Cheat_Sheets.pdf"
tags:
  - enumeration
  - http
  - mdp
  - pdf
  - post_exploitation_verification
  - serial
  - trained
source_file: CQC001_E020_M020_NTFS_Cheat_Sheets.pdf
updated: 2026-10-24 00:57:31
---

# Trained Command Playbook: `CQC001_E020_M020_NTFS_Cheat_Sheets.pdf`

- **Source Document:** `~/Projects/CORA/Training/CQC001_E020_M020_NTFS_Cheat_Sheets.pdf`
- **CEGAR Verified Commands:** `2` (`0` malformed/unsafe snippets filtered)
- **MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`):** `2`
- **Discovered IPs/Subnets:** `None`
- **Discovered Interfaces:** `None`
- **Related Knowledge Note:** [[knowledge/trained_cqc001_e020_m020_ntfs_cheat_sheets]]

## Distilled MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`)
| Pre-State ($s$) | Tactic ($\tau$) | Technique ($k$) | Tool ($u$) | Post-State ($s'$) | Verified Command ($c$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `attrib` | `s_active_services_enumerated` | `Attrib ID` |
| `s_cross_subnet_pivot_routed` | **`Post_Exploitation_Verification`** | Post-Action Host Identity, Privilege & Objective Verification | `attrib` | `s_goal_verified_complete` | `Attrib ID starts from zero` |

## Verified Executable Commands (Grouped by Capability Layer)

### General_System (2 commands)
```bash
Attrib ID
Attrib ID starts from zero
```

