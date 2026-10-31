---
title: "Trained Knowledge & Topology: Tasklist"
category: knowledge
domain_hub: "[[knowledge/01_windows_system_process_and_sysinternals]]"
os_platform: windows
primary_tactic: Passive_Enum
summary: "Operational architecture, decision workflows & Windows/Linux command reference for Tasklist: Windows live incident response, process tree/PPID investigation, service binary auditing, kernel architecture, file searching (fin"
when_to_apply: "Apply when working with Tasklist (windows): Apply when performing initial Windows host triage (s_init_unknown), investigating running processes/PPIDs, mapping svchost.exe services, hunting unsigned/injected DLLs, searching files by timestamp/content, or executing Sysinternals live response."
tags: [credential_access, https, lateral_movement_routing_pivot, mdp, passive_enum, pdf, trained, windows, sysinternals, pslist, listdlls, autorunsc, psservice, psloggedon, handle, sigcheck, accesschk, procdump, tasklist, systeminfo, sc, wmic]
source_file: "Tasklist"
updated: 2026-10-30
---

# Trained Knowledge & Architecture: `Tasklist.pdf`

- **Source Path:** `~/Projects/CORA/Training/Tasklist.pdf` (`pdf`)
- **Extracted Technical Entities:** `https`
- **Extracted IPs / Subnets:** `None`
- **Extracted Interfaces:** `None`
- **Linked Command Playbook:** [[commands/trained_tasklist]] (`7` CEGAR-verified commands | `7` MDP transitions)

## Command & Tactic Coverage Summary
- **Total CEGAR-Verified Commands:** `7` (full executable list in [[commands/trained_tasklist]])
- **Tactic Distribution:** `Lateral_Movement_Routing_Pivot` (3), `Passive_Enum` (3), `Credential_Access` (1)
- **Top Extracted CLI Tools:** `tasklist` (7)

## Extracted Reference Excerpt
--- [Page 1] ---
11/2/2017
Tasklist
https://technet.microsoft.com/en­us/library/bb491010(d=printer).aspx
1/3
Tasklist
Displays a list of applications and services with their Process ID ﴾PID﴿ for all tasks running on either a local or a remote computer.
Syntax
tasklist[.exe] [/s computer] [/u domain\user [/p password]] [/fo {TABLE|LIST|CSV}] [/nh] [/fi FilterName [/fi FilterName2 [ ...
]]] [/m [ModuleName] | /svc | /v] 
Top of page 
Parameters
/s   Computer   : Specifies the name or IP address of a remote computer ﴾do not use backslashes﴿. The default is the local
computer.
/u   Domain \ User   : Runs the command with the account permissions of the user specified by User or Domain\User. The
default is the permissions of the current logged on user on the computer issuing the command.
/p   Password   : Specifies the password of the user account that is specified in the /u parameter.
/fo { TABLE | LIST | CSV } : Specifies the format to use for the output. Valid values are TABLE, LIST, and CSV. The default format
for output is TABLE.
/nh   : Suppresses column headers in the output. Valid when the /fo parameter is set to TABLE or CSV.
/fi   FilterName   : Specifies the types of process﴾es﴿ to include in or exclude from the query. The following table lists valid filter
names, operators, and values.
Name
Operators
Value
Status
eq, ne
RUNNING|NOT RESPONDING
Imagename
eq, ne
Any valid string.
PID
eq, ne, gt, lt,
ge, le
Any valid positive integer.
Session
eq, ne, gt, lt,
ge, le
Any valid session number.
SessionNam
e
eq, ne
Any valid string.
CPUTime
eq, ne, gt, lt,
ge, le
Valid time in the format of hh:mm:ss. The mm and ss parameters should be between 0 and
59 and hh can be any valid unsigned numeric value.
Memusage
eq, ne, gt, lt,
ge, le
Any valid integer.

--- [Page 2] ---
11/2/2017
Tasklist
https://technet.microsoft.com/en­us/library/bb491010(d=printer).aspx
2/3
Username
eq, ne
Any valid user name ﴾[Domain\]User﴿.
Services
eq, ne
Any valid string.
Windowtitle
eq, ne
Any valid string.
Modules
eq, ne
Any valid string.
/m [ ModuleName ] : Specifies to show module information for each process. When a module is specified, all the processes
using that module are shown. When a module is not specified, all the processes for all the modules are shown. Cannot be used
with the /svc or the /v parameter.
/svc   : Lists all the service information for each process without truncation. Valid when the /fo parameter is set to TABLE.
Cannot be used with the /m or the /v parameter.
/v   : Specifies that verbose task information be displayed in the output. Cannot be used with the /svc or the /m parameter.
/? : Displays help at the command prompt.
Top of page 
Remarks
Tasklist is a replacement for the TList tool.
Top of page 
Examples
The following examples show how you can use th

<!-- CORA-MAXIMIZED-COMMANDS-START -->
## Maximized Windows & Linux Command Examples for `Tasklist`

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
