---
title: "Trained Command Playbook: CQC001_E040_M005_PowerShell_Comparison.pdf"
tags:
  - curl
  - enumeration
  - mdp
  - passive_enum
  - pdf
  - powershell
  - reconnaissance
  - trained
source_file: CQC001_E040_M005_PowerShell_Comparison.pdf
updated: 2026-10-24 00:57:41
---

# Trained Command Playbook: `CQC001_E040_M005_PowerShell_Comparison.pdf`

- **Source Document:** `~/Projects/CORA/Training/CQC001_E040_M005_PowerShell_Comparison.pdf`
- **CEGAR Verified Commands:** `21` (`0` malformed/unsafe snippets filtered)
- **MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`):** `21`
- **Discovered IPs/Subnets:** `None`
- **Discovered Interfaces:** `None`
- **Related Knowledge Note:** [[knowledge/trained_cqc001_e040_m005_powershell_comparison]]

## Distilled MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`)
| Pre-State ($s$) | Tactic ($\tau$) | Technique ($k$) | Tool ($u$) | Post-State ($s'$) | Verified Command ($c$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `get-` | `s_active_services_enumerated` | `Get-` |
| `s_init_unknown` | **`Reconnaissance`** | Domain, DNS, OSINT & Target Footprint Reconnaissance | `get-content` | `s_passive_topology_mapped` | `Get-Content` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `get-help` | `s_passive_topology_mapped` | `Get-Help` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `test-` | `s_active_services_enumerated` | `Test-` |
| `s_init_unknown` | **`Reconnaissance`** | Domain, DNS, OSINT & Target Footprint Reconnaissance | `clear-host` | `s_passive_topology_mapped` | `Clear-Host` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `get-process` | `s_passive_topology_mapped` | `Get-Process` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `rename-` | `s_active_services_enumerated` | `Rename-` |
| `s_init_unknown` | **`Reconnaissance`** | Domain, DNS, OSINT & Target Footprint Reconnaissance | `copy-item` | `s_passive_topology_mapped` | `Copy-Item` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `rename` | `s_active_services_enumerated` | `Rename a file/a directory` |
| `s_init_unknown` | **`Reconnaissance`** | Domain, DNS, OSINT & Target Footprint Reconnaissance | `copy` | `s_passive_topology_mapped` | `Copy one or several files/a whole directory` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `get-location` | `s_active_services_enumerated` | `Get-Location` |
| `s_init_unknown` | **`Reconnaissance`** | Domain, DNS, OSINT & Target Footprint Reconnaissance | `move-item` | `s_passive_topology_mapped` | `Move-Item` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `set-location` | `s_active_services_enumerated` | `Set-Location` |
| `s_init_unknown` | **`Reconnaissance`** | Domain, DNS, OSINT & Target Footprint Reconnaissance | `remove-` | `s_passive_topology_mapped` | `Remove-` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `tee-object` | `s_active_services_enumerated` | `Tee-Object` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `write-` | `s_active_services_enumerated` | `Write-` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `stop-process` | `s_active_services_enumerated` | `Stop-Process` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `select-string` | `s_active_services_enumerated` | `Select-String` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `set-variable` | `s_active_services_enumerated` | `Set-Variable` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `invoke-` | `s_active_services_enumerated` | `Invoke-` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `popd` | `s_active_services_enumerated` | `popd implemented` |

## Verified Executable Commands (Grouped by Capability Layer)

### General_System (21 commands)
```bash
Get-
Test-
Get-Content
Get-Help
Clear-Host
Copy-Item
Copy one or several files/a whole directory
Move-Item
Remove-
Rename-
Rename a file/a directory
Get-Location
Set-Location
Tee-Object
Write-
Get-Process
Stop-Process
Select-String
Set-Variable
Invoke-
popd implemented
```

