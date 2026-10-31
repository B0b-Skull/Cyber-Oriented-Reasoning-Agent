---
title: "Trained Command Playbook: CQC001 E030 M020 transcript"
category: commands
domain_hub: "[[knowledge/03_windows_security_acls_auditing_and_logs]]"
os_platform: windows
primary_tactic: Defense_Evasion_Firewall
summary: "Verified Windows & Linux command playbook for CQC001 E030 M020 transcript (Defense_Evasion_Firewall): Windows Security Identifiers (Well-Known SIDs), ACE/DACL inheritance rules, icacls/cacls/takeown file permission management, auditpol s"
when_to_apply: "Apply when working with CQC001 E030 M020 transcript (windows): Apply when inspecting or modifying Windows file/directory/service ACLs (`icacls`/`takeown`), mapping Well-Known SIDs, configuring or auditing Windows Security audit policy (`auditpol`), querying Windows Event Logs (`wevtutil`/`Get-WinEvent`/`psloglist`), or evaluating exploit mitigations (ASLR/DEP) and local privilege escalation vectors."
tags: [active_enum, credential_access, dsquery, enumeration, mdp, passive_enum, pdf, privilege_escalation, trained, windows, icacls, cacls, takeown, auditpol, wevtutil, psloglist, get-winevent, sid, acl, dacl, event_id, aslr]
source_file: "CQC001 E030 M020 transcript"
updated: 2026-10-30
---

