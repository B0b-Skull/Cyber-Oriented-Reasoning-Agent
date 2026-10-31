---
title: "Trained Knowledge & Topology: BCF EnCase Searching"
category: knowledge
domain_hub: "[[knowledge/10_digital_forensics_pe_reversing_and_threat_intel]]"
os_platform: cross-platform
primary_tactic: Passive_Enum
summary: "Operational architecture, decision workflows & Windows/Linux command reference for BCF EnCase Searching: Digital forensics workflows (Autopsy, EnCase, SleuthKit), NTFS Master File Table ($MFT), Alternate Data Streams (ADS), file/RAM sl"
when_to_apply: "Apply when working with BCF EnCase Searching (cross-platform): Apply when performing disk/image forensics (Autopsy, EnCase, SleuthKit), analyzing NTFS `$MFT` records, Alternate Data Streams (`dir /r`), or slack space, reverse-engineering Windows PE (`.exe`/`.dll`/`.sys`) or Linux ELF binaries, or hunting APT28 / Fancy Bear IOCs and TTPs."
tags: [http, mdp, pdf, trained, windows, linux, forensics, autopsy, encase, ntfs, mft, oplocks, pe_header, apt28, strings, sigcheck, sha256sum, passive_enum]
source_file: "BCF EnCase Searching"
updated: 2026-10-30
---

# Trained Knowledge & Architecture: `BCF_EnCase Searching.pdf`

- **Source Path:** `~/Projects/CORA/Training/BCF_EnCase Searching.pdf` (`pdf`)
- **Extracted Technical Entities:** `http`
- **Extracted IPs / Subnets:** `None`
- **Extracted Interfaces:** `None`

### Visual & Network Diagram Intelligence (`BCF_EnCase Searching.pdf#page1`)
- **Spatially Grouped Diagram Nodes (Box/Component Clusters):**
  1. `[JCHIRON | TRAINING]`
  2. `[Basic Computer Forsensics | DISCOVERYANDCOUNTER-INFILTRATIONPROFESSIONALTM(DCIP)TM]`

### Visual & Network Diagram Intelligence (`BCF_EnCase Searching.pdf#page2`)
- **Spatially Grouped Diagram Nodes (Box/Component Clusters):**
  1. `[EnCase Search]`
  2. `[Keyword | GREP | Data Carving]`
  3. `[OVERVIEW]`

### Visual & Network Diagram Intelligence (`BCF_EnCase Searching.pdf#page19`)
- **Spatially Grouped Diagram Nodes (Box/Component Clusters):**
  1. `[WCHIRON | TRAINING]`
  2. `[Select Keyword Tab | EnCase Law Enforcement | FEileEditView IoolsHelp | NewOpen Save Print | Add Device  Search | Keywords | Table]`
  3. `[Global]`
  4. `[Cases | Home | -Entries | Home | File Extents | Text]`
  5. `[Timeline | Disk | Code | Name | in | Path | nfl_e_allenmerrimanpwrrnk_57.....infl_e_allenmerrimanpwrrnk_.5 | nfl_g_belichick_134[1].jpg | nf_nfc_preview_134[1].ipg | Re...,nfl_g_belichick_134[1].jpg | R..,nf_nfc_preview_134[1].jpg | nf_draft_35[1].jpg | Registry ...,nfl_draft_35[1]ipg | bg_nfl_scoreboard_green[1].ipg...(bg_nfl_scoreboard_green[1]. | ReportConsoleDetails]`
  6. `[Filter | Repo | In | EnScript | Filters[= Conditi<]`
  7. `[34745 | 34746 | 34747 | 34748 | 34749 | HexDocTranscript | Picture]`
  8. `[no | EnScript | Forensic | Examples | Case Processor]`
  9. `[Registry View/,Terror Attack_11C(Users\UserlAppData\Locall...↓nfl_g_belichick_134[1].ipg (PS 124360 LS 122312 CL 15289 5O 000 FO 0 LE 6) | EnCase LawEnforcement | FileEdit yiew IoolsHelp | Newopen  Save  Print | Cases | Keywords | Keywords]`
  10. `[OR]`
  11. `[Add Device Search | Table | ReportGalleryTimeline | Name | 一 | nfl_e_allenmerimanpwrrnk.5.....inf_e_llenmerimanpwrrnk_.5 | 34745 | 34746 | nfl_nfc_preview_134[1].ipg | 34747 | nfl_g_belichick_134[1].ipg | 34748 | nfl_draft_35[1].ipg | 34749]`
  12. `[Disk | Code | Full | Path | ...(nf_nfc_preview_134[1].jipg | Re..,nfl_g_belichick_134[1].jipg | Registry ...,nfl_draft_35[1].ipg | bg_nfl_scoreboard_green[1].jipg ...(bg_nf_scoreboard_green[1].]`
  13. `[Filter | In | Repo | Enscript | Filters [= Conditi]`
  14. `[Home | File Extents | TextHexDoc]`
  15. `[Local]`
  16. `[Transcript | Picture]`
  17. `[ReportConsole Details | Registry ViewTerror Attack_11C(Users\User(AppData\Local..,nf_g_belichick_134[1].jipg (PS 124360 LS 122312 CL 15289 SO 000 FO 0 LE 6)]`
  18. `[EnScript | 中 | 口 | Examples | 白 | Forensic | Case Processor]`

