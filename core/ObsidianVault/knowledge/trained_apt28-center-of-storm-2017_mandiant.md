---
title: "Trained Knowledge & Topology: APT28-Center-of-Storm-2017 MANDIANT"
category: knowledge
domain_hub: "[[knowledge/10_digital_forensics_pe_reversing_and_threat_intel]]"
os_platform: cross-platform
primary_tactic: Passive_Enum
summary: "Operational architecture, decision workflows & Windows/Linux command reference for APT28-Center-of-Storm-2017 MANDIANT: Digital forensics workflows (Autopsy, EnCase, SleuthKit), NTFS Master File Table ($MFT), Alternate Data Streams (ADS), file/RAM sl"
when_to_apply: "Apply when working with APT28-Center-of-Storm-2017 MANDIANT (cross-platform): Apply when performing disk/image forensics (Autopsy, EnCase, SleuthKit), analyzing NTFS `$MFT` records, Alternate Data Streams (`dir /r`), or slack space, reverse-engineering Windows PE (`.exe`/`.dll`/`.sys`) or Linux ELF binaries, or hunting APT28 / Fancy Bear IOCs and TTPs."
tags: [cve-2015-1701, cve-2015-2424, cve-2015-2590, cve-2015-3043, cve-2015-5119, cve-2016-7255, cve-2016-7855, john, mdp, pdf, powershell, trained, windows, linux, forensics, autopsy, encase, ntfs, mft, oplocks, pe_header, apt28]
source_file: "APT28-Center-of-Storm-2017 MANDIANT"
updated: 2026-10-30
---

# Trained Knowledge & Architecture: `APT28-Center-of-Storm-2017_MANDIANT.pdf`

- **Source Path:** `~/Projects/CORA/Training/APT28-Center-of-Storm-2017_MANDIANT.pdf` (`pdf`)
- **Extracted Technical Entities:** `cve-2015-1701, cve-2015-2424, cve-2015-2590, cve-2015-3043, cve-2015-5119, cve-2016-7255, cve-2016-7855, john, powershell`
- **Extracted IPs / Subnets:** `None`
- **Extracted Interfaces:** `None`

## LLM Distilled Operational Summary
### Operational Techniques & Decision Workflows
*   **Strategic Espionage to Information Operations:** APT28 evolved from traditional intelligence collection (defense/geopolitics) to active information operations. The workflow involves compromising a target, stealing internal data, and selectively leaking it to advance specific Russian political narratives (e.g., Syria conflict, NATO-Ukraine relations, 2016 US election).
*   **Target Selection:** Primary targets include governments, militaries, defense attaches, media entities, and dissidents in the US, Europe, and former Soviet Union. Specific focus on regional security organizations like NATO and OSCE.
*   **Tool Development & Adaptation:** The group demonstrates a sophisticated development cycle, adapting malware and operational procedures to evade detection over time (e.g., using decoys).
*   **Long-Term Persistence:** Operations date back to at least 2007, indicating a capability for long-term access and continuous monitoring of target environments.

### Critical Command Patterns & Required Flags
*   **Malware Families:** While specific command strings aren't detailed in this chunk, the report references the **Pawn Storm** campaign (Trend Micro's alias for APT28 activity).
*   **Detection Context:** Operations are characterized by endpoint and network detections requiring continuous monitoring. Specific flags are implied through the use of "decoys" to evade detection, suggesting commands related to credential harvesting or lateral movement that mimic legitimate traffic.

### Network Topology & Relationships
*   **Attribution:** Confirmed by DHS/FBI (Dec 2016) and FireEye as being sponsored by the **Russian Government**.
*   **Key Targets & Events:**
    *   **OSCE:** Confirmed breach in November 2016.
    *   **German CDU:** Targeted in May 2016.
    *   **DNC:** June 2016 breach attributed to the Russian Government.
    *   **WADA:** Investigated in the context of the 2016 Olympic doping scandal.
*   **Geographic Scope:** US, Europe, and former Soviet Union nations.
*   **Organizational Focus:** Governments, militaries, defense attaches, media, and political parties (e.g., German Christian Democratic Union).

