---
title: "Trained Command Playbook: Address Space Layout Randomization"
category: commands
domain_hub: "[[knowledge/03_windows_security_acls_auditing_and_logs]]"
os_platform: windows
primary_tactic: Defense_Evasion_Firewall
summary: "Verified Windows & Linux command playbook for Address Space Layout Randomization (Defense_Evasion_Firewall): Windows Security Identifiers (Well-Known SIDs), ACE/DACL inheritance rules, icacls/cacls/takeown file permission management, auditpol s"
when_to_apply: "Apply when working with Address Space Layout Randomization (windows): Apply when inspecting or modifying Windows file/directory/service ACLs (`icacls`/`takeown`), mapping Well-Known SIDs, configuring or auditing Windows Security audit policy (`auditpol`), querying Windows Event Logs (`wevtutil`/`Get-WinEvent`/`psloglist`), or evaluating exploit mitigations (ASLR/DEP) and local privilege escalation vectors."
tags: [enumeration, http, mdp, pdf, trained, windows, icacls, cacls, takeown, auditpol, wevtutil, psloglist, get-winevent, sid, acl, dacl, event_id, aslr, dep, privilege_escalation, defense_evasion_firewall, credential_access]
source_file: "Address Space Layout Randomization"
updated: 2026-10-30
---

icacls "C:\Program Files\TargetApp" && icacls "C:\Windows\Temp"
# Trained Command Playbook: `Address_Space_Layout_Randomization.pdf`
icacls "C:\Program Files\TargetApp" && icacls "C:\Windows\Temp"
- **Source Document:** `~/Projects/CORA/Training/Address_Space_Layout_Randomization.pdf`
- **CEGAR Verified Commands:** `30` (`0` malformed/unsafe snippets filtered)
- **MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`):** `30`
- **Discovered IPs/Subnets:** `None`
- **Discovered Interfaces:** `None`
- **Related Knowledge Note:** [[knowledge/trained_address_space_layout_randomization]]
icacls "C:\Program Files\TargetApp" && icacls "C:\Windows\Temp"
## Distilled MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`)
| Pre-State ($s$) | Tactic ($\tau$) | Technique ($k$) | Tool ($u$) | Post-State ($s'$) | Verified Command ($c$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `copy` | `s_active_services_enumerated` | `Copy /Y ASLR.exe ASLR-1.exe` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `copy` | `s_active_services_enumerated` | `Copy /Y ASLR.exe ASLR-2.exe` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `copy` | `s_active_services_enumerated` | `Copy /Y ASLR.exe ASLR-3.exe` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `copy` | `s_active_services_enumerated` | `Copy /Y ASLR.exe ASLR-4.exe` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `copy` | `s_active_services_enumerated` | `Copy /Y ASLR.exe ASLR-5.exe` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `copy` | `s_active_services_enumerated` | `Copy /Y ASLR.exe ASLR-6.exe` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `copy` | `s_active_services_enumerated` | `Copy /Y ASLR.exe ASLR-7.exe` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `copy` | `s_active_services_enumerated` | `Copy /Y ASLR.exe ASLR-8.exe` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `copy` | `s_active_services_enumerated` | `Copy /Y ASLR.exe ASLR-9.exe` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `copy` | `s_active_services_enumerated` | `Copy /Y ASLR.exe ASLR-A.exe` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `copy` | `s_active_services_enumerated` | `Copy /Y ASLR.exe ASLR-B.exe` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `copy` | `s_active_services_enumerated` | `Copy /Y ASLR.exe ASLR-C.exe` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `copy` | `s_active_services_enumerated` | `Copy /Y ASLR.exe ASLR-D.exe` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `copy` | `s_active_services_enumerated` | `Copy /Y ASLR.exe ASLR-E.exe` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `copy` | `s_active_services_enumerated` | `Copy /Y ASLR.exe ASLR-F.exe` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `del` | `s_active_services_enumerated` | `Del ASLR-1.exe` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `del` | `s_active_services_enumerated` | `Del ASLR-2.exe` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `del` | `s_active_services_enumerated` | `Del ASLR-3.exe` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `del` | `s_active_services_enumerated` | `Del ASLR-4.exe` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `del` | `s_active_services_enumerated` | `Del ASLR-5.exe` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `del` | `s_active_services_enumerated` | `Del ASLR-6.exe` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `del` | `s_active_services_enumerated` | `Del ASLR-7.exe` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `del` | `s_active_services_enumerated` | `Del ASLR-8.exe` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `del` | `s_active_services_enumerated` | `Del ASLR-9.exe` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `del` | `s_active_services_enumerated` | `Del ASLR-A.exe` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `del` | `s_active_services_enumerated` | `Del ASLR-B.exe` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `del` | `s_active_services_enumerated` | `Del ASLR-C.exe` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `del` | `s_active_services_enumerated` | `Del ASLR-D.exe` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `del` | `s_active_services_enumerated` | `Del ASLR-E.exe` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `del` | `s_active_services_enumerated` | `Del ASLR-F.exe` |
icacls "C:\Program Files\TargetApp" && icacls "C:\Windows\Temp"
## Verified Executable Commands (Grouped by Capability Layer)
icacls "C:\Program Files\TargetApp" && icacls "C:\Windows\Temp"
### General_System (30 commands)
```bash
Copy /Y ASLR.exe ASLR-1.exe
Copy /Y ASLR.exe ASLR-2.exe
Copy /Y ASLR.exe ASLR-3.exe
Copy /Y ASLR.exe ASLR-4.exe
Copy /Y ASLR.exe ASLR-5.exe
Copy /Y ASLR.exe ASLR-6.exe
Copy /Y ASLR.exe ASLR-7.exe
Copy /Y ASLR.exe ASLR-8.exe
Copy /Y ASLR.exe ASLR-9.exe
Copy /Y ASLR.exe ASLR-A.exe
Copy /Y ASLR.exe ASLR-B.exe
Copy /Y ASLR.exe ASLR-C.exe
Copy /Y ASLR.exe ASLR-D.exe
Copy /Y ASLR.exe ASLR-E.exe
Copy /Y ASLR.exe ASLR-F.exe
Del ASLR-1.exe
Del ASLR-2.exe
Del ASLR-3.exe
Del ASLR-4.exe
Del ASLR-5.exe
Del ASLR-6.exe
Del ASLR-7.exe
Del ASLR-8.exe
Del ASLR-9.exe
Del ASLR-A.exe
Del ASLR-B.exe
Del ASLR-C.exe
Del ASLR-D.exe
Del ASLR-E.exe
Del ASLR-F.exe
```
icacls "C:\Program Files\TargetApp" && icacls "C:\Windows\Temp"

<!-- CORA-MAXIMIZED-COMMANDS-START -->
## Maximized Windows & Linux Command Examples for `Address Space Layout Randomization`

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
