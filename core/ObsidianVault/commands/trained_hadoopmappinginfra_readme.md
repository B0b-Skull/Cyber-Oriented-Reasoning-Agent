---
title: "Trained Command Playbook: HadoopMappingInfra_ReadMe.md"
tags:
  - active_enum
  - http
  - https
  - mdp
  - nmap
  - text
  - trained
source_file: HadoopMappingInfra_ReadMe.md
updated: 2026-10-24 00:58:24
---

# Trained Command Playbook: `HadoopMappingInfra_ReadMe.md`

- **Source Document:** `~/Projects/CORA/Training/HadoopMappingInfra_ReadMe.md`
- **CEGAR Verified Commands:** `1` (`0` malformed/unsafe snippets filtered)
- **MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`):** `1`
- **Discovered IPs/Subnets:** `172.24.11.150, 2.7.1.2`
- **Discovered Interfaces:** `None`
- **Related Knowledge Note:** [[knowledge/trained_hadoopmappinginfra_readme]]

## Distilled MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`)
| Pre-State ($s$) | Tactic ($\tau$) | Technique ($k$) | Tool ($u$) | Post-State ($s'$) | Verified Command ($c$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `s_passive_topology_mapped` | **`Active_Enum`** | Active Network, Cloud, Directory Service & Endpoint Probing | `nmap` | `s_active_services_enumerated` | `nmap -sV --script=http-enum -p- 172.24.11.150` |

## Verified Executable Commands (Grouped by Capability Layer)

### L4_Port_Service (1 commands)
```bash
nmap -sV --script=http-enum -p- 172.24.11.150
```

