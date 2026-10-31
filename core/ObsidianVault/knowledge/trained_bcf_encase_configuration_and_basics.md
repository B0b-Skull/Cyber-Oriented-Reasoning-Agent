---
title: "Trained Knowledge & Topology: BCF EnCase Configuration and Basics"
category: knowledge
domain_hub: "[[knowledge/10_digital_forensics_pe_reversing_and_threat_intel]]"
os_platform: cross-platform
primary_tactic: Passive_Enum
summary: "Operational architecture, decision workflows & Windows/Linux command reference for BCF EnCase Configuration and Basics: Digital forensics workflows (Autopsy, EnCase, SleuthKit), NTFS Master File Table ($MFT), Alternate Data Streams (ADS), file/RAM sl"
when_to_apply: "Apply when working with BCF EnCase Configuration and Basics (cross-platform): Apply when performing disk/image forensics (Autopsy, EnCase, SleuthKit), analyzing NTFS `$MFT` records, Alternate Data Streams (`dir /r`), or slack space, reverse-engineering Windows PE (`.exe`/`.dll`/`.sys`) or Linux ELF binaries, or hunting APT28 / Fancy Bear IOCs and TTPs."
tags: [mdp, pdf, trained, windows, linux, forensics, autopsy, encase, ntfs, mft, oplocks, pe_header, apt28, strings, sigcheck, sha256sum, passive_enum]
source_file: "BCF EnCase Configuration and Basics"
updated: 2026-10-30
---

# Trained Knowledge & Architecture: `BCF_EnCase Configuration and Basics.pdf`

- **Source Path:** `~/Projects/CORA/Training/BCF_EnCase Configuration and Basics.pdf` (`pdf`)
- **Extracted Technical Entities:** `general`
- **Extracted IPs / Subnets:** `None`
- **Extracted Interfaces:** `None`

### Visual & Network Diagram Intelligence (`BCF_EnCase Configuration and Basics.pdf#page1`)
- **Spatially Grouped Diagram Nodes (Box/Component Clusters):**
  1. `[ICHIRON | TRAINING]`
  2. `[Basic Computer Forensics | 26-28Mar2018 | DISCOVERYANDCOUNTER-INFILTRATIONPROFESSIONALTM(DCIP)TM]`

### Visual & Network Diagram Intelligence (`BCF_EnCase Configuration and Basics.pdf#page2`)
- **Spatially Grouped Diagram Nodes (Box/Component Clusters):**
  1. `[EnCase | Configuration]`
  2. `[OVERVIEW]`
  3. `[Adding Images | Pane Properties]`

### Visual & Network Diagram Intelligence (`BCF_EnCase Configuration and Basics.pdf#page3`)
- **Spatially Grouped Diagram Nodes (Box/Component Clusters):**
  1. `[WCHIRON | TRAINING]`
  2. `[Starting EnCase - Need Dongle]`
  3. `[F | EnCase Acquisition | File Edit View Tools Help | 港 New | Open]`
  4. `[EnCase Law Enforcement | File Edit  View Toos  Help | New  Open  Refresh]`
  5. `[Refresh]`
  6. `[Report | Code]`
  7. `[DISCOVERYANDCOUNTER-INFILTRATION | PROFESSIONALTM(DCIP)TM | @ 2016 CHIRON TECHNOLOGY SERVICES, INC.]`
  8. `[Basic Computer Forensics | Any unauthorized use or disclosure of this material is strictly prohibited.]`

## LLM Distilled Operational Summary
### Operational Techniques & Decision Workflows

*   **Case Initialization:** Create a new case via `File > New`, defining the Case Name, Examiner Name, and file paths.
*   **Image Ingestion:**
    *   Navigate to `File > Add Raw Image`.
    *   Select all `.img` files (exclude `.txt` logs) and drag them into the "Component Files" window.
    *   Reorder images by highlighting them in reverse sequence to match the physical disk layout.
    *   Alternatively, use the "Add Device" tab for previously acquired hardware.
*   **File Viewer Configuration:**
    *   Access `View > File Viewers > New` to create custom viewers.
    *   Assign application paths (e.g., IrfanView for images, Firefox/Chrome for HTML).
    *   Configure `View > File Types` to override default OS rendering (e.g., set HTML to use Mozilla Firefox).
*   **Global Options Setup:**
    *   Enable "Auto Save" and configure "Picture Viewer" settings (ART Image, Timeout, Corrupted Image handling).
    *   Set "Show True/False" conditions to display "yes/no" values for clarity.
*   **Table Pane Optimization:**
    *   Right-click column headers to hide unnecessary columns, reorder, or lock specific columns.
    *   Utilize "Green Homeplate" in the Tree pane to expand/collapse directory structures.
    *   Use blue checkmarks in the Table pane to select files for bulk operations.

### Critical Command Patterns & Required Flags

*   **Menu Path for Images:** `File` → `Add Raw Image`
*   **Menu Path for Viewers:** `View` → `File Viewers` → `New`
*   **Menu Path for File Types:** `View` → `File Types`
*   **Menu Path for Global Settings:** `Options` → `Global` Tab
*   **Column Management:** Right-click column header → `Show Columns` (Uncheck desired)
*   **Selection Logic:** Highlight files in reverse order when adding multiple images to ensure correct chronological/physical sequence.

### Network Topology & Service Relationships

*   **Default Rendering Services:** EnCase defaults to the Windows OS application for rendering webpages and documents unless explicitly overridden via the `File Types` configuration.
*   **Recommended External Viewers:**
    *   **HTML:** Mozilla Firefox or Google Chrome.
    *   **Images (bmp, jpg, gif):** IrfanView.
    *   **Advanced Graphics (psd):** Adobe Photoshop or GIMP.
*   **Dongle Dependency:** The software requires a physical dongle to start the acquisition process.

## Document Structure & Key Topics
- Visual & Network Diagram Intelligence (`BCF_EnCase Configuration and Basics.pdf#page1`)
- Visual & Network Diagram Intelligence (`BCF_EnCase Configuration and Basics.pdf#page2`)
- Visual & Network Diagram Intelligence (`BCF_EnCase Configuration and Basics.pdf#page3`)

<!-- CORA-MAXIMIZED-COMMANDS-START -->
## Maximized Windows & Linux Command Examples for `BCF EnCase Configuration and Basics`

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
