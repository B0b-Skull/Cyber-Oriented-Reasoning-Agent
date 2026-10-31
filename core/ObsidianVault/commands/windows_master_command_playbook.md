---
title: "Windows Master Command Playbook (CMD, PowerShell, WMI/CIM, Sysinternals, Netsh, Registry, ACLs & Auditing)"
category: commands
domain_hub: "[[knowledge/01_windows_system_process_and_sysinternals]]"
os_platform: windows
primary_tactic: Passive_Enum
summary: "Comprehensive Windows operational command playbook covering CMD, PowerShell, WMI/CIM, Sysinternals, Registry, Netsh Firewall/Routing, ICACLS permissions, AuditPol, Wevtutil Event Logs, and Active Directory with flag explanations and When-to-Apply rules."
when_to_apply: "Apply whenever operating on, enumerating, triaging, hardening, or troubleshooting a Windows host or Active Directory environment across L2/L3 networking, processes, services, registry persistence, file ACLs, firewall rules, or security event logs."
tags: [windows, powershell, cmd, sysinternals, wmic, netsh, ipconfig, netstat, icacls, auditpol, wevtutil, bcdedit, reg, tasklist, sc, schtasks, dsquery, kerberos, passive_enum, active_enum, defense_evasion_firewall, privilege_escalation, credential_access]
updated: 2026-10-30
---

# Windows Master Command Playbook (`CMD`, `PowerShell`, `WMI/CIM`, `Sysinternals`, `Netsh` & `AD`)

> **Summary:** Authoritative Windows command reference with flag-by-flag breakdowns, expected outputs, 15-Engine H-MDP state triggers, and Linux cross-platform equivalents.  
> **Backlinks:** [[00_MEMORY_INDEX]] | [[00_TRAINED_INDEX]] | [[commands/linux_master_command_playbook]]  
> **Domain Knowledge Hubs:** [[knowledge/01_windows_system_process_and_sysinternals]] | [[knowledge/02_windows_registry_boot_and_persistence]] | [[knowledge/03_windows_security_acls_auditing_and_logs]] | [[knowledge/04_windows_powershell_wmi_cim_and_active_directory]] | [[knowledge/05_windows_and_linux_networking_routing_and_firewalls]]

---

## When to Apply (LLM & 15-Engine Decision Matrix)

| Operational Scenario / Symptom | H-MDP Pre-State ($s$) | Optimal Tactic ($\tau$) | Primary Windows Tools | Isolation Compatibility |
| :--- | :--- | :--- | :--- | :--- |
| **Initial Host Triage & OS Baseline** | `s_init_unknown` | `Passive_Enum` | `systeminfo`, `whoami /all`, `tasklist /svc`, `Get-ComputerInfo` | `RED`, `BLUE`, `WHITE` |
| **L2/L3 Adapter, IP, Route & ARP Verification** | `s_init_unknown` | `Passive_Enum` | `ipconfig /all`, `route print -4`, `arp -a`, `Get-NetAdapter`, `Get-NetRoute` | `RED`, `BLUE`, `WHITE` |
| **L4 Listening Ports & Established Socket Audit** | `s_passive_topology_mapped` | `Passive_Enum` | `netstat -ano`, `netstat -abno`, `Get-NetTCPConnection`, `tcpvcon -a -c` | `RED`, `BLUE`, `WHITE` |
| **Cross-Subnet Reachability & Port Probing** | `s_l2_l3_verified` | `Active_Enum` | `ping -n 3 -w 1200`, `tracert -d`, `Test-NetConnection`, `nslookup` | `RED`, `BLUE` (Allowed NICs) |
| **Suspicious Process, DLL Injection & Handle Triage** | `s_init_unknown` | `Passive_Enum` | `wmic process`, `pslist -t`, `listdlls`, `handle -a`, `sigcheck -e -u`, `procdump` | `RED`, `BLUE`, `WHITE` |
| **Registry Run Keys, Services & Boot Persistence** | `s_passive_topology_mapped` | `Passive_Enum` | `reg query`, `autorunsc -a * -c -h`, `sc qc`, `schtasks /query`, `bcdedit /enum` | `RED`, `BLUE`, `WHITE` |
| **File/Service DACL Permissions & Privilege Audit** | `s_initial_shell_or_api_access` | `Privilege_Escalation` | `icacls`, `takeown`, `accesschk -uwcqv`, `Get-Acl`, `whoami /priv` | `RED`, `BLUE`, `WHITE` |
| **Host Firewall, Portproxy & Audit Policy Control** | `s_oob_serial_enumerated` | `Defense_Evasion_Firewall` | `netsh advfirewall`, `netsh interface portproxy`, `auditpol`, `pktmon` | `RED`, `BLUE`, `WHITE` |
| **Event Log Forensics & Domain/Kerberos Recon** | `s_active_services_enumerated` | `Credential_Access` | `wevtutil qe`, `Get-WinEvent`, `psloglist`, `dsquery`, `nltest`, `klist`, `setspn` | `RED`, `BLUE`, `WHITE` |

