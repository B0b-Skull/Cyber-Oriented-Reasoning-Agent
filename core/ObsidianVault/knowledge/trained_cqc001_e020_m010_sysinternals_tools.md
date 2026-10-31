---
title: "Trained Knowledge & Topology: CQC001 E020 M010 Sysinternals Tools"
category: knowledge
domain_hub: "[[knowledge/01_windows_system_process_and_sysinternals]]"
os_platform: windows
primary_tactic: Passive_Enum
summary: "Operational architecture, decision workflows & Windows/Linux command reference for CQC001 E020 M010 Sysinternals Tools: Windows live incident response, process tree/PPID investigation, service binary auditing, kernel architecture, file searching (fin"
when_to_apply: "Apply when working with CQC001 E020 M010 Sysinternals Tools (windows): Apply when performing initial Windows host triage (s_init_unknown), investigating running processes/PPIDs, mapping svchost.exe services, hunting unsigned/injected DLLs, searching files by timestamp/content, or executing Sysinternals live response."
tags: [credential_access, enumeration, lateral_movement_routing_pivot, listdlls, mdp, passive_enum, pdf, powershell, protocol_chaining, pslist, sysinternals, trained, wevtutil, wmic, windows, autorunsc, psservice, psloggedon, handle, sigcheck, accesschk, procdump]
source_file: "CQC001 E020 M010 Sysinternals Tools"
updated: 2026-10-30
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

<!-- CORA-MAXIMIZED-COMMANDS-START -->
## Maximized Windows & Linux Command Examples for `CQC001 E020 M010 Sysinternals Tools`

> **Domain Hub:** [[knowledge/01_windows_system_process_and_sysinternals|Domain Hub 01: Windows Live Response, Processes, Services, Kernel & Sysinternals Suite]]  
> **Master Playbooks:** [[commands/windows_master_command_playbook]] | [[commands/linux_master_command_playbook]] | [[commands/curl_playbook]] | [[commands/tio_serial_playbook]]  
> **When to Apply:** Apply when performing initial Windows host triage (s_init_unknown), investigating running processes/PPIDs, mapping svchost.exe services, hunting unsigned/injected DLLs, searching files by timestamp/content, or executing Sysinternals live response.  
> **15-Engine H-MDP State Transition:** `s_init_unknown` $\xrightarrow{\text{Passive_Enum}}$ `s_passive_topology_mapped` | **Bayesian Root-Cause Triggers:** `suspicious_process_lineage, service_misconfiguration, unsigned_dll_injection, resource_exhaustion` | **Isolation:** `RED, BLUE, WHITE (100% local host telemetry compatible)`

