---
title: "Trained Knowledge & Topology: CBM 1 2 2006 Goppit PE Format Reverse Engineer View"
category: knowledge
domain_hub: "[[knowledge/10_digital_forensics_pe_reversing_and_threat_intel]]"
os_platform: cross-platform
primary_tactic: Passive_Enum
summary: "Operational architecture, decision workflows & Windows/Linux command reference for CBM 1 2 2006 Goppit PE Format Reverse Engineer View: Digital forensics workflows (Autopsy, EnCase, SleuthKit), NTFS Master File Table ($MFT), Alternate Data Streams (ADS), file/RAM sl"
when_to_apply: "Apply when working with CBM 1 2 2006 Goppit PE Format Reverse Engineer View (cross-platform): Apply when performing disk/image forensics (Autopsy, EnCase, SleuthKit), analyzing NTFS `$MFT` records, Alternate Data Streams (`dir /r`), or slack space, reverse-engineering Windows PE (`.exe`/`.dll`/`.sys`) or Linux ELF binaries, or hunting APT28 / Fancy Bear IOCs and TTPs."
tags: [http, john, mdp, pdf, tls, trained, windows, linux, forensics, autopsy, encase, ntfs, mft, oplocks, pe_header, apt28, strings, sigcheck, sha256sum, passive_enum]
source_file: "CBM 1 2 2006 Goppit PE Format Reverse Engineer View"
updated: 2026-10-30
---

# Trained Knowledge & Architecture: `CBM_1_2_2006_Goppit_PE_Format_Reverse_Engineer_View.pdf`

- **Source Path:** `~/Projects/CORA/Training/CBM_1_2_2006_Goppit_PE_Format_Reverse_Engineer_View.pdf` (`pdf`)
- **Extracted Technical Entities:** `http, john, tls`
- **Extracted IPs / Subnets:** `None`
- **Extracted Interfaces:** `None`

## Document Structure & Key Topics
- The Section Table (p. 18)
- The PE File Sections (p. 20)
- The Import Section (p. 29)
- The Loader (p. 35)
- Navigating Imports on Disk (p. 39)
- Adding Code to a PE File (p. 46)
- Adding Import to an Executable (p. 53)
- Infection of PE Files by Viruses (p. 71)

## Extracted Operational Steps & Workflows
- 1. Read in the first page of the file with the DOS header, PE header, and section headers.
- 2. Determine whether the target area of the address space is available, if not allocate another area.
- 3. Using info in the section headers, map sections of the file to the appropriate places in the allocated
- 4. If the file is not loaded at its target address (ImageBase), apply relocation fix-ups.
- 5. Go through list of DLLs in the imports section and load any that aren't already loaded (recursive).
- 6. Resolve all the imported symbols in the imports section.
- 7. Create the initial stack and heap using values from the PE header.
- 8. Create the initial thread and start the process.
- 1. Check to see if the module is already loaded.
- 2. Map the module and supporting information into memory.
- 3. Walk the module's import descriptor table (find other modules this one is importing).
- 4. Update the module's load count as well as any others brought in by this DLL.
- 5. Initialize the module.
- 6. Clear some sort of flag, indicating that the load has finished.
- 1. Add to an existing section when there is enough space for your code.
- 2. Enlarge an existing section when there is not enough space.
- 3. Add an entirely new section.
- 1. If the section is followed by other sections then you will need to move the following sections up to make
- 2. There are various references within the file headers that will need to be adjusted if you change the file
- 3. References between various sections (such as references to data values from the code section) will all
- 1. Each DLL must be declared with an IMAGE_IMPORT_DESCRIPTOR (IID), remembering to close the
- 2. Each IID needs at least Name1 and FirstThunk fields, the rest can be set to 0 (setting OriginalFirstThunk
- 3. Each entry of the FirstThunk must be an RVA to an Image_Thunk_Data (the IAT) which in turn contains a
- 4. If IIDs have been added then the isize field of the Import Table in the Data Directory may need
- 1. select basecalc.exe in the box at the top (it should still be running in Olly.)
- 2. Next enter our OEP (2ADB4) in the appropriate box
- 3. Press the "IAT AutoSearch" button and click OK on the messagebox
- 4. Press the "Get Imports" button
- 5. Press "Show Invalid" - in this case there are none
- 6. Press "Fix Dump" and select basecalc_dmp.exe in the open dialogbox
- 7. Exit.
- 1. The virus moves the PE  header to the end of the host app and inserts its code into the space.
- 2. The virus appends the host app to itself.

## Extracted Reference Excerpt
--- [Page 1] ---
Volume 1, Issue 2, 2006 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
Portable Executable File Format – A Reverse Engineer View 
 
Goppit 
January 2006 
 
Abstract 
This tutorial aims to collate information from a variety of sources and present it in a way which is accessible 
to beginners. Although detailed in parts, it is oriented towards reverse code engineering and superfluous 
information has been omitted.

--- [Page 2] ---
PORTABLE EXECUTABLE FILE FORMAT – A REVERSE ENGINEER VIEW 
This disclaimer is not meant to sidestep the responsibility for the material we will share 
with you, but rather is designed to emphasize the purpose of this CodeBreakers Magazine 
feature, which is to provide information for your own purposes. The subjects presented 
have been chosen for their educational value. The information contained herein consists of 
Secure Software Engineering, Software Security Engineering, Software Management, 
Security Analysis, Algorithms, Virus-Research, Software-Protection and Reverse Code 
Engineering, Cryptanalysis, White Hat and Black Hat Content, and is derived from authors 
of academically institutions, commercials, organizations, as well as private persons. The 
information should not be considered to be completely error-free or to include all relevant 
information; nor should it be used as an exclusive basis for decision-making. The user 
understands and accepts that if CodeBreakers Magazine were to accept the risk of harm to 
the user from use of this information, it would not be able to make the information 
available because the cost to cover the risk of harms to all users would be too great. Thus, 
use of the information is strictly voluntary and at the users sole risk. 
  
The information contained herein is not a license, either expressly or impliedly, to any 
intellectual property owned or controlled by any of the authors or developers of 
CodeBreakers Magazine. The information contained herein is provided on an "AS IS" basis 
and to the maximum extent permitted by applicable law, this information is provided AS IS 
AND WITH ALL FAULTS, and the authors and developers of CodeBreakers Magazine hereby 
disclaim all other warranties and conditions, either express, implied or statutory, including, 
but not limited to, any (if any) implied warranties, duties or conditions of merchantability, 
of fitness for a particular purpose, of accuracy or completeness of responses, of results, of 
workmanlike effort, of lack of viruses, and of lack of negligence, all with regard to the 
contribution.  
ALSO, THERE IS NO WARRANTY OR CONDITION OF TITLE, QUIET ENJOYMENT, QUIET 
POSSESSION, CORRESPONDENCE TO DESCRIPTION OR NON-INFRINGEMENT WITH 
REGARD TO CODEBREAKERS MAGAZINE.  
IN NO EVENT WILL ANY AUTHOR OR DEVELOPER OF

<!-- CORA-MAXIMIZED-COMMANDS-START -->
## Maximized Windows & Linux Command Examples for `CBM 1 2 2006 Goppit PE Format Reverse Engineer View`

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
