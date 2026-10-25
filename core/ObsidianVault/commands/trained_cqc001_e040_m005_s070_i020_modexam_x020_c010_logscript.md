---
title: "Trained Command Playbook: CQC001_E040_M005_S070_I020_ModExam_X020_C010_LogScript.txt"
tags:
  - http
  - lateral_movement_routing_pivot
  - mdp
  - text
  - trained
source_file: CQC001_E040_M005_S070_I020_ModExam_X020_C010_LogScript.txt
updated: 2026-10-25 00:57:52
---

# Trained Command Playbook: `CQC001_E040_M005_S070_I020_ModExam_X020_C010_LogScript.txt`

- **Source Document:** `~/Projects/CORA/Training/CQC001_E040_M005_S070_I020_ModExam_X020_C010_LogScript.txt`
- **CEGAR Verified Commands:** `1` (`0` malformed/unsafe snippets filtered)
- **MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`):** `1`
- **Discovered IPs/Subnets:** `None`
- **Discovered Interfaces:** `None`
- **Related Knowledge Note:** [[knowledge/trained_cqc001_e040_m005_s070_i020_modexam_x020_c010_logscript]]

## Distilled MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`)
| Pre-State ($s$) | Tactic ($\tau$) | Technique ($k$) | Tool ($u$) | Post-State ($s'$) | Verified Command ($c$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `s_firewall_or_acl_unlocked` | **`Lateral_Movement_Routing_Pivot`** | Remote Host Execution, L2/L3 Route Injection & Subnet Pivot | `get-wmiobject` | `s_cross_subnet_pivot_routed` | `get-wmiobject -query $query -computername $computer \| select-object RecordNumber,TimeGenerated,ComputerName,LogFile,User,SourceName,EventCode,Type,Message` |

## Verified Executable Commands (Grouped by Capability Layer)

### General_System (1 commands)
```bash
get-wmiobject -query $query -computername $computer | select-object RecordNumber,TimeGenerated,ComputerName,LogFile,User,SourceName,EventCode,Type,Message
```

