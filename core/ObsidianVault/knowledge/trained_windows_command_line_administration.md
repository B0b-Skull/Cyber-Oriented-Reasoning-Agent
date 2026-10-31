---
title: "Trained Knowledge & Topology: windows command line Administration"
category: knowledge
domain_hub: "[[knowledge/01_windows_system_process_and_sysinternals]]"
os_platform: windows
primary_tactic: Passive_Enum
summary: "Operational architecture, decision workflows & Windows/Linux command reference for windows command line Administration: Windows live incident response, process tree/PPID investigation, service binary auditing, kernel architecture, file searching (fin"
when_to_apply: "Apply when working with windows command line Administration (windows): Apply when performing initial Windows host triage (s_init_unknown), investigating running processes/PPIDs, mapping svchost.exe services, hunting unsigned/injected DLLs, searching files by timestamp/content, or executing Sysinternals live response."
tags: [active_enum, auditpol, bcdedit, covert_exfil, credential_access, defense_evasion_firewall, dsquery, enumeration, http, https, icacls, ipconfig, john, kerberos, lateral_movement_routing_pivot, mdp, netsh, netstat, passive_enum, pdf, post_exploitation_verification, serial]
source_file: "windows command line Administration"
updated: 2026-10-30
---

# Trained Knowledge & Architecture: `windows_command_line_Administration.pdf`

- **Source Path:** `~/Projects/CORA/Training/windows_command_line_Administration.pdf` (`pdf`)
- **Extracted Technical Entities:** `auditpol, bcdedit, dsquery, http, https, icacls, ipconfig, john, kerberos, netsh, netstat, serial, ssl, wevtutil, wmic`
- **Extracted IPs / Subnets:** `127.0.0.1, 172.24.0.244`
- **Extracted Interfaces:** `None`
- **Linked Command Playbook:** [[commands/trained_windows_command_line_administration]] (`332` CEGAR-verified commands | `332` MDP transitions)

## Command & Tactic Coverage Summary
- **Total CEGAR-Verified Commands:** `332` (full executable list in [[commands/trained_windows_command_line_administration]])
- **Tactic Distribution:** `Passive_Enum` (123), `Enumeration` (91), `Defense_Evasion_Firewall` (35), `Credential_Access` (27), `Active_Enum` (24), `Post_Exploitation_Verification` (12), `Privilege_Escalation` (12), `Covert_Exfil` (3), `Reconnaissance` (3), `Lateral_Movement_Routing_Pivot` (2)
- **Top Extracted CLI Tools:** `type` (48), `net` (32), `auditpol` (18), `script` (15), `wmic` (14), `dsquery` (11), `wevtutil` (11), `netsh` (10), `echo` (8), `fsutil` (8), `prompt` (8), `reg` (8), `schtasks` (8), `dsadd` (7), `dsget` (7), `dsmod` (7), `icacls` (7), `locate` (7), `bcdedit` (6), `cmdkey` (6), `groups` (6), `sfc` (6), `openfiles` (5), `xcopy` (5), `cscript` (4)

### Visual & Network Diagram Intelligence (`windows_command_line_Administration.pdf#page1`)
- **Spatially Grouped Diagram Nodes (Box/Component Clusters):**
  1. `[John Mueller | Microsoft" | Windows]`
  2. `[Command-Line | Administration]`
  3. `[INSTANT | REFERENCE]`
  4. `[Quick&EasyLookup | ·Real-World Solutions | Answers onthe Spot]`
  5. `[55 | 5 | 50]`
  6. `[40 | 35 | 30]`
  7. `[SYBEX]`
  8. `[SERIOUS SKILLS.]`

### Visual & Network Diagram Intelligence (`windows_command_line_Administration.pdf#page2`)

### Visual & Network Diagram Intelligence (`windows_command_line_Administration.pdf#page3`)
- **Spatially Grouped Diagram Nodes (Box/Component Clusters):**
  1. `[Windows? Command Line | Administration | Instant Reference]`
  2. `[JohnPaul Mueller]`
  3. `[WILEY | Wiley Publishing, Inc.]`

## Document Structure & Key Topics
- Visual & Network Diagram Intelligence (`windows_command_line_Administration.pdf#page1`)
- Visual & Network Diagram Intelligence (`windows_command_line_Administration.pdf#page2`)
- Visual & Network Diagram Intelligence (`windows_command_line_Administration.pdf#page3`)

