---
title: "Trained Command Playbook: CQC001_E010_M050_DHCP_Fingerprints.txt"
tags:
  - enumeration
  - http
  - mdp
  - text
  - trained
  - z3
source_file: CQC001_E010_M050_DHCP_Fingerprints.txt
updated: 2026-10-25 00:57:27
---

# Trained Command Playbook: `CQC001_E010_M050_DHCP_Fingerprints.txt`

- **Source Document:** `~/Projects/CORA/Training/CQC001_E010_M050_DHCP_Fingerprints.txt`
- **CEGAR Verified Commands:** `4` (`0` malformed/unsafe snippets filtered)
- **MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`):** `4`
- **Discovered IPs/Subnets:** `1.5.0.0, 1.6.0.3, 1.8.5.3, 10.0.10.648, 10.0.10.672, 10.0.10.684, 10.0.10.690, 10.0.10.738, 10.3.0.700, 10.3.1.226, 10.3.1.821, 10.3.2.281, 10.3.2.500, 10.3.2.680, 10.3.2.798, 10.3.2.858, 10.3.2.876, 2.0.14.1, 2.6.5.5, 2.7.0.1, 3.2.1.70, 3.6.2.5, 3.6.3.12, 3.7.1.0, 3.7.1.28, 3.8.2.99, 3.9.0.834, 4.1.0.29, 4.1.4.1, 4.1.7.252, 4.2.7.498, 4.4.2.1, 4.5.3.1, 4.5.4.2, 4.5.9.461, 4.6.0.126, 4.6.0.216, 4.6.1.250, 4.6.1.310, 4.6.1.314, 5.0.0.344, 5.0.0.351, 5.0.0.497, 5.0.0.509, 5.0.0.592, 5.0.0.593, 5.0.0.604, 5.0.0.654, 5.0.0.656, 5.0.0.681, 5.0.0.743, 5.0.0.794, 5.0.0.832, 5.0.0.845, 5.0.0.846, 5.0.0.862, 5.0.0.900, 5.0.0.955, 5.0.0.975, 5.1.2.9, 5.1.3.19, 5.1.4.020, 5.1.5.002, 5.5.2.2, 5.5.3.1, 5.5.6.1, 6.0.0.141, 6.0.0.246, 6.0.0.285, 6.0.0.294, 6.0.0.337, 6.0.0.431, 6.0.0.436, 6.0.0.448, 6.0.0.461, 6.0.0.480, 6.0.0.481, 6.0.0.526, 6.0.0.534, 6.0.0.546, 6.0.0.570, 6.0.0.576, 6.0.0.600, 6.0.0.615, 6.0.0.666, 6.0.0.668, 6.0.0.706, 6.0.0.719, 6.0.0.723, 6.0.0.747, 6.5.3.5, 6.6.0.19, 6.6.0.42, 6.7.0.34, 6.7.2.2, 6.7.3.2, 6.8.0.23, 6.8.1.26, 6.9.0.28, 6.9.1.1, 7.0.0.254, 7.0.0.261, 7.0.0.296, 7.0.0.317, 7.0.0.319, 7.0.0.353, 7.0.0.374, 7.0.0.482, 7.0.0.513, 7.0.0.528, 7.0.0.530, 7.0.0.540, 7.0.0.557, 7.0.0.576, 7.0.0.579, 7.0.0.585, 7.0.0.586, 7.0.0.590, 7.0.0.598, 7.0.0.611, 7.1.0.163, 7.1.0.219, 7.1.0.267, 7.1.0.284, 7.1.0.336, 7.1.0.342, 7.1.0.391, 7.1.0.398, 7.1.0.477, 7.1.0.523, 7.1.0.569, 7.1.0.580, 7.1.0.634, 7.1.0.658, 7.1.0.694, 7.1.0.714, 7.1.0.746, 7.1.0.755, 7.1.0.768, 7.1.0.794, 7.1.0.821, 7.1.0.862, 7.1.0.865, 7.1.0.907, 7.1.0.912, 7.4.1.42`
- **Discovered Interfaces:** `None`
- **Related Knowledge Note:** [[knowledge/trained_cqc001_e010_m050_dhcp_fingerprints]]

## Distilled MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`)
| Pre-State ($s$) | Tactic ($\tau$) | Technique ($k$) | Tool ($u$) | Post-State ($s'$) | Verified Command ($c$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `echo` | `s_active_services_enumerated` | `Echo                                                         1` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `gem` | `s_active_services_enumerated` | `Gem 2.1                                                      1,3,6,28,33,51,58,59,121` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `cat` | `s_active_services_enumerated` | `CAT B15 4.1.2                                                1,33,3,6,15,28,51,58,59` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `find` | `s_active_services_enumerated` | `Find 5 4.1.1                                                 1,33,3,6,15,28,51,58,59` |

## Verified Executable Commands (Grouped by Capability Layer)

### General_System (4 commands)
```bash
Echo                                                         1
Gem 2.1                                                      1,3,6,28,33,51,58,59,121
CAT B15 4.1.2                                                1,33,3,6,15,28,51,58,59
Find 5 4.1.1                                                 1,33,3,6,15,28,51,58,59
```

