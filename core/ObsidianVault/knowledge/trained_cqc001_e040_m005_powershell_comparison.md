---
title: "Trained Knowledge & Topology: CQC001_E040_M005_PowerShell_Comparison.pdf"
tags:
  - curl
  - enumeration
  - mdp
  - passive_enum
  - pdf
  - powershell
  - reconnaissance
  - trained
source_file: CQC001_E040_M005_PowerShell_Comparison.pdf
doc_type: pdf
updated: 2026-10-25 00:57:41
---

# Trained Knowledge & Architecture: `CQC001_E040_M005_PowerShell_Comparison.pdf`

- **Source Path:** `~/Projects/CORA/Training/CQC001_E040_M005_PowerShell_Comparison.pdf` (`pdf`)
- **Extracted Technical Entities:** `curl, powershell`
- **Extracted IPs / Subnets:** `None`
- **Extracted Interfaces:** `None`
- **Linked Command Playbook:** [[commands/trained_cqc001_e040_m005_powershell_comparison]] (`21` CEGAR-verified commands | `21` MDP transitions)

## Command & Tactic Coverage Summary
- **Total CEGAR-Verified Commands:** `21` (full executable list in [[commands/trained_cqc001_e040_m005_powershell_comparison]])
- **Tactic Distribution:** `Enumeration` (13), `Reconnaissance` (6), `Passive_Enum` (2)
- **Top Extracted CLI Tools:** `clear-host` (1), `copy` (1), `copy-item` (1), `get-` (1), `get-content` (1), `get-help` (1), `get-location` (1), `get-process` (1), `invoke-` (1), `move-item` (1), `popd` (1), `remove-` (1), `rename` (1), `rename-` (1), `select-string` (1), `set-location` (1), `set-variable` (1), `stop-process` (1), `tee-object` (1), `test-` (1), `write-` (1)

### Visual & Network Diagram Intelligence (`CQC001_E040_M005_PowerShell_Comparison.pdf#page3`)
- **Spatially Grouped Diagram Nodes (Box/Component Clusters):**
  1. `[POWERSHELL | Features built within PowerShell]`
  2. `[History | Argument | res | Yes; multiple stacks; | (F8) | Yes | Yes | multiple location types]`
  3. `[Name | comeneldam | Path Completion | Yes | Yes | Yes]`
  4. `[Value prompt | Yes | Yes | Yes | (viaSET/ | Pcommand) | No]`
  5. `[Windows | PowerShell | Windows | CMD.EXE | Partial | ksh | Yes | (ksh93t+) | (extend-]`
  6. `[Yes | Partial | No | No | Yes | (F8) | No | No | No | Yes]`
  7. `[Yes (PUSHD, POPD) | Yes (cdpath builtin, pushd, | No | popd implemented | as functions) | Yes | Yes (cdpath, pushd, popd)]`
  8. `[Yes | able) | (extend- | able) | Yes | Yes | No | No]`
  9. `[Yes | Yes | No | No (only via | external | CHOICEcommand, | inDR-DOSalso]`
  10. `[csh | .COM | COMMAND | No]`
  11. `[Yes | No | No | No | No | No]`
  12. `[No | Yes | Yes | defined | When | Yes]`
  13. `[No | No | No | Yes (CDPATH, pushd, popd) | Yes]`
  14. `[viaSWITCH/ | DRSWITCHinternal | commands) | Yes]`
  15. `[bash (v4.0]`
  16. `[Yes]`
  17. `[3]`

## LLM Distilled Operational Summary
### Key Operational Techniques & Decision Workflows

*   **Command Selection Strategy**: Determine the target environment (PowerShell, CMD.EXE, or UNIX shell) to select the appropriate command alias. PowerShell uses `Cmdlet` syntax (e.g., `Get-ChildItem`) while legacy Windows shells use `COMMAND.COM` syntax (e.g., `dir`, `type`).
*   **Directory Navigation Workflow**: Utilize the directory stack for complex navigation. Use `Push-Location` (alias: `pushd`) to save the current path and `Pop-Location` (alias: `popd`) to restore it, enabling multi-level directory traversal without losing context.
*   **Process Management**: Identify running processes via `Get-Process` (alias: `gps`, `ps`) and terminate them using `Stop-Process` (alias: `spps`, `kill`).
*   **File & Data Manipulation**: Retrieve file contents with `Get-Content` (alias: `gc`, `type`) and list directory contents with `Get-ChildItem` (alias: `gci`, `dir`). Use `Tee-Object` to simultaneously output data to a file and pass it down the pipeline.
*   **Interactive Input Handling**: Capture user input using the `Value prompt` feature, which is native to PowerShell but limited or absent in CMD.EXE and some UNIX shells.

### Critical Command Patterns and Required Flags

*   **File Operations**:
    *   List: `Get-ChildItem` (Aliases: `gci`, `dir`, `ls`)
    *   Read: `Get-Content` (Aliases: `gc`, `type`, `cat`)
    *   Copy: `Copy-Item` (Aliases: `cpi`, `copy`, `cp`)
    *   Move/Rename: `Move-Item` / `Rename-Item` (Aliases: `mi`, `mv`, `ren`)
    *   Delete: `Remove-Item` (Aliases: `ri`, `del`, `rm`)
*   **System & Network**:
    *   Ping: `Test-Connection` (No direct alias in standard PowerShell, maps to `ping` in CMD/UNIX).
    *   Processes: `Get-Process` (Aliases: `gps`, `ps`) and `Stop-Process` (Aliases: `spps`, `kill`).
    *   Web: `Invoke-WebRequest` (Aliases: `iwr`, `curl`, `wget`).
*   **Environment & Navigation**:
    *   Current Path: `Get-Location` (Aliases: `gl`, `cd`, `pwd`).
    *   Stack Management: `Push-Location` / `Pop-Location` (Aliases: `pushd`, `popd`).
    *   Screen Clear: `Clear-Host` (Aliases: `cls`, `clear`).

### Network Topology & Service Relationships

*   **Cross-Platform Compatibility**: PowerShell provides native equivalents for common UNIX commands (`ls`, `cat`, `grep`, `ps`) and CMD commands (`dir`, `type`, `ping`), reducing the need for external tools.
*   **Stack-Based Navigation**: Unlike standard shells that rely solely on the current path, PowerShell supports a directory stack, allowing users to push and pop locations for complex script

## Document Structure & Key Topics
- Visual & Network Diagram Intelligence (`CQC001_E040_M005_PowerShell_Comparison.pdf#page3`)

