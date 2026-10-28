---
title: "Trained Knowledge & Topology: CQC001_E030_M050_Auditing_Tools.pdf"
tags:
  - auditpol
  - credential_access
  - defense_evasion_firewall
  - https
  - mdp
  - pdf
  - trained
source_file: CQC001_E030_M050_Auditing_Tools.pdf
doc_type: pdf
updated: 2026-10-24 00:57:38
---

# Trained Knowledge & Architecture: `CQC001_E030_M050_Auditing_Tools.pdf`

- **Source Path:** `~/Projects/CORA/Training/CQC001_E030_M050_Auditing_Tools.pdf` (`pdf`)
- **Extracted Technical Entities:** `auditpol, https`
- **Extracted IPs / Subnets:** `None`
- **Extracted Interfaces:** `None`
- **Linked Command Playbook:** [[commands/trained_cqc001_e030_m050_auditing_tools]] (`9` CEGAR-verified commands | `9` MDP transitions)

## Command & Tactic Coverage Summary
- **Total CEGAR-Verified Commands:** `9` (full executable list in [[commands/trained_cqc001_e030_m050_auditing_tools]])
- **Tactic Distribution:** `Defense_Evasion_Firewall` (8), `Credential_Access` (1)
- **Top Extracted CLI Tools:** `auditpol` (8), `psloglist` (1)

## LLM Distilled Operational Summary
### 1. Key Operational Techniques & Decision Workflows

*   **Windows XP/2003 Audit Configuration**: Use `AuditPol.exe` to enable/disable specific categories (System, Logon, Object, Privilege, Process, Policy, SAM) and options (Success, Failure, All, None).
    *   *Workflow*: Identify target category → Select success/failure scope → Execute `/enable` or `/disable` with specific flags (e.g., `/system:all`).
*   **Windows 7 Audit Configuration**: Use `AuditPol.exe` sub-commands for granular control.
    *   *Workflow*: Use `/get` to inspect current state, `/set` to apply changes, `/backup` to save policies, and `/clear` to reset.
*   **Event Log Analysis (Local/Remote)**: Use `EVENTQUERY.vbs` for flexible querying of local or remote systems.
    *   *Workflow*: Define target system (`/S`), select logs (`/L`), apply filters (`/FI`), and choose output format (`/FO`).
*   **Time-Based Log Extraction**: Use `PsLogList.exe` to dump logs within specific date ranges or filter by event ID.
    *   *Workflow*: Specify target machine, define start/end dates (`-a`, `-b`), or filter by ID (`-i`, `-e`).

### 2. Critical Command Patterns and Required Flags

**AuditPol.exe (Windows 7)**
*   `/get`: Display current audit policy.
*   `/set`: Apply new audit policy.
*   `/backup`: Save policy to file.
*   `/restore`: Load policy from file.
*   `/clear`: Reset policy to default.
*   `/remove`: Clear per-user audit policy.

**EVENTQUERY.vbs**
*   `/S <system>`: Target remote system.
*   `/U <user> /P <password>`: Authenticate for remote access.
*   `/L <logname>`: Specify log (e.g., `Security`, `System`, `Application`).
*   `/FI "Filter"`: Define filter logic (e.g., `"Type eq Error"`).
*   `/FO <format>`: Output format (`TABLE`, `LIST`, `CSV`).
*   `/R <range>`: Limit results (e.g., `10` for 10 most recent, `-10` for 10 oldest).
*   `/V`: Enable verbose output.

**PsLogList.exe**
*   `[\\computer]`: Target local or remote machine.
*   `-a <date>`: Dump records after date.
*   `-b <date>`: Dump records before date.
*   `-i <ID>`: Include specific Event IDs.
*   `-e <ID>`: Exclude specific Event IDs.
*   `-c`: Clear log after display.

### 3. Network Topology & Service Relationships

*   **Remote Execution**: Both `AuditPol` and `EVENTQUERY.vbs` support remote execution via the `\\ComputerName` syntax or `/S` flag, requiring valid credentials (`/U`, `/P`) for non-local targets.
*   **Log Sources**: Tools interact with standard Windows Event Logs: `System`, `

