---
title: "Trained Command Playbook: CQC001_E020_M010_Sysinternals_Tools.pdf"
tags:
  - credential_access
  - enumeration
  - lateral_movement_routing_pivot
  - listdlls
  - mdp
  - passive_enum
  - pdf
  - powershell
  - protocol_chaining
  - pslist
  - sysinternals
  - trained
  - wevtutil
  - wmic
source_file: CQC001_E020_M010_Sysinternals_Tools.pdf
updated: 2026-10-25 00:57:31
---

# Trained Command Playbook: `CQC001_E020_M010_Sysinternals_Tools.pdf`

- **Source Document:** `~/Projects/CORA/Training/CQC001_E020_M010_Sysinternals_Tools.pdf`
- **CEGAR Verified Commands:** `14` (`0` malformed/unsafe snippets filtered)
- **MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`):** `14`
- **Discovered IPs/Subnets:** `None`
- **Discovered Interfaces:** `None`
- **Related Knowledge Note:** [[knowledge/trained_cqc001_e020_m010_sysinternals_tools]]

## Distilled MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`)
| Pre-State ($s$) | Tactic ($\tau$) | Technique ($k$) | Tool ($u$) | Post-State ($s'$) | Verified Command ($c$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `wmic` | `s_passive_topology_mapped` | `wmic datafile where` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `tasklist` | `s_credentials_or_certs_acquired` | `tasklist / taskkill` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `last` | `s_active_services_enumerated` | `last 24` |
| `s_firewall_or_acl_unlocked` | **`Lateral_Movement_Routing_Pivot`** | Remote Host Execution, L2/L3 Route Injection & Subnet Pivot | `psexec` | `s_cross_subnet_pivot_routed` | `psexec @run_file [options]` |
| `s_credentials_or_certs_acquired` | **`Protocol_Chaining`** | Multi-Protocol Handshake & Tunnel Relay Chaining | `invoke-command` | `s_protocol_chain_established` | `Invoke-Command -ComputerName` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `listdlls` | `s_passive_topology_mapped` | `listdlls [-r] [-v \| -u]` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `wmic` | `s_credentials_or_certs_acquired` | `wmic useraccount where` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `listdlls` | `s_passive_topology_mapped` | `listdlls [-r] [-v] [-d dllname]` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `psloglist` | `s_credentials_or_certs_acquired` | `psloglist [- ]` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `listdlls` | `s_passive_topology_mapped` | `listdlls -v` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `wevtutil` | `s_credentials_or_certs_acquired` | `wevtutil <command>` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `tasklist` | `s_passive_topology_mapped` | `tasklist /m /fi "imagename eq outlook.exe"` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `psloggedon` | `s_passive_topology_mapped` | `psloggedon [- ] [-l] [-x]` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `psloglist` | `s_passive_topology_mapped` | `Psloglist - a tool to parse` |

## Verified Executable Commands (Grouped by Capability Layer)

### General_System (14 commands)
```bash
wmic datafile where
tasklist / taskkill
wmic useraccount where
listdlls [-r] [-v | -u]
listdlls [-r] [-v] [-d dllname]
listdlls -v
tasklist /m /fi "imagename eq outlook.exe"
psloggedon [- ] [-l] [-x]
Psloglist - a tool to parse
psloglist [- ]
wevtutil <command>
last 24
psexec @run_file [options]
Invoke-Command -ComputerName
```

