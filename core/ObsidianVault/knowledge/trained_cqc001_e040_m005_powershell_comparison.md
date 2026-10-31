---
title: "Trained Knowledge & Topology: CQC001 E040 M005 PowerShell Comparison"
category: knowledge
domain_hub: "[[knowledge/04_windows_powershell_wmi_cim_and_active_directory]]"
os_platform: windows
primary_tactic: Active_Enum
summary: "Operational architecture, decision workflows & Windows/Linux command reference for CQC001 E040 M005 PowerShell Comparison: PowerShell 2.0-7+ cmdlets, Get-CimInstance/Get-WmiObject/wmic queries, WinRM/PSRemoting (Invoke-Command, Enter-PSSession), Active "
when_to_apply: "Apply when working with CQC001 E040 M005 PowerShell Comparison (windows): Apply when automating Windows enumeration with PowerShell or WMI/CIM (`Get-CimInstance`/`wmic`), executing commands remotely via WinRM/WMI, enumerating Active Directory users/groups/computers/trusts/GPOs (`dsquery`/`nltest`/`net`), or auditing Kerberos tickets (`klist`) and SPNs (`setspn`)."
tags: [curl, enumeration, mdp, passive_enum, pdf, powershell, reconnaissance, trained, windows, wmic, get-ciminstance, winrm, invoke-command, dsquery, nltest, kerberos, klist, setspn, active_directory, ldap, powerview, powerup]
source_file: "CQC001 E040 M005 PowerShell Comparison"
updated: 2026-10-30
---

# Trained Knowledge & Architecture: `CQC001_E040_M005_PowerShell_Comparison.pdf`

- **Source Path:** `~/Projects/CORA/Training/CQC001_E040_M005_PowerShell_Comparison.pdf` (`pdf`)
- **Extracted Technical Entities:** `curl, powershell`
- **Extracted IPs / Subnets:** `None`
- **Extracted Interfaces:** `None`
- **Linked Command Playbook:** [[commands/trained_cqc001_e040_m005_powershell_comparison]] (`21` CEGAR-verified commands | `21` MDP transitions)

## Command & Tactic Coverage Summary
- **Total CEGAR-Verified Commands:** `21` (full executable list in [[commands/trained_cqc001_e040_m005_powershell_comparison]])
- **Tactic Distribution:** `Enumeration` (13), `Reconnaissance` (6), `Passive_Enum` (2)
- **Top Extracted CLI Tools:** `clear-host` (1), `copy` (1), `copy-item` (1), `get-` (1), `get-content` (1), `get-help` (1), `get-location` (1), `get-process` (1), `invoke-` (1), `move-item` (1), `popd` (1), `remove-` (1), `rename` (1), `rename-` (1), `select-string` (1), `set-location` (1), `set-variable` (1), `stop-process` (1), `tee-object` (1), `test-` (1), `write-` (1)

### Visual & Network Diagram Intelligence (`CQC001_E040_M005_PowerShell_Comparison.pdf#page3`)
- **Spatially Grouped Diagram Nodes (Box/Component Clusters):**
  1. `[POWERSHELL | Features built within PowerShell]`
  2. `[History | Argument | res | Yes; multiple stacks; | (F8) | Yes | Yes | multiple location types]`
  3. `[Name | comeneldam | Path Completion | Yes | Yes | Yes]`
  4. `[Value prompt | Yes | Yes | Yes | (viaSET/ | Pcommand) | No]`
  5. `[Windows | PowerShell | Windows | CMD.EXE | Partial | ksh | Yes | (ksh93t+) | (extend-]`
  6. `[Yes | Partial | No | No | Yes | (F8) | No | No | No | Yes]`
  7. `[Yes (PUSHD, POPD) | Yes (cdpath builtin, pushd, | No | popd implemented | as functions) | Yes | Yes (cdpath, pushd, popd)]`
  8. `[Yes | able) | (extend- | able) | Yes | Yes | No | No]`
  9. `[Yes | Yes | No | No (only via | external | CHOICEcommand, | inDR-DOSalso]`
  10. `[csh | .COM | COMMAND | No]`
  11. `[Yes | No | No | No | No | No]`
  12. `[No | Yes | Yes | defined | When | Yes]`
  13. `[No | No | No | Yes (CDPATH, pushd, popd) | Yes]`
  14. `[viaSWITCH/ | DRSWITCHinternal | commands) | Yes]`
  15. `[bash (v4.0]`
  16. `[Yes]`
  17. `[3]`

