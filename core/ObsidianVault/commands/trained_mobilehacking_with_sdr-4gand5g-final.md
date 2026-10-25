---
title: "Trained Command Playbook: MobileHacking_with_SDR-4Gand5G-final.pdf"
tags:
  - adb
  - cve-2012-6636
  - cve-2013-4710
  - enumeration
  - http
  - https
  - mdp
  - passive_enum
  - pdf
  - serial
  - tls
  - trained
  - ttyusb1
source_file: MobileHacking_with_SDR-4Gand5G-final.pdf
updated: 2026-10-25 00:59:21
---

# Trained Command Playbook: `MobileHacking_with_SDR-4Gand5G-final.pdf`

- **Source Document:** `~/Projects/CORA/Training/MobileHacking_with_SDR-4Gand5G-final.pdf`
- **CEGAR Verified Commands:** `3` (`0` malformed/unsafe snippets filtered)
- **MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`):** `3`
- **Discovered IPs/Subnets:** `127.0.1.1, 127.0.1.100, 127.0.1.200, 172.16.0.2`
- **Discovered Interfaces:** `ttyUSB1, ttyUSB2`
- **Related Knowledge Note:** [[knowledge/trained_mobilehacking_with_sdr-4gand5g-final]]

## Distilled MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`)
| Pre-State ($s$) | Tactic ($\tau$) | Technique ($k$) | Tool ($u$) | Post-State ($s'$) | Verified Command ($c$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `type` | `s_passive_topology_mapped` | `Type <t> to view trace` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `lte` | `s_active_services_enumerated` | `sudo lte softmodem O` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `nr` | `s_active_services_enumerated` | `sudo ./nr softmodem O` |

## Verified Executable Commands (Grouped by Capability Layer)

### General_System (3 commands)
```bash
Type <t> to view trace
sudo lte softmodem O
sudo ./nr softmodem O
```

