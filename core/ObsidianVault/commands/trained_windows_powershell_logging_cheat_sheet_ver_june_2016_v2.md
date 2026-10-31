---
title: "Trained Command Playbook: Windows+PowerShell+Logging+Cheat+Sheet+ver+June+2016+v2"
category: commands
domain_hub: "[[knowledge/03_windows_security_acls_auditing_and_logs]]"
os_platform: windows
primary_tactic: Defense_Evasion_Firewall
summary: "Verified Windows & Linux command playbook for Windows+PowerShell+Logging+Cheat+Sheet+ver+June+2016+v2 (Defense_Evasion_Firewall): Windows Security Identifiers (Well-Known SIDs), ACE/DACL inheritance rules, icacls/cacls/takeown file permission management, auditpol s"
when_to_apply: "Apply when working with Windows+PowerShell+Logging+Cheat+Sheet+ver+June+2016+v2 (windows): Apply when inspecting or modifying Windows file/directory/service ACLs (`icacls`/`takeown`), mapping Well-Known SIDs, configuring or auditing Windows Security audit policy (`auditpol`), querying Windows Event Logs (`wevtutil`/`Get-WinEvent`/`psloglist`), or evaluating exploit mitigations (ASLR/DEP) and local privilege escalation vectors."
tags: [auditpol, covert_exfil, credential_access, enumeration, http, https, mdp, mimikatz, out-of-band_access, passive_enum, pdf, powershell, privilege_escalation, protocol_chaining, splunk, sysinternals, trained, wevtutil, windows, icacls, cacls, takeown]
source_file: "Windows+PowerShell+Logging+Cheat+Sheet+ver+June+2016+v2"
updated: 2026-10-30
---

