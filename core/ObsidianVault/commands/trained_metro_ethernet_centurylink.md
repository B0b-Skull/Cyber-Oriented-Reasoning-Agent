---
title: "Trained Command Playbook: Metro Ethernet CenturyLink.pdf"
tags:
  - enumeration
  - http
  - mdp
  - pdf
  - trained
source_file: Metro Ethernet CenturyLink.pdf
updated: 2026-10-25 22:57:31
---

# Trained Command Playbook: `Metro Ethernet CenturyLink.pdf`

- **Source Document:** `~/Projects/CORA/Training/Metro Ethernet CenturyLink.pdf`
- **CEGAR Verified Commands:** `4` (`0` malformed/unsafe snippets filtered)
- **MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`):** `4`
- **Discovered IPs/Subnets:** `None`
- **Discovered Interfaces:** `None`
- **Related Knowledge Note:** [[knowledge/trained_metro_ethernet_centurylink]]

## Distilled MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`)
| Pre-State ($s$) | Tactic ($\tau$) | Technique ($k$) | Tool ($u$) | Post-State ($s'$) | Verified Command ($c$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `service` | `s_active_services_enumerated` | `service providers'` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `service` | `s_active_services_enumerated` | `service delivery and, in turn, deliver leading-edge services to its customers and partners.` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `service` | `s_active_services_enumerated` | `Service Maturity` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `service` | `s_active_services_enumerated` | `service provider (UNI-N)` |

## Verified Executable Commands (Grouped by Capability Layer)

### General_System
```bash
service providers'
service delivery and, in turn, deliver leading-edge services to its customers and partners.
Service Maturity
service provider (UNI-N)
```

