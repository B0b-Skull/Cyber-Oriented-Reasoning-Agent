---
title: "Trained Command Playbook: CQC001_E040_M005_PowerShell_Examples_4.0.pdf"
tags:
  - covert_infil
  - enumeration
  - http
  - https
  - lateral_movement_routing_pivot
  - mdp
  - passive_enum
  - pdf
  - powershell
  - protocol_chaining
  - trained
source_file: CQC001_E040_M005_PowerShell_Examples_4.0.pdf
updated: 2026-10-25 00:57:41
---

# Trained Command Playbook: `CQC001_E040_M005_PowerShell_Examples_4.0.pdf`

- **Source Document:** `~/Projects/CORA/Training/CQC001_E040_M005_PowerShell_Examples_4.0.pdf`
- **CEGAR Verified Commands:** `20` (`0` malformed/unsafe snippets filtered)
- **MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`):** `20`
- **Discovered IPs/Subnets:** `None`
- **Discovered Interfaces:** `None`
- **Related Knowledge Note:** [[knowledge/trained_cqc001_e040_m005_powershell_examples_4_0]]

## Distilled MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`)
| Pre-State ($s$) | Tactic ($\tau$) | Technique ($k$) | Tool ($u$) | Post-State ($s'$) | Verified Command ($c$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `new-jobtrigger` | `s_active_services_enumerated` | `$trigger = New-JobTrigger -Daily -At 3am` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `get-childitem` | `s_passive_topology_mapped` | `Get-ChildItem *.ps1 -pv a \| Get-Acl \| foreach {"{0} size is {1}" -f $a.Name, $a.length}` |
| `s_firewall_or_acl_unlocked` | **`Lateral_Movement_Routing_Pivot`** | Remote Host Execution, L2/L3 Route Injection & Subnet Pivot | `test-netconnection` | `s_cross_subnet_pivot_routed` | `Test-NetConnection -ComputerName microsoft.com -InformationLevel Detailed` |
| `s_protocol_chain_established` | **`Covert_Infil`** | Staged Artifact / Encapsulated Ingress Delivery | `get-filehash` | `s_covert_infil_channel_ready` | `Get-FileHash C:\downloads\WindowsOS.iso -Algorithm SHA384` |
| `s_credentials_or_certs_acquired` | **`Protocol_Chaining`** | Multi-Protocol Handshake & Tunnel Relay Chaining | `invoke-command` | `s_protocol_chain_established` | `$m = Invoke-Command -ComputerName RemoteServer -ScriptBlock { Get Module  -` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `register-scheduledjob` | `s_active_services_enumerated` | `Register-ScheduledJob -Name DailyBackup -Trigger $trigger -ScriptBlock {Copy-Item` |
| `s_firewall_or_acl_unlocked` | **`Lateral_Movement_Routing_Pivot`** | Remote Host Execution, L2/L3 Route Injection & Subnet Pivot | `test-netconnection` | `s_cross_subnet_pivot_routed` | `Test-NetConnection -ComputerName microsoft.com -Port 80 -InformationLevel Quiet` |
| `s_protocol_chain_established` | **`Covert_Infil`** | Staged Artifact / Encapsulated Ingress Delivery | `invoke-webrequest` | `s_covert_infil_channel_ready` | `$iwr = Invoke-WebRequest http://blogs.msdn.com/b/powershell` |
| `s_credentials_or_certs_acquired` | **`Protocol_Chaining`** | Multi-Protocol Handshake & Tunnel Relay Chaining | `new-pssession` | `s_protocol_chain_established` | `$s = New-PSSession -ComputerName RemoteServer` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `get-job` | `s_active_services_enumerated` | `Get-Job -Name DailyBackup \| Receive-Job` |
| `s_protocol_chain_established` | **`Covert_Infil`** | Staged Artifact / Encapsulated Ingress Delivery | `invoke-restmethod` | `s_covert_infil_channel_ready` | `$irm = Invoke-RestMethod blogs.msdn.com/b/powershell/rss.aspx` |
| `s_credentials_or_certs_acquired` | **`Protocol_Chaining`** | Multi-Protocol Handshake & Tunnel Relay Chaining | `get-module` | `s_protocol_chain_established` | `$m = Get-Module -PSSession $s -Name DhcpServer -ListAvailable` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `start-job` | `s_active_services_enumerated` | `Start-Job -DefinitionName DailyBackup` |
| `s_credentials_or_certs_acquired` | **`Protocol_Chaining`** | Multi-Protocol Handshake & Tunnel Relay Chaining | `new-cimsession` | `s_protocol_chain_established` | `$c = New-CimSession -ComputerName RemoteServer` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `register-scheduledjob` | `s_active_services_enumerated` | `Register-ScheduledJob -Name Backup -ScriptBlock {Copy-Item c:\ImportantFiles d: Backup$((Get-Date).ToFileTime()) -Recurse -Force -PassThru} -RunNow` |
| `s_credentials_or_certs_acquired` | **`Protocol_Chaining`** | Multi-Protocol Handshake & Tunnel Relay Chaining | `get-module` | `s_protocol_chain_established` | `$m = Get-Module -CimSession $c -Name DhcpServer -ListAvailable` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `invoke-restmethod` | `s_active_services_enumerated` | `$sessions = Invoke-RestMethod https://odata.eventpointdata.com/tena2014/` |
| `s_credentials_or_certs_acquired` | **`Protocol_Chaining`** | Multi-Protocol Handshake & Tunnel Relay Chaining | `invoke-command` | `s_protocol_chain_established` | `Invoke-Command -ComputerName Server 1 { param($localVar) echo $localVar } -ArgumentList $localVar` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `invoke-item` | `s_active_services_enumerated` | `Invoke-Item $env:TEMP\sessions.csv` |
| `s_credentials_or_certs_acquired` | **`Protocol_Chaining`** | Multi-Protocol Handshake & Tunnel Relay Chaining | `invoke-command` | `s_protocol_chain_established` | `Invoke-Command -ComputerName Server1 { echo $using:localVar }` |

## Verified Executable Commands (Grouped by Capability Layer)

### General_System (18 commands)
```bash
$trigger = New-JobTrigger -Daily -At 3am
Register-ScheduledJob -Name DailyBackup -Trigger $trigger -ScriptBlock {Copy-Item
Get-Job -Name DailyBackup | Receive-Job
Start-Job -DefinitionName DailyBackup
Register-ScheduledJob -Name Backup -ScriptBlock {Copy-Item c:\ImportantFiles d: Backup$((Get-Date).ToFileTime()) -Recurse -Force -PassThru} -RunNow
Get-ChildItem *.ps1 -pv a | Get-Acl | foreach {"{0} size is {1}" -f $a.Name, $a.length}
Test-NetConnection -ComputerName microsoft.com -InformationLevel Detailed
Test-NetConnection -ComputerName microsoft.com -Port 80 -InformationLevel Quiet
Get-FileHash C:\downloads\WindowsOS.iso -Algorithm SHA384
$irm = Invoke-RestMethod blogs.msdn.com/b/powershell/rss.aspx
Invoke-Item $env:TEMP\sessions.csv
$m = Invoke-Command -ComputerName RemoteServer -ScriptBlock { Get Module  -
$s = New-PSSession -ComputerName RemoteServer
$m = Get-Module -PSSession $s -Name DhcpServer -ListAvailable
$c = New-CimSession -ComputerName RemoteServer
$m = Get-Module -CimSession $c -Name DhcpServer -ListAvailable
Invoke-Command -ComputerName Server 1 { param($localVar) echo $localVar } -ArgumentList $localVar
Invoke-Command -ComputerName Server1 { echo $using:localVar }
```

### L7_HTTP_Web (2 commands)
```bash
$iwr = Invoke-WebRequest http://blogs.msdn.com/b/powershell
$sessions = Invoke-RestMethod https://odata.eventpointdata.com/tena2014/
```

