---
title: "Trained Knowledge & Topology: CQC001 E010 M050 DHCP Fingerprints"
category: knowledge
domain_hub: "[[knowledge/07_packet_capture_bpf_wireshark_and_passive_fingerprinting]]"
os_platform: cross-platform
primary_tactic: Passive_Enum
summary: "Operational architecture, decision workflows & Windows/Linux command reference for CQC001 E010 M050 DHCP Fingerprints: Berkeley Packet Filter (BPF) byte-offset syntax, tcpdump and tshark CLI packet capture, Windows pktmon/netsh trace capture, Wiresh"
when_to_apply: "Apply when working with CQC001 E010 M050 DHCP Fingerprints (cross-platform): Apply when capturing live network traffic (`tcpdump`/`tshark`/`pktmon`), writing BPF byte-offset filters (`tcp[13]`, `icmp[0]`), analyzing `.pcap` files with Wireshark/tshark display filters, decoding IPv4/TCP/ICMP/ARP/STP headers, or passively fingerprinting remote OS types via `p0f` or DHCP options without transmitting active packets."
tags: [enumeration, http, mdp, text, trained, z3, linux, windows, tcpdump, tshark, wireshark, bpf, p0f, pktmon, arp, icmp, tcp, ipv4, dhcp, vlan, stp, pcap]
source_file: "CQC001 E010 M050 DHCP Fingerprints"
updated: 2026-10-30
---

# Trained Knowledge & Architecture: `CQC001_E010_M050_DHCP_Fingerprints.txt`

- **Source Path:** `~/Projects/CORA/Training/CQC001_E010_M050_DHCP_Fingerprints.txt` (`text`)
- **Extracted Technical Entities:** `http, z3`
- **Extracted IPs / Subnets:** `1.5.0.0, 1.6.0.3, 1.8.5.3, 10.0.10.648, 10.0.10.672, 10.0.10.684, 10.0.10.690, 10.0.10.738, 10.3.0.700, 10.3.1.226, 10.3.1.821, 10.3.2.281, 10.3.2.500, 10.3.2.680, 10.3.2.798, 10.3.2.858, 10.3.2.876, 2.0.14.1, 2.6.5.5, 2.7.0.1, 3.2.1.70, 3.6.2.5, 3.6.3.12, 3.7.1.0, 3.7.1.28, 3.8.2.99, 3.9.0.834, 4.1.0.29, 4.1.4.1, 4.1.7.252, 4.2.7.498, 4.4.2.1, 4.5.3.1, 4.5.4.2, 4.5.9.461, 4.6.0.126, 4.6.0.216, 4.6.1.250, 4.6.1.310, 4.6.1.314, 5.0.0.344, 5.0.0.351, 5.0.0.497, 5.0.0.509, 5.0.0.592, 5.0.0.593, 5.0.0.604, 5.0.0.654, 5.0.0.656, 5.0.0.681, 5.0.0.743, 5.0.0.794, 5.0.0.832, 5.0.0.845, 5.0.0.846, 5.0.0.862, 5.0.0.900, 5.0.0.955, 5.0.0.975, 5.1.2.9, 5.1.3.19, 5.1.4.020, 5.1.5.002, 5.5.2.2, 5.5.3.1, 5.5.6.1, 6.0.0.141, 6.0.0.246, 6.0.0.285, 6.0.0.294, 6.0.0.337, 6.0.0.431, 6.0.0.436, 6.0.0.448, 6.0.0.461, 6.0.0.480, 6.0.0.481, 6.0.0.526, 6.0.0.534, 6.0.0.546, 6.0.0.570, 6.0.0.576, 6.0.0.600, 6.0.0.615, 6.0.0.666, 6.0.0.668, 6.0.0.706, 6.0.0.719, 6.0.0.723, 6.0.0.747, 6.5.3.5, 6.6.0.19, 6.6.0.42, 6.7.0.34, 6.7.2.2, 6.7.3.2, 6.8.0.23, 6.8.1.26, 6.9.0.28, 6.9.1.1, 7.0.0.254, 7.0.0.261, 7.0.0.296, 7.0.0.317, 7.0.0.319, 7.0.0.353, 7.0.0.374, 7.0.0.482, 7.0.0.513, 7.0.0.528, 7.0.0.530, 7.0.0.540, 7.0.0.557, 7.0.0.576, 7.0.0.579, 7.0.0.585, 7.0.0.586, 7.0.0.590, 7.0.0.598, 7.0.0.611, 7.1.0.163, 7.1.0.219, 7.1.0.267, 7.1.0.284, 7.1.0.336, 7.1.0.342, 7.1.0.391, 7.1.0.398, 7.1.0.477, 7.1.0.523, 7.1.0.569, 7.1.0.580, 7.1.0.634, 7.1.0.658, 7.1.0.694, 7.1.0.714, 7.1.0.746, 7.1.0.755, 7.1.0.768, 7.1.0.794, 7.1.0.821, 7.1.0.862, 7.1.0.865, 7.1.0.907, 7.1.0.912, 7.4.1.42`
- **Extracted Interfaces:** `None`
- **Linked Command Playbook:** [[commands/trained_cqc001_e010_m050_dhcp_fingerprints]] (`4` CEGAR-verified commands | `4` MDP transitions)

