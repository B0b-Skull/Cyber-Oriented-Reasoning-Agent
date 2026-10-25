---
title: "Trained Command Playbook: WiFi_Handbook_1.pdf"
tags:
  - enumeration
  - mdp
  - passive_enum
  - pdf
  - trained
source_file: WiFi_Handbook_1.pdf
updated: 2026-10-25 23:10:51
---

# Trained Command Playbook: `WiFi_Handbook_1.pdf`

- **Source Document:** `~/Projects/CORA/Training/WiFi_Handbook_1.pdf`
- **CEGAR Verified Commands:** `3` (`0` malformed/unsafe snippets filtered)
- **MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`):** `3`
- **Discovered IPs/Subnets:** `None`
- **Discovered Interfaces:** `None`
- **Related Knowledge Note:** [[knowledge/trained_wifi_handbook_1]]

## Distilled MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`)
| Pre-State ($s$) | Tactic ($\tau$) | Technique ($k$) | Tool ($u$) | Post-State ($s'$) | Verified Command ($c$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Process, Registry, File & Socket Survey | `service` | `s_passive_topology_mapped` | `service connections and tandem offices are used for long-distance` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `service` | `s_active_services_enumerated` | `service providers in the United States. The bandwidth glut of 2000` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `service` | `s_active_services_enumerated` | `service provider. Some entity must go out of business before a tech-` |

## Verified Executable Commands (Grouped by Capability Layer)

### General_System
```bash
service connections and tandem offices are used for long-distance
service providers in the United States. The bandwidth glut of 2000
service provider. Some entity must go out of business before a tech-
```

