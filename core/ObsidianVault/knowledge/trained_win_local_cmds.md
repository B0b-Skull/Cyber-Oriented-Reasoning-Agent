---
title: "Trained Knowledge & Topology: Win Local CMDs"
category: knowledge
domain_hub: "[[knowledge/01_windows_system_process_and_sysinternals]]"
os_platform: windows
primary_tactic: Passive_Enum
summary: "Operational architecture, decision workflows & Windows/Linux command reference for Win Local CMDs: Windows live incident response, process tree/PPID investigation, service binary auditing, kernel architecture, file searching (fin"
when_to_apply: "Apply when working with Win Local CMDs (windows): Apply when performing initial Windows host triage (s_init_unknown), investigating running processes/PPIDs, mapping svchost.exe services, hunting unsigned/injected DLLs, searching files by timestamp/content, or executing Sysinternals live response."
tags: [enumeration, lateral_movement_routing_pivot, listdlls, mdp, passive_enum, pslist, text, trained, wmic, windows, sysinternals, autorunsc, psservice, psloggedon, handle, sigcheck, accesschk, procdump, tasklist, systeminfo, sc, forfiles]
source_file: "Win Local CMDs"
updated: 2026-10-30
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

<!-- CORA-MAXIMIZED-COMMANDS-START -->
## Maximized Windows & Linux Command Examples for `Win Local CMDs`

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
