---
title: "Trained Knowledge & Topology: CQC001_E020_M010_Sysinternals_Tools.pdf"
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
doc_type: pdf
updated: 2026-10-24 00:57:31
---

# Trained Knowledge & Architecture: `CQC001_E020_M010_Sysinternals_Tools.pdf`

- **Source Path:** `~/Projects/CORA/Training/CQC001_E020_M010_Sysinternals_Tools.pdf` (`pdf`)
- **Extracted Technical Entities:** `listdlls, powershell, pslist, sysinternals, wevtutil, wmic`
- **Extracted IPs / Subnets:** `None`
- **Extracted Interfaces:** `None`
- **Linked Command Playbook:** [[commands/trained_cqc001_e020_m010_sysinternals_tools]] (`14` CEGAR-verified commands | `14` MDP transitions)

## Command & Tactic Coverage Summary
- **Total CEGAR-Verified Commands:** `14` (full executable list in [[commands/trained_cqc001_e020_m010_sysinternals_tools]])
- **Tactic Distribution:** `Passive_Enum` (7), `Credential_Access` (4), `Enumeration` (1), `Lateral_Movement_Routing_Pivot` (1), `Protocol_Chaining` (1)
- **Top Extracted CLI Tools:** `listdlls` (3), `psloglist` (2), `tasklist` (2), `wmic` (2), `invoke-command` (1), `last` (1), `psexec` (1), `psloggedon` (1), `wevtutil` (1)

## LLM Distilled Operational Summary
### Operational Techniques & Decision Workflows

*   **Process & Memory Analysis**: Use `pslist` to enumerate processes, inspect virtual/physical memory (`-m`), or dump thread details (`-d`). Cross-reference with native `tasklist` or `wmic datafile`.
*   **User & SID Resolution**: Translate Security Identifiers (SIDs) to display names (or vice versa) for both local and domain accounts using `psgetsid`. Supports remote execution via `\\computer` or file-based batch execution (`@file`).
*   **DLL Loading Verification**: Identify loaded Dynamic Link Libraries within a specific process using `listdlls`. Filter by partial name, process ID, or specific DLL name. Use `-r` to detect relocated DLLs (potential tampering) and `-u` to find unsigned modules.
*   **Event Log Forensics**: Parse Windows Event Logs with `psloglist`. Filter by time windows (`-a`, `-b`, `-d`, `-h`, `-m`), specific Event IDs (`-i`, `-e`), log sources (`-o`, `-q`), and severity (`-f`). Supports clearing logs (`-c`) or monitoring live events (`-w`).
*   **Remote Execution**: Execute commands on remote systems using `psexec`. Requires File/Printer sharing enabled. Supports copying executables (`-c`), running elevated tokens (`-h`), and skipping profile loading (`-e`).

### Critical Command Patterns & Required Flags

| Tool | Key Flags | Purpose |
| :--- | :--- | :--- |
| **sigcheck** | `-d` | Verify digital signatures and certificate chains. |
| **pslist** | `-m`, `-d`, `-x` | Inspect memory, threads, or dump full process details. |
| **psgetsid** | `-u`, `-p` | Remote login (`-u`/`-p`) to query SIDs on target machines. |
| **listdlls** | `-r`, `-v`, `-u` | Detect relocated DLLs, show versions, or list unsigned modules. |
| **psloglist** | `-a`, `-b`, `-i`, `-o` | Filter by date range, Event ID, or source; `-c` to clear logs. |
| **psexec** | `-c`, `-h`, `-e` | Copy files (`-c`), run elevated (`-h`), skip profile load (`-e`). |

### Network Topology & Service Relationships

*   **Remote Execution Dependency**: `psexec` requires **File and Printer Sharing** to be enabled on the target remote system.
*   **Authentication Models**:
    *   **Local/Domain**: `psgetsid` and `psloglist` support both local and domain accounts.
    *   **Remote Login**: Tools like `psgetsid`, `psloglist`, and `psexec` accept remote computer names (`\\computer`) or lists from a file (`@file`).
    *   **Credentials**: Remote tools often require `-u` (username) and `-p` (password) flags for authentication, with passwords passed as clear text unless specified otherwise.
*   **Log Sources**: Event logs can be filtered by source name (e.g., `

