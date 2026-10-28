---
title: "Trained Command Playbook: BCF_CNE Basics.pdf"
tags:
  - defense_evasion_firewall
  - ipconfig
  - mdp
  - netsh
  - netstat
  - nmap
  - out-of-band_access
  - pdf
  - powershell
  - trained
source_file: BCF_CNE Basics.pdf
updated: 2026-10-24 00:56:31
---

# Trained Command Playbook: `BCF_CNE Basics.pdf`

- **Source Document:** `~/Projects/CORA/Training/BCF_CNE Basics.pdf`
- **CEGAR Verified Commands:** `6` (`0` malformed/unsafe snippets filtered)
- **MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`):** `6`
- **Discovered IPs/Subnets:** `172.24.12.4, 172.24.12.9`
- **Discovered Interfaces:** `None`
- **Related Knowledge Note:** [[knowledge/trained_bcf_cne_basics]]

## Distilled MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`)
| Pre-State ($s$) | Tactic ($\tau$) | Technique ($k$) | Tool ($u$) | Post-State ($s'$) | Verified Command ($c$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `ipconfig` | `s_firewall_or_acl_unlocked` | `ipconfig` |
| `s_l2_l3_verified` | **`Out-of-Band_Access`** | UART/Serial Console Out-of-Band Enumeration & Control | `netstat` | `s_oob_serial_enumerated` | `netstat -anob` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `tasklist` | `s_firewall_or_acl_unlocked` | `tasklist` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `systeminfo` | `s_firewall_or_acl_unlocked` | `systeminfo` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `netsh` | `s_firewall_or_acl_unlocked` | `netsh advfirewall show currentprofile` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `netsh` | `s_firewall_or_acl_unlocked` | `netsh advfirewall firewall add rule name="Zoo TCP Port 80" dir=in action=allow protocol=TCP localport=80` |

## Verified Executable Commands (Grouped by Capability Layer)

### General_System (2 commands)
```bash
tasklist
systeminfo
```

### L3_Routing_NAT (3 commands)
```bash
ipconfig
netsh advfirewall show currentprofile
netsh advfirewall firewall add rule name="Zoo TCP Port 80" dir=in action=allow protocol=TCP localport=80
```

### L4_Port_Service (1 commands)
```bash
netstat -anob
```

