---
title: "Trained Knowledge & Topology: Windows+PowerShell+Logging+Cheat+Sheet+ver+June+2016+v2.pdf"
tags:
  - auditpol
  - covert_exfil
  - credential_access
  - enumeration
  - http
  - https
  - mdp
  - mimikatz
  - out-of-band_access
  - passive_enum
  - pdf
  - powershell
  - privilege_escalation
  - protocol_chaining
  - splunk
  - sysinternals
  - trained
  - wevtutil
source_file: Windows+PowerShell+Logging+Cheat+Sheet+ver+June+2016+v2.pdf
doc_type: pdf
updated: 2026-10-25 01:01:12
---

# Trained Knowledge & Architecture: `Windows+PowerShell+Logging+Cheat+Sheet+ver+June+2016+v2.pdf`

- **Source Path:** `~/Projects/CORA/Training/Windows+PowerShell+Logging+Cheat+Sheet+ver+June+2016+v2.pdf` (`pdf`)
- **Extracted Technical Entities:** `auditpol, http, https, mimikatz, powershell, splunk, sysinternals, wevtutil`
- **Extracted IPs / Subnets:** `None`
- **Extracted Interfaces:** `None`
- **Linked Command Playbook:** [[commands/trained_windows_powershell_logging_cheat_sheet_ver_june_2016_v2]] (`16` CEGAR-verified commands | `16` MDP transitions)

## Command & Tactic Coverage Summary
- **Total CEGAR-Verified Commands:** `16` (full executable list in [[commands/trained_windows_powershell_logging_cheat_sheet_ver_june_2016_v2]])
- **Tactic Distribution:** `Privilege_Escalation` (6), `Protocol_Chaining` (4), `Enumeration` (2), `Covert_Exfil` (1), `Credential_Access` (1), `Out-of-Band_Access` (1), `Passive_Enum` (1)
- **Top Extracted CLI Tools:** `enable-duplicatetoken` (1), `get-unattendedinstallfiles,` (1), `get-wmiobject` (1), `get-wmiobject,` (1), `invoke-allchecks,` (1), `invoke-command,` (1), `invoke-masstokens,` (1), `invoke-powershelludp,` (1), `invoke-powershellwmi,` (1), `invoke-servicestop,` (1), `invoke-wmimethod` (1), `out-word,` (1), `powershell` (1), `remove-poshrat,` (1), `restore-serviceexe,` (1), `set-executionpolicy,` (1)

## LLM Distilled Operational Summary
### Operational Techniques & Decision Workflows

*   **Assess Log Volume vs. Noise**: Before enabling detailed logging, evaluate disk space (500,000KB+ recommended for local logs) and determine if high-fidelity events like `EnableScriptBlockInvocationLogging` (Event IDs 4105/4106) are necessary, as they generate significant noise.
*   **Establish Baseline Execution Policy**: Set the default `ExecutionPolicy` to `RemoteSigned` via Group Policy or Registry to allow local scripts while requiring remote script signing.
*   **Enable Core Auditing Events**: Configure Group Policy to capture `ScriptBlock` and `ModuleLoad` details (Event ID 4104) for PowerShell 5 on Windows 7/2008+, which provides visibility into what code is running without excessive overhead.
*   **Implement Process Creation Correlation**: Enable standard "Process Creation" and "Command Line" logging to detect Execution Policy bypass attempts, which often manifest as Event ID 4688 entries showing the specific bypass command.
*   **Centralize Log Harvesting**: Route enabled local logs to a centralized SIEM or syslog solution for long-term retention and correlation, rather than relying solely on local storage.

### Critical Command Patterns & Required Flags

*   **Registry Configuration (PowerShell 5)**:
    *   `EnableModuleLogging`: Set to `1` (REG_DWORD) under `HKLM\SOFTWARE\Policies\Microsoft\Windows\PowerShell`.
    *   `EnableScriptBlockLogging`: Set to `1` (REG_DWORD) for basic command tracing.
    *   `EnableScriptBlockInvocationLogging`: Set to `1` (REG_DWORD) for deep tracing (use with caution due to noise).
    *   `EnableTranscripting`: Set to `1` (REG_DWORD) and specify `OutputDirectory` (REG_SZ) for file-based transcripts.
