---
title: "Trained Command Playbook: sample_perimeter_router_playbook.md"
tags:
  - arp
  - curl
  - https
  - iptables
  - lateral_movement_routing_pivot
  - mdp
  - nmap
  - out-of-band_access
  - serial
  - text
  - tio
  - trained
  - ttyusb0
source_file: sample_perimeter_router_playbook.md
updated: 2026-10-24 01:00:23
---

# Trained Command Playbook: `sample_perimeter_router_playbook.md`

- **Source Document:** `~/Projects/CORA/Training/sample_perimeter_router_playbook.md`
- **CEGAR Verified Commands:** `12` (`0` malformed/unsafe snippets filtered)
- **MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`):** `12`
- **Discovered IPs/Subnets:** `10.20.30.0/24, 10.20.30.10, 172.24.10.1, 172.24.10.1/24, 172.24.10.50/24`
- **Discovered Interfaces:** `enp11s0, ttyUSB0`
- **Related Knowledge Note:** [[knowledge/trained_sample_perimeter_router_playbook]]

## Distilled MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`)
| Pre-State ($s$) | Tactic ($\tau$) | Technique ($k$) | Tool ($u$) | Post-State ($s'$) | Verified Command ($c$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `s_l2_l3_verified` | **`Out-of-Band_Access`** | UART/Serial Console Out-of-Band Enumeration & Control | `ls` | `s_oob_serial_enumerated` | `ls -l /dev/ttyUSB* /dev/ttyACM*` |
| `s_firewall_or_acl_unlocked` | **`Lateral_Movement_Routing_Pivot`** | Remote Host Execution, L2/L3 Route Injection & Subnet Pivot | `ip` | `s_cross_subnet_pivot_routed` | `sudo ip addr replace 172.24.10.50/24 dev enp11s0` |
| `s_l2_l3_verified` | **`Out-of-Band_Access`** | UART/Serial Console Out-of-Band Enumeration & Control | `tio` | `s_oob_serial_enumerated` | `tio -b 115200 --script "write('\r\n'); expect('# ', 3000); write('ip -br addr; ip route show\r\n'); sleep(1); exit()" /dev/ttyUSB0` |
| `s_firewall_or_acl_unlocked` | **`Lateral_Movement_Routing_Pivot`** | Remote Host Execution, L2/L3 Route Injection & Subnet Pivot | `ip` | `s_cross_subnet_pivot_routed` | `sudo ip link set enp11s0 up` |
| `s_l2_l3_verified` | **`Out-of-Band_Access`** | UART/Serial Console Out-of-Band Enumeration & Control | `ip` | `s_oob_serial_enumerated` | `ip -br link show dev enp11s0` |
| `s_firewall_or_acl_unlocked` | **`Lateral_Movement_Routing_Pivot`** | Remote Host Execution, L2/L3 Route Injection & Subnet Pivot | `ip` | `s_cross_subnet_pivot_routed` | `sudo ip route replace 10.20.30.0/24 via 172.24.10.1 dev enp11s0 onlink` |
| `s_l2_l3_verified` | **`Out-of-Band_Access`** | UART/Serial Console Out-of-Band Enumeration & Control | `ip` | `s_oob_serial_enumerated` | `ip neigh show dev enp11s0` |
| `s_firewall_or_acl_unlocked` | **`Lateral_Movement_Routing_Pivot`** | Remote Host Execution, L2/L3 Route Injection & Subnet Pivot | `sysctl` | `s_cross_subnet_pivot_routed` | `sudo sysctl -w net.ipv4.ip_forward=1` |
| `s_l2_l3_verified` | **`Out-of-Band_Access`** | UART/Serial Console Out-of-Band Enumeration & Control | `arping` | `s_oob_serial_enumerated` | `arping -c 2 -w 2 -I enp11s0 172.24.10.1` |
| `s_firewall_or_acl_unlocked` | **`Lateral_Movement_Routing_Pivot`** | Remote Host Execution, L2/L3 Route Injection & Subnet Pivot | `iptables` | `s_cross_subnet_pivot_routed` | `sudo iptables -t nat -C POSTROUTING -o enp11s0 -j MASQUERADE 2>/dev/null \|\| sudo iptables -t nat -A POSTROUTING -o enp11s0 -j MASQUERADE` |
| `s_firewall_or_acl_unlocked` | **`Lateral_Movement_Routing_Pivot`** | Remote Host Execution, L2/L3 Route Injection & Subnet Pivot | `nmap` | `s_cross_subnet_pivot_routed` | `nmap -Pn -sT -T4 -p 22,80,443,8443 10.20.30.10` |
| `s_firewall_or_acl_unlocked` | **`Lateral_Movement_Routing_Pivot`** | Remote Host Execution, L2/L3 Route Injection & Subnet Pivot | `curl` | `s_cross_subnet_pivot_routed` | `curl -i -s -k --connect-timeout 5 --max-time 10 https://10.20.30.10:8443/` |

## Verified Executable Commands (Grouped by Capability Layer)

### General_System (5 commands)
```bash
ip -br link show dev enp11s0
sudo ip addr replace 172.24.10.50/24 dev enp11s0
sudo ip route replace 10.20.30.0/24 via 172.24.10.1 dev enp11s0 onlink
sudo sysctl -w net.ipv4.ip_forward=1
sudo iptables -t nat -C POSTROUTING -o enp11s0 -j MASQUERADE 2>/dev/null || sudo iptables -t nat -A POSTROUTING -o enp11s0 -j MASQUERADE
```

### L1_Serial_OOB (2 commands)
```bash
ls -l /dev/ttyUSB* /dev/ttyACM*
tio -b 115200 --script "write('\r\n'); expect('# ', 3000); write('ip -br addr; ip route show\r\n'); sleep(1); exit()" /dev/ttyUSB0
```

### L2_ARP_Link (3 commands)
```bash
ip neigh show dev enp11s0
arping -c 2 -w 2 -I enp11s0 172.24.10.1
sudo ip link set enp11s0 up
```

### L4_Port_Service (1 commands)
```bash
nmap -Pn -sT -T4 -p 22,80,443,8443 10.20.30.10
```

### L7_HTTP_Web (1 commands)
```bash
curl -i -s -k --connect-timeout 5 --max-time 10 https://10.20.30.10:8443/
```

