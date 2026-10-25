---
title: "Trained Command Playbook: SQL Injection Cheat Sheet by Netsparker.pdf"
tags:
  - covert_infil
  - enumeration
  - http
  - john
  - mdp
  - pdf
  - trained
source_file: SQL Injection Cheat Sheet by Netsparker.pdf
updated: 2026-10-25 01:00:36
---

# Trained Command Playbook: `SQL Injection Cheat Sheet by Netsparker.pdf`

- **Source Document:** `~/Projects/CORA/Training/SQL Injection Cheat Sheet by Netsparker.pdf`
- **CEGAR Verified Commands:** `6` (`0` malformed/unsafe snippets filtered)
- **MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`):** `6`
- **Discovered IPs/Subnets:** `None`
- **Discovered Interfaces:** `None`
- **Related Knowledge Note:** [[knowledge/trained_sql_injection_cheat_sheet_by_netsparker]]

## Distilled MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`)
| Pre-State ($s$) | Tactic ($\tau$) | Technique ($k$) | Tool ($u$) | Post-State ($s'$) | Verified Command ($c$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `mysql` | `s_active_services_enumerated` | `MySQL Version Detection Sample Attacks` |
| `s_protocol_chain_established` | **`Covert_Infil`** | Staged Artifact / Encapsulated Ingress Delivery | `mysql` | `s_covert_infil_channel_ready` | `MySQL Load Data infile` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `mysql` | `s_active_services_enumerated` | `MySQL If Statement` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `mysql` | `s_active_services_enumerated` | `MySQL (M)` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `mysql` | `s_active_services_enumerated` | `MySQL Related` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `mysql` | `s_active_services_enumerated` | `MySQL Gotchas ­ http://sql­info.de/mysql/gotchas.htm` |

## Verified Executable Commands (Grouped by Capability Layer)

### General_System (5 commands)
```bash
MySQL Version Detection Sample Attacks
MySQL If Statement
MySQL (M)
MySQL Load Data infile
MySQL Related
```

### L7_HTTP_Web (1 commands)
```bash
MySQL Gotchas ­ http://sql­info.de/mysql/gotchas.htm
```

