---
title: "Trained Command Playbook: CQC001_E050_M050_transcript.pdf"
tags:
  - enumeration
  - http
  - mdp
  - pdf
  - trained
source_file: CQC001_E050_M050_transcript.pdf
updated: 2026-10-25 00:58:02
---

# Trained Command Playbook: `CQC001_E050_M050_transcript.pdf`

- **Source Document:** `~/Projects/CORA/Training/CQC001_E050_M050_transcript.pdf`
- **CEGAR Verified Commands:** `1` (`0` malformed/unsafe snippets filtered)
- **MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`):** `1`
- **Discovered IPs/Subnets:** `None`
- **Discovered Interfaces:** `None`
- **Related Knowledge Note:** [[knowledge/trained_cqc001_e050_m050_transcript]]

## Distilled MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`)
| Pre-State ($s$) | Tactic ($\tau$) | Technique ($k$) | Tool ($u$) | Post-State ($s'$) | Verified Command ($c$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `kill` | `s_active_services_enumerated` | `kill -s signal pid` |

## Verified Executable Commands (Grouped by Capability Layer)

### General_System (1 commands)
```bash
kill -s signal pid
```

