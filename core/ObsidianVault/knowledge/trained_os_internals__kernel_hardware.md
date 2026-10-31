---
title: "Trained Knowledge & Topology: OS Internals  Kernel & Hardware"
category: knowledge
domain_hub: "[[knowledge/01_windows_system_process_and_sysinternals]]"
os_platform: windows
primary_tactic: Passive_Enum
summary: "Operational architecture, decision workflows & Windows/Linux command reference for OS Internals  Kernel & Hardware: Windows live incident response, process tree/PPID investigation, service binary auditing, kernel architecture, file searching (fin"
when_to_apply: "Apply when working with OS Internals  Kernel & Hardware (windows): Apply when performing initial Windows host triage (s_init_unknown), investigating running processes/PPIDs, mapping svchost.exe services, hunting unsigned/injected DLLs, searching files by timestamp/content, or executing Sysinternals live response."
tags: [mdp, passive_enum, pdf, serial, trained, windows, sysinternals, pslist, listdlls, autorunsc, psservice, psloggedon, handle, sigcheck, accesschk, procdump, tasklist, systeminfo, sc, wmic, forfiles, findstr]
source_file: "OS Internals  Kernel & Hardware"
updated: 2026-10-30
---

# Trained Knowledge & Architecture: `_OS Internals__Kernel & Hardware.pdf`

- **Source Path:** `~/Projects/CORA/Training/_OS Internals__Kernel & Hardware.pdf` (`pdf`)
- **Extracted Technical Entities:** `serial`
- **Extracted IPs / Subnets:** `0.0.1.33, 0.0.100.4, 0.15.0.2`
- **Extracted Interfaces:** `None`
- **Linked Command Playbook:** [[commands/trained_os_internals__kernel_hardware]] (`1` CEGAR-verified commands | `1` MDP transitions)

## Command & Tactic Coverage Summary
- **Total CEGAR-Verified Commands:** `1` (full executable list in [[commands/trained_os_internals__kernel_hardware]])
- **Tactic Distribution:** `Passive_Enum` (1)
- **Top Extracted CLI Tools:** `openssl` (1)

## LLM Distilled Operational Summary
### 1. Key Operational Techniques & Decision Workflows

*   **Boot Chain Execution Flow**: The application processor executes a sequential chain starting with the **SecureROM** image, followed by **LLB** (Low Level Boot), **iBSS** (Second Stage Boot), and finally **iBoot**, which loads the **kernelcache**. Failure at any stage transitions the device into **Recovery Mode** ("Connect to iTunes") or **USB-DFU** mode.
*   **Code Rebase Loop**: Upon loading, components check if the binary resides at a predefined address (e.g., `0x100000000` for A12 SecureROM). If not, the code is dynamically moved to the correct location before execution proceeds.
*   **Common Code Initialization**: All boot components share core initialization routines including CPU setup, Vector Base Address Register (VBAR) configuration, MMU setup, ARM MSRs, and task management for multithreading.
*   **Certificate-Based Verification**: Trust is established via a hard-coded root certificate burned into ROM. This certificate verifies the integrity of subsequent iBoot components and the kernelcache via digital signatures and APTicket entries.
*   **Image Format Handling**: 32-bit devices utilize **IMG3**, while 64-bit devices (and watches) use **IMG4** (DER format) to encode binaries and graphics.

### 2. Critical Command Patterns & Required Flags

*   **SecureROM Certificate Extraction**: Locate the Apple Secure Boot CA by searching for the specific DER encoding sequence `30 82 05 5a` (representing a SEQUENCE of 1,370 bytes) within a ROM dump or decrypted image.
*   **Decryption Keys**: For 64-bit iBoot images (iOS 10+), decryption requires device-specific **GID keys** and **IVs** (Initialization Vectors). These are often sourced from public repositories like the iPhone Wiki or NewOSXBook.com forums.
*   **Source Identification**: While exact versioning is obscured by external `#define` macros, board support files (e.g., `t8010`) and copyright dates (e.g., 2015) help correlate leaked sources (GitHub/Reddit) to specific hardware generations (e.g., iPhone 6S).

### 3. Network Topology & Service Relationships

*   **Firmware Partitioning**: Updatable boot components are extracted from the `.ipsw` file (specifically the `firmware/all_flash` directory) and copied to the device's **boot partition**.
*   **Component Evolution**: On A10 and later devices, the four distinct images (LLB, iBoot, iBEC, iBSS) have converged into a single unified iBoot image that handles all boot phases, though the image may still be tagged as `'illb'` rather than `'ibot'`.
*   **Security Architecture**: The chain of trust relies on the immutability of the ROM certificate. Once verified, this root of trust cascades through the boot stages to validate the kernelcache, forming the foundation for *OS security and runtime integrity.

## Document Structure & Key Topics
- Using openssl, parse the imag4 containers in the boot NVMe namespace,
- looking for the tags following the IM4P magic, but removing the magic
- and compare to fixed address (stored at 0x318, here 0x19c030000).
- _start:

<!-- CORA-MAXIMIZED-COMMANDS-START -->
## Maximized Windows & Linux Command Examples for `OS Internals  Kernel & Hardware`

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
