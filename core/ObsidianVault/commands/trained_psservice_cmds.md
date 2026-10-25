---
title: "Trained Command Playbook: PsService CMDs.txt"
tags:
  - mdp
  - passive_enum
  - text
  - trained
source_file: PsService CMDs.txt
updated: 2026-10-25 01:00:11
---

# Trained Command Playbook: `PsService CMDs.txt`

- **Source Document:** `~/Projects/CORA/Training/PsService CMDs.txt`
- **CEGAR Verified Commands:** `12` (`0` malformed/unsafe snippets filtered)
- **MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`):** `12`
- **Discovered IPs/Subnets:** `None`
- **Discovered Interfaces:** `None`
- **Related Knowledge Note:** [[knowledge/trained_psservice_cmds]]

## Distilled MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`)
| Pre-State ($s$) | Tactic ($\tau$) | Technique ($k$) | Tool ($u$) | Post-State ($s'$) | Verified Command ($c$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `psservice` | `s_passive_topology_mapped` | `psservice \\xp.ops.local -u xp\Administrator -p L33tHax0r` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `psservice` | `s_passive_topology_mapped` | `psservice \\xp.ops.local -u xp\Administrator -p L33tHax0r query "Security Center"` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `psservice` | `s_passive_topology_mapped` | `psservice \\xp.ops.local -u xp\Administrator -p L33tHax0r query wscsvc` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `psservice` | `s_passive_topology_mapped` | `psservice \\xp.ops.local -u xp\administrator -p L33tHax0r query -s all` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `psservice` | `s_passive_topology_mapped` | `psservice stop W32time` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `psservice` | `s_passive_topology_mapped` | `psservice query W32time` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `psservice` | `s_passive_topology_mapped` | `psservice start W32time` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `psservice` | `s_passive_topology_mapped` | `psservice config "Windows Event Collector"` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `psservice` | `s_passive_topology_mapped` | `psservice config "Windows Update"` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `psservice` | `s_passive_topology_mapped` | `psservice config "Security Center"` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `psservice` | `s_passive_topology_mapped` | `psservice config "Parental Control"` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `psservice` | `s_passive_topology_mapped` | `psservice setconfig wpcsvc auto` |

## Verified Executable Commands (Grouped by Capability Layer)

### General_System (12 commands)
```bash
psservice \\xp.ops.local -u xp\Administrator -p L33tHax0r
psservice \\xp.ops.local -u xp\Administrator -p L33tHax0r query "Security Center"
psservice \\xp.ops.local -u xp\Administrator -p L33tHax0r query wscsvc
psservice \\xp.ops.local -u xp\administrator -p L33tHax0r query -s all
psservice stop W32time
psservice query W32time
psservice start W32time
psservice config "Windows Event Collector"
psservice config "Windows Update"
psservice config "Security Center"
psservice config "Parental Control"
psservice setconfig wpcsvc auto
```

