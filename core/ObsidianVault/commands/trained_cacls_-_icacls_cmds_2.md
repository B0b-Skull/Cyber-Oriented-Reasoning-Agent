---
title: "Trained Command Playbook: Cacls - Icacls CMDs 2"
category: commands
domain_hub: "[[knowledge/03_windows_security_acls_auditing_and_logs]]"
os_platform: windows
primary_tactic: Defense_Evasion_Firewall
summary: "Verified Windows & Linux command playbook for Cacls - Icacls CMDs 2 (Defense_Evasion_Firewall): Windows Security Identifiers (Well-Known SIDs), ACE/DACL inheritance rules, icacls/cacls/takeown file permission management, auditpol s"
when_to_apply: "Apply when working with Cacls - Icacls CMDs 2 (windows): Apply when inspecting or modifying Windows file/directory/service ACLs (`icacls`/`takeown`), mapping Well-Known SIDs, configuring or auditing Windows Security audit policy (`auditpol`), querying Windows Event Logs (`wevtutil`/`Get-WinEvent`/`psloglist`), or evaluating exploit mitigations (ASLR/DEP) and local privilege escalation vectors."
tags: [cacls, credential_access, enumeration, icacls, mdp, passive_enum, privilege_escalation, text, trained, windows, takeown, auditpol, wevtutil, psloglist, get-winevent, sid, acl, dacl, event_id, aslr, dep, defense_evasion_firewall]
source_file: "Cacls - Icacls CMDs 2"
updated: 2026-10-30
---

