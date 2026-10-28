---
title: "Trained Command Playbook: CQC001_E060_M030_iptables_and_Snort.pdf"
tags:
  - defense_evasion_firewall
  - http
  - https
  - iptables
  - mdp
  - pdf
  - snort
  - trained
source_file: CQC001_E060_M030_iptables_and_Snort.pdf
updated: 2026-10-23 22:55:22
---

# Trained Command Playbook: `CQC001_E060_M030_iptables_and_Snort.pdf`

- **Source Document:** `~/Projects/CORA/Training/CQC001_E060_M030_iptables_and_Snort.pdf`
- **CEGAR Verified Commands:** `3` (`0` malformed/unsafe snippets filtered)
- **MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`):** `3`
- **Discovered IPs/Subnets:** `None`
- **Discovered Interfaces:** `None`
- **Related Knowledge Note:** [[knowledge/trained_cqc001_e060_m030_iptables_and_snort]]

## Distilled MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`)
| Pre-State ($s$) | Tactic ($\tau$) | Technique ($k$) | Tool ($u$) | Post-State ($s'$) | Verified Command ($c$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, Boot/DEP & Integrity Control Adjustment | `iptables` | `s_firewall_or_acl_unlocked` | `IPTABLES AND SNORT` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, Boot/DEP & Integrity Control Adjustment | `snort` | `s_firewall_or_acl_unlocked` | `Snort rules tutorial:` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, Boot/DEP & Integrity Control Adjustment | `snort` | `s_firewall_or_acl_unlocked` | `Snort Users Manual:` |

## Verified Executable Commands (Grouped by Capability Layer)

### L3_Routing_NAT
```bash
IPTABLES AND SNORT
```

### L4_Port_Service
```bash
Snort rules tutorial:
Snort Users Manual:
```

