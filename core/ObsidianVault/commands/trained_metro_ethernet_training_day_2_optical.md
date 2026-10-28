---
title: "Trained Command Playbook: Metro Ethernet Training_Day_2_Optical.pdf"
tags:
  - enumeration
  - mdp
  - pdf
  - trained
source_file: Metro Ethernet Training_Day_2_Optical.pdf
updated: 2026-10-23 22:58:08
---

# Trained Command Playbook: `Metro Ethernet Training_Day_2_Optical.pdf`

- **Source Document:** `~/Projects/CORA/Training/Metro Ethernet Training_Day_2_Optical.pdf`
- **CEGAR Verified Commands:** `1` (`0` malformed/unsafe snippets filtered)
- **MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`):** `1`
- **Discovered IPs/Subnets:** `None`
- **Discovered Interfaces:** `None`
- **Related Knowledge Note:** [[knowledge/trained_metro_ethernet_training_day_2_optical]]

## Distilled MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`)
| Pre-State ($s$) | Tactic ($\tau$) | Technique ($k$) | Tool ($u$) | Post-State ($s'$) | Verified Command ($c$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `service` | `s_active_services_enumerated` | `Service Mux` |

## Verified Executable Commands (Grouped by Capability Layer)

### General_System
```bash
Service Mux
```

