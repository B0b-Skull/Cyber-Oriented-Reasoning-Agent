---
title: "Trained Knowledge & Topology: Metro Ethernet Training Part 1"
category: knowledge
domain_hub: "[[knowledge/09_hardware_uart_serial_oob_and_telecom_wan]]"
os_platform: cross-platform
primary_tactic: OOB_Serial_Access
summary: "Operational architecture, decision workflows & Windows/Linux command reference for Metro Ethernet Training Part 1: Non-interactive tio 3.9 Lua --script UART serial console automation (/dev/ttyUSB0, -o 15 -O 120 pacing), Windows COM port OOB acce"
when_to_apply: "Apply when working with Metro Ethernet Training Part 1 (cross-platform): Apply whenever network connections to an appliance fail (`Exit 7` Connection Refused or `Exit 28` Timeout) and a hardware serial console (`/dev/ttyUSB0` or `COM1`) is available (`C1_OOB_SERIAL_LOOPBACK_APPLIANCE`), or when analyzing Carrier Metro Ethernet, MPLS/GMPLS labels, OTN/GPON optical links, SD-WAN tunnels, Wi-Fi 802.11, or 2G/3G/4G/5G cellular RAN protocols."
tags: [arp, enumeration, http, https, mdp, passive_enum, pdf, ssl, tls, trained, vlan, linux, windows, tio, serial, ttyusb0, ttyusb1, com1, uart, oob, oob_serial_access, mpls]
source_file: "Metro Ethernet Training Part 1"
updated: 2026-10-30
---

# Trained Knowledge & Architecture: `Metro Ethernet Training_Part_1.pdf`

- **Source Path:** `~/Projects/CORA/Training/Metro Ethernet Training_Part_1.pdf` (`pdf`)
- **Extracted Technical Entities:** `arp, http, https, ssl, tls, vlan`
- **Extracted IPs / Subnets:** `1.0.0.0, 1.1.1.2/32, 1.1.1.4/32, 10.0.0.0/30, 127.255.255.255, 128.0.0.0, 191.255.255.255, 192.0.0.0, 223.255.255.255, 224.0.0.0, 239.255.255.255, 240.0.0.0, 255.255.255.255, 6.3.1.2`
- **Extracted Interfaces:** `LO, Lo`
- **Linked Command Playbook:** [[commands/trained_metro_ethernet_training_part_1]] (`4` CEGAR-verified commands | `4` MDP transitions)

## Command & Tactic Coverage Summary
- **Total CEGAR-Verified Commands:** `4` (full executable list in [[commands/trained_metro_ethernet_training_part_1]])
- **Tactic Distribution:** `Enumeration` (3), `Passive_Enum` (1)
- **Top Extracted CLI Tools:** `locate` (2), `ip` (1), `out-of-band` (1)

### Visual & Network Diagram Intelligence (`Metro Ethernet Training_Part_1.pdf#page1`)
- **Spatially Grouped Diagram Nodes (Box/Component Clusters):**
  1. `[TONEX]`
  2. `[METROETHERNET]`
  3. `[PART 1]`

### Visual & Network Diagram Intelligence (`Metro Ethernet Training_Part_1.pdf#page5`)
- **Spatially Grouped Diagram Nodes (Box/Component Clusters):**
  1. `[METROETHERNET | BASICS]`
  2. `[T]`

### Visual & Network Diagram Intelligence (`Metro Ethernet Training_Part_1.pdf#page9`)
- **Spatially Grouped Diagram Nodes (Box/Component Clusters):**
  1. `[THEMETROBOTTLENECK]`
  2. `[Other Sites]`
  3. `[Access]`
  4. `[Metro]`
  5. `[Core Network]`
  6. `[End User]`
  7. `[Access]`
  8. `[Metro]`
  9. `[Core]`

## LLM Distilled Operational Summary
### Operational Techniques & Decision Workflows
- **Service Selection Logic**: Evaluate cost-effectiveness, flexibility, and simplicity when selecting Ethernet services for business, residential, or mobile subscribers.
- **Network Scope Differentiation**: Distinguish between **Metro Ethernet** (point-to-point/multipoint over a MAN) and **Carrier Ethernet** (versatile, evolved scope including MAN/WAN infrastructure).
- **Architecture Design Principles**: Apply the "SIMPLE, SCALABLE, AUTOMATABLE" triad when designing fabric networks (CLOS, Metro/Access, Core).
- **Protocol Hierarchy Implementation**:
  - **Access Layer**: Utilize IS-IS L1 for fixed/mobile access networks.
  - **Aggregation Layer**: Deploy IS-IS L2 for routing within aggregation networks.
  - **Core Layer**: Implement eBGP/iBGP with IPv4+label stacks for hierarchical LSPs and peering fabrics.
- **BGP Configuration Workflow**: Configure `next-hop-self` on Provider Autonomous System Border Routers (ASBRs) and Route Reflectors (RRs) to ensure proper route propagation in hierarchical MPLS environments.

### Critical Command Patterns & Required Flags
- **BGP Next-Hop Self**:
  - Context: Provider Edge (PE) or ASBR interfaces connecting to customer sites.
  - Pattern: `neighbor <IP> next-hop-self`
  - Purpose: Ensures the next-hop attribute remains reachable for downstream routers in iBGP/eBGP hierarchies.
- **Protocol Selection**:
  - Access/Mobile Aggregation: `protocol isis level-1`
  - Core/Aggregation Interconnect: `protocol isis level-2` or `protocol bgp` (depending on LSP type: iBGP or eBGP).

### Network Topology & Relationships
- **Logical Layers**:
  - **End User**: Connects via Access networks.
  - **Access Network**: Typically IS-IS L1 (Fixed/Mobile).
  - **Metro/Aggregation Network**: IS-IS L2 or MPLS LDP/LSP.
  - **Core Network**: eBGP/iBGP with hierarchical LSPs; includes Peering Fabrics.
- **Key Components**:
  - **UNI (User-Network Interface)**: The demarcation point between the service provider and the customer (e.g., 256 Kb to 10 Gbps Ethernet).
  - **FABRIC DESIGNS**: CLOS fabrics for Metro/Access and Core fabrics for scalability.
  - **BGP Roles**:
    - **CN-ASBR**: Core Network AS Border Router.
    - **AGN-ASBR**: Aggregation Network AS Border Router.
    - **RR (Route Reflector)**: Used for iBGP scale (CN-RR, AGN-RR, Inline RR).
- **Transport Technologies**: Frame Relay (legacy/connected branches), Fast Ethernet, and 10 Gbps Ethernet.

## Document Structure & Key Topics
- Visual & Network Diagram Intelligence (`Metro Ethernet Training_Part_1.pdf#page1`)
- Visual & Network Diagram Intelligence (`Metro Ethernet Training_Part_1.pdf#page5`)
- Visual & Network Diagram Intelligence (`Metro Ethernet Training_Part_1.pdf#page9`)

## Extracted Operational Steps & Workflows
- 3. In the middle of the wire between
- 1. At the port of the service provider equipment
- 2. At the port of the customer’s equipment
- 1.
Point to Point EVC: each EVC associates
- 2.
Multipoint to Multipoint EVC: each EVC
- 3.
Rooted Multipoint EVC : each EVC
- 4. In general, E-NNI is represented by the physical Ethernet port on the service provider access

<!-- CORA-MAXIMIZED-COMMANDS-START -->
## Maximized Windows & Linux Command Examples for `Metro Ethernet Training Part 1`

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
