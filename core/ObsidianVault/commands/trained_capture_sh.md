---
title: "Trained Command Playbook: capture.sh.txt"
tags:
  - enumeration
  - eth1
  - mdp
  - tcpdump
  - text
  - trained
source_file: capture.sh.txt
updated: 2026-10-23 22:54:36
---

# Trained Command Playbook: `capture.sh.txt`

- **Source Document:** `~/Projects/CORA/Training/capture.sh.txt`
- **CEGAR Verified Commands:** `1` (`0` malformed/unsafe snippets filtered)
- **MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`):** `1`
- **Discovered IPs/Subnets:** `None`
- **Discovered Interfaces:** `eth1`
- **Related Knowledge Note:** [[knowledge/trained_capture_sh]]

## Distilled MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`)
| Pre-State ($s$) | Tactic ($\tau$) | Technique ($k$) | Tool ($u$) | Post-State ($s'$) | Verified Command ($c$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `script` | `s_active_services_enumerated` | `Script to capture traffic on eth1 interface` |

## Verified Executable Commands (Grouped by Capability Layer)

### General_System
```bash
Script to capture traffic on eth1 interface
```

