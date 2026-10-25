---
title: "Trained Knowledge & Topology: wp-windows-management-instrumentation.pdf"
tags:
  - credential_access
  - curl
  - enumeration
  - http
  - https
  - lateral_movement_routing_pivot
  - mdp
  - passive_enum
  - pdf
  - powershell
  - sysinternals
  - trained
  - wmic
source_file: wp-windows-management-instrumentation.pdf
doc_type: pdf
updated: 2026-10-25 01:01:14
---

# Trained Knowledge & Architecture: `wp-windows-management-instrumentation.pdf`

- **Source Path:** `~/Projects/CORA/Training/wp-windows-management-instrumentation.pdf` (`pdf`)
- **Extracted Technical Entities:** `curl, http, https, powershell, sysinternals, wmic`
- **Extracted IPs / Subnets:** `1.5.0.7, 127.0.0.1, 172.24.72.131, 172.24.72.134, 172.24.72.135, 2.2.2.7, 5.9.7.6, 7.0.0.1, 7.0.3.5, 8.1.0.4, 8.4.9.8, 9.1.7.0, 9.4.2.9`
- **Extracted Interfaces:** `Lo`
- **Linked Command Playbook:** [[commands/trained_wp-windows-management-instrumentation]] (`50` CEGAR-verified commands | `50` MDP transitions)

## Command & Tactic Coverage Summary
- **Total CEGAR-Verified Commands:** `50` (full executable list in [[commands/trained_wp-windows-management-instrumentation]])
- **Tactic Distribution:** `Enumeration` (29), `Passive_Enum` (10), `Credential_Access` (8), `Lateral_Movement_Routing_Pivot` (3)
- **Top Extracted CLI Tools:** `get-wmiobject` (3), `get-ciminstance` (2), `invoke-wmimethod` (2), `locate` (2), `new-cimsession` (2), `administrator` (1), `get-cimassociatedinstance` (1), `get-cimclass` (1), `get-cimsession` (1), `get-wminamespace` (1), `get-wminamespace-namespace$ns` (1), `get-wmiobject-class__eventconsumer@arguments` (1), `get-wmiobject-class__eventfilter@arguments` (1), `get-wmiobject-class__filtertoconsumerbinding@arguments` (1), `get-wmiobject-namespace$namespace-class__namespace` (1), `get-wmiobject-namespace$namespace-list` (1), `get-wmiobjectwin32_bios-filter'serialnumber` (1), `get-wmiobjectwin32_process-filter'name="vmtoolsd` (1), `invoke-cimmethod` (1), `invoke-wmimethod@commonargs-classstdregprov-` (1), `invoke-wmimethod@commonargs-classstdregprov-namecreatekey-` (1), `invoke-wmimethod@commonargs-classstdregprov-namedeletevalue-` (1), `invoke-wmimethod@commonargs-classwin32_process-namecreate-` (1), `last` (1), `ls` (1)

## LLM Distilled Operational Summary
### Key Operational Techniques & Decision Workflows

*   **Architecture & Standards**: Leverage WMI as the Microsoft implementation of the Web-Based Enterprise Management (WBEM) and Common Information Model (CIM) standards to query, structure, and transmit data regarding managed components (e.g., processes, services, registry).
*   **Data Consumption**: Utilize native tools like PowerShell for simple interaction and execution of WMI methods.
*   **Querying Strategy**: Use the WMI Query Language (WQL), a SQL-like language, to perform fine-grained control over object retrieval.
*   **Attack Vectors**:
    *   **Reconnaissance**: Perform system discovery and environment mapping.
    *   **Detection Evasion**: Utilize WMI for Anti-Virus and Virtual Machine (VM) detection.
    *   **Execution & Movement**: Execute code locally or remotely, facilitate lateral movement, establish persistence, and exfiltrate data.
    *   **C2 Channels**: Implement "Push" (server-initiated) or "Pull" (client-initiated) attack patterns using WMI eventing.
*   **Defense & Forensics**: Deploy existing detection utilities, build custom IDS using WMI eventing, and analyze the underlying CIM Repository file structures (MOF files, `index.btr`, `object.data`) for forensic investigation.

### Critical Command Patterns and Required Flags

*   **PowerShell**: Primary tool for interacting with WMI classes and executing methods.
*   **wmic.exe**: Legacy command-line interface for WMI operations.
*   **wbemtest.exe**: Utility for testing WMI connections and querying specific instances.
*   **WMI Explorer / CIM Studio**: GUI-based tools for visualizing namespaces, classes, and instances.
*   **Windows Script Host (WSH)**: Supports scripting languages (VBScript, JScript) for automation.
*   **COM API (IWbem*)**: Low-level C/C++ interface for programmatic access.
*   **.NET System.Management**: Managed code framework for WMI interaction.
*   **winrm.exe**: Enables remote management sessions over HTTP/HTTPS.
*   **wmic & wmis-pth**: Linux-based tools for interacting with Windows WMI remotely.

### Network Topology, IP/Subnet, Serial, and Service Relationships

*   **Protocol Foundation**: WMI relies on the Distributed Component Object Model (DCOM) for local and remote communication.
*   **Remote Management**: Utilizes Windows Remote Management (WinRM) protocols to extend reach across network boundaries.
*   **Eventing Mechanism**: Operates via an event filter/consumer model requiring specific system privileges and configuration to trigger actions (Intrinsic or Extrinsic events).
*   **Persistence**: Achieved through `ActiveScriptEventConsumer` instances, which allow scripts to run automatically upon specific system events.
*   **Storage**: Data is persisted in the CIM Repository, consisting of MOF files, binary index files (`index.btr`), and object data files (`object.data`).

## Document Structure & Key Topics
- Prep file to drop on remote system
- Establish remote WMI connection
- “Push” file contents
- The PowerShell payload that will drop the stored file contents
- Drop the file to the target filesystem
- Confirm successful file drop
- Create a remote registry key and value
- PowerShell payload that saves the serialized output of `Get-Process
- Invoke PowerShell payload
- Pull the serialized results back
- Deserialize and display the result of the command executed on the

## Extracted Operational Steps & Workflows
- 1.	 Instance queries – Used to query WMI class instances
- 2.	 Event queries – Used as a WMI event registration mechanism – e.g. WMI object
- 3.	 Meta queries – Used to query WMI class schemas
- 1.	 An event filter – The event of interest
- 2.	 An event consumer – An action to perform upon triggering an event
- 3.	 A filter to consumer binding – The registration mechanism that binds a filter
- 1.	 An attacker uses WMI as a
- 2.	 The WMI Shell utility is used as a C2
- 3.	 WMI classes are created to store
- 4.	 An attacker installs a malicious WMI
- 5.	 An attacker persists via the Start
- 6.	 An attacker persists via other
- 7.	 An attacker installs a service
- 1.	 System administrators can disable
- 2.	 Consider blocking the WMI protocol
- 3.	 WMI, DCOM, and WinRM events
- 1.	 Locate the \\.\ROOT\default
- 2.	 Find the class definition for
- 3.	 Enumerate class definitions of the
- 4.	 Build the class layout from the class
- 5.	 Find the class instance object of
- 6.	 Parse the class instance object using
- 7.	 Return the value from property
- 40. Nodes with similar keys showed
- 1.	 NS_2DDE46913C837E49ADBBDD92
- 2.	 NS_86C68CC88277F15FBE6F6D9A
- 3.	 NS_8DFCCA0B7FAB09C327554074
- 4.	 NS_AC3EFBD18065EBF47BE8D959
- 5.	 NS_DA2786B86FA728AF4EC85C5C
- 6.	 NS_DD73323810DAB2D362482D85

