---
title: "Trained Knowledge & Topology: Survey CMDs"
category: knowledge
domain_hub: "[[knowledge/01_windows_system_process_and_sysinternals]]"
os_platform: windows
primary_tactic: Passive_Enum
summary: "Operational architecture, decision workflows & Windows/Linux command reference for Survey CMDs: Windows live incident response, process tree/PPID investigation, service binary auditing, kernel architecture, file searching (fin"
when_to_apply: "Apply when working with Survey CMDs (windows): Apply when performing initial Windows host triage (s_init_unknown), investigating running processes/PPIDs, mapping svchost.exe services, hunting unsigned/injected DLLs, searching files by timestamp/content, or executing Sysinternals live response."
tags: [arp, credential_access, defense_evasion_firewall, enumeration, https, iptables, mdp, netstat, passive_enum, post_exploitation_verification, text, trained, windows, sysinternals, pslist, listdlls, autorunsc, psservice, psloggedon, handle, sigcheck, accesschk]
source_file: "Survey CMDs"
updated: 2026-10-30
---

# Trained Knowledge & Architecture: `Survey CMDs.txt`

- **Source Path:** `~/Projects/CORA/Training/Survey CMDs.txt` (`text`)
- **Extracted Technical Entities:** `arp, https, iptables, netstat`
- **Extracted IPs / Subnets:** `1.0.0.1, 126.255.255.254, 128.1.0.1, 191.255.255.254, 192.0.1.1, 223.255.254.254, 224.0.0.0, 239.255.255.255`
- **Extracted Interfaces:** `None`
- **Linked Command Playbook:** [[commands/trained_survey_cmds]] (`89` CEGAR-verified commands | `89` MDP transitions)

## Command & Tactic Coverage Summary
- **Total CEGAR-Verified Commands:** `89` (full executable list in [[commands/trained_survey_cmds]])
- **Tactic Distribution:** `Passive_Enum` (38), `Defense_Evasion_Firewall` (25), `Credential_Access` (20), `Post_Exploitation_Verification` (4), `Enumeration` (2)
- **Top Extracted CLI Tools:** `ls` (17), `cat` (11), `find` (10), `ps` (6), `netstat` (5), `ip` (2), `iptables` (2), `ss` (2), `uname` (2), `arp` (1), `chkconfig` (1), `cp` (1), `date` (1), `echo` (1), `file` (1), `fuser` (1), `getenforce` (1), `grep` (1), `history` (1), `hostid` (1), `hostname` (1), `ifconfig` (1), `last` (1), `lsmod` (1), `lsof` (1)

## LLM Distilled Operational Summary
### Operational Techniques & Decision Workflows

*   **Session Hygiene:** Disable command history logging (`unset HISTFILE`) and capture the transcript to a file (`script`) before execution; clean up post-survey.
*   **Process Analysis Workflow:**
    *   Identify running processes (`ps -ef`, `ps -auxwe`).
    *   Trace execution paths using `/proc/<PID>/exe` or `strings` on binaries.
    *   Verify user context and working directories (`pwdx`, `ps -p $$`).
*   **Startup & Persistence Hunting:**
    *   Inspect init scripts via `/etc/rc*.d`, `/etc/init.d/*`, and `run-parts`.
    *   Review cron jobs across `/etc/cron*` and `/etc/crontab`.
    *   Check system release info (`/etc/*-release`) and kernel modules (`lsmod`, `modinfo`).
*   **Network Topology & Connections:**
    *   Map active connections (`netstat -anpt`, `ss -lne`).
    *   Identify listening services and bound ports (`ifconfig`, `ip addr`).
    *   Resolve reverse mappings for specific PIDs or ports (`fuser`, `/proc/<PID>/fd`).
*   **File System Anomalies:**
    *   Search for recently modified files (`find ... -newermt`) or hidden files/directories containing specific usernames.
    *   Verify binary types and execution contexts (`file`, `type -a`).

### Critical Command Patterns & Required Flags

| Goal | Command Pattern | Key Flags/Notes |
| :--- | :--- | :--- |
| **Process Tree** | `ps -efh` / `ptree` | `ptree` is Solaris-specific. |
| **Network State** | `netstat -anpt` / `ss -lne` | `-p` (PID), `-t` (TCP), `-u` (UDP), `-n` (numeric). |
| **Init Scripts** | `ls -Rltc /etc/rc.d/init.d` | `-R` (recursive), `-l` (long), `-t` (time), `-c` (change time). |
| **Cron Jobs** | `ls -al /etc/cron*` | Checks all cron-related directories. |
| **User Context** | `cat /etc/passwd` / `who -r` | Verify shell assignment and run level. |
| **Binary Path** | `ps -auxwe \| grep <PID>` | Shows full path and environment. |
| **Hidden Files** | `find / -type f -name ".*"` | Locate hidden artifacts. |

### Network Topology & Service Relationships

*   **OS Specifics:** Commands like `ptree`, `psrinfo`, and `modinfo` indicate **Solaris** environments, while `lsmod`, `ss`, and `/proc/cpuinfo` indicate **Linux**.
*   **Service Discovery:** Services are often defined in `/etc/rc*.d` (S-prefixed scripts execute on boot) and managed via `chkconfig` (Linux) or `service --status-all`.
*   **Port Binding:** Use `fuser <port>/tcp` to find the Process

<!-- CORA-MAXIMIZED-COMMANDS-START -->
## Maximized Windows & Linux Command Examples for `Survey CMDs`

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
