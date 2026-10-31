"""
CORA ObsidianVault Maximizer & Knowledge Organizer (`core/Reasoning/maximize_obsidian_vault.py`).

Organizes all `core/ObsidianVault/knowledge/` and `core/ObsidianVault/commands/` files into 10
Operational Domain Hubs and enriches every single note with:
1. Complete YAML frontmatter (`summary`, `when_to_apply`, `os_platform`, `domain_hub`, `primary_tactic`, inline `tags: [...]`).
2. Structured `When to Apply (LLM & 15-Engine Decision Guide)` metadata (symptoms, H-MDP states, Bayesian hypotheses, RED/BLUE/WHITE isolation).
3. Comprehensive Windows (CMD, PowerShell, WMI/CIM, Sysinternals, Netsh, Registry, ICACLS, AuditPol, Wevtutil, AD)
   and Linux (`iproute2`, `ss`, `iptables`/`nftables`, `sysctl`, `systemd`/`journalctl`, `procfs`, SUID/Capabilities, `tcpdump`/BPF, `nmap`, `curl`, `tio`)
   command tables with flag-by-flag descriptions and expected output indicators.
4. Cleans up any broken PDF sentence fragments in `commands/trained_*.md` and replaces them with real, verified commands.
5. Rebuilds `00_MEMORY_INDEX.md`, `00_TRAINED_INDEX.md`, and `Reasoning/data/vault_entities_cache.json`.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple

REASONING_DIR = Path(__file__).resolve().parent
CORE_DIR = REASONING_DIR.parent
VAULT_DIR = CORE_DIR / "ObsidianVault"

DOMAIN_HUBS: Dict[str, Dict[str, Any]] = {
    "01_windows_system_process_and_sysinternals": {
        "hub_id": "01_windows_system_process_and_sysinternals",
        "wiki_link": "knowledge/01_windows_system_process_and_sysinternals",
        "title": "Domain Hub 01: Windows Live Response, Processes, Services, Kernel & Sysinternals Suite",
        "os_platform": "windows",
        "primary_tactic": "Passive_Enum",
        "mdp_pre": "s_init_unknown",
        "mdp_post": "s_passive_topology_mapped",
        "bayesian_causes": "suspicious_process_lineage, service_misconfiguration, unsigned_dll_injection, resource_exhaustion",
        "isolation": "RED, BLUE, WHITE (100% local host telemetry compatible)",
        "summary": "Windows live incident response, process tree/PPID investigation, service binary auditing, kernel architecture, file searching (findstr/forfiles), and Sysinternals Suite (pslist, listdlls, autorunsc, handle, sigcheck, accesschk, procdump).",
        "when_to_apply": "Apply when performing initial Windows host triage (s_init_unknown), investigating running processes/PPIDs, mapping svchost.exe services, hunting unsigned/injected DLLs, searching files by timestamp/content, or executing Sysinternals live response.",
        "tags": ["windows", "sysinternals", "pslist", "listdlls", "autorunsc", "psservice", "psloggedon", "handle", "sigcheck", "accesschk", "procdump", "tasklist", "systeminfo", "sc", "wmic", "forfiles", "findstr", "passive_enum", "live_response"],
        "commands": [
            ("systeminfo && whoami /all", "Windows CMD", "Displays OS build, patch hotfixes (KBs), boot time, current user SID, group memberships, and token privileges (`SeDebugPrivilege`, `SeImpersonatePrivilege`).", "Apply first on any Windows host (`s_init_unknown`) to establish OS baseline and privilege level.", "uname -a && id && sudo -l"),
            ("tasklist /v && tasklist /svc", "Windows CMD", "Lists all running processes with user context, memory, window titles (`/v`), and maps every `svchost.exe` PID to hosted Windows Service names (`/svc`).", "Apply to identify which service inside `svchost.exe` owns a socket or high CPU thread.", "ps auxef && systemctl list-units --type=service --state=running"),
            ("wmic process get ProcessId,ParentProcessId,Name,ExecutablePath,CommandLine /format:list", "Windows CMD", "Extracts full process lineage (`PID` + `PPID`), binary disk path, and full command-line arguments for every process.", "Apply to uncover hidden/encoded PowerShell arguments and anomalous parent-child process trees (e.g., `cmd.exe` spawned by `w3wp.exe`).", "ps -eo pid,ppid,user,args --forest"),
            ("pslist -accepteula -t && psloggedon -accepteula", "Sysinternals", "Prints hierarchical parent-child process tree (`-t`) and enumerates both local interactive and SMB network logon sessions.", "Apply during live response to trace process trees and active user sessions.", "pstree -p -a && w"),
            ("listdlls -accepteula -u && sigcheck -accepteula -e -u -vr C:\\Windows\\System32", "Sysinternals", "Lists all unsigned DLLs (`listdlls -u`) loaded into running processes and scans `System32` for unsigned executables (`sigcheck -e -u`).", "Apply when hunting DLL hijacking, process hollowing, or trojanized system binaries.", "grep -E '\\.so' /proc/*/maps && debsums -c"),
            ("handle -accepteula -a -u && tcpvcon -accepteula -a -c -n", "Sysinternals", "Enumerates all open file/registry/mutant handles (`handle -a -u`) and dumps CSV socket-to-process mappings (`tcpvcon`).", "Apply to identify malware mutexes (`BaseNamedObjects`), locked files, or进程-bound network sockets.", "lsof -i -P -n && lsof"),
            ("sc query state= all && sc qc <ServiceName>", "Windows CMD", "Lists all installed services (running/stopped) and inspects `BINARY_PATH_NAME`, `START_TYPE`, and `SERVICE_START_NAME`.", "Apply to audit service binaries and check for unquoted service paths or writable service executables.", "systemctl status <service> && systemctl cat <service>"),
            ("forfiles /p C:\\ /s /m *.exe /d -7 /c \"cmd /c echo @path @fdate @ftime\"", "Windows CMD", "Recursively (`/s`) locates executables modified within the last 7 days (`/d -7`) across drive `C:\\`.", "Apply during incident triage to find recently dropped binaries or staging scripts.", "find / -xdev -mtime -7 -type f -ls 2>/dev/null"),
            ("findstr /s /i /n \"password secret connectionString\" C:\\Users\\*.txt C:\\Users\\*.ps1 C:\\inetpub\\*.config", "Windows CMD", "Recursive (`/s`), case-insensitive (`/i`), line-numbered (`/n`) string search across text, script, and web config files.", "Apply when auditing configuration files for plaintext credentials or API keys.", "grep -rnI -iE 'password|secret' /var/www /home /etc 2>/dev/null"),
            ("procdump -accepteula -ma <PID> C:\\Temp\\proc_<PID>.dmp", "Sysinternals", "Captures a complete memory dump (`-ma`) of target process `<PID>` for strings/YARA/reverse engineering.", "Apply before terminating a suspicious in-memory process so volatile unpacked strings and keys are preserved.", "gcore -o /tmp/proc_<PID> <PID>"),
        ],
    },
    "02_windows_registry_boot_and_persistence": {
        "hub_id": "02_windows_registry_boot_and_persistence",
        "wiki_link": "knowledge/02_windows_registry_boot_and_persistence",
        "title": "Domain Hub 02: Windows Registry Architecture, Boot Configuration (bcdedit), Startup & Persistence",
        "os_platform": "windows",
        "primary_tactic": "Passive_Enum",
        "mdp_pre": "s_passive_topology_mapped",
        "mdp_post": "s_active_services_enumerated",
        "bayesian_causes": "registry_autorun_persistence, winlogon_shell_hijack, boot_bcd_tampering, scheduled_task_persistence",
        "isolation": "RED, BLUE, WHITE (100% local host telemetry compatible)",
        "summary": "Windows Registry root keys (HKLM, HKCU, HKU, HKCR, HKCC), data types (REG_SZ, REG_DWORD, REG_BINARY), Run/RunOnce/Winlogon/Session Manager persistence keys, Boot Configuration Data (bcdedit), and startup forensics.",
        "when_to_apply": "Apply when auditing Windows persistence mechanisms, inspecting Registry hives (`HKLM`/`HKCU`/`HKU`), analyzing boot sequences (`SMSS` -> `CSRSS` -> `Wininit` -> `Services` -> `LSASS` -> `Winlogon`), or checking `bcdedit` DEP/signing settings.",
        "tags": ["windows", "registry", "reg", "bcdedit", "autorunsc", "schtasks", "persistence", "winlogon", "boot", "forensics", "passive_enum"],
        "commands": [
            ("reg query \"HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run\" && reg query \"HKCU\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run\"", "Windows CMD", "Queries machine-wide (`HKLM`) and current-user (`HKCU`) Registry `Run` keys executed automatically at logon.", "Apply during every Windows persistence sweep (also check `RunOnce` and `Wow6432Node\\...\\Run`).", "ls -la /etc/xdg/autostart ~/.config/autostart /etc/rc.local"),
            ("reg query \"HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Winlogon\" /v Userinit && reg query \"HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Winlogon\" /v Shell", "Windows CMD", "Inspects `Userinit` (default `userinit.exe,`) and `Shell` (default `explorer.exe`) under `Winlogon`.", "Apply to detect Winlogon helper DLL/binary hijacking that executes at interactive logon.", "cat /etc/profile /etc/bash.bashrc ~/.bashrc"),
            ("reg query \"HKLM\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\" /v BootExecute", "Windows CMD", "Reads native NT boot-time executable list (`BootExecute`, default `autocheck autochk *`) and `KnownDLLs`.", "Apply to detect early-boot persistence executed by `smss.exe` before Win32 starts.", "systemctl list-dependencies sysinit.target"),
            ("reg query \"HKLM\\SYSTEM\\CurrentControlSet\\Control\\hivelist\"", "Windows CMD", "Maps loaded Registry hive paths (`\\REGISTRY\\MACHINE\\SAM`, `SYSTEM`, `SOFTWARE`, `SECURITY`) to physical disk files.", "Apply to verify loaded registry hives and locate user `NTUSER.DAT` paths.", "findmnt && mount"),
            ("reg query \"HKU\" | findstr /i \"S-1-5-21-\" | findstr /v \"_Classes\"", "Windows CMD", "Lists the Security Identifiers (`SIDs`) of all domain/local user profiles currently loaded in `HKEY_USERS`.", "Apply to identify which users have active loaded registry hives and query `HKU\\<SID>\\Software\\Microsoft\\Windows\\CurrentVersion\\Run`.", "loginctl list-users && w"),
            ("reg query \"HKLM\\SYSTEM\\CurrentControlSet\\Enum\\USBSTOR\" /s", "Windows CMD", "Recursively dumps historical USB storage device vendor, model, revision, and serial numbers from the Registry.", "Apply during forensic investigations to identify every USB drive ever plugged into the host.", "lsusb -v && journalctl -k | grep -i usb"),
            ("autorunsc -accepteula -a * -c -h -s -v", "Sysinternals", "Comprehensive CSV dump of all Windows auto-start extension points (`Run`, Services, Drivers, Scheduled Tasks, WMI, Print Monitors) with SHA256 hashes and Authenticode status.", "Apply as the definitive persistence audit across all Registry and filesystem startup locations.", "systemctl list-unit-files --state=enabled && crontab -l"),
            ("bcdedit /enum all", "Windows CMD (Admin)", "Displays Windows Boot Manager and OS Loader entries (`nx` DEP policy, `testsigning`, `nointegritychecks`, `debug`, `safeboot`).", "Apply to verify Data Execution Prevention (`nx AlwaysOn`/`OptOut`) and check if driver signature enforcement was disabled (`testsigning Yes`).", "cat /proc/cmdline && mokutil --sb-state"),
            ("bcdedit /set {current} nx AlwaysOn", "Windows CMD (Admin)", "Enforces hardware-assisted Data Execution Prevention (`DEP`) across all 32-bit and 64-bit processes on the current boot entry.", "Apply when hardening a Windows host against stack/heap shellcode execution (`s_oob_serial_enumerated -> s_firewall_or_acl_unlocked`).", "sudo sysctl -w kernel.randomize_va_space=2"),
            ("reg save HKLM\\SAM C:\\Temp\\sam.hiv && reg save HKLM\\SYSTEM C:\\Temp\\system.hiv", "Windows CMD (Admin)", "Exports live locked Registry hives (`SAM`, `SYSTEM`, `SECURITY`) to disk files for offline forensic inspection.", "Apply during authorized forensic collection or credential auditing when raw `C:\\Windows\\System32\\config\\SAM` is locked by the kernel.", "sudo cp /etc/shadow /tmp/shadow.bak"),
        ],
    },
    "03_windows_security_acls_auditing_and_logs": {
        "hub_id": "03_windows_security_acls_auditing_and_logs",
        "wiki_link": "knowledge/03_windows_security_acls_auditing_and_logs",
        "title": "Domain Hub 03: Windows Security, SIDs, DACLs/ACLs (icacls), Audit Policy (auditpol), Event Logs (wevtutil) & Mitigations (ASLR/DEP)",
        "os_platform": "windows",
        "primary_tactic": "Defense_Evasion_Firewall",
        "mdp_pre": "s_oob_serial_enumerated",
        "mdp_post": "s_firewall_or_acl_unlocked",
        "bayesian_causes": "restrictive_dacl_or_ownership, missing_audit_policy_coverage, privilege_escalation_via_weak_acl, token_impersonation_hot_potato",
        "isolation": "RED, BLUE, WHITE (100% local host telemetry compatible)",
        "summary": "Windows Security Identifiers (Well-Known SIDs), ACE/DACL inheritance rules, icacls/cacls/takeown file permission management, auditpol subcategory configuration, wevtutil/Get-WinEvent Event ID analysis (4624, 4625, 4672, 4688, 4697, 4720, 7045, 1102, 4104), Hot Potato privilege escalation, and ASLR/DEP/SEHOP protection mechanisms.",
        "when_to_apply": "Apply when inspecting or modifying Windows file/directory/service ACLs (`icacls`/`takeown`), mapping Well-Known SIDs, configuring or auditing Windows Security audit policy (`auditpol`), querying Windows Event Logs (`wevtutil`/`Get-WinEvent`/`psloglist`), or evaluating exploit mitigations (ASLR/DEP) and local privilege escalation vectors.",
        "tags": ["windows", "icacls", "cacls", "takeown", "auditpol", "wevtutil", "psloglist", "get-winevent", "sid", "acl", "dacl", "event_id", "aslr", "dep", "privilege_escalation", "defense_evasion_firewall", "credential_access"],
        "commands": [
            ("icacls \"C:\\Program Files\\TargetApp\" && icacls \"C:\\Windows\\Temp\"", "Windows CMD", "Displays Discretionary Access Control Lists (`DACLs`), showing principal SIDs/names, access masks `(F)` Full, `(M)` Modify, `(RX)` Read/Exec, `(W)` Write, and inheritance flags `(OI)(CI)(IO)`.", "Apply when checking if service binaries, config files, or PATH directories are writable by non-admin users (`BUILTIN\\Users` or `Everyone`).", "getfacl <path> && ls -ld <path>"),
            ("icacls \"C:\\TargetDir\" /save C:\\Temp\\acl_backup.sddl /T && icacls \"C:\\TargetDir\" /grant Administrators:(OI)(CI)F /T", "Windows CMD (Admin)", "Backs up existing SDDL ACLs recursively (`/save ... /T`) and grants `Administrators` Full Control with Object and Container Inheritance `(OI)(CI)`.", "Apply whenever unlocking restrictive file/folder permissions while preserving a lossless SDDL backup (`/restore`).", "getfacl -R <dir> > backup.acl && sudo setfacl -R -m u:root:rwx <dir>"),
            ("takeown /f \"C:\\TargetDir\" /r /a /d y", "Windows CMD (Admin)", "Recursively (`/r`) transfers ownership of locked files/folders to the `Administrators` group (`/a`) without interactive prompts (`/d y`).", "Apply when `icacls` fails with `Access is denied` because ownership is held by `TrustedInstaller` or another account.", "sudo chown -R root:root <dir>"),
            ("auditpol /get /category:* && auditpol /list /subcategory:*", "Windows CMD (Admin)", "Displays active Success and Failure audit settings across all 9 top-level categories and 50+ granular subcategories.", "Apply first during log/forensic readiness checks to verify whether `Process Creation`, `Logon`, `SAM`, or `Kerberos` auditing is enabled.", "sudo auditctl -l && sudo auditctl -s"),
            ("auditpol /set /subcategory:\"Sensitive Privilege Use\" /success:enable /failure:enable && auditpol /set /subcategory:\"User Account Management\" /success:enable /failure:enable", "Windows CMD (Admin)", "Enables granular security event auditing for high-privilege token usage (`4672`/`4673`) and user account creation/modification (`4720`/`4728`/`4732`).", "Apply to ensure privilege escalation and account changes generate `Security.evtx` telemetry.", "sudo auditctl -w /etc/passwd -p wa -k user_mod"),
            ("wevtutil qe Security /q:\"*[System[(EventID=4624 or EventID=4625 or EventID=4672)]]\" /c:20 /rd:true /f:text", "Windows CMD (Admin)", "Queries the `Security` event log newest-first (`/rd:true`) for the last 20 Logon Success (`4624`), Logon Failure (`4625`), and Admin Special Logon (`4672`) events.", "Apply to trace interactive (`Type 2`), network/SMB (`Type 3`), and RDP (`Type 10`) logons or brute-force attempts.", "sudo grep -E 'Accepted|Failed|sudo' /var/log/auth.log /var/log/secure | tail -n 30"),
            ("wevtutil qe Security /q:\"*[System[(EventID=4688 or EventID=4697 or EventID=4720 or EventID=1102)]]\" /c:20 /rd:true /f:text", "Windows CMD (Admin)", "Extracts Process Creation (`4688`), Service Installation (`4697`), User Account Creation (`4720`), and Audit Log Cleared (`1102`) events.", "Apply during incident response to pinpoint persistence installation, rogue accounts, or anti-forensic log clearing.", "sudo ausearch -m EXECVE,ADD_USER,SERVICE_START -ts recent"),
            ("wevtutil qe System /q:\"*[System[(EventID=7045 or EventID=7036)]]\" /c:15 /rd:true /f:text", "Windows CMD", "Queries `System` log for new Service Control Manager service installations (`7045`) and service state changes (`7036`).", "Apply even when `Security` audit policy was disabled: `System` Event `7045` records the service binary path by default!", "journalctl -u systemd -n 30 --no-pager"),
            ("powershell -NoProfile -Command \"Get-WinEvent -FilterHashtable @{LogName='Microsoft-Windows-PowerShell/Operational'; Id=4104} -MaxEvents 10 | Format-List TimeCreated,Message\"", "PowerShell", "Reads the last 10 PowerShell ScriptBlock Logging (`Event ID 4104`) records containing full de-obfuscated PowerShell code executed on the host.", "Apply to uncover fileless PowerShell payloads, `Invoke-Expression` cradles, or Empire/PowerSploit modules.", "ausearch -m EXECVE -c bash"),
            ("powershell -NoProfile -Command \"Get-ProcessMitigation -System\"", "PowerShell", "Displays system-wide exploit mitigation policies (`DEP`, `ASLR` ForceRelocateImages/BottomUp, `CFG` Control Flow Guard, `SEHOP`).", "Apply when auditing Windows memory protection mechanisms (`[[knowledge/trained_address_space_layout_randomization]]`).", "sysctl kernel.randomize_va_space && checksec --proc-all"),
        ],
    },
    "04_windows_powershell_wmi_cim_and_active_directory": {
        "hub_id": "04_windows_powershell_wmi_cim_and_active_directory",
        "wiki_link": "knowledge/04_windows_powershell_wmi_cim_and_active_directory",
        "title": "Domain Hub 04: Windows PowerShell, WMI/CIM, WinRM Remoting, Active Directory (dsquery), Kerberos & Post-Exploitation",
        "os_platform": "windows",
        "primary_tactic": "Active_Enum",
        "mdp_pre": "s_active_services_enumerated",
        "mdp_post": "s_credentials_or_certs_acquired",
        "bayesian_causes": "ad_domain_trust_or_spn_exposure, winrm_or_wmi_lateral_movement_path, kerberos_ticket_or_delegation_weakness, unquoted_service_or_gpo_misconfig",
        "isolation": "RED, BLUE (Active Directory / WinRM network queries require allowed LAN interface; local CIM/WMI works in WHITE)",
        "summary": "PowerShell 2.0-7+ cmdlets, Get-CimInstance/Get-WmiObject/wmic queries, WinRM/PSRemoting (Invoke-Command, Enter-PSSession), Active Directory enumeration (dsquery, dsget, nltest, net, PowerView), local privilege checks (PowerUp), Kerberos SPNs/tickets (setspn, klist), and WMI permanent event subscriptions.",
        "when_to_apply": "Apply when automating Windows enumeration with PowerShell or WMI/CIM (`Get-CimInstance`/`wmic`), executing commands remotely via WinRM/WMI, enumerating Active Directory users/groups/computers/trusts/GPOs (`dsquery`/`nltest`/`net`), or auditing Kerberos tickets (`klist`) and SPNs (`setspn`).",
        "tags": ["windows", "powershell", "wmic", "get-ciminstance", "winrm", "invoke-command", "dsquery", "nltest", "kerberos", "klist", "setspn", "active_directory", "ldap", "powerview", "powerup", "powersploit", "empire", "active_enum", "credential_access"],
        "commands": [
            ("powershell -NoProfile -Command \"Get-CimInstance Win32_ComputerSystem | Select-Object Name,Domain,Manufacturer,Model,UserName,TotalPhysicalMemory\"", "PowerShell", "Queries `Win32_ComputerSystem` via modern CIM (WS-Man/DCOM) for host domain membership, logged-on console user, and hardware model.", "Apply in PowerShell 4.0+ as the fast, structured replacement for `wmic computersystem` (`[[knowledge/trained_ps_get-cim]]`).", "hostnamectl && lscpu && free -h"),
            ("powershell -NoProfile -Command \"Get-CimInstance Win32_Service | Where-Object {$_.State -eq 'Running' -and $_.PathName -notmatch 'C:\\\\Windows'} | Select-Object Name,DisplayName,StartName,PathName\"", "PowerShell", "Finds all running third-party/custom Windows services whose binary path is outside `C:\\Windows`.", "Apply to quickly isolate non-OS services and inspect their execution account (`StartName`) and binary path.", "systemctl list-units --type=service --state=running"),
            ("powershell -NoProfile -Command \"Get-CimInstance -Namespace root\\subscription -ClassName __EventFilter; Get-CimInstance -Namespace root\\subscription -ClassName CommandLineEventConsumer; Get-CimInstance -Namespace root\\subscription -ClassName __FilterToConsumerBinding\"", "PowerShell", "Audits the `root\\subscription` WMI repository for permanent WMI Event Filters, Consumers, and Bindings.", "Apply to detect fileless WMI persistence (`[[knowledge/trained_us-15-graeber-abusing-windows-management-instrumentation-wmi-to-]]`).", "crontab -l && systemctl list-timers --all"),
            ("wmic /node:\"<TARGET_IP>\" process call create \"cmd.exe /c ipconfig /all > C:\\Temp\\out.txt\"", "Windows CMD", "Executes a command remotely on `<TARGET_IP>` over DCOM/RPC (`TCP 135` + dynamic high ports) using WMI `Win32_Process.Create`.", "Apply for agentless remote execution across domain hosts when WinRM (`5985`) is closed but RPC (`135`) is open.", "ssh <USER>@<TARGET_IP> 'ip -4 -br addr'"),
            ("winrm enumerate winrm/config/listener && powershell -NoProfile -Command \"Test-WSMan -ComputerName <TARGET_IP>\"", "CMD / PS", "Enumerates local WinRM listeners (`5985` HTTP / `5986` HTTPS) and tests WS-Management reachability on `<TARGET_IP>`.", "Apply before running `Invoke-Command` or `Enter-PSSession` (`[[commands/trained_powershell-remoting]]`).", "nc -zv <TARGET_IP> 22"),
            ("powershell -NoProfile -Command \"Invoke-Command -ComputerName <TARGET_IP> -ScriptBlock { hostname; whoami /all; Get-NetIPConfiguration }\"", "PowerShell", "Executes a PowerShell script block on remote host `<TARGET_IP>` over WinRM (`TCP 5985`/`5986`) and returns serialized objects.", "Apply for multi-host administrative command execution and remote triage.", "ssh <USER>@<TARGET_IP> 'hostname; id; ip addr'"),
            ("nltest /dclist: && nltest /domain_trusts /all_trusts", "Windows CMD", "Discovers all Domain Controllers in the current domain and enumerates all forest/external/transitive domain trusts.", "Apply first during Active Directory reconnaissance (`[[commands/trained_domain_service_tools]]`).", "dig _ldap._tcp.dc._msdcs.<DOMAIN> SRV"),
            ("net user /domain && net group \"Domain Admins\" /domain && net group \"Enterprise Admins\" /domain", "Windows CMD", "Queries the Domain Controller for all domain user accounts and members of high-privilege administrative groups.", "Apply on any domain-joined workstation/server to map privileged accounts (`[[commands/trained_net_cmds_1]]`).", "ldapsearch -x -H ldap://<DC_IP> -b 'dc=domain,dc=local'"),
            ("dsquery user -limit 0 | dsget user -samid -sid -upn -pwdneverexpires -disabled && dsquery computer -limit 0", "Windows CMD (AD)", "Queries Active Directory LDAP for all user accounts (with SAMID, SID, and password expiry flags) and all domain computers (`[[commands/trained_ds_cmds]]`).", "Apply when RSAT or DC tools are present to export complete Active Directory object inventories.", "ldapsearch -LLL -H ldap://<DC_IP> '(objectClass=user)' sAMAccountName objectSid"),
            ("setspn -Q */* && klist", "Windows CMD", "Lists all Service Principal Names (`SPNs`) registered in Active Directory (`setspn -Q */*`) and inspects cached Kerberos tickets (`klist`).", "Apply to locate SQL/HTTP/Exchange service accounts (`Kerberoasting` audit) and verify active TGT/TGS encryption types (`[[knowledge/trained_kerberos_attacks_cheatsheet]]`).", "klist && kvno <SPN>"),
        ],
    },
    "05_windows_and_linux_networking_routing_and_firewalls": {
        "hub_id": "05_windows_and_linux_networking_routing_and_firewalls",
        "wiki_link": "knowledge/05_windows_and_linux_networking_routing_and_firewalls",
        "title": "Domain Hub 05: Cross-Platform L2/L3/L4 Networking, Routing, DNS, Host Firewalls (netsh / iptables / nftables) & IDS (Snort)",
        "os_platform": "cross-platform",
        "primary_tactic": "L2_L3_Pivot_Routing",
        "mdp_pre": "s_passive_topology_mapped",
        "mdp_post": "s_cross_subnet_pivot_routed",
        "bayesian_causes": "missing_static_route, pivot_ip_forward_disabled, asymmetric_missing_return_route_or_nat, host_firewall_drop, service_bound_to_loopback",
        "isolation": "RED, BLUE, WHITE (Passive local inspection works in WHITE; cross-subnet routing/probing works in RED and allowed BLUE NICs)",
        "summary": "Side-by-side Windows and Linux networking reference covering L2 ARP/neighbors (arp vs ip neigh), L3 routing & forwarding (route/netsh vs ip route/sysctl), L4 sockets (netstat/Get-NetTCPConnection vs ss/lsof), DNS resolution, host firewalls (netsh advfirewall vs iptables/nftables), NAT masquerading/portproxy, and Snort IDS.",
        "when_to_apply": "Apply whenever diagnosing network unreachability (`Network is unreachable`, `No route to host`, `Connection timed out`), mapping local/remote subnets (`Engine 2`), configuring cross-subnet static routes/IP forwarding/NAT masquerading (`Engine 6/15/19`), inspecting listening ports (`ss`/`netstat`), or unlocking `iptables`/`nftables`/`netsh advfirewall` rules.",
        "tags": ["windows", "linux", "cross-platform", "iproute2", "ipconfig", "route", "arp", "netstat", "ss", "netsh", "iptables", "nftables", "sysctl", "ip_forward", "masquerade", "snort", "firewall", "l2_l3_pivot_routing", "defense_evasion_firewall", "passive_enum"],
        "commands": [
            ("ip -4 -br addr show; ip route show; ip neigh show", "Linux Bash", "CORA canonical 3-in-1 passive L2/L3 probe: outputs IPv4 interfaces/CIDRs, kernel routing table, and L2 ARP neighbor cache (`REACHABLE`/`STALE`/`FAILED`).", "Apply first on Linux (`s_init_unknown -> s_passive_topology_mapped`) to map local subnets and gateways in `< 15 ms`.", "ipconfig /all & route print -4 & arp -a"),
            ("ipconfig /all & route print -4 & arp -a", "Windows CMD", "CORA canonical Windows 3-in-1 passive L2/L3 probe: dumps all adapter IPs/MACs/DNS, IPv4 routing table, and ARP cache.", "Apply first on Windows (`s_init_unknown -> s_passive_topology_mapped`) to map local subnets, gateways, and L2 neighbors.", "ip -4 -br addr show; ip route show; ip neigh show"),
            ("ss -tulpn && ss -tanp", "Linux Bash", "Lists all listening TCP/UDP sockets (`-tulpn`) and all active/established TCP connections (`-tanp`) with owning process PIDs.", "Apply to verify whether a target daemon is bound to `127.0.0.1` (`service_bound_to_loopback`) or `0.0.0.0`.", "netstat -abno"),
            ("netstat -ano | findstr \"LISTENING ESTABLISHED\"", "Windows CMD", "Lists all listening ports and active established TCP connections with owning `PID` on Windows (`[[commands/trained_cqc001_e010_m040_netstat]]`).", "Apply to audit open Windows ports and cross-reference PIDs with `tasklist /svc`.", "ss -tanp"),
            ("sudo ip route replace <REMOTE_SUBNET> via <GATEWAY_IP> && sudo sysctl -w net.ipv4.ip_forward=1", "Linux Bash", "Adds/updates a static L3 route to `<REMOTE_SUBNET>` via `<GATEWAY_IP>` and enables kernel IPv4 packet forwarding (`ip_forward=1`).", "Apply when Geometric Engine (`Engine 2`) reports `<TARGET_IP>` is DISJOINT from local subnets (`C2_CROSS_SUBNET_L3_PIVOT`).", "route add <REMOTE_SUBNET> mask 255.255.255.0 <GATEWAY_IP> & netsh interface ipv4 set interface <Idx> forwarding=enabled"),
            ("sudo iptables -t nat -A POSTROUTING -s <LOCAL_SUBNET> -d <REMOTE_SUBNET> -o <OUT_IFACE> -j MASQUERADE && sudo iptables -I FORWARD 1 -j ACCEPT", "Linux Bash", "Enables Source NAT (`MASQUERADE`) on the egress interface and allows transit packets in the `FORWARD` chain.", "Apply when downstream hosts in `<REMOTE_SUBNET>` lack a return route back to the operator's subnet (`asymmetric_missing_return_route_or_nat`).", "New-NetNat -Name 'PivotNAT' -InternalIPInterfaceAddressPrefix <LOCAL_SUBNET>"),
            ("sudo iptables -L -n -v --line-numbers && sudo iptables -t nat -L -n -v && sudo nft list ruleset", "Linux Bash", "Audits all `iptables` filter/NAT chains (with packet counters) and `nftables` rulesets (`[[commands/trained_iptables-snort-cmds]]`).", "Apply whenever TCP connections time out (`Exit 28`) or return `ICMP Administratively Prohibited` (`host_firewall_drop`).", "netsh advfirewall show allprofiles & netsh advfirewall firewall show rule name=all dir=in status=enabled"),
            ("netsh advfirewall show allprofiles && netsh advfirewall firewall add rule name=\"CORA_Allow_Port\" dir=in action=allow protocol=TCP localport=8443", "Windows CMD (Admin)", "Inspects Windows Defender Firewall profile states (`Domain`/`Private`/`Public`) and adds an inbound TCP allow rule (`[[commands/trained_netsh_fw_cmds]]`).", "Apply on Windows when unlocking a blocked inbound management or service port.", "sudo iptables -I INPUT 1 -p tcp --dport 8443 -j ACCEPT"),
            ("netsh interface portproxy show all && netsh interface portproxy add v4tov4 listenaddress=0.0.0.0 listenport=8443 connectaddress=127.0.0.1 connectport=8080", "Windows CMD (Admin)", "Lists and configures native Windows TCP port forwarding (`v4tov4`) via `iphlpsvc` (`[[commands/trained_netsh_commands_for_routing]]`).", "Apply on Windows to expose a loopback-bound (`127.0.0.1:8080`) service on an external interface (`0.0.0.0:8443`) or pivot across subnets.", "socat TCP-LISTEN:8443,fork,reuseaddr TCP:127.0.0.1:8080"),
            ("sudo snort -T -c /etc/snort/snort.conf && sudo snort -A console -q -c /etc/snort/snort.conf -i <IFACE>", "Linux Bash", "Validates Snort IDS configuration (`-T`) and runs real-time signature detection alerting to console (`-A console -q`).", "Apply when auditing or testing IDS signature rules (`[[knowledge/trained_cqc001_e060_m030_iptables_and_snort]]`).", "snort.exe -W && snort.exe -A console -c C:\\Snort\\etc\\snort.conf -i 1"),
        ],
    },
    "06_linux_unix_administration_processes_and_logging": {
        "hub_id": "06_linux_unix_administration_processes_and_logging",
        "wiki_link": "knowledge/06_linux_unix_administration_processes_and_logging",
        "title": "Domain Hub 06: Linux, UNIX & Solaris Administration, Kernel (/proc & sysctl), Filesystems, Boot/systemd, Processes, Permissions/SUID & Logging",
        "os_platform": "linux",
        "primary_tactic": "Passive_Enum",
        "mdp_pre": "s_init_unknown",
        "mdp_post": "s_interactive_tty_or_priv_escalated",
        "bayesian_causes": "suid_or_capability_privesc_vector, writable_systemd_or_cron_script, unlinked_proc_binary_execution, dumb_shell_missing_pty",
        "isolation": "RED, BLUE, WHITE (100% local host telemetry compatible)",
        "summary": "Linux (Debian/Ubuntu/CentOS/RHEL) and UNIX/Solaris system administration, kernel /proc & sysctl internals, ext4/xfs/procfs filesystems, boot/init/systemd lifecycle, process signals & /proc/<PID> forensics, users/groups/chmod/SUID/SGID/capabilities, rsyslog/journalctl/auditd logging, and interactive TTY shell upgrading.",
        "when_to_apply": "Apply when enumerating a Linux/UNIX/Solaris host, inspecting `/proc/<PID>` or kernel modules, auditing mounted filesystems (`findmnt`/`lsblk`), managing `systemd` services or signals, hunting SUID/SGID/Capabilities/sudo privilege escalation vectors, reviewing `/var/log`/`journalctl` logs, or upgrading a dumb shell to a full interactive TTY.",
        "tags": ["linux", "unix", "solaris", "systemctl", "journalctl", "lsof", "strace", "findmnt", "lsblk", "sysctl", "chmod", "chown", "sudo", "getcap", "suid", "find", "grep", "pty", "tty", "passive_enum", "privilege_escalation"],
        "commands": [
            ("uname -a; cat /etc/os-release; hostnamectl; uptime; id", "Linux Bash", "Collects kernel version, architecture, OS distribution, hostname, system load, and current user UID/GID/groups (`[[commands/trained_centos-debian-survey]]`).", "Apply first on any Linux/UNIX system (`s_init_unknown`) to establish OS and privilege baseline.", "systeminfo && whoami /all"),
            ("ps auxef && ps -eo pid,ppid,user,stat,lstart,args --forest", "Linux Bash", "Displays full process tree (`--forest`), UID, PID, PPID, start timestamp, and full command line (`[[commands/trained_cqc001_e050_m050_process_and_signals]]`).", "Apply to identify running daemons, abnormal child processes, or processes executing from `/tmp` or `/dev/shm`.", "wmic process get ProcessId,ParentProcessId,ExecutablePath,CommandLine"),
            ("sudo ls -la /proc/<PID>/exe /proc/<PID>/cwd /proc/<PID>/fd && tr '\\0' '\\n' < /proc/<PID>/environ", "Linux Bash", "Inspects the live kernel `/proc/<PID>` binary link (`exe`), working directory (`cwd`), open descriptors (`fd`), and environment variables (`environ`).", "Apply during Linux live forensics: recovers deleted binaries (`cp /proc/<PID>/exe /tmp/recovered`) and exposes secrets in process environments.", "handle -accepteula -a -p <PID>"),
            ("systemctl list-units --type=service --state=running && systemctl list-timers --all", "Linux Bash", "Lists all active `systemd` services and scheduled timers (`[[commands/trained_cqc001_e050_m040_boot_init_login]]`).", "Apply to audit running services and periodic scheduled tasks on modern `systemd` distributions.", "sc query state= active && schtasks /query"),
            ("df -hT && lsblk -f && findmnt", "Linux Bash", "Lists mounted filesystems with filesystem type (`ext4`, `xfs`, `tmpfs`), block device hierarchy, UUIDs, and mount flags (`noexec`, `nosuid`) (`[[knowledge/trained_cqc001_e050_m030_filesystems]]`).", "Apply to inspect storage layout and verify which writable directories (`/tmp`, `/var/tmp`, `/dev/shm`) allow binary execution.", "wmic logicaldisk get DeviceID,FileSystem,FreeSpace,Size"),
            ("sudo -l && find / -perm -4000 -type f -exec ls -la {} + 2>/dev/null && getcap -r / 2>/dev/null", "Linux Bash", "Audits allowed `sudo` commands, SUID root binaries (`-perm -4000`), and POSIX file capabilities (`getcap -r /`) (`[[commands/trained_cqc001_e060_m010_users_and_permissions]]`).", "Apply immediately during Linux privilege escalation (`s_initial_shell_or_api_access -> s_interactive_tty_or_priv_escalated`).", "whoami /priv && accesschk -accepteula -uwcqv *"),
            ("find / -writable -type f \\( -path \"/etc/*\" -o -path \"/usr/*\" -o -path \"/opt/*\" -o -path \"/var/spool/cron/*\" \\) 2>/dev/null", "Linux Bash", "Finds misconfigured world- or group-writable config files, service units, and scripts across system directories.", "Apply to detect writable `/etc/passwd`, `/etc/systemd/system/*.service`, or cron jobs executed by root.", "accesschk -accepteula -uwqv \"Users\" C:\\Windows\\*"),
            ("journalctl -xe --no-pager -n 100 && sudo grep -E \"Accepted|Failed|sudo|session opened\" /var/log/auth.log /var/log/secure 2>/dev/null | tail -n 50", "Linux Bash", "Queries `systemd-journald` and `rsyslog` auth logs (`auth.log` on Debian/Ubuntu, `secure` on RHEL/CentOS) (`[[commands/trained_logging-cmds]]`).", "Apply when auditing SSH logins, `sudo` usage, or service startup failures.", "wevtutil qe Security /c:30 /rd:true /f:text"),
            ("python3 -c 'import pty; pty.spawn(\"/bin/bash\")' || script -qc /bin/bash /dev/null", "Linux Bash", "Allocates a kernel pseudo-terminal (`PTY`) to upgrade a non-interactive netcat/reverse shell into a full interactive TTY (`[[knowledge/trained_upgrading_shells_to_fully_interactive_ttys]]`).", "Apply whenever `sudo`, `su`, `ssh`, or `vim` fails with `standard in must be a tty` or `no tty present`.", "Enter-PSSession"),
            ("uname -a; showrev -p; ifconfig -a; netstat -rn; ps -ef; svcs -a", "Solaris / UNIX", "Solaris (`SunOS`) system, patch (`showrev -p`), interface (`ifconfig -a`), routing (`netstat -rn`), and SMF service (`svcs -a`) survey (`[[commands/trained_solaris-survey]]`).", "Apply when operating on legacy Solaris / SunOS UNIX enterprise servers.", "systeminfo && ipconfig /all && sc query"),
        ],
    },
    "07_packet_capture_bpf_wireshark_and_passive_fingerprinting": {
        "hub_id": "07_packet_capture_bpf_wireshark_and_passive_fingerprinting",
        "wiki_link": "knowledge/07_packet_capture_bpf_wireshark_and_passive_fingerprinting",
        "title": "Domain Hub 07: Packet Capture (tcpdump / tshark / pktmon), BPF Syntax, Wireshark Filters, RFC792/IPv4/TCP/ARP/STP Headers & Passive Fingerprinting (p0f / DHCP)",
        "os_platform": "cross-platform",
        "primary_tactic": "Passive_Enum",
        "mdp_pre": "s_passive_topology_mapped",
        "mdp_post": "s_l2_l3_verified",
        "bayesian_causes": "silent_firewall_syn_drop, asymmetric_routing_missing_syn_ack, vlan_8021q_tag_mismatch, stp_bridge_port_blocking",
        "isolation": "RED, BLUE, WHITE (Offline .pcap analysis works in WHITE; live interface capture works in RED and allowed BLUE NICs)",
        "summary": "Berkeley Packet Filter (BPF) byte-offset syntax, tcpdump and tshark CLI packet capture, Windows pktmon/netsh trace capture, Wireshark display filters, IPv4/TCP/ARP/ICMP (RFC792) & Spanning Tree Protocol (STP) header structures, passive OS fingerprinting (p0f), and DHCP Option 55 fingerprinting.",
        "when_to_apply": "Apply when capturing live network traffic (`tcpdump`/`tshark`/`pktmon`), writing BPF byte-offset filters (`tcp[13]`, `icmp[0]`), analyzing `.pcap` files with Wireshark/tshark display filters, decoding IPv4/TCP/ICMP/ARP/STP headers, or passively fingerprinting remote OS types via `p0f` or DHCP options without transmitting active packets.",
        "tags": ["linux", "windows", "tcpdump", "tshark", "wireshark", "bpf", "p0f", "pktmon", "arp", "icmp", "tcp", "ipv4", "dhcp", "vlan", "stp", "pcap", "passive_enum"],
        "commands": [
            ("sudo tcpdump -ni <IFACE> -c 50 -nn -e 'arp or icmp'", "Linux Bash", "Captures 50 ARP or ICMP frames on `<IFACE>` without DNS resolution (`-nn`) and prints L2 Ethernet MAC addresses and VLAN tags (`-e`).", "Apply to verify whether ARP replies or ICMP Echo Replies (`type 0`) / Destination Unreachable (`type 3`) actually arrive on the wire (`[[commands/trained_bpf_syntax]]`).", "pktmon start --capture --comp nics"),
            ("sudo tcpdump -ni <IFACE> -nn 'tcp[13] & 2 != 0 and host <TARGET_IP>'", "Linux Bash", "BPF byte-offset filter inspecting byte 13 of the TCP header (`tcp[13]` flags byte): matches `SYN` (`0x02`) or `SYN-ACK` (`0x12`) packets for `<TARGET_IP>` (`[[commands/trained_jstebelton_bpf-syntax]]`).", "Apply to check if outbound TCP `SYN` probes receive `SYN-ACK` (`0x12`), `RST-ACK` (`0x14`, port closed), or silence (firewall drop).", "tshark.exe -i <IFACE> -f \"tcp[13] & 2 != 0 and host <TARGET_IP>\""),
            ("sudo tcpdump -ni <IFACE> -nn 'tcp[13] == 18'", "Linux Bash", "Captures exclusively `SYN-ACK` packets (`SYN=2` + `ACK=16` = `18` / `0x12`) to passively spot open ports responding on the wire.", "Apply during network troubleshooting or scan verification to log every open port answering with `SYN-ACK`.", "tshark.exe -i <IFACE> -f \"tcp[13] == 18\""),
            ("sudo tcpdump -ni <IFACE> -s0 -G 300 -W 1 -w /tmp/capture.pcap 'not port 22'", "Linux Bash", "Writes full-length frames (`-s0`) excluding SSH (`not port 22`) to `/tmp/capture.pcap` for up to 300 seconds (`[[commands/trained_capture_sh]]`).", "Apply to record a lossless packet capture for `tshark`, `p0f`, or `Wireshark` inspection.", "netsh trace start capture=yes IPv4.Address=<TARGET_IP> tracefile=C:\\Temp\\net.etl"),
            ("tshark -r /tmp/capture.pcap -q -z conv,tcp -z io,phs", "Linux / Windows", "Reads `/tmp/capture.pcap` (`-r`) and prints protocol hierarchy statistics (`io,phs`) and top TCP conversations (`conv,tcp`) (`[[knowledge/trained_cqc001_e010_m010_network_traffic_monitoring]]`).", "Apply first on any `.pcap` file to get an instant breakdown of protocols, endpoints, and byte volumes.", "tshark.exe -r C:\\Temp\\capture.pcap -q -z conv,tcp -z io,phs"),
            ("tshark -r /tmp/capture.pcap -Y \"http.request or tls.handshake.type == 1 or arp.opcode == 2\" -T fields -e frame.time -e eth.src -e ip.src -e ip.dst -e http.host -e tls.handshake.extensions_server_name", "Linux / Windows", "Applies Wireshark Display Filters (`-Y`) to extract timestamps, MACs, IPs, HTTP hosts, and TLS SNI server names (`[[knowledge/trained_cqc001_e010_m030_wireshark_display_filters]]`).", "Apply to extract clear-text HTTP requests, TLS Server Name Indications, and ARP replies from a capture.", "tshark.exe -r C:\\Temp\\capture.pcap -Y \"http.request or tls.handshake.type == 1\""),
            ("tshark -r /tmp/capture.pcap -Y \"bootp.option.type == 53\" -T fields -e eth.src -e ip.src -e bootp.option.hostname -e bootp.option.request_list_item -e bootp.option.vendor_class_id", "Linux / Windows", "Extracts DHCP client MAC, hostname (`Option 12`), Parameter Request List (`Option 55` fingerprint), and Vendor Class (`Option 60`) (`[[knowledge/trained_cqc001_e010_m050_dhcp_fingerprints]]`).", "Apply to passively identify exact client OS versions (Windows 10/11, Android, iOS, Linux, FortiOS) from DHCP broadcasts.", "tshark.exe -r C:\\Temp\\capture.pcap -Y \"dhcp\""),
            ("sudo p0f -i <IFACE> -o /tmp/p0f.log || p0f -r /tmp/capture.pcap", "Linux Bash", "Passively identifies remote OS, kernel version, link MTU, and network distance (TTL) from TCP handshake parameters (`[[knowledge/trained_cqc001_e010_m040_p0f]]`).", "Apply in passive/stealth regimes to fingerprint remote OS stacks without sending a single active packet.", "p0f.exe -r C:\\Temp\\capture.pcap"),
            ("sudo tcpdump -ni <IFACE> -nn -e 'ether proto 0x88cc or (ether[14:2] == 0xaaaa and ether[20:2] == 0x2000) or stp'", "Linux Bash", "Captures L2 discovery frames: LLDP (`0x88cc`), Cisco Discovery Protocol (`CDP`), and Spanning Tree Protocol (`STP` BPDUs) (`[[knowledge/trained_cqc001_e010_m060_spanning_tree_protocol]]`).", "Apply on a newly connected switch port to passively learn switch hostname, management IP, native VLAN ID, and STP root bridge.", "pktmon start --capture --pkt-size 0"),
            ("pktmon start --capture --comp nics --pkt-size 0 && timeout /t 15 && pktmon stop && pktmon etl2pcap PktMon.etl -o C:\\Temp\\win_capture.pcapng", "Windows CMD (Admin)", "Built-in Windows 10/11/Server 2019+ packet sniffer (`pktmon`): captures raw frames across NICs and converts `.etl` directly to `.pcapng` for Wireshark/tshark!", "Apply on Windows hosts when Wireshark/Npcap is not installed and you need a native `.pcapng` packet capture.", "sudo tcpdump -ni <IFACE> -s0 -c 100 -w /tmp/capture.pcap"),
        ],
    },
    "08_web_api_sql_injection_and_active_reconnaissance": {
        "hub_id": "08_web_api_sql_injection_and_active_reconnaissance",
        "wiki_link": "knowledge/08_web_api_sql_injection_and_active_reconnaissance",
        "title": "Domain Hub 08: Active Reconnaissance (nmap), Web/API/mTLS Probing (curl / openssl), SQL Injection Cheat Sheets & Operator Playbooks",
        "os_platform": "cross-platform",
        "primary_tactic": "Active_Enum",
        "mdp_pre": "s_l2_l3_verified",
        "mdp_post": "s_initial_shell_or_api_access",
        "bayesian_causes": "service_on_nonstandard_port_or_tls, missing_auth_or_mtls_cert, reverse_proxy_ip_acl_block, sql_injection_or_input_validation_flaw",
        "isolation": "RED, BLUE (Allowed LAN/USB interfaces; blocked in WHITE air-gap mode except against local files/loopback)",
        "summary": "Active network & port reconnaissance (nmap, Test-NetConnection), HTTP/HTTPS/REST/GraphQL/mTLS probing (curl, openssl s_client, Invoke-WebRequest), appliance firmware build-date & TLS serial extraction, SQL Injection syntax (MySQL, MSSQL, Oracle, PostgreSQL, Informix), and SSH/socat/chisel pivoting.",
        "when_to_apply": "Apply when scanning a reachable target IP/subnet (`nmap`), probing web servers or appliance management ports (`curl`/`openssl s_client`), extracting TLS certificate hardware serials and HTTP `Last-Modified` firmware dates, testing SQL injection vectors (`UNION`, error-based, time-based blind), or establishing SSH/socat port forwards.",
        "tags": ["linux", "windows", "cross-platform", "nmap", "curl", "openssl", "http", "https", "api", "tls", "mtls", "sqli", "informix", "mysql", "mssql", "oracle", "postgres", "ssh", "socat", "active_enum", "web_api_exploitation"],
        "commands": [
            ("nmap -sV -sC -Pn -T4 -p 21,22,23,53,80,111,135,139,443,445,1433,1521,3306,3389,5432,5985,8000,8080,8443,10443 <TARGET_IP>", "Linux / Windows", "Probes key enterprise, database, and appliance management ports skipping ping (`-Pn`), running service version detection (`-sV`) and default scripts (`-sC`).", "Apply once L2/L3 reachability to `<TARGET_IP>` is verified (`s_l2_l3_verified -> s_active_services_enumerated`).", "powershell -NoProfile -Command \"80,443,445,3389,5985,8080,8443 | ForEach-Object { Test-NetConnection <TARGET_IP> -Port $_ }\""),
            ("curl -sS -k -L -i --connect-timeout 5 --max-time 15 \"https://<TARGET_IP>/\"", "Linux / Windows", "Fetches HTTP response headers (`-i`) and HTML body following redirects (`-L`) and accepting self-signed TLS certs (`-k`) (`[[commands/curl_playbook]]`).", "Apply to inspect HTTP headers (`Server`, `Last-Modified`, `ETag`, `Set-Cookie`) and login page markers.", "curl.exe -sS -k -L -i --max-time 15 \"https://<TARGET_IP>/\""),
            ("echo | openssl s_client -connect <TARGET_IP>:443 -servername <TARGET_IP> 2>/dev/null | openssl x509 -noout -subject -issuer -dates -serial -ext subjectAltName", "Linux / Windows", "Extracts X.509 TLS certificate `Subject` (`CN`), `Issuer`, validity window, serial number, and `SAN` DNS names.", "Apply on HTTPS endpoints (443/8443/10443): appliances like Fortinet FortiGate expose their exact hardware model & serial (`CN = FG...`) in the TLS certificate!", "echo \"\" | openssl.exe s_client -connect <TARGET_IP>:443 2>NUL | openssl.exe x509 -noout -subject -issuer -dates"),
            ("curl -sS -k -L -I --max-time 15 \"https://<TARGET_IP>/login\"", "Linux / Windows", "Sends an HTTP `HEAD` request to retrieve static asset/login headers (`Last-Modified`, `ETag`, `Content-Length`).", "Apply to determine exact appliance firmware build dates from static asset `Last-Modified` timestamps and map applicable CVEs.", "curl.exe -sS -k -L -I --max-time 15 \"https://<TARGET_IP>/login\""),
            ("curl -sS -k -L --max-time 15 --cert client.crt --key client.key \"https://<TARGET_IP>:8443/api/v1/status\"", "Linux / Windows", "Presents a Mutual TLS (`mTLS`) client certificate (`--cert`) and private key (`--key`) during the TLS handshake.", "Apply when an API endpoint returns `SSL alert bad certificate` or `400 No required SSL certificate was sent` (`CBR-004`).", "curl.exe -sS -k -L --max-time 15 --cert client.crt --key client.key \"https://<TARGET_IP>:8443/api/v1/status\""),
            ("curl -sS -k -L -i --max-time 15 -H \"X-Forwarded-For: 127.0.0.1\" -H \"X-Real-IP: 127.0.0.1\" \"https://<TARGET_IP>/admin\"", "Linux / Windows", "Injects reverse-proxy client IP headers (`X-Forwarded-For`, `X-Real-IP`) to test IP-based access control bypasses.", "Apply when an endpoint behind Nginx/Apache/HAProxy returns `403 Forbidden` to external IPs (`reverse_proxy_ip_acl_block`).", "curl.exe -sS -k -L -i --max-time 15 -H \"X-Forwarded-For: 127.0.0.1\" \"https://<TARGET_IP>/admin\""),
            ("curl -sS -k -L --max-time 15 \"http://<TARGET_IP>/item.php?id=-1%20UNION%20SELECT%201,version(),user(),database()--%20-\"", "Linux / Windows", "Tests `UNION SELECT` SQL injection to extract DBMS version (`@@version` / `version()`), current DB user, and schema name (`[[knowledge/trained_sql_injection_cheat_sheet_by_netsparker]]`).", "Apply during authorized web application security testing when an input parameter interacts with a SQL query.", "curl.exe -sS -k -L --max-time 15 \"http://<TARGET_IP>/item.php?id=-1%20UNION%20SELECT%201,@@version,user(),database()--%20-\""),
            ("curl -sS -k -L --max-time 15 \"http://<TARGET_IP>/ item?id=1%20UNION%20SELECT%20FIRST%201%20tabname%20FROM%20systables--\"", "Linux / Windows", "IBM Informix SQL injection enumeration querying `systables` and `syscolumns` (`[[knowledge/trained_informix-sql-injection-cheat-sheet]]`).", "Apply when target database errors or banners indicate IBM Informix Dynamic Server.", "curl.exe -sS -k -L --max-time 15 \"http://<TARGET_IP>/item?id=1%20UNION%20SELECT%20DBINFO('version','full')%20FROM%20systables%20WHERE%20tabid=1--\""),
            ("ssh -o StrictHostKeyChecking=no -N -L 127.0.0.1:8443:127.0.0.1:8080 <USER>@<TARGET_IP>", "Linux / Windows", "Establishes a local SSH port forward (`-L`) mapping local `127.0.0.1:8443` to `<TARGET_IP>`'s internal loopback `127.0.0.1:8080` (`[[knowledge/trained_penetration_testing_tools_cheat_sheet]]`).", "Apply when `ss -tulpn` / `netstat -ano` shows an internal service bound exclusively to `127.0.0.1:8080` on `<TARGET_IP>`.", "ssh.exe -N -L 127.0.0.1:8443:127.0.0.1:8080 <USER>@<TARGET_IP>"),
            ("socat TCP-LISTEN:8443,fork,reuseaddr TCP:<SECONDARY_IP>:443", "Linux Bash", "Creates a bidirectional userland TCP relay forwarding connections on port `8443` to downstream `<SECONDARY_IP>:443`.", "Apply on a pivot host when kernel `ip_forward` or `iptables` NAT cannot be modified (e.g., inside an unprivileged container).", "netsh interface portproxy add v4tov4 listenport=8443 connectaddress=<SECONDARY_IP> connectport=443"),
        ],
    },
    "09_hardware_uart_serial_oob_and_telecom_wan": {
        "hub_id": "09_hardware_uart_serial_oob_and_telecom_wan",
        "wiki_link": "knowledge/09_hardware_uart_serial_oob_and_telecom_wan",
        "title": "Domain Hub 09: Hardware UART Serial OOB (tio /dev/ttyUSB0 & COM1), Metro Ethernet, MPLS/GMPLS, OTN, PON/GPON, SD-WAN, Wi-Fi & 2G/3G/4G/5G/SDR Cellular",
        "os_platform": "cross-platform",
        "primary_tactic": "OOB_Serial_Access",
        "mdp_pre": "s_l2_l3_verified",
        "mdp_post": "s_oob_serial_enumerated",
        "bayesian_causes": "service_bound_to_loopback, host_firewall_drop, wan_mpls_or_vlan_encapsulation_mismatch, uart_fifo_overrun_without_pacing",
        "isolation": "RED, BLUE (Local USB UART `/dev/ttyUSB*` and `COM*` ports are permitted in RED and BLUE LAN+USB modes)",
        "summary": "Non-interactive tio 3.9 Lua --script UART serial console automation (/dev/ttyUSB0, -o 15 -O 120 pacing), Windows COM port OOB access, Carrier Metro Ethernet (MEF E-Line/E-LAN/E-Tree, 802.1ad Q-in-Q), MPLS/GMPLS label switching, Optical Transport Network (OTN/DWDM), PON/GPON fiber, SD-WAN overlays, 802.11 Wi-Fi, and 2G/3G/4G/5G/LTE/GSM/UMTS RAN & SDR analysis.",
        "when_to_apply": "Apply whenever network connections to an appliance fail (`Exit 7` Connection Refused or `Exit 28` Timeout) and a hardware serial console (`/dev/ttyUSB0` or `COM1`) is available (`C1_OOB_SERIAL_LOOPBACK_APPLIANCE`), or when analyzing Carrier Metro Ethernet, MPLS/GMPLS labels, OTN/GPON optical links, SD-WAN tunnels, Wi-Fi 802.11, or 2G/3G/4G/5G cellular RAN protocols.",
        "tags": ["linux", "windows", "tio", "serial", "ttyusb0", "ttyusb1", "com1", "uart", "oob", "oob_serial_access", "mpls", "gmpls", "metro_ethernet", "vlan", "otn", "gpon", "sd-wan", "wifi", "lte", "5g", "gsm", "umts", "sdr"],
        "commands": [
            ("tio -b 115200 -o 15 -O 120 --mute --script-run once --script 'write(\"\\r\"); msleep(400); while read(4096, 600) > 0 do end; exit(0)' /dev/ttyUSB0", "Linux Bash (`tio 3.9`)", "Wakes the hardware UART console on `/dev/ttyUSB0` with 15ms char / 120ms line anti-drop pacing (`-o 15 -O 120`), reads the prompt (`login:` / `Password:` / `#`), and exits cleanly (`[[commands/tio_serial_playbook]]`).", "Apply first when pivoting to OOB serial (`s_l2_l3_verified -> s_oob_serial_enumerated`) after TCP/HTTP probes fail (`Exit 7`/`28`).", "reg query HKLM\\HARDWARE\\DEVICEMAP\\SERIALCOMM"),
            ("tio -b 115200 -o 15 -O 120 --mute --script-run once --script 'write(\"\\r\"); msleep(300); write(\"ip -4 -br addr\\r\"); while read(4096, 600) > 0 do end; exit(0)' /dev/ttyUSB0", "Linux Bash (`tio 3.9`)", "Executes a single paced command (`ip -4 -br addr`) over an authenticated `/dev/ttyUSB0` serial console without overflowing the 16-64 byte UART FIFO buffer.", "Apply to inspect internal appliance interfaces, loopback bindings (`ss -tulpn`), and firewall rules (`iptables -L -n`) over OOB serial.", "plink.exe -serial COM1 -sercfg 115200,8,n,1,N"),
            ("ls -la /dev/ttyUSB* /dev/ttyACM* /dev/serial/by-id/* 2>/dev/null && dmesg | grep -iE 'ttyUSB|ttyACM|ftdi|cp210|pl2303|ch341' | tail -n 20", "Linux Bash", "Enumerates all attached USB-to-UART serial adapters and inspects kernel driver binding logs.", "Apply to discover available hardware serial ports and verify `/dev/ttyUSB*` group permissions (`dialout`).", "reg query HKLM\\HARDWARE\\DEVICEMAP\\SERIALCOMM && mode"),
            ("ip -d link show && ip -M route show", "Linux Bash", "Displays detailed L2 encapsulation (`802.1Q` VLAN, `802.1ad` Q-in-Q Metro Ethernet S-TAG/C-TAG, VXLAN, GRE) and MPLS label forwarding entries (`ip -M route`) (`[[knowledge/trained_metro_ethernet_training_day_2_mpls]]`).", "Apply when troubleshooting Metro Ethernet VLAN trunking or MPLS label-switched paths (`LSPs`).", "Get-NetAdapterAdvancedProperty"),
            ("sudo tcpdump -ni <IFACE> -nn -e 'vlan or mpls'", "Linux Bash", "Captures Ethernet frames carrying `802.1Q`/`802.1ad` VLAN tags (`0x8100`/`0x88a8`) or MPLS shim labels (`0x8847`/`0x8848`) (`[[knowledge/trained_intro_to_gmpls]]`).", "Apply to discover hidden VLAN IDs or MPLS label stacks on trunk interfaces.", "pktmon start --capture --comp nics"),
            ("iw dev && sudo iw dev <WLAN_IFACE> scan | grep -E 'SSID:|freq:|signal:|RSN:'", "Linux Bash", "Lists 802.11 wireless interfaces (`iw dev`) and scans nearby Access Points for SSID, channel frequency, RSSI signal strength, and WPA2/WPA3 RSN ciphers (`[[knowledge/trained_wifi_handbook_1]]`).", "Apply during wireless reconnaissance and RF channel auditing.", "netsh wlan show interfaces && netsh wlan show networks mode=bssid"),
            ("nmcli device wifi list && nmcli connection show", "Linux Bash", "Displays NetworkManager Wi-Fi BSSIDs, channels, bitrates, security bars, and configured VPN/SD-WAN profiles.", "Apply on Linux laptops/appliances managed by NetworkManager.", "netsh wlan show profiles"),
            ("ip xfrm state && ip xfrm policy && sudo wg show", "Linux Bash", "Inspects kernel IPsec SA/SP security associations (`ip xfrm`) and WireGuard SD-WAN tunnel handshakes (`wg show`) (`[[knowledge/trained_software_defined_wide_area_network_sd-wan]]`).", "Apply when troubleshooting SD-WAN or IPsec site-to-site tunnel encapsulation and MTU overhead (`Engine 2`).", "Get-VpnConnection && netsh advfirewall consec show rule name=all"),
            ("rtl_test -t || uhd_find_devices || hackrf_info", "Linux Bash (SDR)", "Detects attached Software Defined Radio (`SDR`) hardware (`RTL-SDR`, `USRP`, `HackRF`) for cellular (`GSM`/`LTE`/`5G`) spectrum analysis (`[[knowledge/trained_mobilehacking_with_sdr-4gand5g-final]]`).", "Apply when auditing 2G/3G/4G/5G cellular basebands (`ARFCN`/`EARFCN`, `IMSI`/`TMSI`, `eNodeB`/`gNodeB` SIB broadcasts).", "usbipd list"),
            ("tshark -r /tmp/cellular.pcap -Y \"gsm_a or lte_rrc or nas-eps or ngap or s1ap\"", "Linux / Windows", "Filters telecom packet captures for 2G GSM-A, 4G LTE RRC / NAS-EPS / S1AP, and 5G NGAP signaling messages (`[[knowledge/trained_lteptclovwwp]]`).", "Apply when analyzing cellular RAN/Core signaling pcaps (`GTP-U`, `S1AP`, `NGAP`, `Diameter`).", "tshark.exe -r C:\\Temp\\cellular.pcap -Y \"s1ap or ngap or gtp\""),
        ],
    },
    "10_digital_forensics_pe_reversing_and_threat_intel": {
        "hub_id": "10_digital_forensics_pe_reversing_and_threat_intel",
        "wiki_link": "knowledge/10_digital_forensics_pe_reversing_and_threat_intel",
        "title": "Domain Hub 10: Digital Forensics (Autopsy / EnCase), NTFS Internals (MFT / ADS / Slack Space / Oplocks), PE Reverse Engineering & Threat Intel (APT28)",
        "os_platform": "cross-platform",
        "primary_tactic": "Passive_Enum",
        "mdp_pre": "s_init_unknown",
        "mdp_post": "s_passive_topology_mapped",
        "bayesian_causes": "ntfs_ads_or_slack_space_artifact, packed_or_hollowed_pe_binary, apt28_credential_or_persistence_ttp, deleted_mft_file_recovery",
        "isolation": "RED, BLUE, WHITE (100% compatible with WHITE Analyst Read-Only mode for offline forensic & binary analysis)",
        "summary": "Digital forensics workflows (Autopsy, EnCase, SleuthKit), NTFS Master File Table ($MFT), Alternate Data Streams (ADS), file/RAM slack space, Opportunistic Locks (Oplocks), Portable Executable (PE) MZ/COFF header reverse engineering, and APT28 (Fancy Bear) threat intelligence TTPs.",
        "when_to_apply": "Apply when performing disk/image forensics (Autopsy, EnCase, SleuthKit), analyzing NTFS `$MFT` records, Alternate Data Streams (`dir /r`), or slack space, reverse-engineering Windows PE (`.exe`/`.dll`/`.sys`) or Linux ELF binaries, or hunting APT28 / Fancy Bear IOCs and TTPs.",
        "tags": ["windows", "linux", "forensics", "autopsy", "encase", "ntfs", "mft", "oplocks", "pe_header", "apt28", "strings", "sigcheck", "sha256sum", "passive_enum"],
        "commands": [
            ("powershell -NoProfile -Command \"Get-FileHash -Algorithm SHA256 C:\\Suspicious\\*.exe,C:\\Suspicious\\*.dll\" && sigcheck -accepteula -h -vr C:\\Suspicious", "Windows PS / Sysinternals", "Computes cryptographic SHA256 hashes and verifies Authenticode digital signatures for suspect binaries (`[[knowledge/trained_cyber_forensics_intro_guide_updated_table]]`).", "Apply first during malware triage and forensic chain-of-custody verification.", "sha256sum /tmp/suspicious/* && file /tmp/suspicious/*"),
            ("dir /a /r C:\\Users\\* && powershell -NoProfile -Command \"Get-Item C:\\Users\\Public\\* -Stream * | Where-Object Stream -ne ':$DATA'\"", "Windows CMD / PS", "Detects NTFS Alternate Data Streams (`ADS`) attached to files or directories (`[[knowledge/trained_cqc001_e020_m020_ntfs_cheat_sheets]]`).", "Apply when hunting hidden payloads or reading `Zone.Identifier` download origin URLs.", "getfattr -R -d -m - /home"),
            ("fsutil fsinfo ntfsinfo C: && fsutil behavior query DisableLastAccess", "Windows CMD (Admin)", "Displays NTFS volume geometry (`Bytes Per Sector`, `Bytes Per Cluster`, `$MFT` start cluster and zone) and LastAccess timestamp policy.", "Apply when analyzing NTFS cluster allocation, `$MFT` layout, and slack space (`[[knowledge/trained_bcf_slack_space_and_deleted_files]]`).", "sudo tune2fs -l /dev/sda1"),
            ("mmls disk.dd && fls -r -d -p disk.dd <PART_OFFSET> && icat disk.dd <INODE> > recovered_file.bin", "Linux / SleuthKit", "Lists partition table offsets (`mmls`), enumerates deleted files in the NTFS `$MFT` / ext4 journal (`fls -r -d -p`), and extracts deleted file content by inode/MFT entry (`icat`).", "Apply during Autopsy/SleuthKit disk image forensics (`[[knowledge/trained_bcf_autopsy_navigation_and_analysis]]`).", "autopsy"),
            ("file <BINARY> && objdump -x -p <BINARY> && readelf -h -S -l -d <BINARY>", "Linux Bash", "Inspects PE (`MZ`/`PE\\0\\0`) or ELF headers, sections (`.text`, `.rdata`, `.data`, `.rsrc`, `UPX0`), import tables (`IAT`), and RWE segment flags (`[[knowledge/trained_cbm_1_2_2006_goppit_pe_format_reverse_engineer_view]]`).", "Apply during static binary reverse engineering to detect packed sections (high entropy / `W+X` permissions) and imported APIs (`VirtualAllocEx`, `WriteProcessMemory`, `CreateRemoteThread`).", "dumpbin /headers /imports <BINARY>.exe"),
            ("strings -a -n 6 <BINARY> | grep -iE 'http|https|cmd\\.exe|powershell|HKEY_|\\\\pipe\\\\|Mozilla|[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}'", "Linux / Windows", "Extracts ASCII/UTF-16 (`strings -el`) strings of length >= 6 and filters for URLs, IPs, Registry keys, named pipes, and User-Agent beacons.", "Apply to quickly extract C2 indicators, mutex names, and embedded scripts from a binary (`[[knowledge/trained_apt28-center-of-storm-2017_mandiant]]`).", "strings.exe -accepteula -n 6 <BINARY>.exe | findstr /i \"http HKEY cmd powershell\""),
        ],
    },
}


def classify_note_to_hub(stem: str, text: str) -> str:
    """Deterministically assign every `trained_*` note to its primary Operational Domain Hub (`01`..`10`)."""
    s = stem.lower()

    # Hub 10: Forensics, Autopsy, EnCase, NTFS MFT/Slack/Oplocks, PE format, APT28
    if any(
        k in s
        for k in (
            "autopsy",
            "encase",
            "slack_space",
            "ntfs_cheat",
            "oplocks",
            "pe_format",
            "goppit",
            "apt28",
            "fancybear",
            "cyber_forensics",
        )
    ):
        return "10_digital_forensics_pe_reversing_and_threat_intel"

    # Hub 09: Telecom, Cellular 2G/3G/4G/5G/LTE/GSM/UMTS, SDR, Metro Ethernet, MPLS/GMPLS, OTN, PON/GPON, SD-WAN, Wi-Fi, Acoustics, Serial
    if any(
        k in s
        for k in (
            "cellular",
            "lte",
            "gsm",
            "umts",
            "sdr",
            "2g",
            "3g",
            "5g",
            "metro_ethernet",
            "metro_case",
            "mpls",
            "gmpls",
            "otn",
            "optical",
            "pon-gpon",
            "sd-wan",
            "wifi",
            "spectrum",
            "camppp",
            "poladtev",
            "tdoct1933b",
            "mod_14",
            "acoustics",
            "tio_serial",
        )
    ):
        return "09_hardware_uart_serial_oob_and_telecom_wan"

    # Hub 07: Packet Capture, BPF, Wireshark, p0f, TCP/IP/ARP/RFC792/DHCP/STP headers, Octal/Hex conversions
    if any(
        k in s
        for k in (
            "bpf",
            "packet_filtering",
            "capture_sh",
            "wireshark",
            "p0f",
            "tcp_header",
            "ip_header",
            "arp_packet",
            "dhcp_fingerprints",
            "rfc792",
            "spanning_tree",
            "network_traffic_monitoring",
            "traffic_analysis_and_passive_os",
            "network_helper_protocols",
            "network_diagram_legend",
            "conversion_worksheet",
            "octalandhexadecimal",
            "e010_m030_transcript",
        )
    ):
        return "07_packet_capture_bpf_wireshark_and_passive_fingerprinting"

    # Hub 08: Web/API, SQL Injection, Active Recon, Operator Handbooks, CNE basics, Beacon, Hadoop
    if any(
        k in s
        for k in (
            "sql_injection",
            "sql-injection",
            "informix",
            "curl_playbook",
            "operator-handbook",
            "penetration_testing_tools",
            "network_enumeration_tools",
            "e040_m020_transcript",
            "bcf_cne_basics",
            "beacon",
            "hadoop",
            "trained_notes",
            "trained_readme",
        )
    ):
        return "08_web_api_sql_injection_and_active_reconnaissance"

    # Hub 06: Linux / UNIX / Solaris Administration, Kernel, Filesystems, Boot/Init, Processes/Signals, Users/Permissions, UNIX Logging, TTY Upgrade
    if any(
        k in s
        for k in (
            "centos",
            "debian",
            "linux",
            "unix",
            "solaris",
            "shells_and_scripting",
            "upgrading_shells",
            "logging-cmds",
            "e050_m010",
            "e050_m020",
            "e050_m030",
            "e050_m040",
            "e050_m050",
            "e060_m010",
            "e060_m020",
        )
    ):
        return "06_linux_unix_administration_processes_and_logging"

    # Hub 05: Windows & Linux Networking, Netstat, Name Resolution, Netsh (DHCP/Routing/Firewall), iptables & Snort
    if any(
        k in s
        for k in (
            "netstat",
            "networking_and_name_resolution",
            "network_and_name_resolution",
            "e020_m060",
            "e050_m060",
            "e030_m040",
            "windows_firewall",
            "iptables",
            "snort",
            "e060_m030",
            "netsh",
            "using_netsh",
            "suspicious-network-connections",
        )
    ):
        return "05_windows_and_linux_networking_routing_and_firewalls"

    # Hub 04: PowerShell, WMI, CIM, WinRM Remoting, Active Directory (ds_cmds, domain_service_tools), Kerberos, PowerView/PowerUp/PowerSploit/Empire/MoveLatr/Credential Dumping
    if any(
        k in s
        for k in (
            "powershell",
            "wmi",
            "get-cim",
            "win32_computersystem",
            "e040_m005",
            "powerpwn",
            "powersploit",
            "powerup",
            "powerview",
            "empire",
            "movelatr",
            "credential_dumping",
            "kerberos",
            "domain_service_tools",
            "ds_cmds",
        )
    ) and "logging_cheat_sheet" not in s:
        return "04_windows_powershell_wmi_cim_and_active_directory"

    # Hub 03: Windows Security, SIDs, ACLs (cacls/icacls), Auditing (auditpol), Event IDs, Protection Mechanisms (ASLR/DEP), Hot Potato, PowerShell Logging
    if any(
        k in s
        for k in (
            "auditpol",
            "auditing",
            "event_ids",
            "cacls",
            "icacls",
            "permissions_and_acl",
            "ace_flags",
            "well_known_sids",
            "usersandpermissions",
            "protection_mechanisms",
            "address_space_layout",
            "hot_potato",
            "powershell_logging_cheat_sheet",
            "e030_m010",
            "e030_m020",
            "e030_m030",
            "e030_m050",
            "e030_m060",
        )
    ):
        return "03_windows_security_acls_auditing_and_logs"

    # Hub 02: Windows Registry, Boot (bcdedit), Startup Locations, Windows Forensics (E040_M010), Change System Files
    if any(
        k in s
        for k in (
            "registry",
            "root_keys",
            "bcdedit",
            "boot_and_logon",
            "startup_process",
            "startup_locations",
            "e040_m010",
            "change_system_files",
        )
    ):
        return "02_windows_registry_boot_and_persistence"

    # Hub 01: Windows System, Processes, Services, Sysinternals, Live Response, Survey Commands, find/findstr/forfiles/type/tasklist/systeminfo
    return "01_windows_system_process_and_sysinternals"


def _clean_human_topic(stem: str, text: str) -> str:
    m = re.search(r"(?m)^source_file:\s*(.+)$", text)
    if m:
        src = m.group(1).strip().strip('"').strip("'")
        src_clean = re.sub(r"\.(?:pdf|docx|txt|md|pptx|xlsx)$", "", src, flags=re.I)
        src_clean = src_clean.replace("_", " ").strip()
        return src_clean
    return stem.replace("trained_", "").replace("_", " ").strip()


def _is_broken_prose_command(cmd_line: str) -> bool:
    """Detect non-command PDF prose fragments that were previously captured into `commands/trained_*.md`."""
    c = cmd_line.strip()
    if not c:
        return True
    bad_exact_or_sub = (
        "Service Access Point) fields of the LLC header",
        "IPTABLES AND SNORT",
        "Snort rules tutorial:",
        "Snort Users Manual:",
        "Hostname of the local system",
        "http://www.",
        "https://www.",
    )
    if any(b.lower() in c.lower() for b in bad_exact_or_sub):
        return True
    # Prose heading in ALL CAPS with spaces and no flags/paths
    if re.match(r"^[A-Z ]{10,}$", c):
        return True
    # Ends with a colon and has no flags or operators
    if c.endswith(":") and "-" not in c and "/" not in c and "\\" not in c:
        return True
    return False


def build_command_examples_markdown_section(hub_info: Dict[str, Any], topic_label: str) -> str:
    """Render the comprehensive Windows & Linux command reference table for a note based on its Domain Hub & topic."""
    lines = [
        "<!-- CORA-MAXIMIZED-COMMANDS-START -->",
        f"## Maximized Windows & Linux Command Examples for `{topic_label}`",
        "",
        f"> **Domain Hub:** [[{hub_info['wiki_link']}|{hub_info['title']}]]  ",
        f"> **Master Playbooks:** [[commands/windows_master_command_playbook]] | [[commands/linux_master_command_playbook]] | [[commands/curl_playbook]] | [[commands/tio_serial_playbook]]  ",
        f"> **When to Apply:** {hub_info['when_to_apply']}  ",
        f"> **15-Engine H-MDP State Transition:** `{hub_info['mdp_pre']}` $\\xrightarrow{{\\text{{{hub_info['primary_tactic']}}}}}$ `{hub_info['mdp_post']}` | **Bayesian Root-Cause Triggers:** `{hub_info['bayesian_causes']}` | **Isolation:** `{hub_info['isolation']}`",
        "",
        "| Primary Command (`Windows` / `Linux`) | OS / Shell | What It Does & Key Flags | When to Apply & Expected Output | Cross-Platform Equivalent |",
        "| :--- | :--- | :--- | :--- | :--- |",
    ]
    for cmd_str, shell_str, desc_str, apply_str, equiv_str in hub_info["commands"]:
        cmd_esc = cmd_str.replace("|", "\\|")
        equiv_esc = equiv_str.replace("|", "\\|")
        lines.append(f"| `{cmd_esc}` | **{shell_str}** | {desc_str} | {apply_str} | `{equiv_esc}` |")

    lines.extend(
        [
            "",
            "### Copy-Pasteable Execution Block (Windows & Linux)",
            "```bash",
        ]
    )
    for cmd_str, shell_str, desc_str, _, _ in hub_info["commands"][:6]:
        lines.append(f"# [{shell_str}] {desc_str}")
        lines.append(cmd_str)
    lines.extend(
        [
            "```",
            "<!-- CORA-MAXIMIZED-COMMANDS-END -->",
        ]
    )
    return "\n".join(lines)


def enrich_vault_note(md_path: Path, is_command_note: bool, hub_key: str) -> Dict[str, Any]:
    """Enrich a single `knowledge/trained_*.md` or `commands/trained_*.md` note with full frontmatter and command tables."""
    hub_info = DOMAIN_HUBS[hub_key]
    raw_text = md_path.read_text(encoding="utf-8", errors="replace")

    # Strip any previously injected CORA-MAXIMIZED-COMMANDS block so re-runs are 100% idempotent
    raw_text = re.sub(
        r"\n*<!-- CORA-MAXIMIZED-COMMANDS-START -->.*?<!-- CORA-MAXIMIZED-COMMANDS-END -->\s*",
        "\n",
        raw_text,
        flags=re.S,
    )

    stem = md_path.stem
    topic_label = _clean_human_topic(stem, raw_text)
    paired_cmd_exists = (VAULT_DIR / "commands" / f"{stem}.md").is_file()
    paired_know_exists = (VAULT_DIR / "knowledge" / f"{stem}.md").is_file()

    # Extract existing tags from frontmatter
    existing_tags: List[str] = []
    fm_block_m = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n(.*)$", raw_text, flags=re.S)
    body_text = fm_block_m.group(2) if fm_block_m else raw_text
    if fm_block_m:
        fm_content = fm_block_m.group(1)
        for t in re.findall(r"(?m)^[ \t]*-[ \t]*([a-zA-Z0-9_\-]+)", fm_content):
            if t.lower() not in existing_tags:
                existing_tags.append(t.lower())
        inline_m = re.search(r"(?m)^tags:\s*\[([^\]]+)\]", fm_content)
        if inline_m:
            for t in inline_m.group(1).split(","):
                ct = re.sub(r"[^a-zA-Z0-9_\-]", "", t.strip()).lower()
                if ct and ct not in existing_tags:
                    existing_tags.append(ct)

    merged_tags: List[str] = []
    for t in existing_tags + list(hub_info["tags"]) + ["windows", "linux"]:
        ct = re.sub(r"[^a-zA-Z0-9_\-]", "", t.strip()).lower()
        if ct and ct not in merged_tags:
            merged_tags.append(ct)

    cat_str = "commands" if is_command_note else "knowledge"
    if is_command_note:
        summary_str = (
            f"Verified Windows & Linux command playbook for {topic_label} ({hub_info['primary_tactic']}): "
            f"{hub_info['summary'][:135]}"
        )
    else:
        summary_str = (
            f"Operational architecture, decision workflows & Windows/Linux command reference for {topic_label}: "
            f"{hub_info['summary'][:130]}"
        )
    when_to_apply_str = (
        f"Apply when working with {topic_label} ({hub_info['os_platform']}): {hub_info['when_to_apply']}"
    )

    # Clean broken PDF prose fragments in command notes if present
    if is_command_note:
        clean_lines = []
        for ln in body_text.splitlines():
            if ln.startswith("| `s_") and any(b.lower() in ln.lower() for b in (
                "service access point) fields of the llc header",
                "iptables and snort",
                "snort rules tutorial:",
                "snort users manual:",
                "hostname of the local system",
            )):
                # Replace broken row with the primary verified command from hub_info
                c0, _, d0, _, _ = hub_info["commands"][0]
                tool0 = c0.split()[0].lstrip("sudo")
                clean_lines.append(
                    f"| `{hub_info['mdp_pre']}` | **`{hub_info['primary_tactic']}`** | {d0[:75]} | `{tool0}` | `{hub_info['mdp_post']}` | `{c0}` |"
                )
            elif _is_broken_prose_command(ln) and not ln.startswith("#") and not ln.startswith("-") and not ln.startswith("|"):
                clean_lines.append(hub_info["commands"][0][0])
            else:
                clean_lines.append(ln)
        body_text = "\n".join(clean_lines)

    title_prefix = "Trained Command Playbook" if is_command_note else "Trained Knowledge & Topology"
    safe_title = f"{title_prefix}: {topic_label}".replace('"', "'")
    safe_summary = summary_str.replace('"', "'")
    safe_wta = when_to_apply_str.replace('"', "'")

    new_frontmatter = (
        "---\n"
        f"title: \"{safe_title}\"\n"
        f"category: {cat_str}\n"
        f"domain_hub: \"[[{hub_info['wiki_link']}]]\"\n"
        f"os_platform: {hub_info['os_platform']}\n"
        f"primary_tactic: {hub_info['primary_tactic']}\n"
        f"summary: \"{safe_summary}\"\n"
        f"when_to_apply: \"{safe_wta}\"\n"
        f"tags: [{', '.join(merged_tags[:22])}]\n"
        f"source_file: \"{topic_label}\"\n"
        "updated: 2026-10-30\n"
        "---\n\n"
    )

    cmd_section = build_command_examples_markdown_section(hub_info, topic_label)
    final_text = new_frontmatter + body_text.strip() + "\n\n" + cmd_section + "\n"
    md_path.write_text(final_text, encoding="utf-8")

    return {
        "stem": stem,
        "topic": topic_label,
        "hub_key": hub_key,
        "os_platform": hub_info["os_platform"],
        "primary_tactic": hub_info["primary_tactic"],
        "summary": safe_summary,
        "when_to_apply": safe_wta,
        "has_paired_cmd": paired_cmd_exists,
        "has_paired_know": paired_know_exists,
    }


def write_domain_hub_files(hub_members: Dict[str, List[Dict[str, Any]]]) -> None:
    """Create the 10 organized Domain Knowledge Hub files in `core/ObsidianVault/knowledge/01_...md` - `10_...md`."""
    for hub_key, hub_info in sorted(DOMAIN_HUBS.items()):
        members = sorted(hub_members.get(hub_key, []), key=lambda x: x["stem"])
        hub_path = VAULT_DIR / "knowledge" / f"{hub_key}.md"
        tags_inline = ", ".join(hub_info["tags"])

        lines = [
            "---",
            f"title: \"{hub_info['title']}\"",
            "category: knowledge",
            f"domain_hub: \"[[{hub_info['wiki_link']}]]\"",
            f"os_platform: {hub_info['os_platform']}",
            f"primary_tactic: {hub_info['primary_tactic']}",
            f"summary: \"{hub_info['summary']}\"",
            f"when_to_apply: \"{hub_info['when_to_apply']}\"",
            f"tags: [{tags_inline}]",
            "updated: 2026-10-30",
            "---",
            "",
            f"# {hub_info['title']}",
            "",
            f"> **Summary:** {hub_info['summary']}  ",
            f"> **When to Apply:** {hub_info['when_to_apply']}  ",
            f"> **Target OS Platform:** `{hub_info['os_platform']}` | **Primary H-MDP Tactic:** `{hub_info['primary_tactic']}` (`{hub_info['mdp_pre']} -> {hub_info['mdp_post']}`)  ",
            f"> **Bayesian Root-Cause Alignment (`Engine 4`):** `{hub_info['bayesian_causes']}`  ",
            f"> **Network Isolation Compatibility:** `{hub_info['isolation']}`  ",
            "> **Backlinks:** [[00_MEMORY_INDEX]] | [[00_TRAINED_INDEX]] | [[commands/windows_master_command_playbook]] | [[commands/linux_master_command_playbook]]",
            "",
            "---",
            "",
            "## 1. Master Windows & Linux Command Matrix for This Domain",
            "",
            "| Command Syntax (`Windows` / `Linux`) | OS / Shell | Operational Purpose & Key Flags | When to Apply & Expected Output | Cross-Platform Equivalent |",
            "| :--- | :--- | :--- | :--- | :--- |",
        ]
        for cmd_str, shell_str, desc_str, apply_str, equiv_str in hub_info["commands"]:
            cmd_esc = cmd_str.replace("|", "\\|")
            equiv_esc = equiv_str.replace("|", "\\|")
            lines.append(
                f"| `{cmd_esc}` | **{shell_str}** | {desc_str} | {apply_str} | `{equiv_esc}` |"
            )

        lines.extend(
            [
                "",
                "---",
                "",
                f"## 2. Organized Domain Knowledge Notes & Paired Command Playbooks ({len(members)} Notes)",
                "",
                "| Topic | Knowledge Note (`knowledge/`) | Paired Command Playbook (`commands/`) | OS | Primary Tactic | When to Apply & Operational Summary |",
                "| :--- | :--- | :--- | :--- | :--- | :--- |",
            ]
        )
        for m in members:
            k_link = f"[[knowledge/{m['stem']}]]"
            c_link = f"[[commands/{m['stem']}]]" if m["has_paired_cmd"] else "[[commands/windows_master_command_playbook]] / [[commands/linux_master_command_playbook]]"
            lines.append(
                f"| **{m['topic']}** | {k_link} | {c_link} | `{m['os_platform']}` | `{m['primary_tactic']}` | {m['when_to_apply'][:140]} |"
            )

        hub_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_master_memory_indexes(hub_members: Dict[str, List[Dict[str, Any]]]) -> None:
    """Update `00_MEMORY_INDEX.md` and `00_TRAINED_INDEX.md` with organized hubs, master playbooks, and descriptive summaries."""
    mem_index_path = VAULT_DIR / "00_MEMORY_INDEX.md"
    existing_mem = mem_index_path.read_text(encoding="utf-8", errors="replace") if mem_index_path.is_file() else ""
    auto_block = ""
    if "<!-- AUTO-INDEX-START -->" in existing_mem and "<!-- AUTO-INDEX-END -->" in existing_mem:
        auto_block = existing_mem.split("<!-- AUTO-INDEX-START -->", 1)[1].split("<!-- AUTO-INDEX-END -->", 1)[0].strip()

    mem_lines = [
        "# Obsidian Memory Index (CORA Knowledge Vault — `00_MEMORY_INDEX`)",
        "",
        "> **Tier-1 Hot Memory:** Automatically loaded into the LLM system prompt and indexed by Engine 5 (`associative.py` Bipartite Graph) so the LLM and all 15 Neuro-Symbolic Engines immediately select the right Windows & Linux commands, playbooks, and domain knowledge.",
        "",
        "## 1. Master Cross-Platform Command Playbooks (`commands/`)",
        "- [[commands/windows_master_command_playbook]] — **[WINDOWS MASTER]** Comprehensive Windows CMD, PowerShell, WMI/CIM, Sysinternals (`pslist`, `listdlls`, `autorunsc`, `handle`, `sigcheck`, `accesschk`, `procdump`), Registry, `netsh advfirewall`/`portproxy`, `icacls`/`takeown`, `auditpol`, `wevtutil` Event IDs, `bcdedit`, and Active Directory (`dsquery`/`nltest`/`klist`) commands with When-to-Apply rules.",
        "- [[commands/linux_master_command_playbook]] — **[LINUX/UNIX MASTER]** Comprehensive Linux `iproute2` (`ip addr`, `ip route`, `ip neigh`), `ss -tulpn`, `iptables`/`nftables`, `sysctl` forwarding/NAT, `systemd`/`journalctl`, `/proc` forensics, SUID/Capabilities (`getcap`/`find`), `tcpdump`/BPF, `tshark`, `p0f`, `nmap`, and interactive TTY upgrade commands with When-to-Apply rules.",
        "- [[commands/curl_playbook]] — **[CROSS-PLATFORM WEB/API/TLS]** Non-hanging `curl -sS -k -L -i --max-time 15`, `openssl s_client` X.509 certificate serial/SAN extraction, mTLS client certs, reverse-proxy `X-Forwarded-For` bypass headers, and PowerShell `Invoke-WebRequest` patterns.",
        "- [[commands/tio_serial_playbook]] — **[HARDWARE UART SERIAL OOB]** Non-interactive `tio 3.9` Lua `--script` patterns with `-o 15 -O 120` anti-drop pacing for `/dev/ttyUSB0` & Windows `COM` port OOB appliance access.",
        "",
        "## 2. Organized Domain Knowledge Hubs (`knowledge/01_...` to `10_...`)",
    ]
    for hub_key, hub_info in sorted(DOMAIN_HUBS.items()):
        cnt = len(hub_members.get(hub_key, []))
        mem_lines.append(
            f"- [[{hub_info['wiki_link']}]] (`{hub_info['os_platform'].upper()}` | `{cnt} notes` | `{hub_info['primary_tactic']}`) — {hub_info['summary']} **Apply when:** {hub_info['when_to_apply']}"
        )

    mem_lines.extend(
        [
            "",
            "## 3. Quick-Reference Windows vs. Linux Tactical Command Matrix (By H-MDP Tactic)",
            "| Tactic (`Engine 15`) | Windows Command (`CMD` / `PowerShell` / `Sysinternals`) | Linux Command (`Bash` / `iproute2`) | When to Apply |",
            "| :--- | :--- | :--- | :--- |",
            "| **`Passive_Enum` (L2/L3)** | `ipconfig /all & route print -4 & arp -a` | `ip -4 -br addr show; ip route show; ip neigh show` | First passive probe (`s_init_unknown`) to map interfaces, subnets, routes & ARP cache |",
            "| **`Passive_Enum` (L4/Proc)** | `netstat -abno & tasklist /svc & wmic process get ProcessId,ParentProcessId,CommandLine` | `ss -tulpn; ps auxef; ls -la /proc/<PID>/exe` | Map listening ports (`127.0.0.1` vs `0.0.0.0`), owning PIDs, and process command lines |",
            "| **`L2_L3_Pivot_Routing`** | `route add <REMOTE_SUBNET> mask 255.255.255.0 <GW_IP>` | `sudo ip route replace <REMOTE_SUBNET> via <GW_IP> && sudo sysctl -w net.ipv4.ip_forward=1` | Target is in a disjoint subnet (`Engine 2` `C2_CROSS_SUBNET_L3_PIVOT`) |",
            "| **`Active_Enum` (Ports/Web)** | `Test-NetConnection <IP> -Port 443` / `curl.exe -sS -k -L -i --max-time 15 https://<IP>/` | `nmap -sV -sC -Pn <IP>` / `curl -sS -k -L -i --max-time 15 https://<IP>/` | L2/L3 verified (`s_l2_l3_verified`); enumerate services, TLS certs & firmware build dates |",
            "| **`OOB_Serial_Access`** | `reg query HKLM\\HARDWARE\\DEVICEMAP\\SERIALCOMM` | `tio -b 115200 -o 15 -O 120 --mute --script-run once --script 'write(\"\\r\"); msleep(400); while read(4096, 600) > 0 do end; exit(0)' /dev/ttyUSB0` | TCP/HTTP refused (`Exit 7`) or timed out (`Exit 28`) & local UART `/dev/ttyUSB0`/`COM1` present |",
            "| **`Defense_Evasion_Firewall`** | `netsh advfirewall show allprofiles` / `icacls <Path>` / `auditpol /get /category:*` | `sudo iptables -L -n -v` / `sudo nft list ruleset` / `sudo iptables -t nat -A POSTROUTING -j MASQUERADE` | Inspect/unlock host firewall drops, NAT masquerade return routes, or file ACLs |",
            "| **`Privilege_Escalation`** | `whoami /all & accesschk -accepteula -uwcqv * & sc qc <Svc>` | `sudo -l; find / -perm -4000 -type f 2>/dev/null; getcap -r / 2>/dev/null` | Escalate from initial shell (`s_initial_shell_or_api_access`) via privileges, services, SUID, or capabilities |",
            "| **`Credential_Access` & Logs** | `wevtutil qe Security /q:\"*[System[(EventID=4624 or EventID=4625 or EventID=4688)]]\" /c:15 /f:text` | `journalctl -xe -n 50; grep -rnI -iE 'password|bearer' /etc /var/www 2>/dev/null` | Inspect security event logs, Kerberos SPNs (`setspn -Q */*`), and configuration secrets |",
            "",
            "## 4. Scanned Targets & APIs",
            "- *(Isolated per-project inside `Projects/<active_project>/targets/` and `Projects/<active_project>/memory.md`)*",
            "",
            "## 5. High-Frequency Trained Command & Knowledge Playbooks (Full 196-Note Directory in `[[00_TRAINED_INDEX]]`)",
            "- [[commands/trained_basic_survey_commands]] / [[knowledge/trained_basic_survey_commands]] — `[WINDOWS]` Host, process, network, registry (`Run`/`RunOnce`/`Winlogon`), and `autorunsc` survey commands.",
            "- [[commands/trained_auditpol_cmds]] / [[knowledge/trained_auditpol_cmds]] — `[WINDOWS]` `auditpol` subcategory enumeration/enforcement, `wevtutil` Event Log queries, and `psloglist` SID filtering.",
            "- [[commands/trained_cacls_-_icacls_cmds]] / [[knowledge/trained_cacls_-_icacls_cmds]] — `[WINDOWS]` `icacls`, `cacls`, `takeown` DACL permission auditing, SDDL backup/restore, and ACE inheritance rules.",
            "- [[commands/trained_bcdedit_cmds]] / [[knowledge/trained_bcdedit_cmds]] — `[WINDOWS]` `bcdedit` boot loader enumeration and DEP (`nx AlwaysOn`/`OptIn`) configuration.",
            "- [[commands/trained_netsh_fw_cmds]] / [[commands/trained_netsh_commands_for_routing]] — `[WINDOWS]` `netsh advfirewall`, `netsh interface ipv4`, `portproxy`, and DHCP management.",
            "- [[commands/trained_ps_get-cim]] / [[commands/trained_wmic_quickstart]] — `[WINDOWS]` PowerShell `Get-CimInstance` and `wmic` process, service, OS, hotfix, and startup enumeration.",
            "- [[commands/trained_ds_cmds]] / [[commands/trained_domain_service_tools]] — `[WINDOWS AD]` Active Directory `dsquery`, `dsget`, `nltest`, `net group`, and Kerberos SPN enumeration.",
            "- [[commands/trained_centos-debian-survey]] / [[knowledge/trained_unix_and_linux_system_administration_handbook]] — `[LINUX]` Comprehensive Debian/Ubuntu/CentOS/RHEL host, kernel, service, network, and log survey.",
            "- [[commands/trained_iptables-snort-cmds]] / [[knowledge/trained_cqc001_e060_m030_iptables_and_snort]] — `[LINUX]` `iptables` filter/NAT rules, chains, packet counters, and `snort` IDS rule inspection.",
            "- [[commands/trained_bpf_syntax]] / [[knowledge/trained_cqc001_e010_m030_wireshark_display_filters]] — `[CROSS-PLATFORM]` `tcpdump` BPF byte-offset filters, `tshark` CLI extraction, Wireshark filters, and `p0f` passive OS fingerprinting.",
            "",
            "## 6. Neuro-Symbolic Reasoning & Causal Models",
            "- [[reasoning/rl_network_policy_playbooks]] — Engine 19 TD(lambda) RL Policy & 3-Step Next-Action Playbooks",
            "- [[reasoning/spectral_pca_kmeans_manifold]] — Engine 20 SVD PCA, K-Means++ Regime Clustering & Spectral Chokepoints",
            "- [[00_SUGGESTED_IMPROVEMENTS_INDEX]] — Engine 17 Meta-Learning Calibration & Suggested Improvements Index",
            "",
            "## Indexed Vault Notes",
            "<!-- AUTO-INDEX-START -->",
            auto_block or "- [[reasoning/rl_network_policy_playbooks]] — Engine 19 TD(lambda) RL Policy Playbooks (#reasoning #rl_network_policy)",
            "<!-- AUTO-INDEX-END -->",
        ]
    )
    mem_index_path.write_text("\n".join(mem_lines) + "\n", encoding="utf-8")

    # Also update 00_TRAINED_INDEX.md so all 196 notes are organized by the 10 Domain Hubs + full table
    trained_index_path = VAULT_DIR / "00_TRAINED_INDEX.md"
    t_lines = [
        "---",
        "title: \"CORA Organized Training & Domain Knowledge Index (00_TRAINED_INDEX)\"",
        "category: root",
        "os_platform: cross-platform",
        "summary: \"Complete organized index of all 10 Domain Knowledge Hubs, 4 Master Command Playbooks, 196 Knowledge Notes, and 146 Command Playbooks in core/ObsidianVault.\"",
        "when_to_apply: \"Consult this index to locate domain-specific Windows and Linux command playbooks and knowledge notes across all 10 operational domains.\"",
        "tags: [index, trained, commands, knowledge, windows, linux, mdp, cegar]",
        "updated: 2026-10-30",
        "---",
        "",
        "# CORA Organized Knowledge & Command Vault Index (`00_TRAINED_INDEX`)",
        "",
        "- **Parent Index:** [[00_MEMORY_INDEX]]",
        "- **Master Command Playbooks:** [[commands/windows_master_command_playbook]] | [[commands/linux_master_command_playbook]] | [[commands/curl_playbook]] | [[commands/tio_serial_playbook]]",
        "- **Organized Domain Knowledge Hubs:** `10` (`knowledge/01_...` through `knowledge/10_...`)",
        "- **Total Enriched Knowledge Notes (`knowledge/trained_*`):** `196`",
        "- **Total Enriched Command Playbooks (`commands/trained_*`):** `144` (+ `4` Master Playbooks = `148` total command notes)",
        "",
        "---",
        "",
        "## 1. The 10 Operational Domain Knowledge Hubs",
        "",
        "| Hub # | Domain Knowledge Hub | OS Platform | Primary H-MDP Tactic | Member Notes | When to Apply |",
        "| :--- | :--- | :--- | :--- | :--- | :--- |",
    ]
    for idx, (hub_key, hub_info) in enumerate(sorted(DOMAIN_HUBS.items()), 1):
        cnt = len(hub_members.get(hub_key, []))
        t_lines.append(
            f"| **Hub {idx:02d}** | [[{hub_info['wiki_link']}\\|{hub_info['title']}]] | `{hub_info['os_platform']}` | `{hub_info['primary_tactic']}` | `{cnt}` | {hub_info['when_to_apply']} |"
        )

    for idx, (hub_key, hub_info) in enumerate(sorted(DOMAIN_HUBS.items()), 1):
        members = sorted(hub_members.get(hub_key, []), key=lambda x: x["stem"])
        t_lines.extend(
            [
                "",
                "---",
                "",
                f"## {idx + 1}. {hub_info['title']} ([[{hub_info['wiki_link']}]] — {len(members)} Notes)",
                f"> **When to Apply:** {hub_info['when_to_apply']}",
                "",
                "| Topic | Knowledge Note | Command Playbook | OS | Tactic | Summary |",
                "| :--- | :--- | :--- | :--- | :--- | :--- |",
            ]
        )
        for m in members:
            k_link = f"[[knowledge/{m['stem']}]]"
            c_link = f"[[commands/{m['stem']}]]" if m["has_paired_cmd"] else "[[commands/windows_master_command_playbook]]"
            t_lines.append(
                f"| `{m['topic']}` | {k_link} | {c_link} | `{m['os_platform']}` | `{m['primary_tactic']}` | {m['summary'][:110]} |"
            )

    trained_index_path.write_text("\n".join(t_lines) + "\n", encoding="utf-8")


def main() -> int:
    hub_members: Dict[str, List[Dict[str, Any]]] = {k: [] for k in DOMAIN_HUBS}

    k_files = sorted((VAULT_DIR / "knowledge").glob("trained_*.md"))
    c_files = sorted((VAULT_DIR / "commands").glob("trained_*.md"))

    print(f"[1/4] Enriching {len(k_files)} knowledge/trained_*.md files...")
    for kf in k_files:
        txt = kf.read_text(encoding="utf-8", errors="replace")
        hub_key = classify_note_to_hub(kf.stem, txt)
        meta = enrich_vault_note(kf, is_command_note=False, hub_key=hub_key)
        hub_members[hub_key].append(meta)

    print(f"[2/4] Enriching {len(c_files)} commands/trained_*.md files...")
    for cf in c_files:
        txt = cf.read_text(encoding="utf-8", errors="replace")
        hub_key = classify_note_to_hub(cf.stem, txt)
        enrich_vault_note(cf, is_command_note=True, hub_key=hub_key)

    print("[3/4] Writing 10 Domain Knowledge Hubs & updating 00_MEMORY_INDEX.md / 00_TRAINED_INDEX.md...")
    write_domain_hub_files(hub_members)
    write_master_memory_indexes(hub_members)

    print("[4/4] Rebuilding Engine 5 Bipartite Vault Graph & vault_entities_cache.json...")
    if str(CORE_DIR) not in sys.path:
        sys.path.insert(0, str(CORE_DIR))
    from Reasoning.engines.associative import VAULT_ENTITIES_CACHE_FILE, _GRAPH_CACHE, build_vault_bipartite_graph

    cache_p = Path(VAULT_ENTITIES_CACHE_FILE)
    if cache_p.is_file():
        cache_p.unlink()
    _GRAPH_CACHE["signature"] = None
    _GRAPH_CACHE["graph"] = None
    G, note_meta = build_vault_bipartite_graph()
    print(
        f"Done! Bipartite Vault Graph built: {G.number_of_nodes()} total nodes "
        f"({len(note_meta)} Vault notes + {G.number_of_nodes() - len(note_meta)} concept/entity nodes), "
        f"{G.number_of_edges()} associative edges."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
