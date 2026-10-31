---
title: "Trained Command Playbook: Netsh commands for Routing"
category: commands
domain_hub: "[[knowledge/05_windows_and_linux_networking_routing_and_firewalls]]"
os_platform: cross-platform
primary_tactic: L2_L3_Pivot_Routing
summary: "Verified Windows & Linux command playbook for Netsh commands for Routing (L2_L3_Pivot_Routing): Side-by-side Windows and Linux networking reference covering L2 ARP/neighbors (arp vs ip neigh), L3 routing & forwarding (route/netsh v"
when_to_apply: "Apply when working with Netsh commands for Routing (cross-platform): Apply whenever diagnosing network unreachability (`Network is unreachable`, `No route to host`, `Connection timed out`), mapping local/remote subnets (`Engine 2`), configuring cross-subnet static routes/IP forwarding/NAT masquerading (`Engine 6/15/19`), inspecting listening ports (`ss`/`netstat`), or unlocking `iptables`/`nftables`/`netsh advfirewall` rules."
tags: [enumeration, https, mdp, netsh, passive_enum, pdf, trained, windows, linux, cross-platform, iproute2, ipconfig, route, arp, netstat, ss, iptables, nftables, sysctl, ip_forward, masquerade, snort]
source_file: "Netsh commands for Routing"
updated: 2026-10-30
---

ip -4 -br addr show; ip route show; ip neigh show
# Trained Command Playbook: `Netsh commands for Routing.pdf`
ip -4 -br addr show; ip route show; ip neigh show
- **Source Document:** `~/Projects/CORA/Training/Netsh commands for Routing.pdf`
- **CEGAR Verified Commands:** `16` (`0` malformed/unsafe snippets filtered)
- **MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`):** `16`
- **Discovered IPs/Subnets:** `0.0.0.0, 10.0.0.2, 10.10.1.100, 10.10.10.0, 10.10.10.1, 10.11.11.1, 10.11.21.154, <LOCAL_HOST_IP>, 255.255.255.0`
- **Discovered Interfaces:** `None`
- **Related Knowledge Note:** [[knowledge/trained_netsh_commands_for_routing]]
ip -4 -br addr show; ip route show; ip neigh show
## Distilled MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`)
| Pre-State ($s$) | Tactic ($\tau$) | Technique ($k$) | Tool ($u$) | Post-State ($s'$) | Verified Command ($c$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `netsh` | `s_active_services_enumerated` | `Netsh commands for Routing` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `ip` | `s_passive_topology_mapped` | `IP address, and the second address is for the high IP address to use in building the filter.` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `netsh` | `s_active_services_enumerated` | `Netsh Routing IP IGMP commands` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `ip` | `s_passive_topology_mapped` | `IP address, and the second address is for the high IP address used in building the filter.` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `netsh` | `s_active_services_enumerated` | `Netsh Routing IP Routerdiscovery commands` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `netsh` | `s_active_services_enumerated` | `Netsh Routing IP RIP commands` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `netsh` | `s_active_services_enumerated` | `Netsh Routing IP Relay commands` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `netsh` | `s_active_services_enumerated` | `Netsh Routing IP OSPF commands` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `netsh` | `s_active_services_enumerated` | `Netsh Routing IP Autodhcp commands` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `netsh` | `s_active_services_enumerated` | `Netsh Routing IP Dnsproxy commands` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `netsh` | `s_active_services_enumerated` | `Netsh Routing IP NAT commands` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `netsh` | `s_active_services_enumerated` | `Netsh Routing IPX commands` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `netsh` | `s_active_services_enumerated` | `Netsh Routing IPX NetBIOS commands` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `netsh` | `s_active_services_enumerated` | `Netsh Routing IPX RIP commands` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `netsh` | `s_active_services_enumerated` | `Netsh Routing IPX SAP commands` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `netsh` | `s_active_services_enumerated` | `Netsh Routing example` |
ip -4 -br addr show; ip route show; ip neigh show
## Verified Executable Commands (Grouped by Capability Layer)
ip -4 -br addr show; ip route show; ip neigh show
### L3_Routing_NAT (16 commands)
```bash
Netsh commands for Routing
Netsh Routing IP IGMP commands
Netsh Routing IP Routerdiscovery commands
Netsh Routing IP RIP commands
IP address, and the second address is for the high IP address to use in building the filter.
IP address, and the second address is for the high IP address used in building the filter.
Netsh Routing IP Relay commands
Netsh Routing IP OSPF commands
Netsh Routing IP Autodhcp commands
Netsh Routing IP Dnsproxy commands
Netsh Routing IP NAT commands
Netsh Routing IPX commands
Netsh Routing IPX NetBIOS commands
Netsh Routing IPX RIP commands
Netsh Routing IPX SAP commands
Netsh Routing example
```
ip -4 -br addr show; ip route show; ip neigh show

<!-- CORA-MAXIMIZED-COMMANDS-START -->
## Maximized Windows & Linux Command Examples for `Netsh commands for Routing`

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
