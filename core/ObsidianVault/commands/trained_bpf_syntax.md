---
title: "Trained Command Playbook: BPF syntax.pdf"
tags:
  - arp
  - enumeration
  - http
  - https
  - mdp
  - pdf
  - tcpdump
  - trained
  - vlan
source_file: BPF syntax.pdf
updated: 2026-10-25 22:54:36
---

# Trained Command Playbook: `BPF syntax.pdf`

- **Source Document:** `~/Projects/CORA/Training/BPF syntax.pdf`
- **CEGAR Verified Commands:** `1` (`0` malformed/unsafe snippets filtered)
- **MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`):** `1`
- **Discovered IPs/Subnets:** `172.24.1.0, 192.9.200.1, 255.0.0.0, 255.255.0.0, 255.255.255.0, 255.255.255.255`
- **Discovered Interfaces:** `None`
- **Related Knowledge Note:** [[knowledge/trained_bpf_syntax]]

## Distilled MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`)
| Pre-State ($s$) | Tactic ($\tau$) | Technique ($k$) | Tool ($u$) | Post-State ($s'$) | Verified Command ($c$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `service` | `s_active_services_enumerated` | `Service Access Point) fields of the LLC header;` |

## Verified Executable Commands (Grouped by Capability Layer)

### General_System
```bash
Service Access Point) fields of the LLC header;
```

