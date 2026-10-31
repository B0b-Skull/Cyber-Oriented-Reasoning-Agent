---
title: "Trained Command Playbook: IPtables-Snort-CMDs"
category: commands
domain_hub: "[[knowledge/05_windows_and_linux_networking_routing_and_firewalls]]"
os_platform: cross-platform
primary_tactic: L2_L3_Pivot_Routing
summary: "Verified Windows & Linux command playbook for IPtables-Snort-CMDs (L2_L3_Pivot_Routing): Side-by-side Windows and Linux networking reference covering L2 ARP/neighbors (arp vs ip neigh), L3 routing & forwarding (route/netsh v"
when_to_apply: "Apply when working with IPtables-Snort-CMDs (cross-platform): Apply whenever diagnosing network unreachability (`Network is unreachable`, `No route to host`, `Connection timed out`), mapping local/remote subnets (`Engine 2`), configuring cross-subnet static routes/IP forwarding/NAT masquerading (`Engine 6/15/19`), inspecting listening ports (`ss`/`netstat`), or unlocking `iptables`/`nftables`/`netsh advfirewall` rules."
tags: [defense_evasion_firewall, eth0, eth1, iptables, mdp, nmap, snort, ssh, tcpdump, text, trained, windows, linux, cross-platform, iproute2, ipconfig, route, arp, netstat, ss, netsh, nftables]
source_file: "IPtables-Snort-CMDs"
updated: 2026-10-30
---

