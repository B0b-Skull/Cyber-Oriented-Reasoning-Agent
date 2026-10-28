---
title: "Trained Command Playbook: BCF_Windows Process Investigation.pdf"
tags:
  - mdp
  - netstat
  - passive_enum
  - pdf
  - post_exploitation_verification
  - powershell
  - trained
  - wmic
source_file: BCF_Windows Process Investigation.pdf
updated: 2026-10-24 00:56:56
---

# Trained Command Playbook: `BCF_Windows Process Investigation.pdf`

- **Source Document:** `~/Projects/CORA/Training/BCF_Windows Process Investigation.pdf`
- **CEGAR Verified Commands:** `8` (`0` malformed/unsafe snippets filtered)
- **MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`):** `8`
- **Discovered IPs/Subnets:** `None`
- **Discovered Interfaces:** `None`
- **Related Knowledge Note:** [[knowledge/trained_bcf_windows_process_investigation]]

## Distilled MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`)
| Pre-State ($s$) | Tactic ($\tau$) | Technique ($k$) | Tool ($u$) | Post-State ($s'$) | Verified Command ($c$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `tasklist` | `s_passive_topology_mapped` | `tasklist /FI "IMAGENAME eq csrss.exe"` |
| `s_cross_subnet_pivot_routed` | **`Post_Exploitation_Verification`** | Post-Action Host Identity, Privilege & Objective Verification | `get-nettcpconnection` | `s_goal_verified_complete` | `Get-NetTCPConnection -OwningProcess <process_id>` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `wmic` | `s_passive_topology_mapped` | `wmic process where name="svchost.exe" get processId, commandline` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `get-wmiobject` | `s_passive_topology_mapped` | `Get-WmiObject win32_service \| where {$_.name -eq` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `netstat` | `s_passive_topology_mapped` | `netstat -ano\| findstr <process_id>` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `get-process` | `s_passive_topology_mapped` | `(Get-Process <process_name>).modules` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `get-childitem` | `s_passive_topology_mapped` | `$file = Get-ChildItem <path_to_exe>` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `get-childitem` | `s_passive_topology_mapped` | `Get-ChildItem -path C:\ -recurse \| where-object { $_.CreationTime.Date -eq` |

## Verified Executable Commands (Grouped by Capability Layer)

### General_System (7 commands)
```bash
tasklist /FI "IMAGENAME eq csrss.exe"
wmic process where name="svchost.exe" get processId, commandline
Get-WmiObject win32_service | where {$_.name -eq
Get-NetTCPConnection -OwningProcess <process_id>
(Get-Process <process_name>).modules
$file = Get-ChildItem <path_to_exe>
Get-ChildItem -path C:\ -recurse | where-object { $_.CreationTime.Date -eq
```

### L4_Port_Service (1 commands)
```bash
netstat -ano| findstr <process_id>
```

