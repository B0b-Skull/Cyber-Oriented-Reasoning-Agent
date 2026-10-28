---
title: "Trained Command Playbook: CBM_1_2_2006_Goppit_PE_Format_Reverse_Engineer_View.pdf"
tags:
  - enumeration
  - http
  - mdp
  - passive_enum
  - pdf
  - tls
  - trained
source_file: CBM_1_2_2006_Goppit_PE_Format_Reverse_Engineer_View.pdf
updated: 2026-10-23 22:54:42
---

# Trained Command Playbook: `CBM_1_2_2006_Goppit_PE_Format_Reverse_Engineer_View.pdf`

- **Source Document:** `~/Projects/CORA/Training/CBM_1_2_2006_Goppit_PE_Format_Reverse_Engineer_View.pdf`
- **CEGAR Verified Commands:** `5` (`0` malformed/unsafe snippets filtered)
- **MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`):** `5`
- **Discovered IPs/Subnets:** `None`
- **Discovered Interfaces:** `None`
- **Related Knowledge Note:** [[knowledge/trained_cbm_1_2_2006_goppit_pe_format_reverse_engineer_view]]

## Distilled MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`)
| Pre-State ($s$) | Tactic ($\tau$) | Technique ($k$) | Tool ($u$) | Post-State ($s'$) | Verified Command ($c$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `export` | `s_active_services_enumerated` | `Export data` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `export` | `s_active_services_enumerated` | `Export Name Table (ENT).` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `export` | `s_active_services_enumerated` | `Export Forwarding` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `copy` | `s_active_services_enumerated` | `copy and relocate it somewhere there is space.` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Process, Registry, File & Socket Survey | `type` | `s_passive_topology_mapped` | `type "upx basecalc.exe":` |

## Verified Executable Commands (Grouped by Capability Layer)

### General_System
```bash
Export data
Export Name Table (ENT).
Export Forwarding
copy and relocate it somewhere there is space.
type "upx basecalc.exe":
```

