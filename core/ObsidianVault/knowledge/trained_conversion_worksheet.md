---
title: "Trained Knowledge & Topology: Conversion Worksheet"
category: knowledge
domain_hub: "[[knowledge/07_packet_capture_bpf_wireshark_and_passive_fingerprinting]]"
os_platform: cross-platform
primary_tactic: Passive_Enum
summary: "Operational architecture, decision workflows & Windows/Linux command reference for Conversion Worksheet: Berkeley Packet Filter (BPF) byte-offset syntax, tcpdump and tshark CLI packet capture, Windows pktmon/netsh trace capture, Wiresh"
when_to_apply: "Apply when working with Conversion Worksheet (cross-platform): Apply when capturing live network traffic (`tcpdump`/`tshark`/`pktmon`), writing BPF byte-offset filters (`tcp[13]`, `icmp[0]`), analyzing `.pcap` files with Wireshark/tshark display filters, decoding IPv4/TCP/ICMP/ARP/STP headers, or passively fingerprinting remote OS types via `p0f` or DHCP options without transmitting active packets."
tags: [http, mdp, pdf, trained, linux, windows, tcpdump, tshark, wireshark, bpf, p0f, pktmon, arp, icmp, tcp, ipv4, dhcp, vlan, stp, pcap, passive_enum]
source_file: "Conversion Worksheet"
updated: 2026-10-30
---

# Trained Knowledge & Architecture: `Conversion_Worksheet.pdf`

- **Source Path:** `~/Projects/CORA/Training/Conversion_Worksheet.pdf` (`pdf`)
- **Extracted Technical Entities:** `http`
- **Extracted IPs / Subnets:** `None`
- **Extracted Interfaces:** `None`

## Extracted Operational Steps & Workflows
- 1. 11001011
- 2. 00110101
- 3. 10000011
- 4. 10001111
- 5. 11100011
- 6. 00000100
- 7. 00010010
- 8. 00111111
- 9. 10101010
- 1. 213
- 2. 9
- 3. 67
- 4. 99
- 5. 23
- 6. 143
- 7. 6
- 8. 1
- 9. 197
- 1. 11001100
- 2. 11110001
- 3. 00110001
- 4. 11000010
- 5. 10100100
- 6. 10100111
- 7. 11101100
- 8. 11111100
- 9. 00111111
- 1. 0x45
- 2. 0xFA
- 3. 0x5D
- 4. 0x99
- 5. 0x03
- 6. 0x6B
- 7. 0xDD
- 8. 0xFE
- 9. 0x22
- 1. 233
- 2. 21
- 3. 9
- 4. 75
- 5. 188
- 6. 56
- 7. 4
- 8. 121
- 9. 94

## Extracted Reference Excerpt
--- [Page 1] ---
Binary, Decimal, Hexadecimal Conversion Exercises 
http://east82.com/ 
 
Binary to decimal 
1. 11001011 
2. 00110101 
3. 10000011 
4. 10001111 
5. 11100011 
6. 00000100 
7. 00010010 
8. 00111111 
9. 10101010 
10.01010101 
Decimal to binary 
1. 213 
2. 9 
3. 67 
4. 99 
5. 23 
6. 143 
7. 6 
8. 1 
9. 197 
10.252 
Binary to hex 
1. 11001100 
2. 11110001 
3. 00110001 
4. 11000010 
5. 10100100 
6. 10100111 
7. 11101100 
8. 11111100 
9. 00111111 
10.00000011 
Hex to binary 
1. 0x45 
2. 0xFA 
3. 0x5D 
4. 0x99 
5. 0x03 
6. 0x6B 
7. 0xDD 
8. 0xFE 
9. 0x22 
10.0x18 
Decimal to hex 
1. 233 
2. 21 
3. 9 
4. 75 
5. 188 
6. 56 
7. 4 
8. 121 
9. 94 
10.201 
Hex to decimal 
1. 0x5A 
2. 0xCC 
3. 0x97 
4. 0x40 
5. 0x07 
6. 0x3D 
7. 0xF1 
8. 0xFB 
9. 0x82 
10.0xE4

--- [Page 2] ---
Binary, Decimal, Hexadecimal Conversion Exercises 
http://east82.com/ 
 
Answers 
Binary to decimal 
1. 11001011 – 203 
2. 00110101 – 53 
3. 10000011 – 131 
4. 10001111 – 143 
5. 11100011 – 227 
6. 00000100 – 4 
7. 00010010 – 18 
8. 00111111 – 63 
9. 10101010 – 170 
10.01010101 – 85 
Decimal to binary 
11.213 – 11010101 
12.9 – 00001001 
1. 67 – 01000011 
2. 99 – 01100011 
3. 23 – 00010111 
4. 143 – 10001111 
5. 6 – 00000110 
6. 1 – 00000001 
7. 197 – 11000101 
8. 252 – 11111100 
Binary to hex 
1. 11001100 – 0xCC 
2. 11110001 – 0xF1 
3. 00110001 – 0x31 
4. 11000010 – 0xC2 
5. 10100100 – 0xA4 
6. 10100111 – 0xA7 
7. 11101100 – 0xEC 
8. 11111100 – 0xFC 
9. 00111111 – 0x3F 
10.00000011 – 0x03 
 
Hex to binary 
1. 0x45 – 01000101 
2. 0xFA – 11111010 
3. 0x5D – 01011101 
4. 0x99 – 10011001 
5. 0x03 – 00000011 
6. 0x6B – 01101011  
7. 0xDD – 11011101 
8. 0xFE – 11111110 
9. 0x22 – 00100010 
10.0x18 – 00011000 
Decimal to hex 
11.233 – 0xE9 
1. 21 – 0x15 
2. 9 – 0x09 
3. 75 – 0x4B 
4. 188 – 0xBC 
5. 56 – 0x38 
6. 4  – 0x04 
7. 121 – 0x79 
8. 94 – 0x5E 
9. 201 – 0xC9 
Hex to decimal 
1. 0x5A – 90 
2. 0xCC – 204 
3. 0x97 – 151 
4. 0x40 – 64 
5. 0x07 – 7 
6. 0x3D – 61 
7. 0xF1 – 241 
8. 0xFB – 251 
9. 0x82 – 130 
10.0xE4 – 228

<!-- CORA-MAXIMIZED-COMMANDS-START -->
## Maximized Windows & Linux Command Examples for `Conversion Worksheet`

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
