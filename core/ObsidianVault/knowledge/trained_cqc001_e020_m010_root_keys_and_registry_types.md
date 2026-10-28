---
title: "Trained Knowledge & Topology: CQC001_E020_M010_Root_Keys_and_Registry_Types.pdf"
tags:
  - bcdedit
  - enumeration
  - http
  - https
  - mdp
  - passive_enum
  - pdf
  - trained
source_file: CQC001_E020_M010_Root_Keys_and_Registry_Types.pdf
doc_type: pdf
updated: 2026-10-24 00:57:31
---

# Trained Knowledge & Architecture: `CQC001_E020_M010_Root_Keys_and_Registry_Types.pdf`

- **Source Path:** `~/Projects/CORA/Training/CQC001_E020_M010_Root_Keys_and_Registry_Types.pdf` (`pdf`)
- **Extracted Technical Entities:** `bcdedit, http, https`
- **Extracted IPs / Subnets:** `None`
- **Extracted Interfaces:** `None`
- **Linked Command Playbook:** [[commands/trained_cqc001_e020_m010_root_keys_and_registry_types]] (`17` CEGAR-verified commands | `17` MDP transitions)

## Command & Tactic Coverage Summary
- **Total CEGAR-Verified Commands:** `17` (full executable list in [[commands/trained_cqc001_e020_m010_root_keys_and_registry_types]])
- **Tactic Distribution:** `Enumeration` (13), `Passive_Enum` (4)
- **Top Extracted CLI Tools:** `reg` (17)

## LLM Distilled Operational Summary
### Key Operational Techniques & Decision Workflows

*   **Root Key Selection Strategy**:
    *   Use **HKCR** for file extension associations and COM/ActiveX object registration. Note that HKCR is a virtualized view combining per-user (`HKCU\Software\Classes`) and system-wide (`HKLM\Software\Classes`) data.
    *   Use **HKCU** for current user preferences and configuration; it dynamically points to the active profile (`ntuser.dat`).
    *   Use **HKLM** for system-wide, persistent configuration (booting, hardware, software installs) that survives reboots.
    *   Use **HKU** to inspect all loaded user profiles, including `.DEFAULT` for system account processes.
    *   Use **HKCC** only when troubleshooting specific hardware profile conflicts.
    *   Use **HKPD** programmatically to query performance counters (data resides outside the registry).

*   **Version-Specific Path Mapping**:
    *   Distinguish between Windows XP/2003 paths (e.g., `\Documents and Settings\`) and Vista/2008+ paths (e.g., `\Users\`) when correlating registry keys to physical files like `ntuser.dat` or `UsrClass.dat`.

### Critical Command Patterns and Required Flags

*   **Registry Enumeration**:
    *   `reg query HKLM\SYSTEM\CurrentControlSet\HardwareProfiles\Current /v CurrentProfile` (Retrieves current hardware profile ID via HKCC link).
    *   `reg query HKCR /v ""` (Lists file extension associations and COM classes).
    *   `reg query HKU /s` (Scans all loaded user profiles under HKU).

### Network Topology, IP/Subnet, Serial, or Service Relationships

*   **Service & Database Relationships**:
    *   **HKLM\SAM**: Directly linked to the **Security Accounts Manager** database; contains account/group data replicated across **Domain Controllers**.
    *   **HKLM\SECURITY**: Stores system-wide security policies enforced by **Domain Controllers**.
    *   **HKCR**: Serves as the bridge for **COM/ActiveX** interprocess communication, replacing legacy DDE mechanisms.

*   **Hardware Profile Linkage**:
    *   **HKCC** acts as a pointer to `HKLM\System\CurrentControlSet\HardwareProfiles\Current`, linking software configuration to specific hardware states.

