---
title: "Trained Command Playbook: Movelatr-SourceCode.txt"
tags:
  - defense_evasion_firewall
  - http
  - mdp
  - text
  - trained
source_file: Movelatr-SourceCode.txt
updated: 2026-10-25 00:59:21
---

# Trained Command Playbook: `Movelatr-SourceCode.txt`

- **Source Document:** `~/Projects/CORA/Training/Movelatr-SourceCode.txt`
- **CEGAR Verified Commands:** `4` (`0` malformed/unsafe snippets filtered)
- **MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`):** `4`
- **Discovered IPs/Subnets:** `None`
- **Discovered Interfaces:** `None`
- **Related Knowledge Note:** [[knowledge/trained_movelatr-sourcecode]]

## Distilled MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`)
| Pre-State ($s$) | Tactic ($\tau$) | Technique ($k$) | Tool ($u$) | Post-State ($s'$) | Verified Command ($c$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `movelatr` | `s_firewall_or_acl_unlocked` | `MOVELATR v1.02, (c)2000-2008 Jeremy Collake` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `movelatr` | `s_firewall_or_acl_unlocked` | `MOVELATR source destination` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `movelatr` | `s_firewall_or_acl_unlocked` | `MOVELATR source /D` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `movelatr` | `s_firewall_or_acl_unlocked` | `MOVELATR /C` |

## Verified Executable Commands (Grouped by Capability Layer)

### General_System (4 commands)
```bash
MOVELATR v1.02, (c)2000-2008 Jeremy Collake
MOVELATR source destination
MOVELATR source /D
MOVELATR /C
```

