---
title: "Trained Knowledge & Topology: AuditPol CMDs"
category: knowledge
domain_hub: "[[knowledge/03_windows_security_acls_auditing_and_logs]]"
os_platform: windows
primary_tactic: Defense_Evasion_Firewall
summary: "Operational architecture, decision workflows & Windows/Linux command reference for AuditPol CMDs: Windows Security Identifiers (Well-Known SIDs), ACE/DACL inheritance rules, icacls/cacls/takeown file permission management, audit"
when_to_apply: "Apply when working with AuditPol CMDs (windows): Apply when inspecting or modifying Windows file/directory/service ACLs (`icacls`/`takeown`), mapping Well-Known SIDs, configuring or auditing Windows Security audit policy (`auditpol`), querying Windows Event Logs (`wevtutil`/`Get-WinEvent`/`psloglist`), or evaluating exploit mitigations (ASLR/DEP) and local privilege escalation vectors."
tags: [auditpol, credential_access, defense_evasion_firewall, kerberos, mdp, passive_enum, text, trained, wevtutil, wmic, windows, icacls, cacls, takeown, psloglist, get-winevent, sid, acl, dacl, event_id, aslr, dep]
source_file: "AuditPol CMDs"
updated: 2026-10-30
---

# Trained Knowledge & Architecture: `AuditPol CMDs.txt`

- **Source Path:** `~/Projects/CORA/Training/AuditPol CMDs.txt` (`text`)
- **Extracted Technical Entities:** `auditpol, kerberos, wevtutil, wmic`
- **Extracted IPs / Subnets:** `None`
- **Extracted Interfaces:** `None`
- **Linked Command Playbook:** [[commands/trained_auditpol_cmds]] (`30` CEGAR-verified commands | `30` MDP transitions)

## Command & Tactic Coverage Summary
- **Total CEGAR-Verified Commands:** `30` (full executable list in [[commands/trained_auditpol_cmds]])
- **Tactic Distribution:** `Defense_Evasion_Firewall` (23), `Passive_Enum` (6), `Credential_Access` (1)
- **Top Extracted CLI Tools:** `auditpol` (23), `psloglist` (4), `wmic` (2), `wevtutil` (1)

## LLM Distilled Operational Summary
### Key Operational Techniques & Decision Workflows

*   **Log Retrieval & Filtering**: Use `psloglist` with specific flags (`-s`, `-t`, `-n`) to retrieve and format the last N security log entries. Combine with `findstr` to filter for specific keywords like "SID" or "Administrators" to identify privilege escalation events.
*   **Policy Verification**: Use `auditpol /list` commands to verify current audit configurations across categories, subcategories, and specific user accounts before or after changes.
*   **Policy Enforcement**: Apply `auditpol /set` commands to enable or disable auditing for specific subcategories (e.g., "User Account Management", "Sensitive Privilege Use") with defined success/failure triggers.
*   **Event Log Inspection**: Query the Windows Event Log using `wevtutil qe` to retrieve recent text-formatted logs from the System category for immediate analysis.
*   **User-to-SID Mapping**: Utilize `wmic useraccount` queries to retrieve Security Identifiers (SIDs) associated with specific usernames across different OS versions (Windows 7/XP).

### Critical Command Patterns and Required Flags

| Command Pattern | Purpose | Key Flags/Parameters |
| :--- | :--- | :--- |
| `psloglist -n <count>` | Retrieve last N log entries. | `-n`: Limit count (e.g., `-n 10`). |
| `psloglist -s -t "\t" -n <count> Security` | Format and filter Security logs. | `-s`: Show SID; `-t "\t"`: Tab delimiter; `-n`: Count. |
| `auditpol /list /category` | List audit categories. | `/category`: Scope to categories. |
| `auditpol /set /subcategory:"Name" /success:enable` | Enable auditing for a subcategory. | `/subcategory`: Target name; `/success:enable` or `/failure:enable`. |
| `wevtutil qe System /c:10 /f:text` | Query Event Log. | `/c`: Count; `/f:text`: Text format. |
| `wmic useraccount where name='X' get sid` | Get User SID. | `where name='X'`: Filter by username; `get sid`: Output SID. |

### Network Topology & Service Relationships

*   **Security Subcategory Dependencies**: Auditing is granularly configured per subcategory within the "Security" category. Key relationships include:
    *   **User Account Management**: Tracks creation, deletion, and privilege changes (e.g., adding users to Administrators).
    *   **Sensitive Privilege Use**: Monitors usage of high-privilege tokens.
    *   **Kerberos Services**: Includes "Service Ticket Operations" and "Authentication Service" for identity verification tracking.
    *   **File & Network**: Covers "File Share" and "Network Policy Server" for access control monitoring.
*   **OS-Specific Behavior**: Command syntax for SID retrieval varies slightly between Windows 7 (`get sid` required) and Windows XP (implicit in `get` output).

<!-- CORA-MAXIMIZED-COMMANDS-START -->
## Maximized Windows & Linux Command Examples for `AuditPol CMDs`

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
