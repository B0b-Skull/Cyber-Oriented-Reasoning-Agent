---
title: "Trained Knowledge & Topology: us-15-Graeber-Abusing-Windows-Management-Instrumentation-WMI-To-Build-A-Persistent Asynchronous-And-Fileless-Backdoor-wp.pdf"
tags:
  - credential_access
  - curl
  - enumeration
  - http
  - https
  - lateral_movement_routing_pivot
  - mdp
  - out-of-band_access
  - passive_enum
  - pdf
  - powershell
  - reconnaissance
  - sysinternals
  - trained
  - wmic
source_file: us-15-Graeber-Abusing-Windows-Management-Instrumentation-WMI-To-Build-A-Persistent Asynchronous-And-Fileless-Backdoor-wp.pdf
doc_type: pdf
updated: 2026-10-25 01:01:08
---

# Trained Knowledge & Architecture: `us-15-Graeber-Abusing-Windows-Management-Instrumentation-WMI-To-Build-A-Persistent Asynchronous-And-Fileless-Backdoor-wp.pdf`

- **Source Path:** `~/Projects/CORA/Training/us-15-Graeber-Abusing-Windows-Management-Instrumentation-WMI-To-Build-A-Persistent Asynchronous-And-Fileless-Backdoor-wp.pdf` (`pdf`)
- **Extracted Technical Entities:** `curl, http, https, powershell, sysinternals, wmic`
- **Extracted IPs / Subnets:** `172.24.72.131, 172.24.72.134, 172.24.72.135`
- **Extracted Interfaces:** `None`
- **Linked Command Playbook:** [[commands/trained_us-15-graeber-abusing-windows-management-instrumentation-wmi-to-]] (`47` CEGAR-verified commands | `47` MDP transitions)

## Command & Tactic Coverage Summary
- **Total CEGAR-Verified Commands:** `47` (full executable list in [[commands/trained_us-15-graeber-abusing-windows-management-instrumentation-wmi-to-]])
- **Tactic Distribution:** `Enumeration` (23), `Passive_Enum` (11), `Credential_Access` (6), `Lateral_Movement_Routing_Pivot` (5), `Out-of-Band_Access` (1), `Reconnaissance` (1)
- **Top Extracted CLI Tools:** `get-wmiobject` (11), `invoke-wmimethod` (6), `get-ciminstance` (3), `new-object` (3), `set-wmiinstance` (3), `get-wminamespace` (2), `new-cimsession` (2), `get-cimassociatedinstance` (1), `get-cimclass` (1), `get-cimsession` (1), `get-credential` (1), `invoke-cimmethod` (1), `ls` (1), `new-ciminstance` (1), `new-cimsessionoption` (1), `register-cimindicationevent` (1), `register-wmievent` (1), `remove-ciminstance` (1), `remove-cimsession` (1), `remove-wmiobject` (1), `set-ciminstance` (1), `set-itemproperty` (1), `test-wsman` (1), `wmic` (1)

## LLM Distilled Operational Summary
### Key Operational Techniques & Decision Workflows
*   **Architecture Exploitation**: Leverage the consistency of WMI across Windows NT 4.0 through modern versions to bypass deprecation cycles.
*   **Data Consumption**: Utilize PowerShell for rapid interaction and querying of managed components (e.g., `Win32_Process`, `Win32_Service`).
*   **Dynamic vs. Persistent Objects**:
    *   Use **Dynamic Objects** for on-the-fly reconnaissance (e.g., listing running processes).
    *   Use **Persistent Objects** stored in `%SystemRoot%\System32\wbem\Repository\OBJECTS.DATA` for long-term persistence and asynchronous execution.
*   **Schema Injection**: Create custom WMI objects directly via .NET code without requiring MOF files, allowing flexible payload definition.
*   **Event-Driven Execution**: Register event handlers on object creation/modification to trigger callbacks or maintain presence.
*   **Lateral Movement**: Execute remote commands using the `Win32_Process.Create` method.

### Critical Command Patterns & Required Flags
*   **Querying Data**: Use **WQL (WMI Query Language)** for fine-grained filtering of object instances.
*   **Remote Transmission**:
    *   **DCOM**: Default local/remote protocol for WMI traffic.
    *   **WinRM**: Alternative protocol for remote management.
*   **Payload Execution**: Invoke `Win32_Process.Create` methods within WMI classes to spawn processes remotely.
*   **Persistence Mechanism**: Inject custom class instances into the **CIM Repository** (`OBJECTS.DATA`) to ensure survival across reboots.

### Network Topology & Service Relationships
*   **Core Service**: `Winmgmt` (Windows Management Instrumentation) service handles data population and query resolution.
*   **Data Storage**: Persistent WMI objects reside in the **CIM Repository** located at `%SystemRoot%\System32\wbem\Repository\OBJECTS.DATA`.
*   **Schema Definition**: Managed Object Format (**MOF**) files define the structure of standard WMI objects, though custom objects can bypass these files.
*   **Standards Compliance**: Implements **WBEM** and **CIM** standards from the **DMTF**, enabling industry-agnostic data transmission.
*   **Interoperability**: Supports both **DCOM** and **WinRM** for remote data transmission, facilitating lateral movement across network segments.

## Document Structure & Key Topics
- Prep file to drop on remote system
- Establish remote WMI connection
- "Push" file contents
- The PowerShell payload that will drop the stored file contents
- Drop the file to the target filesystem
- Confirm successful file drop
- Create a remote registry key and value
- PowerShell payload that saves the serialized output of `Get-Process lsass` to
- Invoke PowerShell payload
- Pull the serialized results back
- Deserialize and display the result of the command executed on the remote system

## Extracted Operational Steps & Workflows
- 1. Instance queries – Query instances on WMI objects
- 2. Event queries – Equivalent to registering an alert upon creation, modification, or deletion of a
- 3. Meta queries – Metaqueries used to query information about WMI namespaces and class
- 1. An event filter – The event of interest
- 2. An event consumer – An action to perform upon triggering an event
- 3. A filter to consumer binding – The registration mechanism that binds a filter to a consumer
- 98. 

- 1. An attacker uses WMI as a persistence mechanism
- 2. The WMI Shell utility is used as a C2 channel
- 3. WMI classes are created to store attacker data
- 4. An attacker installs a malicious WMI provider
- 5. An attacker persists via the Start Menu or registry
- 6. An attacker persists via other additional registry values
- 7. An attacker installs a service
- 1. Consider disabling the WMI service. Consider your organizations need for remote WMI access.
- 2. Consider blocking the WMI protocol ports. If there is no legitimate need to use remote WMI,
- 3. WMI, DCOM, and WinRM events are logged to the following event logs:

