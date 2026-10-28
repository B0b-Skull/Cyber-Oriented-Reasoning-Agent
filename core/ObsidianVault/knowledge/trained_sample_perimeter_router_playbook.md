---
title: "Trained Knowledge & Topology: sample_perimeter_router_playbook.md"
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
doc_type: text
updated: 2026-10-24 01:00:23
---

# Trained Knowledge & Architecture: `sample_perimeter_router_playbook.md`

- **Source Path:** `~/Projects/CORA/Training/sample_perimeter_router_playbook.md` (`text`)
- **Extracted Technical Entities:** `arp, curl, https, iptables, nmap, serial, tio, ttyusb0`
- **Extracted IPs / Subnets:** `10.20.30.0/24, 10.20.30.10, 172.24.10.1, 172.24.10.1/24, 172.24.10.50/24`
- **Extracted Interfaces:** `enp11s0, ttyUSB0`
- **Linked Command Playbook:** [[commands/trained_sample_perimeter_router_playbook]] (`12` CEGAR-verified commands | `12` MDP transitions)

## Command & Tactic Coverage Summary
- **Total CEGAR-Verified Commands:** `12` (full executable list in [[commands/trained_sample_perimeter_router_playbook]])
- **Tactic Distribution:** `Lateral_Movement_Routing_Pivot` (7), `Out-of-Band_Access` (5)
- **Top Extracted CLI Tools:** `ip` (5), `arping` (1), `curl` (1), `iptables` (1), `ls` (1), `nmap` (1), `sysctl` (1), `tio` (1)

## Document Structure & Key Topics
- Field Playbook: Isolated Subnet & Serial UART Router Recovery
- Overview
- Verified Diagnostic & Remediation Commands
- 1. Layer-1 Out-of-Band Serial Discovery (`tio`)
- 2. Layer-2 Link & ARP Neighbor Verification
- 3. Layer-3 Subnet Alias, On-Link Route & NAT Masquerade
- 4. Layer-4 / Layer-7 Service Verification
- Common Failure Signatures & Fixes

## Extracted Reference Excerpt
# Field Playbook: Isolated Subnet & Serial UART Router Recovery

**Author:** CROW Innovations  

## Overview
This operational training document defines verified procedures for discovering and recovering an isolated embedded router (`172.24.10.1/24`) reachable across local Ethernet interface `enp11s0` (`172.24.10.50/24`) or via Out-of-Band USB-UART serial console (`/dev/ttyUSB0` at `115200 8N1`), forwarding traffic to an internal management perimeter (`10.20.30.0/24`, target gateway `10.20.30.10:8443`).

## Verified Diagnostic & Remediation Commands

### 1. Layer-1 Out-of-Band Serial Discovery (`tio`)
```bash
ls -l /dev/ttyUSB* /dev/ttyACM*
tio -b 115200 --script "write('\r\n'); expect('# ', 3000); write('ip -br addr; ip route show\r\n'); sleep(1); exit()" /dev/ttyUSB0
```

### 2. Layer-2 Link & ARP Neighbor Verification
```bash
ip -br link show dev enp11s0
ip neigh show dev enp11s0
arping -c 2 -w 2 -I enp11s0 172.24.10.1
```

### 3. Layer-3 Subnet Alias, On-Link Route & NAT Masquerade
If `RTNETLINK answers: File exists` occurs when adding an IP address, always use `ip addr replace` instead of `ip addr add`:
```bash
sudo ip addr replace 172.24.10.50/24 dev enp11s0
sudo ip link set enp11s0 up
sudo ip route replace 10.20.30.0/24 via 172.24.10.1 dev enp11s0 onlink
sudo sysctl -w net.ipv4.ip_forward=1
sudo iptables -t nat -C POSTROUTING -o enp11s0 -j MASQUERADE 2>/dev/null || sudo iptables -t nat -A POSTROUTING -o enp11s0 -j MASQUERADE
```

### 4. Layer-4 / Layer-7 Service Verification
```bash
nmap -Pn -sT -T4 -p 22,80,443,8443 10.20.30.10
curl -i -s -k --connect-timeout 5 --max-time 10 https://10.20.30.10:8443/
```

## Common Failure Signatures & Fixes
- **`RTNETLINK answers: File exists`** (`ip` exit code `2`): Caused by duplicate IP/route addition. Fix: Use `sudo ip addr replace 172.24.10.50/24 dev enp11s0` or `sudo ip route replace`.
- **`Error: Nexthop has invalid gateway`** (`ip` exit code `2`): Caused by missing local subnet alias on `enp11s0`. Fix: Assign `172.24.10.50/24` to `enp11s0` first or append `onlink`.
- **`100% packet loss`** (`ping` exit code `1`): Target drops ICMP or lacks return route. Fix: Check `ip neigh show` for L2 MAC resolution and enable `iptables -t nat -A POSTROUTING -o enp11s0 -j MASQUERADE`.

