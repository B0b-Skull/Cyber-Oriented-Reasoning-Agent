---
title: "Trained Knowledge & Topology: metro case studies"
category: knowledge
domain_hub: "[[knowledge/09_hardware_uart_serial_oob_and_telecom_wan]]"
os_platform: cross-platform
primary_tactic: OOB_Serial_Access
summary: "Operational architecture, decision workflows & Windows/Linux command reference for metro case studies: Non-interactive tio 3.9 Lua --script UART serial console automation (/dev/ttyUSB0, -o 15 -O 120 pacing), Windows COM port OOB acce"
when_to_apply: "Apply when working with metro case studies (cross-platform): Apply whenever network connections to an appliance fail (`Exit 7` Connection Refused or `Exit 28` Timeout) and a hardware serial console (`/dev/ttyUSB0` or `COM1`) is available (`C1_OOB_SERIAL_LOOPBACK_APPLIANCE`), or when analyzing Carrier Metro Ethernet, MPLS/GMPLS labels, OTN/GPON optical links, SD-WAN tunnels, Wi-Fi 802.11, or 2G/3G/4G/5G cellular RAN protocols."
tags: [enumeration, mdp, pdf, responder, trained, vlan, linux, windows, tio, serial, ttyusb0, ttyusb1, com1, uart, oob, oob_serial_access, mpls, gmpls, metro_ethernet, otn, gpon, sd-wan]
source_file: "metro case studies"
updated: 2026-10-30
---

# Trained Knowledge & Architecture: `metro case studies.pdf`

- **Source Path:** `~/Projects/CORA/Training/metro case studies.pdf` (`pdf`)
- **Extracted Technical Entities:** `responder, vlan`
- **Extracted IPs / Subnets:** `None`
- **Extracted Interfaces:** `LO`
- **Linked Command Playbook:** [[commands/trained_metro_case_studies]] (`1` CEGAR-verified commands | `1` MDP transitions)

## Command & Tactic Coverage Summary
- **Total CEGAR-Verified Commands:** `1` (full executable list in [[commands/trained_metro_case_studies]])
- **Tactic Distribution:** `Enumeration` (1)
- **Top Extracted CLI Tools:** `find` (1)

### Visual & Network Diagram Intelligence (`metro case studies.pdf#page1`)
- **Spatially Grouped Diagram Nodes (Box/Component Clusters):**
  1. `[ciena.]`
  2. `[Verizon Wireless]`
  3. `[Dark Fiber Equipment Solution]`
  4. `[Overview]`

### Visual & Network Diagram Intelligence (`metro case studies.pdf#page19`)
- **Spatially Grouped Diagram Nodes (Box/Component Clusters):**
  1. `[Case Study: | AT&T's Intelligent Optical Network]`
  2. `[The Next Revolution is Here]`

### Visual & Network Diagram Intelligence (`metro case studies.pdf#page33`)
- **Spatially Grouped Diagram Nodes (Box/Component Clusters):**
  1. `[Architecture Variations | (Cisco's Case Study)]`
  2. `[33]`

## LLM Distilled Operational Summary
### Operational Techniques & Decision Workflows
*   **Spatial Clustering:** Group network diagrams by vendor (Ciena, Verizon) and solution type (Dark Fiber, Overview) to isolate architectural variations.
*   **Service Abstraction:** Treat VLANs as equivalent to STS (Synchronous Transport Signal) for simplified ring management and fault isolation.
*   **Scalable Ring Design:** Utilize EBH (Ethernet Backhaul) protection to dynamically grow ring diameter, node count, and bandwidth without hardware replacement.
*   **Multi-Layer Aggregation:** Implement dual-homing strategies to support P2P, P2MP, and multipoint traffic flows across unicast, multicast, and broadcast layers.
*   **Platform Convergence:** Deploy a single software load across 2-slot, 7-slot, 14-slot, and 32-slot chassis to maintain consistency from Metro Edge to ULH Core.
*   **Density Expansion:** Transition from L2 MOTR (2x10G) to eMOTR (12x10G) at MSCs or cell sites to achieve 4x density while maintaining n:1 10GE aggregation.

