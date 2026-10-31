---
title: "Trained Knowledge & Topology: Type"
category: knowledge
domain_hub: "[[knowledge/01_windows_system_process_and_sysinternals]]"
os_platform: windows
primary_tactic: Passive_Enum
summary: "Operational architecture, decision workflows & Windows/Linux command reference for Type: Windows live incident response, process tree/PPID investigation, service binary auditing, kernel architecture, file searching (fin"
when_to_apply: "Apply when working with Type (windows): Apply when performing initial Windows host triage (s_init_unknown), investigating running processes/PPIDs, mapping svchost.exe services, hunting unsigned/injected DLLs, searching files by timestamp/content, or executing Sysinternals live response."
tags: [https, mdp, passive_enum, pdf, trained, windows, sysinternals, pslist, listdlls, autorunsc, psservice, psloggedon, handle, sigcheck, accesschk, procdump, tasklist, systeminfo, sc, wmic, forfiles, findstr]
source_file: "Type"
updated: 2026-10-30
---

# Trained Knowledge & Architecture: `Type.pdf`

- **Source Path:** `~/Projects/CORA/Training/Type.pdf` (`pdf`)
- **Extracted Technical Entities:** `https`
- **Extracted IPs / Subnets:** `None`
- **Extracted Interfaces:** `None`
- **Linked Command Playbook:** [[commands/trained_type]] (`3` CEGAR-verified commands | `3` MDP transitions)

## Command & Tactic Coverage Summary
- **Total CEGAR-Verified Commands:** `3` (full executable list in [[commands/trained_type]])
- **Tactic Distribution:** `Passive_Enum` (3)
- **Top Extracted CLI Tools:** `type` (3)

## LLM Distilled Operational Summary
### Key Operational Techniques & Decision Workflows
*   **Viewing Text Files Safely**: Use `type` to display file contents without modifying the original file. Ideal for quick verification of text-based logs or scripts.
*   **Handling Filenames with Spaces**: When using NTFS drives, always enclose filenames containing spaces in quotation marks (e.g., `"My File.txt"`) to prevent command parsing errors.
*   **Pagination for Large Files**: Pipe the output of `type` into `more` (e.g., `type file.txt | more`) to view lengthy files one screen at a time, preventing terminal overflow.
*   **Binary File Caution**: Avoid using `type` on binary files or program-generated outputs, as control codes (formfeeds, escape sequences) may render as strange characters on the screen.

### Critical Command Patterns and Required Flags
*   **Basic Syntax**: `type [Drive:][Path]FileName`
    *   `[Drive:][Path]`: Specifies the exact location of the file.
    *   `FileName`: The target file name.
*   **Help Flag**: `/?` displays command help at the prompt.
*   **Filtering Pattern**: `type FileName | more` combines display with pagination.

### Network Topology & Service Relationships
*   **Drive/Path Dependency**: The command relies on standard file system paths (e.g., `C:\folder\file.txt`). No specific network IP, subnet, or serial port relationships are defined for the `type` command itself; it operates locally on the specified drive.
*   **File Type Sensitivity**: Performance and readability depend on the file format:
    *   *Text files*: Display cleanly.
    *   *Binary files*: May display garbage characters due to embedded control codes.

<!-- CORA-MAXIMIZED-COMMANDS-START -->
## Maximized Windows & Linux Command Examples for `Type`

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
