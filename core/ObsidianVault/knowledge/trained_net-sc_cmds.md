---
title: "Trained Knowledge & Topology: Net-SC CMDs.txt"
tags:
  - defense_evasion_firewall
  - enumeration
  - lateral_movement_routing_pivot
  - mdp
  - passive_enum
  - privilege_escalation
  - text
  - trained
source_file: Net-SC CMDs.txt
doc_type: text
updated: 2026-10-25 00:59:23
---

# Trained Knowledge & Architecture: `Net-SC CMDs.txt`

- **Source Path:** `~/Projects/CORA/Training/Net-SC CMDs.txt` (`text`)
- **Extracted Technical Entities:** `general`
- **Extracted IPs / Subnets:** `None`
- **Extracted Interfaces:** `None`
- **Linked Command Playbook:** [[commands/trained_net-sc_cmds]] (`25` CEGAR-verified commands | `25` MDP transitions)

## Command & Tactic Coverage Summary
- **Total CEGAR-Verified Commands:** `25` (full executable list in [[commands/trained_net-sc_cmds]])
- **Tactic Distribution:** `Defense_Evasion_Firewall` (13), `Passive_Enum` (4), `Enumeration` (3), `Privilege_Escalation` (3), `Lateral_Movement_Routing_Pivot` (2)
- **Top Extracted CLI Tools:** `sc` (13), `net` (9), `driverquery` (3)

## LLM Distilled Operational Summary
### Key Operational Techniques & Decision Workflows
*   **Service Discovery & Filtering**: Use `driverquery /si` combined with `findstr` to identify security drivers or services running with specific states (e.g., `TRUE`).
*   **Service State Management**: Execute `sc start/stop/pause/continue` or `net start/stop/pause/continue` to dynamically control service lifecycles.
*   **Configuration Changes**: Apply persistent state changes using `sc config <service_name> start= <auto/manual/disabled>`.
*   **Remote Administration**: Utilize `sc \\<hostname> <command>` syntax to manage services on remote machines (e.g., `xp.ops.local`).
*   **Key Retrieval**: Extract service display names via `sc getkeyname` for accurate command targeting.

### Critical Command Patterns & Required Flags
*   **Service Query**: `sc queryex type= service state= all` (filters by state), `sc qc <service>` (quick config).
*   **Driver Inspection**: `driverquery /si` (shows installed drivers with signatures).
*   **Time Service Specifics**: `sc query | findstr "Time"` or `sc queryex ... find /i "Time"`.
*   **Remote Execution**: Prefix commands with `sc \\<target> ` (e.g., `sc \\xp.ops.local query`).
*   **Alias Handling**: Commands like `net start` accept service names directly; `sc config` requires the internal name or display name.

### Network Topology & Service Relationships
*   **Target Host**: `xp.ops.local` is identified as a remote management target for specific services (e.g., Windows Firewall/ICS).
*   **Core Services Mentioned**:
    *   **Print Spooler**: Managed via `net start` or `sc config ... start= disabled`.
    *   **Remote Registry**: Enabled via `net start`.
    *   **Time Service (w32time)**: Queried for synchronization status.
    *   **Network Connections/Netman**: Managed via `sc qc Netman`.
    *   **Audio/UMRDP**: Audio service (`audiosrv`) and UMRDP service (`umrdpservice`) have start/stop aliases.
    *   **LanmanWorkstation**: Configured via `sc qc LanmanWorkstation`.
*   **Telnet**: Requires explicit continuation (`net continue telnet`) after interruption.