### Critical Command Patterns & Required Flags
*   **Protection Switching:** `50ms` restoration time target for rapid service recovery before higher-level fault mechanisms trigger.
*   **Interface Configuration:** Assign specific VLANs to ring interfaces; support for `802.1q` (VLAN tagging) and `802.1ad` (Q-in-Q).
*   **Port Aggregation:** Enable `LAG` (Link Aggregation Group) across ports or cards for load balancing and redundancy.
*   **Traffic Management:** Activate `802.1ag` for connectivity verification and partial `Y.1731` for traffic performance monitoring.
*   **Optical Reach:** Configure `SR/IR/LR` (Short/Intermediate/Long Reach) or `CWDM/DWDM` modules based on distance requirements (up to 28dB reach).

### Network Topology & Relationships
*   **Vendor Ecosystems:**
    *   **Ciena:** Primary provider for OME 6500 family, 6500-7/14/32 edge-to-core solutions, and 5G TMUX.
    *   **Verizon Wireless:** Key customer utilizing Dark Fiber Equipment Solutions and Cellsite Backhaul references.
    *   **Nortel:** Historical context for confidential information regarding 6500 End-to-End Transport.
*   **Physical Topology:**
    *   **Cell Site to Headend:** Connected via `GE to cell site router` and `OME shelf` (CWDM technology).
    *   **Transport Path:** `10G protected traffic` flows East/West between the cell tower and transport switch.
    *   **Shelf Types:** Supports 2RU, 2-slot, 7-slot, 14-slot, and 32-slot configurations with AC/DC power options.
