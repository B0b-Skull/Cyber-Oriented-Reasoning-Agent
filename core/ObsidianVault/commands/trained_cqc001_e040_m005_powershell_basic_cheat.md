---
title: "Trained Command Playbook: CQC001_E040_M005_PowerShell_Basic_Cheat.pdf"
tags:
  - credential_access
  - enumeration
  - mdp
  - passive_enum
  - pdf
  - powershell
  - protocol_chaining
  - reconnaissance
  - trained
source_file: CQC001_E040_M005_PowerShell_Basic_Cheat.pdf
updated: 2026-10-24 00:57:39
---

# Trained Command Playbook: `CQC001_E040_M005_PowerShell_Basic_Cheat.pdf`

- **Source Document:** `~/Projects/CORA/Training/CQC001_E040_M005_PowerShell_Basic_Cheat.pdf`
- **CEGAR Verified Commands:** `55` (`0` malformed/unsafe snippets filtered)
- **MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`):** `55`
- **Discovered IPs/Subnets:** `None`
- **Discovered Interfaces:** `None`
- **Related Knowledge Note:** [[knowledge/trained_cqc001_e040_m005_powershell_basic_cheat]]

## Distilled MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`)
| Pre-State ($s$) | Tactic ($\tau$) | Technique ($k$) | Tool ($u$) | Post-State ($s'$) | Verified Command ($c$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `set-executionpolicy` | `s_active_services_enumerated` | `Set-ExecutionPolicy -ExecutionPolicy Bypass` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `get-command` | `s_passive_topology_mapped` | `Get-Command` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `write-host` | `s_credentials_or_certs_acquired` | `Write-Host "color" -ForegroundColor Red -NoNewLine` |
| `s_init_unknown` | **`Reconnaissance`** | Domain, DNS, OSINT & Target Footprint Reconnaissance | `get-member` | `s_passive_topology_mapped` | `Get-Member` |
| `s_credentials_or_certs_acquired` | **`Protocol_Chaining`** | Multi-Protocol Handshake & Tunnel Relay Chaining | `get-eventlog` | `s_protocol_chain_established` | `Get-EventLog` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `remove-item` | `s_active_services_enumerated` | `Remove-Item` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `get-command` | `s_passive_topology_mapped` | `Get-Command -Module RGHS` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `clear-host` | `s_credentials_or_certs_acquired` | `Clear-Host` |
| `s_credentials_or_certs_acquired` | **`Protocol_Chaining`** | Multi-Protocol Handshake & Tunnel Relay Chaining | `get-winevent` | `s_protocol_chain_established` | `Get-WinEvent` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `rename-item` | `s_active_services_enumerated` | `Rename-Item` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `get-command` | `s_passive_topology_mapped` | `Get-Command Get-p*` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `sort-object` | `s_credentials_or_certs_acquired` | `Sort-Object` |
| `s_credentials_or_certs_acquired` | **`Protocol_Chaining`** | Multi-Protocol Handshake & Tunnel Relay Chaining | `start-sleep` | `s_protocol_chain_established` | `Start-Sleep` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `format-table` | `s_active_services_enumerated` | `Format-Table` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `get-help` | `s_passive_topology_mapped` | `Get-help get-process` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `where-object` | `s_credentials_or_certs_acquired` | `Where-Object` |
| `s_credentials_or_certs_acquired` | **`Protocol_Chaining`** | Multi-Protocol Handshake & Tunnel Relay Chaining | `start-job` | `s_protocol_chain_established` | `Start-Job` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `format-list` | `s_active_services_enumerated` | `Format-List` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `get-process` | `s_passive_topology_mapped` | `Get-Process \| Get-Member` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `compare-object` | `s_credentials_or_certs_acquired` | `Compare-Object` |
| `s_credentials_or_certs_acquired` | **`Protocol_Chaining`** | Multi-Protocol Handshake & Tunnel Relay Chaining | `get-credential` | `s_protocol_chain_established` | `Get-Credential` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `get-content` | `s_active_services_enumerated` | `Get-Content` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `get-process` | `s_passive_topology_mapped` | `Get-Process\| format-list -properties *` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `get-childitem` | `s_credentials_or_certs_acquired` | `Get-ChildItem` |
| `s_credentials_or_certs_acquired` | **`Protocol_Chaining`** | Multi-Protocol Handshake & Tunnel Relay Chaining | `test-connection` | `s_protocol_chain_established` | `Test-Connection` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `set-content` | `s_active_services_enumerated` | `Set-Content` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `get-process` | `s_passive_topology_mapped` | `Get-Process  as list with all properties` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `get-item` | `s_credentials_or_certs_acquired` | `Get-Item` |
| `s_credentials_or_certs_acquired` | **`Protocol_Chaining`** | Multi-Protocol Handshake & Tunnel Relay Chaining | `new-pssession` | `s_protocol_chain_established` | `New-PSSession` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `get-history` | `s_active_services_enumerated` | `Get-History` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `get-ciminstance` | `s_passive_topology_mapped` | `Get-CimInstance` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `copy-item` | `s_credentials_or_certs_acquired` | `Copy-Item` |
| `s_credentials_or_certs_acquired` | **`Protocol_Chaining`** | Multi-Protocol Handshake & Tunnel Relay Chaining | `test-path` | `s_protocol_chain_established` | `Test-Path` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `invoke-history` | `s_active_services_enumerated` | `Invoke-History` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `prompt` | `s_passive_topology_mapped` | `Prompt whether to take action -WhatIf` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `move-item` | `s_credentials_or_certs_acquired` | `Move-Item` |
| `s_credentials_or_certs_acquired` | **`Protocol_Chaining`** | Multi-Protocol Handshake & Tunnel Relay Chaining | `get-aduser` | `s_protocol_chain_established` | `Get-ADUser` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `get-itemproperty` | `s_active_services_enumerated` | `Get-ItemProperty` |
| `s_credentials_or_certs_acquired` | **`Protocol_Chaining`** | Multi-Protocol Handshake & Tunnel Relay Chaining | `get-adcomputer` | `s_protocol_chain_established` | `Get-ADComputer` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `set-itemproperty` | `s_active_services_enumerated` | `Set-ItemProperty` |

## Verified Executable Commands (Grouped by Capability Layer)

### General_System (55 commands)
```bash
Set-ExecutionPolicy -ExecutionPolicy Bypass
Get-Command
Get-Command -Module RGHS
Get-Command Get-p*
Get-help get-process
Get-Process | Get-Member
Get-Process| format-list -properties *
Get-Process  as list with all properties
Write-Host "color" -ForegroundColor Red -NoNewLine
Clear-Host
Sort-Object
Where-Object
Compare-Object
Get-ChildItem
Get-Item
Copy-Item
Move-Item
Remove-Item
Rename-Item
Format-Table
Format-List
Get-CimInstance
Get-Content
Set-Content
Get-History
Invoke-History
Get-ItemProperty
Set-ItemProperty
Get-Location
Get-Member
Select-String
Set-Location
(Get-Date).Date
Get-EventLog
Get-WinEvent
Get-Date
Start-Sleep
Start-Job
Get-Credential
Test-Connection
New-PSSession
Test-Path
Get-ADUser
Get-ADComputer
New-ISESnippet
Get-WMIObject
Export-CliXML
Import-CliXML
Export-CSV
Import-CSV
Out-File
Out-String
Set-Item
New-Item
Prompt whether to take action -WhatIf
```

