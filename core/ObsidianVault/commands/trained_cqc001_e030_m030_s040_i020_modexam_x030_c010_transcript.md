---
title: "Trained Command Playbook: CQC001_E030_M030_S040_I020_ModExam_X030_C010_transcript.txt"
tags:
  - credential_access
  - enumeration
  - icacls
  - mdp
  - privilege_escalation
  - text
  - trained
source_file: CQC001_E030_M030_S040_I020_ModExam_X030_C010_transcript.txt
updated: 2026-10-25 00:57:38
---

# Trained Command Playbook: `CQC001_E030_M030_S040_I020_ModExam_X030_C010_transcript.txt`

- **Source Document:** `~/Projects/CORA/Training/CQC001_E030_M030_S040_I020_ModExam_X030_C010_transcript.txt`
- **CEGAR Verified Commands:** `5` (`0` malformed/unsafe snippets filtered)
- **MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`):** `5`
- **Discovered IPs/Subnets:** `None`
- **Discovered Interfaces:** `None`
- **Related Knowledge Note:** [[knowledge/trained_cqc001_e030_m030_s040_i020_modexam_x030_c010_transcript]]

## Distilled MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`)
| Pre-State ($s$) | Tactic ($\tau$) | Technique ($k$) | Tool ($u$) | Post-State ($s'$) | Verified Command ($c$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `net` | `s_credentials_or_certs_acquired` | `net user bojangles` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `icacls` | `s_interactive_tty_or_priv_escalated` | `icacls random /T` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `w` | `s_active_services_enumerated` | `W - write-only access` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `net` | `s_credentials_or_certs_acquired` | `net user lilith` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `rd` | `s_active_services_enumerated` | `RD - read data/list directory` |

## Verified Executable Commands (Grouped by Capability Layer)

### General_System (5 commands)
```bash
net user bojangles
net user lilith
icacls random /T
W - write-only access
RD - read data/list directory
```