---

## 1. Host Identity, OS Baseline & Privilege Context (`Passive_Enum`)

| Windows Command | Shell | Description & Key Flags | When to Apply & Expected Output | Linux Equivalent |
| :--- | :--- | :--- | :--- | :--- |
| `systeminfo` | CMD / PS | Displays OS build, architecture, install date, boot time, hotfixes (`KB*`), domain/workgroup, and NIC summary. | **Apply first** on any unknown Windows host (`s_init_unknown`) to identify OS version, patch level, and uptime. | `uname -a && hostnamectl && uptime` |
| `whoami /all` | CMD / PS | Outputs current user, SID, domain/local group memberships, Mandatory Integrity Level (`Medium`/`High`/`System`), and token privileges (`SeDebugPrivilege`, `SeImpersonatePrivilege`). | **Apply immediately** to verify elevation status and check for token privileges (`SeImpersonatePrivilege`, `SeBackupPrivilege`). | `id && sudo -l` |
| `wmic os get Caption,CSDVersion,OSArchitecture,Version,LastBootUpTime /format:list` | CMD | Queries `Win32_OperatingSystem` via WMI for exact OS version and boot timestamp without slow hotfix enumeration. | Apply when `systeminfo` is too slow over a constrained shell. | `cat /etc/os-release && uname -r` |
| `wmic qfe list full` | CMD | Lists all installed Quick Fix Engineering (`QFE`) Windows Update patches (`HotFixID`, `InstalledOn`). | Apply when checking if a host is missing security patches or verifying patch compliance. | `dpkg -l` / `rpm -qa` |
| `powershell -NoProfile -Command "Get-ComputerInfo \| Select-Object WindowsProductName,WindowsVersion,OsHardwareAbstractionLayer,CsDomain,CsProcessors"` | PowerShell | Structured PowerShell 5.1+ hardware, HAL, OS, and domain summary. | Apply in PowerShell sessions for structured object inspection. | `hostnamectl` |

---

## 2. L2/L3 Networking: Interfaces, IPv4/IPv6, Routing & ARP Cache (`Passive_Enum` & `L2_L3_Pivot_Routing`)

| Windows Command | Shell | Description & Key Flags | When to Apply & Expected Output | Linux Equivalent |
| :--- | :--- | :--- | :--- | :--- |
| `ipconfig /all` | CMD / PS | Displays all physical/virtual adapters, MAC (`Physical Address`), IPv4/IPv6, Subnet Mask, Default Gateway, DHCP server, and DNS servers. | **Primary L2/L3 passive probe** (`s_init_unknown -> s_passive_topology_mapped`). Identifies active NICs and local subnets. | `ip -4 -br addr show && ip -d link show` |
| `route print -4` | CMD / PS | Prints IPv4 active routing table (`Network Destination`, `Netmask`, `Gateway`, `Interface`, `Metric`) and persistent routes. | Apply when diagnosing `Destination host unreachable` or verifying static routes to remote subnets. | `ip route show table all` |
| `arp -a` | CMD / PS | Displays L2 ARP cache (`Internet Address`, `Physical Address`, `Type: dynamic/static`) per interface IP. | Apply to discover live L2 neighbors on local subnets without sending active scan sweeps. | `ip neigh show` |
| `arp -a <TARGET_IP>` | CMD / PS | Queries the ARP entry for a specific `<TARGET_IP>`. | **Engine 1/15 Consensus Probe** for verifying L2 MAC resolution of a target IP. | `ip neigh show <TARGET_IP>` |
| `route add <REMOTE_SUBNET> mask 255.255.255.0 <GATEWAY_IP> metric 1` | CMD (Admin) | Adds an active L3 static route for `<REMOTE_SUBNET>` via next-hop `<GATEWAY_IP>` (use `-p` to make persistent across reboots). | **Apply when geometric containment (`Engine 2`) reports `<TARGET_IP>` is DISJOINT** from local subnets and reachable via a known gateway. | `sudo ip route replace <REMOTE_SUBNET> via <GATEWAY_IP>` |
| `netsh interface ipv4 show interfaces` | CMD / PS | Lists all IPv4 interfaces with `Idx` (Interface Index), `Met` (Metric), `MTU`, `State` (`connected`/`disconnected`), and `Name`. | Apply before adding interface-scoped routes or checking MTU fragmentation issues (`Engine 2`). | `ip link show` |
| `netsh interface ipv4 show route` | CMD / PS | Displays detailed IPv4 route prefixes, next hops, and publish status via `netsh`. | Apply to verify `netsh` routing state and metric priorities. | `ip -4 route show` |
| `Get-NetAdapter \| Select-Object Name,InterfaceDescription,Status,MacAddress,LinkSpeed` | PowerShell | Enumerates physical and virtual network adapters (`Up`/`Disconnected`), MACs, and link speeds. | Apply in PowerShell to filter active interfaces (`Where-Object Status -eq 'Up'`). | `ip -br link show` |
| `Get-NetIPConfiguration` | PowerShell | Combines interface alias, IPv4/IPv6 address, default gateway, and DNS server per adapter. | Apply in PowerShell as a clean structured alternative to `ipconfig /all`. | `ip addr && resolvectl status` |
| `Get-NetRoute -AddressFamily IPv4 \| Where-Object {$_.NextHop -ne '0.0.0.0'}` | PowerShell | Lists all IPv4 gateway routes with `DestinationPrefix`, `NextHop`, `InterfaceAlias`, and `RouteMetric`. | Apply to quickly identify default and static gateways. | `ip -4 route show` |

