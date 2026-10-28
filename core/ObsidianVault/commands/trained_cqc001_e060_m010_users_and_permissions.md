---
title: "Trained Command Playbook: CQC001_E060_M010_Users_and_Permissions.pdf"
tags:
  - http
  - https
  - mdp
  - pdf
  - privilege_escalation
  - trained
source_file: CQC001_E060_M010_Users_and_Permissions.pdf
updated: 2026-10-24 00:58:02
---

# Trained Command Playbook: `CQC001_E060_M010_Users_and_Permissions.pdf`

- **Source Document:** `~/Projects/CORA/Training/CQC001_E060_M010_Users_and_Permissions.pdf`
- **CEGAR Verified Commands:** `1` (`0` malformed/unsafe snippets filtered)
- **MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`):** `1`
- **Discovered IPs/Subnets:** `None`
- **Discovered Interfaces:** `None`
- **Related Knowledge Note:** [[knowledge/trained_cqc001_e060_m010_users_and_permissions]]

## Distilled MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`)
| Pre-State ($s$) | Tactic ($\tau$) | Technique ($k$) | Tool ($u$) | Post-State ($s'$) | Verified Command ($c$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `chmod` | `s_interactive_tty_or_priv_escalated` | `chmod 644 /tmp/comments.txt` |

## Verified Executable Commands (Grouped by Capability Layer)

### General_System (1 commands)
```bash
chmod 644 /tmp/comments.txt
```

