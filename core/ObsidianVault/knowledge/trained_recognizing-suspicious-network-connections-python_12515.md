---
title: "Trained Knowledge & Topology: recognizing-suspicious-network-connections-python 12515"
category: knowledge
domain_hub: "[[knowledge/05_windows_and_linux_networking_routing_and_firewalls]]"
os_platform: cross-platform
primary_tactic: L2_L3_Pivot_Routing
summary: "Operational architecture, decision workflows & Windows/Linux command reference for recognizing-suspicious-network-connections-python 12515: Side-by-side Windows and Linux networking reference covering L2 ARP/neighbors (arp vs ip neigh), L3 routing & forwarding (route/ne"
when_to_apply: "Apply when working with recognizing-suspicious-network-connections-python 12515 (cross-platform): Apply whenever diagnosing network unreachability (`Network is unreachable`, `No route to host`, `Connection timed out`), mapping local/remote subnets (`Engine 2`), configuring cross-subnet static routes/IP forwarding/NAT masquerading (`Engine 6/15/19`), inspecting listening ports (`ss`/`netstat`), or unlocking `iptables`/`nftables`/`netsh advfirewall` rules."
tags: [arp, defense_evasion_firewall, enumeration, http, https, ipconfig, mdp, netsh, netstat, pdf, powershell, ssh, trained, windows, linux, cross-platform, iproute2, route, ss, iptables, nftables, sysctl]
source_file: "recognizing-suspicious-network-connections-python 12515"
updated: 2026-10-30
---

# Trained Knowledge & Architecture: `recognizing-suspicious-network-connections-python_12515.pdf`

- **Source Path:** `~/Projects/CORA/Training/recognizing-suspicious-network-connections-python_12515.pdf` (`pdf`)
- **Extracted Technical Entities:** `arp, http, https, ipconfig, netsh, netstat, powershell, ssh`
- **Extracted IPs / Subnets:** `None`
- **Extracted Interfaces:** `None`
- **Linked Command Playbook:** [[commands/trained_recognizing-suspicious-network-connections-python_12515]] (`3` CEGAR-verified commands | `3` MDP transitions)

## Command & Tactic Coverage Summary
- **Total CEGAR-Verified Commands:** `3` (full executable list in [[commands/trained_recognizing-suspicious-network-connections-python_12515]])
- **Tactic Distribution:** `Defense_Evasion_Firewall` (2), `Enumeration` (1)
- **Top Extracted CLI Tools:** `get-content` (1), `netsh` (1), `script` (1)

## Document Structure & Key Topics
- DNS parsing for to record multiple DNS entries and extract/normalize
- Without this loop only the first DNS entry will be returned and the
- signal.signal(signal.SIGINT, signal_handler)

## Extracted Operational Steps & Workflows
- 1. Introduction
- 2. DNS
- 3. TCP Network Connections
- 4. Blocking Direct IP Calls as a Theory
- 5. Scapy and Python
- 6. Simulation
- 7. Proof of Concept Walkthrough and Demonstration
- 8. Conclusion

## Extracted Reference Excerpt
--- [Page 1] ---
Global Information Assurance Certification Paper
Copyright SANS Institute
Author Retains Full Rights
This paper is taken from the GIAC directory of certified professionals. Reposting is not permited without express written permission.
Interested in learning more?
Check out the list of upcoming events offering
"Intrusion Detection In-Depth (Security 503)"
at http://www.giac.org/registration/gcia

--- [Page 2] ---
© 2020 The SANS Institute, Author Retains Full Rights
© 2020 The SANS Institute
Author retains full rights. 
Recognizing Suspicious Network Connections 
with Python 
 GIAC (GCIA) Gold Certification 
Author: Gregory Melton, Gregory.Melton@student.sans.edu 
Advisor: Clay Risenhoover 
Accepted: May 10, 2020 
Abstract 
Endpoint protection solutions tend to focus on system indicators and known malicious 
code to defend both enterprise and Small Office-Home Office (SOHO) users.  In the 
absence of a Security Operations Center (SOC) or paid antivirus services, there are few 
proactive defense options for hobbyists and SOHO owners. A significant problem is how 
advanced persistent threat (APT) actors’ Tactics, Techniques, and Procedures (TTPs) 
have changed over the years; it is common for advanced actors to exploit poorly defended 
subcontractors and seemingly less relevant targets. This brings the Small Office-Home 
Office into the picture as a pivotal defense point against advanced attackers. This 
research intends to focus on attackers using Shell, terminal, or Remote Access Tool 
(RAT) connections to SOHO endpoints. This research seeks to block interactive 
connections with system-level network logging and blacklist automation. This method 
will recognize malicious connections and automatically block them in near real-time.

--- [Page 3] ---
© 2020 The SANS Institute, Author Retains Full Rights
© 2020 The SANS Institute
Author retains full rights. 
 
