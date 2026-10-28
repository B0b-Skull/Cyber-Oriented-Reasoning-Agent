---
title: "Trained Command Playbook: Solaris-Network-Enum-Script.txt"
tags:
  - active_enum
  - enumeration
  - mdp
  - passive_enum
  - text
  - trained
source_file: Solaris-Network-Enum-Script.txt
updated: 2026-10-24 01:00:32
---

# Trained Command Playbook: `Solaris-Network-Enum-Script.txt`

- **Source Document:** `~/Projects/CORA/Training/Solaris-Network-Enum-Script.txt`
- **CEGAR Verified Commands:** `4` (`0` malformed/unsafe snippets filtered)
- **MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`):** `4`
- **Discovered IPs/Subnets:** `None`
- **Discovered Interfaces:** `None`
- **Related Knowledge Note:** [[knowledge/trained_solaris-network-enum-script]]

## Distilled MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`)
| Pre-State ($s$) | Tactic ($\tau$) | Technique ($k$) | Tool ($u$) | Post-State ($s'$) | Verified Command ($c$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `echo` | `s_active_services_enumerated` | `echo "Please provide a port number parameter for this script"` |
| `s_passive_topology_mapped` | **`Active_Enum`** | Active Network, Cloud, Directory Service & Endpoint Probing | `echo` | `s_active_services_enumerated` | `echo "Greping for your port, please be patient (CTRL+C breaks) ... "` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `pfiles` | `s_passive_topology_mapped` | `pfiles $i \| grep AF_INET \| grep $1` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `echo` | `s_active_services_enumerated` | `echo "e.g. $0 22"` |

## Verified Executable Commands (Grouped by Capability Layer)

### General_System (4 commands)
```bash
echo "Please provide a port number parameter for this script"
echo "e.g. $0 22"
echo "Greping for your port, please be patient (CTRL+C breaks) ... "
pfiles $i | grep AF_INET | grep $1
```

