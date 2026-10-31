---
title: "Trained Command Playbook: Cyber Forensics Intro Guide updated table"
category: commands
domain_hub: "[[knowledge/10_digital_forensics_pe_reversing_and_threat_intel]]"
os_platform: cross-platform
primary_tactic: Passive_Enum
summary: "Verified Windows & Linux command playbook for Cyber Forensics Intro Guide updated table (Passive_Enum): Digital forensics workflows (Autopsy, EnCase, SleuthKit), NTFS Master File Table ($MFT), Alternate Data Streams (ADS), file/RAM slack s"
when_to_apply: "Apply when working with Cyber Forensics Intro Guide updated table (cross-platform): Apply when performing disk/image forensics (Autopsy, EnCase, SleuthKit), analyzing NTFS `$MFT` records, Alternate Data Streams (`dir /r`), or slack space, reverse-engineering Windows PE (`.exe`/`.dll`/`.sys`) or Linux ELF binaries, or hunting APT28 / Fancy Bear IOCs and TTPs."
tags: [active_enum, arp, credential_access, defense_evasion_firewall, enumeration, http, https, iptables, john, kerberos, mdp, netstat, nmap, passive_enum, pdf, powershell, privilege_escalation, pslist, responder, serial, trained, windows]
source_file: "Cyber Forensics Intro Guide updated table"
updated: 2026-10-30
---

