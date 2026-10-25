---
title: "Trained Command Playbook: Type.pdf"
tags:
  - https
  - mdp
  - passive_enum
  - pdf
  - trained
source_file: Type.pdf
updated: 2026-10-25 01:00:41
---

# Trained Command Playbook: `Type.pdf`

- **Source Document:** `~/Projects/CORA/Training/Type.pdf`
- **CEGAR Verified Commands:** `3` (`0` malformed/unsafe snippets filtered)
- **MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`):** `3`
- **Discovered IPs/Subnets:** `None`
- **Discovered Interfaces:** `None`
- **Related Knowledge Note:** [[knowledge/trained_type]]

## Distilled MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`)
| Pre-State ($s$) | Tactic ($\tau$) | Technique ($k$) | Tool ($u$) | Post-State ($s'$) | Verified Command ($c$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `type` | `s_passive_topology_mapped` | `type [Drive:][Path] FileName` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `type` | `s_passive_topology_mapped` | `type holiday.mar` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `type` | `s_passive_topology_mapped` | `type holiday.mar \| more` |

## Verified Executable Commands (Grouped by Capability Layer)

### General_System (3 commands)
```bash
type [Drive:][Path] FileName
type holiday.mar
type holiday.mar | more
```

