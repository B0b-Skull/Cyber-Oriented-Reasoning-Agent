---
title: "Trained Command Playbook: IPtables-Snort-CMDs.txt"
tags:
  - defense_evasion_firewall
  - eth0
  - eth1
  - iptables
  - mdp
  - nmap
  - snort
  - ssh
  - tcpdump
  - text
  - trained
source_file: IPtables-Snort-CMDs.txt
updated: 2026-10-25 00:58:43
---

# Trained Command Playbook: `IPtables-Snort-CMDs.txt`

- **Source Document:** `~/Projects/CORA/Training/IPtables-Snort-CMDs.txt`
- **CEGAR Verified Commands:** `42` (`0` malformed/unsafe snippets filtered)
- **MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`):** `42`
- **Discovered IPs/Subnets:** `10.18.80.64/26, 172.24.0.0/24, 172.24.1.0/24, 172.24.11.0/24, 172.24.11.13, 172.24.11.15, 172.24.11.254, 192.18.31.253, 198.18.31.253`
- **Discovered Interfaces:** `eth0, eth1, lo`
- **Related Knowledge Note:** [[knowledge/trained_iptables-snort-cmds]]

## Distilled MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`)
| Pre-State ($s$) | Tactic ($\tau$) | Technique ($k$) | Tool ($u$) | Post-State ($s'$) | Verified Command ($c$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `iptables` | `s_firewall_or_acl_unlocked` | `IPTables & Snort` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `nmap` | `s_firewall_or_acl_unlocked` | `nmap -n -Pn -sS -p 21,22,23,25,80,110,111,443 198.18.31.253` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `tcpdump` | `s_firewall_or_acl_unlocked` | `tcpdump -vv src 192.18.31.253 and dst 172.24.11.15` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `nmap` | `s_firewall_or_acl_unlocked` | `nmap -n -Pn -sU -p 53,67,123,135,137,138,161,445,631,1434 198.18.31.253` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `iptables` | `s_firewall_or_acl_unlocked` | `iptables -A INPUT -p udp -j REJECT --reject-with icmp-net-prohibited` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `iptables` | `s_firewall_or_acl_unlocked` | `iptables -A INPUT -p tcp -j REJECT --reject-with tcp-reset` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `iptables` | `s_firewall_or_acl_unlocked` | `iptables -A INPUT -p icmp -j DROP` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `iptables` | `s_firewall_or_acl_unlocked` | `iptables -A INPUT -d 172.24.11.13 \! -i eth0 -j DROP` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `iptables` | `s_firewall_or_acl_unlocked` | `iptables -A INPUT -p tcp -m state --state ESTABLISHED, RELATED -j ACCEPT` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `iptables` | `s_firewall_or_acl_unlocked` | `iptables -P INPUT DROP` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `iptables` | `s_firewall_or_acl_unlocked` | `iptables -t filter -F` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `iptables` | `s_firewall_or_acl_unlocked` | `iptables -t nat -F` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `iptables` | `s_firewall_or_acl_unlocked` | `iptables -X` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `iptables` | `s_firewall_or_acl_unlocked` | `iptables -P INPUT ACCEPT` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `iptables` | `s_firewall_or_acl_unlocked` | `iptables -P OUTPUT ACCEPT` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `iptables` | `s_firewall_or_acl_unlocked` | `iptables -P FORWARD ACCEPT` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `iptables` | `s_firewall_or_acl_unlocked` | `iptables -t filter -A FORWARD -s 172.24.0.0/24 -d 172.24.1.0/24 -i eth0 -o eth1 -j ACCEPT` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `iptables` | `s_firewall_or_acl_unlocked` | `iptables -A INPUT -i lo -j ACCEPT` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `iptables` | `s_firewall_or_acl_unlocked` | `iptables -A OUTPUT -o lo -j ACCEPT` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `iptables` | `s_firewall_or_acl_unlocked` | `iptables -t filter -A INPUT -p tcp --dport 22 -s 10.18.80.64/26 -j ACCEPT` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `iptables` | `s_firewall_or_acl_unlocked` | `iptables -t filter -A OUTPUT -p tcp --sport 22 -d 10.18.80.64/26 -j ACCEPT` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `iptables` | `s_firewall_or_acl_unlocked` | `iptables -t filter -A INPUT -p tcp --dport 22 -s 10.18.80.64/26 -m state --state NEW,ESTABLISHED,RELATED -j ACCEPT` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `iptables` | `s_firewall_or_acl_unlocked` | `iptables -t filter -A OUTPUT -p tcp --sport 22 -d 10.18.80.64/26 -m state --state ESTABLISHED,RELATED -j ACCEPT` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `iptables` | `s_firewall_or_acl_unlocked` | `sudo iptables -A INPUT -s 172.24.11.13 -p tcp --dport 22 -j ACCEPT` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `iptables` | `s_firewall_or_acl_unlocked` | `sudo iptables -A OUTPUT -d 172.24.11.13 -p tcp --sport 22 -j ACCEPT` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `iptables` | `s_firewall_or_acl_unlocked` | `sudo iptables -A INPUT -i lo -j ACCEPT` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `iptables` | `s_firewall_or_acl_unlocked` | `sudo iptables -A OUTPUT -o lo -j ACCEPT` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `iptables` | `s_firewall_or_acl_unlocked` | `iptables -I INPUT 1 -s 172.24.11.13 -p tcp --dport 22 -m state --state NEW,RELATED,ESTABLISHED -j ACCEPT` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `iptables` | `s_firewall_or_acl_unlocked` | `iptables -I OUTPUT 1 -d 172.24.11.13 -p tcp --sport 22 -m state --state RELATED,ESTABLISHED -j ACCEPT` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `ssh` | `s_firewall_or_acl_unlocked` | `ssh haxor@172.24.11.254` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `iptables` | `s_firewall_or_acl_unlocked` | `sudo iptables -I FORWARD 1 -s win7.ops.local -d ad.ops.local -p tcp --dport 23 -m state --state NEW,RELATED,ESTABLISHED -j ACCEPT` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `iptables` | `s_firewall_or_acl_unlocked` | `sudo iptables -I FORWARD 2 -s ad.ops.local -d win7.ops.local -p tcp --sport 23 -m state --state RELATED,ESTABLISHED -j ACCEPT` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `iptables` | `s_firewall_or_acl_unlocked` | `sudo iptables -I FORWARD 3 -s 172.24.11.0/24 -d ad.ops.local -p tcp --dport 23 -j REJECT --reject-with tcp-reset` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `iptables` | `s_firewall_or_acl_unlocked` | `sudo iptables -I FORWARD 4 -s linux.ops.local -d ad.ops.local -p udp --dport 53 -j ACCEPT` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `iptables` | `s_firewall_or_acl_unlocked` | `sudo iptables -I FORWARD 5 -s ad.ops.local -d linux.ops.local -p udp --sport 53 -j ACCEPT` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `iptables` | `s_firewall_or_acl_unlocked` | `sudo iptables -I FORWARD 6 -s linux.ops.local -d ad.ops.local -j DROP` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `iptables` | `s_firewall_or_acl_unlocked` | `sudo iptables -I FORWARD 7 -d www.ops.local -p tcp --dport 80 -m state --state NEW,RELATED,ESTABLISHED -j ACCEPT` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `iptables` | `s_firewall_or_acl_unlocked` | `sudo iptables -I FORWARD 8 -s www.ops.local -p tcp --sport 80 -m state --state RELATED,ESTABLISHED -j ACCEPT` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `iptables` | `s_firewall_or_acl_unlocked` | `sudo iptables -I FORWARD 9 -d www.ops.local -j REJECT --reject-with icmp-host-unreachable` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `iptables` | `s_firewall_or_acl_unlocked` | `sudo iptables -I FORWARD 10 -s www.ops.local -j LOG` |

## Verified Executable Commands (Grouped by Capability Layer)

### General_System (16 commands)
```bash
sudo iptables -A INPUT -s 172.24.11.13 -p tcp --dport 22 -j ACCEPT
sudo iptables -A OUTPUT -d 172.24.11.13 -p tcp --sport 22 -j ACCEPT
sudo iptables -A INPUT -i lo -j ACCEPT
sudo iptables -A OUTPUT -o lo -j ACCEPT
sudo iptables -I FORWARD 1 -s win7.ops.local -d ad.ops.local -p tcp --dport 23 -m state --state NEW,RELATED,ESTABLISHED -j ACCEPT
sudo iptables -I FORWARD 2 -s ad.ops.local -d win7.ops.local -p tcp --sport 23 -m state --state RELATED,ESTABLISHED -j ACCEPT
sudo iptables -I FORWARD 3 -s 172.24.11.0/24 -d ad.ops.local -p tcp --dport 23 -j REJECT --reject-with tcp-reset
sudo iptables -I FORWARD 4 -s linux.ops.local -d ad.ops.local -p udp --dport 53 -j ACCEPT
sudo iptables -I FORWARD 5 -s ad.ops.local -d linux.ops.local -p udp --sport 53 -j ACCEPT
sudo iptables -I FORWARD 6 -s linux.ops.local -d ad.ops.local -j DROP
sudo iptables -I FORWARD 7 -d www.ops.local -p tcp --dport 80 -m state --state NEW,RELATED,ESTABLISHED -j ACCEPT
sudo iptables -I FORWARD 8 -s www.ops.local -p tcp --sport 80 -m state --state RELATED,ESTABLISHED -j ACCEPT
sudo iptables -I FORWARD 9 -d www.ops.local -j REJECT --reject-with icmp-host-unreachable
sudo iptables -I FORWARD 10 -s www.ops.local -j LOG
sudo iptables -I FORWARD 11 -s www.ops.local -j DROP
sudo service iptables save
```

### L3_Routing_NAT (22 commands)
```bash
IPTables & Snort
iptables -A INPUT -p udp -j REJECT --reject-with icmp-net-prohibited
iptables -A INPUT -p tcp -j REJECT --reject-with tcp-reset
iptables -A INPUT -p icmp -j DROP
iptables -A INPUT -d 172.24.11.13 \! -i eth0 -j DROP
iptables -A INPUT -p tcp -m state --state ESTABLISHED, RELATED -j ACCEPT
iptables -P INPUT DROP
iptables -t filter -F
iptables -t nat -F
iptables -X
iptables -P INPUT ACCEPT
iptables -P OUTPUT ACCEPT
iptables -P FORWARD ACCEPT
iptables -t filter -A FORWARD -s 172.24.0.0/24 -d 172.24.1.0/24 -i eth0 -o eth1 -j ACCEPT
iptables -A INPUT -i lo -j ACCEPT
iptables -A OUTPUT -o lo -j ACCEPT
iptables -t filter -A INPUT -p tcp --dport 22 -s 10.18.80.64/26 -j ACCEPT
iptables -t filter -A OUTPUT -p tcp --sport 22 -d 10.18.80.64/26 -j ACCEPT
iptables -t filter -A INPUT -p tcp --dport 22 -s 10.18.80.64/26 -m state --state NEW,ESTABLISHED,RELATED -j ACCEPT
iptables -t filter -A OUTPUT -p tcp --sport 22 -d 10.18.80.64/26 -m state --state ESTABLISHED,RELATED -j ACCEPT
iptables -I INPUT 1 -s 172.24.11.13 -p tcp --dport 22 -m state --state NEW,RELATED,ESTABLISHED -j ACCEPT
iptables -I OUTPUT 1 -d 172.24.11.13 -p tcp --sport 22 -m state --state RELATED,ESTABLISHED -j ACCEPT
```

### L4_Port_Service (4 commands)
```bash
nmap -n -Pn -sS -p 21,22,23,25,80,110,111,443 198.18.31.253
tcpdump -vv src 192.18.31.253 and dst 172.24.11.15
nmap -n -Pn -sU -p 53,67,123,135,137,138,161,445,631,1434 198.18.31.253
ssh haxor@172.24.11.254
```

