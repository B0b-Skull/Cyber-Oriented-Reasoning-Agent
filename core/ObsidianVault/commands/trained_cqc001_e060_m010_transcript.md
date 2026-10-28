---
title: "Trained Command Playbook: CQC001_E060_M010_transcript.pdf"
tags:
  - mdp
  - pdf
  - privilege_escalation
  - trained
source_file: CQC001_E060_M010_transcript.pdf
updated: 2026-10-24 00:58:02
---

# Trained Command Playbook: `CQC001_E060_M010_transcript.pdf`

- **Source Document:** `~/Projects/CORA/Training/CQC001_E060_M010_transcript.pdf`
- **CEGAR Verified Commands:** `4` (`0` malformed/unsafe snippets filtered)
- **MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`):** `4`
- **Discovered IPs/Subnets:** `None`
- **Discovered Interfaces:** `None`
- **Related Knowledge Note:** [[knowledge/trained_cqc001_e060_m010_transcript]]

## Distilled MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`)
| Pre-State ($s$) | Tactic ($\tau$) | Technique ($k$) | Tool ($u$) | Post-State ($s'$) | Verified Command ($c$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `chgrp` | `s_interactive_tty_or_priv_escalated` | `chgrp commands accept the -R option, which essentially directs that the same ownership change` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `chmod` | `s_interactive_tty_or_priv_escalated` | `chmod Results` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `su` | `s_interactive_tty_or_priv_escalated` | `su - A Special SUID Program` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `-` | `s_interactive_tty_or_priv_escalated` | `sudo - Another Special SUID Program` |

## Verified Executable Commands (Grouped by Capability Layer)

### General_System (4 commands)
```bash
chgrp commands accept the -R option, which essentially directs that the same ownership change
chmod Results
su - A Special SUID Program
sudo - Another Special SUID Program
```

