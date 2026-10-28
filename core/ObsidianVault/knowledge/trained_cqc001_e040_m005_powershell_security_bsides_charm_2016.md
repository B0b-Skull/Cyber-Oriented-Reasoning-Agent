---
title: "Trained Knowledge & Topology: CQC001_E040_M005_PowerShell_Security_BSides_Charm_2016.pdf"
tags:
  - covert_exfil
  - credential_access
  - enumeration
  - http
  - https
  - kerberos
  - mdp
  - mimikatz
  - passive_enum
  - pdf
  - powershell
  - privilege_escalation
  - reconnaissance
  - splunk
  - trained
source_file: CQC001_E040_M005_PowerShell_Security_BSides_Charm_2016.pdf
doc_type: pdf
updated: 2026-10-24 00:57:48
---

# Trained Knowledge & Architecture: `CQC001_E040_M005_PowerShell_Security_BSides_Charm_2016.pdf`

- **Source Path:** `~/Projects/CORA/Training/CQC001_E040_M005_PowerShell_Security_BSides_Charm_2016.pdf` (`pdf`)
- **Extracted Technical Entities:** `http, https, kerberos, mimikatz, powershell, splunk`
- **Extracted IPs / Subnets:** `None`
- **Extracted Interfaces:** `None`
- **Linked Command Playbook:** [[commands/trained_cqc001_e040_m005_powershell_security_bsides_charm_2016]] (`122` CEGAR-verified commands | `122` MDP transitions)

## Command & Tactic Coverage Summary
- **Total CEGAR-Verified Commands:** `122` (full executable list in [[commands/trained_cqc001_e040_m005_powershell_security_bsides_charm_2016]])
- **Tactic Distribution:** `Privilege_Escalation` (40), `Covert_Exfil` (36), `Credential_Access` (18), `Enumeration` (18), `Reconnaissance` (6), `Passive_Enum` (4)
- **Top Extracted CLI Tools:** `set-wmiinstance` (3), `get-service` (2), `invoke-dllinjection` (2), `invoke-expression` (2), `invoke-psuacme` (2), `invoke-shellcode` (2), `powershell` (2), `copy-vss` (1), `find-fruit` (1), `find-gpolocation` (1), `find-trusteddocuments` (1), `get-chromedump` (1), `get-clipboardcontents` (1), `get-computerdetails` (1), `get-foxdump` (1), `get-gpppassword` (1), `get-gpppassword.ps1` (1), `get-help` (1), `get-indexeditem` (1), `get-information` (1), `get-keystrokes` (1), `get-keystrokes.ps1` (1), `get-lsasecret` (1), `get-mapdomaintrust` (1), `get-netdomaintrust` (1)

### Visual & Network Diagram Intelligence (`CQC001_E040_M005_PowerShell_Security_BSides_Charm_2016.pdf#page4`)
- **Spatially Grouped Diagram Nodes (Box/Component Clusters):**
  1. `[POWERSHELL?]`
  2. `[ITHOUGHT THIS WAS DOS | Sean Metcalf (@Pyrotek3)]`
  3. `[memegenerator.net]`

### Visual & Network Diagram Intelligence (`CQC001_E040_M005_PowerShell_Security_BSides_Charm_2016.pdf#page10`)
- **Spatially Grouped Diagram Nodes (Box/Component Clusters):**
  1. `[Typical PowerShell defenses]`
  2. `[(and why they fail) | GO AHEAD AND BLOCK | POWERSHELL.EXE]`
  3. `[IBROUGHT MY | OWN]`
  4. `[memegenerator.net]`
  5. `[Sean Metcalf (@Pyrotek3)]`
  6. `[10]`

