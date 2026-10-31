---
title: "Trained Knowledge & Topology: PowerSploit"
category: knowledge
domain_hub: "[[knowledge/04_windows_powershell_wmi_cim_and_active_directory]]"
os_platform: windows
primary_tactic: Active_Enum
summary: "Operational architecture, decision workflows & Windows/Linux command reference for PowerSploit: PowerShell 2.0-7+ cmdlets, Get-CimInstance/Get-WmiObject/wmic queries, WinRM/PSRemoting (Invoke-Command, Enter-PSSession), Active "
when_to_apply: "Apply when working with PowerSploit (windows): Apply when automating Windows enumeration with PowerShell or WMI/CIM (`Get-CimInstance`/`wmic`), executing commands remotely via WinRM/WMI, enumerating Active Directory users/groups/computers/trusts/GPOs (`dsquery`/`nltest`/`net`), or auditing Kerberos tickets (`klist`) and SPNs (`setspn`)."
tags: [credential_access, enumeration, http, https, kerberos, mdp, mimikatz, nmap, passive_enum, pdf, powershell, privilege_escalation, trained, windows, wmic, get-ciminstance, winrm, invoke-command, dsquery, nltest, klist, setspn]
source_file: "PowerSploit"
updated: 2026-10-30
---

# Trained Knowledge & Architecture: `PowerSploit.pdf`

- **Source Path:** `~/Projects/CORA/Training/PowerSploit.pdf` (`pdf`)
- **Extracted Technical Entities:** `http, https, kerberos, mimikatz, nmap, powershell`
- **Extracted IPs / Subnets:** `172.24.1.0/24`
- **Extracted Interfaces:** `None`
- **Linked Command Playbook:** [[commands/trained_powersploit]] (`13` CEGAR-verified commands | `13` MDP transitions)

## Command & Tactic Coverage Summary
- **Total CEGAR-Verified Commands:** `13` (full executable list in [[commands/trained_powersploit]])
- **Tactic Distribution:** `Credential_Access` (5), `Enumeration` (3), `Privilege_Escalation` (3), `Passive_Enum` (2)
- **Top Extracted CLI Tools:** `mimikatz` (2), `base64` (1), `defaults` (1), `get-process` (1), `hexdump` (1), `invoke-tokenmanipulation` (1), `invoke-wmicommand` (1), `new-elevatedpersistenceoption` (1), `new-userpersistenceoption` (1), `out-minidump` (1), `sekurlsa::logonpasswords` (1), `strings` (1)

## LLM Distilled Operational Summary
### Key Operational Techniques & Workflows

*   **Reflective Code Execution**: Use `Invoke-ReflectivePEInjection` to load DLLs/EXEs into PowerShell or remote processes without writing files to disk. Requires a byte array (`-PEBytes`) and optional target process details (`-ProcName`, `-ProcId`).
*   **Shellcode Injection**: Utilize `Invoke-Shellcode` for injecting raw shellcode (byte arrays) into processes. Supports remote execution via `-ComputerName` and forced execution with `-Force`.
*   **Remote Command Execution**: Execute PowerShell scripts on targets using `Invoke-WmiCommand` with a scriptblock payload (`-Payload`) and optional credentials (`-Credential`).
*   **Credential Harvesting & Exfiltration**:
    *   Decrypt GPP passwords via `Get-GPPPassword`.
    *   Log keystrokes (`Get-Keystrokes`) or capture screenshots (`Get-TimedScreenshot`) with configurable intervals and timeouts.
    *   Inject Mimikatz via `Invoke-Mimikatz` to extract hashes (`lsadump::cache`), Kerberos tickets (`kerberos::list /export`), or perform DCSync (`lsadump::dcsync`).
*   **Token Manipulation**: Use `Invoke-TokenManipulation` to enumerate tokens (`-Enumerate`), revert to self (`-RevToSelf`), or create alternate processes with specific tokens (`-CreateProcess`).
*   **Memory Forensics**: Generate full-memory dumps of processes using `Out-Minidump` (pipeline-compatible with `Get-Process`).
*   **File Exfiltration**: Use `Invoke-NinjaCopy` to access locked files (e.g., `NTDS.dit`, `SYSTEM` hives) via raw disk access and copy them locally or remotely.
*   **Persistence**: Build user-land (`New-UserPersistenceOption`) or elevated (`New-ElevatedPersistenceOption`) persistence sets via Registry keys, Scheduled Tasks, or Logon triggers, then apply with `Add-Persistence`.

### Critical Command Patterns & Flags

| Function | Key Flags/Parameters |
| :--- | :--- |
| `Invoke-ReflectivePEInjection` | `-PEBytes`, `-ComputerName`, `-ExeArgs`, `-ProcName`, `-ProcId` |
| `Invoke-Shellcode` | `-ProcessID`, `-Shellcode`, `-Force` |
| `Invoke-WmiCommand` | `-Payload`, `-ComputerName`, `-Credential` |
| `Invoke-Mimikatz` | `-ComputerName`, `-Command` (e.g., `"lsadump::dcsync /user:krbtgt..."`) |
| `Invoke-NinjaCopy` | `-Path`, `-LocalDestination`, `-RemoteDestination`, `-ComputerName` |
| `Invoke-TokenManipulation` | `-Enumerate`, `-RevToSelf`, `-CreateProcess`, `-Username`, `-ProcessId` |
| `Out-Minidump` | `-Process`, `-DumpFilePath` |
| `New-UserPersistenceOption` | `-Registry`, `-AtLogon`, `-ScheduledTask`, `-OnIdle`, `-Daily`, `-Hourly`, `-At` |

### Network Topology & Service Relationships

*   **Remote Execution Targets**: Most functions (`Invoke-ReflectivePEInjection`,

<!-- CORA-MAXIMIZED-COMMANDS-START -->
## Maximized Windows & Linux Command Examples for `PowerSploit`

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
