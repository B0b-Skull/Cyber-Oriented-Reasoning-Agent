---
title: "Trained Knowledge & Topology: CQC001 E020 M050 S040 I030 Exer X010 C010 transcript"
category: knowledge
domain_hub: "[[knowledge/01_windows_system_process_and_sysinternals]]"
os_platform: windows
primary_tactic: Passive_Enum
summary: "Operational architecture, decision workflows & Windows/Linux command reference for CQC001 E020 M050 S040 I030 Exer X010 C010 transcript: Windows live incident response, process tree/PPID investigation, service binary auditing, kernel architecture, file searching (fin"
when_to_apply: "Apply when working with CQC001 E020 M050 S040 I030 Exer X010 C010 transcript (windows): Apply when performing initial Windows host triage (s_init_unknown), investigating running processes/PPIDs, mapping svchost.exe services, hunting unsigned/injected DLLs, searching files by timestamp/content, or executing Sysinternals live response."
tags: [listdlls, mdp, passive_enum, pslist, text, trained, windows, sysinternals, autorunsc, psservice, psloggedon, handle, sigcheck, accesschk, procdump, tasklist, systeminfo, sc, wmic, forfiles, findstr, live_response]
source_file: "CQC001 E020 M050 S040 I030 Exer X010 C010 transcript"
updated: 2026-10-30
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

<!-- CORA-MAXIMIZED-COMMANDS-START -->
## Maximized Windows & Linux Command Examples for `CQC001 E020 M050 S040 I030 Exer X010 C010 transcript`

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
