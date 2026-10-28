---
title: "Trained Command Playbook: LTE_mobile_optimization-a_definitive_guide_wp_en_5216-2018-52_v0100.pdf"
tags:
  - active_enum
  - http
  - mdp
  - pdf
  - post_exploitation_verification
  - tio
  - trained
source_file: LTE_mobile_optimization-a_definitive_guide_wp_en_5216-2018-52_v0100.pdf
updated: 2026-10-24 00:58:53
---

# Trained Command Playbook: `LTE_mobile_optimization-a_definitive_guide_wp_en_5216-2018-52_v0100.pdf`

- **Source Document:** `~/Projects/CORA/Training/LTE_mobile_optimization-a_definitive_guide_wp_en_5216-2018-52_v0100.pdf`
- **CEGAR Verified Commands:** `2` (`1` malformed/unsafe snippets filtered)
- **MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`):** `2`
- **Discovered IPs/Subnets:** `None`
- **Discovered Interfaces:** `None`
- **Related Knowledge Note:** [[knowledge/trained_lte_mobile_optimization-a_definitive_guide_wp_en_5216-2018-52_v0]]

## Distilled MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`)
| Pre-State ($s$) | Tactic ($\tau$) | Technique ($k$) | Tool ($u$) | Post-State ($s'$) | Verified Command ($c$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `s_cross_subnet_pivot_routed` | **`Post_Exploitation_Verification`** | Post-Action Host Identity, Privilege & Objective Verification | `groups` | `s_goal_verified_complete` | `groups (REG) or 36 resource elements (REs) since each REG contains 4 REs. PDCCH cod-` |
| `s_passive_topology_mapped` | **`Active_Enum`** | Active Network, Cloud, Directory Service & Endpoint Probing | `ping` | `s_active_services_enumerated` | `ping -c 3 RTT between UE and application` |

## Verified Executable Commands (Grouped by Capability Layer)

### General_System (1 commands)
```bash
groups (REG) or 36 resource elements (REs) since each REG contains 4 REs. PDCCH cod-
```

### L3_Routing_NAT (1 commands)
```bash
ping -c 3 RTT between UE and application
```

