---
title: "Trained Command Playbook: CQC001 E040 M005 PowerShell Security BSides Charm 2016"
category: commands
domain_hub: "[[knowledge/04_windows_powershell_wmi_cim_and_active_directory]]"
os_platform: windows
primary_tactic: Active_Enum
summary: "Verified Windows & Linux command playbook for CQC001 E040 M005 PowerShell Security BSides Charm 2016 (Active_Enum): PowerShell 2.0-7+ cmdlets, Get-CimInstance/Get-WmiObject/wmic queries, WinRM/PSRemoting (Invoke-Command, Enter-PSSession), Active Direc"
when_to_apply: "Apply when working with CQC001 E040 M005 PowerShell Security BSides Charm 2016 (windows): Apply when automating Windows enumeration with PowerShell or WMI/CIM (`Get-CimInstance`/`wmic`), executing commands remotely via WinRM/WMI, enumerating Active Directory users/groups/computers/trusts/GPOs (`dsquery`/`nltest`/`net`), or auditing Kerberos tickets (`klist`) and SPNs (`setspn`)."
tags: [covert_exfil, credential_access, enumeration, http, https, kerberos, mdp, mimikatz, passive_enum, pdf, powershell, privilege_escalation, reconnaissance, splunk, trained, windows, wmic, get-ciminstance, winrm, invoke-command, dsquery, nltest]
source_file: "CQC001 E040 M005 PowerShell Security BSides Charm 2016"
updated: 2026-10-30
---

