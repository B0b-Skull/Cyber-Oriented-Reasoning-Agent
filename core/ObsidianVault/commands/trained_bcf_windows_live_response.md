---
title: "Trained Command Playbook: BCF Windows Live Response"
category: commands
domain_hub: "[[knowledge/01_windows_system_process_and_sysinternals]]"
os_platform: windows
primary_tactic: Passive_Enum
summary: "Verified Windows & Linux command playbook for BCF Windows Live Response (Passive_Enum): Windows live incident response, process tree/PPID investigation, service binary auditing, kernel architecture, file searching (findstr/"
when_to_apply: "Apply when working with BCF Windows Live Response (windows): Apply when performing initial Windows host triage (s_init_unknown), investigating running processes/PPIDs, mapping svchost.exe services, hunting unsigned/injected DLLs, searching files by timestamp/content, or executing Sysinternals live response."
tags: [auditpol, covert_infil, defense_evasion_firewall, enumeration, ipconfig, lateral_movement_routing_pivot, mdp, netsh, netstat, passive_enum, pdf, post_exploitation_verification, powershell, reconnaissance, responder, trained, wevtutil, windows, sysinternals, pslist, listdlls, autorunsc]
source_file: "BCF Windows Live Response"
updated: 2026-10-30
---

systeminfo && whoami /all
# Trained Command Playbook: `BCF_Windows Live Response.pdf`
systeminfo && whoami /all
- **Source Document:** `~/Projects/CORA/Training/BCF_Windows Live Response.pdf`
- **CEGAR Verified Commands:** `52` (`0` malformed/unsafe snippets filtered)
- **MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`):** `52`
- **Discovered IPs/Subnets:** `None`
- **Discovered Interfaces:** `None`
- **Related Knowledge Note:** [[knowledge/trained_bcf_windows_live_response]]
systeminfo && whoami /all
## Distilled MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`)
| Pre-State ($s$) | Tactic ($\tau$) | Technique ($k$) | Tool ($u$) | Post-State ($s'$) | Verified Command ($c$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `ipconfig` | `s_active_services_enumerated` | `ipconfig.exe > e:\target1\incidentresponse.txt` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `netstat` | `s_passive_topology_mapped` | `netstat.exe >> e:\target1\incidentresponse.txt` |
| `s_init_unknown` | **`Reconnaissance`** | Domain, DNS, OSINT & Target Footprint Reconnaissance | `copy-item` | `s_passive_topology_mapped` | `Copy-Item <item_to_copy> <desired_location>` |
| `s_cross_subnet_pivot_routed` | **`Post_Exploitation_Verification`** | Post-Action Host Identity, Privilege & Objective Verification | `get-date` | `s_goal_verified_complete` | `Get-Date` |
| `s_protocol_chain_established` | **`Covert_Infil`** | Staged Artifact / Encapsulated Ingress Delivery | `who` | `s_covert_infil_channel_ready` | `Who - Determine what user we are running as.` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `auditpol` | `s_firewall_or_acl_unlocked` | `auditpol /get /category:*` |
| `s_firewall_or_acl_unlocked` | **`Lateral_Movement_Routing_Pivot`** | Remote Host Execution, L2/L3 Route Injection & Subnet Pivot | `net` | `s_cross_subnet_pivot_routed` | `net use \\<ip_address>\<share>` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `set-location` | `s_active_services_enumerated` | `Set-Location <desired_directory>` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `get-help` | `s_passive_topology_mapped` | `Get-Help <command>` |
| `s_init_unknown` | **`Reconnaissance`** | Domain, DNS, OSINT & Target Footprint Reconnaissance | `xcopy` | `s_passive_topology_mapped` | `xcopy /e c:\tools\* i:\evidence` |
| `s_cross_subnet_pivot_routed` | **`Post_Exploitation_Verification`** | Post-Action Host Identity, Privilege & Objective Verification | `whoami` | `s_goal_verified_complete` | `whoami` |
| `s_protocol_chain_established` | **`Covert_Infil`** | Staged Artifact / Encapsulated Ingress Delivery | `get-eventlog` | `s_covert_infil_channel_ready` | `Get-EventLog Security -Newest 20` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `get-netfirewallprofile` | `s_firewall_or_acl_unlocked` | `Get-NetFirewallProfile` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `get-itemproperty` | `s_active_services_enumerated` | `Get-ItemProperty HKLM:\SOFTWARE\MalwareBytes\Antimalware` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `get-help` | `s_passive_topology_mapped` | `Get-Help <command> -Examples` |
| `s_protocol_chain_established` | **`Covert_Infil`** | Staged Artifact / Encapsulated Ingress Delivery | `netstat` | `s_covert_infil_channel_ready` | `netstat -ano` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `netsh` | `s_firewall_or_acl_unlocked` | `netsh advfirewall show allprofiles` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `get-logproperties` | `s_active_services_enumerated` | `Get-LogProperties Security \| Format-List enabled` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `get-help` | `s_passive_topology_mapped` | `Get-Help <command> -Full` |
| `s_protocol_chain_established` | **`Covert_Infil`** | Staged Artifact / Encapsulated Ingress Delivery | `netstat` | `s_covert_infil_channel_ready` | `netstat -anob` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `get-computerinfo` | `s_active_services_enumerated` | `Get-ComputerInfo` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `get-childitem` | `s_passive_topology_mapped` | `Get-ChildItem <desired_directory>` |
| `s_protocol_chain_established` | **`Covert_Infil`** | Staged Artifact / Encapsulated Ingress Delivery | `get-childitem` | `s_covert_infil_channel_ready` | `Get-ChildItem -Path C:\ -recurse \| where-Object {` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `get-nettcpconnection` | `s_active_services_enumerated` | `Get-NetTCPConnection` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `dir` | `s_passive_topology_mapped` | `Dir <desired_directory>` |
| `s_protocol_chain_established` | **`Covert_Infil`** | Staged Artifact / Encapsulated Ingress Delivery | `new-psdrive` | `s_covert_infil_channel_ready` | `New-PSDrive -Name S -PSProvider` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `fsutil` | `s_active_services_enumerated` | `fsutil fsinfo drives` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `get-childitem` | `s_passive_topology_mapped` | `Get-ChildItem <desired_directory> \| sort-object` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `dir` | `s_passive_topology_mapped` | `Dir /od <desired_directory>` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `dir` | `s_passive_topology_mapped` | `Dir /o-d <desired_directory>` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `get-childitem` | `s_passive_topology_mapped` | `Get-ChildItem <desired_directory> \| select-object Name,` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `dir` | `s_passive_topology_mapped` | `Dir /tc <desired_directory>` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `date` | `s_passive_topology_mapped` | `Date /t` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `t` | `s_passive_topology_mapped` | `Time /t` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `systeminfo` | `s_passive_topology_mapped` | `systeminfo` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `dir` | `s_passive_topology_mapped` | `dir /a /s c:\` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `get-process` | `s_passive_topology_mapped` | `Get-Process` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `tasklist` | `s_passive_topology_mapped` | `Tasklist` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `reg` | `s_passive_topology_mapped` | `reg query HKLM\SOFTWARE\KasperskyLab` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `get-childitem` | `s_passive_topology_mapped` | `Get-ChildItem HKLM:\SOFTWARE\KasperskyLab` |
systeminfo && whoami /all
## Verified Executable Commands (Grouped by Capability Layer)
systeminfo && whoami /all
### General_System (47 commands)
```bash
Get-Help <command>
Get-Help <command> -Examples
Get-Help <command> -Full
Set-Location <desired_directory>
Get-ChildItem <desired_directory>
Dir <desired_directory>
Get-ChildItem <desired_directory> | sort-object
Dir /od <desired_directory>
Dir /o-d <desired_directory>
Get-ChildItem <desired_directory> | select-object Name,
Dir /tc <desired_directory>
Copy-Item <item_to_copy> <desired_location>
xcopy /e c:\tools\* i:\evidence
Get-Date
Date /t
Time /t
Who - Determine what user we are running as.
whoami
systeminfo
dir /a /s c:\
Get-Process
Tasklist
Get-ItemProperty HKLM:\SOFTWARE\MalwareBytes\Antimalware
reg query HKLM\SOFTWARE\KasperskyLab
Get-ChildItem HKLM:\SOFTWARE\KasperskyLab
reg query HKLM\SOFTWARE\MalwareBytes\Antimalware
Get-Service | where-object { $_.status -eq 'running'}
Net start
Get-LogProperties Security | Format-List enabled
wevtutil gl security | findstr enabled
Get-EventLog Security -Newest 20
wevtutil qe security /rd:true /c:20 /f:text
auditpol /get /category:*
Get-ComputerInfo
Get-NetTCPConnection
Get-wmiobject Win32_LogicalDisk -Filter 'DriveType=3'
fsutil fsinfo drives
Get-Wmiobject Win32_Processor | select LoadPercentage
Get-wmiobject win32_Service | where-object {
schtasks /query /v /fo list
$names = Get-ChildItem C:\Users | where {$_.name -ne
Get-ChildItem -Path C:\ -recurse | where-Object {
Get-NetFirewallProfile
net use R: \\<ip_address>\<share>
net use * \\<ip_address>\<share>
net use \\<ip_address>\<share>
New-PSDrive -Name S -PSProvider
```
systeminfo && whoami /all
### L3_Routing_NAT (2 commands)
```bash
ipconfig.exe > e:\target1\incidentresponse.txt
netsh advfirewall show allprofiles
```
systeminfo && whoami /all
### L4_Port_Service (3 commands)
```bash
netstat.exe >> e:\target1\incidentresponse.txt
netstat -ano
netstat -anob
```
systeminfo && whoami /all

<!-- CORA-MAXIMIZED-COMMANDS-START -->
## Maximized Windows & Linux Command Examples for `BCF Windows Live Response`

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
