---
title: "Trained Command Playbook: WMIC QuickStart.txt"
tags:
  - defense_evasion_firewall
  - mdp
  - passive_enum
  - text
  - trained
  - wmic
source_file: WMIC QuickStart.txt
updated: 2026-10-25 01:01:12
---

# Trained Command Playbook: `WMIC QuickStart.txt`

- **Source Document:** `~/Projects/CORA/Training/WMIC QuickStart.txt`
- **CEGAR Verified Commands:** `12` (`0` malformed/unsafe snippets filtered)
- **MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`):** `12`
- **Discovered IPs/Subnets:** `None`
- **Discovered Interfaces:** `None`
- **Related Knowledge Note:** [[knowledge/trained_wmic_quickstart]]

## Distilled MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`)
| Pre-State ($s$) | Tactic ($\tau$) | Technique ($k$) | Tool ($u$) | Post-State ($s'$) | Verified Command ($c$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `wmic` | `s_passive_topology_mapped` | `wmic - windows management interface` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `rundll32` | `s_firewall_or_acl_unlocked` | `rundll32.exe         "C:\WINDOWS\system32\RUNDLL32.EXE" \` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `wmic` | `s_passive_topology_mapped` | `wmic process get workingsetsize,commandline /format:csv` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `wmic` | `s_passive_topology_mapped` | `wmic process \| sort` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `wmic` | `s_passive_topology_mapped` | `wmic.exe             wmic process` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `wmic` | `s_passive_topology_mapped` | `wmic diskdrive get name,size,model` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `wmic` | `s_passive_topology_mapped` | `wmic partition get name,size,type` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `wmic` | `s_passive_topology_mapped` | `wmic bios get name,serialnumber,version` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `wmic` | `s_passive_topology_mapped` | `wmic csproduct get name,vendor,identifyingNumber` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `wmic` | `s_passive_topology_mapped` | `wmic qfe get description,installedOn /format:csv` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `wmic` | `s_passive_topology_mapped` | `wmic COMPUTERSYSTEM get TotalPhysicalMemory,caption` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `wmic` | `s_passive_topology_mapped` | `wmic nic get macaddress,description` |

## Verified Executable Commands (Grouped by Capability Layer)

### General_System (12 commands)
```bash
wmic - windows management interface
wmic process get workingsetsize,commandline /format:csv
wmic process | sort
rundll32.exe         "C:\WINDOWS\system32\RUNDLL32.EXE" \
wmic.exe             wmic process
wmic diskdrive get name,size,model
wmic partition get name,size,type
wmic bios get name,serialnumber,version
wmic csproduct get name,vendor,identifyingNumber
wmic qfe get description,installedOn /format:csv
wmic COMPUTERSYSTEM get TotalPhysicalMemory,caption
wmic nic get macaddress,description
```

