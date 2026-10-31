---
title: "Trained Knowledge & Topology: Address Space Layout Randomization"
category: knowledge
domain_hub: "[[knowledge/03_windows_security_acls_auditing_and_logs]]"
os_platform: windows
primary_tactic: Defense_Evasion_Firewall
summary: "Operational architecture, decision workflows & Windows/Linux command reference for Address Space Layout Randomization: Windows Security Identifiers (Well-Known SIDs), ACE/DACL inheritance rules, icacls/cacls/takeown file permission management, audit"
when_to_apply: "Apply when working with Address Space Layout Randomization (windows): Apply when inspecting or modifying Windows file/directory/service ACLs (`icacls`/`takeown`), mapping Well-Known SIDs, configuring or auditing Windows Security audit policy (`auditpol`), querying Windows Event Logs (`wevtutil`/`Get-WinEvent`/`psloglist`), or evaluating exploit mitigations (ASLR/DEP) and local privilege escalation vectors."
tags: [enumeration, http, mdp, pdf, trained, windows, icacls, cacls, takeown, auditpol, wevtutil, psloglist, get-winevent, sid, acl, dacl, event_id, aslr, dep, privilege_escalation, defense_evasion_firewall, credential_access]
source_file: "Address Space Layout Randomization"
updated: 2026-10-30
---

# Trained Knowledge & Architecture: `Address_Space_Layout_Randomization.pdf`

- **Source Path:** `~/Projects/CORA/Training/Address_Space_Layout_Randomization.pdf` (`pdf`)
- **Extracted Technical Entities:** `http`
- **Extracted IPs / Subnets:** `None`
- **Extracted Interfaces:** `None`
- **Linked Command Playbook:** [[commands/trained_address_space_layout_randomization]] (`30` CEGAR-verified commands | `30` MDP transitions)

## Command & Tactic Coverage Summary
- **Total CEGAR-Verified Commands:** `30` (full executable list in [[commands/trained_address_space_layout_randomization]])
- **Tactic Distribution:** `Enumeration` (30)
- **Top Extracted CLI Tools:** `copy` (15), `del` (15)

## LLM Distilled Operational Summary
### Operational Techniques & Decision Workflows
*   **Target Environment**: Focus analysis on 32-bit Windows Vista RTM (Release to Manufacturing) as the baseline for measuring default ASLR behavior.
*   **Predictability Assessment**: Evaluate the effectiveness of ASLR by analyzing the randomness of memory layout shifts, specifically looking for patterns that reduce entropy.
*   **Comparative Analysis**: Contrast internal Vista RTM measurements against prior studies using beta releases (e.g., tuxedo-es.org, Rahbar) to validate implementation consistency.
*   **Entropy Verification**: Determine if consecutive execution attempts yield sufficiently distinct address spaces to hinder exploit targeting.

### Critical Command Patterns & Required Flags
*   **Measurement Tooling**: Utilize custom scripts (e.g., `ASLR.cpp`) to probe memory layout shifts across multiple runs.
*   **Re-seeding Mechanism**: Employ batch scripts (e.g., `ReSeed.bat`) to reset or manipulate the randomization seed between test iterations for accurate frequency distribution analysis.
*   **Concurrency Testing**: Execute "Runs between consecutive values" workflows to measure the delta between successive process loads.

### Network Topology & Service Relationships
*   **Service Integration**: ASLR is natively integrated into the default configuration of Windows Vista, affecting all executable services and processes by default.
*   **Vulnerability Scope**: The randomization impacts exploits targeting stack/heap overflows, format strings, and uninitialized variables, requiring attackers to predict specific memory offsets.
*   **Defense Synergy**: ASLR functions as a complementary layer to Data Execution Prevention (DEP); both must be active for maximum defense against memory manipulation.
*   **Cross-Platform Context**: While previously available in OpenBSD/Linux and third-party Windows HIPS solutions, Vista marked the first native OS-level integration.

## Extracted Operational Steps & Workflows
- 1.
E. Berger, DieHard, http://www.cs.umass.edu/~emery/diehard/.
- 2.
R. Brown, DieHarder, http://www.phy.duke.edu/~rgb/General/dieharder.php.
- 3.
I. Hellen, V. Kumar, “Security Engineering in Vista,” Sep. 2006,
- 4.
M. Howard, “Address Space Layout Randomization for Windows,” Sep. 2005,
- 5.
M. Howard, “Address Space Layout Randomization in Windows Vista,” May 2006,
- 6.
M. Howard, “Alleged Bugs in Windows Vista’s ASLR Implementation,” Oct. 2006,
- 7.
Microsoft, “Microsoft Portable Executable and Common Object File Format Specification,” May 2006,
- 8.
N. Goel, Microsoft, Private communications, Jan. 2007.
- 9.
Pageexec, “Protecting against Pointer Subterfuge (Redux),” Dailydave mailing list, Oct. 2006,
- 10. A. Rahbar, “An analysis of Microsoft Windows Vista’s ASLR,” Oct. 2006,
- 11. Security Architects, Ozone, http://www.securityarchitects.com/products.html.
- 12. H. Shacham, M. Page, B. Pfaff, E. Goh, N. Modadugu, D. Boneh, “On the Effectiveness of Address-Space
- 13. Tuxedo-es, “Microsoft Windows Vista: Measuring the security enhancements,” June 2006,
- 14. Tuxedo-es, “Microsoft Windows Vista beta-2 build 5384: Vista-Probe 0.1 results,” June 2006,
- 15. Tuxedo-es, “Vista Probe 0.1 release,” June 2006, http://www.tuxedo-es.org/blog/2026-10-25/
- 16. Tuxedo-es, “Vista Probe 0.2 release,” July 2006, http://www.tuxedo-es.org/blog/2026-10-25/
- 17. Tuxedo-es, “Vista Probe 0.2 test case sources,” http://pearls.tuxedo-es.org/win32/vista-probe-
- 18. Wehnus, “Whentrust,” http://www.wehntrust.com/.
- 19. O. Whitehouse, “Vista address space randomization data,” Feb. 2007, available via email.
- 20. Wikipedia, “Address Space Layout Randomization,”

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
