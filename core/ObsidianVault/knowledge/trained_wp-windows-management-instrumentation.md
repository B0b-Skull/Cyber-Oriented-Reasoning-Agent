---
title: "Trained Knowledge & Topology: wp-windows-management-instrumentation"
category: knowledge
domain_hub: "[[knowledge/01_windows_system_process_and_sysinternals]]"
os_platform: windows
primary_tactic: Passive_Enum
summary: "Operational architecture, decision workflows & Windows/Linux command reference for wp-windows-management-instrumentation: Windows live incident response, process tree/PPID investigation, service binary auditing, kernel architecture, file searching (fin"
when_to_apply: "Apply when working with wp-windows-management-instrumentation (windows): Apply when performing initial Windows host triage (s_init_unknown), investigating running processes/PPIDs, mapping svchost.exe services, hunting unsigned/injected DLLs, searching files by timestamp/content, or executing Sysinternals live response."
tags: [credential_access, curl, enumeration, http, https, lateral_movement_routing_pivot, mdp, passive_enum, pdf, powershell, sysinternals, trained, wmic, windows, pslist, listdlls, autorunsc, psservice, psloggedon, handle, sigcheck, accesschk]
source_file: "wp-windows-management-instrumentation"
updated: 2026-10-30
---

# Trained Knowledge & Architecture: `wp-windows-management-instrumentation.pdf`

- **Source Path:** `~/Projects/CORA/Training/wp-windows-management-instrumentation.pdf` (`pdf`)
- **Extracted Technical Entities:** `curl, http, https, powershell, sysinternals, wmic`
- **Extracted IPs / Subnets:** `1.5.0.7, 127.0.0.1, 172.24.72.131, 172.24.72.134, 172.24.72.135, 2.2.2.7, 5.9.7.6, 7.0.0.1, 7.0.3.5, 8.1.0.4, 8.4.9.8, 9.1.7.0, 9.4.2.9`
- **Extracted Interfaces:** `Lo`
- **Linked Command Playbook:** [[commands/trained_wp-windows-management-instrumentation]] (`50` CEGAR-verified commands | `50` MDP transitions)

## Command & Tactic Coverage Summary
- **Total CEGAR-Verified Commands:** `50` (full executable list in [[commands/trained_wp-windows-management-instrumentation]])
- **Tactic Distribution:** `Enumeration` (29), `Passive_Enum` (10), `Credential_Access` (8), `Lateral_Movement_Routing_Pivot` (3)
- **Top Extracted CLI Tools:** `get-wmiobject` (3), `get-ciminstance` (2), `invoke-wmimethod` (2), `locate` (2), `new-cimsession` (2), `administrator` (1), `get-cimassociatedinstance` (1), `get-cimclass` (1), `get-cimsession` (1), `get-wminamespace` (1), `get-wminamespace-namespace$ns` (1), `get-wmiobject-class__eventconsumer@arguments` (1), `get-wmiobject-class__eventfilter@arguments` (1), `get-wmiobject-class__filtertoconsumerbinding@arguments` (1), `get-wmiobject-namespace$namespace-class__namespace` (1), `get-wmiobject-namespace$namespace-list` (1), `get-wmiobjectwin32_bios-filter'serialnumber` (1), `get-wmiobjectwin32_process-filter'name="vmtoolsd` (1), `invoke-cimmethod` (1), `invoke-wmimethod@commonargs-classstdregprov-` (1), `invoke-wmimethod@commonargs-classstdregprov-namecreatekey-` (1), `invoke-wmimethod@commonargs-classstdregprov-namedeletevalue-` (1), `invoke-wmimethod@commonargs-classwin32_process-namecreate-` (1), `last` (1), `ls` (1)

## LLM Distilled Operational Summary
### Key Operational Techniques & Decision Workflows

*   **Architecture & Standards**: Leverage WMI as the Microsoft implementation of the Web-Based Enterprise Management (WBEM) and Common Information Model (CIM) standards to query, structure, and transmit data regarding managed components (e.g., processes, services, registry).
*   **Data Consumption**: Utilize native tools like PowerShell for simple interaction and execution of WMI methods.
*   **Querying Strategy**: Use the WMI Query Language (WQL), a SQL-like language, to perform fine-grained control over object retrieval.
*   **Attack Vectors**:
    *   **Reconnaissance**: Perform system discovery and environment mapping.
    *   **Detection Evasion**: Utilize WMI for Anti-Virus and Virtual Machine (VM) detection.
    *   **Execution & Movement**: Execute code locally or remotely, facilitate lateral movement, establish persistence, and exfiltrate data.
    *   **C2 Channels**: Implement "Push" (server-initiated) or "Pull" (client-initiated) attack patterns using WMI eventing.
