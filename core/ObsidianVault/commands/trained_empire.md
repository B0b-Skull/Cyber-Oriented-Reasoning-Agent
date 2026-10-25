---
title: "Trained Command Playbook: Empire.pdf"
tags:
  - credential_access
  - enumeration
  - http
  - https
  - initial_access_exploitation
  - ipconfig
  - kerberos
  - mdp
  - mimikatz
  - out-of-band_access
  - pdf
  - powershell
  - trained
source_file: Empire.pdf
updated: 2026-10-25 00:58:23
---

# Trained Command Playbook: `Empire.pdf`

- **Source Document:** `~/Projects/CORA/Training/Empire.pdf`
- **CEGAR Verified Commands:** `9` (`0` malformed/unsafe snippets filtered)
- **MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`):** `9`
- **Discovered IPs/Subnets:** `None`
- **Discovered Interfaces:** `None`
- **Related Knowledge Note:** [[knowledge/trained_empire]]

## Distilled MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`)
| Pre-State ($s$) | Tactic ($\tau$) | Technique ($k$) | Tool ($u$) | Post-State ($s'$) | Verified Command ($c$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `s_active_services_enumerated` | **`Initial_Access_Exploitation`** | Structured Query / Payload / Web API Endpoint Exploitation | `empire.db` | `s_initial_shell_or_api_access` | `./data/empire.db` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `empire.db` | `s_active_services_enumerated` | `./data./empire.db and start back up on Empire startup.` |
| `s_l2_l3_verified` | **`Out-of-Band_Access`** | UART/Serial Console Out-of-Band Enumeration & Control | `file.txt` | `s_oob_serial_enumerated` | `./attacker/path/file.txt` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `sekurlsa::logonpasswords` | `s_credentials_or_certs_acquired` | `sekurlsa::logonpasswords` |
| `s_active_services_enumerated` | **`Initial_Access_Exploitation`** | Structured Query / Payload / Web API Endpoint Exploitation | `agent.log` | `s_initial_shell_or_api_access` | `./downloads/AGENTNAME/agent.log` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `unset` | `s_active_services_enumerated` | `Unset an option: unset OPTION` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `mimikatz` | `s_credentials_or_certs_acquired` | `Mimikatz and the Cred Store` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `kill` | `s_active_services_enumerated` | `kill [tab] ID/all` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `kill` | `s_active_services_enumerated` | `kill PID` |

## Verified Executable Commands (Grouped by Capability Layer)

### General_System (9 commands)
```bash
./data/empire.db
./downloads/AGENTNAME/agent.log
./data./empire.db and start back up on Empire startup.
Unset an option: unset OPTION
kill [tab] ID/all
./attacker/path/file.txt
kill PID
sekurlsa::logonpasswords
Mimikatz and the Cred Store
```