## LLM Distilled Operational Summary
### Key Operational Techniques & Decision Workflows

*   **Command Selection Strategy**: Determine the target environment (PowerShell, CMD.EXE, or UNIX shell) to select the appropriate command alias. PowerShell uses `Cmdlet` syntax (e.g., `Get-ChildItem`) while legacy Windows shells use `COMMAND.COM` syntax (e.g., `dir`, `type`).
*   **Directory Navigation Workflow**: Utilize the directory stack for complex navigation. Use `Push-Location` (alias: `pushd`) to save the current path and `Pop-Location` (alias: `popd`) to restore it, enabling multi-level directory traversal without losing context.
*   **Process Management**: Identify running processes via `Get-Process` (alias: `gps`, `ps`) and terminate them using `Stop-Process` (alias: `spps`, `kill`).
*   **File & Data Manipulation**: Retrieve file contents with `Get-Content` (alias: `gc`, `type`) and list directory contents with `Get-ChildItem` (alias: `gci`, `dir`). Use `Tee-Object` to simultaneously output data to a file and pass it down the pipeline.
*   **Interactive Input Handling**: Capture user input using the `Value prompt` feature, which is native to PowerShell but limited or absent in CMD.EXE and some UNIX shells.

### Critical Command Patterns and Required Flags

*   **File Operations**:
    *   List: `Get-ChildItem` (Aliases: `gci`, `dir`, `ls`)
    *   Read: `Get-Content` (Aliases: `gc`, `type`, `cat`)
    *   Copy: `Copy-Item` (Aliases: `cpi`, `copy`, `cp`)
    *   Move/Rename: `Move-Item` / `Rename-Item` (Aliases: `mi`, `mv`, `ren`)
    *   Delete: `Remove-Item` (Aliases: `ri`, `del`, `rm`)
*   **System & Network**:
    *   Ping: `Test-Connection` (No direct alias in standard PowerShell, maps to `ping` in CMD/UNIX).
    *   Processes: `Get-Process` (Aliases: `gps`, `ps`) and `Stop-Process` (Aliases: `spps`, `kill`).
    *   Web: `Invoke-WebRequest` (Aliases: `iwr`, `curl`, `wget`).
*   **Environment & Navigation**:
    *   Current Path: `Get-Location` (Aliases: `gl`, `cd`, `pwd`).
    *   Stack Management: `Push-Location` / `Pop-Location` (Aliases: `pushd`, `popd`).
    *   Screen Clear: `Clear-Host` (Aliases: `cls`, `clear`).

### Network Topology & Service Relationships

*   **Cross-Platform Compatibility**: PowerShell provides native equivalents for common UNIX commands (`ls`, `cat`, `grep`, `ps`) and CMD commands (`dir`, `type`, `ping`), reducing the need for external tools.
*   **Stack-Based Navigation**: Unlike standard shells that rely solely on the current path, PowerShell supports a directory stack, allowing users to push and pop locations for complex script

## Document Structure & Key Topics
- Visual & Network Diagram Intelligence (`CQC001_E040_M005_PowerShell_Comparison.pdf#page3`)

<!-- CORA-MAXIMIZED-COMMANDS-START -->
## Maximized Windows & Linux Command Examples for `CQC001 E040 M005 PowerShell Comparison`

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
