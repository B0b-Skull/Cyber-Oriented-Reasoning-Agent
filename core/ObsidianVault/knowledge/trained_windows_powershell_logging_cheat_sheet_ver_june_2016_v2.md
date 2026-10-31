---
title: "Trained Knowledge & Topology: Windows+PowerShell+Logging+Cheat+Sheet+ver+June+2016+v2"
category: knowledge
domain_hub: "[[knowledge/03_windows_security_acls_auditing_and_logs]]"
os_platform: windows
primary_tactic: Defense_Evasion_Firewall
summary: "Operational architecture, decision workflows & Windows/Linux command reference for Windows+PowerShell+Logging+Cheat+Sheet+ver+June+2016+v2: Windows Security Identifiers (Well-Known SIDs), ACE/DACL inheritance rules, icacls/cacls/takeown file permission management, audit"
when_to_apply: "Apply when working with Windows+PowerShell+Logging+Cheat+Sheet+ver+June+2016+v2 (windows): Apply when inspecting or modifying Windows file/directory/service ACLs (`icacls`/`takeown`), mapping Well-Known SIDs, configuring or auditing Windows Security audit policy (`auditpol`), querying Windows Event Logs (`wevtutil`/`Get-WinEvent`/`psloglist`), or evaluating exploit mitigations (ASLR/DEP) and local privilege escalation vectors."
tags: [auditpol, covert_exfil, credential_access, enumeration, http, https, mdp, mimikatz, out-of-band_access, passive_enum, pdf, powershell, privilege_escalation, protocol_chaining, splunk, sysinternals, trained, wevtutil, windows, icacls, cacls, takeown]
source_file: "Windows+PowerShell+Logging+Cheat+Sheet+ver+June+2016+v2"
updated: 2026-10-30
---

# Trained Knowledge & Architecture: `Windows+PowerShell+Logging+Cheat+Sheet+ver+June+2016+v2.pdf`

- **Source Path:** `~/Projects/CORA/Training/Windows+PowerShell+Logging+Cheat+Sheet+ver+June+2016+v2.pdf` (`pdf`)
- **Extracted Technical Entities:** `auditpol, http, https, mimikatz, powershell, splunk, sysinternals, wevtutil`
- **Extracted IPs / Subnets:** `None`
- **Extracted Interfaces:** `None`
- **Linked Command Playbook:** [[commands/trained_windows_powershell_logging_cheat_sheet_ver_june_2016_v2]] (`16` CEGAR-verified commands | `16` MDP transitions)

## Command & Tactic Coverage Summary
- **Total CEGAR-Verified Commands:** `16` (full executable list in [[commands/trained_windows_powershell_logging_cheat_sheet_ver_june_2016_v2]])
- **Tactic Distribution:** `Privilege_Escalation` (6), `Protocol_Chaining` (4), `Enumeration` (2), `Covert_Exfil` (1), `Credential_Access` (1), `Out-of-Band_Access` (1), `Passive_Enum` (1)
- **Top Extracted CLI Tools:** `enable-duplicatetoken` (1), `get-unattendedinstallfiles,` (1), `get-wmiobject` (1), `get-wmiobject,` (1), `invoke-allchecks,` (1), `invoke-command,` (1), `invoke-masstokens,` (1), `invoke-powershelludp,` (1), `invoke-powershellwmi,` (1), `invoke-servicestop,` (1), `invoke-wmimethod` (1), `out-word,` (1), `powershell` (1), `remove-poshrat,` (1), `restore-serviceexe,` (1), `set-executionpolicy,` (1)

## LLM Distilled Operational Summary
### Operational Techniques & Decision Workflows

*   **Assess Log Volume vs. Noise**: Before enabling detailed logging, evaluate disk space (500,000KB+ recommended for local logs) and determine if high-fidelity events like `EnableScriptBlockInvocationLogging` (Event IDs 4105/4106) are necessary, as they generate significant noise.
*   **Establish Baseline Execution Policy**: Set the default `ExecutionPolicy` to `RemoteSigned` via Group Policy or Registry to allow local scripts while requiring remote script signing.
*   **Enable Core Auditing Events**: Configure Group Policy to capture `ScriptBlock` and `ModuleLoad` details (Event ID 4104) for PowerShell 5 on Windows 7/2008+, which provides visibility into what code is running without excessive overhead.
*   **Implement Process Creation Correlation**: Enable standard "Process Creation" and "Command Line" logging to detect Execution Policy bypass attempts, which often manifest as Event ID 4688 entries showing the specific bypass command.
*   **Centralize Log Harvesting**: Route enabled local logs to a centralized SIEM or syslog solution for long-term retention and correlation, rather than relying solely on local storage.

