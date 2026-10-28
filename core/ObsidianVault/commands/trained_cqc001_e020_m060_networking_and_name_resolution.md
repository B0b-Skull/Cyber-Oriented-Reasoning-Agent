---
title: "Trained Command Playbook: CQC001_E020_M060_Networking_and_Name_Resolution.pdf"
tags:
  - arp
  - credential_access
  - enumeration
  - http
  - https
  - ipconfig
  - listdlls
  - mdp
  - netsh
  - netstat
  - passive_enum
  - pdf
  - sysinternals
  - trained
source_file: CQC001_E020_M060_Networking_and_Name_Resolution.pdf
updated: 2026-10-24 00:57:34
---

# Trained Command Playbook: `CQC001_E020_M060_Networking_and_Name_Resolution.pdf`

- **Source Document:** `~/Projects/CORA/Training/CQC001_E020_M060_Networking_and_Name_Resolution.pdf`
- **CEGAR Verified Commands:** `22` (`0` malformed/unsafe snippets filtered)
- **MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`):** `22`
- **Discovered IPs/Subnets:** `None`
- **Discovered Interfaces:** `None`
- **Related Knowledge Note:** [[knowledge/trained_cqc001_e020_m060_networking_and_name_resolution]]

## Distilled MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`)
| Pre-State ($s$) | Tactic ($\tau$) | Technique ($k$) | Tool ($u$) | Post-State ($s'$) | Verified Command ($c$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `net` | `s_credentials_or_certs_acquired` | `net accounts` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `net` | `s_active_services_enumerated` | `net group` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `net` | `s_passive_topology_mapped` | `net localgroup` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `net` | `s_credentials_or_certs_acquired` | `net computer` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `net` | `s_active_services_enumerated` | `net helpmsg` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `net` | `s_passive_topology_mapped` | `net session` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `net` | `s_credentials_or_certs_acquired` | `net config` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `net` | `s_active_services_enumerated` | `net pause` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `net` | `s_passive_topology_mapped` | `net share` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `net` | `s_credentials_or_certs_acquired` | `net continue` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `net` | `s_active_services_enumerated` | `net stop` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `net` | `s_passive_topology_mapped` | `net start` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `net` | `s_credentials_or_certs_acquired` | `net file` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `net` | `s_active_services_enumerated` | `net time` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `net` | `s_passive_topology_mapped` | `net statistics` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `handle` | `s_credentials_or_certs_acquired` | `handle remote requests using local procedure calls.` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `net` | `s_passive_topology_mapped` | `net use` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `net` | `s_passive_topology_mapped` | `net user` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `net` | `s_passive_topology_mapped` | `net view` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `ipconfig` | `s_passive_topology_mapped` | `Ipconfig` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `listdlls` | `s_passive_topology_mapped` | `listdlls [-r] [-v \| -u] [processname\|pid]` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `listdlls` | `s_passive_topology_mapped` | `listdlls [-r] [-v] [-d dllname]` |

## Verified Executable Commands (Grouped by Capability Layer)

### General_System (21 commands)
```bash
net accounts
net computer
net config
net continue
net file
net group
net helpmsg
net localgroup
net pause
net session
net share
net start
net statistics
net stop
net time
net use
net user
net view
listdlls [-r] [-v | -u] [processname|pid]
listdlls [-r] [-v] [-d dllname]
handle remote requests using local procedure calls.
```

### L3_Routing_NAT (1 commands)
```bash
Ipconfig
```

