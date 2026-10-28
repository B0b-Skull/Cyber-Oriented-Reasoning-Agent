---
title: "Trained Knowledge & Topology: BCF_Windows Live Response.pdf"
tags:
  - auditpol
  - covert_infil
  - defense_evasion_firewall
  - enumeration
  - ipconfig
  - lateral_movement_routing_pivot
  - mdp
  - netsh
  - netstat
  - passive_enum
  - pdf
  - post_exploitation_verification
  - powershell
  - reconnaissance
  - responder
  - trained
  - wevtutil
source_file: BCF_Windows Live Response.pdf
doc_type: pdf
updated: 2026-10-24 00:56:53
---

# Trained Knowledge & Architecture: `BCF_Windows Live Response.pdf`

- **Source Path:** `~/Projects/CORA/Training/BCF_Windows Live Response.pdf` (`pdf`)
- **Extracted Technical Entities:** `auditpol, ipconfig, netsh, netstat, powershell, responder, wevtutil`
- **Extracted IPs / Subnets:** `None`
- **Extracted Interfaces:** `None`
- **Linked Command Playbook:** [[commands/trained_bcf_windows_live_response]] (`52` CEGAR-verified commands | `52` MDP transitions)

## Command & Tactic Coverage Summary
- **Total CEGAR-Verified Commands:** `52` (full executable list in [[commands/trained_bcf_windows_live_response]])
- **Tactic Distribution:** `Passive_Enum` (31), `Enumeration` (7), `Covert_Infil` (6), `Defense_Evasion_Firewall` (3), `Post_Exploitation_Verification` (2), `Reconnaissance` (2), `Lateral_Movement_Routing_Pivot` (1)
- **Top Extracted CLI Tools:** `get-childitem` (6), `dir` (5), `net` (4), `get-help` (3), `get-wmiobject` (3), `netstat` (3), `reg` (2), `wevtutil` (2), `auditpol` (1), `copy-item` (1), `date` (1), `fsutil` (1), `get-computerinfo` (1), `get-date` (1), `get-eventlog` (1), `get-itemproperty` (1), `get-logproperties` (1), `get-netfirewallprofile` (1), `get-nettcpconnection` (1), `get-process` (1), `get-service` (1), `ipconfig` (1), `netsh` (1), `new-psdrive` (1), `schtasks` (1)

### Visual & Network Diagram Intelligence (`BCF_Windows Live Response.pdf#page1`)
- **Spatially Grouped Diagram Nodes (Box/Component Clusters):**
  1. `[ICHIRON | TRAINING]`
  2. `[Basic Computer Forensics | 26-28Mar2018 | DISCOVERYANDCOUNTER-INFILTRATIONPROFESSIONALTM(DCIP)TM]`

### Visual & Network Diagram Intelligence (`BCF_Windows Live Response.pdf#page2`)
- **Spatially Grouped Diagram Nodes (Box/Component Clusters):**
  1. `[Incident Response]`
  2. `[OVERVIEW]`

### Visual & Network Diagram Intelligence (`BCF_Windows Live Response.pdf#page5`)
- **Diagram Ports / Services:** `:24, :35`
- **Spatially Grouped Diagram Nodes (Box/Component Clusters):**
  1. `[WCHIRON | TRAINING]`
  2. `[Run as Administrator]`
  3. `[ComputerUNTITLED (E:)WIN7 | Open | Burn | New folder | Name | C=4. | Open]`
  4. `[Search WIN7 | Date modified | Size | Type | 10 7:24 AM | Application]`
  5. `[Organize | Desktop | Downloads | Recent Places | Libraries | Documents]`
  6. `[口 | 337KB]`
  7. `[Run as administrator | SkyDrive Pro | Troubleshoot compatibility | Add to archive... | Add to "cmd.rar" | Compress and email... | Compress to "cmd.rar" and email]`
  8. `[Music | Pictures | Videos | Computer | Local Disk (C:) | UNTITLED (E:)]`
  9. `[Send to | Copy | Paste | Create shortcut | Delete]`
  10. `[.fseventsd | Spotlight-V100 | .Temporarylter | .Trashes | DCIM | WIN7 | Shared Folders]`
  11. `[Rename | Properties | Date modified: 11/20/2010 7:24 AM | Size: 337 KB]`
  12. `[cmd | Application | Basic Computer Forensics]`
  13. `[Date created: 11/20/2012 1:35 PM]`
  14. `[DISCOVERYANDCOUNTER-INFILTRATION | PROFESSIONALTM(DCIP)TM | 2016 CHIRON TECHNOLOGY SERVICES, INC]`
  15. `[Any unauthorized use or disclosure of this material is strictly prohibited.]`