icacls "C:\Program Files\TargetApp" && icacls "C:\Windows\Temp"
# Trained Command Playbook: `Cacls - Icacls CMDs 2.txt`
icacls "C:\Program Files\TargetApp" && icacls "C:\Windows\Temp"
- **Source Document:** `~/Projects/CORA/Training/Cacls - Icacls CMDs 2.txt`
- **CEGAR Verified Commands:** `40` (`0` malformed/unsafe snippets filtered)
- **MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`):** `40`
- **Discovered IPs/Subnets:** `None`
- **Discovered Interfaces:** `None`
- **Related Knowledge Note:** [[knowledge/trained_cacls_-_icacls_cmds_2]]
icacls "C:\Program Files\TargetApp" && icacls "C:\Windows\Temp"
## Distilled MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`)
| Pre-State ($s$) | Tactic ($\tau$) | Technique ($k$) | Tool ($u$) | Post-State ($s'$) | Verified Command ($c$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `net` | `s_interactive_tty_or_priv_escalated` | `net localgroup "Power Users" larry moe /add` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `net` | `s_passive_topology_mapped` | `net localgroup users larry moe /delete` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `net` | `s_credentials_or_certs_acquired` | `net user larry 3st00g3s /add` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `md` | `s_active_services_enumerated` | `md "C:\The Stooges\Larry" "C:\The Stooges\Curly" "C:\The Stooges\Moe" "C:\The Stooges\Joe"` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `cacls` | `s_interactive_tty_or_priv_escalated` | `cacls c:\ /t /e /g Administrators:f` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `mkdir` | `s_passive_topology_mapped` | `mkdir "C:\The Stooges"` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `net` | `s_credentials_or_certs_acquired` | `net user Moe 3st00g3s /add` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `echo` | `s_active_services_enumerated` | `echo 'Hello Huey' > "c:\The Ducks\Huey\Hello-Huey.txt" & echo 'Hello Fred' > "c:\The Ducks\Fred\Hello-Fred.txt"` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `cacls` | `s_interactive_tty_or_priv_escalated` | `cacls "C:\The Stooges" /P user1:permissions  user2:permissions user3:permissions` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `net` | `s_passive_topology_mapped` | `net share sharename=drive:path /GRANT:user,[READ \| CHANGE \| FULL] /GRANT:user,[READ \| CHANGE \| FULL]` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `net` | `s_credentials_or_certs_acquired` | `net user Curly 3st00g3s /add` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `cacls` | `s_interactive_tty_or_priv_escalated` | `cacls "C:\The Stooges" /E /P /G "Power Users":f` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `net` | `s_credentials_or_certs_acquired` | `net user Joe 3st00g3s /add` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `cacls` | `s_interactive_tty_or_priv_escalated` | `cacls "C:\The Stooges\Larry" /E /G Larry:f & cacls "C:\The Stooges\Moe" /E /G Moe:f & cacls "C:\The Stooges\Curly" /E /G Curly:f & cacls "C:\The Stooges\Joe" /E /G Joe:f` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `echo` | `s_credentials_or_certs_acquired` | `echo 'Hello Joe' > "c:\The Stooges\Joe\Hello.txt" & echo 'Hello Moe' > "c:\The Stooges\Moe\Hello.txt"` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `cacls` | `s_interactive_tty_or_priv_escalated` | `cacls "C:\The Stooges\Larry" /E /R Users & cacls "C:\The Stooges\Moe" /E /R Users & cacls "C:\The Stooges\Curly" /E /R Users & cacls "C:\The Stooges\Joe" /E /R Users` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `net` | `s_credentials_or_certs_acquired` | `net user Larry /Time:M-F,1am-9am` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `cacls` | `s_interactive_tty_or_priv_escalated` | `cacls "C:\The Stooges\Moe\Hello.txt" /E /R Moe & cacls "C:\The Stooges\Joe\Hello.txt" /E /R Joe` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `net` | `s_credentials_or_certs_acquired` | `net user Huey $Password! /add` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `cacls` | `s_interactive_tty_or_priv_escalated` | `cacls "C:\The Stooges\Joe\Hello.txt" /E /g Joe:F & cacls "C:\The Stooges\Moe" /E /g Joe:W` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `net` | `s_credentials_or_certs_acquired` | `net user Dewey $Password! /add` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `icacls` | `s_interactive_tty_or_priv_escalated` | `icacls "d:\users" /grant "domain admins":(OI)(CI)F /inheritance:r` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `net` | `s_credentials_or_certs_acquired` | `net user Louie $Password! /add` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `icacls` | `s_interactive_tty_or_priv_escalated` | `icacls "d:\users" /grant "everyone":R /inheritance:r` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `net` | `s_credentials_or_certs_acquired` | `net user Fred $Password! /add` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `icacls` | `s_interactive_tty_or_priv_escalated` | `icacls "d:\profiles" /grant "domain admins":(OI)(CI)F /inheritance:r` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `net` | `s_credentials_or_certs_acquired` | `net localgroup Ducks /add` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `icacls` | `s_interactive_tty_or_priv_escalated` | `icacls "d:\profiles" /grant "everyone":R /inheritance:r` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `md` | `s_credentials_or_certs_acquired` | `md "C:\The Ducks\Huey" "C:\The Ducks\Dewey" "C:\The Ducks\Louie" "C:\The Ducks\Fred"` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `cacls` | `s_interactive_tty_or_priv_escalated` | `cacls "c:\The Ducks" /t /e /g Ducks:f` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `icacls` | `s_interactive_tty_or_priv_escalated` | `icacls "c:\The Ducks" /grant Ducks:(CI)(F)` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `icacls` | `s_interactive_tty_or_priv_escalated` | `icacls "c:\The Ducks\Huey" /grant Huey:F /remove "Users" & icacls "c:\The Ducks\Dewey" /grant Dewey:F /remove "Users" & icacls "c:\The Ducks\Louie" /grant Louie:F /remove "Users" & icacls "c:\The Ducks\Fred" /grant Fred:F /remove "Users"` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `icacls` | `s_interactive_tty_or_priv_escalated` | `icacls "c:\The Ducks" /inheritance:d` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `icacls` | `s_interactive_tty_or_priv_escalated` | `icacls "c:\The Ducks" /remove "Authenticated Users"` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `icacls` | `s_interactive_tty_or_priv_escalated` | `icacls "c:\The Ducks" /remove "Users"` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `icacls` | `s_interactive_tty_or_priv_escalated` | `icacls "c:\The Ducks\Huey" /grant Huey:F /remove "Users" /inheritance:e /t & icacls "c:\The Ducks\Dewey" /grant Dewey:F /remove "Users" /inheritance:e /t & icacls "c:\The Ducks\Louie" /grant Louie:F /remove "Users" /inheritance:e /t & icacls "c:\The Ducks\Fred" /grant Fred:F /remove "Users" /inheritance:e /t` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `icacls` | `s_interactive_tty_or_priv_escalated` | `icacls "c:\The Ducks\Huey" /grant Huey:F /remove "Users" /inheritance:d & icacls "c:\The Ducks\Dewey" /grant Dewey:F /remove "Users" /inheritance:d & icacls "c:\The Ducks\Louie" /grant Louie:F /remove "Users" /inheritance:d & icacls "c:\The Ducks\Fred" /grant Fred:F /remove "Users" /inheritance:d` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `icacls` | `s_interactive_tty_or_priv_escalated` | `icacls "c:\The Ducks\Huey" /remove "NT Authority\Authenticated Users" & icacls "c:\The Ducks\Dewey" /remove "NT Authority\Authenticated Users" & icacls "c:\The Ducks\Louie" /remove "NT Authority\Authenticated Users" & icacls "c:\The Ducks\Fred" /remove "NT Authority\Authenticated Users"` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `icacls` | `s_interactive_tty_or_priv_escalated` | `icacls "c:\The Ducks\fred" /grant fred:(F)` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `icacls` | `s_interactive_tty_or_priv_escalated` | `icacls "c:\The Ducks\Huey" /grant fred:(M) /t` |
icacls "C:\Program Files\TargetApp" && icacls "C:\Windows\Temp"
## Verified Executable Commands (Grouped by Capability Layer)
icacls "C:\Program Files\TargetApp" && icacls "C:\Windows\Temp"
### General_System (40 commands)
```bash
net localgroup "Power Users" larry moe /add
net localgroup users larry moe /delete
net user larry 3st00g3s /add
net user Moe 3st00g3s /add
net user Curly 3st00g3s /add
net user Joe 3st00g3s /add
mkdir "C:\The Stooges"
cacls c:\ /t /e /g Administrators:f
cacls "C:\The Stooges" /P user1:permissions  user2:permissions user3:permissions
cacls "C:\The Stooges" /E /P /G "Power Users":f
cacls "C:\The Stooges\Larry" /E /G Larry:f & cacls "C:\The Stooges\Moe" /E /G Moe:f & cacls "C:\The Stooges\Curly" /E /G Curly:f & cacls "C:\The Stooges\Joe" /E /G Joe:f
cacls "C:\The Stooges\Larry" /E /R Users & cacls "C:\The Stooges\Moe" /E /R Users & cacls "C:\The Stooges\Curly" /E /R Users & cacls "C:\The Stooges\Joe" /E /R Users
cacls "C:\The Stooges\Moe\Hello.txt" /E /R Moe & cacls "C:\The Stooges\Joe\Hello.txt" /E /R Joe
cacls "C:\The Stooges\Joe\Hello.txt" /E /g Joe:F & cacls "C:\The Stooges\Moe" /E /g Joe:W
md "C:\The Stooges\Larry" "C:\The Stooges\Curly" "C:\The Stooges\Moe" "C:\The Stooges\Joe"
icacls "d:\users" /grant "domain admins":(OI)(CI)F /inheritance:r
icacls "d:\users" /grant "everyone":R /inheritance:r
icacls "d:\profiles" /grant "domain admins":(OI)(CI)F /inheritance:r
icacls "d:\profiles" /grant "everyone":R /inheritance:r
net share sharename=drive:path /GRANT:user,[READ | CHANGE | FULL] /GRANT:user,[READ | CHANGE | FULL]
echo 'Hello Joe' > "c:\The Stooges\Joe\Hello.txt" & echo 'Hello Moe' > "c:\The Stooges\Moe\Hello.txt"
net user Larry /Time:M-F,1am-9am
net user Huey $Password! /add
net user Dewey $Password! /add
net user Louie $Password! /add
net user Fred $Password! /add
net localgroup Ducks /add
md "C:\The Ducks\Huey" "C:\The Ducks\Dewey" "C:\The Ducks\Louie" "C:\The Ducks\Fred"
cacls "c:\The Ducks" /t /e /g Ducks:f
icacls "c:\The Ducks" /grant Ducks:(CI)(F)
icacls "c:\The Ducks\Huey" /grant Huey:F /remove "Users" & icacls "c:\The Ducks\Dewey" /grant Dewey:F /remove "Users" & icacls "c:\The Ducks\Louie" /grant Louie:F /remove "Users" & icacls "c:\The Ducks\Fred" /grant Fred:F /remove "Users"
icacls "c:\The Ducks" /inheritance:d
icacls "c:\The Ducks" /remove "Authenticated Users"
icacls "c:\The Ducks" /remove "Users"
icacls "c:\The Ducks\Huey" /grant Huey:F /remove "Users" /inheritance:e /t & icacls "c:\The Ducks\Dewey" /grant Dewey:F /remove "Users" /inheritance:e /t & icacls "c:\The Ducks\Louie" /grant Louie:F /remove "Users" /inheritance:e /t & icacls "c:\The Ducks\Fred" /grant Fred:F /remove "Users" /inheritance:e /t
icacls "c:\The Ducks\Huey" /grant Huey:F /remove "Users" /inheritance:d & icacls "c:\The Ducks\Dewey" /grant Dewey:F /remove "Users" /inheritance:d & icacls "c:\The Ducks\Louie" /grant Louie:F /remove "Users" /inheritance:d & icacls "c:\The Ducks\Fred" /grant Fred:F /remove "Users" /inheritance:d
icacls "c:\The Ducks\Huey" /remove "NT Authority\Authenticated Users" & icacls "c:\The Ducks\Dewey" /remove "NT Authority\Authenticated Users" & icacls "c:\The Ducks\Louie" /remove "NT Authority\Authenticated Users" & icacls "c:\The Ducks\Fred" /remove "NT Authority\Authenticated Users"
echo 'Hello Huey' > "c:\The Ducks\Huey\Hello-Huey.txt" & echo 'Hello Fred' > "c:\The Ducks\Fred\Hello-Fred.txt"
icacls "c:\The Ducks\fred" /grant fred:(F)
icacls "c:\The Ducks\Huey" /grant fred:(M) /t
```
icacls "C:\Program Files\TargetApp" && icacls "C:\Windows\Temp"

<!-- CORA-MAXIMIZED-COMMANDS-START -->
## Maximized Windows & Linux Command Examples for `Cacls - Icacls CMDs 2`

> **Domain Hub:** [[knowledge/03_windows_security_acls_auditing_and_logs|Domain Hub 03: Windows Security, SIDs, DACLs/ACLs (icacls), Audit Policy (auditpol), Event Logs (wevtutil) & Mitigations (ASLR/DEP)]]  
> **Master Playbooks:** [[commands/windows_master_command_playbook]] | [[commands/linux_master_command_playbook]] | [[commands/curl_playbook]] | [[commands/tio_serial_playbook]]  
> **When to Apply:** Apply when inspecting or modifying Windows file/directory/service ACLs (`icacls`/`takeown`), mapping Well-Known SIDs, configuring or auditing Windows Security audit policy (`auditpol`), querying Windows Event Logs (`wevtutil`/`Get-WinEvent`/`psloglist`), or evaluating exploit mitigations (ASLR/DEP) and local privilege escalation vectors.  
> **15-Engine H-MDP State Transition:** `s_oob_serial_enumerated` $\xrightarrow{\text{Defense_Evasion_Firewall}}$ `s_firewall_or_acl_unlocked` | **Bayesian Root-Cause Triggers:** `restrictive_dacl_or_ownership, missing_audit_policy_coverage, privilege_escalation_via_weak_acl, token_impersonation_hot_potato` | **Isolation:** `RED, BLUE, WHITE (100% local host telemetry compatible)`

| Primary Command (`Windows` / `Linux`) | OS / Shell | What It Does & Key Flags | When to Apply & Expected Output | Cross-Platform Equivalent |
| :--- | :--- | :--- | :--- | :--- |
| `icacls "C:\Program Files\TargetApp" && icacls "C:\Windows\Temp"` | **Windows CMD** | Displays Discretionary Access Control Lists (`DACLs`), showing principal SIDs/names, access masks `(F)` Full, `(M)` Modify, `(RX)` Read/Exec, `(W)` Write, and inheritance flags `(OI)(CI)(IO)`. | Apply when checking if service binaries, config files, or PATH directories are writable by non-admin users (`BUILTIN\Users` or `Everyone`). | `getfacl <path> && ls -ld <path>` |
| `icacls "C:\TargetDir" /save C:\Temp\acl_backup.sddl /T && icacls "C:\TargetDir" /grant Administrators:(OI)(CI)F /T` | **Windows CMD (Admin)** | Backs up existing SDDL ACLs recursively (`/save ... /T`) and grants `Administrators` Full Control with Object and Container Inheritance `(OI)(CI)`. | Apply whenever unlocking restrictive file/folder permissions while preserving a lossless SDDL backup (`/restore`). | `getfacl -R <dir> > backup.acl && sudo setfacl -R -m u:root:rwx <dir>` |
| `takeown /f "C:\TargetDir" /r /a /d y` | **Windows CMD (Admin)** | Recursively (`/r`) transfers ownership of locked files/folders to the `Administrators` group (`/a`) without interactive prompts (`/d y`). | Apply when `icacls` fails with `Access is denied` because ownership is held by `TrustedInstaller` or another account. | `sudo chown -R root:root <dir>` |
| `auditpol /get /category:* && auditpol /list /subcategory:*` | **Windows CMD (Admin)** | Displays active Success and Failure audit settings across all 9 top-level categories and 50+ granular subcategories. | Apply first during log/forensic readiness checks to verify whether `Process Creation`, `Logon`, `SAM`, or `Kerberos` auditing is enabled. | `sudo auditctl -l && sudo auditctl -s` |
| `auditpol /set /subcategory:"Sensitive Privilege Use" /success:enable /failure:enable && auditpol /set /subcategory:"User Account Management" /success:enable /failure:enable` | **Windows CMD (Admin)** | Enables granular security event auditing for high-privilege token usage (`4672`/`4673`) and user account creation/modification (`4720`/`4728`/`4732`). | Apply to ensure privilege escalation and account changes generate `Security.evtx` telemetry. | `sudo auditctl -w /etc/passwd -p wa -k user_mod` |
| `wevtutil qe Security /q:"*[System[(EventID=4624 or EventID=4625 or EventID=4672)]]" /c:20 /rd:true /f:text` | **Windows CMD (Admin)** | Queries the `Security` event log newest-first (`/rd:true`) for the last 20 Logon Success (`4624`), Logon Failure (`4625`), and Admin Special Logon (`4672`) events. | Apply to trace interactive (`Type 2`), network/SMB (`Type 3`), and RDP (`Type 10`) logons or brute-force attempts. | `sudo grep -E 'Accepted\|Failed\|sudo' /var/log/auth.log /var/log/secure \| tail -n 30` |
| `wevtutil qe Security /q:"*[System[(EventID=4688 or EventID=4697 or EventID=4720 or EventID=1102)]]" /c:20 /rd:true /f:text` | **Windows CMD (Admin)** | Extracts Process Creation (`4688`), Service Installation (`4697`), User Account Creation (`4720`), and Audit Log Cleared (`1102`) events. | Apply during incident response to pinpoint persistence installation, rogue accounts, or anti-forensic log clearing. | `sudo ausearch -m EXECVE,ADD_USER,SERVICE_START -ts recent` |
| `wevtutil qe System /q:"*[System[(EventID=7045 or EventID=7036)]]" /c:15 /rd:true /f:text` | **Windows CMD** | Queries `System` log for new Service Control Manager service installations (`7045`) and service state changes (`7036`). | Apply even when `Security` audit policy was disabled: `System` Event `7045` records the service binary path by default! | `journalctl -u systemd -n 30 --no-pager` |
| `powershell -NoProfile -Command "Get-WinEvent -FilterHashtable @{LogName='Microsoft-Windows-PowerShell/Operational'; Id=4104} -MaxEvents 10 \| Format-List TimeCreated,Message"` | **PowerShell** | Reads the last 10 PowerShell ScriptBlock Logging (`Event ID 4104`) records containing full de-obfuscated PowerShell code executed on the host. | Apply to uncover fileless PowerShell payloads, `Invoke-Expression` cradles, or Empire/PowerSploit modules. | `ausearch -m EXECVE -c bash` |
| `powershell -NoProfile -Command "Get-ProcessMitigation -System"` | **PowerShell** | Displays system-wide exploit mitigation policies (`DEP`, `ASLR` ForceRelocateImages/BottomUp, `CFG` Control Flow Guard, `SEHOP`). | Apply when auditing Windows memory protection mechanisms (`[[knowledge/trained_address_space_layout_randomization]]`). | `sysctl kernel.randomize_va_space && checksec --proc-all` |

### Copy-Pasteable Execution Block (Windows & Linux)
```bash
# [Windows CMD] Displays Discretionary Access Control Lists (`DACLs`), showing principal SIDs/names, access masks `(F)` Full, `(M)` Modify, `(RX)` Read/Exec, `(W)` Write, and inheritance flags `(OI)(CI)(IO)`.
icacls "C:\Program Files\TargetApp" && icacls "C:\Windows\Temp"
# [Windows CMD (Admin)] Backs up existing SDDL ACLs recursively (`/save ... /T`) and grants `Administrators` Full Control with Object and Container Inheritance `(OI)(CI)`.
icacls "C:\TargetDir" /save C:\Temp\acl_backup.sddl /T && icacls "C:\TargetDir" /grant Administrators:(OI)(CI)F /T
# [Windows CMD (Admin)] Recursively (`/r`) transfers ownership of locked files/folders to the `Administrators` group (`/a`) without interactive prompts (`/d y`).
takeown /f "C:\TargetDir" /r /a /d y
# [Windows CMD (Admin)] Displays active Success and Failure audit settings across all 9 top-level categories and 50+ granular subcategories.
auditpol /get /category:* && auditpol /list /subcategory:*
# [Windows CMD (Admin)] Enables granular security event auditing for high-privilege token usage (`4672`/`4673`) and user account creation/modification (`4720`/`4728`/`4732`).
auditpol /set /subcategory:"Sensitive Privilege Use" /success:enable /failure:enable && auditpol /set /subcategory:"User Account Management" /success:enable /failure:enable
# [Windows CMD (Admin)] Queries the `Security` event log newest-first (`/rd:true`) for the last 20 Logon Success (`4624`), Logon Failure (`4625`), and Admin Special Logon (`4672`) events.
wevtutil qe Security /q:"*[System[(EventID=4624 or EventID=4625 or EventID=4672)]]" /c:20 /rd:true /f:text
```
<!-- CORA-MAXIMIZED-COMMANDS-END -->
