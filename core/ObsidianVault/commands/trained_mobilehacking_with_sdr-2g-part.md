---
title: "Trained Command Playbook: MobileHacking_with_SDR-2G-part.pdf"
tags:
  - cve-2012-6636
  - cve-2013-4710
  - docker
  - enumeration
  - https
  - mdp
  - pdf
  - trained
  - wireshark
source_file: MobileHacking_with_SDR-2G-part.pdf
updated: 2026-10-24 00:59:14
---

# Trained Command Playbook: `MobileHacking_with_SDR-2G-part.pdf`

- **Source Document:** `~/Projects/CORA/Training/MobileHacking_with_SDR-2G-part.pdf`
- **CEGAR Verified Commands:** `1` (`0` malformed/unsafe snippets filtered)
- **MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`):** `1`
- **Discovered IPs/Subnets:** `None`
- **Discovered Interfaces:** `None`
- **Related Knowledge Note:** [[knowledge/trained_mobilehacking_with_sdr-2g-part]]

## Distilled MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`)
| Pre-State ($s$) | Tactic ($\tau$) | Technique ($k$) | Tool ($u$) | Post-State ($s'$) | Verified Command ($c$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `python` | `s_active_services_enumerated` | `sudo python modmobmap.py` |

## Verified Executable Commands (Grouped by Capability Layer)

### General_System (1 commands)
```bash
sudo python modmobmap.py
```

