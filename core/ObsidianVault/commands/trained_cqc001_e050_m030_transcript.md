---
title: "Trained Command Playbook: CQC001_E050_M030_transcript.pdf"
tags:
  - enumeration
  - mdp
  - pdf
  - trained
source_file: CQC001_E050_M030_transcript.pdf
updated: 2026-10-25 00:57:59
---

# Trained Command Playbook: `CQC001_E050_M030_transcript.pdf`

- **Source Document:** `~/Projects/CORA/Training/CQC001_E050_M030_transcript.pdf`
- **CEGAR Verified Commands:** `6` (`0` malformed/unsafe snippets filtered)
- **MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`):** `6`
- **Discovered IPs/Subnets:** `None`
- **Discovered Interfaces:** `None`
- **Related Knowledge Note:** [[knowledge/trained_cqc001_e050_m030_transcript]]

## Distilled MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`)
| Pre-State ($s$) | Tactic ($\tau$) | Technique ($k$) | Tool ($u$) | Post-State ($s'$) | Verified Command ($c$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `echo` | `s_active_services_enumerated` | `echo BOO! > /dev/pts/1 the typed text displays on the other terminal window.` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `wc` | `s_active_services_enumerated` | `wc -l counts the number of lines in a file.` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `wc` | `s_active_services_enumerated` | `wc -l file1` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `wc` | `s_active_services_enumerated` | `wc -l file2` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `wc` | `s_active_services_enumerated` | `wc -l file3` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `wc` | `s_active_services_enumerated` | `wc -l file1 file2 file3` |

## Verified Executable Commands (Grouped by Capability Layer)

### General_System (6 commands)
```bash
echo BOO! > /dev/pts/1 the typed text displays on the other terminal window.
wc -l counts the number of lines in a file.
wc -l file1
wc -l file2
wc -l file3
wc -l file1 file2 file3
```

