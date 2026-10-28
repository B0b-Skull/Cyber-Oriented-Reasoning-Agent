---
title: "Trained Command Playbook: Find.pdf"
tags:
  - enumeration
  - https
  - mdp
  - passive_enum
  - pdf
  - trained
source_file: Find.pdf
updated: 2026-10-24 00:58:23
---

# Trained Command Playbook: `Find.pdf`

- **Source Document:** `~/Projects/CORA/Training/Find.pdf`
- **CEGAR Verified Commands:** `4` (`0` malformed/unsafe snippets filtered)
- **MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`):** `4`
- **Discovered IPs/Subnets:** `None`
- **Discovered Interfaces:** `None`
- **Related Knowledge Note:** [[knowledge/trained_find]]

## Distilled MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`)
| Pre-State ($s$) | Tactic ($\tau$) | Technique ($k$) | Tool ($u$) | Post-State ($s'$) | Verified Command ($c$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `find` | `s_active_services_enumerated` | `find [/v] [/c] [/n] [/i] "string" [[Drive:][Path]FileName[...]]` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `dir` | `s_passive_topology_mapped` | `dir c:\ /s /b \| find "CPU"` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `find` | `s_active_services_enumerated` | `find "Pencil Sharpener" pencil.ad` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `find` | `s_active_services_enumerated` | `find "The scientists labeled their paper ""for discussion only."" It is not a final report." report.doc` |

## Verified Executable Commands (Grouped by Capability Layer)

### General_System (4 commands)
```bash
find [/v] [/c] [/n] [/i] "string" [[Drive:][Path]FileName[...]]
find "Pencil Sharpener" pencil.ad
find "The scientists labeled their paper ""for discussion only."" It is not a final report." report.doc
dir c:\ /s /b | find "CPU"
```