## Extracted Operational Steps & Workflows
- 1. Command languages (Computer science)—Handbooks, manuals, etc. 2.  Microsoft Windows
- 1. Click the box in the upper left corner of the command window
- 2. Set the properties on each tab to meet speciﬁc needs, such as dis-
- 1. Open a command window.
- 2. Type a command such as CLS or Dir and press Enter.
- 3. Press the Up arrow.
- 4. Press Esc. The command processor clears the command from the
- 5. Type Cmd and press Enter. You’ve just created a new command pro-
- 6. Press the Up arrow. You don’t see anything because this command
- 7. Now, type a different command (such as CLS or Dir) and press
- 8. Press the Up arrow. You’ll see the command you just typed, but
- 9. Press Esc to clear the command.
- 10. Type Exit and press Enter to close the current command proces-
- 11. Press the Up arrow twice and you’ll see whatever command you
- 12. Press Esc to clear the command.
- 13. Type Cmd and press Enter. This action creates a new command pro-
- 14. Press the Up arrow.
- 15. Type Exit and press Enter. You return to the first command
- 16. Type Exit again and press Enter; the command processor window
- 1. Type Net฀User฀YourLoginName฀YourPassword฀/Add and press Enter.
- 2. Type Net฀LocalGroup฀“Administrators”฀YourLoginName฀/Add and
- 3. Type WMIC฀ComputerSystem฀Where฀Name=”%COMPUTERNAME%”฀Call฀
- 4. Type WMIC฀ComputerSystem฀Where฀Name=”%COMPUTERNAME%”฀Call฀
- 5. Type WMIC฀RDToggle฀Where฀ServerName=”%COMPUTERNAME%”฀Call฀
- 6. Type NetSH฀Firewall฀Set฀PortOpening฀TCP฀3389฀“Remote฀Desktop”
- 7. Type Net฀Share฀“Drive_C”=C:\ and press Enter.
- 8. Type CScript฀//H:CScript and press Enter.
- 9. Type SLMGR฀–ATO and press Enter.
- 10. Type Shutdown฀/r and press Enter.
- 1. Choose Start ➢ Control Panel or Start ➢ Settings ➢ Control
- 2. Click System and Security, and then Allow Remote Access in the
- 3. On older systems, check the Enable Remote Desktop on
- 4. Click OK. Windows makes Remote Desktop access available to
- 1. Start the application and click Options.
- 2. Type the server name or select it from the drop-down list in the
- 3. Type your account name on the server in the User Name ﬁeld.
- 4. (Optional) Type your password in the Password ﬁeld (when this
- 5. (Optional) Type the name of the server in the Domain ﬁeld when
- 6. (Optional) Check Allow Me to Save Credentials (or Save My
- 7. Select the Display tab.
- 8. (Optional) Select the Local Resource tab. Make any settings
- 9. (Optional) Select the Programs tab. Check Start the Following
- 10. Select the Experience tab. Choose the connection speed for your
- 11. Clear the checkmarks next to every feature you don’t really need,
- 12. Select the Advanced tab, if your version of Remote Desktop pro-

## Extracted Reference Excerpt
John Mueller
Microsoft"
Windows
Command-Line
Administration
INSTANT
REFERENCE
Quick&EasyLookup
55
5
50
·Real-World Solutions
Answers onthe Spot
40
35
30
SYBEX
SERIOUS SKILLS.

--- [Page 3] ---
Windows
® Command Line 
Administration
Instant Reference
John Paul Mueller

Windows? Command Line
Administration
Instant Reference
JohnPaul Mueller
WILEY
Wiley Publishing, Inc.

--- [Page 4] ---
Acquisitions Editor: Agatha Kim
Development Editor: Jennifer Leland
Technical Editor: Russ Mullen
Production Editor: Liz Britten, Eric Charbonneau
Copy Editor: Cheryl Hauser
Editorial Manager: Pete Gaughan
Production Manager: Tim Tate
Vice President and Executive Group Publisher: Richard Swadley
Vice President and Publisher: Neil Edde
Book Designer: Maureen Forys, Happenstance Type-O-Rama
Compositor: JoAnn Kolonick, Happenstance Type-O-Rama
Proofreader: Jen Larsen, Word One
Indexer: Ted Laux
Project Coordinator, Cover: Lynsey Stanford
Cover Designer: Ryan Sneed
Cover Image: iStockphoto
Copyright © 2010 by Wiley Publishing, Inc., Indianapolis, Indiana
Published simultaneously in Canada
ISBN: 978-0-470-65046-2
No part of this publication may be reproduced, stored in a retrieval system or transmitted in any 
form or by any means, electronic, mechanical, photocopying, recording, scanning or otherwise, 
except as permitted under Sections 107 or 108 of the 1976 United States Copyright Act, without 
either the prior written permission of the Publisher, or authorization through payment of the 
appropriate per-copy fee to the Copyright Clearance Center, 222 Rosewood Drive, Danvers, MA 
01923, (978) 750-8400, fax (978) 646-8600. Requests to the Publisher for permission should be 
addressed to the Permissions Department, John Wiley & Sons, Inc., 111 River Street, Hoboken, NJ 
07030, (201) 748-6011, fax (201) 748-6008, or online at http://www.wiley.com/go/permissions.
Limit of Liability/Disclaimer of Warranty: The publisher and the author make no representations 
or warranties with respect to the accuracy or completeness of the contents of this work and 
speciﬁcally disclaim all warranties, including without limitation warranties of ﬁtness for a particular 
purpose. No warranty may be created or extended by sales or promotional materials. The advice 
and strategies contained herein may not be suitable for every situation. This work is sold with the 
understanding that the publisher is not engaged in rendering legal, accounting, or other professional 
services. If professional assistance is required, the services of a competent professional person should 
be sought. Neither the publisher nor the author shall be liable for damages arising herefrom. The 
fact that an organization or Web site is referred to in this work as a citation and/or a potential source 
of further information do

<!-- CORA-MAXIMIZED-COMMANDS-START -->
## Maximized Windows & Linux Command Examples for `windows command line Administration`

> **Domain Hub:** [[knowledge/01_windows_system_process_and_sysinternals|Domain Hub 01: Windows Live Response, Processes, Services, Kernel & Sysinternals Suite]]  
> **Master Playbooks:** [[commands/windows_master_command_playbook]] | [[commands/linux_master_command_playbook]] | [[commands/curl_playbook]] | [[commands/tio_serial_playbook]]  
> **When to Apply:** Apply when performing initial Windows host triage (s_init_unknown), investigating running processes/PPIDs, mapping svchost.exe services, hunting unsigned/injected DLLs, searching files by timestamp/content, or executing Sysinternals live response.  
> **15-Engine H-MDP State Transition:** `s_init_unknown` $\xrightarrow{\text{Passive_Enum}}$ `s_passive_topology_mapped` | **Bayesian Root-Cause Triggers:** `suspicious_process_lineage, service_misconfiguration, unsigned_dll_injection, resource_exhaustion` | **Isolation:** `RED, BLUE, WHITE (100% local host telemetry compatible)`

| Primary Command (`Windows` / `Linux`) | OS / Shell | What It Does & Key Flags | When to Apply & Expected Output | Cross-Platform Equivalent |
| :--- | :--- | :--- | :--- | :--- |
| `systeminfo && whoami /all` | **Windows CMD** | Displays OS build, patch hotfixes (KBs), boot time, current user SID, group memberships, and token privileges (`SeDebugPrivilege`, `SeImpersonatePrivilege`). | Apply first on any Windows host (`s_init_unknown`) to establish OS baseline and privilege level. | `uname -a && id && sudo -l` |
| `tasklist /v && tasklist /svc` | **Windows CMD** | Lists all running processes with user context, memory, window titles (`/v`), and maps every `svchost.exe` PID to hosted Windows Service names (`/svc`). | Apply to identify which service inside `svchost.exe` owns a socket or high CPU thread. | `ps auxef && systemctl list-units --type=service --state=running` |
| `wmic process get ProcessId,ParentProcessId,Name,ExecutablePath,CommandLine /format:list` | **Windows CMD** | Extracts full process lineage (`PID` + `PPID`), binary disk path, and full command-line arguments for every process. | Apply to uncover hidden/encoded PowerShell arguments and anomalous parent-child process trees (e.g., `cmd.exe` spawned by `w3wp.exe`). | `ps -eo pid,ppid,user,args --forest` |
| `pslist -accepteula -t && psloggedon -accepteula` | **Sysinternals** | Prints hierarchical parent-child process tree (`-t`) and enumerates both local interactive and SMB network logon sessions. | Apply during live response to trace process trees and active user sessions. | `pstree -p -a && w` |
| `listdlls -accepteula -u && sigcheck -accepteula -e -u -vr C:\Windows\System32` | **Sysinternals** | Lists all unsigned DLLs (`listdlls -u`) loaded into running processes and scans `System32` for unsigned executables (`sigcheck -e -u`). | Apply when hunting DLL hijacking, process hollowing, or trojanized system binaries. | `grep -E '\.so' /proc/*/maps && debsums -c` |
| `handle -accepteula -a -u && tcpvcon -accepteula -a -c -n` | **Sysinternals** | Enumerates all open file/registry/mutant handles (`handle -a -u`) and dumps CSV socket-to-process mappings (`tcpvcon`). | Apply to identify malware mutexes (`BaseNamedObjects`), locked files, or进程-bound network sockets. | `lsof -i -P -n && lsof` |
| `sc query state= all && sc qc <ServiceName>` | **Windows CMD** | Lists all installed services (running/stopped) and inspects `BINARY_PATH_NAME`, `START_TYPE`, and `SERVICE_START_NAME`. | Apply to audit service binaries and check for unquoted service paths or writable service executables. | `systemctl status <service> && systemctl cat <service>` |
| `forfiles /p C:\ /s /m *.exe /d -7 /c "cmd /c echo @path @fdate @ftime"` | **Windows CMD** | Recursively (`/s`) locates executables modified within the last 7 days (`/d -7`) across drive `C:\`. | Apply during incident triage to find recently dropped binaries or staging scripts. | `find / -xdev -mtime -7 -type f -ls 2>/dev/null` |
| `findstr /s /i /n "password secret connectionString" C:\Users\*.txt C:\Users\*.ps1 C:\inetpub\*.config` | **Windows CMD** | Recursive (`/s`), case-insensitive (`/i`), line-numbered (`/n`) string search across text, script, and web config files. | Apply when auditing configuration files for plaintext credentials or API keys. | `grep -rnI -iE 'password\|secret' /var/www /home /etc 2>/dev/null` |
| `procdump -accepteula -ma <PID> C:\Temp\proc_<PID>.dmp` | **Sysinternals** | Captures a complete memory dump (`-ma`) of target process `<PID>` for strings/YARA/reverse engineering. | Apply before terminating a suspicious in-memory process so volatile unpacked strings and keys are preserved. | `gcore -o /tmp/proc_<PID> <PID>` |

### Copy-Pasteable Execution Block (Windows & Linux)
```bash
# [Windows CMD] Displays OS build, patch hotfixes (KBs), boot time, current user SID, group memberships, and token privileges (`SeDebugPrivilege`, `SeImpersonatePrivilege`).
systeminfo && whoami /all
# [Windows CMD] Lists all running processes with user context, memory, window titles (`/v`), and maps every `svchost.exe` PID to hosted Windows Service names (`/svc`).
tasklist /v && tasklist /svc
# [Windows CMD] Extracts full process lineage (`PID` + `PPID`), binary disk path, and full command-line arguments for every process.
wmic process get ProcessId,ParentProcessId,Name,ExecutablePath,CommandLine /format:list
# [Sysinternals] Prints hierarchical parent-child process tree (`-t`) and enumerates both local interactive and SMB network logon sessions.
pslist -accepteula -t && psloggedon -accepteula
# [Sysinternals] Lists all unsigned DLLs (`listdlls -u`) loaded into running processes and scans `System32` for unsigned executables (`sigcheck -e -u`).
listdlls -accepteula -u && sigcheck -accepteula -e -u -vr C:\Windows\System32
# [Sysinternals] Enumerates all open file/registry/mutant handles (`handle -a -u`) and dumps CSV socket-to-process mappings (`tcpvcon`).
handle -accepteula -a -u && tcpvcon -accepteula -a -c -n
```
<!-- CORA-MAXIMIZED-COMMANDS-END -->
