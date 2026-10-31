---
title: "Trained Knowledge & Topology: BCF EnCase Navigation"
category: knowledge
domain_hub: "[[knowledge/10_digital_forensics_pe_reversing_and_threat_intel]]"
os_platform: cross-platform
primary_tactic: Passive_Enum
summary: "Operational architecture, decision workflows & Windows/Linux command reference for BCF EnCase Navigation: Digital forensics workflows (Autopsy, EnCase, SleuthKit), NTFS Master File Table ($MFT), Alternate Data Streams (ADS), file/RAM sl"
when_to_apply: "Apply when working with BCF EnCase Navigation (cross-platform): Apply when performing disk/image forensics (Autopsy, EnCase, SleuthKit), analyzing NTFS `$MFT` records, Alternate Data Streams (`dir /r`), or slack space, reverse-engineering Windows PE (`.exe`/`.dll`/`.sys`) or Linux ELF binaries, or hunting APT28 / Fancy Bear IOCs and TTPs."
tags: [mdp, pdf, trained, windows, linux, forensics, autopsy, encase, ntfs, mft, oplocks, pe_header, apt28, strings, sigcheck, sha256sum, passive_enum]
source_file: "BCF EnCase Navigation"
updated: 2026-10-30
---

# Trained Knowledge & Architecture: `BCF_EnCase Navigation.pdf`

- **Source Path:** `~/Projects/CORA/Training/BCF_EnCase Navigation.pdf` (`pdf`)
- **Extracted Technical Entities:** `general`
- **Extracted IPs / Subnets:** `None`
- **Extracted Interfaces:** `None`

### Visual & Network Diagram Intelligence (`BCF_EnCase Navigation.pdf#page1`)
- **Spatially Grouped Diagram Nodes (Box/Component Clusters):**
  1. `[ICHIRON | TRAINING]`
  2. `[Basic Computer Forensics | 26-28Mar2018 | DISCOVERYANDCOUNTER-INFILTRATIONPROFESSIONALTM(DCIP)TM]`

### Visual & Network Diagram Intelligence (`BCF_EnCase Navigation.pdf#page2`)
- **Spatially Grouped Diagram Nodes (Box/Component Clusters):**
  1. `[EnCase | Tool navigation]`
  2. `[OVERVIEW]`

### Visual & Network Diagram Intelligence (`BCF_EnCase Navigation.pdf#page8`)
- **Spatially Grouped Diagram Nodes (Box/Component Clusters):**
  1. `[WCHIRON | TRAINING]`
  2. `[Filter Pane | What is it looking for?]`
  3. `[Edit "MS Word" | Conditions | Filters | Source Code | Name | M | f) Main | if File Ext equal to [doc]]`
  4. `[Report | and NotFullPath find [\Microsoft Office, \Temporary Internet Files, \C\IWindows, I.] | and Logical Size greater than [0]]`
  5. `[OK | Cancel]`
  6. `[DISCOVERYANDCOUNTER-INFILTRATION | PROFESSIONALTM(DCIP)TM | 2016 CHIRON TECHNOLOGY SERVICES,INC]`
  7. `[Basic Computer Forensics | Any unauthorized use or disclosure of this material is strictly prohibited.]`

## LLM Distilled Operational Summary
### Operational Techniques & Decision Workflows
*   **Case Initialization & Device Verification**: Verify the physical device status in the "Devices" tab. A blue triangle indicates a live device, while a red triangle indicates a remote preview. Ensure the hard drive status is "green-homeplated" before running conditions to confirm readiness.
*   **Filter Construction Workflow**:
    1.  Navigate to the **Filter Pane** and select **Conditions**.
    2.  Define the target file type (e.g., Microsoft Office) by editing the `File Ext` condition.
    3.  Refine the search path using `NotFullPath` to exclude system directories like `\Microsoft Office`, `\Temporary Internet Files`, and `\C\IWindows`.
    4.  Apply a size constraint using `Logical Size greater than [0]` to filter out empty files.
    5.  Execute the query; confirm activation by checking for a green "+" next to "Query" in the pane header.
*   **Report Generation**: Utilize the **Report** function within the Filter Pane to generate outputs based on active queries, specifically targeting file extensions and logical sizes.
*   **Advanced Parsing & EnScripts**: Use **EnScripts** for custom case processing (e.g., converting `.E01` images to DD format). Leverage **File Parsers** (EXIF Viewer, IM Archive Parser) for compound file analysis, noting that parsing PST/DBX/EDB files is memory-intensive and relies on the `ParseCache` subfolder.
*   **Record & Email Analysis**: Access the **Records** tab to view parsed email data (messages, attachments) from mounted compound files like PST or DBX.

### Critical Command Patterns & Required Flags
*   **File Extension Filter**: `if File Ext equal to [doc]` (Update to include `docx` for comprehensive coverage).
*   **Path Exclusion Logic**: `and NotFullPath find [\Microsoft Office, \Temporary Internet Files, \C\IWindows, I.]`.
*   **Size Constraint**: `and Logical Size greater than [0]`.
*   **Query Activation**: Toggle the green "+" indicator next to "Query" to enable/disable the active condition.

### Network Topology & Service Relationships
*   **Remote Device Indicators**: A **red triangle** on a device icon signifies a **remote preview of a live device over the network**, establishing a relationship between the local EnCase instance and a remote physical source.
*   **Secure Storage Dependencies**: Accessing encrypted data in system files and the Registry requires the **EDS certificate**, linking the `Secure Storage` view to specific cryptographic credentials.
*   **Compound File Mounting**: The **Records** tab relies on a cache file located in the `EnCase 6` folder (specifically the `ParseCache` subfolder) to mount and parse compound files like PST, DBX, and EDB.

## Document Structure & Key Topics
- Visual & Network Diagram Intelligence (`BCF_EnCase Navigation.pdf#page1`)
- Visual & Network Diagram Intelligence (`BCF_EnCase Navigation.pdf#page2`)
- Visual & Network Diagram Intelligence (`BCF_EnCase Navigation.pdf#page8`)

<!-- CORA-MAXIMIZED-COMMANDS-START -->
## Maximized Windows & Linux Command Examples for `BCF EnCase Navigation`

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
