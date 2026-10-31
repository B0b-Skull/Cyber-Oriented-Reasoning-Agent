---
title: "Trained Knowledge & Topology: PowerShell-1"
category: knowledge
domain_hub: "[[knowledge/04_windows_powershell_wmi_cim_and_active_directory]]"
os_platform: windows
primary_tactic: Active_Enum
summary: "Operational architecture, decision workflows & Windows/Linux command reference for PowerShell-1: PowerShell 2.0-7+ cmdlets, Get-CimInstance/Get-WmiObject/wmic queries, WinRM/PSRemoting (Invoke-Command, Enter-PSSession), Active "
when_to_apply: "Apply when working with PowerShell-1 (windows): Apply when automating Windows enumeration with PowerShell or WMI/CIM (`Get-CimInstance`/`wmic`), executing commands remotely via WinRM/WMI, enumerating Active Directory users/groups/computers/trusts/GPOs (`dsquery`/`nltest`/`net`), or auditing Kerberos tickets (`klist`) and SPNs (`setspn`)."
tags: [credential_access, defense_evasion_firewall, enumeration, lateral_movement_routing_pivot, mdp, netsh, passive_enum, powershell, reconnaissance, text, trained, windows, wmic, get-ciminstance, winrm, invoke-command, dsquery, nltest, kerberos, klist, setspn, active_directory]
source_file: "PowerShell-1"
updated: 2026-10-30
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

<!-- CORA-MAXIMIZED-COMMANDS-START -->
## Maximized Windows & Linux Command Examples for `PowerShell-1`

> **Domain Hub:** [[knowledge/04_windows_powershell_wmi_cim_and_active_directory|Domain Hub 04: Windows PowerShell, WMI/CIM, WinRM Remoting, Active Directory (dsquery), Kerberos & Post-Exploitation]]  
> **Master Playbooks:** [[commands/windows_master_command_playbook]] | [[commands/linux_master_command_playbook]] | [[commands/curl_playbook]] | [[commands/tio_serial_playbook]]  
> **When to Apply:** Apply when automating Windows enumeration with PowerShell or WMI/CIM (`Get-CimInstance`/`wmic`), executing commands remotely via WinRM/WMI, enumerating Active Directory users/groups/computers/trusts/GPOs (`dsquery`/`nltest`/`net`), or auditing Kerberos tickets (`klist`) and SPNs (`setspn`).  
> **15-Engine H-MDP State Transition:** `s_active_services_enumerated` $\xrightarrow{\text{Active_Enum}}$ `s_credentials_or_certs_acquired` | **Bayesian Root-Cause Triggers:** `ad_domain_trust_or_spn_exposure, winrm_or_wmi_lateral_movement_path, kerberos_ticket_or_delegation_weakness, unquoted_service_or_gpo_misconfig` | **Isolation:** `RED, BLUE (Active Directory / WinRM network queries require allowed LAN interface; local CIM/WMI works in WHITE)`

