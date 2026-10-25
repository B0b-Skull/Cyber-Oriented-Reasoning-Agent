---
title: "Trained Command Playbook: CQC001_E020_M050_S040_I030_Exer_X010_C010_transcript.txt"
tags:
  - listdlls
  - mdp
  - passive_enum
  - pslist
  - text
  - trained
source_file: CQC001_E020_M050_S040_I030_Exer_X010_C010_transcript.txt
updated: 2026-10-25 00:57:33
---

# Trained Command Playbook: `CQC001_E020_M050_S040_I030_Exer_X010_C010_transcript.txt`

- **Source Document:** `~/Projects/CORA/Training/CQC001_E020_M050_S040_I030_Exer_X010_C010_transcript.txt`
- **CEGAR Verified Commands:** `1` (`0` malformed/unsafe snippets filtered)
- **MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`):** `1`
- **Discovered IPs/Subnets:** `None`
- **Discovered Interfaces:** `None`
- **Related Knowledge Note:** [[knowledge/trained_cqc001_e020_m050_s040_i030_exer_x010_c010_transcript]]

## Distilled MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`)
| Pre-State ($s$) | Tactic ($\tau$) | Technique ($k$) | Tool ($u$) | Post-State ($s'$) | Verified Command ($c$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `pslist` | `s_passive_topology_mapped` | `pslist             2904  13   1  138   1984     0:00:00.046     0:00:00.046` |

## Verified Executable Commands (Grouped by Capability Layer)

### General_System (1 commands)
```bash
pslist             2904  13   1  138   1984     0:00:00.046     0:00:00.046
```

