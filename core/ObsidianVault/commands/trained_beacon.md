---
title: "Trained Command Playbook: Beacon.pdf"
tags:
  - credential_access
  - enumeration
  - http
  - https
  - kerberos
  - lateral_movement_routing_pivot
  - mdp
  - mimikatz
  - pdf
  - powershell
  - reconnaissance
  - trained
source_file: Beacon.pdf
updated: 2026-10-25 00:56:56
---

# Trained Command Playbook: `Beacon.pdf`

- **Source Document:** `~/Projects/CORA/Training/Beacon.pdf`
- **CEGAR Verified Commands:** `6` (`0` malformed/unsafe snippets filtered)
- **MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`):** `6`
- **Discovered IPs/Subnets:** `None`
- **Discovered Interfaces:** `None`
- **Related Knowledge Note:** [[knowledge/trained_beacon]]

## Distilled MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`)
| Pre-State ($s$) | Tactic ($\tau$) | Technique ($k$) | Tool ($u$) | Post-State ($s'$) | Verified Command ($c$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `ls` | `s_active_services_enumerated` | `ls <C:\Path>` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `sekurlsa::logonpasswords` | `s_credentials_or_certs_acquired` | `sekurlsa::logonpasswords module which extracts hashes` |
| `s_init_unknown` | **`Reconnaissance`** | Domain, DNS, OSINT & Target Footprint Reconnaissance | `script` | `s_passive_topology_mapped` | `script imported from above using powershell.exe. Then` |
| `s_firewall_or_acl_unlocked` | **`Lateral_Movement_Routing_Pivot`** | Remote Host Execution, L2/L3 Route Injection & Subnet Pivot | `type` | `s_cross_subnet_pivot_routed` | `type to be windows/foreign/reverse_http[s] and input` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `powershell` | `s_active_services_enumerated` | `PowerShell .ps1 script from the control server and save it` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `lsadump::dcync` | `s_credentials_or_certs_acquired` | `lsadump::dcync to extract the hash for the specified user` |

## Verified Executable Commands (Grouped by Capability Layer)

### General_System (6 commands)
```bash
ls <C:\Path>
sekurlsa::logonpasswords module which extracts hashes
lsadump::dcync to extract the hash for the specified user
PowerShell .ps1 script from the control server and save it
script imported from above using powershell.exe. Then
type to be windows/foreign/reverse_http[s] and input
```

