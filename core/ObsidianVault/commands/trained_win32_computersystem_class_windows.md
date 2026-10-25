---
title: "Trained Command Playbook: Win32_ComputerSystem class (Windows).pdf"
tags:
  - bcdedit
  - enumeration
  - https
  - mdp
  - pdf
  - trained
source_file: Win32_ComputerSystem class (Windows).pdf
updated: 2026-10-25 23:11:19
---

# Trained Command Playbook: `Win32_ComputerSystem class (Windows).pdf`

- **Source Document:** `~/Projects/CORA/Training/Win32_ComputerSystem class (Windows).pdf`
- **CEGAR Verified Commands:** `1` (`0` malformed/unsafe snippets filtered)
- **MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`):** `1`
- **Discovered IPs/Subnets:** `None`
- **Discovered Interfaces:** `None`
- **Related Knowledge Note:** [[knowledge/trained_win32_computersystem_class_windows]]

## Distilled MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`)
| Pre-State ($s$) | Tactic ($\tau$) | Technique ($k$) | Tool ($u$) | Post-State ($s'$) | Verified Command ($c$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `service` | `s_active_services_enumerated` | `Service ﴾"Service"﴿` |

## Verified Executable Commands (Grouped by Capability Layer)

### General_System
```bash
Service ﴾"Service"﴿
```

