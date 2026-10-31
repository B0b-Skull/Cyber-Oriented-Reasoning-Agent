---
title: "Trained Knowledge & Topology: Metro Ethernet Training Day 2 MPLS"
category: knowledge
domain_hub: "[[knowledge/09_hardware_uart_serial_oob_and_telecom_wan]]"
os_platform: cross-platform
primary_tactic: OOB_Serial_Access
summary: "Operational architecture, decision workflows & Windows/Linux command reference for Metro Ethernet Training Day 2 MPLS: Non-interactive tio 3.9 Lua --script UART serial console automation (/dev/ttyUSB0, -o 15 -O 120 pacing), Windows COM port OOB acce"
when_to_apply: "Apply when working with Metro Ethernet Training Day 2 MPLS (cross-platform): Apply whenever network connections to an appliance fail (`Exit 7` Connection Refused or `Exit 28` Timeout) and a hardware serial console (`/dev/ttyUSB0` or `COM1`) is available (`C1_OOB_SERIAL_LOOPBACK_APPLIANCE`), or when analyzing Carrier Metro Ethernet, MPLS/GMPLS labels, OTN/GPON optical links, SD-WAN tunnels, Wi-Fi 802.11, or 2G/3G/4G/5G cellular RAN protocols."
tags: [enumeration, eth0, eth1, mdp, passive_enum, pdf, trained, linux, windows, tio, serial, ttyusb0, ttyusb1, com1, uart, oob, oob_serial_access, mpls, gmpls, metro_ethernet, vlan, otn]
source_file: "Metro Ethernet Training Day 2 MPLS"
updated: 2026-10-30
---

# Trained Knowledge & Architecture: `Metro Ethernet Training_Day_2_MPLS.pdf`

- **Source Path:** `~/Projects/CORA/Training/Metro Ethernet Training_Day_2_MPLS.pdf` (`pdf`)
- **Extracted Technical Entities:** `eth0, eth1`
- **Extracted IPs / Subnets:** `10.1.0.0/24, 10.1.2.0/24, 10.2.1.0/24, 10.2.12.0/24, 10.22.12.0/24, 10.3.0.0/16, 10.3.1.0/24, 10.3.3.0/24, 10.4.12.0/24, 134.5.1.5, 134.5.6.1, 137.204.0.0/16, 149.27.2.0/24, 149.27.2.27, 172.16.1.0, 172.26.1.0, 192.4.2.10, 197.26.15.0/24, 197.26.15.1, 197.26.15.1/32, 20.1.0.0/16, 20.2.0.0/16, 20.2.1.0/28, 20.2.1.2, 20.2.1.2/28, 200.3.2.1, 200.3.2.7, 30.0.0.2, 30.1.1.0/28, 47.1.1.1`
- **Extracted Interfaces:** `eth0, eth1`
- **Linked Command Playbook:** [[commands/trained_metro_ethernet_training_day_2_mpls]] (`4` CEGAR-verified commands | `4` MDP transitions)

## Command & Tactic Coverage Summary
- **Total CEGAR-Verified Commands:** `4` (full executable list in [[commands/trained_metro_ethernet_training_day_2_mpls]])
- **Tactic Distribution:** `Passive_Enum` (3), `Enumeration` (1)
- **Top Extracted CLI Tools:** `ip` (3), `new-generation` (1)

### Visual & Network Diagram Intelligence (`Metro Ethernet Training_Day_2_MPLS.pdf#page1`)
- **Spatially Grouped Diagram Nodes (Box/Component Clusters):**
  1. `[TONEX]`
  2. `[METRO ETHERNET]`
  3. `[PART 2]`

### Visual & Network Diagram Intelligence (`Metro Ethernet Training_Day_2_MPLS.pdf#page4`)
- **Spatially Grouped Diagram Nodes (Box/Component Clusters):**
  1. `[QUESTION AND ANSWER]`
  2. `[Q&A]`

### Visual & Network Diagram Intelligence (`Metro Ethernet Training_Day_2_MPLS.pdf#page5`)
- **Spatially Grouped Diagram Nodes (Box/Component Clusters):**
  1. `[INTRODUCTION TO MPLS]`

## LLM Distilled Operational Summary
### Operational Techniques & Decision Workflows
*   **Layer 2.5 Forwarding Logic**: Decide to operate between OSI Layer 2 and 3 to combine data link switching performance with network layer routing scalability.
*   **Flow Setup & Signaling**: Execute a flow setup process using signaling protocols (e.g., RSVP) before forwarding traffic, as MPLS requires explicit path establishment.
*   **Recursive Label Lookup**: Perform recursive lookups on next-hop addresses to resolve VPN labels from MP-BGP announcements, linking them to specific egress interfaces on originating Provider Routers (PR).
*   **Hierarchical Domain Forwarding**: Utilize label stacking (LIFO) to manage multiple forwarding domains, where higher-level labels aggregate LSPs into tunnels.
*   **Traffic Engineering (TE)**: Apply MPLS to steer traffic along specific paths defined by RSVP TE tunnels, distinct from standard L3 routing tables.

### Critical Command Patterns & Required Flags
*   **Label Format Structure**: Ensure the 32-bit MPLS header contains:
    *   **Label Value (20 bits)**: The actual forwarding label.
    *   **Exp (3 bits)**: Experimental/CoS bits for service class identification.
    *   **S (Stacking Bit, 1 bit)**: Set to `1` if no further labels exist beneath; set to `0` for stacked labels.
    *   **TTL (8 bits)**: Time-to-live value (often initialized to 255 in specific network contexts like GX).
*   **Header Placement**: Insert the MPLS header between the Data-Link (L2) and IP (L3) headers.
*   **Tagging Operations**: Perform "Tag in" at the Ingress Provider Edge (PE) and "Tag out" at the Egress PE, ensuring the label stack is maintained across core routers (P).

### Network Topology & Relationships
*   **Device Roles**:
    *   **PE (Provider Edge)**: Handles ingress/egress tagging, recursive label lookups, and POP (Pop of Packet) operations for VPN labels.
    *   **P (Provider Core)**: Performs label swapping based on the top label without inspecting L3 headers.
*   **Protocol Support**: Compatible with ATM, FR, Ethernet (L2), and all L3 protocols.
*   **Topology Types**: Supports Virtual Private Networking (VPN) and Multi-Protocol Label Switching (MPLS) across Metro Ethernet and Optical/DWDM environments.
*   **Routing Interaction**: MPLS paths may differ from L3 forwarding paths; the "Path Label" is derived from RSVP TE tunnels to the originating PR device.

## Document Structure & Key Topics
- Visual & Network Diagram Intelligence (`Metro Ethernet Training_Day_2_MPLS.pdf#page1`)
- Visual & Network Diagram Intelligence (`Metro Ethernet Training_Day_2_MPLS.pdf#page4`)
- Visual & Network Diagram Intelligence (`Metro Ethernet Training_Day_2_MPLS.pdf#page5`)

<!-- CORA-MAXIMIZED-COMMANDS-START -->
## Maximized Windows & Linux Command Examples for `Metro Ethernet Training Day 2 MPLS`

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
