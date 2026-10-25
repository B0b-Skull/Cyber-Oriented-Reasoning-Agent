---
title: "Trained Command Playbook: CQC001_E040_M005_PowerShell_Security_BSides_Charm_2016.pdf"
tags:
  - covert_exfil
  - credential_access
  - enumeration
  - http
  - https
  - kerberos
  - mdp
  - mimikatz
  - passive_enum
  - pdf
  - powershell
  - privilege_escalation
  - reconnaissance
  - splunk
  - trained
source_file: CQC001_E040_M005_PowerShell_Security_BSides_Charm_2016.pdf
updated: 2026-10-25 00:57:48
---

# Trained Command Playbook: `CQC001_E040_M005_PowerShell_Security_BSides_Charm_2016.pdf`

- **Source Document:** `~/Projects/CORA/Training/CQC001_E040_M005_PowerShell_Security_BSides_Charm_2016.pdf`
- **CEGAR Verified Commands:** `122` (`0` malformed/unsafe snippets filtered)
- **MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`):** `122`
- **Discovered IPs/Subnets:** `None`
- **Discovered Interfaces:** `None`
- **Related Knowledge Note:** [[knowledge/trained_cqc001_e040_m005_powershell_security_bsides_charm_2016]]

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

## Verified Executable Commands (Grouped by Capability Layer)

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

