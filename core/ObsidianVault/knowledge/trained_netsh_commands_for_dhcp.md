---
title: "Trained Knowledge & Topology: Netsh commands for DHCP"
category: knowledge
domain_hub: "[[knowledge/05_windows_and_linux_networking_routing_and_firewalls]]"
os_platform: cross-platform
primary_tactic: L2_L3_Pivot_Routing
summary: "Operational architecture, decision workflows & Windows/Linux command reference for Netsh commands for DHCP: Side-by-side Windows and Linux networking reference covering L2 ARP/neighbors (arp vs ip neigh), L3 routing & forwarding (route/ne"
when_to_apply: "Apply when working with Netsh commands for DHCP (cross-platform): Apply whenever diagnosing network unreachability (`Network is unreachable`, `No route to host`, `Connection timed out`), mapping local/remote subnets (`Engine 2`), configuring cross-subnet static routes/IP forwarding/NAT masquerading (`Engine 6/15/19`), inspecting listening ports (`ss`/`netstat`), or unlocking `iptables`/`nftables`/`netsh advfirewall` rules."
tags: [enumeration, https, mdp, netsh, passive_enum, pdf, trained, windows, linux, cross-platform, iproute2, ipconfig, route, arp, netstat, ss, iptables, nftables, sysctl, ip_forward, masquerade, snort]
source_file: "Netsh commands for DHCP"
updated: 2026-10-30
---

# Trained Knowledge & Architecture: `Netsh commands for DHCP.pdf`

- **Source Path:** `~/Projects/CORA/Training/Netsh commands for DHCP.pdf` (`pdf`)
- **Extracted Technical Entities:** `https, netsh`
- **Extracted IPs / Subnets:** `10.0.0.0, 10.0.0.1, 10.1.1.1, 10.1.1.2, 10.1.1.3, 10.1.1.50, 10.2.1.10, 10.2.1.32, 10.2.1.5, 10.2.2.0, 10.2.2.10, 10.2.2.100, 10.2.2.2, 10.2.2.20, 10.2.2.32, 172.24.0.0, 172.24.0.100, 224.0.0.0, 224.2.2.10, 224.2.2.20, 239.255.255.255, 255.255.255.0`
- **Extracted Interfaces:** `None`
- **Linked Command Playbook:** [[commands/trained_netsh_commands_for_dhcp]] (`14` CEGAR-verified commands | `14` MDP transitions)

## Command & Tactic Coverage Summary
- **Total CEGAR-Verified Commands:** `14` (full executable list in [[commands/trained_netsh_commands_for_dhcp]])
- **Tactic Distribution:** `Enumeration` (11), `Passive_Enum` (3)
- **Top Extracted CLI Tools:** `netsh` (6), `del` (5), `ip` (3)

## LLM Distilled Operational Summary
### Operational Techniques & Decision Workflows

*   **Environment Selection**: Use `netsh dhcp` for managing servers in Wide Area Networks (WANs) or when scripting batch operations for automation. Note that these commands require Windows 2000 Server or later; they are not available on local Windows XP Professional/Home editions without Remote Desktop Connection to a Terminal Server.
*   **Server Authorization Workflow**:
    *   **Add**: Use `add server <DNS> <IP>` to authorize a new DHCP server in Active Directory.
    *   **Delete**: Use `delete server <DNS> <IP>` to remove a server from the authorized list.
*   **Configuration Migration (Clone) Workflow**:
    1.  **Prepare Source**: Reconcile scopes and fix inconsistencies on the source server.
    2.  **Dump**: Execute `[{\\ServerName | IPAddress}] dump > FileName` to export the configuration (e.g., `dhcpcfg.dmp`).
    3.  **Prepare Destination**: Close the DHCP console, delete all default option definitions (`delete optiondef 01`, `76`), and remove user/vendor classes (`del class "..."`).
    4.  **Execute**: Transfer the dump file and run `netsh exec FileName` on the destination server.
    5.  **Finalize**: Reconcile scopes, stop the DHCP service (`net stop dhcpserver`), and restart it (`net start dhcpserver`) to apply changes.

### Critical Command Patterns & Required Flags

*   **Server Management**:
    *   `add server <ServerDNS> <ServerIP>` (Both parameters required).
    *   `delete server <ServerDNS> <ServerIP>` (Both parameters required).
*   **Configuration Export**:
    *   `[{\\ServerName | IPAddress}] dump > [FileName]`.
        *   *Flag/Param*: `[\\ServerName | IPAddress]` specifies the remote target; omit for local.
        *   *Flag/Param*: `> [FileName]` redirects output to a file (e.g., `.dmp`).
*   **Configuration Import**:
    *   `netsh exec <FileName>` (Requires a clean destination state).
*   **Cleanup Prerequisites (for Import)**:
    *   `delete optiondef 01`
    *   `delete optiondef 76`
    *   `del class "Default Routing and Remote Access Class"`
    *   `del class "Default BOOTP Class"`
    *   `del class "Microsoft Windows 2000 Options"`
    *   `del class "Microsoft Windows 98 Options"`
    *   `del class "Microsoft Options"`

### Network Topology & Service Relationships

*   **Active Directory Integration**: Authorization commands (`add server`, `delete server`) interact directly with Active Directory to manage the list of trusted DHCP servers.
*   **Service Lifecycle**: The `exec` command modifies the DHCP database; changes only take effect after the `dhcpserver` service is restarted using `net stop dhcpserver` and `net start dhcpserver`.
*   **Remote Management**: Commands support remote execution via `\\ServerName` or `IPAddress`, enabling management of non-local servers provided the connection (e.g., R

## Extracted Operational Steps & Workflows
- 1. Close the DHCP console at the destination server. Do not reopen the console until after you use
- 2. Delete all default option definitions and any user and vendor classes at the destination server.
- 255.
Examples

<!-- CORA-MAXIMIZED-COMMANDS-START -->
## Maximized Windows & Linux Command Examples for `Netsh commands for DHCP`

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
