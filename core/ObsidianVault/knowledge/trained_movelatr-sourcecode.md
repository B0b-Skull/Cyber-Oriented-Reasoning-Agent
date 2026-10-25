---
title: "Trained Knowledge & Topology: Movelatr-SourceCode.txt"
tags:
  - defense_evasion_firewall
  - http
  - mdp
  - text
  - trained
source_file: Movelatr-SourceCode.txt
doc_type: text
updated: 2026-10-25 00:59:21
---

# Trained Knowledge & Architecture: `Movelatr-SourceCode.txt`

- **Source Path:** `~/Projects/CORA/Training/Movelatr-SourceCode.txt` (`text`)
- **Extracted Technical Entities:** `http`
- **Extracted IPs / Subnets:** `None`
- **Extracted Interfaces:** `None`
- **Linked Command Playbook:** [[commands/trained_movelatr-sourcecode]] (`4` CEGAR-verified commands | `4` MDP transitions)

## Command & Tactic Coverage Summary
- **Total CEGAR-Verified Commands:** `4` (full executable list in [[commands/trained_movelatr-sourcecode]])
- **Tactic Distribution:** `Defense_Evasion_Firewall` (4)
- **Top Extracted CLI Tools:** `movelatr` (4)

## LLM Distilled Operational Summary
### Key Operational Techniques & Decision Workflows
*   **Boot-Time Execution**: The tool configures the Windows Registry (`SYSTEM\\CurrentControlSet\\Control\\Session Manager`) to execute file moves, deletions, or replacements automatically during the OS boot sequence.
*   **Persistent File Handling**: Designed specifically for replacing files that are locked or in use by the running operating system, ensuring the new version takes over once the system restarts.
*   **Volume Migration Logic**: Supports moving directories within the same partition (effectively a rename). For cross-volume moves on NT/2k, the file must first be manually copied to the destination volume before invoking `MOVELATR`.
*   **Protected File Bypass**: Detects Windows File Protection (WFP) or System File Checker (SFC) protected files. If enabled, it modifies the registry key `AllowProtectedRenames` to permit overwriting these critical system files.
*   **Directory Deletion Constraint**: Directories are only deleted at boot if they are currently empty; non-empty directories require manual clearing first.
*   **State Management**: Includes functionality to enumerate pending operations and clear all scheduled moves via the `/C` flag.

### Critical Command Patterns and Required Flags
*   `MOVELATR`: Enumerates currently pending move operations.
*   `MOVELATR <source> <destination>`: Schedules a move of `<source>` to `<destination>` at boot.
*   `MOVELATR <source> /D`: Schedules the deletion of `<source>` at boot.
*   `MOVELATR /C`: Clears all pending move operations from the registry.
*   `MOVELATR /C` (Implicit): Used to reset state before or after operations.

### Network Topology, IP/Subnet, Serial, or Service Relationships
*   **Service Dependency**: Relies on the `SFC.DLL` service/library to detect protected files on Windows 2000 and later.
*   **Registry Key Target**: Specifically targets `HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Session Manager`.
*   **Value Name**: Interacts with the `PendingFileRenameOperations` registry value (stored as binary data) to manage the queue of boot-time actions.
*   **Platform Awareness**: Detects the OS version (Win9x vs. NT/2k) to adjust behavior regarding registry creation and file protection checks.

