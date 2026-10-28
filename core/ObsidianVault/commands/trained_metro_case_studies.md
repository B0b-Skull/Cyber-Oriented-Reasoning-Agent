---
title: "Trained Command Playbook: metro case studies.pdf"
tags:
  - enumeration
  - mdp
  - pdf
  - responder
  - trained
  - vlan
source_file: metro case studies.pdf
updated: 2026-10-24 00:58:57
---

# Trained Command Playbook: `metro case studies.pdf`

- **Source Document:** `~/Projects/CORA/Training/metro case studies.pdf`
- **CEGAR Verified Commands:** `1` (`0` malformed/unsafe snippets filtered)
- **MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`):** `1`
- **Discovered IPs/Subnets:** `None`
- **Discovered Interfaces:** `LO`
- **Related Knowledge Note:** [[knowledge/trained_metro_case_studies]]

## Distilled MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`)
| Pre-State ($s$) | Tactic ($\tau$) | Technique ($k$) | Tool ($u$) | Post-State ($s'$) | Verified Command ($c$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `find` | `s_active_services_enumerated` | `Find access/` |

## Verified Executable Commands (Grouped by Capability Layer)

### General_System (1 commands)
```bash
Find access/
```

