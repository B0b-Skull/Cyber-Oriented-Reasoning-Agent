---
title: "Trained Command Playbook: UsersAndPermissions"
category: commands
domain_hub: "[[knowledge/03_windows_security_acls_auditing_and_logs]]"
os_platform: windows
primary_tactic: Defense_Evasion_Firewall
summary: "Verified Windows & Linux command playbook for UsersAndPermissions (Defense_Evasion_Firewall): Windows Security Identifiers (Well-Known SIDs), ACE/DACL inheritance rules, icacls/cacls/takeown file permission management, auditpol s"
when_to_apply: "Apply when working with UsersAndPermissions (windows): Apply when inspecting or modifying Windows file/directory/service ACLs (`icacls`/`takeown`), mapping Well-Known SIDs, configuring or auditing Windows Security audit policy (`auditpol`), querying Windows Event Logs (`wevtutil`/`Get-WinEvent`/`psloglist`), or evaluating exploit mitigations (ASLR/DEP) and local privilege escalation vectors."
tags: [credential_access, enumeration, john, mdp, passive_enum, privilege_escalation, text, trained, windows, icacls, cacls, takeown, auditpol, wevtutil, psloglist, get-winevent, sid, acl, dacl, event_id, aslr, dep]
source_file: "UsersAndPermissions"
updated: 2026-10-30
---

