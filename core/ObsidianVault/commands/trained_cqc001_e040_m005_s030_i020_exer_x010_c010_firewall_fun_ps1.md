---
title: "Trained Command Playbook: CQC001_E040_M005_S030_I020_Exer_X010_C010_Firewall_Fun.ps1.txt"
tags:
  - defense_evasion_firewall
  - mdp
  - netsh
  - text
  - trained
source_file: CQC001_E040_M005_S030_I020_Exer_X010_C010_Firewall_Fun.ps1.txt
updated: 2026-10-25 00:57:51
---

# Trained Command Playbook: `CQC001_E040_M005_S030_I020_Exer_X010_C010_Firewall_Fun.ps1.txt`

- **Source Document:** `~/Projects/CORA/Training/CQC001_E040_M005_S030_I020_Exer_X010_C010_Firewall_Fun.ps1.txt`
- **CEGAR Verified Commands:** `2` (`0` malformed/unsafe snippets filtered)
- **MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`):** `2`
- **Discovered IPs/Subnets:** `None`
- **Discovered Interfaces:** `None`
- **Related Knowledge Note:** [[knowledge/trained_cqc001_e040_m005_s030_i020_exer_x010_c010_firewall_fun_ps1]]

## Distilled MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`)
| Pre-State ($s$) | Tactic ($\tau$) | Technique ($k$) | Tool ($u$) | Post-State ($s'$) | Verified Command ($c$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `select-string` | `s_firewall_or_acl_unlocked` | `Select-String FileName \| select -ExpandProperty line \| Select-String "%systemroot%.+\.log" \|` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `select-string` | `s_firewall_or_acl_unlocked` | `Select-String "\b(?:\d{1,3}\.){3}\d{1,3}\b" $FWLogs \| select -ExpandProperty matches \| select value \|` |

## Verified Executable Commands (Grouped by Capability Layer)

### General_System (2 commands)
```bash
Select-String FileName | select -ExpandProperty line | Select-String "%systemroot%.+\.log" |
Select-String "\b(?:\d{1,3}\.){3}\d{1,3}\b" $FWLogs | select -ExpandProperty matches | select value |
```

