---
title: "Trained Command Playbook: PowerShell-Remoting.txt"
tags:
  - credential_access
  - https
  - lateral_movement_routing_pivot
  - mdp
  - passive_enum
  - powershell
  - protocol_chaining
  - text
  - trained
source_file: PowerShell-Remoting.txt
updated: 2026-10-24 01:00:07
---

# Trained Command Playbook: `PowerShell-Remoting.txt`

- **Source Document:** `~/Projects/CORA/Training/PowerShell-Remoting.txt`
- **CEGAR Verified Commands:** `28` (`0` malformed/unsafe snippets filtered)
- **MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`):** `28`
- **Discovered IPs/Subnets:** `None`
- **Discovered Interfaces:** `None`
- **Related Knowledge Note:** [[knowledge/trained_powershell-remoting]]

## Distilled MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`)
| Pre-State ($s$) | Tactic ($\tau$) | Technique ($k$) | Tool ($u$) | Post-State ($s'$) | Verified Command ($c$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `enable-psremoting` | `s_credentials_or_certs_acquired` | `Enable-PSRemoting` |
| `s_firewall_or_acl_unlocked` | **`Lateral_Movement_Routing_Pivot`** | Remote Host Execution, L2/L3 Route Injection & Subnet Pivot | `get-hotfix` | `s_cross_subnet_pivot_routed` | `Get-Hotfix -ComputerName Win10 -credential barney` |
| `s_credentials_or_certs_acquired` | **`Protocol_Chaining`** | Multi-Protocol Handshake & Tunnel Relay Chaining | `get-credential` | `s_protocol_chain_established` | `$c = Get-Credential` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `get-childitem` | `s_passive_topology_mapped` | `Get-ChildItem \| Select Name, CreationTime` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `get-module` | `s_credentials_or_certs_acquired` | `Get-Module Microsoft.* \| ForEach {$_.LogPipelineExecutionDetails = $False}` |
| `s_firewall_or_acl_unlocked` | **`Lateral_Movement_Routing_Pivot`** | Remote Host Execution, L2/L3 Route Injection & Subnet Pivot | `get-hotfix` | `s_cross_subnet_pivot_routed` | `Get-Hotfix -ComputerName Win10 -credential $c` |
| `s_credentials_or_certs_acquired` | **`Protocol_Chaining`** | Multi-Protocol Handshake & Tunnel Relay Chaining | `new-pssession` | `s_protocol_chain_established` | `$session7 = New-PSSession -computername win7` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `get-childitem` | `s_passive_topology_mapped` | `Get-ChildItem \| Select Name, CreationTime, CreationTimeUTC` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `get-module` | `s_credentials_or_certs_acquired` | `Get-Module Microsoft.* \| ForEach {$_.LogPipelineExecutionDetails = $True}` |
| `s_firewall_or_acl_unlocked` | **`Lateral_Movement_Routing_Pivot`** | Remote Host Execution, L2/L3 Route Injection & Subnet Pivot | `get-hotfix` | `s_cross_subnet_pivot_routed` | `get-hotfix -computername win10 -credential $c \| where {$_.Description -match "Security"}` |
| `s_credentials_or_certs_acquired` | **`Protocol_Chaining`** | Multi-Protocol Handshake & Tunnel Relay Chaining | `new-pssession` | `s_protocol_chain_established` | `$session10 = New-PSSession -computername Win10 -credential $c` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `get-childitem` | `s_passive_topology_mapped` | `Get-ChildItem \| Select Name, CreationTime, CreationTimeUTC, LastWriteTime` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `get-winevent` | `s_credentials_or_certs_acquired` | `Get-WinEvent -FilterHashtable @{LogName='Windows PowerShell';Id ='800'} -MaxEvents 1 \| Select -Expand Message` |
| `s_credentials_or_certs_acquired` | **`Protocol_Chaining`** | Multi-Protocol Handshake & Tunnel Relay Chaining | `get-variable` | `s_protocol_chain_established` | `Get-Variable session7` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `get-childitem` | `s_passive_topology_mapped` | `Get-ChildItem \| Select Name, CreationTime, LastWriteTime, LastAccessTime` |
| `s_credentials_or_certs_acquired` | **`Protocol_Chaining`** | Multi-Protocol Handshake & Tunnel Relay Chaining | `invoke-command` | `s_protocol_chain_established` | `Invoke-Command -session $session7 {get-process}` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `reg` | `s_passive_topology_mapped` | `reg query "HKLM\SOFTWARE\Wow6432Node\Policies\Microsoft\Windows\PowerShell\ModuleLogging"` |
| `s_credentials_or_certs_acquired` | **`Protocol_Chaining`** | Multi-Protocol Handshake & Tunnel Relay Chaining | `invoke-command` | `s_protocol_chain_established` | `Invoke-Command -session $session7 -scriptblock {tasklist}` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `get-module` | `s_passive_topology_mapped` | `Get-Module Microsoft.* \| Select Name, LogPipelineExecutionDetails` |
| `s_credentials_or_certs_acquired` | **`Protocol_Chaining`** | Multi-Protocol Handshake & Tunnel Relay Chaining | `invoke-command` | `s_protocol_chain_established` | `Invoke-Command -session $session10 -scriptblock {tasklist /svc}` |
| `s_credentials_or_certs_acquired` | **`Protocol_Chaining`** | Multi-Protocol Handshake & Tunnel Relay Chaining | `new-pssession` | `s_protocol_chain_established` | `$session10 = new-pssession -computername Win10 -credential $close` |
| `s_credentials_or_certs_acquired` | **`Protocol_Chaining`** | Multi-Protocol Handshake & Tunnel Relay Chaining | `get-variable` | `s_protocol_chain_established` | `Get-Variable $session10` |
| `s_credentials_or_certs_acquired` | **`Protocol_Chaining`** | Multi-Protocol Handshake & Tunnel Relay Chaining | `enter-pssession` | `s_protocol_chain_established` | `Enter-PSSession -session $session10` |
| `s_credentials_or_certs_acquired` | **`Protocol_Chaining`** | Multi-Protocol Handshake & Tunnel Relay Chaining | `get-process` | `s_protocol_chain_established` | `Get-Process` |
| `s_credentials_or_certs_acquired` | **`Protocol_Chaining`** | Multi-Protocol Handshake & Tunnel Relay Chaining | `get-service` | `s_protocol_chain_established` | `Get-Service \| Where {$_.Status -like "Running"` |
| `s_credentials_or_certs_acquired` | **`Protocol_Chaining`** | Multi-Protocol Handshake & Tunnel Relay Chaining | `exit-pssession` | `s_protocol_chain_established` | `Exit-PSSession` |
| `s_credentials_or_certs_acquired` | **`Protocol_Chaining`** | Multi-Protocol Handshake & Tunnel Relay Chaining | `get-pssession` | `s_protocol_chain_established` | `Get-PSsession` |
| `s_credentials_or_certs_acquired` | **`Protocol_Chaining`** | Multi-Protocol Handshake & Tunnel Relay Chaining | `remove-pssession` | `s_protocol_chain_established` | `Remove-PSsession win7,win10 or Remove-PSsession -ID SessionID#` |

## Verified Executable Commands (Grouped by Capability Layer)

### General_System (28 commands)
```bash
Enable-PSRemoting
Get-Hotfix -ComputerName Win10 -credential barney
Get-Hotfix -ComputerName Win10 -credential $c
get-hotfix -computername win10 -credential $c | where {$_.Description -match "Security"}
$c = Get-Credential
$session7 = New-PSSession -computername win7
$session10 = New-PSSession -computername Win10 -credential $c
Get-Variable session7
Invoke-Command -session $session7 {get-process}
Invoke-Command -session $session7 -scriptblock {tasklist}
Invoke-Command -session $session10 -scriptblock {tasklist /svc}
$session10 = new-pssession -computername Win10 -credential $close
Get-Variable $session10
Enter-PSSession -session $session10
Get-Process
Get-Service | Where {$_.Status -like "Running"
Exit-PSSession
Get-PSsession
Remove-PSsession win7,win10 or Remove-PSsession -ID SessionID#
Get-ChildItem | Select Name, CreationTime
Get-ChildItem | Select Name, CreationTime, CreationTimeUTC
Get-ChildItem | Select Name, CreationTime, CreationTimeUTC, LastWriteTime
Get-ChildItem | Select Name, CreationTime, LastWriteTime, LastAccessTime
reg query "HKLM\SOFTWARE\Wow6432Node\Policies\Microsoft\Windows\PowerShell\ModuleLogging"
Get-Module Microsoft.* | Select Name, LogPipelineExecutionDetails
Get-Module Microsoft.* | ForEach {$_.LogPipelineExecutionDetails = $False}
Get-Module Microsoft.* | ForEach {$_.LogPipelineExecutionDetails = $True}
Get-WinEvent -FilterHashtable @{LogName='Windows PowerShell';Id ='800'} -MaxEvents 1 | Select -Expand Message
```

