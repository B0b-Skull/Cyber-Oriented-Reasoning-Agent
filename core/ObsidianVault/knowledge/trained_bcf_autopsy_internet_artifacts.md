---
title: "Trained Knowledge & Topology: BCF Autopsy Internet Artifacts"
category: knowledge
domain_hub: "[[knowledge/10_digital_forensics_pe_reversing_and_threat_intel]]"
os_platform: cross-platform
primary_tactic: Passive_Enum
summary: "Operational architecture, decision workflows & Windows/Linux command reference for BCF Autopsy Internet Artifacts: Digital forensics workflows (Autopsy, EnCase, SleuthKit), NTFS Master File Table ($MFT), Alternate Data Streams (ADS), file/RAM sl"
when_to_apply: "Apply when working with BCF Autopsy Internet Artifacts (cross-platform): Apply when performing disk/image forensics (Autopsy, EnCase, SleuthKit), analyzing NTFS `$MFT` records, Alternate Data Streams (`dir /r`), or slack space, reverse-engineering Windows PE (`.exe`/`.dll`/`.sys`) or Linux ELF binaries, or hunting APT28 / Fancy Bear IOCs and TTPs."
tags: [mdp, pdf, trained, windows, linux, forensics, autopsy, encase, ntfs, mft, oplocks, pe_header, apt28, strings, sigcheck, sha256sum, passive_enum]
source_file: "BCF Autopsy Internet Artifacts"
updated: 2026-10-30
---

# Trained Knowledge & Architecture: `BCF_Autopsy Internet Artifacts.pdf`

- **Source Path:** `~/Projects/CORA/Training/BCF_Autopsy Internet Artifacts.pdf` (`pdf`)
- **Extracted Technical Entities:** `general`
- **Extracted IPs / Subnets:** `None`
- **Extracted Interfaces:** `None`

### Visual & Network Diagram Intelligence (`BCF_Autopsy Internet Artifacts.pdf#page1`)
- **Spatially Grouped Diagram Nodes (Box/Component Clusters):**
  1. `[ICHIRON | TRAINING]`
  2. `[Basic Computer Forensics | 26-28Mar2018 | DISCOVERYANDCOUNTER-INFILTRATIONPROFESSIONALTM(DCIP)TM]`

### Visual & Network Diagram Intelligence (`BCF_Autopsy Internet Artifacts.pdf#page2`)
- **Spatially Grouped Diagram Nodes (Box/Component Clusters):**
  1. `[Internet and Browser]`
  2. `[Artifacts]`
  3. `[OVERVIEW]`

## LLM Distilled Operational Summary
### Operational Techniques & Decision Workflows
*   **Browser Artifact Analysis Workflow:**
    *   Identify the target operating system (Windows XP, Vista, 7) to determine the correct registry path or user profile structure.
    *   Locate specific artifact types: Cache (content), History (URLs), Cookies (session data), and Download files.
    *   Use specialized external viewers for visualization: `IECacheView` for Internet Explorer and `Firefox`'s `places.sqlite` for Mozilla Firefox.
    *   Export artifacts when possible to preserve state, as cached webmail messages are often overwritten quickly.
*   **Spatial Grouping Strategy:**
    *   Cluster findings by browser type (Internet Explorer, Firefox, Chrome) and then by OS version to normalize path discrepancies.
    *   Distinguish between "Local Settings" (XP) and "AppData" (Vista/7) directory structures.

### Critical Command Patterns & Required Flags
*   **Path Resolution Variables:**
    *   `%systemdir%`: System root directory.
    *   `%root%`: Root drive letter (e.g., `C:`).
    *   `%username%` / `%userprofile%`: Current user's profile name.
    *   `%PROFILE%`: Firefox-specific profile identifier.
*   **Key File Formats:**
    *   Firefox: `places.sqlite` (SQLite database format).
    *   IE/Chrome: Folder-based storage (`.ie5`, `.cache`, `.default`).

### Network Topology & Service Relationships
*   **Internet Explorer (IE):**
    *   **XP Path:** `%systemdir%\Documents and Settings\%username%\Local Settings\Temporary Internet Files\Content.ie5` and `Cookies`.
    *   **Vista/7 Path:** `%systemdir%\Users\%username%\AppData\Local\Microsoft\Windows\Temporary Internet Files\` (including `Low` subfolder) and `History`.
*   **Mozilla Firefox:**
    *   **XP Path:** `%root%/Documents and Settings/%userprofile%/Local Settings/Application Data/Mozilla/Firefox/Profiles/*.default/Cache`.
    *   **Vista/7 Path:** `C:\Users\%userprofile%\AppData\Local\Mozilla\Firefox\Profiles\%PROFILE%.default\Cache` and `Roaming` profile.
*   **Google Chrome:**
    *   **XP Path:** `%root%/Documents and Settings/%userprofile%/Local Settings/Application Data/Google/Chrome/User Data/Default/Cache`.
    *   **Vista/7 Path:** `%root%/Users\%username%\AppData\Local\Google\Chrome\User Data\Default\Preference`.
*   **Data Characteristics:**
    *   **Cached Browsing:** Contains actual page content and "read-only" webmail messages.
    *   **Volatility:** Cache data is overwritten rapidly; export is recommended for evidence preservation.

## Document Structure & Key Topics
- Visual & Network Diagram Intelligence (`BCF_Autopsy Internet Artifacts.pdf#page1`)
- Visual & Network Diagram Intelligence (`BCF_Autopsy Internet Artifacts.pdf#page2`)

<!-- CORA-MAXIMIZED-COMMANDS-START -->
## Maximized Windows & Linux Command Examples for `BCF Autopsy Internet Artifacts`

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
