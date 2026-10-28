---
title: "Trained Command Playbook: CQC001_E040_M010_transcript.pdf"
tags:
  - auditpol
  - autorunsc
  - ipconfig
  - mdp
  - netstat
  - passive_enum
  - pdf
  - pslist
  - sysinternals
  - trained
  - wmic
source_file: CQC001_E040_M010_transcript.pdf
updated: 2026-10-24 00:57:54
---

# Trained Command Playbook: `CQC001_E040_M010_transcript.pdf`

- **Source Document:** `~/Projects/CORA/Training/CQC001_E040_M010_transcript.pdf`
- **CEGAR Verified Commands:** `2` (`0` malformed/unsafe snippets filtered)
- **MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`):** `2`
- **Discovered IPs/Subnets:** `0.0.0.0, 127.0.0.1`
- **Discovered Interfaces:** `None`
- **Related Knowledge Note:** [[knowledge/trained_cqc001_e040_m010_transcript]]

## Distilled MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`)
| Pre-State ($s$) | Tactic ($\tau$) | Technique ($k$) | Tool ($u$) | Post-State ($s'$) | Verified Command ($c$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `dir` | `s_passive_topology_mapped` | `dir command, shows the timestamp for directories and files - in this case, the timestamp` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `net` | `s_passive_topology_mapped` | `net users displays all the users that have been created on this system. This registry query` |

## Verified Executable Commands (Grouped by Capability Layer)

### General_System (2 commands)
```bash
dir command, shows the timestamp for directories and files - in this case, the timestamp
net users displays all the users that have been created on this system. This registry query
```