## LLM Distilled Operational Summary
### Operational Techniques & Decision Workflows
*   **Live System Preservation:**
    *   **Imaging:** Create a bit-for-bit, unmodified copy. If time permits, create multiple copies.
    *   **Data Transfer:** Always copy data to an external, trusted device before analysis.
    *   **Minimization:** Minimize interaction with the target system to prevent footprint changes (file system/registry modifications).
    *   **GUI Usage:** Avoid Graphical User Interfaces (GUIs) as they alter the target application state; use Command Line Interfaces (CLI) instead.
    *   **Sleep State Handling:** Wake laptops via touchpad or desktops via mouse movement. Photograph the screen and save open documents without closing applications.
*   **Scripting & Output:** Create custom scripts for the target OS and redirect all command outputs to an external device (e.g., `ipconfig.exe > e:\target1\incidentresponse.txt`).
*   **Tool Selection:** Use trusted, "bring your own" tools. Prefer PowerShell over `cmd` for functionality, but support pre-Windows 7 systems.

### Critical Command Patterns & Required Flags
*   **Directory Navigation:**
    *   PowerShell: `Set-Location <path>`
    *   CMD: `cd <path>`
*   **Directory Listing:**
    *   PowerShell: `Get-ChildItem <path>`
    *   CMD: `dir <path>` (Omit path to list current directory).
*   **Sorting by Modification Time:**
    *   PowerShell: `Get-ChildItem <path> | Sort-Object LastWriteTime`
    *   CMD: `dir /od <path>` (Reverse order: `dir /od`).
*   **Help Retrieval:**
    *   CMD: `<command> /?`
    *   PowerShell: `Get-Help <command>`, `-Examples`, or `-Full`.

### Network Topology & Service Relationships
*   **Diagram Ports/Services:** The document explicitly notes ports **:24** and **:35** in the context of network diagram intelligence.
*   **System Context:**
    *   **OS Versions:** Procedures cover both Windows 7 (specifically mentioned in file paths like `Computer\UNTITLED (E:)WIN7`) and pre-Windows 7 environments.
    *   **File System Artifacts:** Specific folders and files noted include `.fseventsd`, `Spotlight-V100`, `.TemporaryItems`, `.Trashes`, `DCIM`, and `Shared Folders`.
    *   **User Environment:** Standard Windows 7 user directories such as `Desktop`, `Documents`, `Downloads`, `Music`, `Pictures`, and `Videos` are relevant for analysis.
*   **Organization Structure:**
    *   **Training Provider:** ICHIRON / WCHIRON.
    *   **Course Title:** Basic Computer Forensics (26-28 Mar 2018).
    *   **Certification:** DISCOVERY AND COUNTER-INFILTRATION PROFESSIONAL™ (DCIP)™.
    *   **Vendor:** 2016 CHIRON TECHNOLOGY SERVICES, INC.

## Document Structure & Key Topics
- Visual & Network Diagram Intelligence (`BCF_Windows Live Response.pdf#page1`)
- Visual & Network Diagram Intelligence (`BCF_Windows Live Response.pdf#page2`)
- Visual & Network Diagram Intelligence (`BCF_Windows Live Response.pdf#page5`)

