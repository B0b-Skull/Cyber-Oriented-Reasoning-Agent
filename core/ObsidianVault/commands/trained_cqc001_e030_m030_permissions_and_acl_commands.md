---
title: "Trained Command Playbook: CQC001 E030 M030 Permissions and ACL Commands"
category: commands
domain_hub: "[[knowledge/03_windows_security_acls_auditing_and_logs]]"
os_platform: windows
primary_tactic: Defense_Evasion_Firewall
summary: "Verified Windows & Linux command playbook for CQC001 E030 M030 Permissions and ACL Commands (Defense_Evasion_Firewall): Windows Security Identifiers (Well-Known SIDs), ACE/DACL inheritance rules, icacls/cacls/takeown file permission management, auditpol s"
when_to_apply: "Apply when working with CQC001 E030 M030 Permissions and ACL Commands (windows): Apply when inspecting or modifying Windows file/directory/service ACLs (`icacls`/`takeown`), mapping Well-Known SIDs, configuring or auditing Windows Security audit policy (`auditpol`), querying Windows Event Logs (`wevtutil`/`Get-WinEvent`/`psloglist`), or evaluating exploit mitigations (ASLR/DEP) and local privilege escalation vectors."
tags: [cacls, credential_access, enumeration, http, https, icacls, mdp, passive_enum, pdf, privilege_escalation, trained, windows, takeown, auditpol, wevtutil, psloglist, get-winevent, sid, acl, dacl, event_id, aslr]
source_file: "CQC001 E030 M030 Permissions and ACL Commands"
updated: 2026-10-30
---