---

## 3. L4 Sockets, Listening Ports, DNS & Active Connectivity (`Passive_Enum` & `Active_Enum`)

| Windows Command | Shell | Description & Key Flags | When to Apply & Expected Output | Linux Equivalent |
| :--- | :--- | :--- | :--- | :--- |
| `netstat -ano` | CMD / PS | Lists all TCP/UDP endpoints (`-a`), numerical IPs/ports (`-n`), state (`LISTENING`, `ESTABLISHED`, `TIME_WAIT`), and owning `PID` (`-o`). | **Primary L4 socket probe**: maps every open port and active connection to its owning process ID (`PID`). | `ss -tulpn && ss -tanp` |
| `netstat -abno` | CMD (Admin) | Includes the exact executable binary name (`[svchost.exe]`) and service DLL chain (`-b`) for every socket. | Apply when running as Administrator to immediately identify which binary bound a suspicious port. | `sudo ss -tulpn` |
| `netstat -ano \| findstr "LISTENING"` | CMD | Filters `netstat` output to show only locally listening TCP ports and their PIDs. | Apply to enumerate local attack surface or verify if a local service bound to `127.0.0.1` vs `0.0.0.0`. | `ss -tlnp` |
| `netstat -ano \| findstr "ESTABLISHED"` | CMD | Filters `netstat` output to show only active outbound/inbound TCP connections. | Apply during live response to spot active C2 beacons, lateral movement sessions, or database connections. | `ss -tnp state established` |
| `Get-NetTCPConnection -State Listen,Established \| Select-Object LocalAddress,LocalPort,RemoteAddress,RemotePort,State,OwningProcess` | PowerShell | Native PowerShell cmdlet returning structured TCP socket objects with `OwningProcess` PID. | Apply in PowerShell scripts to join `OwningProcess` directly with `Get-Process -Id`. | `ss -tanp` |
| `tcpvcon -a -c -n` | Sysinternals | Sysinternals CLI TCPView: outputs CSV (`-c`) of all endpoints (`-a`) without DNS delay (`-n`), including full process name and path. | Apply when Sysinternals is available for instant CSV socket-to-binary attribution. | `lsof -i -P -n` |
| `ping -n 2 -w 1200 <TARGET_IP>` | CMD / PS | Sends 2 ICMP Echo Requests (`-n 2`) with a 1200ms timeout (`-w 1200`). | Apply to verify L3 ICMP reachability and inspect reply TTL (`TTL=128` Windows, `TTL=64` Linux, `TTL=255` network appliance). | `ping -c 2 -W 1 <TARGET_IP>` |
| `tracert -d -h 15 -w 1000 <TARGET_IP>` | CMD / PS | Traces L3 hop path to `<TARGET_IP>` without DNS reverse lookup delay (`-d`), max 15 hops (`-h 15`). | Apply when packets drop mid-path to identify the exact router hop returning `TTL expired` or `Destination net unreachable`. | `traceroute -n -m 15 -w 1 <TARGET_IP>` |
| `powershell -NoProfile -Command "Test-NetConnection -ComputerName <TARGET_IP> -Port 443 -InformationLevel Detailed"` | PowerShell | Tests TCP 3-way handshake to `<TARGET_IP>:443`, resolves source interface, next-hop route, and ICMP status. | **Primary native Windows TCP port probe** when `nmap` is not installed. | `nc -zv -w 3 <TARGET_IP> 443` |
| `nslookup <TARGET_HOST>` / `Resolve-DnsName <TARGET_HOST>` | CMD / PS | Queries configured DNS server for `A`/`AAAA`/`PTR`/`SRV` records. | Apply when diagnosing name resolution failures or discovering Active Directory `_ldap._tcp.dc._msdcs.<DOMAIN>` SRV records. | `dig <TARGET_HOST>` / `nslookup <TARGET_HOST>` |
| `ipconfig /displaydns` | CMD / PS | Dumps local Windows DNS Client Resolver Cache (recently resolved domains and IPs). | **High-value passive forensics**: reveals domains/IPs recently contacted by the host without generating network traffic. | `resolvectl statistics` |
| `nbtstat -n` / `nbtstat -A <TARGET_IP>` | CMD | Lists local NetBIOS name table (`-n`) or queries remote host NetBIOS table (`-A <TARGET_IP>`). | Apply on legacy/enterprise LANs to identify Windows hostname, domain/workgroup, and `<20>` File Server service bit. | `nmblookup -A <TARGET_IP>` |

