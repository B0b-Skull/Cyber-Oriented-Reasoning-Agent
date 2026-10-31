---
title: "Trained Knowledge & Topology: Basic Survey Commands"
category: knowledge
domain_hub: "[[knowledge/01_windows_system_process_and_sysinternals]]"
os_platform: windows
primary_tactic: Passive_Enum
summary: "Operational architecture, decision workflows & Windows/Linux command reference for Basic Survey Commands: Windows live incident response, process tree/PPID investigation, service binary auditing, kernel architecture, file searching (fin"
when_to_apply: "Apply when working with Basic Survey Commands (windows): Apply when performing initial Windows host triage (s_init_unknown), investigating running processes/PPIDs, mapping svchost.exe services, hunting unsigned/injected DLLs, searching files by timestamp/content, or executing Sysinternals live response."
tags: [arp, auditpol, autorunsc, defense_evasion_firewall, ipconfig, listdlls, mdp, netstat, passive_enum, powershell, pslist, sysinternals, text, trained, wmic, windows, psservice, psloggedon, handle, sigcheck, accesschk, procdump]
source_file: "Basic Survey Commands"
updated: 2026-10-30
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

<!-- CORA-MAXIMIZED-COMMANDS-START -->
## Maximized Windows & Linux Command Examples for `Basic Survey Commands`

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
