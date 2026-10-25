---
title: "Trained Command Playbook: CQC001_E030_M030_transcript.pdf"
tags:
  - mdp
  - pdf
  - post_exploitation_verification
  - trained
source_file: CQC001_E030_M030_transcript.pdf
updated: 2026-10-25 22:55:03
---

# Trained Command Playbook: `CQC001_E030_M030_transcript.pdf`

- **Source Document:** `~/Projects/CORA/Training/CQC001_E030_M030_transcript.pdf`
- **CEGAR Verified Commands:** `1` (`0` malformed/unsafe snippets filtered)
- **MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`):** `1`
- **Discovered IPs/Subnets:** `None`
- **Discovered Interfaces:** `None`
- **Related Knowledge Note:** [[knowledge/trained_cqc001_e030_m030_transcript]]

## Distilled MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`)
| Pre-State ($s$) | Tactic ($\tau$) | Technique ($k$) | Tool ($u$) | Post-State ($s'$) | Verified Command ($c$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `s_cross_subnet_pivot_routed` | **`Post_Exploitation_Verification`** | Post-Action Host Identity, Privilege & Objective Verification | `groups` | `s_goal_verified_complete` | `Groups` |

## Verified Executable Commands (Grouped by Capability Layer)

### General_System
```bash
Groups
```