icacls "C:\Program Files\TargetApp" && icacls "C:\Windows\Temp"
# Trained Command Playbook: `Windows+PowerShell+Logging+Cheat+Sheet+ver+June+2016+v2.pdf`
icacls "C:\Program Files\TargetApp" && icacls "C:\Windows\Temp"
- **Source Document:** `~/Projects/CORA/Training/Windows+PowerShell+Logging+Cheat+Sheet+ver+June+2016+v2.pdf`
- **CEGAR Verified Commands:** `16` (`0` malformed/unsafe snippets filtered)
- **MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`):** `16`
- **Discovered IPs/Subnets:** `None`
- **Discovered Interfaces:** `None`
- **Related Knowledge Note:** [[knowledge/trained_windows_powershell_logging_cheat_sheet_ver_june_2016_v2]]
icacls "C:\Program Files\TargetApp" && icacls "C:\Windows\Temp"
## Distilled MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`)
| Pre-State ($s$) | Tactic ($\tau$) | Technique ($k$) | Tool ($u$) | Post-State ($s'$) | Verified Command ($c$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `powershell` | `s_active_services_enumerated` | `powershell.exe -e ZQBjAGgAbwAgACcAWQBvAHUAIABhAHIAZQAgAHAAdwBuAGUAZAAhACcA     (encoded)` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `get-wmiobject` | `s_passive_topology_mapped` | `Get-WMIObject` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `set-executionpolicy,` | `s_interactive_tty_or_priv_escalated` | `Set-ExecutionPolicy, Set-MasterBootRecord` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `invoke-command,` | `s_credentials_or_certs_acquired` | `Invoke-Command, Invoke-Expression, iex, Invoke-Shellcode, Invoke--Shellcode, Invoke-ShellcodeMSIL, Invoke-` |
| `s_credentials_or_certs_acquired` | **`Protocol_Chaining`** | Multi-Protocol Handshake & Tunnel Relay Chaining | `invoke-powershelludp,` | `s_protocol_chain_established` | `Invoke-PowerShellUdp, Invoke-PsGcatAgent, Invoke-PoshRatHttps, Invoke-PowerShellTcp, Invoke-PoshRatHttp,` |
| `s_l2_l3_verified` | **`Out-of-Band_Access`** | UART/Serial Console Out-of-Band Enumeration & Control | `enable-duplicatetoken` | `s_oob_serial_enumerated` | `Enable-DuplicateToken , Remove-Update, Execute-DNSTXT-Code, Download-Execute-PS, Execute-Command-` |
| `s_interactive_tty_or_priv_escalated` | **`Covert_Exfil`** | Encapsulated / Low-Signature Data Telemetry Transfer | `remove-poshrat,` | `s_covert_exfil_verified` | `Remove-PoshRat, TexttoEXE, Base64ToString, StringtoBase64, Do-Exfiltration, Parse_Keys, Add-Exfiltration, Add-` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `invoke-wmimethod` | `s_active_services_enumerated` | `Invoke-WMIMethod` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `get-wmiobject,` | `s_interactive_tty_or_priv_escalated` | `Get-WMIObject, Get-GPPPassword, Get-Keystrokes, Get-TimedScreenshot, Get-VaultCredential, Get-` |
| `s_credentials_or_certs_acquired` | **`Protocol_Chaining`** | Multi-Protocol Handshake & Tunnel Relay Chaining | `invoke-powershellwmi,` | `s_protocol_chain_established` | `Invoke-PowerShellWmi, Invoke-PSGcat, Invoke-Encode, Invoke-Decode, Invoke-CreateCertificate, Invoke-` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `get-unattendedinstallfiles,` | `s_interactive_tty_or_priv_escalated` | `Get-UnattendedInstallFiles, Get-Webconfig, Get-ApplicationHost, Get-PassHashes, Get-LsaSecret, Get-` |
| `s_credentials_or_certs_acquired` | **`Protocol_Chaining`** | Multi-Protocol Handshake & Tunnel Relay Chaining | `out-word,` | `s_protocol_chain_established` | `Out-Word, Out-Excel, Out-Java, Out-Shortcut, Out-CHM, Out-HTA, Out-Minidump, HTTP-Backdoor, Find-` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `invoke-servicestop,` | `s_interactive_tty_or_priv_escalated` | `Invoke-ServiceStop, Invoke-ServiceEnable, Invoke-ServiceDisable, Invoke-FindDLLHijack, Invoke-FindPathHijack,` |
| `s_credentials_or_certs_acquired` | **`Protocol_Chaining`** | Multi-Protocol Handshake & Tunnel Relay Chaining | `restore-serviceexe,` | `s_protocol_chain_established` | `Restore-ServiceEXE,  Add-ScrnSaveBackdoor, Gupt-Backdoor, Execute-OnTime, DNS_TXT_Pwnage, Write-` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `invoke-allchecks,` | `s_interactive_tty_or_priv_escalated` | `Invoke-AllChecks, Invoke-MassCommand, Invoke-MassMimikatz, Invoke-MassSearch, Invoke-MassTemplate,` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `invoke-masstokens,` | `s_interactive_tty_or_priv_escalated` | `Invoke-MassTokens, Invoke-ADSBackdoor, Invoke-CredentialsPhish, Invoke-BruteForce, Invoke-PowerShellIcmp,` |
icacls "C:\Program Files\TargetApp" && icacls "C:\Windows\Temp"
## Verified Executable Commands (Grouped by Capability Layer)
icacls "C:\Program Files\TargetApp" && icacls "C:\Windows\Temp"
### General_System (16 commands)
```bash
powershell.exe -e ZQBjAGgAbwAgACcAWQBvAHUAIABhAHIAZQAgAHAAdwBuAGUAZAAhACcA     (encoded)
Invoke-WMIMethod
Get-WMIObject
Set-ExecutionPolicy, Set-MasterBootRecord
Get-WMIObject, Get-GPPPassword, Get-Keystrokes, Get-TimedScreenshot, Get-VaultCredential, Get-
Get-UnattendedInstallFiles, Get-Webconfig, Get-ApplicationHost, Get-PassHashes, Get-LsaSecret, Get-
Invoke-Command, Invoke-Expression, iex, Invoke-Shellcode, Invoke--Shellcode, Invoke-ShellcodeMSIL, Invoke-
Invoke-ServiceStop, Invoke-ServiceEnable, Invoke-ServiceDisable, Invoke-FindDLLHijack, Invoke-FindPathHijack,
Invoke-AllChecks, Invoke-MassCommand, Invoke-MassMimikatz, Invoke-MassSearch, Invoke-MassTemplate,
Invoke-MassTokens, Invoke-ADSBackdoor, Invoke-CredentialsPhish, Invoke-BruteForce, Invoke-PowerShellIcmp,
Invoke-PowerShellUdp, Invoke-PsGcatAgent, Invoke-PoshRatHttps, Invoke-PowerShellTcp, Invoke-PoshRatHttp,
Invoke-PowerShellWmi, Invoke-PSGcat, Invoke-Encode, Invoke-Decode, Invoke-CreateCertificate, Invoke-
Out-Word, Out-Excel, Out-Java, Out-Shortcut, Out-CHM, Out-HTA, Out-Minidump, HTTP-Backdoor, Find-
Restore-ServiceEXE,  Add-ScrnSaveBackdoor, Gupt-Backdoor, Execute-OnTime, DNS_TXT_Pwnage, Write-
Enable-DuplicateToken , Remove-Update, Execute-DNSTXT-Code, Download-Execute-PS, Execute-Command-
Remove-PoshRat, TexttoEXE, Base64ToString, StringtoBase64, Do-Exfiltration, Parse_Keys, Add-Exfiltration, Add-
```
icacls "C:\Program Files\TargetApp" && icacls "C:\Windows\Temp"

<!-- CORA-MAXIMIZED-COMMANDS-START -->
## Maximized Windows & Linux Command Examples for `Windows+PowerShell+Logging+Cheat+Sheet+ver+June+2016+v2`

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