icacls "C:\Program Files\TargetApp" && icacls "C:\Windows\Temp"
# Trained Command Playbook: `CQC001_E030_M020_transcript.pdf`
icacls "C:\Program Files\TargetApp" && icacls "C:\Windows\Temp"
- **Source Document:** `~/Projects/CORA/Training/CQC001_E030_M020_transcript.pdf`
- **CEGAR Verified Commands:** `38` (`0` malformed/unsafe snippets filtered)
- **MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`):** `38`
- **Discovered IPs/Subnets:** `None`
- **Discovered Interfaces:** `None`
- **Related Knowledge Note:** [[knowledge/trained_cqc001_e030_m020_transcript]]
icacls "C:\Program Files\TargetApp" && icacls "C:\Windows\Temp"
## Distilled MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`)
| Pre-State ($s$) | Tactic ($\tau$) | Technique ($k$) | Tool ($u$) | Post-State ($s'$) | Verified Command ($c$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `ldifde` | `s_credentials_or_certs_acquired` | `LDIFDE.exe (LDAP Data Interchange Format (LDIF) Data Exchange tool)` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `csvde` | `s_passive_topology_mapped` | `CSVDE cannot be used to modify or delete objects.` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `dsadd` | `s_active_services_enumerated` | `DSADD COMPUTER: Adds a computer to the directory` |
| `s_passive_topology_mapped` | **`Active_Enum`** | Active Network, Cloud, Directory Service & Endpoint Probing | `dsget` | `s_active_services_enumerated` | `DSGET COMPUTER: Displays properties of computers in the directory` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `dsmod` | `s_interactive_tty_or_priv_escalated` | `DSMOD GROUP: Modifies an existing group in the directory` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `csvde` | `s_credentials_or_certs_acquired` | `CSVDE.exe (Comma Separated Value Data Export tool)` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `dsadd` | `s_active_services_enumerated` | `DSADD CONTACT: Adds a contact to the directory` |
| `s_passive_topology_mapped` | **`Active_Enum`** | Active Network, Cloud, Directory Service & Endpoint Probing | `dsget` | `s_active_services_enumerated` | `DSGET CONTACT: Displays properties of contacts in the directory` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `dsadd` | `s_credentials_or_certs_acquired` | `DSADD USER: Adds a user to the directory` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `dsadd` | `s_active_services_enumerated` | `DSADD GROUP: Adds a group to the directory` |
| `s_passive_topology_mapped` | **`Active_Enum`** | Active Network, Cloud, Directory Service & Endpoint Probing | `dsget` | `s_active_services_enumerated` | `DSGET SUBNET: Displays properties of subnets in the directory` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `dsmod` | `s_credentials_or_certs_acquired` | `DSMOD USER: Modifies an existing user in the directory` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `dsadd` | `s_active_services_enumerated` | `DSADD OU: Adds an organizational unit to the directory` |
| `s_passive_topology_mapped` | **`Active_Enum`** | Active Network, Cloud, Directory Service & Endpoint Probing | `dsget` | `s_active_services_enumerated` | `DSGET GROUP: Displays properties of groups in the directory` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `dsadd` | `s_active_services_enumerated` | `DSADD QUOTA: Adds a quota specification to a directory partition` |
| `s_passive_topology_mapped` | **`Active_Enum`** | Active Network, Cloud, Directory Service & Endpoint Probing | `dsget` | `s_active_services_enumerated` | `DSGET OU: Displays properties of organizational units in the directory` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `dsmod` | `s_active_services_enumerated` | `DSMOD COMPUTER: Modifies an existing computer in the directory` |
| `s_passive_topology_mapped` | **`Active_Enum`** | Active Network, Cloud, Directory Service & Endpoint Probing | `dsget` | `s_active_services_enumerated` | `DSGET SERVER: Displays properties of servers in the directory` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `dsmod` | `s_active_services_enumerated` | `DSMOD CONTACT: Modifies an existing contact in the directory` |
| `s_passive_topology_mapped` | **`Active_Enum`** | Active Network, Cloud, Directory Service & Endpoint Probing | `dsget` | `s_active_services_enumerated` | `DSGET SITE: Displays properties of sites in the directory` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `dsmod` | `s_active_services_enumerated` | `DSMOD OU: Modifies an existing organizational unit in the directory` |
| `s_passive_topology_mapped` | **`Active_Enum`** | Active Network, Cloud, Directory Service & Endpoint Probing | `dsget` | `s_active_services_enumerated` | `DSGET USER: Displays properties of users in the directory` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `dsmod` | `s_active_services_enumerated` | `DSMOD SERVER: Modifies an existing domain controller in the directory` |
| `s_passive_topology_mapped` | **`Active_Enum`** | Active Network, Cloud, Directory Service & Endpoint Probing | `dsget` | `s_active_services_enumerated` | `DSGET QUOTA: Displays properties of quotas in the directory` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `dsmod` | `s_active_services_enumerated` | `DSMOD QUOTA: Modifies an existing quota specification in the directory` |
| `s_passive_topology_mapped` | **`Active_Enum`** | Active Network, Cloud, Directory Service & Endpoint Probing | `dsget` | `s_active_services_enumerated` | `DSGET PARTITION: Displays properties of partitions in the directory` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `dsmod` | `s_active_services_enumerated` | `DSMOD PARTITION: Modifies attributes of one or more existing partitions in the directory` |
| `s_passive_topology_mapped` | **`Active_Enum`** | Active Network, Cloud, Directory Service & Endpoint Probing | `dsquery` | `s_active_services_enumerated` | `DSQUERY COMPUTER: Finds computers in the directory` |
| `s_passive_topology_mapped` | **`Active_Enum`** | Active Network, Cloud, Directory Service & Endpoint Probing | `dsquery` | `s_active_services_enumerated` | `DSQUERY CONTACT: Finds contacts in the directory` |
| `s_passive_topology_mapped` | **`Active_Enum`** | Active Network, Cloud, Directory Service & Endpoint Probing | `dsquery` | `s_active_services_enumerated` | `DSQUERY SUBNET: Finds subnets in the directory` |
| `s_passive_topology_mapped` | **`Active_Enum`** | Active Network, Cloud, Directory Service & Endpoint Probing | `dsquery` | `s_active_services_enumerated` | `DSQUERY GROUP: Finds groups in the directory` |
| `s_passive_topology_mapped` | **`Active_Enum`** | Active Network, Cloud, Directory Service & Endpoint Probing | `dsquery` | `s_active_services_enumerated` | `DSQUERY OU: Finds organizational units in the directory` |
| `s_passive_topology_mapped` | **`Active_Enum`** | Active Network, Cloud, Directory Service & Endpoint Probing | `dsquery` | `s_active_services_enumerated` | `DSQUERY SITE: Finds sites in the directory` |
| `s_passive_topology_mapped` | **`Active_Enum`** | Active Network, Cloud, Directory Service & Endpoint Probing | `dsquery` | `s_active_services_enumerated` | `DSQUERY SERVER: Finds domain controllers in the directory` |
| `s_passive_topology_mapped` | **`Active_Enum`** | Active Network, Cloud, Directory Service & Endpoint Probing | `dsquery` | `s_active_services_enumerated` | `DSQUERY USER: Finds users in the directory` |
| `s_passive_topology_mapped` | **`Active_Enum`** | Active Network, Cloud, Directory Service & Endpoint Probing | `dsquery` | `s_active_services_enumerated` | `DSQUERY QUOTA: Finds quota specifications in the directory` |
| `s_passive_topology_mapped` | **`Active_Enum`** | Active Network, Cloud, Directory Service & Endpoint Probing | `dsquery` | `s_active_services_enumerated` | `DSQUERY PARTITION: Finds partitions in the directory` |
| `s_passive_topology_mapped` | **`Active_Enum`** | Active Network, Cloud, Directory Service & Endpoint Probing | `dsquery` | `s_active_services_enumerated` | `DSQUERY *: Finds any object in the directory by using a generic LDAP query` |
icacls "C:\Program Files\TargetApp" && icacls "C:\Windows\Temp"
## Verified Executable Commands (Grouped by Capability Layer)
icacls "C:\Program Files\TargetApp" && icacls "C:\Windows\Temp"
### General_System (38 commands)
```bash
LDIFDE.exe (LDAP Data Interchange Format (LDIF) Data Exchange tool)
CSVDE.exe (Comma Separated Value Data Export tool)
CSVDE cannot be used to modify or delete objects.
DSADD COMPUTER: Adds a computer to the directory
DSADD CONTACT: Adds a contact to the directory
DSADD GROUP: Adds a group to the directory
DSADD OU: Adds an organizational unit to the directory
DSADD USER: Adds a user to the directory
DSADD QUOTA: Adds a quota specification to a directory partition
DSGET COMPUTER: Displays properties of computers in the directory
DSGET CONTACT: Displays properties of contacts in the directory
DSGET SUBNET: Displays properties of subnets in the directory
DSGET GROUP: Displays properties of groups in the directory
DSGET OU: Displays properties of organizational units in the directory
DSGET SERVER: Displays properties of servers in the directory
DSGET SITE: Displays properties of sites in the directory
DSGET USER: Displays properties of users in the directory
DSGET QUOTA: Displays properties of quotas in the directory
DSGET PARTITION: Displays properties of partitions in the directory
DSMOD COMPUTER: Modifies an existing computer in the directory
DSMOD CONTACT: Modifies an existing contact in the directory
DSMOD GROUP: Modifies an existing group in the directory
DSMOD OU: Modifies an existing organizational unit in the directory
DSMOD SERVER: Modifies an existing domain controller in the directory
DSMOD USER: Modifies an existing user in the directory
DSMOD QUOTA: Modifies an existing quota specification in the directory
DSMOD PARTITION: Modifies attributes of one or more existing partitions in the directory
DSQUERY COMPUTER: Finds computers in the directory
DSQUERY CONTACT: Finds contacts in the directory
DSQUERY SUBNET: Finds subnets in the directory
DSQUERY GROUP: Finds groups in the directory
DSQUERY OU: Finds organizational units in the directory
DSQUERY SITE: Finds sites in the directory
DSQUERY SERVER: Finds domain controllers in the directory
DSQUERY USER: Finds users in the directory
DSQUERY QUOTA: Finds quota specifications in the directory
DSQUERY PARTITION: Finds partitions in the directory
DSQUERY *: Finds any object in the directory by using a generic LDAP query
```
icacls "C:\Program Files\TargetApp" && icacls "C:\Windows\Temp"

<!-- CORA-MAXIMIZED-COMMANDS-START -->
## Maximized Windows & Linux Command Examples for `CQC001 E030 M020 transcript`

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
