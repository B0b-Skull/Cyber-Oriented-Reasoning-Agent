---
title: "Trained Knowledge & Topology: CQC001_E040_M005_PowerShell_Examples_4.0.pdf"
tags:
  - covert_infil
  - enumeration
  - http
  - https
  - lateral_movement_routing_pivot
  - mdp
  - passive_enum
  - pdf
  - powershell
  - protocol_chaining
  - trained
source_file: CQC001_E040_M005_PowerShell_Examples_4.0.pdf
doc_type: pdf
updated: 2026-10-24 00:57:41
---

# Trained Knowledge & Architecture: `CQC001_E040_M005_PowerShell_Examples_4.0.pdf`

- **Source Path:** `~/Projects/CORA/Training/CQC001_E040_M005_PowerShell_Examples_4.0.pdf` (`pdf`)
- **Extracted Technical Entities:** `http, https, powershell`
- **Extracted IPs / Subnets:** `None`
- **Extracted Interfaces:** `None`
- **Linked Command Playbook:** [[commands/trained_cqc001_e040_m005_powershell_examples_4_0]] (`20` CEGAR-verified commands | `20` MDP transitions)

## Command & Tactic Coverage Summary
- **Total CEGAR-Verified Commands:** `20` (full executable list in [[commands/trained_cqc001_e040_m005_powershell_examples_4_0]])
- **Tactic Distribution:** `Enumeration` (7), `Protocol_Chaining` (7), `Covert_Infil` (3), `Lateral_Movement_Routing_Pivot` (2), `Passive_Enum` (1)
- **Top Extracted CLI Tools:** `invoke-command` (3), `get-module` (2), `invoke-restmethod` (2), `register-scheduledjob` (2), `test-netconnection` (2), `get-childitem` (1), `get-filehash` (1), `get-job` (1), `invoke-item` (1), `invoke-webrequest` (1), `new-cimsession` (1), `new-jobtrigger` (1), `new-pssession` (1), `start-job` (1)

## LLM Distilled Operational Summary
### Key Operational Techniques & Decision Workflows

*   **Job Scheduling Workflow**: Define a trigger (e.g., daily at 3am) using `New-JobTrigger`, then register the job with `Register-ScheduledJob`. Execute manually via `Start-Job -DefinitionName <Name>` or trigger immediately using the `-RunNow` parameter. Retrieve results post-execution with `Get-Job | Receive-Job`.
*   **Dynamic Method Invocation**: Execute methods by name stored in variables (e.g., `$fn = "ToString"`; `"Hello".$fn()`) or via arrays (`@("ToUpper", "ToLower")[$index]`).
*   **Elevated Privilege Enforcement**: Enforce administrative requirements at script start using `#Requires -RunAsAdministrator`.
*   **Complex Password Generation**: Leverage `.NET` classes via `Add-Type -AssemblyName System.Web` and call `[System.Web.Security.Membership]::GeneratePassword(length, non-alphanumeric-count)`.
*   **Network Diagnostics**: Use `Test-NetConnection` with `-InformationLevel Detailed` for full diagnostics or `-InformationLevel Quiet` for Boolean connectivity checks.
*   **Web Data Parsing**: Extract HTML elements (links, forms) via `Invoke-WebRequest` and access the `.Links` property. Fetch REST/OData data using `Invoke-RestMethod` and process XML content into custom objects (`[PSCustomObject]`) for export.
*   **Pipeline Variable Usage**: Capture intermediate pipeline results with `-pv` (alias for `PipelineVariable`) to pass specific outputs downstream (e.g., `Get-ChildItem *.ps1 -pv a | Get-Acl`).
*   **Default Parameter Configuration**: Set global defaults for cmdlet parameters (like `-Credential`) using `$PSDefaultParameterValues`.

### Critical Command Patterns & Required Flags

| Cmdlet / Pattern | Key Flags / Parameters | Purpose |
| :--- | :--- | :--- |
| `New-JobTrigger` | `-Daily`, `-At <Time>` | Define execution schedule. |
| `Register-ScheduledJob` | `-Name`, `-Trigger`, `-ScriptBlock`, `-RunNow | `-DefinitionName` | Register or start jobs immediately. |
| `Get-Job` / `Receive-Job` | `-Name` | Retrieve and process job output. |
| `Add-Type` | `-AssemblyName <Name>` | Load .NET assemblies for advanced classes. |
| `Test-NetConnection` | `-ComputerName`, `-Port`, `-InformationLevel` | Diagnose network reachability. |
| `Invoke-WebRequest` | `-Uri` | Fetch HTML/REST resources. |
| `Invoke-RestMethod` | `-Uri` | Consume REST/OData services. |
| `Get-FileHash` | `-Path`, `-Algorithm` | Compute file integrity hashes. |
| `Out-GridView` | `-PassThru` | Enable interactive selection for pipeline export. |

### Network Topology & Service Relationships

*   **External Services**: Interactions occur with public endpoints like `blogs.msdn.com` (HTML parsing) and `odata.eventpointdata.com` (OData REST services for event data).
*   **Local Resources**: Operations target local file systems (`c:\`, `d:\`, `$env:TEMP`)

