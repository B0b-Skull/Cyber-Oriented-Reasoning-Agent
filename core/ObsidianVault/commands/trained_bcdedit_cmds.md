---
title: "Trained Command Playbook: BcdEdit CMDs.txt"
tags:
  - bcdedit
  - defense_evasion_firewall
  - mdp
  - passive_enum
  - text
  - trained
source_file: BcdEdit CMDs.txt
updated: 2026-10-25 00:56:14
---

# Trained Command Playbook: `BcdEdit CMDs.txt`

- **Source Document:** `~/Projects/CORA/Training/BcdEdit CMDs.txt`
- **CEGAR Verified Commands:** `8` (`0` malformed/unsafe snippets filtered)
- **MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`):** `8`
- **Discovered IPs/Subnets:** `None`
- **Discovered Interfaces:** `None`
- **Related Knowledge Note:** [[knowledge/trained_bcdedit_cmds]]

## Distilled MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`)
| Pre-State ($s$) | Tactic ($\tau$) | Technique ($k$) | Tool ($u$) | Post-State ($s'$) | Verified Command ($c$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `attrib` | `s_firewall_or_acl_unlocked` | `attrib -s -h boot.ini` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `type` | `s_passive_topology_mapped` | `type boot.ini` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `bcdedit` | `s_firewall_or_acl_unlocked` | `bcdedit /export C:\boot_backup` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `bcdedit` | `s_firewall_or_acl_unlocked` | `bcdedit /timeout 180` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `bcdedit` | `s_firewall_or_acl_unlocked` | `bcdedit /default {47af9428-3f7d-11e4-89de-806e6f6e6963}` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `bcdedit` | `s_firewall_or_acl_unlocked` | `bcdedit /set {47af9428-3f7d-11e4-89de-806e6f6e6963} description "Primary Operating System"` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `bcdedit` | `s_firewall_or_acl_unlocked` | `bcdedit /set {f7428705-3f60-11e4-ae6a-806e6f6e6963} description "Secondary Operating System"` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `bcdedit` | `s_firewall_or_acl_unlocked` | `bcdedit /displayorder {47af9428-3f7d-11e4-89de-806e6f6e6963} {f7428705-3f60-11e4-ae6a-806e6f6e6963}` |

## Verified Executable Commands (Grouped by Capability Layer)

### General_System (8 commands)
```bash
attrib -s -h boot.ini
type boot.ini
bcdedit /export C:\boot_backup
bcdedit /timeout 180
bcdedit /default {47af9428-3f7d-11e4-89de-806e6f6e6963}
bcdedit /set {47af9428-3f7d-11e4-89de-806e6f6e6963} description "Primary Operating System"
bcdedit /set {f7428705-3f60-11e4-ae6a-806e6f6e6963} description "Secondary Operating System"
bcdedit /displayorder {47af9428-3f7d-11e4-89de-806e6f6e6963} {f7428705-3f60-11e4-ae6a-806e6f6e6963}
```