---

## 4. Processes, Services, DLLs & Scheduled Tasks (`Passive_Enum`)

| Windows Command | Shell | Description & Key Flags | When to Apply & Expected Output | Linux Equivalent |
| :--- | :--- | :--- | :--- | :--- |
| `tasklist /v /fo list` | CMD / PS | Lists all running processes with PID, Session Name, Memory Usage, Status, `User Name` context, CPU time, and Window Title (`/v`). | Apply to see which user account (`NT AUTHORITY\SYSTEM`, `LOCAL SERVICE`, or domain user) each process is running under. | `ps auxef` |
| `tasklist /svc` | CMD / PS | Maps every `svchost.exe` and service process PID to the exact Windows Service names hosted inside it. | **Critical when `netstat -ano` points to `svchost.exe`**: identifies which service inside `svchost.exe` owns the port. | `systemctl status <PID>` |
| `tasklist /m` / `tasklist /m <dllname>` | CMD / PS | Lists all DLL modules loaded by each process, or finds every process that has loaded a specific `<dllname>`. | Apply to hunt for injected or non-standard DLLs across running processes. | `lsof -p <PID>` / `cat /proc/<PID>/maps` |
| `wmic process get ProcessId,ParentProcessId,Name,ExecutablePath,CommandLine /format:list` | CMD | Extracts full process tree (`PID` + `PPID`), full disk path (`ExecutablePath`), and full `CommandLine` arguments for every process. | **Essential process investigation command**: `tasklist` hides command-line flags, whereas `wmic process` exposes encoded PowerShell commands and abnormal parent-child relationships (e.g., `cmd.exe` spawned by `w3wp.exe` or `winword.exe`). | `ps -eo pid,ppid,user,args` |
| `powershell -NoProfile -Command "Get-CimInstance Win32_Process \| Select-Object ProcessId,ParentProcessId,Name,ExecutablePath,CommandLine"` | PowerShell | Modern CIM equivalent of `wmic process` (works on Windows 11 / Server 2025 where `wmic` is deprecated). | Apply on modern Windows 10/11/Server 2019–2025 systems for complete command-line and PPID auditing. | `ps -ef` |
| `sc query state= all` | CMD / PS | Enumerates all installed Windows services (`RUNNING` and `STOPPED`), service names, display names, and states. | Apply to inventory all system services and spot rogue or stopped persistence services. | `systemctl list-units --type=service --all` |
| `sc qc <ServiceName>` | CMD / PS | Queries the configuration of `<ServiceName>`: `START_TYPE` (`AUTO_START`, `DEMAND_START`), `BINARY_PATH_NAME`, and `SERVICE_START_NAME` account. | **Apply during service auditing & privilege escalation**: checks for unquoted service paths (`BINARY_PATH_NAME`) and service account privileges. | `systemctl cat <service>` |
| `wmic service get Name,DisplayName,State,StartMode,PathName,StartName /format:list` | CMD | Dumps all services with their binary path (`PathName`), start mode, and execution account (`StartName`) in one command. | Apply to audit all service binary paths at once (`findstr /i /v "C:\Windows\\"`). | `systemctl list-unit-files --type=service` |
| `schtasks /query /fo LIST /v` | CMD / PS | Lists all Scheduled Tasks with `TaskName`, `Next Run Time`, `Task To Run` (command/script), `Run As User`, and `Schedule Type`. | Apply to discover scheduled persistence tasks or privileged tasks running custom scripts. | `crontab -l && ls -la /etc/cron*` |

---

## 5. Sysinternals Suite Live Response & Memory Triage (`Passive_Enum`)

> **Sysinternals EULA Flag:** Always pass `-accepteula` (e.g., `pslist -accepteula -t`) on first execution so the GUI EULA dialog never blocks non-interactive shells.

