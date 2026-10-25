---
title: "Trained Command Playbook: PowerShell CMDs.txt"
tags:
  - mdp
  - passive_enum
  - powershell
  - text
  - trained
source_file: PowerShell CMDs.txt
updated: 2026-10-25 01:00:06
---

# Trained Command Playbook: `PowerShell CMDs.txt`

- **Source Document:** `~/Projects/CORA/Training/PowerShell CMDs.txt`
- **CEGAR Verified Commands:** `4` (`0` malformed/unsafe snippets filtered)
- **MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`):** `4`
- **Discovered IPs/Subnets:** `None`
- **Discovered Interfaces:** `None`
- **Related Knowledge Note:** [[knowledge/trained_powershell_cmds]]

## Distilled MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`)
| Pre-State ($s$) | Tactic ($\tau$) | Technique ($k$) | Tool ($u$) | Post-State ($s'$) | Verified Command ($c$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `get-service` | `s_passive_topology_mapped` | `Get-Service \| Where-Object {$_.displayName.StartsWith("NATION-")} \| Select name` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `get-service` | `s_passive_topology_mapped` | `Get-Service \| Where-Object {$_.displayName.StartsWith("NATION-")} \| Stop-Service` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `get-service` | `s_passive_topology_mapped` | `Get-Service \| Where-Object {$_.displayName.StartsWith("NATION-")} \| Start-Service` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `get-service` | `s_passive_topology_mapped` | `Get-Service \| Where-Object {$_.displayName.StartsWith("NATION-")} \| Restart-Service` |

## Verified Executable Commands (Grouped by Capability Layer)

### General_System (4 commands)
```bash
Get-Service | Where-Object {$_.displayName.StartsWith("NATION-")} | Select name
Get-Service | Where-Object {$_.displayName.StartsWith("NATION-")} | Stop-Service
Get-Service | Where-Object {$_.displayName.StartsWith("NATION-")} | Start-Service
Get-Service | Where-Object {$_.displayName.StartsWith("NATION-")} | Restart-Service
```

