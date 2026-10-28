---
title: "Trained Command Playbook: CQC001_E020_M040_transcript.txt"
tags:
  - listdlls
  - mdp
  - passive_enum
  - pslist
  - sysinternals
  - text
  - trained
source_file: CQC001_E020_M040_transcript.txt
updated: 2026-10-24 00:57:32
---

# Trained Command Playbook: `CQC001_E020_M040_transcript.txt`

- **Source Document:** `~/Projects/CORA/Training/CQC001_E020_M040_transcript.txt`
- **CEGAR Verified Commands:** `1` (`0` malformed/unsafe snippets filtered)
- **MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`):** `1`
- **Discovered IPs/Subnets:** `None`
- **Discovered Interfaces:** `None`
- **Related Knowledge Note:** [[knowledge/trained_cqc001_e020_m040_transcript]]

## Distilled MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`)
| Pre-State ($s$) | Tactic ($\tau$) | Technique ($k$) | Tool ($u$) | Post-State ($s'$) | Verified Command ($c$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `tasklist` | `s_passive_topology_mapped` | `Tasklist` |

## Verified Executable Commands (Grouped by Capability Layer)

### General_System (1 commands)
```bash
Tasklist
```

