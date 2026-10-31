---
title: "Trained Knowledge & Topology: CQC001 E040 M005 PowerShell Security BSides Charm 2016"
category: knowledge
domain_hub: "[[knowledge/04_windows_powershell_wmi_cim_and_active_directory]]"
os_platform: windows
primary_tactic: Active_Enum
summary: "Operational architecture, decision workflows & Windows/Linux command reference for CQC001 E040 M005 PowerShell Security BSides Charm 2016: PowerShell 2.0-7+ cmdlets, Get-CimInstance/Get-WmiObject/wmic queries, WinRM/PSRemoting (Invoke-Command, Enter-PSSession), Active "
when_to_apply: "Apply when working with CQC001 E040 M005 PowerShell Security BSides Charm 2016 (windows): Apply when automating Windows enumeration with PowerShell or WMI/CIM (`Get-CimInstance`/`wmic`), executing commands remotely via WinRM/WMI, enumerating Active Directory users/groups/computers/trusts/GPOs (`dsquery`/`nltest`/`net`), or auditing Kerberos tickets (`klist`) and SPNs (`setspn`)."
tags: [covert_exfil, credential_access, enumeration, http, https, kerberos, mdp, mimikatz, passive_enum, pdf, powershell, privilege_escalation, reconnaissance, splunk, trained, windows, wmic, get-ciminstance, winrm, invoke-command, dsquery, nltest]
source_file: "CQC001 E040 M005 PowerShell Security BSides Charm 2016"
updated: 2026-10-30
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

<!-- CORA-MAXIMIZED-COMMANDS-START -->
## Maximized Windows & Linux Command Examples for `CQC001 E040 M005 PowerShell Security BSides Charm 2016`

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
