---
title: "Trained Knowledge & Topology: Cyber Forensics Intro Guide_updated_table.pdf"
tags:
  - active_enum
  - arp
  - credential_access
  - defense_evasion_firewall
  - enumeration
  - http
  - https
  - iptables
  - john
  - kerberos
  - mdp
  - netstat
  - nmap
  - passive_enum
  - pdf
  - powershell
  - privilege_escalation
  - pslist
  - responder
  - serial
  - trained
source_file: Cyber Forensics Intro Guide_updated_table.pdf
doc_type: pdf
updated: 2026-10-24 00:58:20
---

# Trained Knowledge & Architecture: `Cyber Forensics Intro Guide_updated_table.pdf`

- **Source Path:** `~/Projects/CORA/Training/Cyber Forensics Intro Guide_updated_table.pdf` (`pdf`)
- **Extracted Technical Entities:** `arp, http, https, iptables, john, kerberos, netstat, nmap, powershell, pslist, responder, serial, splunk, ssh, sysinternals, tcpdump, tshark, volatility, wireshark, wmic`
- **Extracted IPs / Subnets:** `172.16.157.136`
- **Extracted Interfaces:** `None`
- **Linked Command Playbook:** [[commands/trained_cyber_forensics_intro_guide_updated_table]] (`17` CEGAR-verified commands | `17` MDP transitions)

## Command & Tactic Coverage Summary
- **Total CEGAR-Verified Commands:** `17` (full executable list in [[commands/trained_cyber_forensics_intro_guide_updated_table]])
- **Tactic Distribution:** `Passive_Enum` (6), `Privilege_Escalation` (6), `Enumeration` (2), `Active_Enum` (1), `Credential_Access` (1), `Defense_Evasion_Firewall` (1)
- **Top Extracted CLI Tools:** `chmod` (4), `crontab` (3), `find` (3), `volatility` (3), `and` (1), `at` (1), `traceroute` (1), `tracert` (1)

### Visual & Network Diagram Intelligence (`Cyber Forensics Intro Guide_updated_table.pdf#page45`)
- **Spatially Grouped Diagram Nodes (Box/Component Clusters):**
  1. `[RegistryEditor | FileEdit | View | Favorites | Computer | D | HKEY_CLASSES_ROOT]`
  2. `[Help | HKEY_CURRENT_USER]`
  3. `[AppEvents | Console | ControlPanel | Environment | EUDC | Identities]`
  4. `[Keyboard Layout | Network | Printers | Software | System | VolatileEnvironment]`
  5. `[HKEY_LOCAL_MACHINE | HKEY_USERS | .DEFAULT | S-1-5-18 | S-1-5-19 | S-1-5-20]`
  6. `[S-1-5-21-4123892437-111928464-3716307427-1002 | AppEvents | Console | Control Panel]`
  7. `[Environment | EUDC | Identities | Keyboard Layout | Network | Printers]`
  8. `[Software | System | VolatileEnvironment]`
  9. `[Figure 2-14: HKCU VS HKU]`
  10. `[PAGE 43]`

### Visual & Network Diagram Intelligence (`Cyber Forensics Intro Guide_updated_table.pdf#page47`)
- **Spatially Grouped Diagram Nodes (Box/Component Clusters):**
  1. `[kTask xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task"> | <Author>S(@&systemroote\system32\regidle.dll,-600)</Author> | <Source>$(@&systemroot+\system32\regidle.dll,-601)</Source> | <URI>Microsoft\Windows\Registry\RegIdleBackup</URI>]`
  2. `[<RegistrationInfo> | <Version>1.0</Version>]`
  3. `[<Description>S(@&svstemroot+\system32\regidle.dll,-602)</Description> | <SecurityDeSCriptor>O:BAG:BAD:P（A;;FA;;;BA)(A;;FA;;;SY)（A;;FR;;;IU)（A;]`
  4. `[</RegistrationInfo> | <Triggers/> | <Settings> | <Enabled>true</Enabled>]`
  5. `[<MultipleInstancesPolicy>IgmoreNew</MultipleInstancesPolicy> | <AllowStartOnDemand>true</AllowStartOnDemand> | <DisallowStartIfOnBatteries>true</DisallowStartIfOnBatteries> | <StopIfGoingOnBatteries>false</StopIfGoingOnBatteries> | <RunOnlyIfNetworkAvailable>false</RunOnlyIfNetworkAvailable> | <ExecutionTimeLimit>PToS</ExecutionTimeLimit>]`
  6. `[<Hidden>true</Hidden> | <WakeToRun>false</WakeToRun> | <StartWnenAvailable>true</StartWnenAvailable> | <Priority>5</Priority> | <RunOnlyIfIdle>false</RunOnlyIfIdle> | <MaintenanceSettings>]`
  7. `[<UseUnifiedSchedulingEngine>true</UseUnifiedSchedulingEngine>]`
  8. `[Period>P10D</Period> | <Deadline>P14D</Deadline> | </MaintenanceSettings> | </Settings> | <Principals> | <Principal id="LocalSystem"> | <UserId>S-1-5-18</UserId>]`
  9. `[</Principal> | </Principals> | <Actions Context="LocalSystem | <ComHandler> | </ComHandler>]`
  10. `[<C1assId>{ca767aa8-9157-4604-b64b-40747123d5f2)</ClassId>]`
  11. `[</Actions> | </Task>]`
  12. `[Figure 2-15: The registry backup task in Windows]`
  13. `[PAGE 45]`

