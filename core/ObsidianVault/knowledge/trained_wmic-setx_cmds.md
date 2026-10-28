---
title: "Trained Knowledge & Topology: WMIC-Setx CMDs.txt"
tags:
  - credential_access
  - enumeration
  - lateral_movement_routing_pivot
  - mdp
  - passive_enum
  - powershell
  - text
  - trained
  - wireshark
  - wmic
source_file: WMIC-Setx CMDs.txt
doc_type: text
updated: 2026-10-24 01:01:12
---

# Trained Knowledge & Architecture: `WMIC-Setx CMDs.txt`

- **Source Path:** `~/Projects/CORA/Training/WMIC-Setx CMDs.txt` (`text`)
- **Extracted Technical Entities:** `powershell, wireshark, wmic`
- **Extracted IPs / Subnets:** `172.24.11.11, 172.24.11.12`
- **Extracted Interfaces:** `None`
- **Linked Command Playbook:** [[commands/trained_wmic-setx_cmds]] (`15` CEGAR-verified commands | `15` MDP transitions)

## Command & Tactic Coverage Summary
- **Total CEGAR-Verified Commands:** `15` (full executable list in [[commands/trained_wmic-setx_cmds]])
- **Tactic Distribution:** `Passive_Enum` (5), `Enumeration` (4), `Lateral_Movement_Routing_Pivot` (4), `Credential_Access` (2)
- **Top Extracted CLI Tools:** `dir` (4), `setx` (4), `wmic` (3), `psexec` (2), `del` (1), `type` (1)

## LLM Distilled Operational Summary
### Operational Techniques & Decision Workflows
*   **Remote Execution via PsExec**: Establish remote command execution on target hosts (e.g., `172.24.11.12`) using PsExec with specific user credentials (`xp\administrator`) and the `-accepteula` flag to bypass license prompts. Supports both `cmd.exe` and `powershell.exe` shells.
*   **System-Wide Environment Variable Injection**: Utilize `setx /s` (system-wide) to modify environment variables across a remote machine (`xp.ops.local`). This includes setting custom `PATH` entries, defining custom `PROMPT` strings, and configuring `DOWNLOAD` directories.
*   **Local Directory Enumeration & Filtering**: Use `dir` with `/on` (one line per file) and `/ah` (all files) flags to list Windows directories. Redirect output (`>`, `>>`) to text files for sorting.
*   **Data Sorting & Cleanup**: Apply `sort` with offset parameters (`/n` or `/+12`) to extract specific columns from text files. Use `del` with wildcards (`*.*`) to clear temporary data files after processing.
*   **WMIC Remote Inventory**: Query remote computer system details using `wmic /node:<IP> /user:<domain>\<user>` with `list brief /format:list` for structured output.

### Critical Command Patterns & Required Flags
*   **`setx` System Scope**: `/s` (System), `/u` (User), `/p` (Password).
    *   *Example*: `setx /s <hostname> /u <domain>\<user> /p <pass> PATH "<new_path>" /M`
*   **`psexec` Remote Shell**: `-accepteula` (Accept EULA), `-u` (User), `-p` (Password).
    *   *Example*: `psexec \\<IP> -accepteula -u <user> -p <pass> cmd.exe`
*   **`dir` Enumeration**: `/on` (One line per file), `/ah` (All files, including hidden).
    *   *Example*: `dir C:\windows /on /ah > output.txt`
*   **`sort` Column Extraction**: `/+<offset>` (Start sorting from Nth byte/character).
    *   *Example*: `sort /+12 < file.txt`

### Network Topology & Service Relationships
*   **Target Hosts**:
    *   `172.24.11.11`: Remote computer system inventory target.
    *   `172.24.11.12`: Primary remote execution target for PsExec commands.
    *   `xp.ops.local`: Hostname used for system-wide `setx` operations.
*   **Credentials**: Domain user `xp\administrator` with password `L33tHax0r` is required for remote access and system variable modification.
*   **Services/Tools**:
    *   **WMIC**: Used for remote hardware/software inventory (`computersystem`).
    *   **PsExec**: Used for remote process execution and shell spawning.
    *   **Notepad++**: Launched via `

