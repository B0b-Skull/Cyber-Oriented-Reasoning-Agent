---
title: "Trained Knowledge & Topology: Win Local CMDs.txt"
tags:
  - enumeration
  - lateral_movement_routing_pivot
  - listdlls
  - mdp
  - passive_enum
  - pslist
  - text
  - trained
  - wmic
source_file: Win Local CMDs.txt
doc_type: text
updated: 2026-10-24 01:01:12
---

# Trained Knowledge & Architecture: `Win Local CMDs.txt`

- **Source Path:** `~/Projects/CORA/Training/Win Local CMDs.txt` (`text`)
- **Extracted Technical Entities:** `listdlls, pslist, wmic`
- **Extracted IPs / Subnets:** `172.17.10.71, 172.17.10.78`
- **Extracted Interfaces:** `None`
- **Linked Command Playbook:** [[commands/trained_win_local_cmds]] (`56` CEGAR-verified commands | `56` MDP transitions)

## Command & Tactic Coverage Summary
- **Total CEGAR-Verified Commands:** `56` (full executable list in [[commands/trained_win_local_cmds]])
- **Tactic Distribution:** `Passive_Enum` (40), `Lateral_Movement_Routing_Pivot` (14), `Enumeration` (2)
- **Top Extracted CLI Tools:** `listdlls` (15), `tasklist` (12), `handle` (10), `pslist` (9), `pskill` (3), `wmic` (3), `taskkill` (2), `telnet` (2)

## LLM Distilled Operational Summary
### Operational Techniques & Decision Workflows

*   **Remote Enumeration**: Use `tasklist /s <IP>` or `pslist \\<IP>` to list processes/services on remote hosts. Always append `/u <domain>\<user> -p <password>` for authentication.
*   **Process Filtering**: Filter by session (`/fi "SESSION eq 1"`), service state (`/fi "services eq bfe"`), or specific image name (`/im`).
*   **Process Termination**: Use `taskkill /im <name>` or `/pid <ID>`. For remote targets, include connection strings (e.g., `\\xp.ops.local`).
*   **DLL Analysis**: Use `listdlls <PID>` or `<executable>` to inspect loaded modules. Apply `-d` for detailed output and `-v` for verbose flags. Pipe output (`| more`) if the buffer overflows.
*   **Handle Attachments**: Use `handle -p <executable>` to find handles for a process name, or `handle -a -p <PID>` to attach to a specific process ID.
*   **Parent Process Discovery**: Use `wmic process where (processid=<ID>) get parentprocessid` to trace execution chains.

### Critical Command Patterns & Flags

| Tool | Pattern | Key Flags/Notes |
| :--- | :--- | :--- |
| **tasklist** | `/s <IP>`, `/im`, `/pid`, `/fi`, `/svc`, `/m`, `/v` | `/s` for remote, `/m` for modules, `/fi` for filters. |
| **taskkill** | `/im <name>`, `/pid <ID>`, `/s <IP>` | `/s` required for remote termination. |
| **pslist** | `\\<IP>`, `/dm`, `/x`, `/t`, `/r <count>` | `/dm` for domain members, `/x` for 32-bit, `/t` for tree view. |
| **pskill** | `- <IP>/<User>/<Pass> <PID>`, `-t` | `-t` for tree kill, `-` prefix for remote targets. |
| **handle** | `-p <exe>`, `-a <exe>`, `-s <PID>` | `-p` finds handles, `-a` attaches, `-s` suspends. |
| **listdlls** | `<PID>`, `<exe>`, `-d`, `-v`, `-u` | `-d` details, `-v` verbose, `-u` unloadable. |
| **wmic** | `process where ...`, `cpu get ...` | Query specific WMI classes for hardware/process data. |

### Network Topology & Relationships

*   **Target Hosts**:
    *   `xp.ops.local` (Domain: `xp.ops.local`)
    *   `win7.ops.local`
    *   `www.ops.local`
    *   `172.17.10.71` (User: `drytortugas\administrator`, Pass: `$eCret`)
    *   `172.17.10.78` (User: `Administrator`, Pass: `KeyF@rg0`)
*

