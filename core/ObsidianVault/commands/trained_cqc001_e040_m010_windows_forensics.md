---
title: "Trained Command Playbook: CQC001_E040_M010_Windows_Forensics.pdf"
tags:
  - http
  - https
  - mdp
  - netstat
  - passive_enum
  - pdf
  - pslist
  - sysinternals
  - trained
  - wmic
source_file: CQC001_E040_M010_Windows_Forensics.pdf
updated: 2026-10-25 00:57:54
---

# Trained Command Playbook: `CQC001_E040_M010_Windows_Forensics.pdf`

- **Source Document:** `~/Projects/CORA/Training/CQC001_E040_M010_Windows_Forensics.pdf`
- **CEGAR Verified Commands:** `10` (`0` malformed/unsafe snippets filtered)
- **MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`):** `10`
- **Discovered IPs/Subnets:** `None`
- **Discovered Interfaces:** `None`
- **Related Knowledge Note:** [[knowledge/trained_cqc001_e040_m010_windows_forensics]]

## Distilled MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`)
| Pre-State ($s$) | Tactic ($\tau$) | Technique ($k$) | Tool ($u$) | Post-State ($s'$) | Verified Command ($c$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `date` | `s_passive_topology_mapped` | `date` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `net` | `s_passive_topology_mapped` | `net session` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `psloglist` | `s_passive_topology_mapped` | `psloglist "Security" -i 528 -s \| find /i "Logon Type: 10"` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `net` | `s_passive_topology_mapped` | `net statistics` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `systeminfo` | `s_passive_topology_mapped` | `systeminfo` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `dir` | `s_passive_topology_mapped` | `dir /t displays: W Last written` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `sc` | `s_passive_topology_mapped` | `sc qc service_name Provides configuration information for a service.` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `sc` | `s_passive_topology_mapped` | `sc query state= all will output all installed services, whether running or stopped.` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `sc` | `s_passive_topology_mapped` | `sc query state= inactive will output only stopped services.` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `sc` | `s_passive_topology_mapped` | `sc query state= inactive \| findstr "DISPLAY_NAME"` |

## Verified Executable Commands (Grouped by Capability Layer)

### General_System (10 commands)
```bash
date
net session
psloglist "Security" -i 528 -s | find /i "Logon Type: 10"
net statistics
systeminfo
dir /t displays: W Last written
sc qc service_name Provides configuration information for a service.
sc query state= all will output all installed services, whether running or stopped.
sc query state= inactive will output only stopped services.
sc query state= inactive | findstr "DISPLAY_NAME"
```

