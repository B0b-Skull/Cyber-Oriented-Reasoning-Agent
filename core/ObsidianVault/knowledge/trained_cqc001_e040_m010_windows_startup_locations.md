---
title: "Trained Knowledge & Topology: CQC001_E040_M010_Windows_Startup_Locations.pdf"
tags:
  - mdp
  - pdf
  - trained
source_file: CQC001_E040_M010_Windows_Startup_Locations.pdf
doc_type: pdf
updated: 2026-10-25 00:57:54
---

# Trained Knowledge & Architecture: `CQC001_E040_M010_Windows_Startup_Locations.pdf`

- **Source Path:** `~/Projects/CORA/Training/CQC001_E040_M010_Windows_Startup_Locations.pdf` (`pdf`)
- **Extracted Technical Entities:** `general`
- **Extracted IPs / Subnets:** `None`
- **Extracted Interfaces:** `None`

## LLM Distilled Operational Summary
### Key Operational Techniques & Decision Workflows

*   **Determine Execution Timing**: Select the appropriate registry key based on whether the program must run before user logon, immediately after logon, or specifically for setup tasks.
    *   *Pre-Logon*: Use `RunServicesOnce` (HKLM/HKCU).
    *   *Post-Logon (General)*: Use `Run` (HKLM runs before HKCU).
    *   *One-Time Execution*: Use `RunOnce` (HKLM runs before other Run entries; HKCU runs after Startup folder).
*   **Verify User-Specific vs. System-Wide Scope**: Check both `HKEY_LOCAL_MACHINE` (HKLM) for all users and `HKEY_CURRENT_USER` (HKCU) for the specific logged-in user.
*   **Inspect Policy-Driven Launches**: Review `Explorer\Run` under `Policies` to identify programs forced by Group Policy or user policies.
*   **Check Custom User Initialization**: Examine the `Userinit` subkey under `Winlogon`, noting it accepts comma-separated values beyond the default `userinit.exe`.
*   **Search Startup Folders**:
    *   *All Users*: Check `Documents and Settings\All Users\Start Menu\Programs\Startup` (Win2000/XP/2003) or `Program Data\Microsoft\Windows\Start Menu\Programs\Startup` (Vista/2008/7).
    *   *Per User*: Check `%usersprofile%\Start Menu\Programs\Startup` (Win2000/XP/2003) or `%userprofile%\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup` (Vista/2008/7).

### Critical Command Patterns & Required Flags

*   **Registry Keys**:
    *   `HKLM\Software\Microsoft\Windows\CurrentVersion\RunServicesOnce`
    *   `HKCU\Software\Microsoft\Windows\CurrentVersion\RunServicesOnce`
    *   `HKLM\Software\Microsoft\Windows\CurrentVersion\Run`
    *   `HKCU\Software\Microsoft\Windows\CurrentVersion\Run`
    *   `HKLM\Software\Microsoft\Windows\CurrentVersion\RunOnce`
    *   `HKCU\Software\Microsoft\Windows\CurrentVersion\RunOnce`
    *   `HKLM\Software\Microsoft\Windows\CurrentVersion\RunOnceEx` (XP specific)
    *   `HKLM\Software\Microsoft\Windows\CurrentVersion\Policies\Explorer\Run`
    *   `HKCU\Software\Microsoft\Windows\CurrentVersion\Policies\Explorer\Run`
    *   `HKLM\Software\Microsoft\Windows NT\CurrentVersion\Winlogon\Userinit`
    *   `HKCU\Software\Microsoft\Windows NT\CurrentVersion\Windows\load`

### Network Topology & Service Relationships

*   **Service Precedence**: `RunServicesOnce` executes before user logon and other registry startup keys. `RunServices` executes immediately after `RunServicesOnce` but before user logon.
*   **Logon Sequence**: `Run