ip -4 -br addr show; ip route show; ip neigh show
# Trained Command Playbook: `IPtables-Snort-CMDs.txt`
ip -4 -br addr show; ip route show; ip neigh show
- **Source Document:** `~/Projects/CORA/Training/IPtables-Snort-CMDs.txt`
- **CEGAR Verified Commands:** `42` (`0` malformed/unsafe snippets filtered)
- **MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`):** `42`
- **Discovered IPs/Subnets:** `10.18.80.64/26, 172.24.0.0/24, 172.24.1.0/24, 172.24.11.0/24, 172.24.11.13, 172.24.11.15, 172.24.11.254, 192.18.31.253, 198.18.31.253`
- **Discovered Interfaces:** `eth0, eth1, lo`
- **Related Knowledge Note:** [[knowledge/trained_iptables-snort-cmds]]
ip -4 -br addr show; ip route show; ip neigh show
## Distilled MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`)
| Pre-State ($s$) | Tactic ($\tau$) | Technique ($k$) | Tool ($u$) | Post-State ($s'$) | Verified Command ($c$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `iptables` | `s_firewall_or_acl_unlocked` | `IPTables & Snort` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `nmap` | `s_firewall_or_acl_unlocked` | `nmap -n -Pn -sS -p 21,22,23,25,80,110,111,443 198.18.31.253` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `tcpdump` | `s_firewall_or_acl_unlocked` | `tcpdump -vv src 192.18.31.253 and dst 172.24.11.15` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `nmap` | `s_firewall_or_acl_unlocked` | `nmap -n -Pn -sU -p 53,67,123,135,137,138,161,445,631,1434 198.18.31.253` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `iptables` | `s_firewall_or_acl_unlocked` | `iptables -A INPUT -p udp -j REJECT --reject-with icmp-net-prohibited` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `iptables` | `s_firewall_or_acl_unlocked` | `iptables -A INPUT -p tcp -j REJECT --reject-with tcp-reset` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `iptables` | `s_firewall_or_acl_unlocked` | `iptables -A INPUT -p icmp -j DROP` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `iptables` | `s_firewall_or_acl_unlocked` | `iptables -A INPUT -d 172.24.11.13 \! -i eth0 -j DROP` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `iptables` | `s_firewall_or_acl_unlocked` | `iptables -A INPUT -p tcp -m state --state ESTABLISHED, RELATED -j ACCEPT` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `iptables` | `s_firewall_or_acl_unlocked` | `iptables -P INPUT DROP` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `iptables` | `s_firewall_or_acl_unlocked` | `iptables -t filter -F` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `iptables` | `s_firewall_or_acl_unlocked` | `iptables -t nat -F` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `iptables` | `s_firewall_or_acl_unlocked` | `iptables -X` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `iptables` | `s_firewall_or_acl_unlocked` | `iptables -P INPUT ACCEPT` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `iptables` | `s_firewall_or_acl_unlocked` | `iptables -P OUTPUT ACCEPT` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `iptables` | `s_firewall_or_acl_unlocked` | `iptables -P FORWARD ACCEPT` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `iptables` | `s_firewall_or_acl_unlocked` | `iptables -t filter -A FORWARD -s 172.24.0.0/24 -d 172.24.1.0/24 -i eth0 -o eth1 -j ACCEPT` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `iptables` | `s_firewall_or_acl_unlocked` | `iptables -A INPUT -i lo -j ACCEPT` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `iptables` | `s_firewall_or_acl_unlocked` | `iptables -A OUTPUT -o lo -j ACCEPT` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `iptables` | `s_firewall_or_acl_unlocked` | `iptables -t filter -A INPUT -p tcp --dport 22 -s 10.18.80.64/26 -j ACCEPT` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `iptables` | `s_firewall_or_acl_unlocked` | `iptables -t filter -A OUTPUT -p tcp --sport 22 -d 10.18.80.64/26 -j ACCEPT` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `iptables` | `s_firewall_or_acl_unlocked` | `iptables -t filter -A INPUT -p tcp --dport 22 -s 10.18.80.64/26 -m state --state NEW,ESTABLISHED,RELATED -j ACCEPT` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `iptables` | `s_firewall_or_acl_unlocked` | `iptables -t filter -A OUTPUT -p tcp --sport 22 -d 10.18.80.64/26 -m state --state ESTABLISHED,RELATED -j ACCEPT` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `iptables` | `s_firewall_or_acl_unlocked` | `sudo iptables -A INPUT -s 172.24.11.13 -p tcp --dport 22 -j ACCEPT` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `iptables` | `s_firewall_or_acl_unlocked` | `sudo iptables -A OUTPUT -d 172.24.11.13 -p tcp --sport 22 -j ACCEPT` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `iptables` | `s_firewall_or_acl_unlocked` | `sudo iptables -A INPUT -i lo -j ACCEPT` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `iptables` | `s_firewall_or_acl_unlocked` | `sudo iptables -A OUTPUT -o lo -j ACCEPT` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `iptables` | `s_firewall_or_acl_unlocked` | `iptables -I INPUT 1 -s 172.24.11.13 -p tcp --dport 22 -m state --state NEW,RELATED,ESTABLISHED -j ACCEPT` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `iptables` | `s_firewall_or_acl_unlocked` | `iptables -I OUTPUT 1 -d 172.24.11.13 -p tcp --sport 22 -m state --state RELATED,ESTABLISHED -j ACCEPT` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `ssh` | `s_firewall_or_acl_unlocked` | `ssh haxor@172.24.11.254` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `iptables` | `s_firewall_or_acl_unlocked` | `sudo iptables -I FORWARD 1 -s win7.ops.local -d ad.ops.local -p tcp --dport 23 -m state --state NEW,RELATED,ESTABLISHED -j ACCEPT` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `iptables` | `s_firewall_or_acl_unlocked` | `sudo iptables -I FORWARD 2 -s ad.ops.local -d win7.ops.local -p tcp --sport 23 -m state --state RELATED,ESTABLISHED -j ACCEPT` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `iptables` | `s_firewall_or_acl_unlocked` | `sudo iptables -I FORWARD 3 -s 172.24.11.0/24 -d ad.ops.local -p tcp --dport 23 -j REJECT --reject-with tcp-reset` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `iptables` | `s_firewall_or_acl_unlocked` | `sudo iptables -I FORWARD 4 -s linux.ops.local -d ad.ops.local -p udp --dport 53 -j ACCEPT` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `iptables` | `s_firewall_or_acl_unlocked` | `sudo iptables -I FORWARD 5 -s ad.ops.local -d linux.ops.local -p udp --sport 53 -j ACCEPT` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `iptables` | `s_firewall_or_acl_unlocked` | `sudo iptables -I FORWARD 6 -s linux.ops.local -d ad.ops.local -j DROP` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `iptables` | `s_firewall_or_acl_unlocked` | `sudo iptables -I FORWARD 7 -d www.ops.local -p tcp --dport 80 -m state --state NEW,RELATED,ESTABLISHED -j ACCEPT` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `iptables` | `s_firewall_or_acl_unlocked` | `sudo iptables -I FORWARD 8 -s www.ops.local -p tcp --sport 80 -m state --state RELATED,ESTABLISHED -j ACCEPT` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `iptables` | `s_firewall_or_acl_unlocked` | `sudo iptables -I FORWARD 9 -d www.ops.local -j REJECT --reject-with icmp-host-unreachable` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `iptables` | `s_firewall_or_acl_unlocked` | `sudo iptables -I FORWARD 10 -s www.ops.local -j LOG` |
ip -4 -br addr show; ip route show; ip neigh show
## Verified Executable Commands (Grouped by Capability Layer)
ip -4 -br addr show; ip route show; ip neigh show
### General_System (16 commands)
```bash
sudo iptables -A INPUT -s 172.24.11.13 -p tcp --dport 22 -j ACCEPT
sudo iptables -A OUTPUT -d 172.24.11.13 -p tcp --sport 22 -j ACCEPT
sudo iptables -A INPUT -i lo -j ACCEPT
sudo iptables -A OUTPUT -o lo -j ACCEPT
sudo iptables -I FORWARD 1 -s win7.ops.local -d ad.ops.local -p tcp --dport 23 -m state --state NEW,RELATED,ESTABLISHED -j ACCEPT
sudo iptables -I FORWARD 2 -s ad.ops.local -d win7.ops.local -p tcp --sport 23 -m state --state RELATED,ESTABLISHED -j ACCEPT
sudo iptables -I FORWARD 3 -s 172.24.11.0/24 -d ad.ops.local -p tcp --dport 23 -j REJECT --reject-with tcp-reset
sudo iptables -I FORWARD 4 -s linux.ops.local -d ad.ops.local -p udp --dport 53 -j ACCEPT
sudo iptables -I FORWARD 5 -s ad.ops.local -d linux.ops.local -p udp --sport 53 -j ACCEPT
sudo iptables -I FORWARD 6 -s linux.ops.local -d ad.ops.local -j DROP
sudo iptables -I FORWARD 7 -d www.ops.local -p tcp --dport 80 -m state --state NEW,RELATED,ESTABLISHED -j ACCEPT
sudo iptables -I FORWARD 8 -s www.ops.local -p tcp --sport 80 -m state --state RELATED,ESTABLISHED -j ACCEPT
sudo iptables -I FORWARD 9 -d www.ops.local -j REJECT --reject-with icmp-host-unreachable
sudo iptables -I FORWARD 10 -s www.ops.local -j LOG
sudo iptables -I FORWARD 11 -s www.ops.local -j DROP
sudo service iptables save
```
ip -4 -br addr show; ip route show; ip neigh show
### L3_Routing_NAT (22 commands)
```bash
IPTables & Snort
iptables -A INPUT -p udp -j REJECT --reject-with icmp-net-prohibited
iptables -A INPUT -p tcp -j REJECT --reject-with tcp-reset
iptables -A INPUT -p icmp -j DROP
iptables -A INPUT -d 172.24.11.13 \! -i eth0 -j DROP
iptables -A INPUT -p tcp -m state --state ESTABLISHED, RELATED -j ACCEPT
iptables -P INPUT DROP
iptables -t filter -F
iptables -t nat -F
iptables -X
iptables -P INPUT ACCEPT
iptables -P OUTPUT ACCEPT
iptables -P FORWARD ACCEPT
iptables -t filter -A FORWARD -s 172.24.0.0/24 -d 172.24.1.0/24 -i eth0 -o eth1 -j ACCEPT
iptables -A INPUT -i lo -j ACCEPT
iptables -A OUTPUT -o lo -j ACCEPT
iptables -t filter -A INPUT -p tcp --dport 22 -s 10.18.80.64/26 -j ACCEPT
iptables -t filter -A OUTPUT -p tcp --sport 22 -d 10.18.80.64/26 -j ACCEPT
iptables -t filter -A INPUT -p tcp --dport 22 -s 10.18.80.64/26 -m state --state NEW,ESTABLISHED,RELATED -j ACCEPT
iptables -t filter -A OUTPUT -p tcp --sport 22 -d 10.18.80.64/26 -m state --state ESTABLISHED,RELATED -j ACCEPT
iptables -I INPUT 1 -s 172.24.11.13 -p tcp --dport 22 -m state --state NEW,RELATED,ESTABLISHED -j ACCEPT
iptables -I OUTPUT 1 -d 172.24.11.13 -p tcp --sport 22 -m state --state RELATED,ESTABLISHED -j ACCEPT
```
ip -4 -br addr show; ip route show; ip neigh show
### L4_Port_Service (4 commands)
```bash
nmap -n -Pn -sS -p 21,22,23,25,80,110,111,443 198.18.31.253
tcpdump -vv src 192.18.31.253 and dst 172.24.11.15
nmap -n -Pn -sU -p 53,67,123,135,137,138,161,445,631,1434 198.18.31.253
ssh haxor@172.24.11.254
```
ip -4 -br addr show; ip route show; ip neigh show

<!-- CORA-MAXIMIZED-COMMANDS-START -->
## Maximized Windows & Linux Command Examples for `IPtables-Snort-CMDs`

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