powershell -NoProfile -Command "Get-CimInstance Win32_ComputerSystem | Select-Object Name,Domain,Manufacturer,Model,UserName,TotalPhysicalMemory"
# Trained Command Playbook: `CQC001_E040_M005_PowerShell_Security_BSides_Charm_2016.pdf`
powershell -NoProfile -Command "Get-CimInstance Win32_ComputerSystem | Select-Object Name,Domain,Manufacturer,Model,UserName,TotalPhysicalMemory"
- **Source Document:** `~/Projects/CORA/Training/CQC001_E040_M005_PowerShell_Security_BSides_Charm_2016.pdf`
- **CEGAR Verified Commands:** `122` (`0` malformed/unsafe snippets filtered)
- **MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`):** `122`
- **Discovered IPs/Subnets:** `None`
- **Discovered Interfaces:** `None`
- **Related Knowledge Note:** [[knowledge/trained_cqc001_e040_m005_powershell_security_bsides_charm_2016]]
powershell -NoProfile -Command "Get-CimInstance Win32_ComputerSystem | Select-Object Name,Domain,Manufacturer,Model,UserName,TotalPhysicalMemory"
## Distilled MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`)
| Pre-State ($s$) | Tactic ($\tau$) | Technique ($k$) | Tool ($u$) | Post-State ($s'$) | Verified Command ($c$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `powershell` | `s_active_services_enumerated` | `PowerShell.exe (CLI) or` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `get-service` | `s_passive_topology_mapped` | `Get-Service vs Start-Service vs Stop-Service` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `invoke-mimikatz` | `s_interactive_tty_or_priv_escalated` | `Invoke-Mimikatz` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `invoke-wmicommand.ps1` | `s_credentials_or_certs_acquired` | `Invoke-WmiCommand.ps1` |
| `s_interactive_tty_or_priv_escalated` | **`Covert_Exfil`** | Encapsulated / Low-Signature Data Telemetry Transfer | `mimikatz` | `s_covert_exfil_verified` | `Mimikatz execution from PowerShell` |
| `s_init_unknown` | **`Reconnaissance`** | Domain, DNS, OSINT & Target Footprint Reconnaissance | `get-netuser` | `s_passive_topology_mapped` | `Get-NetUser` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `invoke-expression.` | `s_active_services_enumerated` | `Invoke-Expression.` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `get-service` | `s_passive_topology_mapped` | `Get-Service -Name "Netlogon"` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `invoke-dllinjection.ps1` | `s_interactive_tty_or_priv_escalated` | `Invoke-DllInjection.ps1` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `get-gpppassword.ps1` | `s_credentials_or_certs_acquired` | `Get-GPPPassword.ps1` |
| `s_interactive_tty_or_priv_escalated` | **`Covert_Exfil`** | Encapsulated / Low-Signature Data Telemetry Transfer | `invoke-adsbackdoor` | `s_covert_exfil_verified` | `Invoke-ADSBackdoor` |
| `s_init_unknown` | **`Reconnaissance`** | Domain, DNS, OSINT & Target Footprint Reconnaissance | `get-netgroup` | `s_passive_topology_mapped` | `Get-NetGroup` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `invoke-reflectivepeinjection.` | `s_active_services_enumerated` | `Invoke-ReflectivePEInjection.` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `get-help` | `s_passive_topology_mapped` | `Get-Help Get-Service (-example/-full)` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `invoke-shellcode.ps1` | `s_interactive_tty_or_priv_escalated` | `Invoke-Shellcode.ps1` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `get-keystrokes.ps1` | `s_credentials_or_certs_acquired` | `Get-Keystrokes.ps1` |
| `s_interactive_tty_or_priv_escalated` | **`Covert_Exfil`** | Encapsulated / Low-Signature Data Telemetry Transfer | `invoke-psuacme` | `s_covert_exfil_verified` | `Invoke-PsUaCme` |
| `s_init_unknown` | **`Reconnaissance`** | Domain, DNS, OSINT & Target Footprint Reconnaissance | `get-netgroupmember` | `s_passive_topology_mapped` | `Get-NetGroupMember` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `get-netou` | `s_active_services_enumerated` | `Get-NetOU` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `powershell` | `s_passive_topology_mapped` | `powershell.exe -noprofile -windowstyle hidden -executionpolicy bypass iex` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `set-adobject` | `s_interactive_tty_or_priv_escalated` | `Set-ADObject` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `get-timedscreenshot.ps1` | `s_credentials_or_certs_acquired` | `Get-TimedScreenshot.ps1` |
| `s_interactive_tty_or_priv_escalated` | **`Covert_Exfil`** | Encapsulated / Low-Signature Data Telemetry Transfer | `remove-update` | `s_covert_exfil_verified` | `Remove-Update` |
| `s_init_unknown` | **`Reconnaissance`** | Domain, DNS, OSINT & Target Footprint Reconnaissance | `get-netlocalgroup` | `s_passive_topology_mapped` | `Get-NetLocalGroup` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `find-gpolocation` | `s_active_services_enumerated` | `Find-GPOLocation` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `invoke-downgradeaccount` | `s_interactive_tty_or_priv_escalated` | `Invoke-DowngradeAccount` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `get-vaultcredential.ps1` | `s_credentials_or_certs_acquired` | `Get-VaultCredential.ps1` |
| `s_interactive_tty_or_priv_escalated` | **`Covert_Exfil`** | Encapsulated / Low-Signature Data Telemetry Transfer | `copy-vss` | `s_covert_exfil_verified` | `Copy-VSS` |
| `s_init_unknown` | **`Reconnaissance`** | Domain, DNS, OSINT & Target Footprint Reconnaissance | `get-netsession` | `s_passive_topology_mapped` | `Get-NetSession` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `get-netgpogroup` | `s_active_services_enumerated` | `Get-NetGPOGroup` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `get-netforest` | `s_interactive_tty_or_priv_escalated` | `Get-NetForest` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `invoke-credentialinjection.ps1` | `s_credentials_or_certs_acquired` | `Invoke-CredentialInjection.ps1` |
| `s_interactive_tty_or_priv_escalated` | **`Covert_Exfil`** | Encapsulated / Low-Signature Data Telemetry Transfer | `get-information` | `s_covert_exfil_verified` | `Get-Information` |
| `s_init_unknown` | **`Reconnaissance`** | Domain, DNS, OSINT & Target Footprint Reconnaissance | `invoke-userhunter` | `s_passive_topology_mapped` | `Invoke-UserHunter` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `get-objectacl` | `s_active_services_enumerated` | `Get-ObjectACL` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `get-netforesttrust` | `s_interactive_tty_or_priv_escalated` | `Get-NetForestTrust` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `invoke-mimikatz.ps1` | `s_credentials_or_certs_acquired` | `Invoke-Mimikatz.ps1` |
| `s_interactive_tty_or_priv_escalated` | **`Covert_Exfil`** | Encapsulated / Low-Signature Data Telemetry Transfer | `get-lsasecret` | `s_covert_exfil_verified` | `Get-LSASecret` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `invoke-aclscanner` | `s_active_services_enumerated` | `Invoke-ACLScanner` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `get-netforestdomain` | `s_interactive_tty_or_priv_escalated` | `Get-NetForestDomain` |
powershell -NoProfile -Command "Get-CimInstance Win32_ComputerSystem | Select-Object Name,Domain,Manufacturer,Model,UserName,TotalPhysicalMemory"
## Verified Executable Commands (Grouped by Capability Layer)
powershell -NoProfile -Command "Get-CimInstance Win32_ComputerSystem | Select-Object Name,Domain,Manufacturer,Model,UserName,TotalPhysicalMemory"
### General_System (122 commands)
```bash
PowerShell.exe (CLI) or
Get-Service vs Start-Service vs Stop-Service
Get-Service -Name "Netlogon"
Get-Help Get-Service (-example/-full)
Invoke-Expression.
Invoke-ReflectivePEInjection.
powershell.exe -noprofile -windowstyle hidden -executionpolicy bypass iex
Invoke-Mimikatz
Invoke-DllInjection.ps1
Invoke-Shellcode.ps1
Invoke-WmiCommand.ps1
Get-GPPPassword.ps1
Get-Keystrokes.ps1
Get-TimedScreenshot.ps1
Get-VaultCredential.ps1
Invoke-CredentialInjection.ps1
Invoke-Mimikatz.ps1
Invoke-NinjaCopy.ps1
Invoke-TokenManipulation.ps1
Out-Minidump.ps1
Invoke-ReflectivePEInjection.ps1
Mimikatz execution from PowerShell
Get-NetUser
Get-NetGroup
Get-NetGroupMember
Get-NetLocalGroup
Get-NetSession
Invoke-UserHunter
Get-NetOU
Find-GPOLocation
Get-NetGPOGroup
Get-ObjectACL
Invoke-ACLScanner
Set-ADObject
Invoke-DowngradeAccount
Get-NetForest
Get-NetForestTrust
Get-NetForestDomain
Get-NetDomainTrust
Get-MapDomainTrust
Get-ServiceUnquoted
Get-ServiceFilePermission
Get-ServicePermission
Invoke-ServiceAbuse
Install-ServiceBinary
Get-RegAutoLogon
Get-RegAlwaysInstallElevated
Get-Unconstrained
Invoke-ADSBackdoor
Invoke-PsUaCme
Remove-Update
Copy-VSS
Get-Information
Get-LSASecret
Get-PassHashes
Invoke-PoshRatHttp
Invoke-PowerShellTCP
Invoke-PowerShellWMI
Start-CaptureServer
Get-GPPPassword
Invoke-NinjaCopy
Invoke-Shellcode
Invoke-WMICommand
Get-WLAN-Keys
Invoke-PsUACme
Invoke-DllInjection
Invoke-ReflectivePEInjection
Invoke-ShellCode
Get-ChromeDump
Get-ClipboardContents
Get-FoxDump
Get-IndexedItem
Get-Keystrokes
Get-Screenshot
Invoke-Inveigh
Invoke-NetRipper
Out-Minidump
Invoke-EgressCheck
Invoke-PostExfil
Invoke-PSInject
Invoke-RunAs
New-HoneyHash
Set-MacAttribute
Get-VaultCredential
Invoke-DCSync
Invoke-PowerDump
Invoke-TokenManipulation
Invoke-ThunderStruck
Invoke-VoiceTroll
Set-Wallpaper
Invoke-InveighRelay
Invoke-PsExec
Invoke-SSHCommand
Get-SecurityPackages
Install-SSP
Invoke-BackdoorLNK
Get-SiteListPassword
Get-System
Invoke-BypassUAC
Invoke-Tater
Invoke-WScriptBypassUAC
Get-RickAstley
Find-Fruit
Find-TrustedDocuments
Get-ComputerDetails
Get-SystemDNSServer
Invoke-Paranoia
Invoke-WinEnum
Get-SPN
Invoke-ARPScan
Invoke-PortScan
Invoke-ReverseDNSLookup
Invoke-SMBScanner
Get-ScheduledTask | where { $_.State -ne
$filter = Set-WmiInstance -Class __EventFilter -Namespace "root\subscription"
$consumer = Set-WmiInstance -Namespace "root\subscription" -Class
Set-WmiInstance -Namespace "root\subscription" -Class
Invoke-IR / PowerForensics
Invoke-Expression (and derivatives: "iex").
Invoke-Expression (IEX)
Invoke-DLLInjection
Remove-Item Env:\__PSLockdownPolicy
```
powershell -NoProfile -Command "Get-CimInstance Win32_ComputerSystem | Select-Object Name,Domain,Manufacturer,Model,UserName,TotalPhysicalMemory"

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