| Primary Command (`Windows` / `Linux`) | OS / Shell | What It Does & Key Flags | When to Apply & Expected Output | Cross-Platform Equivalent |
| :--- | :--- | :--- | :--- | :--- |
| `powershell -NoProfile -Command "Get-CimInstance Win32_ComputerSystem \| Select-Object Name,Domain,Manufacturer,Model,UserName,TotalPhysicalMemory"` | **PowerShell** | Queries `Win32_ComputerSystem` via modern CIM (WS-Man/DCOM) for host domain membership, logged-on console user, and hardware model. | Apply in PowerShell 4.0+ as the fast, structured replacement for `wmic computersystem` (`[[knowledge/trained_ps_get-cim]]`). | `hostnamectl && lscpu && free -h` |
| `powershell -NoProfile -Command "Get-CimInstance Win32_Service \| Where-Object {$_.State -eq 'Running' -and $_.PathName -notmatch 'C:\\Windows'} \| Select-Object Name,DisplayName,StartName,PathName"` | **PowerShell** | Finds all running third-party/custom Windows services whose binary path is outside `C:\Windows`. | Apply to quickly isolate non-OS services and inspect their execution account (`StartName`) and binary path. | `systemctl list-units --type=service --state=running` |
| `powershell -NoProfile -Command "Get-CimInstance -Namespace root\subscription -ClassName __EventFilter; Get-CimInstance -Namespace root\subscription -ClassName CommandLineEventConsumer; Get-CimInstance -Namespace root\subscription -ClassName __FilterToConsumerBinding"` | **PowerShell** | Audits the `root\subscription` WMI repository for permanent WMI Event Filters, Consumers, and Bindings. | Apply to detect fileless WMI persistence (`[[knowledge/trained_us-15-graeber-abusing-windows-management-instrumentation-wmi-to-]]`). | `crontab -l && systemctl list-timers --all` |
| `wmic /node:"<TARGET_IP>" process call create "cmd.exe /c ipconfig /all > C:\Temp\out.txt"` | **Windows CMD** | Executes a command remotely on `<TARGET_IP>` over DCOM/RPC (`TCP 135` + dynamic high ports) using WMI `Win32_Process.Create`. | Apply for agentless remote execution across domain hosts when WinRM (`5985`) is closed but RPC (`135`) is open. | `ssh <USER>@<TARGET_IP> 'ip -4 -br addr'` |
| `winrm enumerate winrm/config/listener && powershell -NoProfile -Command "Test-WSMan -ComputerName <TARGET_IP>"` | **CMD / PS** | Enumerates local WinRM listeners (`5985` HTTP / `5986` HTTPS) and tests WS-Management reachability on `<TARGET_IP>`. | Apply before running `Invoke-Command` or `Enter-PSSession` (`[[commands/trained_powershell-remoting]]`). | `nc -zv <TARGET_IP> 22` |
| `powershell -NoProfile -Command "Invoke-Command -ComputerName <TARGET_IP> -ScriptBlock { hostname; whoami /all; Get-NetIPConfiguration }"` | **PowerShell** | Executes a PowerShell script block on remote host `<TARGET_IP>` over WinRM (`TCP 5985`/`5986`) and returns serialized objects. | Apply for multi-host administrative command execution and remote triage. | `ssh <USER>@<TARGET_IP> 'hostname; id; ip addr'` |
| `nltest /dclist: && nltest /domain_trusts /all_trusts` | **Windows CMD** | Discovers all Domain Controllers in the current domain and enumerates all forest/external/transitive domain trusts. | Apply first during Active Directory reconnaissance (`[[commands/trained_domain_service_tools]]`). | `dig _ldap._tcp.dc._msdcs.<DOMAIN> SRV` |
| `net user /domain && net group "Domain Admins" /domain && net group "Enterprise Admins" /domain` | **Windows CMD** | Queries the Domain Controller for all domain user accounts and members of high-privilege administrative groups. | Apply on any domain-joined workstation/server to map privileged accounts (`[[commands/trained_net_cmds_1]]`). | `ldapsearch -x -H ldap://<DC_IP> -b 'dc=domain,dc=local'` |
| `dsquery user -limit 0 \| dsget user -samid -sid -upn -pwdneverexpires -disabled && dsquery computer -limit 0` | **Windows CMD (AD)** | Queries Active Directory LDAP for all user accounts (with SAMID, SID, and password expiry flags) and all domain computers (`[[commands/trained_ds_cmds]]`). | Apply when RSAT or DC tools are present to export complete Active Directory object inventories. | `ldapsearch -LLL -H ldap://<DC_IP> '(objectClass=user)' sAMAccountName objectSid` |
| `setspn -Q */* && klist` | **Windows CMD** | Lists all Service Principal Names (`SPNs`) registered in Active Directory (`setspn -Q */*`) and inspects cached Kerberos tickets (`klist`). | Apply to locate SQL/HTTP/Exchange service accounts (`Kerberoasting` audit) and verify active TGT/TGS encryption types (`[[knowledge/trained_kerberos_attacks_cheatsheet]]`). | `klist && kvno <SPN>` |

### Copy-Pasteable Execution Block (Windows & Linux)
```bash
# [PowerShell] Queries `Win32_ComputerSystem` via modern CIM (WS-Man/DCOM) for host domain membership, logged-on console user, and hardware model.
powershell -NoProfile -Command "Get-CimInstance Win32_ComputerSystem | Select-Object Name,Domain,Manufacturer,Model,UserName,TotalPhysicalMemory"
# [PowerShell] Finds all running third-party/custom Windows services whose binary path is outside `C:\Windows`.
powershell -NoProfile -Command "Get-CimInstance Win32_Service | Where-Object {$_.State -eq 'Running' -and $_.PathName -notmatch 'C:\\Windows'} | Select-Object Name,DisplayName,StartName,PathName"
# [PowerShell] Audits the `root\subscription` WMI repository for permanent WMI Event Filters, Consumers, and Bindings.
powershell -NoProfile -Command "Get-CimInstance -Namespace root\subscription -ClassName __EventFilter; Get-CimInstance -Namespace root\subscription -ClassName CommandLineEventConsumer; Get-CimInstance -Namespace root\subscription -ClassName __FilterToConsumerBinding"
# [Windows CMD] Executes a command remotely on `<TARGET_IP>` over DCOM/RPC (`TCP 135` + dynamic high ports) using WMI `Win32_Process.Create`.
wmic /node:"<TARGET_IP>" process call create "cmd.exe /c ipconfig /all > C:\Temp\out.txt"
# [CMD / PS] Enumerates local WinRM listeners (`5985` HTTP / `5986` HTTPS) and tests WS-Management reachability on `<TARGET_IP>`.
winrm enumerate winrm/config/listener && powershell -NoProfile -Command "Test-WSMan -ComputerName <TARGET_IP>"
# [PowerShell] Executes a PowerShell script block on remote host `<TARGET_IP>` over WinRM (`TCP 5985`/`5986`) and returns serialized objects.
powershell -NoProfile -Command "Invoke-Command -ComputerName <TARGET_IP> -ScriptBlock { hostname; whoami /all; Get-NetIPConfiguration }"
```
<!-- CORA-MAXIMIZED-COMMANDS-END -->
