---
title: "Trained Command Playbook: informix-sql-injection-cheat-sheet.html"
tags:
  - html
  - initial_access_exploitation
  - mdp
  - nmap
  - trained
source_file: informix-sql-injection-cheat-sheet.html
updated: 2026-10-25 00:58:35
---

# Trained Command Playbook: `informix-sql-injection-cheat-sheet.html`

- **Source Document:** `~/Projects/CORA/Training/informix-sql-injection-cheat-sheet.html`
- **CEGAR Verified Commands:** `1` (`0` malformed/unsafe snippets filtered)
- **MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`):** `1`
- **Discovered IPs/Subnets:** `10.0.0.1`
- **Discovered Interfaces:** `None`
- **Related Knowledge Note:** [[knowledge/trained_informix-sql-injection-cheat-sheet]]

## Distilled MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`)
| Pre-State ($s$) | Tactic ($\tau$) | Technique ($k$) | Tool ($u$) | Post-State ($s'$) | Verified Command ($c$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `s_active_services_enumerated` | **`Initial_Access_Exploitation`** | Structured Query / Payload / Web API Endpoint Exploitation | `nmap` | `s_initial_shell_or_api_access` | `sudo nmap -sS -sV 10.0.0.1 -p- -v -version-all` |

## Verified Executable Commands (Grouped by Capability Layer)

### General_System (1 commands)
```bash
sudo nmap -sS -sV 10.0.0.1 -p- -v -version-all
```

