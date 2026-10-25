---
title: "Trained Knowledge & Topology: Change System Files CMDs.txt"
tags:
  - bcdedit
  - cacls
  - defense_evasion_firewall
  - enumeration
  - icacls
  - ipconfig
  - mdp
  - passive_enum
  - privilege_escalation
  - text
  - trained
  - wmic
source_file: Change System Files CMDs.txt
doc_type: text
updated: 2026-10-25 00:57:11
---

# Trained Knowledge & Architecture: `Change System Files CMDs.txt`

- **Source Path:** `~/Projects/CORA/Training/Change System Files CMDs.txt` (`text`)
- **Extracted Technical Entities:** `bcdedit, cacls, icacls, ipconfig, wmic`
- **Extracted IPs / Subnets:** `None`
- **Extracted Interfaces:** `None`
- **Linked Command Playbook:** [[commands/trained_change_system_files_cmds]] (`31` CEGAR-verified commands | `31` MDP transitions)

## Command & Tactic Coverage Summary
- **Total CEGAR-Verified Commands:** `31` (full executable list in [[commands/trained_change_system_files_cmds]])
- **Tactic Distribution:** `Defense_Evasion_Firewall` (14), `Passive_Enum` (7), `Enumeration` (6), `Privilege_Escalation` (4)
- **Top Extracted CLI Tools:** `copy` (9), `del` (4), `dir` (3), `bcdedit` (2), `icacls` (2), `wmic` (2), `cacls` (1), `movelatr` (1), `pechksum` (1), `reg` (1), `ren` (1), `rename` (1), `sfc` (1), `shell` (1), `takeown` (1)

## LLM Distilled Operational Summary
### Operational Techniques & Decision Workflows
*   **File Discovery & Verification**: Use `dir C:\ /s /b | find "filename.exe"` to locate executables recursively. Verify directory contents after deletions using `dir /on` to ensure no orphaned files remain.
*   **Backup & Restore Workflow**: Establish a backup before modification (e.g., `copy %systemroot%\system32\ipconfig.exe "C:\...\ipconfig.bak"`), perform the operation, then restore from the backup if needed.
*   **DLL Cache Manipulation**: When modifying system DLLs, check the `dllcache` folder (`cd %systemroot%\system32\dllcache`) and ensure consistency between the live file and the cache to prevent boot issues.
*   **Permission Management**: Use `takeown` followed by `icacls` to grant specific user groups (e.g., `win7\administrator`) full control (`(F)`) over system files before modification.
*   **System File Checker (SFC)**: Run `sfc /SCANFILE=<path>` to verify file integrity post-modification, or `sfc /scannow` for a full system check.
*   **Data Execution Prevention (DEP) Configuration**: Modify OS security policies using `bcdedit /set nx <MODE>` where modes include `AlwaysOff`, `AlwaysOn`, `OptOut`, or `OptIn`. Verify changes with `wmic OS Get DataExecutionPrevention_*`.

### Critical Command Patterns & Required Flags
*   **Recursive Directory Search**: `dir <Path> /s /b | find "<Target>"`
*   **File Backup**: `copy <Source> "<Destination>.bak"`
*   **File Replacement**: `del <OldPath> & copy <NewPath> <OldPath>`
*   **Permission Granting**: `icacls <Path> /grant <User>:(F)`
*   **BCD Configuration**: `bcdedit /set nx <MODE>` (Requires reboot for effect).
*   **Checksum Verification**: `PEChksum.exe <Path>` (Custom tool usage).

### Network Topology & Service Relationships
*   **System Root**: All operations target `%systemroot%\system32\` (typically `C:\Windows\System32`).
*   **DLL Cache**: Critical relationship exists between `%systemroot%\system32\` and `%systemroot%\system32\dllcache\`. Modifications to one must reflect in the other to maintain system stability.
*   **User Context**: Backups are often stored in user-specific directories like `C:\Documents and Settings\administrator\desktop\`.
*   **Service Impact**: Modifying `ipconfig.exe` or `notepad.exe` directly affects network diagnostics and user interface services respectively. Changing `sfcfiles.dll` impacts the System File Checker utility.

