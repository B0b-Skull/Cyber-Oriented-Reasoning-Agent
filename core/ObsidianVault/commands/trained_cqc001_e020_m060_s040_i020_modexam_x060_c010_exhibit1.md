---
title: "Trained Command Playbook: CQC001_E020_M060_S040_I020_ModExam_X060_C010_exhibit1.pdf"
tags:
  - mdp
  - out-of-band_access
  - pdf
  - trained
  - wmic
source_file: CQC001_E020_M060_S040_I020_ModExam_X060_C010_exhibit1.pdf
updated: 2026-10-24 00:57:34
---

# Trained Command Playbook: `CQC001_E020_M060_S040_I020_ModExam_X060_C010_exhibit1.pdf`

- **Source Document:** `~/Projects/CORA/Training/CQC001_E020_M060_S040_I020_ModExam_X060_C010_exhibit1.pdf`
- **CEGAR Verified Commands:** `1` (`0` malformed/unsafe snippets filtered)
- **MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`):** `1`
- **Discovered IPs/Subnets:** `None`
- **Discovered Interfaces:** `None`
- **Related Knowledge Note:** [[knowledge/trained_cqc001_e020_m060_s040_i020_modexam_x060_c010_exhibit1]]

## Distilled MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`)
| Pre-State ($s$) | Tactic ($\tau$) | Technique ($k$) | Tool ($u$) | Post-State ($s'$) | Verified Command ($c$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `s_l2_l3_verified` | **`Out-of-Band_Access`** | UART/Serial Console Out-of-Band Enumeration & Control | `wmic` | `s_oob_serial_enumerated` | `wmic process get description,executablepath,processid /format:htable` |

## Verified Executable Commands (Grouped by Capability Layer)

### General_System (1 commands)
```bash
wmic process get description,executablepath,processid /format:htable
```

