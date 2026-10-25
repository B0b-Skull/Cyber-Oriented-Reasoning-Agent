---
title: "Trained Command Playbook: CQC001_E010_M050_RFC792.pdf"
tags:
  - enumeration
  - mdp
  - pdf
  - reconnaissance
  - trained
source_file: CQC001_E010_M050_RFC792.pdf
updated: 2026-10-25 00:57:28
---

# Trained Command Playbook: `CQC001_E010_M050_RFC792.pdf`

- **Source Document:** `~/Projects/CORA/Training/CQC001_E010_M050_RFC792.pdf`
- **CEGAR Verified Commands:** `2` (`0` malformed/unsafe snippets filtered)
- **MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`):** `2`
- **Discovered IPs/Subnets:** `None`
- **Discovered Interfaces:** `None`
- **Related Knowledge Note:** [[knowledge/trained_cqc001_e010_m050_rfc792]]

## Distilled MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`)
| Pre-State ($s$) | Tactic ($\tau$) | Technique ($k$) | Tool ($u$) | Post-State ($s'$) | Verified Command ($c$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `s_init_unknown` | **`Reconnaissance`** | Domain, DNS, OSINT & Target Footprint Reconnaissance | `cut` | `s_passive_topology_mapped` | `cut back the rate at which it is sending traffic to the internet` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `echo` | `s_active_services_enumerated` | `Echo or Echo Reply Message` |

## Verified Executable Commands (Grouped by Capability Layer)

### General_System (2 commands)
```bash
cut back the rate at which it is sending traffic to the internet
Echo or Echo Reply Message
```