*   **Defense & Forensics**: Deploy existing detection utilities, build custom IDS using WMI eventing, and analyze the underlying CIM Repository file structures (MOF files, `index.btr`, `object.data`) for forensic investigation.

### Critical Command Patterns and Required Flags

*   **PowerShell**: Primary tool for interacting with WMI classes and executing methods.
*   **wmic.exe**: Legacy command-line interface for WMI operations.
*   **wbemtest.exe**: Utility for testing WMI connections and querying specific instances.
*   **WMI Explorer / CIM Studio**: GUI-based tools for visualizing namespaces, classes, and instances.
*   **Windows Script Host (WSH)**: Supports scripting languages (VBScript, JScript) for automation.
*   **COM API (IWbem*)**: Low-level C/C++ interface for programmatic access.
*   **.NET System.Management**: Managed code framework for WMI interaction.
*   **winrm.exe**: Enables remote management sessions over HTTP/HTTPS.
*   **wmic & wmis-pth**: Linux-based tools for interacting with Windows WMI remotely.

### Network Topology, IP/Subnet, Serial, and Service Relationships

*   **Protocol Foundation**: WMI relies on the Distributed Component Object Model (DCOM) for local and remote communication.
*   **Remote Management**: Utilizes Windows Remote Management (WinRM) protocols to extend reach across network boundaries.
*   **Eventing Mechanism**: Operates via an event filter/consumer model requiring specific system privileges and configuration to trigger actions (Intrinsic or Extrinsic events).
*   **Persistence**: Achieved through `ActiveScriptEventConsumer` instances, which allow scripts to run automatically upon specific system events.
*   **Storage**: Data is persisted in the CIM Repository, consisting of MOF files, binary index files (`index.btr`), and object data files (`object.data`).

## Document Structure & Key Topics
- Prep file to drop on remote system
- Establish remote WMI connection
- “Push” file contents
- The PowerShell payload that will drop the stored file contents
- Drop the file to the target filesystem
- Confirm successful file drop
- Create a remote registry key and value
- PowerShell payload that saves the serialized output of `Get-Process
- Invoke PowerShell payload
- Pull the serialized results back
- Deserialize and display the result of the command executed on the

## Extracted Operational Steps & Workflows
- 1.	 Instance queries – Used to query WMI class instances
- 2.	 Event queries – Used as a WMI event registration mechanism – e.g. WMI object
- 3.	 Meta queries – Used to query WMI class schemas
- 1.	 An event filter – The event of interest
- 2.	 An event consumer – An action to perform upon triggering an event
- 3.	 A filter to consumer binding – The registration mechanism that binds a filter
- 1.	 An attacker uses WMI as a
- 2.	 The WMI Shell utility is used as a C2
- 3.	 WMI classes are created to store
- 4.	 An attacker installs a malicious WMI
- 5.	 An attacker persists via the Start
- 6.	 An attacker persists via other
- 7.	 An attacker installs a service
- 1.	 System administrators can disable
- 2.	 Consider blocking the WMI protocol
- 3.	 WMI, DCOM, and WinRM events
- 1.	 Locate the \\.\ROOT\default
- 2.	 Find the class definition for
- 3.	 Enumerate class definitions of the
- 4.	 Build the class layout from the class
- 5.	 Find the class instance object of
- 6.	 Parse the class instance object using
- 7.	 Return the value from property
- 40. Nodes with similar keys showed
- 1.	 NS_2DDE46913C837E49ADBBDD92
- 2.	 NS_86C68CC88277F15FBE6F6D9A
- 3.	 NS_8DFCCA0B7FAB09C327554074
- 4.	 NS_AC3EFBD18065EBF47BE8D959
- 5.	 NS_DA2786B86FA728AF4EC85C5C
- 6.	 NS_DD73323810DAB2D362482D85

<!-- CORA-MAXIMIZED-COMMANDS-START -->
## Maximized Windows & Linux Command Examples for `wp-windows-management-instrumentation`

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