### Visual & Network Diagram Intelligence (`CQC001_E040_M005_PowerShell_Security_BSides_Charm_2016.pdf#page14`)
- **Spatially Grouped Diagram Nodes (Box/Component Clusters):**
  1. `[PowerShell: More than PowerShell.exe]`
  2. `[PSC:\temp>$PS=[PowerShel1]::Create() | $PS.AddCommand（"Get-Process")]`
  3. `[$PS.InvokeO | Commands]`
  4. `[:System.Management.Automation.PsCommand | System.Management.Automation.PSDataStreams | 57ef9f1e-be3a-43al-a7ed-cec4e9177c76 | InvocationStateInfo :System.Management.Automation.PSInvocationStateInfo]`
  5. `[Streams | InstanceId | IsNested]`
  6. `[:False | :False]`
  7. `[HadErrors | Runspace | RunspacePool | IsRunspaceOwner]`
  8. `[System.Management.Automation.Runspaces.LocalRunspace]`
  9. `[True]`
  10. `[HistoryString | PI | 396 | Handles | 373]`
  11. `[CPU | Name]`
  12. `[Sean Metcalf (@Pyrotek3)]`
  13. `[14]`
  14. `[csrss]`

## LLM Distilled Operational Summary
### Operational Techniques & Decision Workflows
*   **Execution Policy Bypass:** When `Restricted` policy blocks `.PS1` files, use `PowerShell.exe -ExecutionPolicy Bypass` for one-off scripts or `Set-ExecutionPolicy Unrestricted` for persistent changes.
*   **Process Injection via Native Objects:** Attackers bypass `PowerShell.exe` blocking by creating a native `System.Management.Automation.PSObject` instance and injecting commands directly into its command stream without spawning the executable.
*   **Defense Evasion via ACLs:** Blocking `PowerShell.exe` via Access Control Lists (ACL) or AppLocker often fails because legitimate admin tools (Exchange, Logon) rely on it; attackers respond by dropping their own `PowerShell.exe` binary to maintain functionality.
*   **In-Memory Execution:** Scripts are downloaded and executed directly in memory, avoiding disk artifacts and traditional file-based detection.

### Critical Command Patterns & Flags
*   **Version Detection:** `$PSVersionTable`
*   **Execution Policy Bypass:** `PowerShell.exe -ExecutionPolicy Bypass`
*   **Policy Modification:** `Set-ExecutionPolicy –ExecutionPolicy UnRestricted`
*   **Native Object Creation:** `[PowerShell]::Create()`
*   **Command Injection:** `$PS.AddCommand("Get-Process")` followed by `$PS.Invoke()`
*   **Help Verification:** `Get-Help <Cmdlet> -Example`

### Network Topology & Service Relationships
*   **Primary Binary:** `PowerShell.exe` (CLI) and `PowerShell_ISE.exe` (GUI).
*   **Core Dependencies:** Leverages `.NET` framework and Windows API for deep system access (WMI, Registry, Event Logs).
*   **Service Interaction:** Commonly targets `Netlogon` service via `Get-Service -Name "Netlogon"`.
*   **Runtime Environment:** Operates within `System.Management.Automation.PSDataStreams` and `LocalRunspace` contexts.
*   **Legacy Compatibility:** Version 2 on Windows 7/2008 R2; Version 5 on Windows 10/2016.

## Document Structure & Key Topics
- Visual & Network Diagram Intelligence (`CQC001_E040_M005_PowerShell_Security_BSides_Charm_2016.pdf#page4`)
- Visual & Network Diagram Intelligence (`CQC001_E040_M005_PowerShell_Security_BSides_Charm_2016.pdf#page10`)
- Visual & Network Diagram Intelligence (`CQC001_E040_M005_PowerShell_Security_BSides_Charm_2016.pdf#page14`)

## Extracted Operational Steps & Workflows
- 1. Microsoft Defender: Now
- 2. AVG: Now (AVG
- 3. Avast:
- 4. Trend Micro: ??
- 5. Symantec: ???
- 6. McAfee: ???
- 7. Sophos: ??
- 8. Kaspersky: ??
- 9. BitDefender: ??

