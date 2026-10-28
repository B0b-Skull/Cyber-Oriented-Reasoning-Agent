---
title: "Trained Command Playbook: CQC001_E060_M020_UNIX_Logging.pdf"
tags:
  - http
  - https
  - mdp
  - passive_enum
  - pdf
  - trained
source_file: CQC001_E060_M020_UNIX_Logging.pdf
updated: 2026-10-24 00:58:02
---

# Trained Command Playbook: `CQC001_E060_M020_UNIX_Logging.pdf`

- **Source Document:** `~/Projects/CORA/Training/CQC001_E060_M020_UNIX_Logging.pdf`
- **CEGAR Verified Commands:** `1` (`0` malformed/unsafe snippets filtered)
- **MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`):** `1`
- **Discovered IPs/Subnets:** `None`
- **Discovered Interfaces:** `None`
- **Related Knowledge Note:** [[knowledge/trained_cqc001_e060_m020_unix_logging]]

## Distilled MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`)
| Pre-State ($s$) | Tactic ($\tau$) | Technique ($k$) | Tool ($u$) | Post-State ($s'$) | Verified Command ($c$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `handle` | `s_passive_topology_mapped` | `handle messages from different facilities in different ways.` |

## Verified Executable Commands (Grouped by Capability Layer)

### General_System (1 commands)
```bash
handle messages from different facilities in different ways.
```