## Extracted Operational Steps & Workflows
- 1. 	
Gauquelin, Blaise. “La Russie soupçonnée d’être responsable d’un piratage informatique contre l’OSCE.” Le Monde. 28 Dec. 2016. Web. 29 Dec. 2016.
- 2. 	
Trend Micro refers to activity corresponding to FireEye’s APT28 as “Pawn Storm.”
- 3. 	
Hacquebord Feike. “Pawn Storm Targets German Christian Democratic Union.” Trend Micro. 11 May 2016. Web. 29 Dec. 2016.
- 4. 	
Hacquebord Feike. “Pawn Storm’s Domestic Spying Campaign Revealed; Ukraine and US Top Global Targets.” TrendLabs Security Intelligence Blog, Trend Micro. 18 August 2015. Web. 29 Dec.  2016.
- 5. 	
“Neuer Hackerangriff auf Bundespolitiker / BSI warnt Parteien vor Cyberangriffen.” Westdeutscher Rundfunk. 20 Sept. 2016. Web. 29 Dec. 2016.
- 8.	 “WADA Confirms Attack by Russian Cyber Espionage Group.” World Anti-Doping Agency. 13 Sept. 2016. Web. 29 Dec. 2016.
- 9.	 Fancy Bears’ HT (fancybears). “@AnonPress Greetings. We hacked #WADA. We have Proof of American Athletes taking doping. Fancybear.net.” 12 Sept. 2016, 4:12 PM. Tweet.
- 10.	 CrowdStrike refers to activity corresponding to FireEye’s APT28 and APT29 as “Fancy Bear” and “Cozy Bear,” respectively.
- 11. 	 “Nakashima, Ellen. “Cyber Researchers Confirm Russian Government Hack of Democratic National Committee.” The Washington Post. 20 June 2016. Web. 29 Dec. 2016.
- 12. 	 “Rid, Thomas. “All Signs Point to Russia Being Behind the DNC Hack.” Motherboard, Vice. 25 July 2016. Web. 29 Dec. 2016.
- 13.  	 “Bennett, Cory. “Guccifer 2.0 Drops More DNC Docs.” Politico. 13 Sept. 2016. Web. 2 Jan. 2017. <>
- 14.	 Perlroth, Nicole. Shear, Michael D. “Private Security Group Says Russia was Behind John Podesta’s Email Hack.” The New York Times. 21 Oct. 2016. Web. 2 Jan. 2017.
- 15. 	 “Franceschi-Bicchierai, Lorenzo. “How Hackers Broke Into John Podesta and Colin Powell’s Gmail Accounts.” 20 Oct. 2016. Web. 2 Jan. 2017.
- 16.	 “Nakashima, Ellen. “FBI Probes Suspected Breach of Another Democratic Organization by Russian Hackers.” The Washington Post. 29 July 2016. Web. 29 Dec. 2016.
- 17. 	 “Pelosi, Nancy. “DCCC Cyber Breach.” 13 August 2016. Email. U.S. House of Representatives. Washington, DC. Politico. Web. 29 Dec. 2016.
- 18. 	 “Lipton, Eric. Shane, Scott. “Democratic House Candidates Were Also Targets of Russian Hacking.” The New York Times. 13 Dec. 2016. Web. 29 Dec. 2016.
- 19. 	 Ibid.
- 20.	 Gallagher, Sean. “Guccifer 2.0 Posts DCCC Docs, Says They’re From Clinton Foundation.” Ars Technica. 4 Oct. 2016. Web. 3 Jan. 2017.
- 21.	 “Russian Hackers Suspected in French TV Cyberattack.” Deutsche Welle. 6 Oct. 2015. Web. 29 Dec. 2016.
- 22.	 Joselow, Gabe. “Election Cyberattacks: Pro-Russia Hackers Have Been Accused in Past.” NBC News. 3 Nov. 2016. Web. 29 Dec. 2016.
- 23. 	Clayton, Mark. “Ukraine Election Narrowly Avoided ‘Wanton Destruction’ From Hackers (+Video).” The Christian Science Monitor. 17 June 2014. Web. 2 Jan. 2017.
- 24. “Foundation Board Media Release: WADA Strengthens Anti-Doping Worldwide.” World Anti-Doping Agency. 18 November 2015.
- 25. 	“Russia State-Sponsored Doping Across Majority of Olympic Sports, Claims Report.” The BBC. 18 July 2016. Web. 29 Dec. 2016.
- 26.	 Macguire, Eoghan. Almasy, Steve. “271 Russian Athletes Cleared for Rio Games.” CNN. 5 August 2016. Web. 29 Dec. 2016.
- 27. 	“Cyber Security Update: WADA’s Incident Response.” World Anti-Doping Agency. 5 Oct. 2016. Web. 3 Jan. 2017.
- 28. 	“WADA Confirms Attack by Russian Cyber Espionage Group.” World Anti-Doping Agency. 13 Sept. 2016.
- 29.	 “WADA Confirms Another Batch of Athlete Data Leaked by Russian Cyber Hackers ‘Fancy Bear.’” World Anti-Doping Agency. 14 Sept. 2016. Web. 29 Dec. 2016. <>
- 30.	 [OP PL]. “www.tas-cas.org.” Online video clip. YouTube. YouTube, 9 Aug. 2016. Web. 3 Jan. 2017.
- 31. 	 Anonymous Poland (@anpoland). “@Cryptomeorg @ben_rumsby @PogoWasRight @Jason_A_Murdock @Cyber_War_News @kevincollier Tomorrow will ddos WADA and publish some secret dosc.” 11 Aug 2016 10:10
- 32. 	Anonymous Poland (@anpoland). “@JoeUchill within a few days will be new attack on the WADA/Olimpic.” 5 Sept. 2016 5:19 AM. Tweet.
- 33.	 Fancy Bears’ HT (fancybears). “@AnonPress Greetings. We hacked #WADA. We have Proof of American Athletes taking doping. Fancybear.net.”
- 34.	 Ibid.
- 35. 	“WADA Confirms Attack by Russian Cyber Espionage Group.”World Anti-Doping Agency.13 Sept. 2016.
- 36.	 Russian Hackers Leak Simone Biles and Serena Williams Files.” The BBC. 13 Sept. 2016. Web. 29 Dec. 2016.
- 37.	 Rumsby, Ben. “US Superstars Serena and Venus Williams and Simone Biles Given Drugs Exemption, Russian Hackers Reveal.” The Telegraph. 14 Sept. 2016. Web. 29 Dec. 2016.
- 38.	 Luhn, Alec.”Fancy Bears Origins Unclear But Russia Seizes Chance to Put Boot into Wada.” 15 Sept. 2016. Web. 29 Dec. 2016.
- 39. 	Gibson, Owen. “Russian Sports Minister Vitaly Mutko Denies Link to Wada Hackers.” The Guardian. 14 Sept. 2016. Web. 29 Dec. 2016.

<!-- CORA-MAXIMIZED-COMMANDS-START -->
## Maximized Windows & Linux Command Examples for `APT28-Center-of-Storm-2017 MANDIANT`

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
