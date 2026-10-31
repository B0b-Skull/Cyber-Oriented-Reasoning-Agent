---
title: "Trained Knowledge & Topology: BCF Windows Live Response"
category: knowledge
domain_hub: "[[knowledge/01_windows_system_process_and_sysinternals]]"
os_platform: windows
primary_tactic: Passive_Enum
summary: "Operational architecture, decision workflows & Windows/Linux command reference for BCF Windows Live Response: Windows live incident response, process tree/PPID investigation, service binary auditing, kernel architecture, file searching (fin"
when_to_apply: "Apply when working with BCF Windows Live Response (windows): Apply when performing initial Windows host triage (s_init_unknown), investigating running processes/PPIDs, mapping svchost.exe services, hunting unsigned/injected DLLs, searching files by timestamp/content, or executing Sysinternals live response."
tags: [auditpol, covert_infil, defense_evasion_firewall, enumeration, ipconfig, lateral_movement_routing_pivot, mdp, netsh, netstat, passive_enum, pdf, post_exploitation_verification, powershell, reconnaissance, responder, trained, wevtutil, windows, sysinternals, pslist, listdlls, autorunsc]
source_file: "BCF Windows Live Response"
updated: 2026-10-30
---

# Trained Knowledge & Architecture: `BCF_Windows Live Response.pdf`

- **Source Path:** `~/Projects/CORA/Training/BCF_Windows Live Response.pdf` (`pdf`)
- **Extracted Technical Entities:** `auditpol, ipconfig, netsh, netstat, powershell, responder, wevtutil`
- **Extracted IPs / Subnets:** `None`
- **Extracted Interfaces:** `None`
- **Linked Command Playbook:** [[commands/trained_bcf_windows_live_response]] (`52` CEGAR-verified commands | `52` MDP transitions)

## Command & Tactic Coverage Summary
- **Total CEGAR-Verified Commands:** `52` (full executable list in [[commands/trained_bcf_windows_live_response]])
- **Tactic Distribution:** `Passive_Enum` (31), `Enumeration` (7), `Covert_Infil` (6), `Defense_Evasion_Firewall` (3), `Post_Exploitation_Verification` (2), `Reconnaissance` (2), `Lateral_Movement_Routing_Pivot` (1)
- **Top Extracted CLI Tools:** `get-childitem` (6), `dir` (5), `net` (4), `get-help` (3), `get-wmiobject` (3), `netstat` (3), `reg` (2), `wevtutil` (2), `auditpol` (1), `copy-item` (1), `date` (1), `fsutil` (1), `get-computerinfo` (1), `get-date` (1), `get-eventlog` (1), `get-itemproperty` (1), `get-logproperties` (1), `get-netfirewallprofile` (1), `get-nettcpconnection` (1), `get-process` (1), `get-service` (1), `ipconfig` (1), `netsh` (1), `new-psdrive` (1), `schtasks` (1)

### Visual & Network Diagram Intelligence (`BCF_Windows Live Response.pdf#page1`)
- **Spatially Grouped Diagram Nodes (Box/Component Clusters):**
  1. `[ICHIRON | TRAINING]`
  2. `[Basic Computer Forensics | 26-28Mar2018 | DISCOVERYANDCOUNTER-INFILTRATIONPROFESSIONALTM(DCIP)TM]`

### Visual & Network Diagram Intelligence (`BCF_Windows Live Response.pdf#page2`)
- **Spatially Grouped Diagram Nodes (Box/Component Clusters):**
  1. `[Incident Response]`
  2. `[OVERVIEW]`

