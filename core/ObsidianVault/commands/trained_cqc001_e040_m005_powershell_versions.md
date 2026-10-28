---
title: "Trained Command Playbook: CQC001_E040_M005_PowerShell_Versions.pdf"
tags:
  - enumeration
  - mdp
  - passive_enum
  - pdf
  - powershell
  - trained
source_file: CQC001_E040_M005_PowerShell_Versions.pdf
updated: 2026-10-23 22:55:15
---

# Trained Command Playbook: `CQC001_E040_M005_PowerShell_Versions.pdf`

- **Source Document:** `~/Projects/CORA/Training/CQC001_E040_M005_PowerShell_Versions.pdf`
- **CEGAR Verified Commands:** `2` (`0` malformed/unsafe snippets filtered)
- **MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`):** `2`
- **Discovered IPs/Subnets:** `None`
- **Discovered Interfaces:** `None`
- **Related Knowledge Note:** [[knowledge/trained_cqc001_e040_m005_powershell_versions]]

## Distilled MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`)
| Pre-State ($s$) | Tactic ($\tau$) | Technique ($k$) | Tool ($u$) | Post-State ($s'$) | Verified Command ($c$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `powershell` | `s_active_services_enumerated` | `PowerShell Versions` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Process, Registry, File & Socket Survey | `date` | `s_passive_topology_mapped` | `Date` |

## Verified Executable Commands (Grouped by Capability Layer)

### General_System
```bash
PowerShell Versions
Date
```

