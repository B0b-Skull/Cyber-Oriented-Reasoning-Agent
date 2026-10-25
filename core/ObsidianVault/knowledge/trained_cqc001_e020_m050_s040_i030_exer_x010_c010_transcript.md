---
title: "Trained Knowledge & Topology: CQC001_E020_M050_S040_I030_Exer_X010_C010_transcript.txt"
tags:
  - listdlls
  - mdp
  - passive_enum
  - pslist
  - text
  - trained
source_file: CQC001_E020_M050_S040_I030_Exer_X010_C010_transcript.txt
doc_type: text
updated: 2026-10-25 00:57:33
---

# Trained Knowledge & Architecture: `CQC001_E020_M050_S040_I030_Exer_X010_C010_transcript.txt`

- **Source Path:** `~/Projects/CORA/Training/CQC001_E020_M050_S040_I030_Exer_X010_C010_transcript.txt` (`text`)
- **Extracted Technical Entities:** `listdlls, pslist`
- **Extracted IPs / Subnets:** `None`
- **Extracted Interfaces:** `None`
- **Linked Command Playbook:** [[commands/trained_cqc001_e020_m050_s040_i030_exer_x010_c010_transcript]] (`1` CEGAR-verified commands | `1` MDP transitions)

## Command & Tactic Coverage Summary
- **Total CEGAR-Verified Commands:** `1` (full executable list in [[commands/trained_cqc001_e020_m050_s040_i030_exer_x010_c010_transcript]])
- **Tactic Distribution:** `Passive_Enum` (1)
- **Top Extracted CLI Tools:** `pslist` (1)

## LLM Distilled Operational Summary
### Key Operational Techniques & Decision Workflows

*   **Process Enumeration**: Execute `pslist` to retrieve a comprehensive table of running processes, including Name, PID, Priority, Thread count, Handle count, Privilege level, and CPU/Time metrics. This establishes the baseline process landscape.
*   **Command Line Correlation**: Pipe `listdlls` output through `find /I "command"` to isolate and display the full command-line arguments for every loaded module. This reveals hidden startup parameters, service groupings (e.g., `-k DcomLaunch`), and specific instance configurations (e.g., DLL hosting via `/Processid`).
*   **Privilege & Handle Analysis**: Cross-reference the `pslist` output to identify high-handle-count processes (e.g., `lsass` with 24,736 handles) and high-privilege users (e.g., `System`, `LocalSystem`) to pinpoint potential attack vectors or resource exhaustion points.
*   **Service Grouping Verification**: Validate that `svchost.exe` instances are correctly grouped by their `-k` flags (e.g., `netsvcs`, `DcomLaunch`) to understand which services are co-located and potentially affected by a single process crash or injection.

### Critical Command Patterns and Required Flags

*   **Process List**: `pslist` (Standard output: Tab-separated values).
*   **Command Line Extraction**: `listdlls | find /I "command"` (Case-insensitive search for "command" in the command line column).
*   **Key Flags Observed**:
    *   `svchost.exe -k <Group>`: Defines the service group (e.g., `DcomLaunch`, `RPCSS`, `netsvcs`).
    *   `dllhost.exe /Processid={GUID}`: Indicates a COM+ application host running a specific component.
    *   `conhost.exe "GUID"`: Manages console host sessions with unique identifiers.

### Network Topology & Service Relationships

*   **Core System Services**: `smss.exe`, `csrss.exe`, `wininit.exe`, `winlogon.exe`, `services.exe`, `lsass.exe`, and `lsm.exe` form the initial Windows subsystem and session management layer.
*   **Network & Directory Services**:
    *   `dns.exe` (PID 1288): Primary DNS resolver service.
    *   `Microsoft.ActiveDirectory.WebServices` (PID 1212): Handles ADWS communication.
    *   `dfsrs.exe` / `dfssvc.exe`: Distributed File System Replication services.
*   **Remote Access**: `tlntsvr.exe` indicates Telnet server presence.
*   **User Interface & Shell**: `explorer.exe`, `dwm.exe` (Desktop Window Manager), and `taskhost.exe` manage the GUI environment.
*   **Third-Party**: `nortonav.exe` indicates active antivirus monitoring, which may interact with system hooks.