| Primary Command (`Windows` / `Linux`) | OS / Shell | What It Does & Key Flags | When to Apply & Expected Output | Cross-Platform Equivalent |
| :--- | :--- | :--- | :--- | :--- |
| `systeminfo && whoami /all` | **Windows CMD** | Displays OS build, patch hotfixes (KBs), boot time, current user SID, group memberships, and token privileges (`SeDebugPrivilege`, `SeImpersonatePrivilege`). | Apply first on any Windows host (`s_init_unknown`) to establish OS baseline and privilege level. | `uname -a && id && sudo -l` |
| `tasklist /v && tasklist /svc` | **Windows CMD** | Lists all running processes with user context, memory, window titles (`/v`), and maps every `svchost.exe` PID to hosted Windows Service names (`/svc`). | Apply to identify which service inside `svchost.exe` owns a socket or high CPU thread. | `ps auxef && systemctl list-units --type=service --state=running` |
| `wmic process get ProcessId,ParentProcessId,Name,ExecutablePath,CommandLine /format:list` | **Windows CMD** | Extracts full process lineage (`PID` + `PPID`), binary disk path, and full command-line arguments for every process. | Apply to uncover hidden/encoded PowerShell arguments and anomalous parent-child process trees (e.g., `cmd.exe` spawned by `w3wp.exe`). | `ps -eo pid,ppid,user,args --forest` |
| `pslist -accepteula -t && psloggedon -accepteula` | **Sysinternals** | Prints hierarchical parent-child process tree (`-t`) and enumerates both local interactive and SMB network logon sessions. | Apply during live response to trace process trees and active user sessions. | `pstree -p -a && w` |
| `listdlls -accepteula -u && sigcheck -accepteula -e -u -vr C:\Windows\System32` | **Sysinternals** | Lists all unsigned DLLs (`listdlls -u`) loaded into running processes and scans `System32` for unsigned executables (`sigcheck -e -u`). | Apply when hunting DLL hijacking, process hollowing, or trojanized system binaries. | `grep -E '\.so' /proc/*/maps && debsums -c` |
| `handle -accepteula -a -u && tcpvcon -accepteula -a -c -n` | **Sysinternals** | Enumerates all open file/registry/mutant handles (`handle -a -u`) and dumps CSV socket-to-process mappings (`tcpvcon`). | Apply to identify malware mutexes (`BaseNamedObjects`), locked files, or进程-bound network sockets. | `lsof -i -P -n && lsof` |
| `sc query state= all && sc qc <ServiceName>` | **Windows CMD** | Lists all installed services (running/stopped) and inspects `BINARY_PATH_NAME`, `START_TYPE`, and `SERVICE_START_NAME`. | Apply to audit service binaries and check for unquoted service paths or writable service executables. | `systemctl status <service> && systemctl cat <service>` |
| `forfiles /p C:\ /s /m *.exe /d -7 /c "cmd /c echo @path @fdate @ftime"` | **Windows CMD** | Recursively (`/s`) locates executables modified within the last 7 days (`/d -7`) across drive `C:\`. | Apply during incident triage to find recently dropped binaries or staging scripts. | `find / -xdev -mtime -7 -type f -ls 2>/dev/null` |
| `findstr /s /i /n "password secret connectionString" C:\Users\*.txt C:\Users\*.ps1 C:\inetpub\*.config` | **Windows CMD** | Recursive (`/s`), case-insensitive (`/i`), line-numbered (`/n`) string search across text, script, and web config files. | Apply when auditing configuration files for plaintext credentials or API keys. | `grep -rnI -iE 'password\|secret' /var/www /home /etc 2>/dev/null` |
| `procdump -accepteula -ma <PID> C:\Temp\proc_<PID>.dmp` | **Sysinternals** | Captures a complete memory dump (`-ma`) of target process `<PID>` for strings/YARA/reverse engineering. | Apply before terminating a suspicious in-memory process so volatile unpacked strings and keys are preserved. | `gcore -o /tmp/proc_<PID> <PID>` |

### Copy-Pasteable Execution Block (Windows & Linux)
```bash
# [Windows CMD] Displays OS build, patch hotfixes (KBs), boot time, current user SID, group memberships, and token privileges (`SeDebugPrivilege`, `SeImpersonatePrivilege`).
systeminfo && whoami /all
# [Windows CMD] Lists all running processes with user context, memory, window titles (`/v`), and maps every `svchost.exe` PID to hosted Windows Service names (`/svc`).
tasklist /v && tasklist /svc
# [Windows CMD] Extracts full process lineage (`PID` + `PPID`), binary disk path, and full command-line arguments for every process.
wmic process get ProcessId,ParentProcessId,Name,ExecutablePath,CommandLine /format:list
# [Sysinternals] Prints hierarchical parent-child process tree (`-t`) and enumerates both local interactive and SMB network logon sessions.
pslist -accepteula -t && psloggedon -accepteula
# [Sysinternals] Lists all unsigned DLLs (`listdlls -u`) loaded into running processes and scans `System32` for unsigned executables (`sigcheck -e -u`).
listdlls -accepteula -u && sigcheck -accepteula -e -u -vr C:\Windows\System32
# [Sysinternals] Enumerates all open file/registry/mutant handles (`handle -a -u`) and dumps CSV socket-to-process mappings (`tcpvcon`).
handle -accepteula -a -u && tcpvcon -accepteula -a -c -n
```
<!-- CORA-MAXIMIZED-COMMANDS-END -->
