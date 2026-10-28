---
title: "Trained Knowledge & Topology: CQC001_E040_M005_WMI_QR_PowerShell_4.0.pdf"
tags:
  - enumeration
  - http
  - lateral_movement_routing_pivot
  - mdp
  - out-of-band_access
  - passive_enum
  - pdf
  - powershell
  - reconnaissance
  - trained
source_file: CQC001_E040_M005_WMI_QR_PowerShell_4.0.pdf
doc_type: pdf
updated: 2026-10-24 00:57:53
---

# Trained Knowledge & Architecture: `CQC001_E040_M005_WMI_QR_PowerShell_4.0.pdf`

- **Source Path:** `~/Projects/CORA/Training/CQC001_E040_M005_WMI_QR_PowerShell_4.0.pdf` (`pdf`)
- **Extracted Technical Entities:** `http, powershell`
- **Extracted IPs / Subnets:** `127.0.0.1`
- **Extracted Interfaces:** `None`
- **Linked Command Playbook:** [[commands/trained_cqc001_e040_m005_wmi_qr_powershell_4_0]] (`39` CEGAR-verified commands | `39` MDP transitions)

## Command & Tactic Coverage Summary
- **Total CEGAR-Verified Commands:** `39` (full executable list in [[commands/trained_cqc001_e040_m005_wmi_qr_powershell_4_0]])
- **Tactic Distribution:** `Passive_Enum` (21), `Enumeration` (10), `Reconnaissance` (5), `Out-of-Band_Access` (2), `Lateral_Movement_Routing_Pivot` (1)
- **Top Extracted CLI Tools:** `get-ciminstance` (14), `get-cimclass` (6), `gcim` (3), `get-cimassociatedinstance` (3), `new-cimsession` (2), `register-cimindicationevent` (2), `set-ciminstance` (2), `unregister-event` (2), `get-command` (1), `get-event` (1), `new-ciminstance` (1), `new-cimsessionoption` (1), `remove-ciminstance` (1)

## LLM Distilled Operational Summary
### Operational Techniques & Workflows
*   **Discovery via Tab Completion**: Use `Get-CimInstance` with tab completion to rapidly explore top-level namespaces and class names. If a namespace is omitted, the default `root/cimv2` is assumed. Note that tab completion functions only on the local machine.
*   **Advanced Class Filtering**: Utilize `Get-CimClass` to search for classes by method patterns (e.g., `-MethodName Stop*`), property names (e.g., `-PropertyName Handle`), or qualifiers (e.g., `-QualifierName Association`, `-QualifierName Indication`). This requires a CIM server supporting schema retrieval.
*   **Data Retrieval Strategies**:
    *   Fetch full instances: `Get-CimInstance -ClassName <Class>`.
    *   Apply WQL queries: Use the `-Query` parameter for complex filtering (e.g., `Select * from Win32_Service Where Name like 'app%'`).
    *   Optimize footprint: Use `-KeyOnly` for unique identifiers or `-Property` to list specific attributes, reducing memory/network usage.
*   **Object Handling**: Recognize that `CimInstance` objects are snapshots. Passing an instance as input (e.g., `Get-CimInstance -InputObject $a[0]`) preserves the original object state.
*   **Serialization**: Leverage `export-clixml` and `import-clixml` to serialize/deserialize `CimInstance` objects for portability.
*   **Filtering Logic**: Apply `-Filter` with WQL syntax (e.g., `'DriveType = 3'`) to narrow results directly within the cmdlet.

### Critical Command Patterns & Flags
*   **`Get-CimInstance`**:
    *   `-ClassName`: Specifies the target class.
    *   `-Namespace`: Defines the WMI namespace (default: `root/cimv2`).
    *   `-Query`: Executes a WQL statement.
    *   `-KeyOnly`: Returns only the unique key properties.
    *   `-Property`: Limits output to specified properties.
    *   `-Filter`: Applies a WQL filter string.
*   **`Get-CimClass`**:
    *   `-MethodName`: Filters classes by method name patterns.
    *   `-PropertyName`: Filters classes by property name patterns.
    *   `-QualifierName`: Filters classes by specific qualifiers (e.g., `Association`, `Indication`).
    *   `-Namespace`: Targets a specific namespace.

### Network & Service Relationships
*   **Default Namespace**: `root/cimv2` is the standard location for WMI/CIM classes unless explicitly overridden.
*   **Schema Dependency**: Advanced operations like `Get-CimClass` and accurate schema retrieval (`.CimClass`) depend on the remote CIM server supporting `GetClass` and `EnumerateClasses` operations.
*   **Portability**: `CimInstance` objects support full serialization, allowing data transfer across network boundaries without losing structural integrity.

## Document Structure & Key Topics
- Get instance of Win32_LogicalDisk class with DriveType==3 (hard drives)
- Get the associated instancec disk1
- Given an instance of Win32_LogicalDisk, get the associated instances of specific type
- Subscribe to events using the filter
- Get the events using Windows PowerShell eventing
- Install Windows Management Framework 4.0 (recommended)
- OR use DCOM protocol

