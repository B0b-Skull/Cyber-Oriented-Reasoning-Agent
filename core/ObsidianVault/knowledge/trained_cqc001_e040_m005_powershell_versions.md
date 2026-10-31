---
title: "Trained Knowledge & Topology: CQC001 E040 M005 PowerShell Versions"
category: knowledge
domain_hub: "[[knowledge/04_windows_powershell_wmi_cim_and_active_directory]]"
os_platform: windows
primary_tactic: Active_Enum
summary: "Operational architecture, decision workflows & Windows/Linux command reference for CQC001 E040 M005 PowerShell Versions: PowerShell 2.0-7+ cmdlets, Get-CimInstance/Get-WmiObject/wmic queries, WinRM/PSRemoting (Invoke-Command, Enter-PSSession), Active "
when_to_apply: "Apply when working with CQC001 E040 M005 PowerShell Versions (windows): Apply when automating Windows enumeration with PowerShell or WMI/CIM (`Get-CimInstance`/`wmic`), executing commands remotely via WinRM/WMI, enumerating Active Directory users/groups/computers/trusts/GPOs (`dsquery`/`nltest`/`net`), or auditing Kerberos tickets (`klist`) and SPNs (`setspn`)."
tags: [mdp, pdf, powershell, trained, windows, wmic, get-ciminstance, winrm, invoke-command, dsquery, nltest, kerberos, klist, setspn, active_directory, ldap, powerview, powerup, powersploit, empire, active_enum, credential_access]
source_file: "CQC001 E040 M005 PowerShell Versions"
updated: 2026-10-30
---

# Trained Knowledge & Architecture: `CQC001_E040_M005_PowerShell_Versions.pdf`

- **Source Path:** `~/Projects/CORA/Training/CQC001_E040_M005_PowerShell_Versions.pdf` (`pdf`)
- **Extracted Technical Entities:** `powershell`
- **Extracted IPs / Subnets:** `None`
- **Extracted Interfaces:** `None`

### Visual & Network Diagram Intelligence (`CQC001_E040_M005_PowerShell_Versions.pdf#page1`)
- **Spatially Grouped Diagram Nodes (Box/Component Clusters):**
  1. `[POWERSHELL]`
  2. `[PowerShell Versions | PowerShell | Release | Version | Date | 1.0]`
  3. `[Default Windows | Versions | WindowsServer2008(*)]`
  4. `[AvailableWindowsVersions | Windows XP SP2 | WindowsServer 2003 R2 | Windows XP SP3 | WindowsVista | Windows Server 2003 SP2 | Windows Server 2003 SP1 | Windows Vista SP2]`
  5. `[November | 2006 | 2.0 | October | Windows7 | 2009]`
  6. `[Windows XP SP3 | WindowsServer2003SP2 | Windows Vista SP1 | Windows Vista SP2 | Windows 7 SP1 | Windows Server 2008 SP2 | WindowsServer2008R2SP1]`
  7. `[Windows Server 2008 SP1 | WindowsServer2008SP2]`
  8. `[WindowsServer2008R2(**) | Windows8 | WindowsServer2012]`
  9. `[3.0 | September | 2012 | 4.0 | October]`
  10. `[Windows 8.1 | 2013 | WindowsServer2012R2 | April 2014 | Windows10]`
  11. `[Windows 7 SP1 | Windows Server 2008 R2 SP1 | Windows Server 2012 | Windows 8.1 | Windows Server 2012 R2]`
  12. `[5.0 | (***)]`

## LLM Distilled Operational Summary
### Key Operational Techniques & Decision Workflows
- **Version-to-OS Mapping**: Correlate PowerShell release versions with specific Windows OS releases and Service Pack (SP) levels to determine native availability.
- **Release Timeline Analysis**: Track chronological release dates (e.g., Nov 2006 for v1.0, Oct 2013 for v4.0) to assess maturity and feature sets.
- **Default vs. Available Versions**: Distinguish between versions included by default in an OS installation versus those available via add-ons or later updates.

### Critical Command Patterns & Required Flags
- **Version Identification**: Use `Get-Command -Module Microsoft.PowerShell` or `powershell -Version` to identify the runtime version.
- **Compatibility Checks**: Verify OS compatibility using flags like `-Version` against known matrices (e.g., v5.0 requires Windows 10/Server 2012 R2).
- **Release Date Verification**: Cross-reference release dates (e.g., `2014-04` for v5.0) to ensure alignment with patch cycles.

### Network Topology & Service Relationships
- **OS Dependency Matrix**:
  - **v1.0**: Native to Windows Server 2008 (*), Windows XP SP2/SP3, Windows Vista/SP2.
  - **v2.0**: Native to Windows 7, Windows Server 2008 SP1/SP2, Windows Server 2008 R2 (**).
  - **v3.0**: Native to Windows 8, Windows 7 SP1, Windows Server 2012.
  - **v4.0**: Native to Windows 8.1, Windows 7 SP1, Windows Server 2012/2012 R2.
  - **v5.0**: Native to Windows 10, Windows Server 2012 R2.
- **Service Pack Constraints**: Specific SP levels (e.g., SP1, SP2) often dictate feature availability for older OS versions.
- **Release Cadence**: Major releases align with Windows OS launches (e.g., Windows 8.1 in 2013, Windows 10 in 2014).

### Summary
Operational success depends on matching the PowerShell version to the specific Windows OS and Service Pack. Key decision points involve checking default inclusion versus available versions and verifying release dates against deployment timelines.

## Document Structure & Key Topics
- Visual & Network Diagram Intelligence (`CQC001_E040_M005_PowerShell_Versions.pdf#page1`)

<!-- CORA-MAXIMIZED-COMMANDS-START -->
## Maximized Windows & Linux Command Examples for `CQC001 E040 M005 PowerShell Versions`

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
