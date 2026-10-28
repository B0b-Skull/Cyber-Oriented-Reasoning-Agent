---
title: "Trained Knowledge & Topology: BCF_Windows Process Investigation.pdf"
tags:
  - mdp
  - netstat
  - passive_enum
  - pdf
  - post_exploitation_verification
  - powershell
  - trained
  - wmic
source_file: BCF_Windows Process Investigation.pdf
doc_type: pdf
updated: 2026-10-24 00:56:56
---

# Trained Knowledge & Architecture: `BCF_Windows Process Investigation.pdf`

- **Source Path:** `~/Projects/CORA/Training/BCF_Windows Process Investigation.pdf` (`pdf`)
- **Extracted Technical Entities:** `netstat, powershell, wmic`
- **Extracted IPs / Subnets:** `None`
- **Extracted Interfaces:** `None`
- **Linked Command Playbook:** [[commands/trained_bcf_windows_process_investigation]] (`8` CEGAR-verified commands | `8` MDP transitions)

## Command & Tactic Coverage Summary
- **Total CEGAR-Verified Commands:** `8` (full executable list in [[commands/trained_bcf_windows_process_investigation]])
- **Tactic Distribution:** `Passive_Enum` (7), `Post_Exploitation_Verification` (1)
- **Top Extracted CLI Tools:** `get-childitem` (2), `get-nettcpconnection` (1), `get-process` (1), `get-wmiobject` (1), `netstat` (1), `tasklist` (1), `wmic` (1)

### Visual & Network Diagram Intelligence (`BCF_Windows Process Investigation.pdf#page1`)
- **Spatially Grouped Diagram Nodes (Box/Component Clusters):**
  1. `[ICHIRON | TRAINING]`
  2. `[Basic Computer Forensics | 26-28Mar2018 | DISCOVERYANDCOUNTER-INFILTRATIONPROFESSIONALTM(DCIP)TM]`

### Visual & Network Diagram Intelligence (`BCF_Windows Process Investigation.pdf#page3`)
- **Spatially Grouped Diagram Nodes (Box/Component Clusters):**
  1. `[Vetting Process | Listings]`

## LLM Distilled Operational Summary
### Operational Techniques & Decision Workflows

*   **Process Vetting Workflow:**
    *   Pull a process listing (e.g., via `tasklist`).
    *   Eliminate known good Windows system processes.
    *   Conduct open-source research on unknown entries.
    *   Compare running processes against research data to identify anomalies.
*   **Attacker Blending Techniques to Detect:**
    *   Inverting characters in legitimate process names.
    *   Using legitimate names from different Windows versions.
    *   Using legitimate binaries located in wrong directories.
    *   High instance counts of `svchost.exe` or `csrss.exe`.
*   **Service Vetting Workflow:**
    *   Pull a service listing.
    *   Verify binary paths, execution context (System vs. Local/Network), and start modes (Boot vs. Manual).
    *   Cross-reference with known good service data.
*   **Malware Detection Indicators:**
    *   Presence of Command and Control (C2) network activity.
    *   Existence of a persistence mechanism to survive reboots.

### Critical Command Patterns & Required Flags

*   **Filtering Specific Processes:**
    *   `tasklist /FI "IMAGENAME eq <process_name>"` (e.g., `csrss.exe`)
*   **Inspecting `svchost.exe` Details:**
    *   **WMIC:** `wmic process where name="svchost.exe" get processId, commandline`
    *   **PowerShell:** `Get-WmiObject win32_process | Where {$_.name –eq 'svchost.exe' | select processid, commandline}`
*   **Inspecting Service Details:**
    *   **PowerShell (Path):** `Get-WmiObject win32_service | where {$_.name –eq '<service_name>' } | select pathname`
    *   **PowerShell (Start Name):** `Get-WmiObject win32_service | where {$_.name –eq '<service_name>' } | select startname`
    *   **PowerShell (Start Mode):** `Get-WmiObject win32_service | where {$_.name –eq '<service_name>' } | select startmode`

### Network Topology & Service Relationships

*   **Common System Processes:** `smss.exe`, `csrss.exe`, `winlogon.exe`, `lsass.exe`, `spoolsv.exe`, `itunes.exe`, `explorer.exe`, `cmd.exe`.
*   **High-Volume System Process:** `svchost.exe` (Often requires verification of instance count and associated service keys like `-k DcomLaunch`).
*   **Malware Characteristics:**
    *   **Network:** Typically establishes connections for Command and Control (C2).
    *   **Persistence:** Implements mechanisms to maintain execution across system reboots.
*   **Vetting Context:** Both processes and services require verification of default installation paths, publisher identity, associated support files, and file hashes (e.g., MD5).

## Document Structure & Key Topics
- Visual & Network Diagram Intelligence (`BCF_Windows Process Investigation.pdf#page1`)
- Visual & Network Diagram Intelligence (`BCF_Windows Process Investigation.pdf#page3`)

