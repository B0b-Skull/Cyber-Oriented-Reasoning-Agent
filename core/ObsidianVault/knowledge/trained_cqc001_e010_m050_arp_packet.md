---
title: "Trained Knowledge & Topology: CQC001 E010 M050 ARP Packet"
category: knowledge
domain_hub: "[[knowledge/07_packet_capture_bpf_wireshark_and_passive_fingerprinting]]"
os_platform: cross-platform
primary_tactic: Passive_Enum
summary: "Operational architecture, decision workflows & Windows/Linux command reference for CQC001 E010 M050 ARP Packet: Berkeley Packet Filter (BPF) byte-offset syntax, tcpdump and tshark CLI packet capture, Windows pktmon/netsh trace capture, Wiresh"
when_to_apply: "Apply when working with CQC001 E010 M050 ARP Packet (cross-platform): Apply when capturing live network traffic (`tcpdump`/`tshark`/`pktmon`), writing BPF byte-offset filters (`tcp[13]`, `icmp[0]`), analyzing `.pcap` files with Wireshark/tshark display filters, decoding IPv4/TCP/ICMP/ARP/STP headers, or passively fingerprinting remote OS types via `p0f` or DHCP options without transmitting active packets."
tags: [arp, http, https, mdp, pdf, trained, linux, windows, tcpdump, tshark, wireshark, bpf, p0f, pktmon, icmp, tcp, ipv4, dhcp, vlan, stp, pcap, passive_enum]
source_file: "CQC001 E010 M050 ARP Packet"
updated: 2026-10-30
---

# Trained Knowledge & Architecture: `CQC001_E010_M050_ARP_Packet.pdf`

- **Source Path:** `~/Projects/CORA/Training/CQC001_E010_M050_ARP_Packet.pdf` (`pdf`)
- **Extracted Technical Entities:** `arp, http, https`
- **Extracted IPs / Subnets:** `129.25.10.11`
- **Extracted Interfaces:** `None`

## LLM Distilled Operational Summary
### Key Operational Techniques & Decision Workflows
*   **Same-Network Communication**: Hosts on the same LAN use ARP directly to resolve the destination IP to a MAC address before encapsulating data in an Ethernet frame.
*   **Cross-Network Communication**: Hosts on different networks consult their routing tables to identify the next-hop router (gateway), then use ARP to resolve the router's MAC address.
*   **Router-to-Router Forwarding**: Routers use ARP to resolve MAC addresses for subsequent hops or destinations on directly connected networks.
*   **Cache Optimization**: After an ARP request/reply exchange, both the requester and the responder update their local ARP caches. This allows future packets destined for the same IP to bypass the ARP request phase, reducing latency.

### Critical Command Patterns and Required Flags
*   **Broadcast Request**: The initiating host sends an ARP Request to the Ethernet broadcast address `FF:FF:FF:FF:FF:FF`.
*   **Unicast Reply**: The target host responds with a specific ARP Reply sent directly (unicast) to the requester's MAC address.
*   **Operation Codes**:
    *   `1`: Indicates an ARP Request.
    *   `2`: Indicates an ARP Reply.

### Network Topology & Address Relationships
*   **Hardware Type (HTYPE)**: Specifies the link-layer protocol; for standard Ethernet, the value is `1`.
*   **Protocol Type (PTYPE)**: Identifies the internetwork protocol; for IPv4, the value is `0x0800`.
*   **Address Lengths**:
    *   **Hardware Length (HLEN)**: 6 octets (48-bit) for Ethernet MAC addresses.
    *   **Protocol Length (PLEN)**: 4 octets (32-bit) for IPv4 addresses.
*   **Field Roles**:
    *   **Sender Hardware Address (SHA)**: The MAC address of the device sending the packet.
    *   **Sender Protocol Address (SPA)**: The IP address of the device sending the packet.
    *   **Target Hardware Address (THA)**: The MAC address of the intended receiver (ignored in Requests, populated in Replies).
    *   **Target Protocol Address (TPA)**: The IP address of the intended receiver.

## Extracted Operational Steps & Workflows
- 1. When two hosts are on the same network and one desires to send a packet to the other
- 2. When two hosts are on different networks and must use a gateway or router to reach the other host
- 3. When a router needs to forward a packet for one host through another router
- 4. When a router needs to forward a packet from one host to the destination host on the same network

<!-- CORA-MAXIMIZED-COMMANDS-START -->
## Maximized Windows & Linux Command Examples for `CQC001 E010 M050 ARP Packet`

