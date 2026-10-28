---
title: "Trained Command Playbook: recognizing-suspicious-network-connections-python_12515.pdf"
tags:
  - arp
  - defense_evasion_firewall
  - enumeration
  - http
  - https
  - ipconfig
  - mdp
  - netsh
  - netstat
  - pdf
  - powershell
  - ssh
  - trained
source_file: recognizing-suspicious-network-connections-python_12515.pdf
updated: 2026-10-24 01:00:17
---

# Trained Command Playbook: `recognizing-suspicious-network-connections-python_12515.pdf`

- **Source Document:** `~/Projects/CORA/Training/recognizing-suspicious-network-connections-python_12515.pdf`
- **CEGAR Verified Commands:** `3` (`0` malformed/unsafe snippets filtered)
- **MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`):** `3`
- **Discovered IPs/Subnets:** `None`
- **Discovered Interfaces:** `None`
- **Related Knowledge Note:** [[knowledge/trained_recognizing-suspicious-network-connections-python_12515]]

## Distilled MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`)
| Pre-State ($s$) | Tactic ($\tau$) | Technique ($k$) | Tool ($u$) | Post-State ($s'$) | Verified Command ($c$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `netsh` | `s_firewall_or_acl_unlocked` | `netsh advfirewall firewall add rule name="IP Block" dir=in` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `get-content` | `s_active_services_enumerated` | `Get-Content suspicious.txt \| foreach-object` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `script` | `s_firewall_or_acl_unlocked` | `script a few seconds to create a pcap and 'suspicious.txt'` |

## Verified Executable Commands (Grouped by Capability Layer)

### General_System (2 commands)
```bash
Get-Content suspicious.txt | foreach-object
script a few seconds to create a pcap and 'suspicious.txt'
```

### L3_Routing_NAT (1 commands)
```bash
netsh advfirewall firewall add rule name="IP Block" dir=in
```

