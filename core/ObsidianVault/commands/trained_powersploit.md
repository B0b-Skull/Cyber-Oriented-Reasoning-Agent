---
title: "Trained Command Playbook: PowerSploit.pdf"
tags:
  - credential_access
  - enumeration
  - http
  - https
  - kerberos
  - mdp
  - mimikatz
  - nmap
  - passive_enum
  - pdf
  - powershell
  - privilege_escalation
  - trained
source_file: PowerSploit.pdf
updated: 2026-10-24 01:00:07
---

# Trained Command Playbook: `PowerSploit.pdf`

- **Source Document:** `~/Projects/CORA/Training/PowerSploit.pdf`
- **CEGAR Verified Commands:** `13` (`0` malformed/unsafe snippets filtered)
- **MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`):** `13`
- **Discovered IPs/Subnets:** `172.24.1.0/24`
- **Discovered Interfaces:** `None`
- **Related Knowledge Note:** [[knowledge/trained_powersploit]]

## Distilled MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`)
| Pre-State ($s$) | Tactic ($\tau$) | Technique ($k$) | Tool ($u$) | Post-State ($s'$) | Verified Command ($c$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `mimikatz` | `s_interactive_tty_or_priv_escalated` | `Mimikatz Authors: @gentilkiwi and Vincent LE TOUX` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `hexdump` | `s_passive_topology_mapped` | `hexdump -ve '/1 "0x%02x,"' file.bin \|sed 's/.$//'` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `invoke-wmicommand` | `s_credentials_or_certs_acquired` | `Invoke-WmiCommand executes a PowerShell code on a` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `out-minidump` | `s_active_services_enumerated` | `Out-Minidump generates a full-memory minidump of a` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `base64` | `s_interactive_tty_or_priv_escalated` | `base64 -w 0 powerkatz.dll, and replace the base64-DLL` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `get-process` | `s_passive_topology_mapped` | `Get-Process \| Out-Minidump -DumpFilePath C:\Temp` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `sekurlsa::logonpasswords` | `s_credentials_or_certs_acquired` | `sekurlsa::logonpasswords module.` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `new-userpersistenceoption` | `s_active_services_enumerated` | `New-UserPersistenceOption builds a user-land option` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `defaults` | `s_interactive_tty_or_priv_escalated` | `defaults to 100 -Threads <X>` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `mimikatz` | `s_credentials_or_certs_acquired` | `Mimikatz project, compile for both Win32 and x64,` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `new-elevatedpersistenceoption` | `s_active_services_enumerated` | `New-ElevatedPersistenceOption builds an elevated` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `strings` | `s_credentials_or_certs_acquired` | `strings in Invoke-Mimikatz.` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `invoke-tokenmanipulation` | `s_credentials_or_certs_acquired` | `Invoke-TokenManipulation manipulates tokens and is` |

## Verified Executable Commands (Grouped by Capability Layer)

### General_System (13 commands)
```bash
Mimikatz Authors: @gentilkiwi and Vincent LE TOUX
hexdump -ve '/1 "0x%02x,"' file.bin |sed 's/.$//'
Invoke-WmiCommand executes a PowerShell code on a
sekurlsa::logonpasswords module.
Mimikatz project, compile for both Win32 and x64,
base64 -w 0 powerkatz.dll, and replace the base64-DLL
strings in Invoke-Mimikatz.
Invoke-TokenManipulation manipulates tokens and is
Out-Minidump generates a full-memory minidump of a
Get-Process | Out-Minidump -DumpFilePath C:\Temp
New-UserPersistenceOption builds a user-land option
New-ElevatedPersistenceOption builds an elevated
defaults to 100 -Threads <X>
```

