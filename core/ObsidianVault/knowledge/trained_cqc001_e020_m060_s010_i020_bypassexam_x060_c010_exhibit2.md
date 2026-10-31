---
title: "Trained Knowledge & Topology: CQC001 E020 M060 S010 I020 BypassExam X060 C010 exhibit2"
category: knowledge
domain_hub: "[[knowledge/05_windows_and_linux_networking_routing_and_firewalls]]"
os_platform: cross-platform
primary_tactic: L2_L3_Pivot_Routing
summary: "Operational architecture, decision workflows & Windows/Linux command reference for CQC001 E020 M060 S010 I020 BypassExam X060 C010 exhibit2: Side-by-side Windows and Linux networking reference covering L2 ARP/neighbors (arp vs ip neigh), L3 routing & forwarding (route/ne"
when_to_apply: "Apply when working with CQC001 E020 M060 S010 I020 BypassExam X060 C010 exhibit2 (cross-platform): Apply whenever diagnosing network unreachability (`Network is unreachable`, `No route to host`, `Connection timed out`), mapping local/remote subnets (`Engine 2`), configuring cross-subnet static routes/IP forwarding/NAT masquerading (`Engine 6/15/19`), inspecting listening ports (`ss`/`netstat`), or unlocking `iptables`/`nftables`/`netsh advfirewall` rules."
tags: [mdp, pdf, trained, windows, linux, cross-platform, iproute2, ipconfig, route, arp, netstat, ss, netsh, iptables, nftables, sysctl, ip_forward, masquerade, snort, firewall, l2_l3_pivot_routing, defense_evasion_firewall]
source_file: "CQC001 E020 M060 S010 I020 BypassExam X060 C010 exhibit2"
updated: 2026-10-30
---

# Trained Knowledge & Architecture: `CQC001_E020_M060_S010_I020_BypassExam_X060_C010_exhibit2.pdf`

- **Source Path:** `~/Projects/CORA/Training/CQC001_E020_M060_S010_I020_BypassExam_X060_C010_exhibit2.pdf` (`pdf`)
- **Extracted Technical Entities:** `general`
- **Extracted IPs / Subnets:** `0.0.0.0, 104.64.57.171, 127.0.0.1, 172.16.1.168, 172.24.1.120, 172.24.1.243, 172.24.2.112, 172.24.5.1, 172.24.56.1, 31.13.73.1, 54.88.232.60`
- **Extracted Interfaces:** `None`

## LLM Distilled Operational Summary
### Key Operational Techniques & Decision Workflows

*   **Process Identification via PID Mapping**: Correlate high-risk ports (e.g., 135, 445) with specific PIDs to identify the owning service.
    *   `PID 4` owns critical SMB/NetBIOS services (Ports 135, 445, 139, 137, 138).
    *   `PID 1096` handles multiple active HTTPS connections (Port 443).
    *   `PID 1616` manages dynamic high ports (47163, 49152+) and IPv6 equivalents.
*   **Connection State Analysis**: Differentiate between active data transfer (`ESTABLISHED`) and potential zombie processes or connection leaks (`CLOSE_WAIT`, `SYN_SENT`).
    *   Multiple `CLOSE_WAIT` states on Port 443 (e.g., to `104.64.57.171`) indicate a specific application failing to close sockets properly.
*   **Network Segmentation Verification**: Confirm traffic flow between distinct subnets.
    *   Internal-to-Internal: `172.24.1.120` ↔ `172.24.1.243` (SMB).
    *   Internal-to-External: `172.24.1.120` ↔ `31.13.73.1` (HTTPS).

### Critical Command Patterns and Required Flags

*   **Port Scanning & Service Enumeration**:
    *   `netstat -ano` (Windows): Displays active connections with Process IDs (PID) for immediate process lookup via Task Manager.
    *   `netstat -aon | findstr "ESTABLISHED"`: Isolates active sessions for analysis.
*   **Process Investigation**:
    *   `tasklist | findstr <PID>`: Identifies the executable name associated with a specific PID (e.g., PID 4 is typically `svchost.exe` hosting `LSASS` or `SPSVC`).
*   **IPv6/Loopback Verification**:
    *   Check `[::]` and `[::1]` bindings to ensure services are listening on all interfaces or restricted to localhost.

### Network Topology, IP/Subnet, and Service Relationships

*   **Primary Host**: `172.24.1.120` (Likely a Domain Controller or File Server given the SMB stack).
*   **Key Subnets**:
    *   `172.24.1.x`: Primary internal network segment.
    *   `172.24.5.x`: Secondary internal segment (Port 139 listening).
    *   `172.24.56.x`: Tertiary internal segment (UDP 137/138/1900).
*   **External Services**:
    *   `31.13.73.1:443` & `104.64.57.171:443`: Active HTTPS clients (Potential web

<!-- CORA-MAXIMIZED-COMMANDS-START -->
## Maximized Windows & Linux Command Examples for `CQC001 E020 M060 S010 I020 BypassExam X060 C010 exhibit2`

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