| Windows Command | Tool | Description & Key Flags | When to Apply & Expected Output | Linux Equivalent |
| :--- | :--- | :--- | :--- | :--- |
| `pslist -accepteula -t` | `pslist` | Displays parent-child process tree (`-t`) with PID, PPID, threads, handles, and CPU time. | Apply to visualize process lineage (`explorer.exe -> cmd.exe -> powershell.exe`) and spot anomalous parent processes. | `pstree -p -a` |
| `psloggedon -accepteula` | `psloggedon` | Shows both locally logged-on users (via registry `ProfileList`) and remote users connected via SMB/named pipes. | Apply during incident response to see active interactive and network logon sessions. | `w && who -a` |
| `psservice -accepteula query` / `psservice -accepteula security <Svc>` | `psservice` | Queries service status or dumps the exact security descriptor (DACL permissions) of `<Svc>` (`security`). | Apply when checking if a non-admin user has `SERVICE_CHANGE_CONFIG` or `SERVICE_START` rights on a privileged service. | `systemctl status` |
| `listdlls -accepteula -u` | `listdlls` | Lists only **unsigned** DLLs (`-u`) loaded into any running process, including version and load address. | **High-signal malware/injection hunter**: legitimate Windows system processes rarely load unsigned DLLs from user-writable paths. | `grep -E '\.so' /proc/*/maps` |
| `autorunsc -accepteula -a * -c -h -s -v` | `autorunsc` | Dumps all auto-start extension points (`-a *`: Run keys, services, drivers, scheduled tasks, WMI, Winlogon, KnownDLLs) as CSV (`-c`) with SHA256 hashes (`-h`) and signature verification (`-s`). | **Gold-standard Windows persistence sweep**: uncovers virtually every userland and kernel persistence mechanism in one pass. | `systemctl list-unit-files --state=enabled` |
| `handle -accepteula -a -u` | `handle` | Dumps all open handles (files, registry keys, mutants/mutexes, sections, threads) across processes (`-a`) with owning username (`-u`). | Apply to find which process holds a lock on a file or to detect malware mutexes (`BaseNamedObjects`). | `lsof` |
| `sigcheck -accepteula -e -u -vr C:\Windows\System32` | `sigcheck` | Scans executable files (`-e`) and reports only unsigned binaries (`-u`) inside `C:\Windows\System32`. | Apply to detect trojanized or masquerading binaries dropped into system directories. | `debsums -c` / `rpm -Va` |
| `accesschk -accepteula -uwcqv "Users" *` | `accesschk` | Lists all Windows services (`-c`) where the `"Users"` group has write (`-w`) or reconfiguration permissions. | **Primary service privilege-escalation finder**: identifies services whose `binPath` can be hijacked by a standard user. | `find /etc/systemd/system -writable` |
| `procdump -accepteula -ma <PID> C:\Temp\proc_<PID>.dmp` | `procdump` | Creates a full memory dump (`-ma`) of process `<PID>` for offline forensic/string analysis. | Apply when a suspicious process is running in memory (e.g., packed/hollowed binary) and you need its unpacked memory image. | `gcore <PID>` |

---

## 6. Windows Registry Architecture, Boot (`bcdedit`) & Persistence (`Passive_Enum`)

| Windows Command | Shell | Description & Key Flags | When to Apply & Expected Output | Linux Equivalent |
| :--- | :--- | :--- | :--- | :--- |
| `reg query "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Run"` | CMD / PS | Lists machine-wide startup programs executed at every user logon (`Run`). Also check `RunOnce`, `HKCU\...\Run`, and `Wow6432Node`. | Apply during every persistence survey to check standard registry autostart locations. | `ls -la /etc/xdg/autostart ~/.config/autostart` |
| `reg query "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon" /v Userinit` | CMD / PS | Inspects `Userinit` (default `C:\Windows\system32\userinit.exe,`) and `Shell` (default `explorer.exe`). | Apply to detect Winlogon helper persistence (comma-appended binaries after `userinit.exe,`). | `cat /etc/profile /etc/bash.bashrc` |
| `reg query "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager" /v BootExecute` | CMD / PS | Checks native boot-time executables (default `autocheck autochk *`). | Apply to detect early-boot native binaries executed before Win32 subsystem initialization. | `cat /etc/rc.local` |
| `reg query "HKLM\SYSTEM\CurrentControlSet\Services" /s /f "ImagePath"` | CMD / PS | Searches all Services registry keys recursively (`/s`) for `ImagePath` values. | Apply to audit all kernel driver and Win32 service binary paths directly from the registry hive. | `ls -la /etc/systemd/system/` |
| `reg query "HKLM\SYSTEM\CurrentControlSet\Enum\USBSTOR"` | CMD / PS | Lists historical USB mass storage devices connected to the Windows host (vendor, product, serial number). | **Apply during digital forensics (`Domain Hub 02/10`)** to prove removable media usage. | `dmesg \| grep -i usb` / `lsusb` |
| `reg query "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Memory Management" /v MoveImages` | CMD / PS | Checks Address Space Layout Randomization (`ASLR`) registry setting (`MoveImages`). | Apply when auditing OS memory protection mechanisms (`[[knowledge/trained_address_space_layout_randomization]]`). | `sysctl kernel.randomize_va_space` |
| `bcdedit /enum all` | CMD (Admin) | Enumerates Windows Boot Manager and Boot Loader entries (`nx` DEP policy: `OptIn`/`OptOut`/`AlwaysOn`/`AlwaysOff`, `testsigning`, `safeboot`, `debug`). | **Apply when auditing boot security, DEP (`nx`), or rootkit `testsigning` status** (`[[commands/trained_bcdedit_cmds]]`). | `cat /proc/cmdline && grubby --info=ALL` |

