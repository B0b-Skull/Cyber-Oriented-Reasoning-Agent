---
title: "Trained Knowledge & Topology: CQC001_E040_M005_PowerShell_Basic_Cheat.pdf"
tags:
  - credential_access
  - enumeration
  - mdp
  - passive_enum
  - pdf
  - powershell
  - protocol_chaining
  - reconnaissance
  - trained
source_file: CQC001_E040_M005_PowerShell_Basic_Cheat.pdf
doc_type: pdf
updated: 2026-10-24 00:57:39
---

# Trained Knowledge & Architecture: `CQC001_E040_M005_PowerShell_Basic_Cheat.pdf`

- **Source Path:** `~/Projects/CORA/Training/CQC001_E040_M005_PowerShell_Basic_Cheat.pdf` (`pdf`)
- **Extracted Technical Entities:** `powershell`
- **Extracted IPs / Subnets:** `None`
- **Extracted Interfaces:** `None`
- **Linked Command Playbook:** [[commands/trained_cqc001_e040_m005_powershell_basic_cheat]] (`55` CEGAR-verified commands | `55` MDP transitions)

## Command & Tactic Coverage Summary
- **Total CEGAR-Verified Commands:** `55` (full executable list in [[commands/trained_cqc001_e040_m005_powershell_basic_cheat]])
- **Tactic Distribution:** `Enumeration` (23), `Protocol_Chaining` (13), `Credential_Access` (9), `Passive_Enum` (9), `Reconnaissance` (1)
- **Top Extracted CLI Tools:** `get-command` (3), `get-process` (3), `clear-host` (1), `compare-object` (1), `copy-item` (1), `export-clixml` (1), `export-csv` (1), `format-list` (1), `format-table` (1), `get-adcomputer` (1), `get-aduser` (1), `get-childitem` (1), `get-ciminstance` (1), `get-content` (1), `get-credential` (1), `get-date` (1), `get-date).date` (1), `get-eventlog` (1), `get-help` (1), `get-history` (1), `get-item` (1), `get-itemproperty` (1), `get-location` (1), `get-member` (1), `get-winevent` (1)

## LLM Distilled Operational Summary
### Operational Techniques & Workflows
*   **Execution Control**: Bypass default restrictions with `Set-ExecutionPolicy -ExecutionPolicy Bypass`. Run scripts in current scope using `"path\script.ps1"` or script scope using `&"path\script.ps1"`.
*   **Pipeline Logic**: Chain commands using `|` to pass objects. Example: `Get-Process | Where-Object { $_.CPU -gt 50 } | Stop-Process`.
*   **Interactive Input**: Capture user data with `Read-Host`. Use `-asSecureString` for passwords.
*   **Flow Control**: Implement logic using `If/Else`, `While`, and `For` loops. Iterate over collections with `Foreach-Object` or pipeline syntax (`1..10 | foreach {$_}`).
*   **Object Inspection**: Use `Get-Member` to discover properties, `Format-List` for detailed views, and `Select-Object` to filter specific properties before output.

### Critical Command Patterns & Flags
*   **Discovery & Filtering**:
    *   `Get-Command -Module <Name>`: Find module-specific commands.
    *   `Get-Process | Where-Object { $_.Name -like "*excel*" }`: Filter objects using wildcards.
    *   `-Confirm` / `-WhatIf`: Test actions without execution or prompt confirmation.
*   **File & Path Operations**:
    *   `Split-Path`: Extract directory or filename components.
    *   `Test-Path`: Verify existence before operations.
    *   `Get-Content` (`gc`) / `Set-Content` (`sc`): Read/modify file contents.
*   **Data Conversion**:
    *   `Export-CliXML` / `Import-CliXML`: Serialize objects to XML.
    *   `ConvertTo-CSV` / `Import-CSV`: Handle comma-separated data.

### Network & Service Relationships
*   **Service Discovery**: `Get-WMIObject` (legacy) and `Get-CimInstance` (modern) query Windows Management Instrumentation for service states, processes, and hardware details.
*   **Event Logging**: `Get-WinEvent` replaces `Get-EventLog` for retrieving structured event logs from the system.
*   **Directory Services**: `Get-ADUser` and `Get-ADComputer` interact with Active Directory (requires RSAT/AD module).
*   **Remote Sessions**: `New-PSSession` establishes remote PowerShell connections; `Test-Connection` verifies network reachability.