Recognizing Suspicious Network Connections with Python 
 
2 
 
Melton, Gregory [USA] 
 
1. Introduction 
Meaningful endpoint security against interactive threats is a difficult security 
challenge to manage. Typically, if an attacker obtains a Shell or terminal connection, they 
have already defeated the system’s security protocols. From a developer’s standpoint, it 
may not be worth the effort to wrangle Windows Application Programming Interfaces 
(APIs) against the unlikely occurrence of an interactive threat to home or small office 
users. Unfortunately, APT groups commonly target smaller entities and search for 
backend routes into larger targets by abusing contractor access. By focusing a defensive 
posture on network connections as a chokepoint, it may be possible to create a module 
that recognizes suspicious IP connections and adds said IP address to the system’s 
firewall b

<!-- CORA-MAXIMIZED-COMMANDS-START -->
## Maximized Windows & Linux Command Examples for `recognizing-suspicious-network-connections-python 12515`

> **Domain Hub:** [[knowledge/05_windows_and_linux_networking_routing_and_firewalls|Domain Hub 05: Cross-Platform L2/L3/L4 Networking, Routing, DNS, Host Firewalls (netsh / iptables / nftables) & IDS (Snort)]]  
> **Master Playbooks:** [[commands/windows_master_command_playbook]] | [[commands/linux_master_command_playbook]] | [[commands/curl_playbook]] | [[commands/tio_serial_playbook]]  
> **When to Apply:** Apply whenever diagnosing network unreachability (`Network is unreachable`, `No route to host`, `Connection timed out`), mapping local/remote subnets (`Engine 2`), configuring cross-subnet static routes/IP forwarding/NAT masquerading (`Engine 6/15/19`), inspecting listening ports (`ss`/`netstat`), or unlocking `iptables`/`nftables`/`netsh advfirewall` rules.  
> **15-Engine H-MDP State Transition:** `s_passive_topology_mapped` $\xrightarrow{\text{L2_L3_Pivot_Routing}}$ `s_cross_subnet_pivot_routed` | **Bayesian Root-Cause Triggers:** `missing_static_route, pivot_ip_forward_disabled, asymmetric_missing_return_route_or_nat, host_firewall_drop, service_bound_to_loopback` | **Isolation:** `RED, BLUE, WHITE (Passive local inspection works in WHITE; cross-subnet routing/probing works in RED and allowed BLUE NICs)`

