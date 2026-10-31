---
title: "Trained Command Playbook: Win Local CMDs"
category: commands
domain_hub: "[[knowledge/01_windows_system_process_and_sysinternals]]"
os_platform: windows
primary_tactic: Passive_Enum
summary: "Verified Windows & Linux command playbook for Win Local CMDs (Passive_Enum): Windows live incident response, process tree/PPID investigation, service binary auditing, kernel architecture, file searching (findstr/"
when_to_apply: "Apply when working with Win Local CMDs (windows): Apply when performing initial Windows host triage (s_init_unknown), investigating running processes/PPIDs, mapping svchost.exe services, hunting unsigned/injected DLLs, searching files by timestamp/content, or executing Sysinternals live response."
tags: [enumeration, lateral_movement_routing_pivot, listdlls, mdp, passive_enum, pslist, text, trained, wmic, windows, sysinternals, autorunsc, psservice, psloggedon, handle, sigcheck, accesschk, procdump, tasklist, systeminfo, sc, forfiles]
source_file: "Win Local CMDs"
updated: 2026-10-30
---

systeminfo && whoami /all
# Trained Command Playbook: `Win Local CMDs.txt`
systeminfo && whoami /all
- **Source Document:** `~/Projects/CORA/Training/Win Local CMDs.txt`
- **CEGAR Verified Commands:** `56` (`0` malformed/unsafe snippets filtered)
- **MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`):** `56`
- **Discovered IPs/Subnets:** `172.17.10.71, 172.17.10.78`
- **Discovered Interfaces:** `None`
- **Related Knowledge Note:** [[knowledge/trained_win_local_cmds]]
systeminfo && whoami /all
## Distilled MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`)
| Pre-State ($s$) | Tactic ($\tau$) | Technique ($k$) | Tool ($u$) | Post-State ($s'$) | Verified Command ($c$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `tasklist` | `s_passive_topology_mapped` | `tasklist` |
| `s_firewall_or_acl_unlocked` | **`Lateral_Movement_Routing_Pivot`** | Remote Host Execution, L2/L3 Route Injection & Subnet Pivot | `tasklist` | `s_cross_subnet_pivot_routed` | `tasklist /s xp.ops.local /u xp\administrator /p L33tHax0r` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `taskkill` | `s_active_services_enumerated` | `taskkill /im <imagename>` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `tasklist` | `s_passive_topology_mapped` | `tasklist /svc` |
| `s_firewall_or_acl_unlocked` | **`Lateral_Movement_Routing_Pivot`** | Remote Host Execution, L2/L3 Route Injection & Subnet Pivot | `taskkill` | `s_cross_subnet_pivot_routed` | `taskkill /pid 1187 /s xp.ops.local /u xp\administrator /p L33tHax0r` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `pskill` | `s_active_services_enumerated` | `pskill -t` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `tasklist` | `s_passive_topology_mapped` | `tasklist /m` |
| `s_firewall_or_acl_unlocked` | **`Lateral_Movement_Routing_Pivot`** | Remote Host Execution, L2/L3 Route Injection & Subnet Pivot | `pslist` | `s_cross_subnet_pivot_routed` | `pslist \\xp.ops.local -u xp\administrator -p L33tHax0r` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `tasklist` | `s_passive_topology_mapped` | `tasklist /fi "SESSION eq 1"` |
| `s_firewall_or_acl_unlocked` | **`Lateral_Movement_Routing_Pivot`** | Remote Host Execution, L2/L3 Route Injection & Subnet Pivot | `pskill` | `s_cross_subnet_pivot_routed` | `pskill - \\xp.ops.local /u xp\administrator /p L33tHax0r 2843` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `pslist` | `s_passive_topology_mapped` | `pslist /dm` |
| `s_firewall_or_acl_unlocked` | **`Lateral_Movement_Routing_Pivot`** | Remote Host Execution, L2/L3 Route Injection & Subnet Pivot | `pskill` | `s_cross_subnet_pivot_routed` | `pskill - \\xp.ops.local /u xp\administrator /p L33tHax0r "notepad.exe\|2843"` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `pslist` | `s_passive_topology_mapped` | `pslist /x` |
| `s_firewall_or_acl_unlocked` | **`Lateral_Movement_Routing_Pivot`** | Remote Host Execution, L2/L3 Route Injection & Subnet Pivot | `pslist` | `s_cross_subnet_pivot_routed` | `pslist \\172.17.10.71 -u drytortugas\administrator -p $eCret` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `pslist` | `s_passive_topology_mapped` | `pslist /s 120 /r 3` |
| `s_firewall_or_acl_unlocked` | **`Lateral_Movement_Routing_Pivot`** | Remote Host Execution, L2/L3 Route Injection & Subnet Pivot | `tasklist` | `s_cross_subnet_pivot_routed` | `tasklist /s 172.17.10.71 -u drytortugas\administrator -p $eCret` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `pslist` | `s_passive_topology_mapped` | `pslist /t` |
| `s_firewall_or_acl_unlocked` | **`Lateral_Movement_Routing_Pivot`** | Remote Host Execution, L2/L3 Route Injection & Subnet Pivot | `telnet` | `s_cross_subnet_pivot_routed` | `telnet 172.17.10.71 23` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `handle` | `s_passive_topology_mapped` | `handle -p notepad.exe` |
| `s_firewall_or_acl_unlocked` | **`Lateral_Movement_Routing_Pivot`** | Remote Host Execution, L2/L3 Route Injection & Subnet Pivot | `telnet` | `s_cross_subnet_pivot_routed` | `telnet win7.ops.local` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `handle` | `s_passive_topology_mapped` | `handle -p cmd.exe` |
| `s_firewall_or_acl_unlocked` | **`Lateral_Movement_Routing_Pivot`** | Remote Host Execution, L2/L3 Route Injection & Subnet Pivot | `tasklist` | `s_cross_subnet_pivot_routed` | `tasklist /s 172.17.10.78 /u administrator /p KeyF@rg0 /fi "session eq 0"` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `handle` | `s_passive_topology_mapped` | `handle notepad.exe` |
| `s_firewall_or_acl_unlocked` | **`Lateral_Movement_Routing_Pivot`** | Remote Host Execution, L2/L3 Route Injection & Subnet Pivot | `tasklist` | `s_cross_subnet_pivot_routed` | `tasklist /s 172.17.10.78 /u administrator /p KeyF@rg0 /m IIS*` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `handle` | `s_passive_topology_mapped` | `handle -a cmd.exe` |
| `s_firewall_or_acl_unlocked` | **`Lateral_Movement_Routing_Pivot`** | Remote Host Execution, L2/L3 Route Injection & Subnet Pivot | `tasklist` | `s_cross_subnet_pivot_routed` | `tasklist /S 172.17.10.78 /U Administrator /P KeyF@rg0 /SVC` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `handle` | `s_passive_topology_mapped` | `handle -a -p PID` |
| `s_firewall_or_acl_unlocked` | **`Lateral_Movement_Routing_Pivot`** | Remote Host Execution, L2/L3 Route Injection & Subnet Pivot | `tasklist` | `s_cross_subnet_pivot_routed` | `tasklist /S 172.17.10.78 /U Administrator /P KeyF@rg0` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `listdlls` | `s_passive_topology_mapped` | `listdlls` |
| `s_firewall_or_acl_unlocked` | **`Lateral_Movement_Routing_Pivot`** | Remote Host Execution, L2/L3 Route Injection & Subnet Pivot | `pslist` | `s_cross_subnet_pivot_routed` | `pslist \\www.ops.local -u administrator -p opsDMZ321!!!` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `pslist` | `s_passive_topology_mapped` | `pslist notepad` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `listdlls` | `s_passive_topology_mapped` | `listdlls 1140` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `listdlls` | `s_passive_topology_mapped` | `listdlls notepad.exe` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `listdlls` | `s_passive_topology_mapped` | `listdlls -d wow64.dll` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `tasklist` | `s_passive_topology_mapped` | `tasklist /fi "services eq bfe"` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `wmic` | `s_passive_topology_mapped` | `wmic process where (processid=1388) get parentprocessid` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `wmic` | `s_passive_topology_mapped` | `wmic cpu get numberoflogicalprocessors` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `wmic` | `s_passive_topology_mapped` | `wmic datafile where name='c:\\windows\\system32\\drivers\\mrxsmb10.sys' get creationdate` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `tasklist` | `s_passive_topology_mapped` | `tasklist /v` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `pslist` | `s_passive_topology_mapped` | `pslist -t` |
systeminfo && whoami /all
## Verified Executable Commands (Grouped by Capability Layer)
systeminfo && whoami /all
### General_System (54 commands)
```bash
tasklist
tasklist /svc
tasklist /m
tasklist /s xp.ops.local /u xp\administrator /p L33tHax0r
tasklist /fi "SESSION eq 1"
taskkill /im <imagename>
taskkill /pid 1187 /s xp.ops.local /u xp\administrator /p L33tHax0r
pslist /dm
pslist /x
pslist /s 120 /r 3
pslist \\xp.ops.local -u xp\administrator -p L33tHax0r
pslist /t
pskill -t
pskill - \\xp.ops.local /u xp\administrator /p L33tHax0r 2843
pskill - \\xp.ops.local /u xp\administrator /p L33tHax0r "notepad.exe|2843"
handle -p notepad.exe
handle -p cmd.exe
handle notepad.exe
handle -a cmd.exe
handle -a -p PID
listdlls
pslist notepad
listdlls 1140
listdlls notepad.exe
listdlls -d wow64.dll
pslist \\172.17.10.71 -u drytortugas\administrator -p $eCret
tasklist /s 172.17.10.71 -u drytortugas\administrator -p $eCret
tasklist /s 172.17.10.78 /u administrator /p KeyF@rg0 /fi "session eq 0"
tasklist /s 172.17.10.78 /u administrator /p KeyF@rg0 /m IIS*
tasklist /fi "services eq bfe"
wmic process where (processid=1388) get parentprocessid
wmic cpu get numberoflogicalprocessors
wmic datafile where name='c:\\windows\\system32\\drivers\\mrxsmb10.sys' get creationdate
tasklist /S 172.17.10.78 /U Administrator /P KeyF@rg0 /SVC
tasklist /S 172.17.10.78 /U Administrator /P KeyF@rg0
tasklist /v
pslist \\www.ops.local -u administrator -p opsDMZ321!!!
pslist -t
listdlls -d defender
listdlls |more
listdlls -d [dll-name]
listdlls -d C:\Windows\WinSxS\x86_microsoft.windows
listdlls cmd
listdlls -d dssenh.dll
listdlls -v -d gdi32.dll
listdlls -v -d pku2u.dll
listdlls -d sxssrv.dll
listdlls -u
listdlls msdtc
handle -p conhost
handle -a music
handle -a -p LogonUI | more
handle -a -p cmd
handle -s -p [PID of smss]
```
systeminfo && whoami /all
### L4_Port_Service (2 commands)
```bash
telnet 172.17.10.71 23
telnet win7.ops.local
```
systeminfo && whoami /all

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