---

## 7. File System, NTFS Alternate Data Streams (`ADS`), Search & Timestamps (`Passive_Enum`)

| Windows Command | Shell | Description & Key Flags | When to Apply & Expected Output | Linux Equivalent |
| :--- | :--- | :--- | :--- | :--- |
| `dir /a /r C:\Users\Public` | CMD | Lists all files including hidden/system files (`/a`) and displays **NTFS Alternate Data Streams (`ADS`)** (`/r`, e.g., `file.txt:secret.exe:$DATA`). | **Apply when hunting hidden NTFS payloads** or `Zone.Identifier` download URLs (`[[knowledge/trained_cqc001_e020_m020_ntfs_cheat_sheets]]`). | `getfattr -d -m - <path>` |
| `dir /tc /od C:\Windows\System32` | CMD | Lists files sorted by Creation Date (`/tc /od`) oldest-to-newest so recently dropped files appear at the bottom. | Apply to spot newly dropped binaries/DLLs in `System32` whose timestamps differ from initial OS install (`[[commands/trained_basic_survey_commands]]`). | `ls -la --time=birth -rt /usr/bin` |
| `forfiles /p C:\ /s /m *.bat /c "cmd /c echo @path @fdate @ftime"` | CMD | Recursively (`/s`) searches for files matching mask (`/m`) and/or modification date (`/d +01/01/2026` or `/d -30`). | Apply to find recently modified scripts, configs, or staging archives (`[[commands/trained_forfiles]]`). | `find / -name "*.sh" -printf "%p %TY-%Tm-%Td\n"` |
| `findstr /s /i /n "password connectionString Bearer" C:\inetpub\*.config C:\Users\*.txt C:\Users\*.ps1` | CMD | Case-insensitive (`/i`) recursive (`/s`) regex/string search with line numbers (`/n`). | **Apply during post-exploitation & config auditing** to locate hardcoded credentials, API keys, or connection strings (`[[commands/trained_findstr]]`). | `grep -rnI -iE "password\|bearer" /var/www /home` |
| `powershell -NoProfile -Command "Get-ChildItem -Path C:\Users -Recurse -Include *.txt,*.ps1,*.xml,*.config -ErrorAction SilentlyContinue \| Select-String -Pattern 'password\|apikey\|secret'"` | PowerShell | PowerShell recursive content search across multiple file extensions with silent permission-denied handling. | Apply in PowerShell for fast multi-extension credential and artifact discovery. | `grep -rnI --include="*.conf" "secret" /etc` |
| `powershell -NoProfile -Command "Get-Item -Path C:\path\file.txt -Stream *"` / `Get-Content C:\path\file.txt -Stream Zone.Identifier` | PowerShell | Enumerates all NTFS streams attached to a file and reads the `Zone.Identifier` (`HostUrl` / `ReferrerUrl`) stream. | Apply to determine the exact external URL from which a file was downloaded. | `xattr -l <file>` |

---

## 8. File ACLs (`icacls`), Ownership (`takeown`) & SIDs (`Privilege_Escalation` & `Defense_Evasion_Firewall`)

| Windows Command | Shell | Description & Key Flags | When to Apply & Expected Output | Linux Equivalent |
| :--- | :--- | :--- | :--- | :--- |
| `icacls "C:\Program Files\App\service.exe"` | CMD / PS | Displays Discretionary Access Control List (`DACL`) entries: `(F)` Full, `(M)` Modify, `(RX)` Read & Execute, `(W)` Write, `(OI)` Object Inherit, `(CI)` Container Inherit. | **Apply whenever checking if a service binary, script, or config directory is writable** by `BUILTIN\Users`, `Everyone`, or `Authenticated Users` (`[[commands/trained_cacls_-_icacls_cmds]]`). | `getfacl <path> && ls -ld <path>` |
| `icacls C:\TargetDir /grant Users:(OI)(CI)F /T` | CMD (Admin) | Grants `Users` Full Control `(F)` with Object/Container Inheritance `(OI)(CI)` recursively (`/T`). | Apply when unlocking restrictive file/directory ACLs during remediation or authorized testing. | `chmod -R u+rwx <dir>` / `setfacl -R -m u:user:rwx <dir>` |
| `icacls C:\TargetFile /save C:\Temp\acl_backup.txt` | CMD (Admin) | Saves the exact SDDL DACL state of files to a backup file before modifying permissions (restore with `icacls C:\ /restore C:\Temp\acl_backup.txt`). | **Best practice before modifying ACLs**: guarantees 100% lossless ACL restoration. | `getfacl -R <dir> > acl_backup.txt` |
| `takeown /f "C:\TargetFile" /a` | CMD (Admin) | Transfers file ownership to the `Administrators` group (`/a`) (add `/r /d y` for recursive directory ownership). | Apply when `icacls` returns `Access is denied` because ownership belongs to `TrustedInstaller` or another SID. | `sudo chown root:root <file>` |
| `wmic useraccount get Name,Domain,SID,Status,Disabled,Lockout` | CMD / PS | Lists all user accounts and their Security Identifiers (`S-1-5-21-<domain>-<RID>`, where `RID 500` = Built-in Administrator, `501` = Guest). | Apply to map usernames to SIDs (`[[knowledge/trained_cqc001_e030_m010_well_known_sids]]`). | `getent passwd` |

