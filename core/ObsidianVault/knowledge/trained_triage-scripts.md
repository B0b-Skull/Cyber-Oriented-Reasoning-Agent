---
title: "Trained Knowledge & Topology: Triage-Scripts.txt"
tags:
  - arp
  - enumeration
  - ipconfig
  - mdp
  - netstat
  - passive_enum
  - post_exploitation_verification
  - powershell
  - text
  - trained
  - wmic
source_file: Triage-Scripts.txt
doc_type: text
updated: 2026-10-25 01:00:41
---

# Trained Knowledge & Architecture: `Triage-Scripts.txt`

- **Source Path:** `~/Projects/CORA/Training/Triage-Scripts.txt` (`text`)
- **Extracted Technical Entities:** `arp, ipconfig, netstat, powershell, wmic`
- **Extracted IPs / Subnets:** `None`
- **Extracted Interfaces:** `None`
- **Linked Command Playbook:** [[commands/trained_triage-scripts]] (`40` CEGAR-verified commands | `40` MDP transitions)

## Command & Tactic Coverage Summary
- **Total CEGAR-Verified Commands:** `40` (full executable list in [[commands/trained_triage-scripts]])
- **Tactic Distribution:** `Passive_Enum` (38), `Enumeration` (1), `Post_Exploitation_Verification` (1)
- **Top Extracted CLI Tools:** `wmic` (9), `dir` (8), `get-childitem` (3), `netstat` (3), `net` (2), `tasklist` (2), `arp` (1), `date` (1), `fport` (1), `get-date` (1), `get-process` (1), `get-windowspackage` (1), `hostname` (1), `ipconfig` (1), `psloglist` (1), `route` (1), `systeminfo` (1), `t` (1), `ver` (1)

## LLM Distilled Operational Summary
### System Characterization & Time Verification
*   **Time/Version Checks**: Use `date /t`, `time /t`, and `ver` to establish baseline system state without altering settings.
*   **Session & Uptime**: Run `net session` or `net statistics {Server|Workstation}` to determine system uptime. Use `psloglist "Security" -i 528 -s | find /i "Logon Type: 10"` to identify recent interactive logons.
*   **Hardware & Network Topology**: Execute `systeminfo` for processor/memory details, `hostname` for identity, `ipconfig` for IP/DNS, and `arp -a`/`route print` for layer 2/3 topology. Use `fport` to map active port calls.

### Process & Module Analysis
*   **Process Enumeration**: Utilize `tasklist`, `wmic process list`, or PowerShell's `Get-Process` to list running processes. Filter by PID (`tasklist /fi "PID eq xxxx"`) or name (`wmic process where "name='apnmcp.exe'"`).
*   **Parent/Child Relationships**: Determine parent process IDs using `wmic process where (processid=xxxx) get parentprocessid`.
*   **Module Inspection**: Expand process modules with `get-process <name> | select -expand modules`.
*   **Executable Paths**: Retrieve full paths via `wmic process where "name='...'" get ProcessID, ExecutablePath /FORMAT:LIST`.

### File System & Registry Forensics
*   **File Properties**: Use `wmic datafile` or PowerShell (`Get-Childitem`) to inspect creation, installation, and last modification dates. Example: `wmic datafile where name='c:\\windows\\system32\\calc.exe'`.
*   **Recursive Search**: Find files by name recursively using `dir C:\ /s /b | find /i "filename"`.
*   **Date-Based Filtering**: Locate files modified within specific windows using PowerShell:
    *   Define date variables: `$FindDate = Get-Date -Year 2016 -Month 06 -Day 24`.
    *   Filter by LastWriteTime: `Where-Object { $_.LastWriteTime -ge $FindDate }`.
    *   Calculate file "age" in days using custom calculated fields for sorting.
*   **Registry Configuration**: Check NTFS last access update settings via `HKLM\System\CurrentControlSet\Control\FileSystem\NtfsDisableLastAccessUpdate`.

### Advanced PowerShell Patterns
*   **Recent Updates**: List updates installed in the last 15 days: `Get-WindowsPackage -Online | ?{ $_.InstallTime -gt [datetime]::now.AddDays(-15) }`.
*   **User Activity Analysis**: Analyze user directories for recent activity: `dir C:\users -recurse | Select Fullname,CreationTime,LastWriteTime, @{Name="Age";Expression={(Get-Date)-$_.LastWriteTime}}...`.
*   **Keyword Search**: Search for specific strings (e.g., usernames) in file contents recursively: `dir c:\*.* /s /q /t:{c|w|a}| find /i "username