> **Domain Hub:** [[knowledge/07_packet_capture_bpf_wireshark_and_passive_fingerprinting|Domain Hub 07: Packet Capture (tcpdump / tshark / pktmon), BPF Syntax, Wireshark Filters, RFC792/IPv4/TCP/ARP/STP Headers & Passive Fingerprinting (p0f / DHCP)]]  
> **Master Playbooks:** [[commands/windows_master_command_playbook]] | [[commands/linux_master_command_playbook]] | [[commands/curl_playbook]] | [[commands/tio_serial_playbook]]  
> **When to Apply:** Apply when capturing live network traffic (`tcpdump`/`tshark`/`pktmon`), writing BPF byte-offset filters (`tcp[13]`, `icmp[0]`), analyzing `.pcap` files with Wireshark/tshark display filters, decoding IPv4/TCP/ICMP/ARP/STP headers, or passively fingerprinting remote OS types via `p0f` or DHCP options without transmitting active packets.  
> **15-Engine H-MDP State Transition:** `s_passive_topology_mapped` $\xrightarrow{\text{Passive_Enum}}$ `s_l2_l3_verified` | **Bayesian Root-Cause Triggers:** `silent_firewall_syn_drop, asymmetric_routing_missing_syn_ack, vlan_8021q_tag_mismatch, stp_bridge_port_blocking` | **Isolation:** `RED, BLUE, WHITE (Offline .pcap analysis works in WHITE; live interface capture works in RED and allowed BLUE NICs)`

| Primary Command (`Windows` / `Linux`) | OS / Shell | What It Does & Key Flags | When to Apply & Expected Output | Cross-Platform Equivalent |
| :--- | :--- | :--- | :--- | :--- |
| `sudo tcpdump -ni <IFACE> -c 50 -nn -e 'arp or icmp'` | **Linux Bash** | Captures 50 ARP or ICMP frames on `<IFACE>` without DNS resolution (`-nn`) and prints L2 Ethernet MAC addresses and VLAN tags (`-e`). | Apply to verify whether ARP replies or ICMP Echo Replies (`type 0`) / Destination Unreachable (`type 3`) actually arrive on the wire (`[[commands/trained_bpf_syntax]]`). | `pktmon start --capture --comp nics` |
| `sudo tcpdump -ni <IFACE> -nn 'tcp[13] & 2 != 0 and host <TARGET_IP>'` | **Linux Bash** | BPF byte-offset filter inspecting byte 13 of the TCP header (`tcp[13]` flags byte): matches `SYN` (`0x02`) or `SYN-ACK` (`0x12`) packets for `<TARGET_IP>` (`[[commands/trained_jstebelton_bpf-syntax]]`). | Apply to check if outbound TCP `SYN` probes receive `SYN-ACK` (`0x12`), `RST-ACK` (`0x14`, port closed), or silence (firewall drop). | `tshark.exe -i <IFACE> -f "tcp[13] & 2 != 0 and host <TARGET_IP>"` |
| `sudo tcpdump -ni <IFACE> -nn 'tcp[13] == 18'` | **Linux Bash** | Captures exclusively `SYN-ACK` packets (`SYN=2` + `ACK=16` = `18` / `0x12`) to passively spot open ports responding on the wire. | Apply during network troubleshooting or scan verification to log every open port answering with `SYN-ACK`. | `tshark.exe -i <IFACE> -f "tcp[13] == 18"` |
| `sudo tcpdump -ni <IFACE> -s0 -G 300 -W 1 -w /tmp/capture.pcap 'not port 22'` | **Linux Bash** | Writes full-length frames (`-s0`) excluding SSH (`not port 22`) to `/tmp/capture.pcap` for up to 300 seconds (`[[commands/trained_capture_sh]]`). | Apply to record a lossless packet capture for `tshark`, `p0f`, or `Wireshark` inspection. | `netsh trace start capture=yes IPv4.Address=<TARGET_IP> tracefile=C:\Temp\net.etl` |
| `tshark -r /tmp/capture.pcap -q -z conv,tcp -z io,phs` | **Linux / Windows** | Reads `/tmp/capture.pcap` (`-r`) and prints protocol hierarchy statistics (`io,phs`) and top TCP conversations (`conv,tcp`) (`[[knowledge/trained_cqc001_e010_m010_network_traffic_monitoring]]`). | Apply first on any `.pcap` file to get an instant breakdown of protocols, endpoints, and byte volumes. | `tshark.exe -r C:\Temp\capture.pcap -q -z conv,tcp -z io,phs` |
| `tshark -r /tmp/capture.pcap -Y "http.request or tls.handshake.type == 1 or arp.opcode == 2" -T fields -e frame.time -e eth.src -e ip.src -e ip.dst -e http.host -e tls.handshake.extensions_server_name` | **Linux / Windows** | Applies Wireshark Display Filters (`-Y`) to extract timestamps, MACs, IPs, HTTP hosts, and TLS SNI server names (`[[knowledge/trained_cqc001_e010_m030_wireshark_display_filters]]`). | Apply to extract clear-text HTTP requests, TLS Server Name Indications, and ARP replies from a capture. | `tshark.exe -r C:\Temp\capture.pcap -Y "http.request or tls.handshake.type == 1"` |
| `tshark -r /tmp/capture.pcap -Y "bootp.option.type == 53" -T fields -e eth.src -e ip.src -e bootp.option.hostname -e bootp.option.request_list_item -e bootp.option.vendor_class_id` | **Linux / Windows** | Extracts DHCP client MAC, hostname (`Option 12`), Parameter Request List (`Option 55` fingerprint), and Vendor Class (`Option 60`) (`[[knowledge/trained_cqc001_e010_m050_dhcp_fingerprints]]`). | Apply to passively identify exact client OS versions (Windows 10/11, Android, iOS, Linux, FortiOS) from DHCP broadcasts. | `tshark.exe -r C:\Temp\capture.pcap -Y "dhcp"` |
| `sudo p0f -i <IFACE> -o /tmp/p0f.log \|\| p0f -r /tmp/capture.pcap` | **Linux Bash** | Passively identifies remote OS, kernel version, link MTU, and network distance (TTL) from TCP handshake parameters (`[[knowledge/trained_cqc001_e010_m040_p0f]]`). | Apply in passive/stealth regimes to fingerprint remote OS stacks without sending a single active packet. | `p0f.exe -r C:\Temp\capture.pcap` |
| `sudo tcpdump -ni <IFACE> -nn -e 'ether proto 0x88cc or (ether[14:2] == 0xaaaa and ether[20:2] == 0x2000) or stp'` | **Linux Bash** | Captures L2 discovery frames: LLDP (`0x88cc`), Cisco Discovery Protocol (`CDP`), and Spanning Tree Protocol (`STP` BPDUs) (`[[knowledge/trained_cqc001_e010_m060_spanning_tree_protocol]]`). | Apply on a newly connected switch port to passively learn switch hostname, management IP, native VLAN ID, and STP root bridge. | `pktmon start --capture --pkt-size 0` |
| `pktmon start --capture --comp nics --pkt-size 0 && timeout /t 15 && pktmon stop && pktmon etl2pcap PktMon.etl -o C:\Temp\win_capture.pcapng` | **Windows CMD (Admin)** | Built-in Windows 10/11/Server 2019+ packet sniffer (`pktmon`): captures raw frames across NICs and converts `.etl` directly to `.pcapng` for Wireshark/tshark! | Apply on Windows hosts when Wireshark/Npcap is not installed and you need a native `.pcapng` packet capture. | `sudo tcpdump -ni <IFACE> -s0 -c 100 -w /tmp/capture.pcap` |