---

## 9. Audit Policy (`auditpol`) & Windows Event Logs (`wevtutil` / `Get-WinEvent`)

| Windows Command | Shell | Description & Key Flags | When to Apply & Expected Output | Linux Equivalent |
| :--- | :--- | :--- | :--- | :--- |
| `auditpol /get /category:*` | CMD (Admin) | Displays the active Success/Failure audit policy across all categories and subcategories (`Logon/Logoff`, `Object Access`, `Privilege Use`, `Detailed Tracking`, `Account Management`). | **Apply first during log/forensic assessment** (`[[commands/trained_auditpol_cmds]]`) to see which security events are actually being recorded. | `sudo auditctl -l && sudo auditctl -s` |
| `auditpol /set /subcategory:"Process Creation" /success:enable /failure:enable` | CMD (Admin) | Enables Security Event ID `4688` (Process Creation) logging for both successful and failed process launches. | Apply when hardening a host or enabling process creation telemetry. | `sudo auditctl -a always,exit -F arch=b64 -S execve` |
| `wevtutil el` / `wevtutil gli Security` | CMD / PS | Lists all Windows Event Log channels (`el`) or inspects size, retention, and record count of the `Security` log (`gli`). | Apply to verify log capacity and last write time. | `journalctl --disk-usage` |
| `wevtutil qe Security /q:"*[System[(EventID=4624 or EventID=4625)]]" /c:15 /rd:true /f:text` | CMD (Admin) | Queries the `Security` log for the 15 most recent (`/rd:true /c:15`) Successful Logons (`4624`) and Failed Logons (`4625`) in plain text (`/f:text`). | **Apply to investigate authentication activity**, brute-force attempts (`4625`), and Logon Types (`Type 2` Interactive, `Type 3` Network/SMB, `Type 10` RDP). | `journalctl -u ssh -n 30` / `grep -E "Accepted\|Failed" /var/log/auth.log` |
| `wevtutil qe Security /q:"*[System[(EventID=4688 or EventID=4697 or EventID=4720 or EventID=1102)]]" /c:20 /rd:true /f:text` | CMD (Admin) | Queries for Process Creation (`4688`), Service Installed (`4697`), User Account Created (`4720`), or Audit Log Cleared (`1102`). | **High-priority incident response query**: catches persistence installation, rogue account creation, and log tampering (`[[knowledge/trained_cqc001_e030_m050_event_ids]]`). | `ausearch -m ADD_USER,DEL_USER,SERVICE_START` |
| `wevtutil qe System /q:"*[System[(EventID=7045)]]" /c:15 /rd:true /f:text` | CMD / PS | Queries `System` log for Event ID `7045` (New Service Installed), showing Service Name, Image Path, and Account. | Apply even when `Security` log auditing was disabled, because `System` Event `7045` is logged by Service Control Manager by default! | `journalctl -u systemd -n 30` |
| `powershell -NoProfile -Command "Get-WinEvent -FilterHashtable @{LogName='Microsoft-Windows-PowerShell/Operational'; Id=4104} -MaxEvents 10 \| Select-Object TimeCreated,Message \| Format-List"` | PowerShell | Extracts the 10 most recent PowerShell ScriptBlock Logging (`Event ID 4104`) entries containing de-obfuscated script blocks executed on the host. | **Apply when investigating PowerShell activity** (`[[knowledge/trained_windows_powershell_logging_cheat_sheet_ver_june_2016_v2]]`). | `cat ~/.bash_history` / `ausearch -m EXECVE` |

---

## 10. Windows Defender Firewall (`netsh advfirewall`) & Port Forwarding (`Defense_Evasion_Firewall`)

