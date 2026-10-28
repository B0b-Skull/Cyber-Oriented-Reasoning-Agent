---
title: "Trained Command Playbook: Systeminfo.pdf"
tags:
  - credential_access
  - https
  - mdp
  - passive_enum
  - pdf
  - trained
source_file: Systeminfo.pdf
updated: 2026-10-24 01:00:38
---

# Trained Command Playbook: `Systeminfo.pdf`

- **Source Document:** `~/Projects/CORA/Training/Systeminfo.pdf`
- **CEGAR Verified Commands:** `4` (`0` malformed/unsafe snippets filtered)
- **MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`):** `4`
- **Discovered IPs/Subnets:** `None`
- **Discovered Interfaces:** `None`
- **Related Knowledge Note:** [[knowledge/trained_systeminfo]]

## Distilled MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`)
| Pre-State ($s$) | Tactic ($\tau$) | Technique ($k$) | Tool ($u$) | Post-State ($s'$) | Verified Command ($c$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `systeminfo` | `s_passive_topology_mapped` | `Systeminfo` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `systeminfo` | `s_credentials_or_certs_acquired` | `systeminfo.exe /s srvmain` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `systeminfo` | `s_credentials_or_certs_acquired` | `systeminfo.exe /s srvmain /u maindom\hiropln` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `systeminfo` | `s_credentials_or_certs_acquired` | `systeminfo /s srvmain /u maindom\hiropln /p p@ssW23 /fo table` |

## Verified Executable Commands (Grouped by Capability Layer)

### General_System (4 commands)
```bash
Systeminfo
systeminfo.exe /s srvmain
systeminfo.exe /s srvmain /u maindom\hiropln
systeminfo /s srvmain /u maindom\hiropln /p p@ssW23 /fo table
```

