---
title: "Trained Command Playbook: CQC001_E050_M040_Boot_Init_Login.pdf"
tags:
  - http
  - https
  - mdp
  - passive_enum
  - pdf
  - trained
source_file: CQC001_E050_M040_Boot_Init_Login.pdf
updated: 2026-10-25 22:55:20
---

# Trained Command Playbook: `CQC001_E050_M040_Boot_Init_Login.pdf`

- **Source Document:** `~/Projects/CORA/Training/CQC001_E050_M040_Boot_Init_Login.pdf`
- **CEGAR Verified Commands:** `1` (`0` malformed/unsafe snippets filtered)
- **MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`):** `1`
- **Discovered IPs/Subnets:** `None`
- **Discovered Interfaces:** `None`
- **Related Knowledge Note:** [[knowledge/trained_cqc001_e050_m040_boot_init_login]]

## Distilled MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`)
| Pre-State ($s$) | Tactic ($\tau$) | Technique ($k$) | Tool ($u$) | Post-State ($s'$) | Verified Command ($c$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Process, Registry, File & Socket Survey | `script` | `s_passive_topology_mapped` | `script in /etc/rc.d/init.d. The chkconfig command, on the other hand, modifies the rc.d directory and` |

## Verified Executable Commands (Grouped by Capability Layer)

### General_System
```bash
script in /etc/rc.d/init.d. The chkconfig command, on the other hand, modifies the rc.d directory and
```