## LLM Distilled Operational Summary
### Operational Techniques & Decision Workflows
- **Registry Analysis Workflow**: Identify user-specific (`HKCU`) vs. system-wide (`HKU`, `HKEY_LOCAL_MACHINE`) registry hives to distinguish between interactive user activity and system-level persistence.
- **Scheduled Task Forensics**: Extract task XML metadata (Author, Source, URI, Security Descriptor) to reconstruct automated execution chains, specifically targeting maintenance tasks like `RegIdleBackup`.
- **File System Carving Strategy**: Navigate the hard drive hierarchy from the Master Boot Record (MBR) and Partition Boot Sector down to the Filesystem Area, focusing on the Master File Table (MFT) and unallocated space for file carving operations.

### Critical Command Patterns & Required Flags
- **Registry Hive Inspection**: Use `reg query` or `regedit` to traverse clusters like `HKEY_CLASSES_ROOT`, `HKEY_CURRENT_USER`, and `HKEY_USERS` (specifically SIDs `S-1-5-18`, `S-1-5-19`, `S-1-5-20`).
- **Task Scheduler Parsing**: Utilize XML parsing tools to read `<RegistrationInfo>`, `<Triggers>`, and `<Actions>` elements within `.xml` files located in `%SystemRoot%\System32\Tasks`.
- **NTFS/MFT Analysis**: Target the `Master File Table (MFT)` and scan `Unallocated Space` for residual data fragments using file carving techniques.

### Network Topology & Service Relationships
- **System Identity Mapping**: Correlate Security Identifiers (SIDs) with service roles:
  - `S-1-5-18`: Local System (High Privilege/Service Context).
  - `S-1-5-19` / `S-1-5-20`: First and Second Interactive Logon Users.
- **Task Execution Context**: The `RegIdleBackup` task runs under `LocalSystem` (`UserId: S-1-5-18`) with a 10-day period (`P10D`) and a 14-day deadline (`P14D`), executing the `regidle.dll` handler.
- **Environment Clusters**: Grouping of `Environment`, `EUDC`, `Identities`, and `VolatileEnvironment` suggests a workflow for analyzing volatile state persistence and user environment configuration.

## Document Structure & Key Topics
- A note to the reader (p. 11)
- Digital forensic goals (p. 13)
- Hard drive structure (p. 15)
- Master boot record (p. 15)
- Partition boot sector (p. 16)
- The filesystem area in partition (p. 16)
- Data area (p. 16)
- The FAT filesystem (p. 17)
- FAT components (p. 17)
- FAT limitations (p. 19)
- The NTFS filesystem (p. 19)
- NTFS components (p. 19)
- Master File Table (MFT) (p. 20)
- Unallocated Space and File Carving (p. 20)
- File systems (p. 20)
- Allocated and unallocated space (p. 21)
- Data persistence (p. 21)
- How magnetic hard drives store data (p. 21)
- File Carving (p. 27)
- Alternate data streams (p. 28)
- Windows File Structure (p. 28)
- Hidden files and folders (p. 30)
- Executable file types on windows (p. 31)
- Programs (p. 31)
- Scripts (p. 32)
- Shortcuts (p. 32)
- Other (p. 33)
- Office Macros (p. 33)
- Windows PATH variable (p. 33)
- Windows Timestamps (p. 34)
- The Windows Registry (p. 36)
- The registry structure (p. 36)
- Root keys (p. 37)
- HKEY_CLASSES_ROOT or HKCR (p. 38)
- HKEY_LOCAL_MACHINE (p. 39)
- HKEY_USERS or HKU (p. 40)
- HKEY_CURRENT_USER or HKCU (p. 42)
- Mapping a hive to the filesystem (p. 44)
- Backing up the registry files (p. 44)
- Further Reading (p. 46)
- Event Logs structure (p. 48)
- Security Event Logs (p. 50)
- Important Event Logs (p. 52)
- Logon Types (p. 54)
- SYSMON (p. 55)
- Overview of Sysmon Capabilities (p. 56)
- Sysmon Event IDs (p. 56)
- What is Active Directory (p. 61)
- AD Objects (p. 61)
- Major features in Active Directory Domain Services (p. 62)
- Active Directory versus Workgroup (p. 65)
- Windows Accounts (p. 65)
- Domain vs local (p. 65)
- SID vs RID (p. 66)
- Common SIDs (p. 67)
- Windows prefetch files (p. 68)
- Prefetch file analysis (p. 69)
- LNK files (p. 70)
- System Resource Usage Monitor (SRUM) (p. 72)
- Jump lists (p. 72)
- ThumbCache (p. 73)
- Startup Folder (p. 73)
- ShimCache (p. 73)
- AmCache (p. 74)
- Web Activity (p. 75)
- Cookies (p. 75)
- Internet History (p. 76)
- Browser Cache (p. 77)
- Chat Programs (p. 78)
- Typed URLs (p. 79)
- Autocomplete (p. 79)
- Session Restore (p. 79)
- Downloads (p. 80)
- Registry Keys (p. 80)
- Open/Save MRU (p. 81)
- UserAssist (p. 81)
- RecentApps (p. 82)
- Last-Visited MRU (p. 82)
- WordWheelQuery (p. 82)
- Registry persistence (p. 83)
- Wireless devices connected (p. 85)
- Mounted devices/USBs connected (p. 86)
- Network Shares connected (p. 87)
- Lateral Movement (p. 87)
- Remote Desktop (p. 88)
- Mapping Network Shares (p. 89)
- PsExec (p. 90)
- Scheduled Tasks (p. 92)
- Services (p. 93)
- WMI/WMIC (p. 94)
- Powershell Remoting (p. 95)
- Persistence (p. 97)
- Account Manipulation (p. 97)
- Boot or Logon AutoStart Execution (p. 98)
- Logon Scripts (p. 99)
- Create Account (p. 100)
- Services (p. 100)
- Scheduled Tasks (p. 101)
- Windows Memory Forensics (p. 103)
- Memory Structure (p. 103)
- Sources of Memory Dumps (p. 103)
- Hibernation file (p. 103)
- Crash dump (p. 104)
- Page Files (p. 104)
- Windows Boot Process (p. 105)
- System (p. 107)
- Smss.exe (p. 107)
- Csrss.exe (p. 107)
- Wininit.exe (p. 107)
- Services.exe (p. 108)
- Svchost.exe (p. 108)
- RuntimeBroker.exe (p. 108)
- Taskhostw.exe (p. 109)
- Lsaiso.exe (p. 109)
- Lsass.exe (p. 109)
- Winlogon.exe (p. 109)
- Explorer.exe (p. 110)
- Processes in Memory (p. 110)
- Network Connections in Memory (p. 111)
- DLL Injection (p. 111)

