---
title: "Trained Knowledge & Topology: CQC001 E020 M010 Kernel Functions"
category: knowledge
domain_hub: "[[knowledge/01_windows_system_process_and_sysinternals]]"
os_platform: windows
primary_tactic: Passive_Enum
summary: "Operational architecture, decision workflows & Windows/Linux command reference for CQC001 E020 M010 Kernel Functions: Windows live incident response, process tree/PPID investigation, service binary auditing, kernel architecture, file searching (fin"
when_to_apply: "Apply when working with CQC001 E020 M010 Kernel Functions (windows): Apply when performing initial Windows host triage (s_init_unknown), investigating running processes/PPIDs, mapping svchost.exe services, hunting unsigned/injected DLLs, searching files by timestamp/content, or executing Sysinternals live response."
tags: [http, https, mdp, pdf, trained, windows, sysinternals, pslist, listdlls, autorunsc, psservice, psloggedon, handle, sigcheck, accesschk, procdump, tasklist, systeminfo, sc, wmic, forfiles, findstr]
source_file: "CQC001 E020 M010 Kernel Functions"
updated: 2026-10-30
---

# Trained Knowledge & Architecture: `CQC001_E020_M010_Kernel_Functions.pdf`

- **Source Path:** `~/Projects/CORA/Training/CQC001_E020_M010_Kernel_Functions.pdf` (`pdf`)
- **Extracted Technical Entities:** `http, https`
- **Extracted IPs / Subnets:** `None`
- **Extracted Interfaces:** `None`

## LLM Distilled Operational Summary
### Key Operational Techniques & Decision Workflows

*   **Memory Management & Allocation**:
    *   **Contiguous Memory**: Use `AllocPhysMem` (Kernel-only) for physically contiguous blocks; release via `FreePhysMem`.
    *   **Virtual Mapping**: Create static mappings (`CreateStaticMapping`) for physical-to-virtual address translation; remove with `DeleteStaticMapping`.
    *   **Shared Memory**: Allocate read/write memory for the caller and read-only for others using `CeVirtualSharedAlloc`.
    *   **Page Fault Control**: Lock specific virtual address regions with `LockPages` to prevent swapping; force swap-out of discardable pages with `ForcePageout`.
    *   **Module Swapping**: Use `PageOutModule` to swap out all pages of a specific process or DLL.

*   **Cache & Memory Attributes**:
    *   **Cache Operations**: Flush specific ranges with `CacheRangeFlush` or the entire cache with `CacheSync`. Retrieve cache info via `CeGetCacheInfo`.
    *   **Hardware Attributes**: Apply hardware-specific memory attributes using `CeSetMemoryAttributes`.

*   **Interrupt Handling Workflow**:
    *   **Initialization**: Initialize hardware interrupts via `InterruptInitialize` and register ISRs using `HookInterrupt`.
    *   **Inter-Processor**: Install IPI handlers with `HookIPI`.
    *   **State Management**: Enable/Disable specific interrupts (`InterruptDisable`, `InterruptMask`) or toggle all (`INTERRUPTS_ON`, `INTERRUPTS_OFF`, `INTERRUPTS_ENABLE`).
    *   **Completion**: Signal ISR completion with `InterruptDone` and obtain the exception program counter (EPC) via `GetEPC`.

*   **Error Reporting & Profiling**:
    *   **Watson Dumps**: Manage error reporting dumps by clearing (`DrWatsonClear`), flushing (`DrWatsonFlush`), resizing, reading, or writing data.
    *   **Profiling**: Record samples via `ProfilerHit` (kernel) or `ProfilerHitEx` (OAL/ISR layer). Query profiler status with `ProfileCaptureStatus`.

### Critical Command Patterns & Required Flags

*   **Kernel-Only Functions**: Most low-level operations (e.g., `AllocPhysMem`, `CacheSync`, `HookInterrupt`) require execution in **Kernel Mode**.
*   **User-Mode Accessible**: Higher-level or coordination functions (e.g., `CeCallUserProc`, `CreateAPIHandle`, `GetCallerVMProcessId`) can be called from User Mode.
*   **Interrupt Prototypes**:
    *   `ISRHandler`: Prototype for OEM/IHV installable interrupt handlers.
    *   `PFN_UIENTRYPOINT`: Prototype for the UI proxy device driver entry point.
    *   `PFNAPIERRHANDLER`: Prototype for the API error handler.

### Network Topology & Service Relationships

*   **Device Drivers**: `CeCallUserProc` loads the User Interface (UI) proxy device driver.
*   **Standard I/O**: `GetStdioPathW` retrieves the device driver name used for standard input/output/error operations.
*   **Inter-Process Communication**: `ForwardDeviceIoControl` allows drivers to forward I/O controls to other drivers without validation when the current driver lacks context, preserving direct caller information for downstream

<!-- CORA-MAXIMIZED-COMMANDS-START -->
## Maximized Windows & Linux Command Examples for `CQC001 E020 M010 Kernel Functions`

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