### Critical Command Patterns & Required Flags

*   **Registry Configuration (PowerShell 5)**:
    *   `EnableModuleLogging`: Set to `1` (REG_DWORD) under `HKLM\SOFTWARE\Policies\Microsoft\Windows\PowerShell`.
    *   `EnableScriptBlockLogging`: Set to `1` (REG_DWORD) for basic command tracing.
    *   `EnableScriptBlockInvocationLogging`: Set to `1` (REG_DWORD) for deep tracing (use with caution due to noise).
    *   `EnableTranscripting`: Set to `1` (REG_DWORD) and specify `OutputDirectory` (REG_SZ) for file-based transcripts.
*   **Group Policy Settings**:
    *   Target: `Computer Configuration > Policies > Windows Settings > Security Settings > Local Policies > Security Options`.
    *   Key: "Turn on Script Block Logging" and "Turn on Module Logging".

### Network Topology & Service Relationships

*   **Service Dependency**: PowerShell logging relies on the **Windows Management Framework (WMF)** and the **.NET Framework** APIs. Attackers exploit these same APIs to bypass traditional AV controls.
*   **Log Event IDs**:
    *   **Event ID 4104**: PowerShell Script Block Logging (Core visibility).
    *   **Event ID 4105/4106**: PowerShell Script Block Invocation Logging (High-fidelity, noisy).
    *   **Event ID 4688**: Process Creation (Critical for detecting Execution Policy bypasses via command line arguments).
*   **Common Exploitation Tools**: Monitor logs for activity from tools like **PowerSploit**, **PowerShell Empire**, **MetaSploit**, and **SET** which often utilize WMF commands to execute with minimal local footprint.

## Extracted Operational Steps & Workflows
- 1. Why Enable and Configure PowerShell logging?  PowerShell, or its new official name, the “Windows Management
- 1. LOCAL LOG SIZE:  Increase the size of your local PowerShell logs.  Don’t worry, you have plenty of disk space, CPU is not
- 2. LOCAL SECURITY POLICY:  No settings needed
- 3. GROUP POLICY:  You can control all the PowerShell settings in Group Policy
- 4. REGISTRY SETTINGS:
- 1. The ability to bypass your PowerShell controls is a concern and why it is crucial to alert on these bypass attempts as an indication
- 2. Execution Policy Bypass:  The Execution Policy that you set can be bypassed by anyone with malicious intent.  Alert on
- 3. Profile Bypass:  The profile(s) you set to configure PowerShell when each session is launched can also be bypassed.
- 4. These commands are often joined in malicious activity and can be in any form of the following:
- 1. PowerShell Transcript:  For PowerShell versions 2, 3, 4 & 5.  You can record a PowerShell transcript of everything
- 2. You may also Start and Stop the transcripts as needed within your scripts with Start-Transcript or Stop-Transcript
- 1. WEvtUtil:  Use this utility to configure your log settings or configure them in Group Policy
- 2. For more history in your logs, consider making the log size 1GB
- 1. Default Profile:  In order to capture the command line of a Windows PowerShell session for all users on the system,
- 1. Reg.exe:  Use this utility to query the registry and check the settings
- 1. REGISTRY AUDIT:  To help you catch malicious activity trying to alter your PowerShell configuration, audit the
- 2. POWERSHELL KEYS TO AUDIT:
- 1. PowerShell Versions and OS:  The ability to perform advanced logging of PowerShell is limited to certain operating
- 1. LOG CLEAR:  Watch for log clear messages
- 1. PROCESSES:  Watch for a Process to start and call
- 1. REGISTRY:  Monitor certain Keys for Add, Changes and
- 1. WEvtUtil:  Use this utility to query your logs
- 2. Filtering Log Results:  Use this method to filter lines within the logs
- 3. For PowerShell 4 and 5 Event ID 4104.  These logs are large in content
- 4. Get-EventLog:  Use this PowerShell module to query your logs.  There too many options to list here, but here a
- 1. FIREWALL:  Windows Filtering Platform - Watch for Inbound and Outbound connections – Requires Windows Firewall to be
- 1. Monitor for these Dll’s being called by an executable other than PowerShell.exe or PowerShell_ISE.exe
- 2. Monitor for calls to WMI, they are not necessarily malicious, but could indicate WMI is being used in an attack
- 3. In order to detect PowerShell DLL’s being called by something other than PowerShell.exe or PowerShell_ISE.exe, you should
- 1. PROFILES:  Locations that profile.ps1 can be stored should be monitored for new profiles or changes since these can be
- 1. POWERSHELL  MODULES:  The following is a list of PowerShell module calls that you should monitor for executing using

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