| Windows Command | Shell | Description & Key Flags | When to Apply & Expected Output | Linux Equivalent |
| :--- | :--- | :--- | :--- | :--- |
| `netsh advfirewall show allprofiles` | CMD / PS | Shows state (`ON`/`OFF`), inbound/outbound policy (`BlockInbound,AllowOutbound`), and log location for `Domain`, `Private`, and `Public` firewall profiles. | **Apply whenever Bayesian Root Cause (`Engine 4`) ranks `host_firewall_drop` or `acl_block`** (`[[commands/trained_netsh_fw_cmds]]`). | `sudo iptables -L -n -v && sudo nft list ruleset` |
| `netsh advfirewall firewall show rule name=all dir=in status=enabled` | CMD / PS | Lists all enabled inbound firewall rules, ports, programs, and actions (`Allow`/`Block`). | Apply to audit which inbound ports/binaries are permitted through the host firewall. | `sudo ufw status verbose` |
| `netsh advfirewall firewall add rule name="Allow_TCP_8443" dir=in action=allow protocol=TCP localport=8443` | CMD (Admin) | Adds an inbound allow rule for TCP port `8443`. | Apply when unlocking a blocked management/service port (`s_oob_serial_enumerated -> s_firewall_or_acl_unlocked`). | `sudo iptables -I INPUT 1 -p tcp --dport 8443 -j ACCEPT` |
| `netsh interface portproxy show all` | CMD / PS | Displays all configured IPv4/IPv6 TCP port-forwarding proxies (`v4tov4`, `v4tov6`) managed by the `iphlpsvc` service. | **Apply during both lateral movement & incident response**: reveals local loopback services exposed externally or pivot relays (`[[commands/trained_netsh_commands_for_routing]]`). | `sudo iptables -t nat -L PREROUTING -n -v` |
| `netsh interface portproxy add v4tov4 listenaddress=0.0.0.0 listenport=8443 connectaddress=127.0.0.1 connectport=8080` | CMD (Admin) | Forwards external TCP traffic arriving on `0.0.0.0:8443` to a loopback-bound service on `127.0.0.1:8080`. | **Apply when a target service is bound to `127.0.0.1:8080` (`service_bound_to_loopback`)** and needs external reachability. | `socat TCP-LISTEN:8443,fork,reuseaddr TCP:127.0.0.1:8080` |

---

## 11. Active Directory (`dsquery`, `net`, `nltest`), Kerberos & WinRM (`Active_Enum` & `Credential_Access`)

| Windows Command | Shell | Description & Key Flags | When to Apply & Expected Output | Linux Equivalent |
| :--- | :--- | :--- | :--- | :--- |
| `net user /domain` / `net group "Domain Admins" /domain` | CMD / PS | Queries the Primary Domain Controller for all domain users or members of the `"Domain Admins"` group. | Apply on domain-joined hosts to map privileged domain accounts (`[[commands/trained_net-sc_cmds]]`). | `ldapsearch -x -H ldap://<DC_IP> -b "dc=corp,dc=local"` |
| `nltest /dclist:<DOMAIN>` / `nltest /domain_trusts` | CMD / PS | Enumerates all Domain Controllers for `<DOMAIN>` and maps inbound/outbound forest and domain trust relationships. | **Apply first in Active Directory environments** (`[[commands/trained_domain_service_tools]]`) to locate DCs and cross-domain trust paths. | `dig _ldap._tcp.dc._msdcs.<DOMAIN> SRV` |
| `dsquery user -limit 0` / `dsquery computer -limit 0` | CMD (RSAT/DC) | Queries Active Directory LDAP for the Distinguished Names (`DN`) of all users or computers in the domain (`[[commands/trained_ds_cmds]]`). | Apply when `dsquery` is available to pipe DNs into `dsget user -samid -sid -memberof`. | `ldapsearch -LLL "(objectClass=computer)" cn dNSHostName` |
| `setspn -T <DOMAIN> -Q */*` | CMD / PS | Queries Active Directory for all registered Service Principal Names (`SPNs`, e.g., `MSSQLSvc/...`, `HTTP/...`) across user and computer accounts. | **Apply to discover domain services and Kerberoastable service accounts** (`[[knowledge/trained_kerberos_attacks_cheatsheet]]`). | `GetUserSPNs.py <DOMAIN>/<USER>@<DC_IP>` |
| `klist` / `klist sessions` | CMD / PS | Displays cached Kerberos Ticket Granting Tickets (`TGT`) and Service Tickets (`TGS`) in the current logon session. | Apply to inspect active Kerberos encryption types (`AES256`, `RC4-HMAC`) and ticket lifetimes. | `klist` |
| `gpresult /r /z` | CMD / PS | Generates a verbose Resultant Set of Policy (`RSoP`) report showing applied Group Policy Objects (`GPOs`), login scripts, and security settings. | Apply to identify GPO-enforced firewall rules, AppLocker policies, or logon script paths. | `realm list` / `sssctl domain-status` |
| `winrm enumerate winrm/config/listener` | CMD / PS | Lists active WS-Management (`WinRM`) HTTP (`5985`) and HTTPS (`5986`) listeners and bound IP addresses. | Apply before using `Invoke-Command` or `Enter-PSSession` (`[[commands/trained_powershell-remoting]]`). | `ss -tlnp \| grep :22` |
| `powershell -NoProfile -Command "Invoke-Command -ComputerName <TARGET_IP> -ScriptBlock { hostname; whoami; ipconfig }"` | PowerShell | Executes a script block remotely on `<TARGET_IP>` over WinRM (`TCP 5985/5986`). | Apply for native agentless remote command execution across Windows hosts. | `ssh <USER>@<TARGET_IP> "hostname; id; ip -br addr"` |