## Command & Tactic Coverage Summary
- **Total CEGAR-Verified Commands:** `4` (full executable list in [[commands/trained_cqc001_e010_m050_dhcp_fingerprints]])
- **Tactic Distribution:** `Enumeration` (4)
- **Top Extracted CLI Tools:** `cat` (1), `echo` (1), `find` (1), `gem` (1)

## LLM Distilled Operational Summary
### 1. Key Operational Techniques & Decision Workflows

*   **Fingerprint Identification**: Identify device types (e.g., Android, Windows, PXE, VoIP) by analyzing the ordered list of DHCP option codes within the `DHCP DISCOVER` message.
*   **Differentiation Strategy**: Distinguish between similar devices (e.g., various *Polycom SoundStation IP 7000* models or *Xerox* printers) by detecting specific, optional option codes that appear in subsets of the base fingerprint.
*   **Base vs. Extended Fingerprinting**: Recognize that many devices share a common "base" set of options (typically `1,2,3,4,6,15,28,42,43`) and rely on additional codes (e.g., `120`, `132`, `160`) to confirm specific hardware revisions or vendor implementations.
*   **Vendor-Specific Signatures**: Leverage unique option clusters for specific vendors:
    *   **PXE/Network Boot**: High option count including `50, 54, 60, 66, 67` (bootfile, server, client identifier).
    *   **Printers**: Distinctive presence of options `26, 85-88, 44-47`.
    *   **VoIP**: Frequent inclusion of `54, 160, 159, 150`.

### 2. Critical Command Patterns and Required Flags

*   **Capture Target**: `DHCP DISCOVER` message payload.
*   **Primary Field**: `DHCP options` field.
*   **Analysis Unit**: Ordered list of **Option Codes** (e.g., `1, 2, 3...`).
*   **Sorting Logic**: Fingerprint lists are sorted by the sequence of option codes.

### 3. Network Topology & Service Relationships

*   **Common Base Options**: Most devices share options `1` (Message Type), `2` (Server Identifier), `3` (IP Address), `4` (Server Name), `6` (Subnet Mask), `15` (DNS Name), `28` (DNS Server), and `42` (Client Identifier).
*   **PXE/Boot Services**: Devices requiring network boot (PXE) exhibit a large set of options including `50` (Boot File Name), `54` (DHCP Server Identifier), `60` (Client Class), `66` (Boot Server Host Name), and `67` (Boot File Size).
*   **VoIP/Telephony**: Devices like Polycom and Grandstream often include `54` (DHCP Server), `160` (Vendor Specific), and `159/150` (Cisco/Grandstream specific).
*   **Printer Services**: Printers (Brother, Xerox, Dell) consistently show options `26` (Printer Name), `85-88` (Printer Status/Info), and `44-47` (Printer Options).
*   **Mobile/Consumer**: Devices like Apple iPhone/TV and Android phones typically use a minimal set (`1` or `1,

<!-- CORA-MAXIMIZED-COMMANDS-START -->
## Maximized Windows & Linux Command Examples for `CQC001 E010 M050 DHCP Fingerprints`

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
