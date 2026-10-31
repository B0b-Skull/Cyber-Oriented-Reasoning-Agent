---
title: "Trained Knowledge & Topology: Software Defined Wide Area Network (SD-WAN)"
category: knowledge
domain_hub: "[[knowledge/09_hardware_uart_serial_oob_and_telecom_wan]]"
os_platform: cross-platform
primary_tactic: OOB_Serial_Access
summary: "Operational architecture, decision workflows & Windows/Linux command reference for Software Defined Wide Area Network (SD-WAN): Non-interactive tio 3.9 Lua --script UART serial console automation (/dev/ttyUSB0, -o 15 -O 120 pacing), Windows COM port OOB acce"
when_to_apply: "Apply when working with Software Defined Wide Area Network (SD-WAN) (cross-platform): Apply whenever network connections to an appliance fail (`Exit 7` Connection Refused or `Exit 28` Timeout) and a hardware serial console (`/dev/ttyUSB0` or `COM1`) is available (`C1_OOB_SERIAL_LOOPBACK_APPLIANCE`), or when analyzing Carrier Metro Ethernet, MPLS/GMPLS labels, OTN/GPON optical links, SD-WAN tunnels, Wi-Fi 802.11, or 2G/3G/4G/5G cellular RAN protocols."
tags: [http, https, mdp, pdf, ssl, trained, vlan, linux, windows, tio, serial, ttyusb0, ttyusb1, com1, uart, oob, oob_serial_access, mpls, gmpls, metro_ethernet, otn, gpon]
source_file: "Software Defined Wide Area Network (SD-WAN)"
updated: 2026-10-30
---

# Trained Knowledge & Architecture: `Software Defined Wide Area Network (SD-WAN).pdf`

- **Source Path:** `~/Projects/CORA/Training/Software Defined Wide Area Network (SD-WAN).pdf` (`pdf`)
- **Extracted Technical Entities:** `http, https, ssl, vlan`
- **Extracted IPs / Subnets:** `1.2.3.4, 5.6.7.8`
- **Extracted Interfaces:** `vlan1`

### Visual & Network Diagram Intelligence (`Software Defined Wide Area Network (SD-WAN).pdf#page19`)
- **Spatially Grouped Diagram Nodes (Box/Component Clusters):**
  1. `[Scope of NFV and OpenFlow/SDN | VirtualizevalueaddednetworkfunctionsoncommodityPCs | (thatarenormallyimplemented onspecializedhardware)]`
  2. `[Application | program | Server mngt. | software | NWmanagement]`
  3. `[Application | program | Server mngt. | software | NWmanagement]`
  4. `[Application | program | Server mngt. | software | NW management]`
  5. `[NW | Functions | Virtualiz.]`
  6. `[SW | Equipment/ | Server+software]`
  7. `[software | OpenFlow | controller | OpenFlow | switch]`
  8. `[software | Router | switch]`
  9. `[software | Otherarchitecture | NWequipment]`
  10. `[VDPI | VNAT | VBRAS | Other | architecture]`
  11. `[HW]`
  12. `[OpenFlow | architecture]`
  13. `[Legacy | architecture | High speed network functions onvirtualized commodity | hardware:optimized dataplane undervirtualization]`
  14. `[Source: NEC]`

## LLM Distilled Operational Summary
### 1. Key Operational Techniques & Decision Workflows
*   **Decoupling Control from Data**: Shift from classical distributed control planes (using OSPF, IS-IS, BGP) to a centralized software controller that manages the network logic independently of the underlying hardware.
*   **Virtualization of Network Functions (NFV)**: Migrate specialized network functions (e.g., VBRAS, VNAT, V DPI) from dedicated hardware appliances to commodity PCs using virtualization layers.
*   **OpenFlow Protocol Implementation**: Utilize OpenFlow as the standard interface to remotely control routing tables and construct a logical map of the network across multi-vendor hardware and ASICs.
*   **Three-Plane Architecture Management**:
    *   **Application Plane**: Hosts management software for server and network administration.
    *   **Control Plane**: Managed via open-source implementations like OpenDaylight to handle decision-making logic.
    *   **Data Plane**: Simplified hardware focused solely on packet forwarding, guided by the controller.

### 2. Critical Command Patterns & Required Flags
*   **Controller Communication**: Use **OpenFlow** as the primary data plane interface to interact with the control plane.
*   **API Integration**: Leverage **Northbound APIs** to allow applications to interact with the SDN controller for policy enforcement and automation.
*   **Hardware Abstraction**: Deploy **Well-defined open APIs** to construct a logical network map, ensuring vendor-agnostic operation.

### 3. Network Topology & Component Relationships
*   **Logical Map Construction**: The SDN controller constructs a unified logical map of the network, abstracting the physical topology into manageable software entities.
*   **Component Clusters**:
    *   **Virtualized Functions**: Includes V DPI (Deep Packet Inspection), VNAT (Virtual Network Address Translation), and VBRAS (Virtual Broadband Remote Access Server).
    *   **Hardware Layers**: Ranges from specialized packet forwarding hardware to simple forwarding hardware and commodity PCs.
    *   **Software Layers**: Encompasses network operating systems (Network OS), application management software, and OpenFlow controllers.
*   **Architecture Evolution**: Transition from vertically integrated, specialized hardware architectures to flexible, software-defined architectures optimized for virtualization and high-speed dataplanes.

## Document Structure & Key Topics
- Visual & Network Diagram Intelligence (`Software Defined Wide Area Network (SD-WAN).pdf#page19`)

## Extracted Operational Steps & Workflows
- 1. Forward packet to port(s)
- 2. Encapsulate and forward to controller
- 3. Drop packet
- 4. Send to normal processing pipeline
- 1. Open interface to packet forwarding
- 3. Well-defined open API
- 2. At least one Network OS
- 1.
Forward packet to port(s)
- 2.
Encapsulate and forward to
- 3.
Drop packet
- 4.
Send to normal processing pipeline
- 1. Packet
- 2. Byte counters

<!-- CORA-MAXIMIZED-COMMANDS-START -->
## Maximized Windows & Linux Command Examples for `Software Defined Wide Area Network (SD-WAN)`

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