*   **Service Relationships:**
    *   **OTN Encapsulation:** Used on all services for consistent, networkable, and manageable deployments.
    *   **Layer Support:** Agnostic to Server Layer (Ethernet, OTN, SONET/

## Document Structure & Key Topics
- Visual & Network Diagram Intelligence (`metro case studies.pdf#page1`)
- Visual & Network Diagram Intelligence (`metro case studies.pdf#page19`)
- Visual & Network Diagram Intelligence (`metro case studies.pdf#page33`)

<!-- CORA-MAXIMIZED-COMMANDS-START -->
## Maximized Windows & Linux Command Examples for `metro case studies`

> **Domain Hub:** [[knowledge/09_hardware_uart_serial_oob_and_telecom_wan|Domain Hub 09: Hardware UART Serial OOB (tio /dev/ttyUSB0 & COM1), Metro Ethernet, MPLS/GMPLS, OTN, PON/GPON, SD-WAN, Wi-Fi & 2G/3G/4G/5G/SDR Cellular]]  
> **Master Playbooks:** [[commands/windows_master_command_playbook]] | [[commands/linux_master_command_playbook]] | [[commands/curl_playbook]] | [[commands/tio_serial_playbook]]  
> **When to Apply:** Apply whenever network connections to an appliance fail (`Exit 7` Connection Refused or `Exit 28` Timeout) and a hardware serial console (`/dev/ttyUSB0` or `COM1`) is available (`C1_OOB_SERIAL_LOOPBACK_APPLIANCE`), or when analyzing Carrier Metro Ethernet, MPLS/GMPLS labels, OTN/GPON optical links, SD-WAN tunnels, Wi-Fi 802.11, or 2G/3G/4G/5G cellular RAN protocols.  
> **15-Engine H-MDP State Transition:** `s_l2_l3_verified` $\xrightarrow{\text{OOB_Serial_Access}}$ `s_oob_serial_enumerated` | **Bayesian Root-Cause Triggers:** `service_bound_to_loopback, host_firewall_drop, wan_mpls_or_vlan_encapsulation_mismatch, uart_fifo_overrun_without_pacing` | **Isolation:** `RED, BLUE (Local USB UART `/dev/ttyUSB*` and `COM*` ports are permitted in RED and BLUE LAN+USB modes)`

| Primary Command (`Windows` / `Linux`) | OS / Shell | What It Does & Key Flags | When to Apply & Expected Output | Cross-Platform Equivalent |
| :--- | :--- | :--- | :--- | :--- |
| `tio -b 115200 -o 15 -O 120 --mute --script-run once --script 'write("\r"); msleep(400); while read(4096, 600) > 0 do end; exit(0)' /dev/ttyUSB0` | **Linux Bash (`tio 3.9`)** | Wakes the hardware UART console on `/dev/ttyUSB0` with 15ms char / 120ms line anti-drop pacing (`-o 15 -O 120`), reads the prompt (`login:` / `Password:` / `#`), and exits cleanly (`[[commands/tio_serial_playbook]]`). | Apply first when pivoting to OOB serial (`s_l2_l3_verified -> s_oob_serial_enumerated`) after TCP/HTTP probes fail (`Exit 7`/`28`). | `reg query HKLM\HARDWARE\DEVICEMAP\SERIALCOMM` |
| `tio -b 115200 -o 15 -O 120 --mute --script-run once --script 'write("\r"); msleep(300); write("ip -4 -br addr\r"); while read(4096, 600) > 0 do end; exit(0)' /dev/ttyUSB0` | **Linux Bash (`tio 3.9`)** | Executes a single paced command (`ip -4 -br addr`) over an authenticated `/dev/ttyUSB0` serial console without overflowing the 16-64 byte UART FIFO buffer. | Apply to inspect internal appliance interfaces, loopback bindings (`ss -tulpn`), and firewall rules (`iptables -L -n`) over OOB serial. | `plink.exe -serial COM1 -sercfg 115200,8,n,1,N` |
| `ls -la /dev/ttyUSB* /dev/ttyACM* /dev/serial/by-id/* 2>/dev/null && dmesg \| grep -iE 'ttyUSB\|ttyACM\|ftdi\|cp210\|pl2303\|ch341' \| tail -n 20` | **Linux Bash** | Enumerates all attached USB-to-UART serial adapters and inspects kernel driver binding logs. | Apply to discover available hardware serial ports and verify `/dev/ttyUSB*` group permissions (`dialout`). | `reg query HKLM\HARDWARE\DEVICEMAP\SERIALCOMM && mode` |
| `ip -d link show && ip -M route show` | **Linux Bash** | Displays detailed L2 encapsulation (`802.1Q` VLAN, `802.1ad` Q-in-Q Metro Ethernet S-TAG/C-TAG, VXLAN, GRE) and MPLS label forwarding entries (`ip -M route`) (`[[knowledge/trained_metro_ethernet_training_day_2_mpls]]`). | Apply when troubleshooting Metro Ethernet VLAN trunking or MPLS label-switched paths (`LSPs`). | `Get-NetAdapterAdvancedProperty` |
| `sudo tcpdump -ni <IFACE> -nn -e 'vlan or mpls'` | **Linux Bash** | Captures Ethernet frames carrying `802.1Q`/`802.1ad` VLAN tags (`0x8100`/`0x88a8`) or MPLS shim labels (`0x8847`/`0x8848`) (`[[knowledge/trained_intro_to_gmpls]]`). | Apply to discover hidden VLAN IDs or MPLS label stacks on trunk interfaces. | `pktmon start --capture --comp nics` |
| `iw dev && sudo iw dev <WLAN_IFACE> scan \| grep -E 'SSID:\|freq:\|signal:\|RSN:'` | **Linux Bash** | Lists 802.11 wireless interfaces (`iw dev`) and scans nearby Access Points for SSID, channel frequency, RSSI signal strength, and WPA2/WPA3 RSN ciphers (`[[knowledge/trained_wifi_handbook_1]]`). | Apply during wireless reconnaissance and RF channel auditing. | `netsh wlan show interfaces && netsh wlan show networks mode=bssid` |
| `nmcli device wifi list && nmcli connection show` | **Linux Bash** | Displays NetworkManager Wi-Fi BSSIDs, channels, bitrates, security bars, and configured VPN/SD-WAN profiles. | Apply on Linux laptops/appliances managed by NetworkManager. | `netsh wlan show profiles` |
| `ip xfrm state && ip xfrm policy && sudo wg show` | **Linux Bash** | Inspects kernel IPsec SA/SP security associations (`ip xfrm`) and WireGuard SD-WAN tunnel handshakes (`wg show`) (`[[knowledge/trained_software_defined_wide_area_network_sd-wan]]`). | Apply when troubleshooting SD-WAN or IPsec site-to-site tunnel encapsulation and MTU overhead (`Engine 2`). | `Get-VpnConnection && netsh advfirewall consec show rule name=all` |
| `rtl_test -t \|\| uhd_find_devices \|\| hackrf_info` | **Linux Bash (SDR)** | Detects attached Software Defined Radio (`SDR`) hardware (`RTL-SDR`, `USRP`, `HackRF`) for cellular (`GSM`/`LTE`/`5G`) spectrum analysis (`[[knowledge/trained_mobilehacking_with_sdr-4gand5g-final]]`). | Apply when auditing 2G/3G/4G/5G cellular basebands (`ARFCN`/`EARFCN`, `IMSI`/`TMSI`, `eNodeB`/`gNodeB` SIB broadcasts). | `usbipd list` |
| `tshark -r /tmp/cellular.pcap -Y "gsm_a or lte_rrc or nas-eps or ngap or s1ap"` | **Linux / Windows** | Filters telecom packet captures for 2G GSM-A, 4G LTE RRC / NAS-EPS / S1AP, and 5G NGAP signaling messages (`[[knowledge/trained_lteptclovwwp]]`). | Apply when analyzing cellular RAN/Core signaling pcaps (`GTP-U`, `S1AP`, `NGAP`, `Diameter`). | `tshark.exe -r C:\Temp\cellular.pcap -Y "s1ap or ngap or gtp"` |

### Copy-Pasteable Execution Block (Windows & Linux)
```bash
# [Linux Bash (`tio 3.9`)] Wakes the hardware UART console on `/dev/ttyUSB0` with 15ms char / 120ms line anti-drop pacing (`-o 15 -O 120`), reads the prompt (`login:` / `Password:` / `#`), and exits cleanly (`[[commands/tio_serial_playbook]]`).
tio -b 115200 -o 15 -O 120 --mute --script-run once --script 'write("\r"); msleep(400); while read(4096, 600) > 0 do end; exit(0)' /dev/ttyUSB0
# [Linux Bash (`tio 3.9`)] Executes a single paced command (`ip -4 -br addr`) over an authenticated `/dev/ttyUSB0` serial console without overflowing the 16-64 byte UART FIFO buffer.
tio -b 115200 -o 15 -O 120 --mute --script-run once --script 'write("\r"); msleep(300); write("ip -4 -br addr\r"); while read(4096, 600) > 0 do end; exit(0)' /dev/ttyUSB0
# [Linux Bash] Enumerates all attached USB-to-UART serial adapters and inspects kernel driver binding logs.
ls -la /dev/ttyUSB* /dev/ttyACM* /dev/serial/by-id/* 2>/dev/null && dmesg | grep -iE 'ttyUSB|ttyACM|ftdi|cp210|pl2303|ch341' | tail -n 20
# [Linux Bash] Displays detailed L2 encapsulation (`802.1Q` VLAN, `802.1ad` Q-in-Q Metro Ethernet S-TAG/C-TAG, VXLAN, GRE) and MPLS label forwarding entries (`ip -M route`) (`[[knowledge/trained_metro_ethernet_training_day_2_mpls]]`).
ip -d link show && ip -M route show
# [Linux Bash] Captures Ethernet frames carrying `802.1Q`/`802.1ad` VLAN tags (`0x8100`/`0x88a8`) or MPLS shim labels (`0x8847`/`0x8848`) (`[[knowledge/trained_intro_to_gmpls]]`).
sudo tcpdump -ni <IFACE> -nn -e 'vlan or mpls'
# [Linux Bash] Lists 802.11 wireless interfaces (`iw dev`) and scans nearby Access Points for SSID, channel frequency, RSSI signal strength, and WPA2/WPA3 RSN ciphers (`[[knowledge/trained_wifi_handbook_1]]`).
iw dev && sudo iw dev <WLAN_IFACE> scan | grep -E 'SSID:|freq:|signal:|RSN:'
```
<!-- CORA-MAXIMIZED-COMMANDS-END -->
