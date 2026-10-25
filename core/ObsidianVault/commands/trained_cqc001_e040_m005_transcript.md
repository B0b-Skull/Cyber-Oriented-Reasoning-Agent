---
title: "Trained Command Playbook: CQC001_E040_M005_transcript.pdf"
tags:
  - aws
  - enumeration
  - http
  - kerberos
  - lateral_movement_routing_pivot
  - mdp
  - mimikatz
  - passive_enum
  - pdf
  - powershell
  - reconnaissance
  - trained
source_file: CQC001_E040_M005_transcript.pdf
updated: 2026-10-25 00:57:53
---

# Trained Command Playbook: `CQC001_E040_M005_transcript.pdf`

- **Source Document:** `~/Projects/CORA/Training/CQC001_E040_M005_transcript.pdf`
- **CEGAR Verified Commands:** `17` (`0` malformed/unsafe snippets filtered)
- **MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`):** `17`
- **Discovered IPs/Subnets:** `127.0.0.1, 172.24.1.10`
- **Discovered Interfaces:** `None`
- **Related Knowledge Note:** [[knowledge/trained_cqc001_e040_m005_transcript]]

## Distilled MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`)
| Pre-State ($s$) | Tactic ($\tau$) | Technique ($k$) | Tool ($u$) | Post-State ($s'$) | Verified Command ($c$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `set-item,` | `s_passive_topology_mapped` | `Set-Item, Get-ChildItem, Remove-Item, etc. also work with the registry.` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `format-table` | `s_active_services_enumerated` | `Format-Table LastWriteTime, CreationTime` |
| `s_init_unknown` | **`Reconnaissance`** | Domain, DNS, OSINT & Target Footprint Reconnaissance | `write-host` | `s_passive_topology_mapped` | `Write-Host "Testing" $i "coming soon to a network near you ...";` |
| `s_firewall_or_acl_unlocked` | **`Lateral_Movement_Routing_Pivot`** | Remote Host Execution, L2/L3 Route Injection & Subnet Pivot | `get-wmiobject` | `s_cross_subnet_pivot_routed` | `Get-WmiObject -computername $i -class win32_process \| Select-Object name, processID, Priority, ThreadCount, PageFaults,` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `get-command,` | `s_passive_topology_mapped` | `Get-Command, or Get-PSProvider. When cmdlets use the "Get" Verb pattern, they display` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `script` | `s_active_services_enumerated` | `Script block logging records blocks of code as they are executed by the PowerShell engine, thereby` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `get-command` | `s_passive_topology_mapped` | `Get-Command` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `script` | `s_active_services_enumerated` | `Script block logging will not record output from the executed code. Script block logging events are` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `gcm` | `s_passive_topology_mapped` | `gcm Get-Command \| Format-List *` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `script` | `s_active_services_enumerated` | `Script block logging generates fewer events than module logging, and records valuable indicators` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `gcm` | `s_passive_topology_mapped` | `gcm -verb u*` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `script` | `s_active_services_enumerated` | `Script block logging, and` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `gcm` | `s_passive_topology_mapped` | `gcm -noun p*` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `get-childitem` | `s_passive_topology_mapped` | `Get-ChildItem *.zip \| Sort-Object -Property` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `get-service` | `s_passive_topology_mapped` | `Get-Service \| Sort-Object -Property` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `where-object` | `s_passive_topology_mapped` | `Where-Object {!$_.processID -eq 0} \| Sort-Object -property name \| Format-Table \| Out-File $strFile}` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `get-command` | `s_passive_topology_mapped` | `Get-Command -Noun PSSessionConfiguration \| select Name` |

## Verified Executable Commands (Grouped by Capability Layer)

### General_System (17 commands)
```bash
Set-Item, Get-ChildItem, Remove-Item, etc. also work with the registry.
Get-Command, or Get-PSProvider. When cmdlets use the "Get" Verb pattern, they display
Get-Command
gcm Get-Command | Format-List *
gcm -verb u*
gcm -noun p*
Get-ChildItem *.zip | Sort-Object -Property
Format-Table LastWriteTime, CreationTime
Get-Service | Sort-Object -Property
Write-Host "Testing" $i "coming soon to a network near you ...";
Get-WmiObject -computername $i -class win32_process | Select-Object name, processID, Priority, ThreadCount, PageFaults,
Where-Object {!$_.processID -eq 0} | Sort-Object -property name | Format-Table | Out-File $strFile}
Get-Command -Noun PSSessionConfiguration | select Name
Script block logging records blocks of code as they are executed by the PowerShell engine, thereby
Script block logging will not record output from the executed code. Script block logging events are
Script block logging generates fewer events than module logging, and records valuable indicators
Script block logging, and
```