powershell -NoProfile -Command "Get-FileHash -Algorithm SHA256 C:\Suspicious\*.exe,C:\Suspicious\*.dll" && sigcheck -accepteula -h -vr C:\Suspicious
# Trained Command Playbook: `Cyber Forensics Intro Guide_updated_table.pdf`
powershell -NoProfile -Command "Get-FileHash -Algorithm SHA256 C:\Suspicious\*.exe,C:\Suspicious\*.dll" && sigcheck -accepteula -h -vr C:\Suspicious
- **Source Document:** `~/Projects/CORA/Training/Cyber Forensics Intro Guide_updated_table.pdf`
- **CEGAR Verified Commands:** `17` (`0` malformed/unsafe snippets filtered)
- **MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`):** `17`
- **Discovered IPs/Subnets:** `172.16.157.136`
- **Discovered Interfaces:** `None`
- **Related Knowledge Note:** [[knowledge/trained_cyber_forensics_intro_guide_updated_table]]
powershell -NoProfile -Command "Get-FileHash -Algorithm SHA256 C:\Suspicious\*.exe,C:\Suspicious\*.dll" && sigcheck -accepteula -h -vr C:\Suspicious
## Distilled MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`)
| Pre-State ($s$) | Tactic ($\tau$) | Technique ($k$) | Tool ($u$) | Post-State ($s'$) | Verified Command ($c$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `volatility` | `s_passive_topology_mapped` | `volatility framework.  The below section will cover some of the most common plugins an` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `chmod` | `s_interactive_tty_or_priv_escalated` | `chmod g+r file` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `crontab` | `s_active_services_enumerated` | `crontab file, usually by running the crontab command. For example, the crontab entry` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `find` | `s_credentials_or_certs_acquired` | `find injected code.` |
| `s_passive_topology_mapped` | **`Active_Enum`** | Active Network, Cloud, Directory Service & Endpoint Probing | `traceroute` | `s_active_services_enumerated` | `Traceroute Attack` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `tracert` | `s_firewall_or_acl_unlocked` | `tracert command in Windows.` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `volatility` | `s_passive_topology_mapped` | `volatility plugin, filescan, parses for the file object tag in memory and lists all the opened` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `chmod` | `s_interactive_tty_or_priv_escalated` | `chmod o+r file` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `at` | `s_active_services_enumerated` | `At 22:30` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `volatility` | `s_passive_topology_mapped` | `volatility plugin can provide more information about VADs in one process.` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `chmod` | `s_interactive_tty_or_priv_escalated` | `chmod go+r file` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `crontab` | `s_passive_topology_mapped` | `crontab file to install file as your current crontab. The crontab command checks the file` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `chmod` | `s_interactive_tty_or_priv_escalated` | `chmod 644 file` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `crontab` | `s_passive_topology_mapped` | `crontab -l. To remove the crontab, use crontab -r.` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `and` | `s_interactive_tty_or_priv_escalated` | `SUDO AND /ETC/SUDOERS` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `find` | `s_passive_topology_mapped` | `find traces on the file system. To mitigate this challenge, use all of the information` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `find` | `s_interactive_tty_or_priv_escalated` | `find /mnt/evidence -user root -perm -04000 -print` |
powershell -NoProfile -Command "Get-FileHash -Algorithm SHA256 C:\Suspicious\*.exe,C:\Suspicious\*.dll" && sigcheck -accepteula -h -vr C:\Suspicious
## Verified Executable Commands (Grouped by Capability Layer)
powershell -NoProfile -Command "Get-FileHash -Algorithm SHA256 C:\Suspicious\*.exe,C:\Suspicious\*.dll" && sigcheck -accepteula -h -vr C:\Suspicious
### General_System (15 commands)
```bash
volatility framework.  The below section will cover some of the most common plugins an
volatility plugin, filescan, parses for the file object tag in memory and lists all the opened
volatility plugin can provide more information about VADs in one process.
chmod g+r file
chmod o+r file
chmod go+r file
chmod 644 file
SUDO AND /ETC/SUDOERS
crontab file, usually by running the crontab command. For example, the crontab entry
crontab file to install file as your current crontab. The crontab command checks the file
crontab -l. To remove the crontab, use crontab -r.
At 22:30
find /mnt/evidence -user root -perm -04000 -print
find traces on the file system. To mitigate this challenge, use all of the information
find injected code.
```
powershell -NoProfile -Command "Get-FileHash -Algorithm SHA256 C:\Suspicious\*.exe,C:\Suspicious\*.dll" && sigcheck -accepteula -h -vr C:\Suspicious
### L3_Routing_NAT (2 commands)
```bash
Traceroute Attack
tracert command in Windows.
```
powershell -NoProfile -Command "Get-FileHash -Algorithm SHA256 C:\Suspicious\*.exe,C:\Suspicious\*.dll" && sigcheck -accepteula -h -vr C:\Suspicious

<!-- CORA-MAXIMIZED-COMMANDS-START -->
## Maximized Windows & Linux Command Examples for `Cyber Forensics Intro Guide updated table`

> **Domain Hub:** [[knowledge/10_digital_forensics_pe_reversing_and_threat_intel|Domain Hub 10: Digital Forensics (Autopsy / EnCase), NTFS Internals (MFT / ADS / Slack Space / Oplocks), PE Reverse Engineering & Threat Intel (APT28)]]  
> **Master Playbooks:** [[commands/windows_master_command_playbook]] | [[commands/linux_master_command_playbook]] | [[commands/curl_playbook]] | [[commands/tio_serial_playbook]]  
> **When to Apply:** Apply when performing disk/image forensics (Autopsy, EnCase, SleuthKit), analyzing NTFS `$MFT` records, Alternate Data Streams (`dir /r`), or slack space, reverse-engineering Windows PE (`.exe`/`.dll`/`.sys`) or Linux ELF binaries, or hunting APT28 / Fancy Bear IOCs and TTPs.  
> **15-Engine H-MDP State Transition:** `s_init_unknown` $\xrightarrow{\text{Passive_Enum}}$ `s_passive_topology_mapped` | **Bayesian Root-Cause Triggers:** `ntfs_ads_or_slack_space_artifact, packed_or_hollowed_pe_binary, apt28_credential_or_persistence_ttp, deleted_mft_file_recovery` | **Isolation:** `RED, BLUE, WHITE (100% compatible with WHITE Analyst Read-Only mode for offline forensic & binary analysis)`

| Primary Command (`Windows` / `Linux`) | OS / Shell | What It Does & Key Flags | When to Apply & Expected Output | Cross-Platform Equivalent |
| :--- | :--- | :--- | :--- | :--- |
| `powershell -NoProfile -Command "Get-FileHash -Algorithm SHA256 C:\Suspicious\*.exe,C:\Suspicious\*.dll" && sigcheck -accepteula -h -vr C:\Suspicious` | **Windows PS / Sysinternals** | Computes cryptographic SHA256 hashes and verifies Authenticode digital signatures for suspect binaries (`[[knowledge/trained_cyber_forensics_intro_guide_updated_table]]`). | Apply first during malware triage and forensic chain-of-custody verification. | `sha256sum /tmp/suspicious/* && file /tmp/suspicious/*` |
| `dir /a /r C:\Users\* && powershell -NoProfile -Command "Get-Item C:\Users\Public\* -Stream * \| Where-Object Stream -ne ':$DATA'"` | **Windows CMD / PS** | Detects NTFS Alternate Data Streams (`ADS`) attached to files or directories (`[[knowledge/trained_cqc001_e020_m020_ntfs_cheat_sheets]]`). | Apply when hunting hidden payloads or reading `Zone.Identifier` download origin URLs. | `getfattr -R -d -m - /home` |
| `fsutil fsinfo ntfsinfo C: && fsutil behavior query DisableLastAccess` | **Windows CMD (Admin)** | Displays NTFS volume geometry (`Bytes Per Sector`, `Bytes Per Cluster`, `$MFT` start cluster and zone) and LastAccess timestamp policy. | Apply when analyzing NTFS cluster allocation, `$MFT` layout, and slack space (`[[knowledge/trained_bcf_slack_space_and_deleted_files]]`). | `sudo tune2fs -l /dev/sda1` |
| `mmls disk.dd && fls -r -d -p disk.dd <PART_OFFSET> && icat disk.dd <INODE> > recovered_file.bin` | **Linux / SleuthKit** | Lists partition table offsets (`mmls`), enumerates deleted files in the NTFS `$MFT` / ext4 journal (`fls -r -d -p`), and extracts deleted file content by inode/MFT entry (`icat`). | Apply during Autopsy/SleuthKit disk image forensics (`[[knowledge/trained_bcf_autopsy_navigation_and_analysis]]`). | `autopsy` |
| `file <BINARY> && objdump -x -p <BINARY> && readelf -h -S -l -d <BINARY>` | **Linux Bash** | Inspects PE (`MZ`/`PE\0\0`) or ELF headers, sections (`.text`, `.rdata`, `.data`, `.rsrc`, `UPX0`), import tables (`IAT`), and RWE segment flags (`[[knowledge/trained_cbm_1_2_2006_goppit_pe_format_reverse_engineer_view]]`). | Apply during static binary reverse engineering to detect packed sections (high entropy / `W+X` permissions) and imported APIs (`VirtualAllocEx`, `WriteProcessMemory`, `CreateRemoteThread`). | `dumpbin /headers /imports <BINARY>.exe` |
| `strings -a -n 6 <BINARY> \| grep -iE 'http\|https\|cmd\.exe\|powershell\|HKEY_\|\\pipe\\\|Mozilla\|[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}'` | **Linux / Windows** | Extracts ASCII/UTF-16 (`strings -el`) strings of length >= 6 and filters for URLs, IPs, Registry keys, named pipes, and User-Agent beacons. | Apply to quickly extract C2 indicators, mutex names, and embedded scripts from a binary (`[[knowledge/trained_apt28-center-of-storm-2017_mandiant]]`). | `strings.exe -accepteula -n 6 <BINARY>.exe \| findstr /i "http HKEY cmd powershell"` |

### Copy-Pasteable Execution Block (Windows & Linux)
```bash
# [Windows PS / Sysinternals] Computes cryptographic SHA256 hashes and verifies Authenticode digital signatures for suspect binaries (`[[knowledge/trained_cyber_forensics_intro_guide_updated_table]]`).
powershell -NoProfile -Command "Get-FileHash -Algorithm SHA256 C:\Suspicious\*.exe,C:\Suspicious\*.dll" && sigcheck -accepteula -h -vr C:\Suspicious
# [Windows CMD / PS] Detects NTFS Alternate Data Streams (`ADS`) attached to files or directories (`[[knowledge/trained_cqc001_e020_m020_ntfs_cheat_sheets]]`).
dir /a /r C:\Users\* && powershell -NoProfile -Command "Get-Item C:\Users\Public\* -Stream * | Where-Object Stream -ne ':$DATA'"
# [Windows CMD (Admin)] Displays NTFS volume geometry (`Bytes Per Sector`, `Bytes Per Cluster`, `$MFT` start cluster and zone) and LastAccess timestamp policy.
fsutil fsinfo ntfsinfo C: && fsutil behavior query DisableLastAccess
# [Linux / SleuthKit] Lists partition table offsets (`mmls`), enumerates deleted files in the NTFS `$MFT` / ext4 journal (`fls -r -d -p`), and extracts deleted file content by inode/MFT entry (`icat`).
mmls disk.dd && fls -r -d -p disk.dd <PART_OFFSET> && icat disk.dd <INODE> > recovered_file.bin
# [Linux Bash] Inspects PE (`MZ`/`PE\0\0`) or ELF headers, sections (`.text`, `.rdata`, `.data`, `.rsrc`, `UPX0`), import tables (`IAT`), and RWE segment flags (`[[knowledge/trained_cbm_1_2_2006_goppit_pe_format_reverse_engineer_view]]`).
file <BINARY> && objdump -x -p <BINARY> && readelf -h -S -l -d <BINARY>
# [Linux / Windows] Extracts ASCII/UTF-16 (`strings -el`) strings of length >= 6 and filters for URLs, IPs, Registry keys, named pipes, and User-Agent beacons.
strings -a -n 6 <BINARY> | grep -iE 'http|https|cmd\.exe|powershell|HKEY_|\\pipe\\|Mozilla|[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}'
```
<!-- CORA-MAXIMIZED-COMMANDS-END -->
