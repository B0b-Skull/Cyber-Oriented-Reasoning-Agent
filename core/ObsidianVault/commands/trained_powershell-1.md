---
title: "Trained Command Playbook: PowerShell-1.txt"
tags:
  - credential_access
  - defense_evasion_firewall
  - enumeration
  - lateral_movement_routing_pivot
  - mdp
  - netsh
  - passive_enum
  - powershell
  - reconnaissance
  - text
  - trained
source_file: PowerShell-1.txt
updated: 2026-10-25 01:00:06
---

# Trained Command Playbook: `PowerShell-1.txt`

- **Source Document:** `~/Projects/CORA/Training/PowerShell-1.txt`
- **CEGAR Verified Commands:** `48` (`0` malformed/unsafe snippets filtered)
- **MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`):** `48`
- **Discovered IPs/Subnets:** `127.0.0.1, 172.17.10.71`
- **Discovered Interfaces:** `None`
- **Related Knowledge Note:** [[knowledge/trained_powershell-1]]

## Distilled MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`)
| Pre-State ($s$) | Tactic ($\tau$) | Technique ($k$) | Tool ($u$) | Post-State ($s'$) | Verified Command ($c$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `$psversiontable` | `s_passive_topology_mapped` | `$PSVersionTable` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `get-verb` | `s_active_services_enumerated` | `Get-Verb` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `get-wmiobject` | `s_credentials_or_certs_acquired` | `Get-WmiObject -Class Win32_Service -filter "StartMode = 'Auto'"` |
| `s_firewall_or_acl_unlocked` | **`Lateral_Movement_Routing_Pivot`** | Remote Host Execution, L2/L3 Route Injection & Subnet Pivot | `get-wmiobject` | `s_cross_subnet_pivot_routed` | `Get-WmiObject Win32_Service -computer 172.17.10.71 -credential $c -Filter "state='Running'"` |
| `s_init_unknown` | **`Reconnaissance`** | Domain, DNS, OSINT & Target Footprint Reconnaissance | `write-host` | `s_passive_topology_mapped` | `Write-Host "Testing" $i "coming soon to a network near you ...";` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `set-strictmode` | `s_firewall_or_acl_unlocked` | `Set-StrictMode` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `get-host` | `s_passive_topology_mapped` | `Get-Host` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `set-psdebug` | `s_active_services_enumerated` | `Set-PSDebug` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `get-credential` | `s_credentials_or_certs_acquired` | `$c = Get-Credential` |
| `s_firewall_or_acl_unlocked` | **`Lateral_Movement_Routing_Pivot`** | Remote Host Execution, L2/L3 Route Injection & Subnet Pivot | `get-wmiobject` | `s_cross_subnet_pivot_routed` | `Get-WmiObject -computername $i -class win32_process \| Select-Object name, processID, Priority, ThreadCount, PageFaults, PageFileUsage \| Where-Object {!$_.processID -eq 0} \| Sort-Object -property name \| Format-Table \| Out-File $strFile}` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `netsh` | `s_firewall_or_acl_unlocked` | `netsh advfirewall set allprofiles state on` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `get-service` | `s_passive_topology_mapped` | `Get-Service -Name "name"` |
| `s_firewall_or_acl_unlocked` | **`Lateral_Movement_Routing_Pivot`** | Remote Host Execution, L2/L3 Route Injection & Subnet Pivot | `get-wmiobject` | `s_cross_subnet_pivot_routed` | `Get-WmiObject -query "select * from Win32_SystemEnclosure" -ComputerName win7 -Credential $c \| select SerialNumber` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `netsh` | `s_firewall_or_acl_unlocked` | `netsh advfirewall show allprofiles` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `get-psprovider` | `s_passive_topology_mapped` | `Get-PSProvider` |
| `s_firewall_or_acl_unlocked` | **`Lateral_Movement_Routing_Pivot`** | Remote Host Execution, L2/L3 Route Injection & Subnet Pivot | `get-wmiobject` | `s_cross_subnet_pivot_routed` | `$appToRemove = Get-WmiObject Win32_Product -computername win7 -credential $c -Filter "Name like '%Ask'"` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `netsh` | `s_firewall_or_acl_unlocked` | `netsh advfirewall set allprofiles logging droppedconnections enable` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `get-module` | `s_passive_topology_mapped` | `Get-Module` |
| `s_firewall_or_acl_unlocked` | **`Lateral_Movement_Routing_Pivot`** | Remote Host Execution, L2/L3 Route Injection & Subnet Pivot | `get-wmiobject` | `s_cross_subnet_pivot_routed` | `(Get-WmiObject Win32_Product -computername win7 -credential $c -filter "Name like '%Ask'").Uninstall()` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `netsh` | `s_firewall_or_acl_unlocked` | `netsh advfirewall set currentprofile logging maxfilesize 1024` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `get-module` | `s_passive_topology_mapped` | `Get-Module -ListAvailable` |
| `s_firewall_or_acl_unlocked` | **`Lateral_Movement_Routing_Pivot`** | Remote Host Execution, L2/L3 Route Injection & Subnet Pivot | `get-wmiobject` | `s_cross_subnet_pivot_routed` | `Get-WmiObject Win32_Product -computername -credential $c -Filter "Name like '%Ask'"` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `netsh` | `s_firewall_or_acl_unlocked` | `netsh firewall set logging droppedpackets=enable connections=enable maxfilesize=1024` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `get-help` | `s_passive_topology_mapped` | `Get-Help Get-Command -examples` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `netsh` | `s_firewall_or_acl_unlocked` | `netsh advfirewall show allprofiles \| Select-String FileName \| select -ExpandProperty line \| Select-String "%systemroot%.+\.log" \| select -ExpandProperty matches \| select -ExpandProperty value \| sort -uniq` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `get-help` | `s_passive_topology_mapped` | `Get-Help Get-Alias -examples` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `select-string` | `s_firewall_or_acl_unlocked` | `Select-String FileName \| select -ExpandProperty line \| Select-String "%systemroot%.+\.log" \|` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `get-help` | `s_passive_topology_mapped` | `get-help set-alias -full` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `set-alias` | `s_passive_topology_mapped` | `Set-Alias gh Get-Help` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `get-alias` | `s_passive_topology_mapped` | `Get-Alias -Description <Name>` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `get-alias` | `s_passive_topology_mapped` | `Get-Alias -name gwmi` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `get-alias` | `s_passive_topology_mapped` | `Get-Alias \| select * \| Format-Table -AutoSize` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `get-executionpolicy` | `s_passive_topology_mapped` | `Get-ExecutionPolicy -List` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `get-help` | `s_passive_topology_mapped` | `Get-Help Get-Wmi*` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `get-childitem` | `s_passive_topology_mapped` | `Get-ChildItem C:\ \| select name, length, lastaccesstime \| Format-Table -AutoSize` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `get-childitem` | `s_passive_topology_mapped` | `Get-ChildItem *.zip \| Sort-Object -property @{Expression={$_.LastWriteTime - $_.CreationTime}; Ascending=$false} \| Format-Table lastWriteTime, CreationTime` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `get-service` | `s_passive_topology_mapped` | `Get-Service \| Sort-Object -Property @{Expression="Status";Descending=$True}, @{Expression="DsiplayName";Descending=$false}` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `get-command` | `s_passive_topology_mapped` | `Get-Command Get-Command \| Format-List *` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `gcm` | `s_passive_topology_mapped` | `gcm Get-Command \| Format-List *` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `gcm` | `s_passive_topology_mapped` | `(gcm Get-Command).definition` |

## Verified Executable Commands (Grouped by Capability Layer)

### General_System (42 commands)
```bash
$PSVersionTable
Get-Host
Get-Service -Name "name"
Get-PSProvider
Get-Module
Get-Module -ListAvailable
Get-Help Get-Command -examples
Get-Help Get-Alias -examples
get-help set-alias -full
Set-Alias gh Get-Help
Get-Alias -Description <Name>
Get-Alias -name gwmi
Get-Alias | select * | Format-Table -AutoSize
Get-ExecutionPolicy -List
Get-Help Get-Wmi*
Get-Verb
Get-ChildItem C:\ | select name, length, lastaccesstime | Format-Table -AutoSize
Get-ChildItem *.zip | Sort-Object -property @{Expression={$_.LastWriteTime - $_.CreationTime}; Ascending=$false} | Format-Table lastWriteTime, CreationTime
Get-Service | Sort-Object -Property @{Expression="Status";Descending=$True}, @{Expression="DsiplayName";Descending=$false}
Get-Command Get-Command | Format-List *
gcm Get-Command | Format-List *
(gcm Get-Command).definition
gcm -verb u*
gcm -noun p*
Get-Help set* | select name, category, synopsis | Format-Table -AutoSize
Get-Command -Noun PSSessionConfiguration | select Name
Get-WmiObject Win32_Processor | Format-List *
Get-WmiObject -List | ? {$_.name -Match "Win32"}
Get-WmiObject -class Win32_bios
Get-WmiObject Win32_Service -Filter "state='Running'"
Get-WmiObject -Class Win32_Service -filter "StartMode = 'Auto'"
$c = Get-Credential
Get-WmiObject Win32_Service -computer 172.17.10.71 -credential $c -Filter "state='Running'"
Write-Host "Testing" $i "coming soon to a network near you ...";
Get-WmiObject -computername $i -class win32_process | Select-Object name, processID, Priority, ThreadCount, PageFaults, PageFileUsage | Where-Object {!$_.processID -eq 0} | Sort-Object -property name | Format-Table | Out-File $strFile}
Set-PSDebug
Set-StrictMode
Select-String FileName | select -ExpandProperty line | Select-String "%systemroot%.+\.log" |
Get-WmiObject -query "select * from Win32_SystemEnclosure" -ComputerName win7 -Credential $c | select SerialNumber
$appToRemove = Get-WmiObject Win32_Product -computername win7 -credential $c -Filter "Name like '%Ask'"
(Get-WmiObject Win32_Product -computername win7 -credential $c -filter "Name like '%Ask'").Uninstall()
Get-WmiObject Win32_Product -computername -credential $c -Filter "Name like '%Ask'"
```

### L3_Routing_NAT (6 commands)
```bash
netsh advfirewall set allprofiles state on
netsh advfirewall show allprofiles
netsh advfirewall set allprofiles logging droppedconnections enable
netsh advfirewall set currentprofile logging maxfilesize 1024
netsh firewall set logging droppedpackets=enable connections=enable maxfilesize=1024
netsh advfirewall show allprofiles | Select-String FileName | select -ExpandProperty line | Select-String "%systemroot%.+\.log" | select -ExpandProperty matches | select -ExpandProperty value | sort -uniq
```