## LLM Distilled Operational Summary
### Operational Techniques & Decision Workflows
*   **Pre-Search Preparation**: Always configure `Keywords.ini` files in a dedicated folder before launching EnCase to define search terms.
*   **Indexing Strategy**: Recognize that EnCase does not index evidence by default; indexing the entire device is an optional but slow process. Rely on refined keyword terms to minimize false positives during unindexed searches.
*   **Result Verification**: Utilize the "Refresh" function in the Search Hits tab to update results dynamically without restarting the full search.
*   **Advanced Filtering**: Use Globally Search for Regular Expressions (GREP) to surgically reduce false hits, particularly when carving data from unallocated space, pagefiles, or volume slack.

### Critical Command Patterns & Required Flags
*   **Code Page Selection**:
    *   Default: ANSI Latin-1.
    *   Unicode: Searches both Unicode and ASCII formats (2 bytes/char).
    *   UTF-8: Variable-length sequences (up to 4 bytes); standard for web content.
    *   UTF-7: Obsolete scheme with high-bit clear octets.
*   **GREP Syntax Patterns**:
    *   `.`: Matches any single character (e.g., `bad.guy`).
    *   `[set]`: Matches any character within the set (e.g., `bad[ ,;]guy`).
    *   `[a-z]`: Matches a range of characters (e.g., `bad[a-z]guy`).
    *   `[^#]`: Matches any character *except* those in the set (e.g., `bad[^0-9]guy`).
    *   `+`: Repeats the preceding character or set one or more times.

### Network Topology & Service Relationships
*   **File System Relationships**: Searches traverse `File Extents`, `Text`, `Hex`, `Doc`, and `Picture` views. Specific artifacts include registry entries (e.g., `Terror Attack_11C`) and user-specific paths (`Users\User\AppData\Local`).
*   **Artifact Clustering**: Diagram nodes group related files such as `nfl_e_allenmerrimanpwrrnk_5`, `nfl_g_belichick_134[1].jpg`, and `bg_nfl_scoreboard_green[1].jpg` under categories like `Timeline`, `Disk`, `Code`, and `Name`.
*   **Tool Integration**: The workflow integrates `EnCase Search`, `Keyword`, `GREP`, and `Data Carving` modules, often accessed via the `Keywords` tab, `Add Device`, and `Search` menus within the EnCase Law Enforcement interface.

## Document Structure & Key Topics
- Visual & Network Diagram Intelligence (`BCF_EnCase Searching.pdf#page1`)
- Visual & Network Diagram Intelligence (`BCF_EnCase Searching.pdf#page2`)
- Visual & Network Diagram Intelligence (`BCF_EnCase Searching.pdf#page19`)

<!-- CORA-MAXIMIZED-COMMANDS-START -->
## Maximized Windows & Linux Command Examples for `BCF EnCase Searching`

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