icacls "C:\Program Files\TargetApp" && icacls "C:\Windows\Temp"
# Trained Command Playbook: `UsersAndPermissions.txt`
icacls "C:\Program Files\TargetApp" && icacls "C:\Windows\Temp"
- **Source Document:** `~/Projects/CORA/Training/UsersAndPermissions.txt`
- **CEGAR Verified Commands:** `39` (`0` malformed/unsafe snippets filtered)
- **MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`):** `39`
- **Discovered IPs/Subnets:** `None`
- **Discovered Interfaces:** `None`
- **Related Knowledge Note:** [[knowledge/trained_usersandpermissions]]
icacls "C:\Program Files\TargetApp" && icacls "C:\Windows\Temp"
## Distilled MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`)
| Pre-State ($s$) | Tactic ($\tau$) | Technique ($k$) | Tool ($u$) | Post-State ($s'$) | Verified Command ($c$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `chown` | `s_interactive_tty_or_priv_escalated` | `chown -R --from=userA UserB /usr/directory` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `find` | `s_passive_topology_mapped` | `find / -xdev -group <group>` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `cp` | `s_credentials_or_certs_acquired` | `cp -r /etc/skel /home/freddo` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `cp` | `s_active_services_enumerated` | `cp /tmp/helloscript.sh .` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `chown` | `s_interactive_tty_or_priv_escalated` | `chown newOwnerUsername Filename` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `ls` | `s_passive_topology_mapped` | `ls -l /home/johnd/comments.txt` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `cp` | `s_active_services_enumerated` | `cp /tmp/helloscript.sh ~fred` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `chown` | `s_interactive_tty_or_priv_escalated` | `chown newOnwerUsername:newOwnerGroup Filename` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `mkdir` | `s_passive_topology_mapped` | `mkdir /stooge /stooge/larry /stooge/moe /stooge/shemp /stooge/curly /stooge/joe; cd /stooge` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `cp` | `s_active_services_enumerated` | `cp /etc/passwd /stooge` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `chmod` | `s_interactive_tty_or_priv_escalated` | `chmod symbolic-mode-list filename` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `ls` | `s_active_services_enumerated` | `ls /stooge` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `chmod` | `s_interactive_tty_or_priv_escalated` | `chmod u+rw,g=x,go-wx /home/johnd/script.sh` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `chmod` | `s_interactive_tty_or_priv_escalated` | `chmod u+rw,g=,o=u /home/johnd/pod.txt` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `chmod` | `s_interactive_tty_or_priv_escalated` | `chmod a=r /home/johnd/pod.txt` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `chmod` | `s_interactive_tty_or_priv_escalated` | `chmod ugo=r	/home/johnd/pod.txt` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `chmod` | `s_interactive_tty_or_priv_escalated` | `chmod absolute-mode filename` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `chmod` | `s_interactive_tty_or_priv_escalated` | `chmod 653 /home/johnd/comments` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `chmod` | `s_interactive_tty_or_priv_escalated` | `chmod u+x,g-x,o= /home/johnd/comments.txt` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `chmod` | `s_interactive_tty_or_priv_escalated` | `chmod 650 /tmp/comments.txt` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `chmod` | `s_interactive_tty_or_priv_escalated` | `chmod u-x,g=rx,o-r /tmp/comments.txt` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `chmod` | `s_interactive_tty_or_priv_escalated` | `chmod u=rw,g+x,g-w,o-r /tmp/comments.txt` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `chmod` | `s_interactive_tty_or_priv_escalated` | `chmod ugo-rwx,u-x,g-w,o-rwx /tmp/comments.txt` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `chown` | `s_interactive_tty_or_priv_escalated` | `chown -R fred:staff /home/freddo` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `chmod` | `s_interactive_tty_or_priv_escalated` | `chmod 6640 /home/johnd/scripts/*.sh` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `-u` | `s_interactive_tty_or_priv_escalated` | `sudo -u root ./setup.sh` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `chown` | `s_interactive_tty_or_priv_escalated` | `chown fred:staff helloscript.sh` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `chown` | `s_interactive_tty_or_priv_escalated` | `chown fred helloscript.sh` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `chgrp` | `s_interactive_tty_or_priv_escalated` | `chgrp staff helloscript.sh` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `chmod` | `s_interactive_tty_or_priv_escalated` | `chmod 750 helloscript.sh` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `chown` | `s_interactive_tty_or_priv_escalated` | `chown :staff helloprog` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `chgrp` | `s_interactive_tty_or_priv_escalated` | `chgrp staff helloprog` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `chmod` | `s_interactive_tty_or_priv_escalated` | `chmod g-r helloscript.sh` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `chmod` | `s_interactive_tty_or_priv_escalated` | `chmod go-r helloprog` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `chgrp` | `s_interactive_tty_or_priv_escalated` | `chgrp -R stooges /stooge` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `chmod` | `s_interactive_tty_or_priv_escalated` | `chmod 710 /stooge` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `chmod` | `s_interactive_tty_or_priv_escalated` | `chmod 750 curly larry moe joe shemp` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `chmod` | `s_interactive_tty_or_priv_escalated` | `chmod g+rw /stooge` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `chmod` | `s_interactive_tty_or_priv_escalated` | `chmod +t /stooge` |
icacls "C:\Program Files\TargetApp" && icacls "C:\Windows\Temp"
## Verified Executable Commands (Grouped by Capability Layer)
icacls "C:\Program Files\TargetApp" && icacls "C:\Windows\Temp"
### General_System (39 commands)
```bash
chown -R --from=userA UserB /usr/directory
find / -xdev -group <group>
chown newOwnerUsername Filename
chown newOnwerUsername:newOwnerGroup Filename
chmod symbolic-mode-list filename
chmod u+rw,g=x,go-wx /home/johnd/script.sh
chmod u+rw,g=,o=u /home/johnd/pod.txt
chmod a=r /home/johnd/pod.txt
chmod ugo=r	/home/johnd/pod.txt
chmod absolute-mode filename
ls -l /home/johnd/comments.txt
chmod 653 /home/johnd/comments
chmod u+x,g-x,o= /home/johnd/comments.txt
chmod 650 /tmp/comments.txt
chmod u-x,g=rx,o-r /tmp/comments.txt
chmod u=rw,g+x,g-w,o-r /tmp/comments.txt
chmod ugo-rwx,u-x,g-w,o-rwx /tmp/comments.txt
cp -r /etc/skel /home/freddo
chown -R fred:staff /home/freddo
chmod 6640 /home/johnd/scripts/*.sh
sudo -u root ./setup.sh
cp /tmp/helloscript.sh .
cp /tmp/helloscript.sh ~fred
chown fred:staff helloscript.sh
chown fred helloscript.sh
chgrp staff helloscript.sh
chmod 750 helloscript.sh
chown :staff helloprog
chgrp staff helloprog
chmod g-r helloscript.sh
chmod go-r helloprog
mkdir /stooge /stooge/larry /stooge/moe /stooge/shemp /stooge/curly /stooge/joe; cd /stooge
cp /etc/passwd /stooge
chgrp -R stooges /stooge
chmod 710 /stooge
chmod 750 curly larry moe joe shemp
ls /stooge
chmod g+rw /stooge
chmod +t /stooge
```
icacls "C:\Program Files\TargetApp" && icacls "C:\Windows\Temp"

<!-- CORA-MAXIMIZED-COMMANDS-START -->
## Maximized Windows & Linux Command Examples for `UsersAndPermissions`

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
