---
title: "Trained Command Playbook: wp-windows-management-instrumentation"
category: commands
domain_hub: "[[knowledge/01_windows_system_process_and_sysinternals]]"
os_platform: windows
primary_tactic: Passive_Enum
summary: "Verified Windows & Linux command playbook for wp-windows-management-instrumentation (Passive_Enum): Windows live incident response, process tree/PPID investigation, service binary auditing, kernel architecture, file searching (findstr/"
when_to_apply: "Apply when working with wp-windows-management-instrumentation (windows): Apply when performing initial Windows host triage (s_init_unknown), investigating running processes/PPIDs, mapping svchost.exe services, hunting unsigned/injected DLLs, searching files by timestamp/content, or executing Sysinternals live response."
tags: [credential_access, curl, enumeration, http, https, lateral_movement_routing_pivot, mdp, passive_enum, pdf, powershell, sysinternals, trained, wmic, windows, pslist, listdlls, autorunsc, psservice, psloggedon, handle, sigcheck, accesschk]
source_file: "wp-windows-management-instrumentation"
updated: 2026-10-30
---

systeminfo && whoami /all
# Trained Command Playbook: `wp-windows-management-instrumentation.pdf`
systeminfo && whoami /all
- **Source Document:** `~/Projects/CORA/Training/wp-windows-management-instrumentation.pdf`
- **CEGAR Verified Commands:** `50` (`0` malformed/unsafe snippets filtered)
- **MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`):** `50`
- **Discovered IPs/Subnets:** `1.5.0.7, 127.0.0.1, 172.24.72.131, 172.24.72.134, 172.24.72.135, 2.2.2.7, 5.9.7.6, 7.0.0.1, 7.0.3.5, 8.1.0.4, 8.4.9.8, 9.1.7.0, 9.4.2.9`
- **Discovered Interfaces:** `Lo`
- **Related Knowledge Note:** [[knowledge/trained_wp-windows-management-instrumentation]]
systeminfo && whoami /all
## Distilled MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`)
| Pre-State ($s$) | Tactic ($\tau$) | Technique ($k$) | Tool ($u$) | Post-State ($s'$) | Verified Command ($c$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `wmic` | `s_passive_topology_mapped` | `wmic and wmis-pth for Linux` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `get-wminamespace-namespace$ns` | `s_active_services_enumerated` | `Get-WmiNamespace-Namespace$ns` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `get-wmiobject` | `s_credentials_or_certs_acquired` | `Get-WmiObject -Class Win32_Process -ComputerName` |
| `s_firewall_or_acl_unlocked` | **`Lateral_Movement_Routing_Pivot`** | Remote Host Execution, L2/L3 Route Injection & Subnet Pivot | `test-wsman` | `s_cross_subnet_pivot_routed` | `Test-WSMan -ComputerName 172.24.72.134` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `get-wmiobject-namespace$namespace-class__namespace` | `s_passive_topology_mapped` | `Get-WmiObject-Namespace$Namespace-Class__NAMESPACE\|ForEach-Object {` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `get-wminamespace` | `s_active_services_enumerated` | `$WmiClasses=Get-WmiNamespace\|ForEach-Object {` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `get-ciminstance` | `s_credentials_or_certs_acquired` | `Get-CimInstance -CimSession $CimSession -ClassName Win32_Process` |
| `s_firewall_or_acl_unlocked` | **`Lateral_Movement_Routing_Pivot`** | Remote Host Execution, L2/L3 Route Injection & Subnet Pivot | `new-cimsession` | `s_cross_subnet_pivot_routed` | `$CimSession = New-CimSession -ComputerName 172.24.72.134 -Credential 'WIN-B85AAA7ST4U Administrator' -Authentic` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `get-wmiobject-namespace$namespace-list` | `s_passive_topology_mapped` | `Get-WmiObject-Namespace$Namespace-List\| ForEach-Object { $_.Path.Path }` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `get-cimassociatedinstance` | `s_active_services_enumerated` | `Get-CimAssociatedInstance` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `new-objectmanagement.connectionoptions` | `s_credentials_or_certs_acquired` | `$Options=New-ObjectManagement.ConnectionOptions` |
| `s_firewall_or_acl_unlocked` | **`Lateral_Movement_Routing_Pivot`** | Remote Host Execution, L2/L3 Route Injection & Subnet Pivot | `invoke-wmimethod` | `s_cross_subnet_pivot_routed` | `Invoke-WmiMethod -Class Win32_Process -Name Create -ArgumentList 'notepad.exe' -ComputerName 172.24.72.134 -Cre` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `get-wmiobject` | `s_passive_topology_mapped` | `Get-WmiObject` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `get-cimclass` | `s_active_services_enumerated` | `Get-CimClass` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `new-objectmanagement.managementscope` | `s_credentials_or_certs_acquired` | `$Connection=New-ObjectManagement.ManagementScope` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `get-ciminstance` | `s_passive_topology_mapped` | `Get-CimInstance` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `get-cimsession` | `s_active_services_enumerated` | `Get-CimSession` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `administrator` | `s_credentials_or_certs_acquired` | `$Credential=Get-Credential'WIN-B85AAA7ST4U\Administrator'` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `get-wmiobject` | `s_passive_topology_mapped` | `Get-WmiObject -Namespace root\SecurityCenter2 -Class AntiVirusProduct` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `set-wmiinstance` | `s_active_services_enumerated` | `Set-WmiInstance` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `get-wmiobject-class__filtertoconsumerbinding@arguments` | `s_credentials_or_certs_acquired` | `Get-WmiObject-Class__FilterToConsumerBinding@Arguments` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `get-wmiobjectwin32_bios-filter'serialnumber` | `s_passive_topology_mapped` | `$VMBios=Get-WmiObjectWin32_BIOS-Filter'SerialNumber LIKE "%VMware%"'` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `set-ciminstance` | `s_active_services_enumerated` | `Set-CimInstance` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `get-wmiobject-class__eventfilter@arguments` | `s_credentials_or_certs_acquired` | `Get-WmiObject-Class__EventFilter@Arguments` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `get-wmiobjectwin32_process-filter'name="vmtoolsd` | `s_passive_topology_mapped` | `$VMToolsRunning=Get-WmiObjectWin32_Process-Filter'Name="vmtoolsd.exe"'` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `invoke-wmimethod` | `s_active_services_enumerated` | `Invoke-WmiMethod` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `get-wmiobject-class__eventconsumer@arguments` | `s_credentials_or_certs_acquired` | `Get-WmiObject-Class__EventConsumer@Arguments` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `ver` | `s_passive_topology_mapped` | `ver file contains a single unsigned 32-bit` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `invoke-cimmethod` | `s_active_services_enumerated` | `Invoke-CimMethod` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `type` | `s_passive_topology_mapped` | `TYPE qualifier with the value uint32.` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `new-ciminstance` | `s_active_services_enumerated` | `New-CimInstance` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `new-cimsession` | `s_active_services_enumerated` | `New-CimSession` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `new-cimsessionoption` | `s_active_services_enumerated` | `New-CimSessionOption` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `register-cimindicationevent` | `s_active_services_enumerated` | `Register-CimIndicationEvent` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `register-wmievent` | `s_active_services_enumerated` | `Register-WmiEvent` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `remove-ciminstance` | `s_active_services_enumerated` | `Remove-CimInstance` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `remove-wmiobject` | `s_active_services_enumerated` | `Remove-WmiObject` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `remove-cimsession` | `s_active_services_enumerated` | `Remove-CimSession` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `ls` | `s_active_services_enumerated` | `ls WSMan:\localhost` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `set-wmiinstance-class__eventfilter-` | `s_active_services_enumerated` | `$WMIEventFilter=Set-WmiInstance-Class__EventFilter-` |
systeminfo && whoami /all
## Verified Executable Commands (Grouped by Capability Layer)
systeminfo && whoami /all
### General_System (50 commands)
```bash
wmic and wmis-pth for Linux
Get-WmiObject-Namespace$Namespace-Class__NAMESPACE|ForEach-Object {
Get-WmiNamespace-Namespace$ns
$WmiClasses=Get-WmiNamespace|ForEach-Object {
Get-WmiObject-Namespace$Namespace-List| ForEach-Object { $_.Path.Path }
Get-WmiObject
Get-CimAssociatedInstance
Get-CimClass
Get-CimInstance
Get-CimSession
Set-WmiInstance
Set-CimInstance
Invoke-WmiMethod
Invoke-CimMethod
New-CimInstance
New-CimSession
New-CimSessionOption
Register-CimIndicationEvent
Register-WmiEvent
Remove-CimInstance
Remove-WmiObject
Remove-CimSession
Get-WmiObject -Class Win32_Process -ComputerName
ls WSMan:\localhost
Test-WSMan -ComputerName 172.24.72.134
$CimSession = New-CimSession -ComputerName 172.24.72.134 -Credential 'WIN-B85AAA7ST4U Administrator' -Authentic
Get-CimInstance -CimSession $CimSession -ClassName Win32_Process
$WMIEventFilter=Set-WmiInstance-Class__EventFilter-
$WMIEventConsumer=Set-WmiInstance-
Set-WmiInstance-Class__FilterToConsumerBinding-
Get-WmiObject -Namespace root\SecurityCenter2 -Class AntiVirusProduct
$VMBios=Get-WmiObjectWin32_BIOS-Filter'SerialNumber LIKE "%VMware%"'
$VMToolsRunning=Get-WmiObjectWin32_Process-Filter'Name="vmtoolsd.exe"'
Invoke-WmiMethod -Class Win32_Process -Name Create -ArgumentList 'notepad.exe' -ComputerName 172.24.72.134 -Cre
$Options=New-ObjectManagement.ConnectionOptions
$Connection=New-ObjectManagement.ManagementScope
$Credential=Get-Credential'WIN-B85AAA7ST4U\Administrator'
Invoke-WmiMethod@CommonArgs-ClassWin32_Process-NameCreate-
Invoke-WmiMethod@CommonArgs-ClassStdRegProv-NameCreateKey-
Invoke-WmiMethod@CommonArgs-ClassStdRegProv-NameDeleteValue-
Set-ItemProperty -Path HKLM:\SOFTWARE\EvilKey -Name Result -Value
$RemoteOutput=Invoke-WmiMethod@CommonArgs-ClassStdRegProv-
Get-WmiObject-Class__FilterToConsumerBinding@Arguments
Get-WmiObject-Class__EventFilter@Arguments
Get-WmiObject-Class__EventConsumer@Arguments
last time.
ver file contains a single unsigned 32-bit
locate classes and instances. For
locate its offset. The index operates
TYPE qualifier with the value uint32.
```
systeminfo && whoami /all

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
