---
title: "Trained Knowledge & Topology: MobileHacking with SDR-4Gand5G-final"
category: knowledge
domain_hub: "[[knowledge/09_hardware_uart_serial_oob_and_telecom_wan]]"
os_platform: cross-platform
primary_tactic: OOB_Serial_Access
summary: "Operational architecture, decision workflows & Windows/Linux command reference for MobileHacking with SDR-4Gand5G-final: Non-interactive tio 3.9 Lua --script UART serial console automation (/dev/ttyUSB0, -o 15 -O 120 pacing), Windows COM port OOB acce"
when_to_apply: "Apply when working with MobileHacking with SDR-4Gand5G-final (cross-platform): Apply whenever network connections to an appliance fail (`Exit 7` Connection Refused or `Exit 28` Timeout) and a hardware serial console (`/dev/ttyUSB0` or `COM1`) is available (`C1_OOB_SERIAL_LOOPBACK_APPLIANCE`), or when analyzing Carrier Metro Ethernet, MPLS/GMPLS labels, OTN/GPON optical links, SD-WAN tunnels, Wi-Fi 802.11, or 2G/3G/4G/5G cellular RAN protocols."
tags: [adb, cve-2012-6636, cve-2013-4710, enumeration, http, https, mdp, passive_enum, pdf, serial, tls, trained, ttyusb1, linux, windows, tio, ttyusb0, com1, uart, oob, oob_serial_access, mpls]
source_file: "MobileHacking with SDR-4Gand5G-final"
updated: 2026-10-30
---

# Trained Knowledge & Architecture: `MobileHacking_with_SDR-4Gand5G-final.pdf`

- **Source Path:** `~/Projects/CORA/Training/MobileHacking_with_SDR-4Gand5G-final.pdf` (`pdf`)
- **Extracted Technical Entities:** `adb, cve-2012-6636, cve-2013-4710, http, https, serial, tls, ttyusb1`
- **Extracted IPs / Subnets:** `127.0.1.1, 127.0.1.100, 127.0.1.200, 172.16.0.2`
- **Extracted Interfaces:** `ttyUSB1, ttyUSB2`
- **Linked Command Playbook:** [[commands/trained_mobilehacking_with_sdr-4gand5g-final]] (`3` CEGAR-verified commands | `3` MDP transitions)

## Command & Tactic Coverage Summary
- **Total CEGAR-Verified Commands:** `3` (full executable list in [[commands/trained_mobilehacking_with_sdr-4gand5g-final]])
- **Tactic Distribution:** `Enumeration` (2), `Passive_Enum` (1)
- **Top Extracted CLI Tools:** `lte` (1), `nr` (1), `type` (1)

### Visual & Network Diagram Intelligence (`MobileHacking_with_SDR-4Gand5G-final.pdf#page1`)
- **Spatially Grouped Diagram Nodes (Box/Component Clusters):**
  1. `[penthertz]`
  2. `[Mobile Hacking with]`
  3. `[SDR | 3G - 5G]`

### Visual & Network Diagram Intelligence (`MobileHacking_with_SDR-4Gand5G-final.pdf#page2`)
- **Spatially Grouped Diagram Nodes (Box/Component Clusters):**
  1. `[3G Radio]`

## LLM Distilled Operational Summary
### Operational Techniques & Decision Workflows
- **Modulation Selection Workflow**: Select modulation based on channel quality and generation:
  - **3G (UMTS)**: Default QPSK; upgrade to 16QAM (HSDPA) or 64QAM (HSDPA+) for high-speed data.
  - **4G (LTE)**: Scale from QPSK to 256/1024 QAM based on signal-to-noise ratio measurements.
  - **5G**: Support QPSK through 1024 QAM (Rel. 17) with CP-OFDM for downlink and DFT-s-OFDM for uplink.
- **Multiplexing Strategy**:
  - **Downlink**: Use OFDMA (4G) or CP-OFDM (5G) for high spectral efficiency.
  - **Uplink**: Prefer SC-FDMA (4G) or DFT-s-OFDM (5G) to minimize Peak-to-Average Power Ratio (PAPR).
- **Architecture Evolution**:
  - **5G NSA**: Retain legacy EPC core for backward compatibility.
  - **5G SA**: Deploy Software-Defined Network (SDN) with CUPS architecture for dynamic resource allocation and reduced OPEX.
- **Security Hardening**:
  - **3G Encryption**: Upgrade from vulnerable A5/1 or A5/2 to A5/3 (KASUMI, 128-bit key).
  - **GPRS Encryption**: Migrate from GEA0/GEA1 to GEA2 for enhanced stream cipher security.

### Critical Command Patterns & Required Flags
- **Signal Analysis Commands**:
  - `sdr# fft_view`: Trigger FFT visualization to inspect frequency domain occupancy.
  - `sdr# modulation_check`: Verify active modulation (QPSK/16QAM/64QAM) against expected standards.
- **Resource Block Configuration**:
  - `sdr# prb_config`: Set Physical Resource Block parameters (12 sub-carriers, 7 symbols normal CP).
  - `sdr# bandwidth_set`: Configure carrier width (e.g., 5 MHz for LTE, 25 MHz for 5G FDMA).
- **Security Mode Command**:
  - `bts# cipher_mode_cmd`: Instruct Base Transceiver Station to switch encryption algorithms (e.g., `A5/3` or `GEA2`).

### Network Topology & Service Relationships
- **3G Topology**: UMTS (Europe) / CDMA2000 (US); WCDMA spread spectrum with OVSF coding trees.
- **4G Topology**: LTE/E-UTRA with FDD (paired spectrum + diplexer) or TDD (shared timeslot) modes.
- **5G Topology**:
  - **NSA**: Integrated with 4G EPC core.
  - **SA**: Service-Based Architecture (SBA) involving UPF, SMF, PCF, AMF, and UDR functions.
- **Key Interfaces**: N1 (NAS signaling), N2 (Control Plane), N3 (User Plane) between UE and Core Network Functions.
- **Open

## Document Structure & Key Topics
- Visual & Network Diagram Intelligence (`MobileHacking_with_SDR-4Gand5G-final.pdf#page1`)
- Visual & Network Diagram Intelligence (`MobileHacking_with_SDR-4Gand5G-final.pdf#page2`)
- eNB
- gNB
- echo -e 'AT+QLINUXCMD="/sbin/getty -L ttyGS0 115200
- microcom /dev/ttyUSB1

<!-- CORA-MAXIMIZED-COMMANDS-START -->
## Maximized Windows & Linux Command Examples for `MobileHacking with SDR-4Gand5G-final`

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
