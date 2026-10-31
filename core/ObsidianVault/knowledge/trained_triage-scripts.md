---
title: "Trained Knowledge & Topology: Triage-Scripts"
category: knowledge
domain_hub: "[[knowledge/01_windows_system_process_and_sysinternals]]"
os_platform: windows
primary_tactic: Passive_Enum
summary: "Operational architecture, decision workflows & Windows/Linux command reference for Triage-Scripts: Windows live incident response, process tree/PPID investigation, service binary auditing, kernel architecture, file searching (fin"
when_to_apply: "Apply when working with Triage-Scripts (windows): Apply when performing initial Windows host triage (s_init_unknown), investigating running processes/PPIDs, mapping svchost.exe services, hunting unsigned/injected DLLs, searching files by timestamp/content, or executing Sysinternals live response."
tags: [arp, enumeration, ipconfig, mdp, netstat, passive_enum, post_exploitation_verification, powershell, text, trained, wmic, windows, sysinternals, pslist, listdlls, autorunsc, psservice, psloggedon, handle, sigcheck, accesschk, procdump]
source_file: "Triage-Scripts"
updated: 2026-10-30
---

# Trained Knowledge & Architecture: `Triage-Scripts.txt`

- **Source Path:** `~/Projects/CORA/Training/Triage-Scripts.txt` (`text`)
- **Extracted Technical Entities:** `arp, ipconfig, netstat, powershell, wmic`
- **Extracted IPs / Subnets:** `None`
- **Extracted Interfaces:** `None`
- **Linked Command Playbook:** [[commands/trained_triage-scripts]] (`40` CEGAR-verified commands | `40` MDP transitions)

## Command & Tactic Coverage Summary
- **Total CEGAR-Verified Commands:** `40` (full executable list in [[commands/trained_triage-scripts]])
- **Tactic Distribution:** `Passive_Enum` (38), `Enumeration` (1), `Post_Exploitation_Verification` (1)
- **Top Extracted CLI Tools:** `wmic` (9), `dir` (8), `get-childitem` (3), `netstat` (3), `net` (2), `tasklist` (2), `arp` (1), `date` (1), `fport` (1), `get-date` (1), `get-process` (1), `get-windowspackage` (1), `hostname` (1), `ipconfig` (1), `psloglist` (1), `route` (1), `systeminfo` (1), `t` (1), `ver` (1)

## LLM Distilled Operational Summary
### System Characterization & Time Verification
*   **Time/Version Checks**: Use `date /t`, `time /t`, and `ver` to establish baseline system state without altering settings.
*   **Session & Uptime**: Run `net session` or `net statistics {Server|Workstation}` to determine system uptime. Use `psloglist "Security" -i 528 -s | find /i "Logon Type: 10"` to identify recent interactive logons.
*   **Hardware & Network Topology**: Execute `systeminfo` for processor/memory details, `hostname` for identity, `ipconfig` for IP/DNS, and `arp -a`/`route print` for layer 2/3 topology. Use `fport` to map active port calls.

### Process & Module Analysis
*   **Process Enumeration**: Utilize `tasklist`, `wmic process list`, or PowerShell's `Get-Process` to list running processes. Filter by PID (`tasklist /fi "PID eq xxxx"`) or name (`wmic process where "name='apnmcp.exe'"`).
*   **Parent/Child Relationships**: Determine parent process IDs using `wmic process where (processid=xxxx) get parentprocessid`.
*   **Module Inspection**: Expand process modules with `get-process <name> | select -expand modules`.
*   **Executable Paths**: Retrieve full paths via `wmic process where "name='...'" get ProcessID, ExecutablePath /FORMAT:LIST`.

### File System & Registry Forensics
*   **File Properties**: Use `wmic datafile` or PowerShell (`Get-Childitem`) to inspect creation, installation, and last modification dates. Example: `wmic datafile where name='c:\\windows\\system32\\calc.exe'`.
*   **Recursive Search**: Find files by name recursively using `dir C:\ /s /b | find /i "filename"`.
*   **Date-Based Filtering**: Locate files modified within specific windows using PowerShell:
    *   Define date variables: `$FindDate = Get-Date -Year 2016 -Month 06 -Day 24`.
    *   Filter by LastWriteTime: `Where-Object { $_.LastWriteTime -ge $FindDate }`.
    *   Calculate file "age" in days using custom calculated fields for sorting.
*   **Registry Configuration**: Check NTFS last access update settings via `HKLM\System\CurrentControlSet\Control\FileSystem\NtfsDisableLastAccessUpdate`.

### Advanced PowerShell Patterns
*   **Recent Updates**: List updates installed in the last 15 days: `Get-WindowsPackage -Online | ?{ $_.InstallTime -gt [datetime]::now.AddDays(-15) }`.
*   **User Activity Analysis**: Analyze user directories for recent activity: `dir C:\users -recurse | Select Fullname,CreationTime,LastWriteTime, @{Name="Age";Expression={(Get-Date)-$_.LastWriteTime}}...`.
*   **Keyword Search**: Search for specific strings (e.g., usernames) in file contents recursively: `dir c:\*.* /s /q /t:{c|w|a}| find /i "username

<!-- CORA-MAXIMIZED-COMMANDS-START -->
## Maximized Windows & Linux Command Examples for `Triage-Scripts`

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
