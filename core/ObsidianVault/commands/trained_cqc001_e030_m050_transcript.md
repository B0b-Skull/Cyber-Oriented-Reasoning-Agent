---
title: "Trained Command Playbook: CQC001_E030_M050_transcript.pdf"
tags:
  - auditpol
  - credential_access
  - kerberos
  - mdp
  - pdf
  - trained
source_file: CQC001_E030_M050_transcript.pdf
updated: 2026-10-25 00:57:38
---

# Trained Command Playbook: `CQC001_E030_M050_transcript.pdf`

- **Source Document:** `~/Projects/CORA/Training/CQC001_E030_M050_transcript.pdf`
- **CEGAR Verified Commands:** `1` (`0` malformed/unsafe snippets filtered)
- **MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`):** `1`
- **Discovered IPs/Subnets:** `None`
- **Discovered Interfaces:** `None`
- **Related Knowledge Note:** [[knowledge/trained_cqc001_e030_m050_transcript]]

## Distilled MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`)
| Pre-State ($s$) | Tactic ($\tau$) | Technique ($k$) | Tool ($u$) | Post-State ($s'$) | Verified Command ($c$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `handle` | `s_credentials_or_certs_acquired` | `handle duplication, indirect access to an object, and process exit.` |

## Verified Executable Commands (Grouped by Capability Layer)

### General_System (1 commands)
```bash
handle duplication, indirect access to an object, and process exit.
```

