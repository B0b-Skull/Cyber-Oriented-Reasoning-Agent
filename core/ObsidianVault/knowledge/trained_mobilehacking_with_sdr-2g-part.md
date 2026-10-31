---
title: "Trained Knowledge & Topology: MobileHacking with SDR-2G-part"
category: knowledge
domain_hub: "[[knowledge/09_hardware_uart_serial_oob_and_telecom_wan]]"
os_platform: cross-platform
primary_tactic: OOB_Serial_Access
summary: "Operational architecture, decision workflows & Windows/Linux command reference for MobileHacking with SDR-2G-part: Non-interactive tio 3.9 Lua --script UART serial console automation (/dev/ttyUSB0, -o 15 -O 120 pacing), Windows COM port OOB acce"
when_to_apply: "Apply when working with MobileHacking with SDR-2G-part (cross-platform): Apply whenever network connections to an appliance fail (`Exit 7` Connection Refused or `Exit 28` Timeout) and a hardware serial console (`/dev/ttyUSB0` or `COM1`) is available (`C1_OOB_SERIAL_LOOPBACK_APPLIANCE`), or when analyzing Carrier Metro Ethernet, MPLS/GMPLS labels, OTN/GPON optical links, SD-WAN tunnels, Wi-Fi 802.11, or 2G/3G/4G/5G cellular RAN protocols."
tags: [cve-2012-6636, cve-2013-4710, docker, enumeration, https, mdp, pdf, trained, wireshark, linux, windows, tio, serial, ttyusb0, ttyusb1, com1, uart, oob, oob_serial_access, mpls, gmpls, metro_ethernet]
source_file: "MobileHacking with SDR-2G-part"
updated: 2026-10-30
---

# Trained Knowledge & Architecture: `MobileHacking_with_SDR-2G-part.pdf`

- **Source Path:** `~/Projects/CORA/Training/MobileHacking_with_SDR-2G-part.pdf` (`pdf`)
- **Extracted Technical Entities:** `cve-2012-6636, cve-2013-4710, docker, https, wireshark`
- **Extracted IPs / Subnets:** `None`
- **Extracted Interfaces:** `None`
- **Linked Command Playbook:** [[commands/trained_mobilehacking_with_sdr-2g-part]] (`1` CEGAR-verified commands | `1` MDP transitions)

## Command & Tactic Coverage Summary
- **Total CEGAR-Verified Commands:** `1` (full executable list in [[commands/trained_mobilehacking_with_sdr-2g-part]])
- **Tactic Distribution:** `Enumeration` (1)
- **Top Extracted CLI Tools:** `python` (1)

### Visual & Network Diagram Intelligence (`MobileHacking_with_SDR-2G-part.pdf#page1`)
- **Spatially Grouped Diagram Nodes (Box/Component Clusters):**
  1. `[penthertz]`
  2. `[Mobile Hacking | 2G part]`

### Visual & Network Diagram Intelligence (`MobileHacking_with_SDR-2G-part.pdf#page4`)
- **Spatially Grouped Diagram Nodes (Box/Component Clusters):**
  1. `[Introduction]`

### Visual & Network Diagram Intelligence (`MobileHacking_with_SDR-2G-part.pdf#page8`)
- **Spatially Grouped Diagram Nodes (Box/Component Clusters):**
  1. `[Introduction | Evolution]`
  2. `[Mobile network → more than 40 years]`
  3. `[1G-TACS/AMPS]`
  4. `[2G-GSM/GPRS/EDGE | 3G-WCDMA/UMTS/HSPA/HSPA+]`
  5. `[4G-LTE/LTEAdvanced/LTEAdvancedPro | 2010]`
  6. `[Research | Industry | 1980]`
  7. `[5G-LTE/5G-NR | 2020 | 2030]`
  8. `[1990 | 2000]`
  9. `[penthertz.com]`
  10. `[penthertz 1 8]`

## LLM Distilled Operational Summary
### Operational Techniques & Decision Workflows
- **Threat Modeling**: Identify risks associated with Over-The-Air (OTA) attacks including eavesdropping, replay, injection, relay, jamming, and Denial-of-Service (DoS) via high-amplitude transmission.
- **Target Scope Definition**: Focus on access controls, mobile phones, navigation systems, autonomous vehicles, and industrial IoT components.
- **Regulatory Compliance Check**: Verify frequency band licensing requirements (e.g., ANFR, FCC) before deploying transmitters, noting exemptions for specific equipment like Wi-Fi or telemetry.
- **Technology Selection**: Choose between circuit-switched (GSM) and packet-switched (GPRS/EDGE) networks based on the target's service type, acknowledging that radio physics remain similar across 2G variants.

### Critical Command Patterns & Concepts
- **Modulation & Multiplexing**: Utilize GMSK modulation for standard 2G/2.5G and 8PSK for EDGE. Apply Frequency Division Multiple Access (FDMA) combined with Time-Division Multiple Access (TDMA) within 25 MHz bandwidths.
- **TDMA Frame Structure**: Configure signals into frames of 8 timeslots, where each time-slot contains 156.25 symbols at a transmission rate of 270.83 kbits/s.
- **Logical Channel Interactions**:
  - *Broadcast Channels*: Use FCCH for oscillator tuning, SCH for frame synchronization (BSIC), and BCCH for network identity (MCC/MNC/CGI) verification against SIM data.
  - *Common Control Channels*: Monitor PCH for incoming calls, RACH for mobile-originated requests, AGCH for access grants, and CBCH for cell broadcast messages.
  - *Dedicated Control Channels*: Leverage SDCCH for call setup and SACCH for control/supervisory signaling.

### Network Topology & Relationships
- **Global vs. Regional Standards**: While GSM/GPRS/EDGE/EGPRS are worldwide, the US utilizes CDMA. European implementations specifically use GMSK modulation and FDMA/TDMA multiplexing.
- **Evolutionary Timeline**: The mobile network has evolved from 1G (TACS/AMPS) through 2G (GSM), 3G (WCDMA/UMTS), 4G (LTE), to 5G (NR), spanning from the 1980s to the 2030s.
- **Device-Network Interaction**: The Mobile Station (MS) must successfully tune to the RF carrier (via FCCH), synchronize to the physical slot (via SCH), and verify network identity (via BCCH/SIM comparison) before establishing a connection.

## Document Structure & Key Topics
- Visual & Network Diagram Intelligence (`MobileHacking_with_SDR-2G-part.pdf#page1`)
- Visual & Network Diagram Intelligence (`MobileHacking_with_SDR-2G-part.pdf#page4`)
- Visual & Network Diagram Intelligence (`MobileHacking_with_SDR-2G-part.pdf#page8`)
- associating attacker IMSI with a resident number

## Extracted Operational Steps & Workflows
- 1. Get the TMSI of the victim
- 2. Analyze the cell you and the victim are camping on
- 3. Capture traffic and use the results of your analysis to construct
- 4. Use Kraken to crack the key
- 5. Use the key to decode the data you captured

<!-- CORA-MAXIMIZED-COMMANDS-START -->
## Maximized Windows & Linux Command Examples for `MobileHacking with SDR-2G-part`

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
