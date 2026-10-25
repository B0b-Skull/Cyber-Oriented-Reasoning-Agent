---
title: "Trained Command Playbook: Findstr.pdf"
tags:
  - https
  - mdp
  - passive_enum
  - pdf
  - trained
source_file: Findstr.pdf
updated: 2026-10-25 00:58:23
---

# Trained Command Playbook: `Findstr.pdf`

- **Source Document:** `~/Projects/CORA/Training/Findstr.pdf`
- **CEGAR Verified Commands:** `9` (`0` malformed/unsafe snippets filtered)
- **MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`):** `9`
- **Discovered IPs/Subnets:** `None`
- **Discovered Interfaces:** `None`
- **Related Knowledge Note:** [[knowledge/trained_findstr]]

## Distilled MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`)
| Pre-State ($s$) | Tactic ($\tau$) | Technique ($k$) | Tool ($u$) | Post-State ($s'$) | Verified Command ($c$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `findstr` | `s_passive_topology_mapped` | `findstr [/b] [/e] [/l] [/r] [/s] [/i] [/x] [/v] [/n] [/m] [/o] [/p] [/offline] [/g:file] [/f:file] [/c:string] [/d:dirlist] [/a:ColorAttribute]` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `findstr` | `s_passive_topology_mapped` | `findstr "hello there" x.y` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `findstr` | `s_passive_topology_mapped` | `findstr /c:"hello there" x.y` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `findstr` | `s_passive_topology_mapped` | `findstr Windows proposal.txt` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `findstr` | `s_passive_topology_mapped` | `findstr /s /i Windows *.*` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `findstr` | `s_passive_topology_mapped` | `findstr /b /n /c:" *FOR" *.bas` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `findstr` | `s_passive_topology_mapped` | `findstr /g:finddata.txt /f:filelist.txt > results.out` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `findstr` | `s_passive_topology_mapped` | `findstr /s /i /m "\<computer\>" *.*` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `findstr` | `s_passive_topology_mapped` | `findstr /s /i /m "\<comp.*" *.*` |

## Verified Executable Commands (Grouped by Capability Layer)

### General_System (9 commands)
```bash
findstr [/b] [/e] [/l] [/r] [/s] [/i] [/x] [/v] [/n] [/m] [/o] [/p] [/offline] [/g:file] [/f:file] [/c:string] [/d:dirlist] [/a:ColorAttribute]
findstr "hello there" x.y
findstr /c:"hello there" x.y
findstr Windows proposal.txt
findstr /s /i Windows *.*
findstr /b /n /c:" *FOR" *.bas
findstr /g:finddata.txt /f:filelist.txt > results.out
findstr /s /i /m "\<computer\>" *.*
findstr /s /i /m "\<comp.*" *.*
```

