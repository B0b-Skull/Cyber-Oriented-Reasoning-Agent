---
title: "Trained Knowledge & Topology: WiFi Handbook 1"
category: knowledge
domain_hub: "[[knowledge/09_hardware_uart_serial_oob_and_telecom_wan]]"
os_platform: cross-platform
primary_tactic: OOB_Serial_Access
summary: "Operational architecture, decision workflows & Windows/Linux command reference for WiFi Handbook 1: Non-interactive tio 3.9 Lua --script UART serial console automation (/dev/ttyUSB0, -o 15 -O 120 pacing), Windows COM port OOB acce"
when_to_apply: "Apply when working with WiFi Handbook 1 (cross-platform): Apply whenever network connections to an appliance fail (`Exit 7` Connection Refused or `Exit 28` Timeout) and a hardware serial console (`/dev/ttyUSB0` or `COM1`) is available (`C1_OOB_SERIAL_LOOPBACK_APPLIANCE`), or when analyzing Carrier Metro Ethernet, MPLS/GMPLS labels, OTN/GPON optical links, SD-WAN tunnels, Wi-Fi 802.11, or 2G/3G/4G/5G cellular RAN protocols."
tags: [mdp, pdf, trained, linux, windows, tio, serial, ttyusb0, ttyusb1, com1, uart, oob, oob_serial_access, mpls, gmpls, metro_ethernet, vlan, otn, gpon, sd-wan, wifi, lte]
source_file: "WiFi Handbook 1"
updated: 2026-10-30
---

# Trained Knowledge & Architecture: `WiFi_Handbook_1.pdf`

- **Source Path:** `~/Projects/CORA/Training/WiFi_Handbook_1.pdf` (`pdf`)
- **Extracted Technical Entities:** `general`
- **Extracted IPs / Subnets:** `None`
- **Extracted Interfaces:** `None`

### Visual & Network Diagram Intelligence (`WiFi_Handbook_1.pdf#page3`)
- **Spatially Grouped Diagram Nodes (Box/Component Clusters):**
  1. `[CHAPTER | 1]`
  2. `[Introduction]`

## Document Structure & Key Topics
- Visual & Network Diagram Intelligence (`WiFi_Handbook_1.pdf#page3`)

## Extracted Operational Steps & Workflows
- 1. IEEE 802.11 (Standard)
- 2. Internet service providers—Standards.
- 3. Telecommuncation—Technological innovations—United States.

## Extracted Reference Excerpt
--- [Page 1] ---
Wi-Fi
Handbook
Building 802.11b
Wireless Networks
Frank Ohrtman
Konrad Roeder
McGraw-Hill
New York
Chicago
San Francisco
Lisbon
London
Madrid
Mexico City
Milan
New Delhi
San Juan
Seoul
Singapore
Sydney
Toronto

--- [Page 2] ---
Library of Congress Cataloging-in-Publication Data
Ohrtman, Frank.
Wi-Fi handbook: building 802.11b wireless networks / Frank Ohrtman,
Konrad Roeder.
p.
cm.
Includes Index
ISBN 0-07-141251-4 (alk. paper)
1. IEEE 802.11 (Standard)
2. Internet service providers—Standards.
3. Telecommuncation—Technological innovations—United States.
I. Roeder, Konrad.
II. Title
TK5105.5668.036
2003
004.67'8—dc21                                           
2003044574 
Information contained in this work has been obtained by The McGraw-Hill
Companies, Inc. (“McGraw-Hill”) from sources believed to be reliable. However,
neither McGraw-Hill nor its authors guarantee the accuracy or completeness of
any information published herein, and neither McGraw-Hill nor its authors
shall be responsible for any errors, omissions, or damages arising out of use of
this information.This work is published with the understanding that McGraw-
Hill and its authors are supplying information but are not attempting to render
engineering or other professional services. If such services are required, the
assistance of an appropriate professional should be sought.
Copyright © 2003 by The McGraw-Hill Companies, Inc. All rights reserved.
Printed in the United States of America. Except as permitted under the United
States Copyright Act of 1976, no part of this publication may be reproduced or
distributed in any form or by any means, or stored in a data base or retrieval
system, without the prior written permission of the publisher.
1 2 3 4 5 6 7 8 9 0
DOC/DOC
0 9 8 7 6 5 4 3
ISBN 0-07-141251-4
The sponsoring editor for this book was Stephen S. Chapman and the production 
supervisor was Sherri Souffrance. It was set in Century Schoolbook by MacAllister 
Publishing Services, LLC.
Printed and bound by RR Donnelley.
McGraw-Hill books are available at special quantity discounts to use as premiums and
sales promotions, or for use in corporate training programs. For more information,
please write to the Director of Special Sales, Professional Publishing, McGraw-Hill,
Two Penn Plaza, New York, NY 10121-2298. Or contact your local bookstore.
This book is printed on recycled, acid-free paper containing a minimum of 50 
percent recycled de-inked fiber.

--- [Page 3] ---
Introduction
CHAPTER 1

CHAPTER
1
Introduction

--- [Page 4] ---
In the late 1990s, the telecommunications boom went bust because
new market entrants, known as Competitive Local Exchange Carri-
ers (CLECs), were forced to compete with Incumbent Local Exchange
Carriers (ILECs) on the same financial terms of the

<!-- CORA-MAXIMIZED-COMMANDS-START -->
## Maximized Windows & Linux Command Examples for `WiFi Handbook 1`

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
