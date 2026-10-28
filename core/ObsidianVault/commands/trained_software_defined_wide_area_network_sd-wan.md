---
title: "Trained Command Playbook: Software Defined Wide Area Network (SD-WAN).pdf"
tags:
  - defense_evasion_firewall
  - enumeration
  - http
  - https
  - mdp
  - pdf
  - ssl
  - trained
  - vlan
source_file: Software Defined Wide Area Network (SD-WAN).pdf
updated: 2026-10-23 23:06:43
---

# Trained Command Playbook: `Software Defined Wide Area Network (SD-WAN).pdf`

- **Source Document:** `~/Projects/CORA/Training/Software Defined Wide Area Network (SD-WAN).pdf`
- **CEGAR Verified Commands:** `4` (`0` malformed/unsafe snippets filtered)
- **MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`):** `4`
- **Discovered IPs/Subnets:** `1.2.3.4, 5.6.7.8`
- **Discovered Interfaces:** `vlan1`
- **Related Knowledge Note:** [[knowledge/trained_software_defined_wide_area_network_sd-wan]]

## Distilled MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`)
| Pre-State ($s$) | Tactic ($\tau$) | Technique ($k$) | Tool ($u$) | Post-State ($s'$) | Verified Command ($c$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `service` | `s_active_services_enumerated` | `Service chaining / traffic` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, Boot/DEP & Integrity Control Adjustment | `service` | `s_firewall_or_acl_unlocked` | `Service Function Chaining (SFC)` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, Boot/DEP & Integrity Control Adjustment | `service` | `s_firewall_or_acl_unlocked` | `Service Function Chaining` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `service` | `s_active_services_enumerated` | `service that enables application-aware, policy-` |

## Verified Executable Commands (Grouped by Capability Layer)

### General_System
```bash
Service chaining / traffic
Service Function Chaining (SFC)
Service Function Chaining
service that enables application-aware, policy-
```

