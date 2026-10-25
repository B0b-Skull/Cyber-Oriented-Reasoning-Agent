---
title: "Trained Knowledge & Topology: Win32_ComputerSystem class (Windows).pdf"
tags:
  - bcdedit
  - https
  - mdp
  - pdf
  - trained
source_file: Win32_ComputerSystem class (Windows).pdf
doc_type: pdf
updated: 2026-10-25 01:01:12
---

# Trained Knowledge & Architecture: `Win32_ComputerSystem class (Windows).pdf`

- **Source Path:** `~/Projects/CORA/Training/Win32_ComputerSystem class (Windows).pdf` (`pdf`)
- **Extracted Technical Entities:** `bcdedit, https`
- **Extracted IPs / Subnets:** `None`
- **Extracted Interfaces:** `None`

## LLM Distilled Operational Summary
### Key Operational Techniques & Decision Workflows
*   **Domain/Workgroup Management**: Use `JoinDomainOrWorkgroup` to add a system to an Active Directory domain or a workgroup, and `UnjoinDomainOrWorkgroup` to remove it.
*   **Local Identity Renaming**: Execute the `Rename` method to change the local computer name.
*   **Power State Control**: Attempt `SetPowerState` (note: implementation details are inherited from `CIM_UnitaryComputerSystem`).
*   **Boot Behavior Configuration**:
    *   Enable/Disable automatic reset on crash via `AutomaticResetBootOption`.
    *   Configure system action upon reset limit reach using `BootOptionOnLimit` (values: 0=Reserved, 1=OS, 2=Utils, 3=No Reboot).
    *   Define watchdog timer actions via `BootOptionOnWatchDog`.
*   **Hardware Security Verification**: Check `AdminPasswordStatus` (0=Disabled, 1=Enabled, 2=Not Implemented, 3=Unknown) to assess SMBIOS Type 24 hardware security settings.
*   **Memory & Processor Inventory**: Retrieve `TotalPhysicalMemory` and `NumberOfLogicalProcessors` for resource assessment.

### Critical Command Patterns and Required Flags
*   **WMI Query Syntax**:
    ```powershell
    Get-WmiObject -Class Win32_ComputerSystem | Select-Object Name, Domain, UserName, TotalPhysicalMemory
    ```
*   **Domain Joining (PowerShell)**:
    ```powershell
    $obj = Get-WmiObject -Class Win32_ComputerSystem
    $obj.JoinDomainOrWorkgroup("DOMAIN_NAME", "DOMAIN_USER", "DOMAIN_PASSWORD")
    ```
*   **Renaming**:
    ```powershell
    $obj = Get-WmiObject -Class Win32_ComputerSystem
    $obj.Rename("NewComputerName")
    ```
*   **Key Properties to Monitor**:
    *   `PartOfDomain` (boolean): Indicates domain membership status.
    *   `DNSHostName` (string): Resolvable DNS name.
    *   `Manufacturer` & `Model` (string): Hardware identification.
    *   `InstallDate` (datetime): System installation timestamp.

### Network Topology & Service Relationships
*   **Domain/Workgroup Context**: The class directly exposes `Domain` and `Workgroup` strings, defining the logical network container.
*   **Authentication Context**: `UserName` provides the current logged-in user, critical for session-based service relationships.
*   **SMBIOS Integration**: Several properties (e.g., `AdminPasswordStatus`, `BootOptionOnLimit`) map directly to SMBIOS Type 23 and Type 24 structures, linking WMI data to low-level hardware inventory standards.
*   **Boot State Monitoring**: `BootupState` and `BootStatus` arrays provide runtime state information relevant to network boot protocols (PXE/NetBoot) and fail-safe boot modes.

