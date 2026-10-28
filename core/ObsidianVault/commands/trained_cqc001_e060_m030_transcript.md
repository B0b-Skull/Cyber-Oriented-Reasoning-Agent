---
title: "Trained Command Playbook: CQC001_E060_M030_transcript.pdf"
tags:
  - defense_evasion_firewall
  - eth0
  - eth1
  - http
  - iptables
  - mdp
  - pdf
  - snort
  - ssh
  - trained
source_file: CQC001_E060_M030_transcript.pdf
updated: 2026-10-24 00:58:03
---

# Trained Command Playbook: `CQC001_E060_M030_transcript.pdf`

- **Source Document:** `~/Projects/CORA/Training/CQC001_E060_M030_transcript.pdf`
- **CEGAR Verified Commands:** `18` (`0` malformed/unsafe snippets filtered)
- **MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`):** `18`
- **Discovered IPs/Subnets:** `10.18.80.64/26, 172.24.0.0/24, 172.24.1.0/24, 172.24.11.13`
- **Discovered Interfaces:** `eth0, eth1, lo`
- **Related Knowledge Note:** [[knowledge/trained_cqc001_e060_m030_transcript]]

## Distilled MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`)
| Pre-State ($s$) | Tactic ($\tau$) | Technique ($k$) | Tool ($u$) | Post-State ($s'$) | Verified Command ($c$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `iptables` | `s_firewall_or_acl_unlocked` | `IPTables and Snort: Section 1 Transcript` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `snort` | `s_firewall_or_acl_unlocked` | `Snort configuration.` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `iptables` | `s_firewall_or_acl_unlocked` | `IPTables and Snort: Section 2 Transcript` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `ip` | `s_firewall_or_acl_unlocked` | `IP address is assigned to the iptables host, then the packet will be analyzed against the rules in the` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `iptables` | `s_firewall_or_acl_unlocked` | `IPTables and Snort: Section 3 Transcript` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `iptables` | `s_firewall_or_acl_unlocked` | `iptables -A INPUT -d 172.24.11.13 \! -i eth0 -j DROP` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `ip` | `s_firewall_or_acl_unlocked` | `IP address 172.24.11.13. The second \! -i eth0 requires that the packet be incoming on an` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `ip` | `s_firewall_or_acl_unlocked` | `IP address 172.24.11.13 that arrive on an interface other than eth0. Though we have not yet` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `iptables` | `s_firewall_or_acl_unlocked` | `iptables -t filter -F (Flush all rules from the filter table)` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `iptables` | `s_firewall_or_acl_unlocked` | `iptables -t nat -F (Flush all rules from the NAT table)` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `iptables` | `s_firewall_or_acl_unlocked` | `iptables -X (Remove all user-defined chains from the filter table)` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `iptables` | `s_firewall_or_acl_unlocked` | `iptables -P INPUT ACCEPT (Set the default policy on the INPUT chain of the filter table)` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `iptables` | `s_firewall_or_acl_unlocked` | `iptables -P OUTPUT ACCEPT (Set the default policy on the OUTPUT chain of the filter table)` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `iptables` | `s_firewall_or_acl_unlocked` | `iptables -A INPUT -i lo -j ACCEPT` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `iptables` | `s_firewall_or_acl_unlocked` | `iptables -A OUTPUT -o lo -j ACCEPT` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `iptables` | `s_firewall_or_acl_unlocked` | `IPTables and Snort: Section 4 Transcript` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `snort` | `s_firewall_or_acl_unlocked` | `Snort Rules` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `iptables` | `s_firewall_or_acl_unlocked` | `IPTables and Snort: Section 5 Transcript` |

## Verified Executable Commands (Grouped by Capability Layer)

### L3_Routing_NAT (16 commands)
```bash
IPTables and Snort: Section 1 Transcript
IPTables and Snort: Section 2 Transcript
IP address is assigned to the iptables host, then the packet will be analyzed against the rules in the
IPTables and Snort: Section 3 Transcript
iptables -A INPUT -d 172.24.11.13 \! -i eth0 -j DROP
IP address 172.24.11.13. The second \! -i eth0 requires that the packet be incoming on an
IP address 172.24.11.13 that arrive on an interface other than eth0. Though we have not yet
iptables -t filter -F (Flush all rules from the filter table)
iptables -t nat -F (Flush all rules from the NAT table)
iptables -X (Remove all user-defined chains from the filter table)
iptables -P INPUT ACCEPT (Set the default policy on the INPUT chain of the filter table)
iptables -P OUTPUT ACCEPT (Set the default policy on the OUTPUT chain of the filter table)
iptables -A INPUT -i lo -j ACCEPT
iptables -A OUTPUT -o lo -j ACCEPT
IPTables and Snort: Section 4 Transcript
IPTables and Snort: Section 5 Transcript
```

### L4_Port_Service (2 commands)
```bash
Snort configuration.
Snort Rules
```

