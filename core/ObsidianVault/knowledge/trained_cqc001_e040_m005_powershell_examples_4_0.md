---
title: "Trained Knowledge & Topology: CQC001 E040 M005 PowerShell Examples 4.0"
category: knowledge
domain_hub: "[[knowledge/04_windows_powershell_wmi_cim_and_active_directory]]"
os_platform: windows
primary_tactic: Active_Enum
summary: "Operational architecture, decision workflows & Windows/Linux command reference for CQC001 E040 M005 PowerShell Examples 4.0: PowerShell 2.0-7+ cmdlets, Get-CimInstance/Get-WmiObject/wmic queries, WinRM/PSRemoting (Invoke-Command, Enter-PSSession), Active "
when_to_apply: "Apply when working with CQC001 E040 M005 PowerShell Examples 4.0 (windows): Apply when automating Windows enumeration with PowerShell or WMI/CIM (`Get-CimInstance`/`wmic`), executing commands remotely via WinRM/WMI, enumerating Active Directory users/groups/computers/trusts/GPOs (`dsquery`/`nltest`/`net`), or auditing Kerberos tickets (`klist`) and SPNs (`setspn`)."
tags: [covert_infil, enumeration, http, https, lateral_movement_routing_pivot, mdp, passive_enum, pdf, powershell, protocol_chaining, trained, windows, wmic, get-ciminstance, winrm, invoke-command, dsquery, nltest, kerberos, klist, setspn, active_directory]
source_file: "CQC001 E040 M005 PowerShell Examples 4.0"
updated: 2026-10-30
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

<!-- CORA-MAXIMIZED-COMMANDS-START -->
## Maximized Windows & Linux Command Examples for `CQC001 E040 M005 PowerShell Examples 4.0`

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
