---
title: "Trained Knowledge & Topology: Spectrum-GSMA-Spectrum-Handbook-2012"
category: knowledge
domain_hub: "[[knowledge/09_hardware_uart_serial_oob_and_telecom_wan]]"
os_platform: cross-platform
primary_tactic: OOB_Serial_Access
summary: "Operational architecture, decision workflows & Windows/Linux command reference for Spectrum-GSMA-Spectrum-Handbook-2012: Non-interactive tio 3.9 Lua --script UART serial console automation (/dev/ttyUSB0, -o 15 -O 120 pacing), Windows COM port OOB acce"
when_to_apply: "Apply when working with Spectrum-GSMA-Spectrum-Handbook-2012 (cross-platform): Apply whenever network connections to an appliance fail (`Exit 7` Connection Refused or `Exit 28` Timeout) and a hardware serial console (`/dev/ttyUSB0` or `COM1`) is available (`C1_OOB_SERIAL_LOOPBACK_APPLIANCE`), or when analyzing Carrier Metro Ethernet, MPLS/GMPLS labels, OTN/GPON optical links, SD-WAN tunnels, Wi-Fi 802.11, or 2G/3G/4G/5G cellular RAN protocols."
tags: [http, mdp, pdf, trained, linux, windows, tio, serial, ttyusb0, ttyusb1, com1, uart, oob, oob_serial_access, mpls, gmpls, metro_ethernet, vlan, otn, gpon, sd-wan, wifi]
source_file: "Spectrum-GSMA-Spectrum-Handbook-2012"
updated: 2026-10-30
---

# Trained Knowledge & Architecture: `Spectrum-GSMA-Spectrum-Handbook-2012.pdf`

- **Source Path:** `~/Projects/CORA/Training/Spectrum-GSMA-Spectrum-Handbook-2012.pdf` (`pdf`)
- **Extracted Technical Entities:** `http`
- **Extracted IPs / Subnets:** `None`
- **Extracted Interfaces:** `None`

## Extracted Reference Excerpt
--- [Page 1] ---
1
Spectrum Handbook
Understanding the Basics of Spectrum Policy 
for Mobile Telecommunications
1 GHz
2 GHz
4 GHz
3 GHz
5 GHz
6 GHz
2.5 GHz
December 2011

--- [Page 2] ---
2
3
4
7
9
12
14
16
17
18
Why Spectrum Matters
Radio Frequency Spectrum Explained
A Resource in High Demand
Mobile Technologies and Spectrum Use
The Evolution of Mobile Technologies	
International Regulators and Initiatives
Managing Spectrum for the Long Term
Additional Resources
Glossary of Terms
Contents

--- [Page 3] ---
3
Society benefits in countless ways from 
devices that communicate over the 
airwaves. Radio frequency spectrum 
is used to send information instantly 
across distances short and long — 
without wires or cables — making 
things possible that most people take 
for granted: television and radio, 
mobile phones, airplane navigation 
and radar, and Wi-Fi connections in 
airport lounges. Wireless technologies 
are ubiquitous, and people have come 
to depend on them in an increasingly 
connected, information-driven world. 
Now that mobile phones have become 
pervasive around the world, the boom 
is in mobile data, as people are using 
smartphones to access the internet, send 
and receive email, watch videos and 
use mobile apps. In fact, mobile data 
traffic is projected to grow annually by 
92 per cent, through 2015, according to 
Cisco Systems.1 The mobile industry is 
growing by leaps and bounds.
Mobile penetration is directly linked 
to economic growth, and not only in 
developed economies. One study found 
that a 10 per cent increase in mobile 
penetration in a developing country 
typically leads to a 1.2% growth in its 
GDP.2
However, the portion of the radio 
spectrum that can be used for many 
services is very limited. With so much 
at stake, for society and national 
economies, responsible management of 
this valuable resource is critical.
About this handbook
This handbook gives a nontechnical 
introduction to radio spectrum and 
the issues surrounding spectrum 
management, for people who don’t have 
a technical background in the subject. 
While there is far more to know about 
spectrum than is contained in these 
pages, it is hoped that this overview will 
be a useful primer.
Why Spectrum Matters
The ‘mobile miracle’ is putting 
ICT services within reach of 
even the most disadvantaged 
people and communities. Our 
challenge now is to replicate 
that success in broadband.
— ITU Secretary General 
Hamadoun Touré
1Cisco Visual Networking Index: Global Mobile Data Traffic Forecast Update, 2010–2015
2GSMA Global Mobile Tax Review 2006-07

--- [Page 4] ---
4
Radio waves are a form of 
electromagnetic radiation which, like 
visible light or infrared, make up one 
portion of the entire spectrum. They 
cannot be perceived by human eyes 
or ears, and

<!-- CORA-MAXIMIZED-COMMANDS-START -->
## Maximized Windows & Linux Command Examples for `Spectrum-GSMA-Spectrum-Handbook-2012`

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
