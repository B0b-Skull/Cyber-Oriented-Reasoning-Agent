---
title: "Domain Hub 01: Windows Live Response, Processes, Services, Kernel & Sysinternals Suite"
category: knowledge
domain_hub: "[[knowledge/01_windows_system_process_and_sysinternals]]"
os_platform: windows
primary_tactic: Passive_Enum
summary: "Windows live incident response, process tree/PPID investigation, service binary auditing, kernel architecture, file searching (findstr/forfiles), and Sysinternals Suite (pslist, listdlls, autorunsc, handle, sigcheck, accesschk, procdump)."
when_to_apply: "Apply when performing initial Windows host triage (s_init_unknown), investigating running processes/PPIDs, mapping svchost.exe services, hunting unsigned/injected DLLs, searching files by timestamp/content, or executing Sysinternals live response."
tags: [windows, sysinternals, pslist, listdlls, autorunsc, psservice, psloggedon, handle, sigcheck, accesschk, procdump, tasklist, systeminfo, sc, wmic, forfiles, findstr, passive_enum, live_response]
updated: 2026-10-30
---

# Domain Hub 01: Windows Live Response, Processes, Services, Kernel & Sysinternals Suite

> **Summary:** Windows live incident response, process tree/PPID investigation, service binary auditing, kernel architecture, file searching (findstr/forfiles), and Sysinternals Suite (pslist, listdlls, autorunsc, handle, sigcheck, accesschk, procdump).  
> **When to Apply:** Apply when performing initial Windows host triage (s_init_unknown), investigating running processes/PPIDs, mapping svchost.exe services, hunting unsigned/injected DLLs, searching files by timestamp/content, or executing Sysinternals live response.  
> **Target OS Platform:** `windows` | **Primary H-MDP Tactic:** `Passive_Enum` (`s_init_unknown -> s_passive_topology_mapped`)  
> **Bayesian Root-Cause Alignment (`Engine 4`):** `suspicious_process_lineage, service_misconfiguration, unsigned_dll_injection, resource_exhaustion`  
> **Network Isolation Compatibility:** `RED, BLUE, WHITE (100% local host telemetry compatible)`  
> **Backlinks:** [[00_MEMORY_INDEX]] | [[00_TRAINED_INDEX]] | [[reasoning/windows_kernel_and_userspace_enumeration_strategy_playbook]] | [[commands/windows_kernel_and_userspace_enumeration_playbook]] | [[commands/windows_master_command_playbook]] | [[commands/linux_master_command_playbook]]

---

## 1. Master Windows & Linux Command Matrix for This Domain

| Command Syntax (`Windows` / `Linux`) | OS / Shell | Operational Purpose & Key Flags | When to Apply & Expected Output | Cross-Platform Equivalent |
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

---

## 2. Organized Domain Knowledge Notes & Paired Command Playbooks (25 Notes)