## Extracted Operational Steps & Workflows
- 1. What is Digital Forensics ........................................................................................................................ 12
- 2. Windows File System .............................................................................................................................. 15
- 3.  Windows Event Logs ............................................................................................................................. 47
- 4.  Active Directory...................................................................................................................................... 61
- 5.  Forensically Relevant Windows Files .................................................................................................. 68
- 6. 
Windows Memory Forensics ............................................................................................................ 103
- 7.  Linux File System................................................................................................................................... 118
- 8.  Forensically relevant Linux artifacts .................................................................................................. 144
- 9.  Linux Memory Forensics ......................................................................................................................173
- 10.  Network Forensics .............................................................................................................................. 199
- 1. What is Digital Forensics
- 2. Windows File System
- 6.

--- [Page 28] ---
- 3.  Windows Event Logs
- 70. These event logs can be found at the following location:
- 4.  Active Directory
- 5.  Forensically Relevant Windows Files
- 1. The original path of the file
- 2. MAC times of the original file; not only will a LNK file contain timestamps for
- 3. Information about the volume and system where the LNK file is stored. This will
- 4. Network details if the file was stored on a network share or remote computer
- 5. File size of the linked file
- 6.   Windows Memory Forensics
- 7.  Linux File System
- 1.  It starts a secure random-number generator, to provide random numbers for use in
- 2.  If the /var/dumps directory exists, rc.sysinit starts the dumper utility to capture (in
- 3.  If /etc/host_cfg/$HOSTNAME/rc.d/rc.local exists and is executable, rc.sysinit runs it.
- 4.  Finally, rc.sysinit runs tinit.  By default, rc.sysinit tells tinit to use text mode.
- 1. BIOS – Basic Input/Output System executes MBR
- 2. MBR – Master Boot Record execute GRUB
- 3. GRUB – Grand Unified Bootloader executes Kernel
- 4. Kernel – Kernel executes /sbin/init
- 5. Init – Init executes runlevel programs
- 6. Runlevel – Runlevel programs are executed from /etc/rc.d/rc*.d/
- 8.  Forensically relevant Linux artifacts
- 4.  However, every part of the rootkit and hidden directory is subject to change in later
- 9.  Linux Memory Forensics
- 1. Read “task_struct” process structure to determine where the “mm_struct” is located in
- 2. Read the “mm_struct” structure to determine the start and end addresses of the
- 3. Extract the pages associated with the ELF executable and combine them into a single
- 10.  Network Forensics
- 1.   Switch off device and turn off its power supply.
- 2.  Disconnect the cables and pack the device in proper anti-static packing material.
- 3.  Fill the chain of custody form – which is the official documentation form used by law
- 1. Dynamic Host Configuration Protocol (DHCP): Before sending any data on the

