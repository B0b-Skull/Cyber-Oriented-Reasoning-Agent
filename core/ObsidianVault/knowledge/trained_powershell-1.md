---
title: "Trained Knowledge & Topology: PowerShell-1.txt"
tags:
  - credential_access
  - defense_evasion_firewall
  - enumeration
  - lateral_movement_routing_pivot
  - mdp
  - netsh
  - passive_enum
  - powershell
  - reconnaissance
  - text
  - trained
source_file: PowerShell-1.txt
doc_type: text
updated: 2026-10-24 01:00:06
---

# Trained Knowledge & Architecture: `PowerShell-1.txt`

- **Source Path:** `~/Projects/CORA/Training/PowerShell-1.txt` (`text`)
- **Extracted Technical Entities:** `netsh, powershell`
- **Extracted IPs / Subnets:** `127.0.0.1, 172.17.10.71`
- **Extracted Interfaces:** `None`
- **Linked Command Playbook:** [[commands/trained_powershell-1]] (`48` CEGAR-verified commands | `48` MDP transitions)

## Command & Tactic Coverage Summary
- **Total CEGAR-Verified Commands:** `48` (full executable list in [[commands/trained_powershell-1]])
- **Tactic Distribution:** `Passive_Enum` (29), `Defense_Evasion_Firewall` (8), `Lateral_Movement_Routing_Pivot` (6), `Credential_Access` (2), `Enumeration` (2), `Reconnaissance` (1)
- **Top Extracted CLI Tools:** `get-wmiobject` (11), `netsh` (6), `get-help` (5), `gcm` (4), `get-alias` (3), `get-childitem` (2), `get-command` (2), `get-module` (2), `get-service` (2), `$psversiontable` (1), `get-credential` (1), `get-executionpolicy` (1), `get-host` (1), `get-psprovider` (1), `get-verb` (1), `select-string` (1), `set-alias` (1), `set-psdebug` (1), `set-strictmode` (1), `write-host` (1)

## LLM Distilled Operational Summary
### Operational Techniques & Decision Workflows

*   **Environment & Module Discovery**: Use `$PSVersionTable` or `Get-Host` for versioning. List all modules with `Get-Module` (loaded) or `-ListAvailable`. Retrieve provider info via `Get-PSProvider`.
*   **Alias Management**: Create aliases using `Set-Alias <new> <cmdlet>` (e.g., `Set-Alias gh Get-Help`). Verify definitions with `Get-Alias -name <target>`. Search aliases by description.
*   **Execution Policy & Debugging**: Check current policy with `Get-ExecutionPolicy -List`. Enable strict mode and debugging via `Set-StrictMode` and `Set-PSDebug` to catch uninitialized variables.
*   **Remote Service Enumeration**: Authenticate remotely using `Get-Credential`. Query remote services with `Get-WmiObject Win32_Service -computer <IP> -credential $c -Filter "state='Running'"`.
*   **Batched Remote Process Logging**: Iterate through a list of hosts (e.g., localhost, 127.0.0.1) using a `foreach` loop. Construct file paths dynamically, execute `Get-WmiObject -class win32_process`, filter out PID 0, sort by name, and output to files.
*   **WQL Queries**: Execute SQL-like queries against WMI (e.g., `Get-WmiObject -query "select * from Win32_SystemEnclosure"`).
*   **Application Removal**: Identify products via `Get-WmiObject Win32_Product` with name filters, then invoke `.Uninstall()`. Verify removal by re-querying the product list.
*   **Firewall Logging Configuration**: Enable dropped connection logging via `netsh advfirewall set allprofiles logging droppedconnections enable`. Extract specific log file paths using `Select-String` and regex patterns against `netsh` output.

### Critical Command Patterns & Flags

*   **Tab Completion**: Use the Tab key to autocomplete cmdlet names (e.g., `$PSV` for `$PSVersionTable`).
*   **Help & Examples**: Use `Get-Help <Cmdlet> -examples` or `-full` for detailed syntax. Use `gcm` as a shorthand for `Get-Command`.
*   **Filtering & Sorting**: Combine `Sort-Object` with custom expressions (e.g., sorting by date difference) and `Format-Table -AutoSize`.
*   **Credential Handling**: Always capture credentials into a variable: `$c = Get-Credential`.
*   **WMI Filtering**: Use `-Filter` parameter for simple SQL-like filtering (e.g., `"state='Running'"`).

### Network Topology & Service Relationships

*   **Target Hosts**: Scripts target specific internal IPs (e.g., `172.17.10.71`) and loopback addresses (`127.0.0.1`, `localhost`).
*   **Service State**: Primary focus is on services with `state='Running'` and `StartMode = 'Auto'`.
*   **Log Locations**: Firewall logs are located within `%systemroot%` (e.g., `C:\Windows\System32\drivers\etc\...` or similar system directories depending on OS version).
*   **

