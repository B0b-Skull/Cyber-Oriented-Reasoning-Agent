---
title: "Trained Command Playbook: CQC001 E010 M040 Netstat"
category: commands
domain_hub: "[[knowledge/05_windows_and_linux_networking_routing_and_firewalls]]"
os_platform: cross-platform
primary_tactic: L2_L3_Pivot_Routing
summary: "Verified Windows & Linux command playbook for CQC001 E010 M040 Netstat (L2_L3_Pivot_Routing): Side-by-side Windows and Linux networking reference covering L2 ARP/neighbors (arp vs ip neigh), L3 routing & forwarding (route/netsh v"
when_to_apply: "Apply when working with CQC001 E010 M040 Netstat (cross-platform): Apply whenever diagnosing network unreachability (`Network is unreachable`, `No route to host`, `Connection timed out`), mapping local/remote subnets (`Engine 2`), configuring cross-subnet static routes/IP forwarding/NAT masquerading (`Engine 6/15/19`), inspecting listening ports (`ss`/`netstat`), or unlocking `iptables`/`nftables`/`netsh advfirewall` rules."
tags: [eth0, eth2, http, https, mdp, netstat, passive_enum, pdf, ssh, trained, windows, linux, cross-platform, iproute2, ipconfig, route, arp, ss, netsh, iptables, nftables, sysctl]
source_file: "CQC001 E010 M040 Netstat"
updated: 2026-10-30
---

ip -4 -br addr show; ip route show; ip neigh show
# Trained Command Playbook: `CQC001_E010_M040_Netstat.pdf`
ip -4 -br addr show; ip route show; ip neigh show
- **Source Document:** `~/Projects/CORA/Training/CQC001_E010_M040_Netstat.pdf`
- **CEGAR Verified Commands:** `21` (`0` malformed/unsafe snippets filtered)
- **MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`):** `21`
- **Discovered IPs/Subnets:** `0.0.0.0, 10.99.99.1, 101.101.34.101, 101.11.169.230, 101.174.100.22, 172.24.1.0, 172.24.1.1, 172.24.185.75, 255.255.0.0, 255.255.255.0`
- **Discovered Interfaces:** `eth0, eth2, lo`
- **Related Knowledge Note:** [[knowledge/trained_cqc001_e010_m040_netstat]]
ip -4 -br addr show; ip route show; ip neigh show
## Distilled MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`)
| Pre-State ($s$) | Tactic ($\tau$) | Technique ($k$) | Tool ($u$) | Post-State ($s'$) | Verified Command ($c$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `netstat` | `s_passive_topology_mapped` | `netstat -e` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `netstat` | `s_passive_topology_mapped` | `netstat -a -n` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `netstat` | `s_passive_topology_mapped` | `netstat -s` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `netstat` | `s_passive_topology_mapped` | `netstat -a \| more` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `netstat` | `s_passive_topology_mapped` | `netstat -at` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `netstat` | `s_passive_topology_mapped` | `netstat -au` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `netstat` | `s_passive_topology_mapped` | `netstat -l` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `netstat` | `s_passive_topology_mapped` | `netstat -lt` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `netstat` | `s_passive_topology_mapped` | `netstat -lu` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `netstat` | `s_passive_topology_mapped` | `netstat -lx` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `netstat` | `s_passive_topology_mapped` | `netstat -st` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `netstat` | `s_passive_topology_mapped` | `netstat -su` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `netstat` | `s_passive_topology_mapped` | `netstat -pt` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `netstat` | `s_passive_topology_mapped` | `netstat -an` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `netstat` | `s_passive_topology_mapped` | `netstat -c` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `netstat` | `s_passive_topology_mapped` | `netstat --verbose` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `netstat` | `s_passive_topology_mapped` | `netstat -r` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `netstat` | `s_passive_topology_mapped` | `netstat -ap \| grep ssh` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `netstat` | `s_passive_topology_mapped` | `netstat -an \| grep ':80'` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `netstat` | `s_passive_topology_mapped` | `netstat -i` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `netstat` | `s_passive_topology_mapped` | `netstat -ie` |
ip -4 -br addr show; ip route show; ip neigh show
## Verified Executable Commands (Grouped by Capability Layer)
ip -4 -br addr show; ip route show; ip neigh show
### L4_Port_Service (21 commands)
```bash
netstat -e
netstat -a -n
netstat -s
netstat -a | more
netstat -at
netstat -au
netstat -l
netstat -lt
netstat -lu
netstat -lx
netstat -st
netstat -su
netstat -pt
netstat -an
netstat -c
netstat --verbose
netstat -r
netstat -ap | grep ssh
netstat -an | grep ':80'
netstat -i
netstat -ie
```
ip -4 -br addr show; ip route show; ip neigh show

<!-- CORA-MAXIMIZED-COMMANDS-START -->
## Maximized Windows & Linux Command Examples for `CQC001 E010 M040 Netstat`

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
