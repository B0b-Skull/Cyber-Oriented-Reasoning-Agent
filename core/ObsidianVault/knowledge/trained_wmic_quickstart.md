---
title: "Trained Knowledge & Topology: WMIC QuickStart.txt"
tags:
  - defense_evasion_firewall
  - mdp
  - passive_enum
  - text
  - trained
  - wmic
source_file: WMIC QuickStart.txt
doc_type: text
updated: 2026-10-25 01:01:12
---

# Trained Knowledge & Architecture: `WMIC QuickStart.txt`

- **Source Path:** `~/Projects/CORA/Training/WMIC QuickStart.txt` (`text`)
- **Extracted Technical Entities:** `wmic`
- **Extracted IPs / Subnets:** `None`
- **Extracted Interfaces:** `None`
- **Linked Command Playbook:** [[commands/trained_wmic_quickstart]] (`12` CEGAR-verified commands | `12` MDP transitions)

## Command & Tactic Coverage Summary
- **Total CEGAR-Verified Commands:** `12` (full executable list in [[commands/trained_wmic_quickstart]])
- **Tactic Distribution:** `Passive_Enum` (11), `Defense_Evasion_Firewall` (1)
- **Top Extracted CLI Tools:** `wmic` (11), `rundll32` (1)

## LLM Distilled Operational Summary
### Operational Techniques & Decision Workflows

*   **Platform Compatibility Check**: Verify the target OS is Windows XP Pro before executing `wmic.exe`, as it is absent in Windows 2000 and XP Home editions.
*   **Process Analysis Workflow**:
    *   Use `/format:csv` to generate comma-separated values for program names and memory usage (`workingsetsize`).
    *   Pipe output to `sort` to alphabetize process lists for easier scanning.
*   **Hardware Inventory**:
    *   Query disk drives (`wmic diskdrive`) for model, name, and size.
    *   Query partitions (`wmic partition`) for name, size, and type (e.g., Installable File System).
    *   Extract BIOS serial numbers and product identifying numbers (Service Tags) from `wmic bios` and `wmic csproduct`.
*   **Patch Management Audit**: Retrieve installed Windows patches and their installation dates using `wmic qfe` formatted as CSV.
*   **Memory Verification**: Confirm physical RAM capacity via `wmic COMPUTERSYSTEM`.
*   **Network Interface Discovery**: List all network adapters with descriptions and MAC addresses using `wmic nic`.

### Critical Command Patterns & Required Flags

*   **Standard Query**: `wmic [class] get [properties]`
    *   *Example*: `wmic process get workingsetsize,commandline`
*   **CSV Formatting**: Append `/format:csv` to any query for machine-readable output.
    *   *Example*: `wmic qfe get description,installedOn /format:csv`
*   **Output Sorting**: Pipe results to the `sort` command.
    *   *Example*: `wmic process | sort`
*   **Remote Connection**: Use the `node` parameter to target remote WMI instances (specific syntax not fully detailed in chunk, but implied by section header).

### Network Topology & Service Relationships

*   **Local Service Mapping**: The process list reveals specific service associations:
    *   `svchost.exe` instances are grouped by `-k` flags (e.g., `-k DcomLaunch`, `-k rpcss`, `-k netsvcs`).
    *   Third-party services include Symantec components (`ccApp.exe`, `DefWatch.exe`, `Rtvscan.exe`) and Mozilla (`mozilla.exe`).
*   **Network Interfaces**: Identified adapters include:
    *   Wireless: Intel(R) PRO/Wireless 215ABG.
    *   Wired: Broadcom NetXtreme 57xx Gigabit Controller.
    *   Virtual/Remote: WAN Miniports (L2TP, PPTP, PPPOE) and RAS Async Adapter.
*   **Hardware Identification**: The system is identified as a Dell Latitude D610 with a Phoenix ROM BIOS.

