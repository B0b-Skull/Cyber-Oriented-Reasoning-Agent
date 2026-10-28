---
title: "Trained Command Playbook: sample_perimeter_network_diagram.png"
tags:
  - eth0
  - https
  - image_diagram
  - lateral_movement_routing_pivot
  - mdp
  - out-of-band_access
  - serial
  - ssh
  - trained
  - ttyusb0
source_file: sample_perimeter_network_diagram.png
updated: 2026-10-24 01:00:22
---

# Trained Command Playbook: `sample_perimeter_network_diagram.png`

- **Source Document:** `~/Projects/CORA/Training/sample_perimeter_network_diagram.png`
- **CEGAR Verified Commands:** `2` (`0` malformed/unsafe snippets filtered)
- **MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`):** `2`
- **Discovered IPs/Subnets:** `10.20.30.0/24, 10.20.30.1, 10.20.30.1/24, 10.20.30.10/24, 172.24.10.1, 172.24.10.1/24, 172.24.10.50/24`
- **Discovered Interfaces:** `enp11s0, eth0, ttyUSB0`
- **Related Knowledge Note:** [[knowledge/trained_sample_perimeter_network_diagram]]

## Distilled MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`)
| Pre-State ($s$) | Tactic ($\tau$) | Technique ($k$) | Tool ($u$) | Post-State ($s'$) | Verified Command ($c$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `s_l2_l3_verified` | **`Out-of-Band_Access`** | UART/Serial Console Out-of-Band Enumeration & Control | `ip` | `s_oob_serial_enumerated` | `sudo ip addr replace 172.24.10.50/24 dev enp11s0` |
| `s_firewall_or_acl_unlocked` | **`Lateral_Movement_Routing_Pivot`** | Remote Host Execution, L2/L3 Route Injection & Subnet Pivot | `ip` | `s_cross_subnet_pivot_routed` | `sudo ip route replace 10.20.30.0/24 via 172.24.10.1 dev enp11s0 onlink` |

## Verified Executable Commands (Grouped by Capability Layer)

### General_System (2 commands)
```bash
sudo ip addr replace 172.24.10.50/24 dev enp11s0
sudo ip route replace 10.20.30.0/24 via 172.24.10.1 dev enp11s0 onlink
```