| Primary Command (`Windows` / `Linux`) | OS / Shell | What It Does & Key Flags | When to Apply & Expected Output | Cross-Platform Equivalent |
| :--- | :--- | :--- | :--- | :--- |
| `ip -4 -br addr show; ip route show; ip neigh show` | **Linux Bash** | CORA canonical 3-in-1 passive L2/L3 probe: outputs IPv4 interfaces/CIDRs, kernel routing table, and L2 ARP neighbor cache (`REACHABLE`/`STALE`/`FAILED`). | Apply first on Linux (`s_init_unknown -> s_passive_topology_mapped`) to map local subnets and gateways in `< 15 ms`. | `ipconfig /all & route print -4 & arp -a` |
| `ipconfig /all & route print -4 & arp -a` | **Windows CMD** | CORA canonical Windows 3-in-1 passive L2/L3 probe: dumps all adapter IPs/MACs/DNS, IPv4 routing table, and ARP cache. | Apply first on Windows (`s_init_unknown -> s_passive_topology_mapped`) to map local subnets, gateways, and L2 neighbors. | `ip -4 -br addr show; ip route show; ip neigh show` |
| `ss -tulpn && ss -tanp` | **Linux Bash** | Lists all listening TCP/UDP sockets (`-tulpn`) and all active/established TCP connections (`-tanp`) with owning process PIDs. | Apply to verify whether a target daemon is bound to `127.0.0.1` (`service_bound_to_loopback`) or `0.0.0.0`. | `netstat -abno` |
| `netstat -ano \| findstr "LISTENING ESTABLISHED"` | **Windows CMD** | Lists all listening ports and active established TCP connections with owning `PID` on Windows (`[[commands/trained_cqc001_e010_m040_netstat]]`). | Apply to audit open Windows ports and cross-reference PIDs with `tasklist /svc`. | `ss -tanp` |
| `sudo ip route replace <REMOTE_SUBNET> via <GATEWAY_IP> && sudo sysctl -w net.ipv4.ip_forward=1` | **Linux Bash** | Adds/updates a static L3 route to `<REMOTE_SUBNET>` via `<GATEWAY_IP>` and enables kernel IPv4 packet forwarding (`ip_forward=1`). | Apply when Geometric Engine (`Engine 2`) reports `<TARGET_IP>` is DISJOINT from local subnets (`C2_CROSS_SUBNET_L3_PIVOT`). | `route add <REMOTE_SUBNET> mask 255.255.255.0 <GATEWAY_IP> & netsh interface ipv4 set interface <Idx> forwarding=enabled` |
| `sudo iptables -t nat -A POSTROUTING -s <LOCAL_SUBNET> -d <REMOTE_SUBNET> -o <OUT_IFACE> -j MASQUERADE && sudo iptables -I FORWARD 1 -j ACCEPT` | **Linux Bash** | Enables Source NAT (`MASQUERADE`) on the egress interface and allows transit packets in the `FORWARD` chain. | Apply when downstream hosts in `<REMOTE_SUBNET>` lack a return route back to the operator's subnet (`asymmetric_missing_return_route_or_nat`). | `New-NetNat -Name 'PivotNAT' -InternalIPInterfaceAddressPrefix <LOCAL_SUBNET>` |
| `sudo iptables -L -n -v --line-numbers && sudo iptables -t nat -L -n -v && sudo nft list ruleset` | **Linux Bash** | Audits all `iptables` filter/NAT chains (with packet counters) and `nftables` rulesets (`[[commands/trained_iptables-snort-cmds]]`). | Apply whenever TCP connections time out (`Exit 28`) or return `ICMP Administratively Prohibited` (`host_firewall_drop`). | `netsh advfirewall show allprofiles & netsh advfirewall firewall show rule name=all dir=in status=enabled` |
| `netsh advfirewall show allprofiles && netsh advfirewall firewall add rule name="CORA_Allow_Port" dir=in action=allow protocol=TCP localport=8443` | **Windows CMD (Admin)** | Inspects Windows Defender Firewall profile states (`Domain`/`Private`/`Public`) and adds an inbound TCP allow rule (`[[commands/trained_netsh_fw_cmds]]`). | Apply on Windows when unlocking a blocked inbound management or service port. | `sudo iptables -I INPUT 1 -p tcp --dport 8443 -j ACCEPT` |
| `netsh interface portproxy show all && netsh interface portproxy add v4tov4 listenaddress=0.0.0.0 listenport=8443 connectaddress=127.0.0.1 connectport=8080` | **Windows CMD (Admin)** | Lists and configures native Windows TCP port forwarding (`v4tov4`) via `iphlpsvc` (`[[commands/trained_netsh_commands_for_routing]]`). | Apply on Windows to expose a loopback-bound (`127.0.0.1:8080`) service on an external interface (`0.0.0.0:8443`) or pivot across subnets. | `socat TCP-LISTEN:8443,fork,reuseaddr TCP:127.0.0.1:8080` |
| `sudo snort -T -c /etc/snort/snort.conf && sudo snort -A console -q -c /etc/snort/snort.conf -i <IFACE>` | **Linux Bash** | Validates Snort IDS configuration (`-T`) and runs real-time signature detection alerting to console (`-A console -q`). | Apply when auditing or testing IDS signature rules (`[[knowledge/trained_cqc001_e060_m030_iptables_and_snort]]`). | `snort.exe -W && snort.exe -A console -c C:\Snort\etc\snort.conf -i 1` |

### Copy-Pasteable Execution Block (Windows & Linux)
```bash
# [Linux Bash] CORA canonical 3-in-1 passive L2/L3 probe: outputs IPv4 interfaces/CIDRs, kernel routing table, and L2 ARP neighbor cache (`REACHABLE`/`STALE`/`FAILED`).
ip -4 -br addr show; ip route show; ip neigh show
# [Windows CMD] CORA canonical Windows 3-in-1 passive L2/L3 probe: dumps all adapter IPs/MACs/DNS, IPv4 routing table, and ARP cache.
ipconfig /all & route print -4 & arp -a
# [Linux Bash] Lists all listening TCP/UDP sockets (`-tulpn`) and all active/established TCP connections (`-tanp`) with owning process PIDs.
ss -tulpn && ss -tanp
# [Windows CMD] Lists all listening ports and active established TCP connections with owning `PID` on Windows (`[[commands/trained_cqc001_e010_m040_netstat]]`).
netstat -ano | findstr "LISTENING ESTABLISHED"
# [Linux Bash] Adds/updates a static L3 route to `<REMOTE_SUBNET>` via `<GATEWAY_IP>` and enables kernel IPv4 packet forwarding (`ip_forward=1`).
sudo ip route replace <REMOTE_SUBNET> via <GATEWAY_IP> && sudo sysctl -w net.ipv4.ip_forward=1
# [Linux Bash] Enables Source NAT (`MASQUERADE`) on the egress interface and allows transit packets in the `FORWARD` chain.
sudo iptables -t nat -A POSTROUTING -s <LOCAL_SUBNET> -d <REMOTE_SUBNET> -o <OUT_IFACE> -j MASQUERADE && sudo iptables -I FORWARD 1 -j ACCEPT
```
<!-- CORA-MAXIMIZED-COMMANDS-END -->
