---
title: "Trained Knowledge & Topology: WMIC QuickStart"
category: knowledge
domain_hub: "[[knowledge/04_windows_powershell_wmi_cim_and_active_directory]]"
os_platform: windows
primary_tactic: Active_Enum
summary: "Operational architecture, decision workflows & Windows/Linux command reference for WMIC QuickStart: PowerShell 2.0-7+ cmdlets, Get-CimInstance/Get-WmiObject/wmic queries, WinRM/PSRemoting (Invoke-Command, Enter-PSSession), Active "
when_to_apply: "Apply when working with WMIC QuickStart (windows): Apply when automating Windows enumeration with PowerShell or WMI/CIM (`Get-CimInstance`/`wmic`), executing commands remotely via WinRM/WMI, enumerating Active Directory users/groups/computers/trusts/GPOs (`dsquery`/`nltest`/`net`), or auditing Kerberos tickets (`klist`) and SPNs (`setspn`)."
tags: [defense_evasion_firewall, mdp, passive_enum, text, trained, wmic, windows, powershell, get-ciminstance, winrm, invoke-command, dsquery, nltest, kerberos, klist, setspn, active_directory, ldap, powerview, powerup, powersploit, empire]
source_file: "WMIC QuickStart"
updated: 2026-10-30
---

# Trained Knowledge & Architecture: `WMIC QuickStart.txt`

- **Source Path:** `~/Projects/CORA/Training/WMIC QuickStart.txt` (`text`)
- **Extracted Technical Entities:** `wmic`
- **Extracted IPs / Subnets:** `None`
- **Extracted Interfaces:** `None`
- **Linked Command Playbook:** [[commands/trained_wmic_quickstart]] (`12` CEGAR-verified commands | `12` MDP transitions)

## Command & Tactic Coverage Summary
- **Total CEGAR-Verified Commands:** `12` (full executable list in [[commands/trained_wmic_quickstart]])
- **Tactic Distribution:** `Passive_Enum` (11), `Defense_Evasion_Firewall` (1)
- **Top Extracted CLI Tools:** `wmic` (11), `rundll32` (1)

## LLM Distilled Operational Summary
### Operational Techniques & Decision Workflows

*   **Platform Compatibility Check**: Verify the target OS is Windows XP Pro before executing `wmic.exe`, as it is absent in Windows 2000 and XP Home editions.
*   **Process Analysis Workflow**:
    *   Use `/format:csv` to generate comma-separated values for program names and memory usage (`workingsetsize`).
    *   Pipe output to `sort` to alphabetize process lists for easier scanning.
*   **Hardware Inventory**:
    *   Query disk drives (`wmic diskdrive`) for model, name, and size.
    *   Query partitions (`wmic partition`) for name, size, and type (e.g., Installable File System).
    *   Extract BIOS serial numbers and product identifying numbers (Service Tags) from `wmic bios` and `wmic csproduct`.
*   **Patch Management Audit**: Retrieve installed Windows patches and their installation dates using `wmic qfe` formatted as CSV.
*   **Memory Verification**: Confirm physical RAM capacity via `wmic COMPUTERSYSTEM`.
*   **Network Interface Discovery**: List all network adapters with descriptions and MAC addresses using `wmic nic`.

### Critical Command Patterns & Required Flags

*   **Standard Query**: `wmic [class] get [properties]`
    *   *Example*: `wmic process get workingsetsize,commandline`
*   **CSV Formatting**: Append `/format:csv` to any query for machine-readable output.
    *   *Example*: `wmic qfe get description,installedOn /format:csv`
*   **Output Sorting**: Pipe results to the `sort` command.
    *   *Example*: `wmic process | sort`
*   **Remote Connection**: Use the `node` parameter to target remote WMI instances (specific syntax not fully detailed in chunk, but implied by section header).

### Network Topology & Service Relationships

*   **Local Service Mapping**: The process list reveals specific service associations:
    *   `svchost.exe` instances are grouped by `-k` flags (e.g., `-k DcomLaunch`, `-k rpcss`, `-k netsvcs`).
    *   Third-party services include Symantec components (`ccApp.exe`, `DefWatch.exe`, `Rtvscan.exe`) and Mozilla (`mozilla.exe`).
*   **Network Interfaces**: Identified adapters include:
    *   Wireless: Intel(R) PRO/Wireless 215ABG.
    *   Wired: Broadcom NetXtreme 57xx Gigabit Controller.
    *   Virtual/Remote: WAN Miniports (L2TP, PPTP, PPPOE) and RAS Async Adapter.
*   **Hardware Identification**: The system is identified as a Dell Latitude D610 with a Phoenix ROM BIOS.

<!-- CORA-MAXIMIZED-COMMANDS-START -->
## Maximized Windows & Linux Command Examples for `WMIC QuickStart`

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