| Topic | Knowledge Note (`knowledge/`) | Paired Command Playbook (`commands/`) | OS | Primary Tactic | When to Apply & Operational Summary |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Basic Survey Commands** | [[knowledge/trained_basic_survey_commands]] | [[commands/trained_basic_survey_commands]] | `windows` | `Passive_Enum` | Apply when working with Basic Survey Commands (windows): Apply when performing initial Windows host triage (s_init_unknown), investigating r |
| **BCF Windows Live Response** | [[knowledge/trained_bcf_windows_live_response]] | [[commands/trained_bcf_windows_live_response]] | `windows` | `Passive_Enum` | Apply when working with BCF Windows Live Response (windows): Apply when performing initial Windows host triage (s_init_unknown), investigati |
| **BCF Windows Process Investigation** | [[knowledge/trained_bcf_windows_process_investigation]] | [[commands/trained_bcf_windows_process_investigation]] | `windows` | `Passive_Enum` | Apply when working with BCF Windows Process Investigation (windows): Apply when performing initial Windows host triage (s_init_unknown), inv |
| **CQC001 E020 M010 Kernel Functions** | [[knowledge/trained_cqc001_e020_m010_kernel_functions]] | [[commands/windows_master_command_playbook]] / [[commands/linux_master_command_playbook]] | `windows` | `Passive_Enum` | Apply when working with CQC001 E020 M010 Kernel Functions (windows): Apply when performing initial Windows host triage (s_init_unknown), inv |
| **CQC001 E020 M010 Kernel Mode Components** | [[knowledge/trained_cqc001_e020_m010_kernel_mode_components]] | [[commands/windows_master_command_playbook]] / [[commands/linux_master_command_playbook]] | `windows` | `Passive_Enum` | Apply when working with CQC001 E020 M010 Kernel Mode Components (windows): Apply when performing initial Windows host triage (s_init_unknown |
| **CQC001 E020 M010 Sysinternals Tools** | [[knowledge/trained_cqc001_e020_m010_sysinternals_tools]] | [[commands/trained_cqc001_e020_m010_sysinternals_tools]] | `windows` | `Passive_Enum` | Apply when working with CQC001 E020 M010 Sysinternals Tools (windows): Apply when performing initial Windows host triage (s_init_unknown), i |
| **CQC001 E020 M040 transcript** | [[knowledge/trained_cqc001_e020_m040_transcript]] | [[commands/trained_cqc001_e020_m040_transcript]] | `windows` | `Passive_Enum` | Apply when working with CQC001 E020 M040 transcript (windows): Apply when performing initial Windows host triage (s_init_unknown), investiga |
| **CQC001 E020 M040 Windows Processes** | [[knowledge/trained_cqc001_e020_m040_windows_processes]] | [[commands/trained_cqc001_e020_m040_windows_processes]] | `windows` | `Passive_Enum` | Apply when working with CQC001 E020 M040 Windows Processes (windows): Apply when performing initial Windows host triage (s_init_unknown), in |
| **CQC001 E020 M050 S040 I030 Exer X010 C010 transcript** | [[knowledge/trained_cqc001_e020_m050_s040_i030_exer_x010_c010_transcript]] | [[commands/trained_cqc001_e020_m050_s040_i030_exer_x010_c010_transcript]] | `windows` | `Passive_Enum` | Apply when working with CQC001 E020 M050 S040 I030 Exer X010 C010 transcript (windows): Apply when performing initial Windows host triage (s |
| **Find** | [[knowledge/trained_find]] | [[commands/trained_find]] | `windows` | `Passive_Enum` | Apply when working with Find (windows): Apply when performing initial Windows host triage (s_init_unknown), investigating running processes/ |
| **Findstr** | [[knowledge/trained_findstr]] | [[commands/trained_findstr]] | `windows` | `Passive_Enum` | Apply when working with Findstr (windows): Apply when performing initial Windows host triage (s_init_unknown), investigating running process |
| **FORFILES** | [[knowledge/trained_forfiles]] | [[commands/trained_forfiles]] | `windows` | `Passive_Enum` | Apply when working with FORFILES (windows): Apply when performing initial Windows host triage (s_init_unknown), investigating running proces |
| **Net-SC CMDs** | [[knowledge/trained_net-sc_cmds]] | [[commands/trained_net-sc_cmds]] | `windows` | `Passive_Enum` | Apply when working with Net-SC CMDs (windows): Apply when performing initial Windows host triage (s_init_unknown), investigating running pro |
| **Net CMDs 1** | [[knowledge/trained_net_cmds_1]] | [[commands/trained_net_cmds_1]] | `windows` | `Passive_Enum` | Apply when working with Net CMDs 1 (windows): Apply when performing initial Windows host triage (s_init_unknown), investigating running proc |
| **OS Internals  Kernel & Hardware** | [[knowledge/trained_os_internals__kernel_hardware]] | [[commands/trained_os_internals__kernel_hardware]] | `windows` | `Passive_Enum` | Apply when working with OS Internals  Kernel & Hardware (windows): Apply when performing initial Windows host triage (s_init_unknown), inves |
| **PsService CMDs** | [[knowledge/trained_psservice_cmds]] | [[commands/trained_psservice_cmds]] | `windows` | `Passive_Enum` | Apply when working with PsService CMDs (windows): Apply when performing initial Windows host triage (s_init_unknown), investigating running  |
| **Survey CMDs** | [[knowledge/trained_survey_cmds]] | [[commands/trained_survey_cmds]] | `windows` | `Passive_Enum` | Apply when working with Survey CMDs (windows): Apply when performing initial Windows host triage (s_init_unknown), investigating running pro |
| **Survey CMDs -2** | [[knowledge/trained_survey_cmds_-2]] | [[commands/trained_survey_cmds_-2]] | `windows` | `Passive_Enum` | Apply when working with Survey CMDs -2 (windows): Apply when performing initial Windows host triage (s_init_unknown), investigating running  |
| **Systeminfo** | [[knowledge/trained_systeminfo]] | [[commands/trained_systeminfo]] | `windows` | `Passive_Enum` | Apply when working with Systeminfo (windows): Apply when performing initial Windows host triage (s_init_unknown), investigating running proc |
| **Tasklist** | [[knowledge/trained_tasklist]] | [[commands/trained_tasklist]] | `windows` | `Passive_Enum` | Apply when working with Tasklist (windows): Apply when performing initial Windows host triage (s_init_unknown), investigating running proces |
| **Triage-Scripts** | [[knowledge/trained_triage-scripts]] | [[commands/trained_triage-scripts]] | `windows` | `Passive_Enum` | Apply when working with Triage-Scripts (windows): Apply when performing initial Windows host triage (s_init_unknown), investigating running  |
| **Type** | [[knowledge/trained_type]] | [[commands/trained_type]] | `windows` | `Passive_Enum` | Apply when working with Type (windows): Apply when performing initial Windows host triage (s_init_unknown), investigating running processes/ |
| **Win Local CMDs** | [[knowledge/trained_win_local_cmds]] | [[commands/trained_win_local_cmds]] | `windows` | `Passive_Enum` | Apply when working with Win Local CMDs (windows): Apply when performing initial Windows host triage (s_init_unknown), investigating running  |
| **windows command line Administration** | [[knowledge/trained_windows_command_line_administration]] | [[commands/trained_windows_command_line_administration]] | `windows` | `Passive_Enum` | Apply when working with windows command line Administration (windows): Apply when performing initial Windows host triage (s_init_unknown), i |
| **wp-windows-management-instrumentation** | [[knowledge/trained_wp-windows-management-instrumentation]] | [[commands/trained_wp-windows-management-instrumentation]] | `windows` | `Passive_Enum` | Apply when working with wp-windows-management-instrumentation (windows): Apply when performing initial Windows host triage (s_init_unknown), |
