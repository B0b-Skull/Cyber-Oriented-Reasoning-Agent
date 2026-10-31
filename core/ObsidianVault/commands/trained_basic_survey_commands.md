---
title: "Trained Command Playbook: Basic Survey Commands"
category: commands
domain_hub: "[[knowledge/01_windows_system_process_and_sysinternals]]"
os_platform: windows
primary_tactic: Passive_Enum
summary: "Verified Windows & Linux command playbook for Basic Survey Commands (Passive_Enum): Windows live incident response, process tree/PPID investigation, service binary auditing, kernel architecture, file searching (findstr/"
when_to_apply: "Apply when working with Basic Survey Commands (windows): Apply when performing initial Windows host triage (s_init_unknown), investigating running processes/PPIDs, mapping svchost.exe services, hunting unsigned/injected DLLs, searching files by timestamp/content, or executing Sysinternals live response."
tags: [arp, auditpol, autorunsc, defense_evasion_firewall, ipconfig, listdlls, mdp, netstat, passive_enum, powershell, pslist, sysinternals, text, trained, wmic, windows, psservice, psloggedon, handle, sigcheck, accesschk, procdump]
source_file: "Basic Survey Commands"
updated: 2026-10-30
---

systeminfo && whoami /all
# Trained Command Playbook: `Basic Survey Commands.txt`
systeminfo && whoami /all
- **Source Document:** `~/Projects/CORA/Training/Basic Survey Commands.txt`
- **CEGAR Verified Commands:** `39` (`0` malformed/unsafe snippets filtered)
- **MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`):** `39`
- **Discovered IPs/Subnets:** `None`
- **Discovered Interfaces:** `None`
- **Related Knowledge Note:** [[knowledge/trained_basic_survey_commands]]
systeminfo && whoami /all
## Distilled MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`)
| Pre-State ($s$) | Tactic ($\tau$) | Technique ($k$) | Tool ($u$) | Post-State ($s'$) | Verified Command ($c$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `prompt` | `s_passive_topology_mapped` | `prompt $P$B$D$B$T$G` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `auditpol` | `s_firewall_or_acl_unlocked` | `auditpol /get /category:*` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `date` | `s_passive_topology_mapped` | `date /t && time/t` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `ipconfig` | `s_passive_topology_mapped` | `ipconfig /all` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `tasklist` | `s_passive_topology_mapped` | `tasklist /v` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `tasklist` | `s_passive_topology_mapped` | `Tasklist /svc` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `psloggedon` | `s_passive_topology_mapped` | `psloggedon` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `systeminfo` | `s_passive_topology_mapped` | `systeminfo` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `listdlls` | `s_passive_topology_mapped` | `listdlls \| find /I "Command"` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `wmic` | `s_passive_topology_mapped` | `wmic process get executablepath, processid, parentprocessid \| more` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `wmic` | `s_passive_topology_mapped` | `wmic process get commandline \| more` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `wmic` | `s_passive_topology_mapped` | `wmic os get servicepackmajorversion` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `wmic` | `s_passive_topology_mapped` | `wmic useraccount get name,sid` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `wmic` | `s_passive_topology_mapped` | `wmic qfe list full` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `nbtstat` | `s_passive_topology_mapped` | `nbtstat -n` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `nbtstat` | `s_passive_topology_mapped` | `nbtstat -s` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `route` | `s_passive_topology_mapped` | `route -reg` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `netstat` | `s_passive_topology_mapped` | `netstat -ano \| findstr EST` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `netstat` | `s_passive_topology_mapped` | `netstat -ano \| findstr LIST` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `net` | `s_passive_topology_mapped` | `net users` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `net` | `s_passive_topology_mapped` | `net use` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `net` | `s_passive_topology_mapped` | `net share` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `net` | `s_passive_topology_mapped` | `net start` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `dir` | `s_passive_topology_mapped` | `dir /tc /od C:\windows\system32` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `autorunsc` | `s_passive_topology_mapped` | `autorunsc -b` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `autorunsc` | `s_passive_topology_mapped` | `autorunsc -l` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `reg` | `s_passive_topology_mapped` | `reg query hklm\software\microsoft\windows\currentversion\run` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `reg` | `s_passive_topology_mapped` | `reg query hkcu\software\microsoft\windows\currentversion\run` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `reg` | `s_passive_topology_mapped` | `reg query hklm\software\microsoft\windows\currentversion\runonce` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `reg` | `s_passive_topology_mapped` | `reg query hkcu\software\microsoft\windows\currentversion\runonce` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `reg` | `s_passive_topology_mapped` | `reg query "hklm\software\microsoft\windows nt\currentversion\winlogon" /v shell` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `reg` | `s_passive_topology_mapped` | `reg query "hklm\system\currentcontrolset\control\session manager"` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `reg` | `s_passive_topology_mapped` | `reg query hklm\system\currentcontrolset\control\windows` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `reg` | `s_passive_topology_mapped` | `reg query hklm\system\currentcontrolset\control\hivelist` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `reg` | `s_passive_topology_mapped` | `reg query hklm\system\currentcontrolset\services\tcpip\parameters` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `reg` | `s_passive_topology_mapped` | `reg query hku \| find "HKEY_USERS\S-1-5-21-" \| find /v "_Classes"` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `wmic` | `s_passive_topology_mapped` | `wmic fsdir where name="C:\\DirectoryOfInterest" get creationdate,lastmodified,lastaccessed /format:list` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `wmic` | `s_passive_topology_mapped` | `wmic datafile where name="C:\\FileOfInterest" get creationdate,lastmodified,lastaccessed /format:list` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `date` | `s_passive_topology_mapped` | `date /t >> C:\sysinfo.txt && time/t >> C:\sysinfo.txt && systeminfo >> C:\sysinfo.txt && ver >> C:\sysinfo.txt && net session >> C:\sysinfo.txt && net statistics >> C:\sysinfo.txt && ipconfig /all >> C:\sysinfo.txt && arp -a >> C:\sysinfo.txt && route print >> C:\sysinfo.txt` |
systeminfo && whoami /all
## Verified Executable Commands (Grouped by Capability Layer)
systeminfo && whoami /all
### General_System (33 commands)
```bash
prompt $P$B$D$B$T$G
date /t && time/t
tasklist /v
Tasklist /svc
psloggedon
systeminfo
listdlls | find /I "Command"
wmic process get executablepath, processid, parentprocessid | more
wmic process get commandline | more
wmic os get servicepackmajorversion
wmic useraccount get name,sid
wmic qfe list full
auditpol /get /category:*
net users
net use
net share
net start
dir /tc /od C:\windows\system32
autorunsc -b
autorunsc -l
reg query hklm\software\microsoft\windows\currentversion\run
reg query hkcu\software\microsoft\windows\currentversion\run
reg query hklm\software\microsoft\windows\currentversion\runonce
reg query hkcu\software\microsoft\windows\currentversion\runonce
reg query "hklm\software\microsoft\windows nt\currentversion\winlogon" /v shell
reg query "hklm\system\currentcontrolset\control\session manager"
reg query hklm\system\currentcontrolset\control\windows
reg query hklm\system\currentcontrolset\control\hivelist
reg query hklm\system\currentcontrolset\services\tcpip\parameters
reg query hku | find "HKEY_USERS\S-1-5-21-" | find /v "_Classes"
wmic fsdir where name="C:\\DirectoryOfInterest" get creationdate,lastmodified,lastaccessed /format:list
wmic datafile where name="C:\\FileOfInterest" get creationdate,lastmodified,lastaccessed /format:list
date /t >> C:\sysinfo.txt && time/t >> C:\sysinfo.txt && systeminfo >> C:\sysinfo.txt && ver >> C:\sysinfo.txt && net session >> C:\sysinfo.txt && net statistics >> C:\sysinfo.txt && ipconfig /all >> C:\sysinfo.txt && arp -a >> C:\sysinfo.txt && route print >> C:\sysinfo.txt
```
systeminfo && whoami /all
### L3_Routing_NAT (2 commands)
```bash
ipconfig /all
route -reg
```
systeminfo && whoami /all
### L4_Port_Service (4 commands)
```bash
nbtstat -n
nbtstat -s
netstat -ano | findstr EST
netstat -ano | findstr LIST
```
systeminfo && whoami /all

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
