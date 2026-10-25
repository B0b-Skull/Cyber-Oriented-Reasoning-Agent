---
title: "Trained Command Playbook: CQC001_E020_M030_Boot_and_Logon_Resource_-_Windows_XP_-_2003.pdf"
tags:
  - enumeration
  - mdp
  - pdf
  - trained
source_file: CQC001_E020_M030_Boot_and_Logon_Resource_-_Windows_XP_-_2003.pdf
updated: 2026-10-25 22:54:58
---

# Trained Command Playbook: `CQC001_E020_M030_Boot_and_Logon_Resource_-_Windows_XP_-_2003.pdf`

- **Source Document:** `~/Projects/CORA/Training/CQC001_E020_M030_Boot_and_Logon_Resource_-_Windows_XP_-_2003.pdf`
- **CEGAR Verified Commands:** `1` (`0` malformed/unsafe snippets filtered)
- **MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`):** `1`
- **Discovered IPs/Subnets:** `None`
- **Discovered Interfaces:** `None`
- **Related Knowledge Note:** [[knowledge/trained_cqc001_e020_m030_boot_and_logon_resource_-_windows_xp_-_2003]]

## Distilled MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`)
| Pre-State ($s$) | Tactic ($\tau$) | Technique ($k$) | Tool ($u$) | Post-State ($s'$) | Verified Command ($c$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `service` | `s_active_services_enumerated` | `Service Control Manager (SCM) - loads and initializes AUTO_START` |

## Verified Executable Commands (Grouped by Capability Layer)

### General_System
```bash
Service Control Manager (SCM) - loads and initializes AUTO_START
```