*   **Group Policy Settings**:
    *   Target: `Computer Configuration > Policies > Windows Settings > Security Settings > Local Policies > Security Options`.
    *   Key: "Turn on Script Block Logging" and "Turn on Module Logging".

### Network Topology & Service Relationships

*   **Service Dependency**: PowerShell logging relies on the **Windows Management Framework (WMF)** and the **.NET Framework** APIs. Attackers exploit these same APIs to bypass traditional AV controls.
*   **Log Event IDs**:
    *   **Event ID 4104**: PowerShell Script Block Logging (Core visibility).
    *   **Event ID 4105/4106**: PowerShell Script Block Invocation Logging (High-fidelity, noisy).
    *   **Event ID 4688**: Process Creation (Critical for detecting Execution Policy bypasses via command line arguments).
*   **Common Exploitation Tools**: Monitor logs for activity from tools like **PowerSploit**, **PowerShell Empire**, **MetaSploit**, and **SET** which often utilize WMF commands to execute with minimal local footprint.

## Extracted Operational Steps & Workflows
- 1. Why Enable and Configure PowerShell logging?  PowerShell, or its new official name, the “Windows Management
- 1. LOCAL LOG SIZE:  Increase the size of your local PowerShell logs.  Don’t worry, you have plenty of disk space, CPU is not
- 2. LOCAL SECURITY POLICY:  No settings needed
- 3. GROUP POLICY:  You can control all the PowerShell settings in Group Policy
- 4. REGISTRY SETTINGS:
- 1. The ability to bypass your PowerShell controls is a concern and why it is crucial to alert on these bypass attempts as an indication
- 2. Execution Policy Bypass:  The Execution Policy that you set can be bypassed by anyone with malicious intent.  Alert on
- 3. Profile Bypass:  The profile(s) you set to configure PowerShell when each session is launched can also be bypassed.
- 4. These commands are often joined in malicious activity and can be in any form of the following:
- 1. PowerShell Transcript:  For PowerShell versions 2, 3, 4 & 5.  You can record a PowerShell transcript of everything
- 2. You may also Start and Stop the transcripts as needed within your scripts with Start-Transcript or Stop-Transcript
- 1. WEvtUtil:  Use this utility to configure your log settings or configure them in Group Policy
- 2. For more history in your logs, consider making the log size 1GB
- 1. Default Profile:  In order to capture the command line of a Windows PowerShell session for all users on the system,
- 1. Reg.exe:  Use this utility to query the registry and check the settings
- 1. REGISTRY AUDIT:  To help you catch malicious activity trying to alter your PowerShell configuration, audit the
- 2. POWERSHELL KEYS TO AUDIT:
- 1. PowerShell Versions and OS:  The ability to perform advanced logging of PowerShell is limited to certain operating
- 1. LOG CLEAR:  Watch for log clear messages
- 1. PROCESSES:  Watch for a Process to start and call
- 1. REGISTRY:  Monitor certain Keys for Add, Changes and
- 1. WEvtUtil:  Use this utility to query your logs
- 2. Filtering Log Results:  Use this method to filter lines within the logs
- 3. For PowerShell 4 and 5 Event ID 4104.  These logs are large in content
- 4. Get-EventLog:  Use this PowerShell module to query your logs.  There too many options to list here, but here a
- 1. FIREWALL:  Windows Filtering Platform - Watch for Inbound and Outbound connections – Requires Windows Firewall to be
- 1. Monitor for these Dll’s being called by an executable other than PowerShell.exe or PowerShell_ISE.exe
- 2. Monitor for calls to WMI, they are not necessarily malicious, but could indicate WMI is being used in an attack
- 3. In order to detect PowerShell DLL’s being called by something other than PowerShell.exe or PowerShell_ISE.exe, you should
- 1. PROFILES:  Locations that profile.ps1 can be stored should be monitored for new profiles or changes since these can be
- 1. POWERSHELL  MODULES:  The following is a list of PowerShell module calls that you should monitor for executing using

