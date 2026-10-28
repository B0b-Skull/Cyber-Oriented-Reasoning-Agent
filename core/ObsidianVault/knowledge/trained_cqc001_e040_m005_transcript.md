---
title: "Trained Knowledge & Topology: CQC001_E040_M005_transcript.pdf"
tags:
  - aws
  - enumeration
  - http
  - kerberos
  - lateral_movement_routing_pivot
  - mdp
  - mimikatz
  - passive_enum
  - pdf
  - powershell
  - reconnaissance
  - trained
source_file: CQC001_E040_M005_transcript.pdf
doc_type: pdf
updated: 2026-10-24 00:57:53
---

# Trained Knowledge & Architecture: `CQC001_E040_M005_transcript.pdf`

- **Source Path:** `~/Projects/CORA/Training/CQC001_E040_M005_transcript.pdf` (`pdf`)
- **Extracted Technical Entities:** `aws, http, kerberos, mimikatz, powershell`
- **Extracted IPs / Subnets:** `127.0.0.1, 172.24.1.10`
- **Extracted Interfaces:** `None`
- **Linked Command Playbook:** [[commands/trained_cqc001_e040_m005_transcript]] (`17` CEGAR-verified commands | `17` MDP transitions)

## Command & Tactic Coverage Summary
- **Total CEGAR-Verified Commands:** `17` (full executable list in [[commands/trained_cqc001_e040_m005_transcript]])
- **Tactic Distribution:** `Passive_Enum` (10), `Enumeration` (5), `Lateral_Movement_Routing_Pivot` (1), `Reconnaissance` (1)
- **Top Extracted CLI Tools:** `script` (4), `gcm` (3), `get-command` (2), `format-table` (1), `get-childitem` (1), `get-command,` (1), `get-service` (1), `get-wmiobject` (1), `set-item,` (1), `where-object` (1), `write-host` (1)

### Visual & Network Diagram Intelligence (`CQC001_E040_M005_transcript.pdf#page23`)

## LLM Distilled Operational Summary
### Operational Techniques & Decision Workflows
*   **Module Assessment**: Evaluate current PowerShell version compatibility (e.g., v5.0 on Windows 10/Server 2016 vs. v4.0 on pre-Windows 10) and .NET Framework prerequisites.
*   **Legacy Command Mapping**: Utilize `Get-Alias` to resolve legacy CMD or UNIX-style aliases to their underlying PowerShell cmdlets, ensuring backward compatibility during migration.
*   **Data Pipeline Construction**: Design workflows that pass complex .NET objects between cmdlets using pipes, rather than simple text streams, to simplify tasks like date/time parsing and object manipulation.
*   **Administrative Task Execution**: Leverage built-in cmdlets for registry management, WMI/CIM interaction, and system configuration without relying solely on `cmd.exe`.
*   **Scripting Environment Selection**: Choose between the standard PowerShell console for CLI-driven tasks and the Integrated Scripting Environment (ISE) for GUI-assisted development and debugging.

### Critical Command Patterns & Required Flags
*   **Alias Resolution**: `Get-Alias <AliasName>` (e.g., `Get-Alias cls`) to identify the full cmdlet path associated with a short alias.
*   **Pipeline Usage**: Chain cmdlets using the pipe operator (`|`) to flow .NET objects from output to input, enabling multi-step data processing in a single line of code.
*   **Module/Component Discovery**: Inspect module structures containing cmdlets, aliases, and providers to understand available functionality.

### Network Topology & Service Relationships
*   **Framework Dependency**: PowerShell functionality is strictly dependent on the installed version of the .NET Framework; older OS versions require manual installation of specific framework versions to support newer PowerShell releases.
*   **Integrated Service Hooks**: PowerShell management hooks are natively embedded within Microsoft server products (SQL Server, Exchange, System Center, SharePoint), creating a unified management plane across the Windows ecosystem.
*   **Interoperability Layer**: Acts as a bridge between traditional text-based CLI streams (CMD/UNIX) and object-oriented data models, allowing seamless interaction with COM and WMI services.

## Document Structure & Key Topics
- Visual & Network Diagram Intelligence (`CQC001_E040_M005_transcript.pdf#page23`)

## Extracted Operational Steps & Workflows
- 1. Obtain the directory information
- 2. Select name, length, and last access time
- 3. Format the output
- 1. Restricted - Does not load configuration files such as the Windows PowerShell profile or run
- 2. AllSigned - Requires that all scripts and configuration files be signed by a trusted publisher,
- 3. RemoteSigned - Requires that all scripts and configuration files downloaded from the Internet
- 4. Unrestricted - Loads all configuration files and runs all scripts. If you run an unsigned script that
- 5. Bypass - Blocks nothing and issues no warnings or prompts.
- 6. Undefined - Removes the currently assigned execution policy from the current scope. This
- 1. Process - The execution policy affects only the current Windows PowerShell process.
- 2. CurrentUser - The execution policy affects only the current user.
- 3. LocalMachine - The execution policy affects all users of the computer. Setting the Local-

