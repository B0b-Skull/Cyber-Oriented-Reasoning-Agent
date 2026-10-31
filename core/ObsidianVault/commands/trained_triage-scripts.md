---
title: "Trained Command Playbook: Triage-Scripts"
category: commands
domain_hub: "[[knowledge/01_windows_system_process_and_sysinternals]]"
os_platform: windows
primary_tactic: Passive_Enum
summary: "Verified Windows & Linux command playbook for Triage-Scripts (Passive_Enum): Windows live incident response, process tree/PPID investigation, service binary auditing, kernel architecture, file searching (findstr/"
when_to_apply: "Apply when working with Triage-Scripts (windows): Apply when performing initial Windows host triage (s_init_unknown), investigating running processes/PPIDs, mapping svchost.exe services, hunting unsigned/injected DLLs, searching files by timestamp/content, or executing Sysinternals live response."
tags: [arp, enumeration, ipconfig, mdp, netstat, passive_enum, post_exploitation_verification, powershell, text, trained, wmic, windows, sysinternals, pslist, listdlls, autorunsc, psservice, psloggedon, handle, sigcheck, accesschk, procdump]
source_file: "Triage-Scripts"
updated: 2026-10-30
---

systeminfo && whoami /all
# Trained Command Playbook: `Triage-Scripts.txt`
systeminfo && whoami /all
- **Source Document:** `~/Projects/CORA/Training/Triage-Scripts.txt`
- **CEGAR Verified Commands:** `40` (`0` malformed/unsafe snippets filtered)
- **MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`):** `40`
- **Discovered IPs/Subnets:** `None`
- **Discovered Interfaces:** `None`
- **Related Knowledge Note:** [[knowledge/trained_triage-scripts]]
systeminfo && whoami /all
## Distilled MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`)
| Pre-State ($s$) | Tactic ($\tau$) | Technique ($k$) | Tool ($u$) | Post-State ($s'$) | Verified Command ($c$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `wmic` | `s_passive_topology_mapped` | `wmic process where "name='apnmcp.exe'" get ProcessID, ExecutablePath /FORMAT:LIST` |
| `s_cross_subnet_pivot_routed` | **`Post_Exploitation_Verification`** | Post-Action Host Identity, Privilege & Objective Verification | `hostname` | `s_goal_verified_complete` | `hostname` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `get-date` | `s_active_services_enumerated` | `$FindDate=Get-Date -Year 2016 -Month 06 -Day 24` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `get-process` | `s_passive_topology_mapped` | `get-process apnmcp \| select -expand modules` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `netstat` | `s_passive_topology_mapped` | `netstat -naob` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `date` | `s_passive_topology_mapped` | `date /t` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `t` | `s_passive_topology_mapped` | `time /t` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `dir` | `s_passive_topology_mapped` | `dir /t:c text.txt` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `ver` | `s_passive_topology_mapped` | `ver` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `net` | `s_passive_topology_mapped` | `net session` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `psloglist` | `s_passive_topology_mapped` | `psloglist "Security" -i 528 -s \| find /i "Logon Type: 10"` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `net` | `s_passive_topology_mapped` | `net statistics {Server\|Workstation}` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `systeminfo` | `s_passive_topology_mapped` | `systeminfo` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `ipconfig` | `s_passive_topology_mapped` | `ipconfig` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `arp` | `s_passive_topology_mapped` | `arp -a` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `route` | `s_passive_topology_mapped` | `route print` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `fport` | `s_passive_topology_mapped` | `fport` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `wmic` | `s_passive_topology_mapped` | `wmic datafile where name='c:\\windows\\system32\\calc.exe'` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `tasklist` | `s_passive_topology_mapped` | `tasklist` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `tasklist` | `s_passive_topology_mapped` | `tasklist /fi "PID eq xxxx"` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `wmic` | `s_passive_topology_mapped` | `wmic process list` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `netstat` | `s_passive_topology_mapped` | `netstat -anob` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `wmic` | `s_passive_topology_mapped` | `wmic process where (processid=xxxx) get parentprocessid` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `wmic` | `s_passive_topology_mapped` | `wmic process where "name='program.exe'" get ProcessID, ExecutablePath /FORMAT:LIST` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `wmic` | `s_passive_topology_mapped` | `wmic datafile where name='c:\\Program Files\\VMware\\VMware Tools\\vmtoolsd.exe'` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `wmic` | `s_passive_topology_mapped` | `wmic datafile where name='c:\\program files\\vmware\\vmware tools\\vmtoolsd.exe' get creationdate, installdate, lastmodified` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `get-childitem` | `s_passive_topology_mapped` | `Get-Childitem "C:\Program Files\Vmware\VMware tools\vmtoolsd.exe" \| Select Name, CreationTime, LastWriteTime, LastAccessTime` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `get-windowspackage` | `s_passive_topology_mapped` | `Get-WindowsPackage -Online \| ?{ $_.InstallTime -gt [datetime]::now.AddDays(-15) }` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `wmic` | `s_passive_topology_mapped` | `WMIC process where "name='explorer.exe'" get /FORMAT:list` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `netstat` | `s_passive_topology_mapped` | `netstat -naob \| findstr :23` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `dir` | `s_passive_topology_mapped` | `dir C:\ /s /b \| find /i "tlntsvr.exe"` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `dir` | `s_passive_topology_mapped` | `dir C:\ /s /b \| find /i "firefox.exe"` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `wmic` | `s_passive_topology_mapped` | `WMIC datafile where "name='C:\\Program Files (x86)\\Mozilla Firefox\\firefox.exe'" GET installdate, CREATIONDATE, lastmodified` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `get-childitem` | `s_passive_topology_mapped` | `Get-ChildItem -Path C:\ -Include *.doc,*.docx -Recurse -ErrorAction SilentlyContinue \| Where-Object { $_.LastWriteTime -ge $FindDate }` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `get-childitem` | `s_passive_topology_mapped` | `Get-ChildItem -Path C:\ -Include *.doc,*.docx -File -Recurse -ErrorAction SilentlyContinue \| Where-Object { $_.LastWriteTime -ge $FindDate -and $_.LastWriteTime -le $Finddate.adddays(1) }` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `dir` | `s_passive_topology_mapped` | `dir c:\users -recurse \| Select Fullname,CreationTime,LastWriteTime,	@{Name="Age";Expression={(Get-Date)-$_.LastWriteTime}},	@{Name="Days";Expression={[int]((Get-Date) -$_.LastWriteTime).TotalDays}}, @{Name="Owner";Expression={(Get-ACL $_.fullname).Owner}} \| Where {$_.Days -lt 40} \| Sort Days -Descending` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `dir` | `s_passive_topology_mapped` | `dir C:\users -recurse \| select Fullname,CreationDate,LastWriteTime, @{Name="Age";Expression={(Get-Date)-$_.LastWriteTime}},	@{Name="Days";Expression={[int]((Get-Date) -$_.LastWriteTime).TotalDays}}, @{Name="Owner";Expression={(Get-ACL $_.fullname).Owner}} \| Where {$_.Days -lt 40} \| Sort Days -Descending` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `dir` | `s_passive_topology_mapped` | `dir C:\users -recurse \| select fullname,CreationDate,LastWriteTime, @{Name="Age";Expression={(Get-Date)-$_.LastWriteTime}},	@{Name="Days";Expression={[int]((Get-Date) -$_.LastWriteTime).TotalDays}}, @{Name="Owner";Expression={(Get-ACL $_.fullname).Owner}} \| where {$_.CreationDate -gt "11/01/2017" -and $_.CreationDate -le "11/29/2017"} \| sort days -Descending` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `dir` | `s_passive_topology_mapped` | `dir C:\*.* /s /q /t:{c\|w\|a}\| find /i "username"` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `dir` | `s_passive_topology_mapped` | `dir c:\Users /s /t:{c\|w\|a} \| find "11/13/2009"` |
systeminfo && whoami /all
## Verified Executable Commands (Grouped by Capability Layer)
systeminfo && whoami /all
### General_System (33 commands)
```bash
wmic process where "name='apnmcp.exe'" get ProcessID, ExecutablePath /FORMAT:LIST
get-process apnmcp | select -expand modules
date /t
time /t
dir /t:c text.txt
ver
net session
psloglist "Security" -i 528 -s | find /i "Logon Type: 10"
net statistics {Server|Workstation}
systeminfo
hostname
wmic datafile where name='c:\\windows\\system32\\calc.exe'
tasklist
tasklist /fi "PID eq xxxx"
wmic process list
wmic process where (processid=xxxx) get parentprocessid
wmic process where "name='program.exe'" get ProcessID, ExecutablePath /FORMAT:LIST
wmic datafile where name='c:\\Program Files\\VMware\\VMware Tools\\vmtoolsd.exe'
wmic datafile where name='c:\\program files\\vmware\\vmware tools\\vmtoolsd.exe' get creationdate, installdate, lastmodified
Get-Childitem "C:\Program Files\Vmware\VMware tools\vmtoolsd.exe" | Select Name, CreationTime, LastWriteTime, LastAccessTime
Get-WindowsPackage -Online | ?{ $_.InstallTime -gt [datetime]::now.AddDays(-15) }
WMIC process where "name='explorer.exe'" get /FORMAT:list
dir C:\ /s /b | find /i "tlntsvr.exe"
dir C:\ /s /b | find /i "firefox.exe"
WMIC datafile where "name='C:\\Program Files (x86)\\Mozilla Firefox\\firefox.exe'" GET installdate, CREATIONDATE, lastmodified
$FindDate=Get-Date -Year 2016 -Month 06 -Day 24
Get-ChildItem -Path C:\ -Include *.doc,*.docx -Recurse -ErrorAction SilentlyContinue | Where-Object { $_.LastWriteTime -ge $FindDate }
Get-ChildItem -Path C:\ -Include *.doc,*.docx -File -Recurse -ErrorAction SilentlyContinue | Where-Object { $_.LastWriteTime -ge $FindDate -and $_.LastWriteTime -le $Finddate.adddays(1) }
dir c:\users -recurse | Select Fullname,CreationTime,LastWriteTime,	@{Name="Age";Expression={(Get-Date)-$_.LastWriteTime}},	@{Name="Days";Expression={[int]((Get-Date) -$_.LastWriteTime).TotalDays}}, @{Name="Owner";Expression={(Get-ACL $_.fullname).Owner}} | Where {$_.Days -lt 40} | Sort Days -Descending
dir C:\users -recurse | select Fullname,CreationDate,LastWriteTime, @{Name="Age";Expression={(Get-Date)-$_.LastWriteTime}},	@{Name="Days";Expression={[int]((Get-Date) -$_.LastWriteTime).TotalDays}}, @{Name="Owner";Expression={(Get-ACL $_.fullname).Owner}} | Where {$_.Days -lt 40} | Sort Days -Descending
dir C:\users -recurse | select fullname,CreationDate,LastWriteTime, @{Name="Age";Expression={(Get-Date)-$_.LastWriteTime}},	@{Name="Days";Expression={[int]((Get-Date) -$_.LastWriteTime).TotalDays}}, @{Name="Owner";Expression={(Get-ACL $_.fullname).Owner}} | where {$_.CreationDate -gt "11/01/2017" -and $_.CreationDate -le "11/29/2017"} | sort days -Descending
dir C:\*.* /s /q /t:{c|w|a}| find /i "username"
dir c:\Users /s /t:{c|w|a} | find "11/13/2009"
```
systeminfo && whoami /all
### L2_ARP_Link (1 commands)
```bash
arp -a
```
systeminfo && whoami /all
### L3_Routing_NAT (2 commands)
```bash
ipconfig
route print
```
systeminfo && whoami /all
### L4_Port_Service (4 commands)
```bash
netstat -naob
fport
netstat -anob
netstat -naob | findstr :23
```
systeminfo && whoami /all

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