### Copy-Pasteable Execution Block (Windows & Linux)
```bash
# [Linux Bash] Captures 50 ARP or ICMP frames on `<IFACE>` without DNS resolution (`-nn`) and prints L2 Ethernet MAC addresses and VLAN tags (`-e`).
sudo tcpdump -ni <IFACE> -c 50 -nn -e 'arp or icmp'
# [Linux Bash] BPF byte-offset filter inspecting byte 13 of the TCP header (`tcp[13]` flags byte): matches `SYN` (`0x02`) or `SYN-ACK` (`0x12`) packets for `<TARGET_IP>` (`[[commands/trained_jstebelton_bpf-syntax]]`).
sudo tcpdump -ni <IFACE> -nn 'tcp[13] & 2 != 0 and host <TARGET_IP>'
# [Linux Bash] Captures exclusively `SYN-ACK` packets (`SYN=2` + `ACK=16` = `18` / `0x12`) to passively spot open ports responding on the wire.
sudo tcpdump -ni <IFACE> -nn 'tcp[13] == 18'
# [Linux Bash] Writes full-length frames (`-s0`) excluding SSH (`not port 22`) to `/tmp/capture.pcap` for up to 300 seconds (`[[commands/trained_capture_sh]]`).
sudo tcpdump -ni <IFACE> -s0 -G 300 -W 1 -w /tmp/capture.pcap 'not port 22'
# [Linux / Windows] Reads `/tmp/capture.pcap` (`-r`) and prints protocol hierarchy statistics (`io,phs`) and top TCP conversations (`conv,tcp`) (`[[knowledge/trained_cqc001_e010_m010_network_traffic_monitoring]]`).
tshark -r /tmp/capture.pcap -q -z conv,tcp -z io,phs
# [Linux / Windows] Applies Wireshark Display Filters (`-Y`) to extract timestamps, MACs, IPs, HTTP hosts, and TLS SNI server names (`[[knowledge/trained_cqc001_e010_m030_wireshark_display_filters]]`).
tshark -r /tmp/capture.pcap -Y "http.request or tls.handshake.type == 1 or arp.opcode == 2" -T fields -e frame.time -e eth.src -e ip.src -e ip.dst -e http.host -e tls.handshake.extensions_server_name
```
<!-- CORA-MAXIMIZED-COMMANDS-END -->