### Visual & Network Diagram Intelligence (`BCF_Windows Live Response.pdf#page5`)
- **Diagram Ports / Services:** `:24, :35`
- **Spatially Grouped Diagram Nodes (Box/Component Clusters):**
  1. `[WCHIRON | TRAINING]`
  2. `[Run as Administrator]`
  3. `[ComputerUNTITLED (E:)WIN7 | Open | Burn | New folder | Name | C=4. | Open]`
  4. `[Search WIN7 | Date modified | Size | Type | 10 7:24 AM | Application]`
  5. `[Organize | Desktop | Downloads | Recent Places | Libraries | Documents]`
  6. `[口 | 337KB]`
  7. `[Run as administrator | SkyDrive Pro | Troubleshoot compatibility | Add to archive... | Add to "cmd.rar" | Compress and email... | Compress to "cmd.rar" and email]`
  8. `[Music | Pictures | Videos | Computer | Local Disk (C:) | UNTITLED (E:)]`
  9. `[Send to | Copy | Paste | Create shortcut | Delete]`
  10. `[.fseventsd | Spotlight-V100 | .Temporarylter | .Trashes | DCIM | WIN7 | Shared Folders]`
  11. `[Rename | Properties | Date modified: 11/20/2010 7:24 AM | Size: 337 KB]`
  12. `[cmd | Application | Basic Computer Forensics]`
  13. `[Date created: 11/20/2012 1:35 PM]`
  14. `[DISCOVERYANDCOUNTER-INFILTRATION | PROFESSIONALTM(DCIP)TM | 2016 CHIRON TECHNOLOGY SERVICES, INC]`
  15. `[Any unauthorized use or disclosure of this material is strictly prohibited.]`

## LLM Distilled Operational Summary
### Operational Techniques & Decision Workflows
*   **Live System Preservation:**
    *   **Imaging:** Create a bit-for-bit, unmodified copy. If time permits, create multiple copies.
    *   **Data Transfer:** Always copy data to an external, trusted device before analysis.
    *   **Minimization:** Minimize interaction with the target system to prevent footprint changes (file system/registry modifications).
    *   **GUI Usage:** Avoid Graphical User Interfaces (GUIs) as they alter the target application state; use Command Line Interfaces (CLI) instead.
    *   **Sleep State Handling:** Wake laptops via touchpad or desktops via mouse movement. Photograph the screen and save open documents without closing applications.
*   **Scripting & Output:** Create custom scripts for the target OS and redirect all command outputs to an external device (e.g., `ipconfig.exe > e:\target1\incidentresponse.txt`).
*   **Tool Selection:** Use trusted, "bring your own" tools. Prefer PowerShell over `cmd` for functionality, but support pre-Windows 7 systems.

### Critical Command Patterns & Required Flags
*   **Directory Navigation:**
    *   PowerShell: `Set-Location <path>`
    *   CMD: `cd <path>`
*   **Directory Listing:**
    *   PowerShell: `Get-ChildItem <path>`
    *   CMD: `dir <path>` (Omit path to list current directory).
*   **Sorting by Modification Time:**
    *   PowerShell: `Get-ChildItem <path> | Sort-Object LastWriteTime`
    *   CMD: `dir /od <path>` (Reverse order: `dir /od`).
*   **Help Retrieval:**
    *   CMD: `<command> /?`
    *   PowerShell: `Get-Help <command>`, `-Examples`, or `-Full`.

### Network Topology & Service Relationships
*   **Diagram Ports/Services:** The document explicitly notes ports **:24** and **:35** in the context of network diagram intelligence.
*   **System Context:**
    *   **OS Versions:** Procedures cover both Windows 7 (specifically mentioned in file paths like `Computer\UNTITLED (E:)WIN7`) and pre-Windows 7 environments.
    *   **File System Artifacts:** Specific folders and files noted include `.fseventsd`, `Spotlight-V100`, `.TemporaryItems`, `.Trashes`, `DCIM`, and `Shared Folders`.
    *   **User Environment:** Standard Windows 7 user directories such as `Desktop`, `Documents`, `Downloads`, `Music`, `Pictures`, and `Videos` are relevant for analysis.
*   **Organization Structure:**
    *   **Training Provider:** ICHIRON / WCHIRON.
    *   **Course Title:** Basic Computer Forensics (26-28 Mar 2018).
    *   **Certification:** DISCOVERY AND COUNTER-INFILTRATION PROFESSIONAL™ (DCIP)™.
    *   **Vendor:** 2016 CHIRON TECHNOLOGY SERVICES, INC.

## Document Structure & Key Topics
- Visual & Network Diagram Intelligence (`BCF_Windows Live Response.pdf#page1`)
- Visual & Network Diagram Intelligence (`BCF_Windows Live Response.pdf#page2`)
- Visual & Network Diagram Intelligence (`BCF_Windows Live Response.pdf#page5`)

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
