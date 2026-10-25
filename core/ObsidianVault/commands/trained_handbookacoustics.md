---
title: "Trained Command Playbook: HandbookAcoustics.pdf"
tags:
  - enumeration
  - http
  - john
  - lateral_movement_routing_pivot
  - mdp
  - passive_enum
  - pdf
  - tls
  - trained
source_file: HandbookAcoustics.pdf
updated: 2026-10-25 00:58:34
---

# Trained Command Playbook: `HandbookAcoustics.pdf`

- **Source Document:** `~/Projects/CORA/Training/HandbookAcoustics.pdf`
- **CEGAR Verified Commands:** `10` (`0` malformed/unsafe snippets filtered)
- **MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`):** `10`
- **Discovered IPs/Subnets:** `None`
- **Discovered Interfaces:** `None`
- **Related Knowledge Note:** [[knowledge/trained_handbookacoustics]]

## Distilled MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`)
| Pre-State ($s$) | Tactic ($\tau$) | Technique ($k$) | Tool ($u$) | Post-State ($s'$) | Verified Command ($c$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `echo` | `s_active_services_enumerated` | `Echo level direct - dB` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `strings` | `s_passive_topology_mapped` | `strings and vibrate like a combination of solid rods and stretched strings. Thus piano` |
| `s_firewall_or_acl_unlocked` | **`Lateral_Movement_Routing_Pivot`** | Remote Host Execution, L2/L3 Route Injection & Subnet Pivot | `echo` | `s_cross_subnet_pivot_routed` | `Echo region` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `echo` | `s_active_services_enumerated` | `Echo delay - msec` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `fuser` | `s_passive_topology_mapped` | `fuser (QRD) is a construction that uses a series of wells of constant width, sepa-` |
| `s_firewall_or_acl_unlocked` | **`Lateral_Movement_Routing_Pivot`** | Remote Host Execution, L2/L3 Route Injection & Subnet Pivot | `echo` | `s_cross_subnet_pivot_routed` | `echo control in, 378–380` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `echo` | `s_active_services_enumerated` | `echo problem while at the same time conserving useful music and speech energy. Music` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `echo` | `s_active_services_enumerated` | `Echo region - dB` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `echo` | `s_active_services_enumerated` | `echo A delayed return of sound that is perceived by the ear as a discrete repetition.` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `echo` | `s_active_services_enumerated` | `echo and, 379` |

## Verified Executable Commands (Grouped by Capability Layer)

### General_System (10 commands)
```bash
Echo level direct - dB
Echo delay - msec
strings and vibrate like a combination of solid rods and stretched strings. Thus piano
Echo region
fuser (QRD) is a construction that uses a series of wells of constant width, sepa-
echo problem while at the same time conserving useful music and speech energy. Music
Echo region - dB
echo A delayed return of sound that is perceived by the ear as a discrete repetition.
echo control in, 378–380
echo and, 379
```

