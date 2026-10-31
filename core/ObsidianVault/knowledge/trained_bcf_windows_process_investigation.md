---
title: "Trained Knowledge & Topology: BCF Windows Process Investigation"
category: knowledge
domain_hub: "[[knowledge/01_windows_system_process_and_sysinternals]]"
os_platform: windows
primary_tactic: Passive_Enum
summary: "Operational architecture, decision workflows & Windows/Linux command reference for BCF Windows Process Investigation: Windows live incident response, process tree/PPID investigation, service binary auditing, kernel architecture, file searching (fin"
when_to_apply: "Apply when working with BCF Windows Process Investigation (windows): Apply when performing initial Windows host triage (s_init_unknown), investigating running processes/PPIDs, mapping svchost.exe services, hunting unsigned/injected DLLs, searching files by timestamp/content, or executing Sysinternals live response."
tags: [mdp, netstat, passive_enum, pdf, post_exploitation_verification, powershell, trained, wmic, windows, sysinternals, pslist, listdlls, autorunsc, psservice, psloggedon, handle, sigcheck, accesschk, procdump, tasklist, systeminfo, sc]
source_file: "BCF Windows Process Investigation"
updated: 2026-10-30
---

# Trained Knowledge & Architecture: `BCF_Windows Process Investigation.pdf`

- **Source Path:** `~/Projects/CORA/Training/BCF_Windows Process Investigation.pdf` (`pdf`)
- **Extracted Technical Entities:** `netstat, powershell, wmic`
- **Extracted IPs / Subnets:** `None`
- **Extracted Interfaces:** `None`
- **Linked Command Playbook:** [[commands/trained_bcf_windows_process_investigation]] (`8` CEGAR-verified commands | `8` MDP transitions)

## Command & Tactic Coverage Summary
- **Total CEGAR-Verified Commands:** `8` (full executable list in [[commands/trained_bcf_windows_process_investigation]])
- **Tactic Distribution:** `Passive_Enum` (7), `Post_Exploitation_Verification` (1)
- **Top Extracted CLI Tools:** `get-childitem` (2), `get-nettcpconnection` (1), `get-process` (1), `get-wmiobject` (1), `netstat` (1), `tasklist` (1), `wmic` (1)

### Visual & Network Diagram Intelligence (`BCF_Windows Process Investigation.pdf#page1`)
- **Spatially Grouped Diagram Nodes (Box/Component Clusters):**
  1. `[ICHIRON | TRAINING]`
  2. `[Basic Computer Forensics | 26-28Mar2018 | DISCOVERYANDCOUNTER-INFILTRATIONPROFESSIONALTM(DCIP)TM]`

### Visual & Network Diagram Intelligence (`BCF_Windows Process Investigation.pdf#page3`)
- **Spatially Grouped Diagram Nodes (Box/Component Clusters):**
  1. `[Vetting Process | Listings]`

## LLM Distilled Operational Summary
### Operational Techniques & Decision Workflows

*   **Process Vetting Workflow:**
    *   Pull a process listing (e.g., via `tasklist`).
    *   Eliminate known good Windows system processes.
    *   Conduct open-source research on unknown entries.
    *   Compare running processes against research data to identify anomalies.
*   **Attacker Blending Techniques to Detect:**
    *   Inverting characters in legitimate process names.
    *   Using legitimate names from different Windows versions.
    *   Using legitimate binaries located in wrong directories.
    *   High instance counts of `svchost.exe` or `csrss.exe`.
*   **Service Vetting Workflow:**
    *   Pull a service listing.
    *   Verify binary paths, execution context (System vs. Local/Network), and start modes (Boot vs. Manual).
    *   Cross-reference with known good service data.
*   **Malware Detection Indicators:**
    *   Presence of Command and Control (C2) network activity.
    *   Existence of a persistence mechanism to survive reboots.

### Critical Command Patterns & Required Flags

*   **Filtering Specific Processes:**
    *   `tasklist /FI "IMAGENAME eq <process_name>"` (e.g., `csrss.exe`)
*   **Inspecting `svchost.exe` Details:**
    *   **WMIC:** `wmic process where name="svchost.exe" get processId, commandline`
    *   **PowerShell:** `Get-WmiObject win32_process | Where {$_.name –eq 'svchost.exe' | select processid, commandline}`
*   **Inspecting Service Details:**
    *   **PowerShell (Path):** `Get-WmiObject win32_service | where {$_.name –eq '<service_name>' } | select pathname`
    *   **PowerShell (Start Name):** `Get-WmiObject win32_service | where {$_.name –eq '<service_name>' } | select startname`
    *   **PowerShell (Start Mode):** `Get-WmiObject win32_service | where {$_.name –eq '<service_name>' } | select startmode`

### Network Topology & Service Relationships

*   **Common System Processes:** `smss.exe`, `csrss.exe`, `winlogon.exe`, `lsass.exe`, `spoolsv.exe`, `itunes.exe`, `explorer.exe`, `cmd.exe`.
*   **High-Volume System Process:** `svchost.exe` (Often requires verification of instance count and associated service keys like `-k DcomLaunch`).
*   **Malware Characteristics:**
    *   **Network:** Typically establishes connections for Command and Control (C2).
    *   **Persistence:** Implements mechanisms to maintain execution across system reboots.
*   **Vetting Context:** Both processes and services require verification of default installation paths, publisher identity, associated support files, and file hashes (e.g., MD5).

## Document Structure & Key Topics
- Visual & Network Diagram Intelligence (`BCF_Windows Process Investigation.pdf#page1`)
- Visual & Network Diagram Intelligence (`BCF_Windows Process Investigation.pdf#page3`)

<!-- CORA-MAXIMIZED-COMMANDS-START -->
## Maximized Windows & Linux Command Examples for `BCF Windows Process Investigation`

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
