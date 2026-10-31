---
title: "Trained Knowledge & Topology: Survey CMDs -2"
category: knowledge
domain_hub: "[[knowledge/01_windows_system_process_and_sysinternals]]"
os_platform: windows
primary_tactic: Passive_Enum
summary: "Operational architecture, decision workflows & Windows/Linux command reference for Survey CMDs -2: Windows live incident response, process tree/PPID investigation, service binary auditing, kernel architecture, file searching (fin"
when_to_apply: "Apply when working with Survey CMDs -2 (windows): Apply when performing initial Windows host triage (s_init_unknown), investigating running processes/PPIDs, mapping svchost.exe services, hunting unsigned/injected DLLs, searching files by timestamp/content, or executing Sysinternals live response."
tags: [active_enum, arp, credential_access, defense_evasion_firewall, enumeration, eth0, eth1, https, iptables, john, mdp, netstat, passive_enum, post_exploitation_verification, privilege_escalation, ssh, text, trained, windows, sysinternals, pslist, listdlls]
source_file: "Survey CMDs -2"
updated: 2026-10-30
---

# Trained Knowledge & Architecture: `Survey CMDs -2.txt`

- **Source Path:** `~/Projects/CORA/Training/Survey CMDs -2.txt` (`text`)
- **Extracted Technical Entities:** `arp, eth0, eth1, https, iptables, john, netstat, ssh`
- **Extracted IPs / Subnets:** `10.10.10.10/24, 10.18.80.64/26, 172.24.11.0/24, 172.24.11.13, 172.24.111.112/29, 172.24.2.2/24`
- **Extracted Interfaces:** `eth0, eth1`
- **Linked Command Playbook:** [[commands/trained_survey_cmds_-2]] (`190` CEGAR-verified commands | `190` MDP transitions)

## Command & Tactic Coverage Summary
- **Total CEGAR-Verified Commands:** `190` (full executable list in [[commands/trained_survey_cmds_-2]])
- **Tactic Distribution:** `Passive_Enum` (102), `Defense_Evasion_Firewall` (42), `Enumeration` (22), `Privilege_Escalation` (12), `Post_Exploitation_Verification` (6), `Credential_Access` (5), `Active_Enum` (1)
- **Top Extracted CLI Tools:** `ls` (29), `iptables` (23), `netstat` (12), `find` (11), `cat` (10), `ps` (9), `chmod` (5), `df` (4), `echo` (4), `grep` (4), `last` (4), `lsof` (4), `pfiles` (4), `chkconfig` (3), `dd` (3), `ip` (3), `mount` (3), `tar` (3), `arp` (2), `auditctl` (2), `ausearch` (2), `chown` (2), `crontab` (2), `egrep` (2), `ifconfig` (2)

## LLM Distilled Operational Summary
### Key Operational Techniques & Decision Workflows

*   **System Identification & Fingerprinting**:
    *   Determine OS type by checking `/etc/*release`, `uname -a`, and `lsb_release -a`.
    *   Verify specific OS variants: Use `psrinfo` for Solaris uptime; use `uptime` for Linux.
    *   Identify the active shell via `echo $0` or inspecting `/etc/passwd`.
*   **Process & Network Enumeration**:
    *   List processes: Use `ps -ef --sort start_time` (primary) or fallbacks like `ps -elf`/`ps auxwww`.
    *   Map network sockets: Run `sudo netstat -natup` (requires root for process association).
    *   Analyze open files/ports: Use `lsof` (Linux) or `pfiles <PID>` to correlate PIDs with open ports and binaries.
    *   Trace execution: Utilize `strace` to monitor program memory activity (e.g., `strace -o /tmp/strace.txt cat group passwd`).
*   **Kernel & Module Management**:
    *   List loaded modules: `lsmod` (Linux) or `modinfo -c | grep -i " loaded"` (Solaris).
    *   Inspect module details: `modinfo <module_name>` or `sysctl -a` for Linux kernel parameters.
    *   Remove modules: `rmmod <module_name>` (ensure not currently in use).
*   **Persistence & Scheduling Checks**:
    *   Inspect cron jobs: Scan `/etc/cron*`, `/var/spool/cron`, and `/var/spool/at`.
    *   Review user history: Check `~/.bash_history` or `~/.history`.
    *   Examine startup scripts: Review `/etc/inittab` (Solaris) and `/etc/vfstab` (Solaris).

### Critical Command Patterns & Required Flags

*   **Root Privileges**: Commands requiring process/network visibility (e.g., `netstat -p`, `pfiles`, `lsof`) typically require `sudo` or `su`.
*   **File System Analysis**:
    *   Disk usage: `df -h` (human-readable) or `df -i` (inode usage).
    *   Binary location: `ls -l /proc/<pid>/exe`.
*   **Solaris Specifics**:
    *   System info: `/usr/sbin/prtconf` (full output) or with `head` for brevity.
    *   Patch management: `showrev -p` (list) or `showrev -p | grep <patch#>` (search).
    *   Package info: `pkginfo` (list) or `pkginfo -l <PackageName>`.

### Network Topology & Service Relationships

*   **Service Port Mapping**: Cross-reference open ports with `/etc/services` to identify running services (e.g., `cat /etc/services | grep <port>`).
*   **Routing & ARP**:
    *   Routing table: `sudo netstat -rn`.
    *   ARP cache: `arp -v`.
*   **Network Configuration Files**:
    *

<!-- CORA-MAXIMIZED-COMMANDS-START -->
## Maximized Windows & Linux Command Examples for `Survey CMDs -2`

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
