---
title: "Trained Knowledge & Topology: Basic Survey Commands.txt"
tags:
  - arp
  - auditpol
  - autorunsc
  - defense_evasion_firewall
  - ipconfig
  - listdlls
  - mdp
  - netstat
  - passive_enum
  - powershell
  - pslist
  - sysinternals
  - text
  - trained
  - wmic
source_file: Basic Survey Commands.txt
doc_type: text
updated: 2026-10-24 00:56:13
---

# Trained Knowledge & Architecture: `Basic Survey Commands.txt`

- **Source Path:** `~/Projects/CORA/Training/Basic Survey Commands.txt` (`text`)
- **Extracted Technical Entities:** `arp, auditpol, autorunsc, ipconfig, listdlls, netstat, powershell, pslist, sysinternals, wmic`
- **Extracted IPs / Subnets:** `None`
- **Extracted Interfaces:** `None`
- **Linked Command Playbook:** [[commands/trained_basic_survey_commands]] (`39` CEGAR-verified commands | `39` MDP transitions)

## Command & Tactic Coverage Summary
- **Total CEGAR-Verified Commands:** `39` (full executable list in [[commands/trained_basic_survey_commands]])
- **Tactic Distribution:** `Passive_Enum` (38), `Defense_Evasion_Firewall` (1)
- **Top Extracted CLI Tools:** `reg` (10), `wmic` (7), `net` (4), `autorunsc` (2), `date` (2), `nbtstat` (2), `netstat` (2), `tasklist` (2), `auditpol` (1), `dir` (1), `ipconfig` (1), `listdlls` (1), `prompt` (1), `psloggedon` (1), `route` (1), `systeminfo` (1)

## LLM Distilled Operational Summary
### Operational Techniques & Decision Workflows

*   **Drive/Folder Tracking**: Use `prompt $P$B$D$B$T$G` to dynamically display the current drive, folder, date, and time for command lineage tracking.
*   **Process & Service Analysis**:
    *   Use `tasklist /v` or `tasklist /svc` for basic process lists.
    *   Leverage `wmic process get executablepath, processid, parentprocessid` to map process hierarchies.
    *   Filter services with `wmic service ... | findstr /i "auto" | findstr /i /v "c:\windows\\"` to identify non-standard auto-start binaries.
*   **Persistence & Startup Verification**:
    *   Check Registry Run keys via `reg query hklm\...\run` and `hkcu\...\run`.
    *   Use `autorunsc -b` (boot) and `autorunsc -l` (logon) to detect startup programs.
    *   Inspect `winlogon` shell settings with `reg query ... /v shell`.
*   **Network Topology & Sessions**:
    *   Identify NetBIOS names with `nbtstat -n` and active sessions with `nbtstat -s`.
    *   Map listening ports via `netstat -ano | findstr LIST` and established connections via `netstat -ano | findstr EST`.
    *   Determine domain/workgroup status by checking `tcpip\parameters` for the `NV Domain` key.
*   **User & Account Context**:
    *   Retrieve logged-on users using `wmic computersystem get username`, `psloggedon`, or `reg query ... hivelist`.
    *   Extract user SIDs and names via `wmic useraccount get name,sid`.

### Critical Command Patterns & Flags

*   **Sysinternals Utilities**: `pslist -x / -t` (extended process info), `autorunsc -b/-l`, `psloggedon`.
*   **Registry Queries**: Use `reg query <path>` for `HKLM`/`HKCU` keys related to `CurrentVersion\Run`, `Winlogon`, and `Session Manager`.
*   **File/Directory Timestamps**: `wmic fsdir` or `wmic datafile` with `/format:list` to retrieve creation/modification/access dates.
*   **System Characterization Script**: A consolidated command chain redirects multiple outputs (`date`, `time`, `systeminfo`, `ipconfig`, `arp`, `route`) into a single log file (`C:\sysinfo.txt`).

### Network Topology & Relationships

*   **NetBIOS Integration**: `nbtstat` reveals local NetBIOS name registration and active session states, indicating potential lateral movement paths.
*   **Domain vs. Workgroup**: The existence of the `NV Domain` key in `HKLM\SYSTEM\CurrentControlSet\Control\TCPip\Parameters` definitively indicates domain membership; absence implies workgroup mode.
*   **Service Pack & Hotfix Correlation**: `wmic os get servicepackmajorversion` and `wmic qfe list full` provide the baseline for patch management and vulnerability assessment.
*   **

