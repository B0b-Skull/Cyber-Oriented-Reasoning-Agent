---
title: "Trained Command Playbook: CQC001_E030_M040_transcript.pdf"
tags:
  - defense_evasion_firewall
  - mdp
  - netsh
  - pdf
  - trained
source_file: CQC001_E030_M040_transcript.pdf
updated: 2026-10-24 00:57:38
---

# Trained Command Playbook: `CQC001_E030_M040_transcript.pdf`

- **Source Document:** `~/Projects/CORA/Training/CQC001_E030_M040_transcript.pdf`
- **CEGAR Verified Commands:** `2` (`0` malformed/unsafe snippets filtered)
- **MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`):** `2`
- **Discovered IPs/Subnets:** `None`
- **Discovered Interfaces:** `None`
- **Related Knowledge Note:** [[knowledge/trained_cqc001_e030_m040_transcript]]

## Distilled MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`)
| Pre-State ($s$) | Tactic ($\tau$) | Technique ($k$) | Tool ($u$) | Post-State ($s'$) | Verified Command ($c$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `netsh` | `s_firewall_or_acl_unlocked` | `netsh advfirewall firewall set rule group="File and Printer Sharing" new enable=no` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `netsh` | `s_firewall_or_acl_unlocked` | `netsh advfirewall firewall set rule group="File and Printer Sharing" new enable=yes` |

## Verified Executable Commands (Grouped by Capability Layer)

### L3_Routing_NAT (2 commands)
```bash
netsh advfirewall firewall set rule group="File and Printer Sharing" new enable=no
netsh advfirewall firewall set rule group="File and Printer Sharing" new enable=yes
```