icacls "C:\Program Files\TargetApp" && icacls "C:\Windows\Temp"
# Trained Command Playbook: `CQC001_E030_M030_Permissions_and_ACL_Commands.pdf`
icacls "C:\Program Files\TargetApp" && icacls "C:\Windows\Temp"
- **Source Document:** `~/Projects/CORA/Training/CQC001_E030_M030_Permissions_and_ACL_Commands.pdf`
- **CEGAR Verified Commands:** `32` (`0` malformed/unsafe snippets filtered)
- **MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`):** `32`
- **Discovered IPs/Subnets:** `None`
- **Discovered Interfaces:** `None`
- **Related Knowledge Note:** [[knowledge/trained_cqc001_e030_m030_permissions_and_acl_commands]]
icacls "C:\Program Files\TargetApp" && icacls "C:\Windows\Temp"
## Distilled MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`)
| Pre-State ($s$) | Tactic ($\tau$) | Technique ($k$) | Tool ($u$) | Post-State ($s'$) | Verified Command ($c$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `net` | `s_credentials_or_certs_acquired` | `Net user` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `net` | `s_active_services_enumerated` | `net help user \| more` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `net` | `s_passive_topology_mapped` | `Net localgroup` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `cacls` | `s_interactive_tty_or_priv_escalated` | `cacls FileName [/t] [/e] [/c] [/g User:permission] [/r User [...]] [/p User:permission [...]] [/d User [...]]` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `net` | `s_credentials_or_certs_acquired` | `net user [username [password \| *] [options]] [/domain]` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `net` | `s_active_services_enumerated` | `net help command: Displays help for the specified net command.` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `net` | `s_passive_topology_mapped` | `net localgroup [GroupName [/comment:"text"]] [/domain]` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `icacls` | `s_interactive_tty_or_priv_escalated` | `icacls <FileName> [/grant[:r] <Sid>:<Perm>[...]] [/deny <Sid>:<Perm>[...]] [/remove[:g\|:d]]` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `net` | `s_credentials_or_certs_acquired` | `Net user https://web.archive.org/web/20160804124854/https://technet.microsoft.com/en-us/library/Cc771865.aspx` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `write-only` | `s_active_services_enumerated` | `write-only access` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `net` | `s_passive_topology_mapped` | `net localgroup [GroupName {/add [/comment:"text"] \| /delete} [/domain]]` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `icacls` | `s_interactive_tty_or_priv_escalated` | `icacls <Directory> [/substitute <SidOld> <SidNew> [...]] [/restore <ACLfile> [/c] [/l] [/q]]` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `net` | `s_credentials_or_certs_acquired` | `Net localgroup https://web.archive.org/web/20160804124941/https://technet.microsoft.com/en-` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `net` | `s_passive_topology_mapped` | `net localgroup [GroupName name [ ...] {/add \| /delete} [/domain]]` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `icacls` | `s_interactive_tty_or_priv_escalated` | `icacls c:\windows\* /save aclfile /t` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `net` | `s_passive_topology_mapped` | `net localgroup` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `icacls` | `s_interactive_tty_or_priv_escalated` | `icacls c:\windows\ /restore aclfile` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `net` | `s_passive_topology_mapped` | `net localgroup exec /add` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `icacls` | `s_interactive_tty_or_priv_escalated` | `icacls test1 /grant User1:(d,wdac)` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `net` | `s_passive_topology_mapped` | `net localgroup exec /add /domain` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `icacls` | `s_interactive_tty_or_priv_escalated` | `icacls test2 /grant *S-1-1-0:(d,wdac)` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `net` | `s_passive_topology_mapped` | `net localgroup exec stevev sales\ralphr jennyt /add` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `runas` | `s_interactive_tty_or_priv_escalated` | `runas [{/profile\|/noprofile}] [/env] [/netonly] [/smartcard] [/showtrustlevels] [/trustlevel] /user:UserAccountName program` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `net` | `s_passive_topology_mapped` | `net localgroup exec stevev ralphr jennyt /add /domain` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `runas` | `s_interactive_tty_or_priv_escalated` | `runas /user:localmachinename\administrator cmd` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `net` | `s_passive_topology_mapped` | `net localgroup exec` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `runas` | `s_interactive_tty_or_priv_escalated` | `runas /user:companydomain\domainadmin "mmc %windir%\system32\compmgmt.msc"` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `net` | `s_passive_topology_mapped` | `net localgroup exec /comment:"The executive staff."` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `runas` | `s_interactive_tty_or_priv_escalated` | `runas /user:user@domain.microsoft.com "notepad my_file.txt"` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `runas` | `s_interactive_tty_or_priv_escalated` | `runas /netonly /user:domain\username "command"` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `cacls` | `s_interactive_tty_or_priv_escalated` | `CACLS https://web.archive.org/web/20160804125059/https://technet.microsoft.com/en-us/library/bb490872.aspx` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `icacls` | `s_interactive_tty_or_priv_escalated` | `ICACLS https://web.archive.org/web/20160611031312/https://technet.microsoft.com/en-` |
icacls "C:\Program Files\TargetApp" && icacls "C:\Windows\Temp"
## Verified Executable Commands (Grouped by Capability Layer)
icacls "C:\Program Files\TargetApp" && icacls "C:\Windows\Temp"
### General_System (28 commands)
```bash
Net user
net user [username [password | *] [options]] [/domain]
net help user | more
Net localgroup
net localgroup [GroupName [/comment:"text"]] [/domain]
net localgroup [GroupName {/add [/comment:"text"] | /delete} [/domain]]
net localgroup [GroupName name [ ...] {/add | /delete} [/domain]]
net help command: Displays help for the specified net command.
net localgroup
net localgroup exec /add
net localgroup exec /add /domain
net localgroup exec stevev sales\ralphr jennyt /add
net localgroup exec stevev ralphr jennyt /add /domain
net localgroup exec
net localgroup exec /comment:"The executive staff."
cacls FileName [/t] [/e] [/c] [/g User:permission] [/r User [...]] [/p User:permission [...]] [/d User [...]]
icacls <FileName> [/grant[:r] <Sid>:<Perm>[...]] [/deny <Sid>:<Perm>[...]] [/remove[:g|:d]]
icacls <Directory> [/substitute <SidOld> <SidNew> [...]] [/restore <ACLfile> [/c] [/l] [/q]]
write-only access
icacls c:\windows\* /save aclfile /t
icacls c:\windows\ /restore aclfile
icacls test1 /grant User1:(d,wdac)
icacls test2 /grant *S-1-1-0:(d,wdac)
runas [{/profile|/noprofile}] [/env] [/netonly] [/smartcard] [/showtrustlevels] [/trustlevel] /user:UserAccountName program
runas /user:localmachinename\administrator cmd
runas /user:companydomain\domainadmin "mmc %windir%\system32\compmgmt.msc"
runas /user:user@domain.microsoft.com "notepad my_file.txt"
runas /netonly /user:domain\username "command"
```
icacls "C:\Program Files\TargetApp" && icacls "C:\Windows\Temp"
### L7_HTTP_Web (4 commands)
```bash
Net user https://web.archive.org/web/20160804124854/https://technet.microsoft.com/en-us/library/Cc771865.aspx
Net localgroup https://web.archive.org/web/20160804124941/https://technet.microsoft.com/en-
CACLS https://web.archive.org/web/20160804125059/https://technet.microsoft.com/en-us/library/bb490872.aspx
ICACLS https://web.archive.org/web/20160611031312/https://technet.microsoft.com/en-
```
icacls "C:\Program Files\TargetApp" && icacls "C:\Windows\Temp"

<!-- CORA-MAXIMIZED-COMMANDS-START -->
## Maximized Windows & Linux Command Examples for `CQC001 E030 M030 Permissions and ACL Commands`

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
