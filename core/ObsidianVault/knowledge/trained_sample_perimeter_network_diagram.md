---
title: "Trained Knowledge & Topology: sample_perimeter_network_diagram.png"
tags:
  - eth0
  - https
  - image_diagram
  - lateral_movement_routing_pivot
  - mdp
  - out-of-band_access
  - serial
  - ssh
  - trained
  - ttyusb0
source_file: sample_perimeter_network_diagram.png
doc_type: image_diagram
updated: 2026-10-24 01:00:22
---

# Trained Knowledge & Architecture: `sample_perimeter_network_diagram.png`

- **Source Path:** `~/Projects/CORA/Training/sample_perimeter_network_diagram.png` (`image_diagram`)
- **Extracted Technical Entities:** `eth0, https, serial, ssh, ttyusb0`
- **Extracted IPs / Subnets:** `10.20.30.0/24, 10.20.30.1, 10.20.30.1/24, 10.20.30.10/24, 172.24.10.1, 172.24.10.1/24, 172.24.10.50/24`
- **Extracted Interfaces:** `enp11s0, eth0, ttyUSB0`
- **Linked Command Playbook:** [[commands/trained_sample_perimeter_network_diagram]] (`2` CEGAR-verified commands | `2` MDP transitions)

## Command & Tactic Coverage Summary
- **Total CEGAR-Verified Commands:** `2` (full executable list in [[commands/trained_sample_perimeter_network_diagram]])
- **Tactic Distribution:** `Lateral_Movement_Routing_Pivot` (1), `Out-of-Band_Access` (1)
- **Top Extracted CLI Tools:** `ip` (2)

### Visual & Network Diagram Intelligence (`sample_perimeter_network_diagram.png`)
- **Diagram IPv4 / Subnets:** `10.20.30.0/24, 10.20.30.1, 10.20.30.1/24, 10.20.30.10/24, 172.24.10.1, 172.24.10.1/24, 172.24.10.50/24`
- **Diagram Interfaces / Serial Ports:** `enp11s0, eth0, ttyUSB0`
- **Diagram Ports / Services:** `22, :8443`
- **Spatially Grouped Diagram Nodes (Box/Component Clusters):**
  1. `[PERIMETERROUTER&SERIALOOBRECOVERYARCHITECTURE | L2ARP]`
  2. `[HOST:LLM-WORKSTATION | NIC: enp1ls0 | IP: 172.24.10.50/24 | UART:/dev/ttyUSB0 115200 | NAT:MASQUERADEenp11s0]`
  3. `[ROUTER:EDGE-GW-01 | WAN: eth0 172.24.10.1/24 | LAN:br0 10.20.30.1/24 | PORT: 22/tcp SSH | SERIAL: ttyS0 115200]`
  4. `[TARGET:PERIMETER-CORE | NIC: eth0 | onlink rou | IP: 10.20.30.10/24 | GW: 10.20.30.1 | HTTPS:8443/tcp]`
  5. `[CMD1: sudo ip addr replace 172.24.10.50/24 dev enp11s0 | CMD2: sudo ip route replace 10.20.30.0/24 via 172.24.10.1 dev enp11s0 onlink]`

## Document Structure & Key Topics
- Visual & Network Diagram Intelligence (`sample_perimeter_network_diagram.png`)

## Extracted Reference Excerpt
PERIMETERROUTER&SERIALOOBRECOVERYARCHITECTURE
HOST:LLM-WORKSTATION
ROUTER:EDGE-GW-01
TARGET:PERIMETER-CORE
NIC: enp1ls0
L2ARP
WAN: eth0 172.24.10.1/24
NIC: eth0
IP: 172.24.10.50/24
LAN:br0 10.20.30.1/24
onlink rou
IP: 10.20.30.10/24
UART:/dev/ttyUSB0 115200
PORT: 22/tcp SSH
GW: 10.20.30.1
NAT:MASQUERADEenp11s0
SERIAL: ttyS0 115200
HTTPS:8443/tcp
CMD1: sudo ip addr replace 172.24.10.50/24 dev enp11s0
CMD2: sudo ip route replace 10.20.30.0/24 via 172.24.10.1 dev enp11s0 onlink

