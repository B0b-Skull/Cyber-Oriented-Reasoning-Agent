---
title: "Trained Command Playbook: FORFILES.txt"
tags:
  - mdp
  - passive_enum
  - text
  - trained
source_file: FORFILES.txt
updated: 2026-10-25 00:58:24
---

# Trained Command Playbook: `FORFILES.txt`

- **Source Document:** `~/Projects/CORA/Training/FORFILES.txt`
- **CEGAR Verified Commands:** `5` (`0` malformed/unsafe snippets filtered)
- **MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`):** `5`
- **Discovered IPs/Subnets:** `None`
- **Discovered Interfaces:** `None`
- **Related Knowledge Note:** [[knowledge/trained_forfiles]]

## Distilled MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`)
| Pre-State ($s$) | Tactic ($\tau$) | Technique ($k$) | Tool ($u$) | Post-State ($s'$) | Verified Command ($c$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `forfiles` | `s_passive_topology_mapped` | `forfiles /p c:\ /s /m *.bat /c "cmd /c echo @file is a batch file"` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `forfiles` | `s_passive_topology_mapped` | `forfiles /p c:\ /s /m *.* /c "cmd /c if @isdir==true echo @file is a directory"` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `forfiles` | `s_passive_topology_mapped` | `forfiles /s /m *.* /d -365 /c "cmd /c echo @file is at least one year old."` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `forfiles` | `s_passive_topology_mapped` | `forfiles /s /m *.* /d -01/01/2007 /c "cmd /c echo @file is outdated."` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `forfiles` | `s_passive_topology_mapped` | `forfiles /s /m *.* /c "cmd /c echo The extension of @file is 0x09@ext"` |

## Verified Executable Commands (Grouped by Capability Layer)

### General_System (5 commands)
```bash
forfiles /p c:\ /s /m *.bat /c "cmd /c echo @file is a batch file"
forfiles /p c:\ /s /m *.* /c "cmd /c if @isdir==true echo @file is a directory"
forfiles /s /m *.* /d -365 /c "cmd /c echo @file is at least one year old."
forfiles /s /m *.* /d -01/01/2007 /c "cmd /c echo @file is outdated."
forfiles /s /m *.* /c "cmd /c echo The extension of @file is 0x09@ext"
```

