---
title: "Trained Knowledge & Topology: CQC001 E040 M005 transcript"
category: knowledge
domain_hub: "[[knowledge/04_windows_powershell_wmi_cim_and_active_directory]]"
os_platform: windows
primary_tactic: Active_Enum
summary: "Operational architecture, decision workflows & Windows/Linux command reference for CQC001 E040 M005 transcript: PowerShell 2.0-7+ cmdlets, Get-CimInstance/Get-WmiObject/wmic queries, WinRM/PSRemoting (Invoke-Command, Enter-PSSession), Active "
when_to_apply: "Apply when working with CQC001 E040 M005 transcript (windows): Apply when automating Windows enumeration with PowerShell or WMI/CIM (`Get-CimInstance`/`wmic`), executing commands remotely via WinRM/WMI, enumerating Active Directory users/groups/computers/trusts/GPOs (`dsquery`/`nltest`/`net`), or auditing Kerberos tickets (`klist`) and SPNs (`setspn`)."
tags: [aws, enumeration, http, kerberos, lateral_movement_routing_pivot, mdp, mimikatz, passive_enum, pdf, powershell, reconnaissance, trained, windows, wmic, get-ciminstance, winrm, invoke-command, dsquery, nltest, klist, setspn, active_directory]
source_file: "CQC001 E040 M005 transcript"
updated: 2026-10-30
---

# Trained Knowledge & Architecture: `CQC001_E040_M005_transcript.pdf`

- **Source Path:** `~/Projects/CORA/Training/CQC001_E040_M005_transcript.pdf` (`pdf`)
- **Extracted Technical Entities:** `aws, http, kerberos, mimikatz, powershell`
- **Extracted IPs / Subnets:** `127.0.0.1, 172.24.1.10`
- **Extracted Interfaces:** `None`
- **Linked Command Playbook:** [[commands/trained_cqc001_e040_m005_transcript]] (`17` CEGAR-verified commands | `17` MDP transitions)

## Command & Tactic Coverage Summary
- **Total CEGAR-Verified Commands:** `17` (full executable list in [[commands/trained_cqc001_e040_m005_transcript]])
- **Tactic Distribution:** `Passive_Enum` (10), `Enumeration` (5), `Lateral_Movement_Routing_Pivot` (1), `Reconnaissance` (1)
- **Top Extracted CLI Tools:** `script` (4), `gcm` (3), `get-command` (2), `format-table` (1), `get-childitem` (1), `get-command,` (1), `get-service` (1), `get-wmiobject` (1), `set-item,` (1), `where-object` (1), `write-host` (1)

### Visual & Network Diagram Intelligence (`CQC001_E040_M005_transcript.pdf#page23`)

## LLM Distilled Operational Summary
### Operational Techniques & Decision Workflows
*   **Module Assessment**: Evaluate current PowerShell version compatibility (e.g., v5.0 on Windows 10/Server 2016 vs. v4.0 on pre-Windows 10) and .NET Framework prerequisites.
*   **Legacy Command Mapping**: Utilize `Get-Alias` to resolve legacy CMD or UNIX-style aliases to their underlying PowerShell cmdlets, ensuring backward compatibility during migration.
*   **Data Pipeline Construction**: Design workflows that pass complex .NET objects between cmdlets using pipes, rather than simple text streams, to simplify tasks like date/time parsing and object manipulation.
*   **Administrative Task Execution**: Leverage built-in cmdlets for registry management, WMI/CIM interaction, and system configuration without relying solely on `cmd.exe`.
*   **Scripting Environment Selection**: Choose between the standard PowerShell console for CLI-driven tasks and the Integrated Scripting Environment (ISE) for GUI-assisted development and debugging.

### Critical Command Patterns & Required Flags
*   **Alias Resolution**: `Get-Alias <AliasName>` (e.g., `Get-Alias cls`) to identify the full cmdlet path associated with a short alias.
*   **Pipeline Usage**: Chain cmdlets using the pipe operator (`|`) to flow .NET objects from output to input, enabling multi-step data processing in a single line of code.
*   **Module/Component Discovery**: Inspect module structures containing cmdlets, aliases, and providers to understand available functionality.

### Network Topology & Service Relationships
*   **Framework Dependency**: PowerShell functionality is strictly dependent on the installed version of the .NET Framework; older OS versions require manual installation of specific framework versions to support newer PowerShell releases.
*   **Integrated Service Hooks**: PowerShell management hooks are natively embedded within Microsoft server products (SQL Server, Exchange, System Center, SharePoint), creating a unified management plane across the Windows ecosystem.
*   **Interoperability Layer**: Acts as a bridge between traditional text-based CLI streams (CMD/UNIX) and object-oriented data models, allowing seamless interaction with COM and WMI services.

## Document Structure & Key Topics
- Visual & Network Diagram Intelligence (`CQC001_E040_M005_transcript.pdf#page23`)

## Extracted Operational Steps & Workflows
- 1. Obtain the directory information
- 2. Select name, length, and last access time
- 3. Format the output
- 1. Restricted - Does not load configuration files such as the Windows PowerShell profile or run
- 2. AllSigned - Requires that all scripts and configuration files be signed by a trusted publisher,
- 3. RemoteSigned - Requires that all scripts and configuration files downloaded from the Internet
- 4. Unrestricted - Loads all configuration files and runs all scripts. If you run an unsigned script that
- 5. Bypass - Blocks nothing and issues no warnings or prompts.
- 6. Undefined - Removes the currently assigned execution policy from the current scope. This
- 1. Process - The execution policy affects only the current Windows PowerShell process.
- 2. CurrentUser - The execution policy affects only the current user.
- 3. LocalMachine - The execution policy affects all users of the computer. Setting the Local-

<!-- CORA-MAXIMIZED-COMMANDS-START -->
## Maximized Windows & Linux Command Examples for `CQC001 E040 M005 transcript`

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
