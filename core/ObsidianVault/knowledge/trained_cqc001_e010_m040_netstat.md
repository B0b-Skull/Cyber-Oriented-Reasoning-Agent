---
title: "Trained Knowledge & Topology: CQC001_E010_M040_Netstat.pdf"
tags:
  - eth0
  - eth2
  - http
  - https
  - mdp
  - netstat
  - passive_enum
  - pdf
  - ssh
  - trained
source_file: CQC001_E010_M040_Netstat.pdf
doc_type: pdf
updated: 2026-10-24 00:57:25
---

# Trained Knowledge & Architecture: `CQC001_E010_M040_Netstat.pdf`

- **Source Path:** `~/Projects/CORA/Training/CQC001_E010_M040_Netstat.pdf` (`pdf`)
- **Extracted Technical Entities:** `eth0, eth2, http, https, netstat, ssh`
- **Extracted IPs / Subnets:** `0.0.0.0, 10.99.99.1, 101.101.34.101, 101.11.169.230, 101.174.100.22, 172.24.1.0, 172.24.1.1, 172.24.185.75, 255.255.0.0, 255.255.255.0`
- **Extracted Interfaces:** `eth0, eth2, lo`
- **Linked Command Playbook:** [[commands/trained_cqc001_e010_m040_netstat]] (`21` CEGAR-verified commands | `21` MDP transitions)

## Command & Tactic Coverage Summary
- **Total CEGAR-Verified Commands:** `21` (full executable list in [[commands/trained_cqc001_e010_m040_netstat]])
- **Tactic Distribution:** `Passive_Enum` (21)
- **Top Extracted CLI Tools:** `netstat` (21)

## LLM Distilled Operational Summary
### Key Operational Techniques & Decision Workflows

*   **Rapid Connection Audit**: Use `netstat -a -n` to list all active connections and listening ports without DNS resolution, speeding up execution for immediate triage.
*   **Interface Health Verification**: Execute `netstat -e` to inspect interface statistics. Analyze "Discards" and "Errors" to distinguish between local host overload (high receive discards) and physical link issues (high send errors).
*   **Protocol-Specific Diagnostics**: Combine `-s` with `-p <protocol>` (e.g., `netstat -s -p tcp`) to isolate statistics for specific protocols, reducing noise in large output sets.
*   **Routing Table Inspection**: Use `netstat -r` to verify persistent routes and current routing table contents.
*   **Dynamic Monitoring**: Utilize the interval switch (e.g., `netstat -s -i 5`) to refresh statistics every 5 seconds, allowing real-time observation of connection states until stopped with `CTRL-C`.
*   **Unix Domain Socket Analysis**: On Linux/Unix systems, use `netstat -a | more` and filter for `unix` types to inspect local socket paths (e.g., `/var/run/acpid.socket`) and their states.

### Critical Command Patterns and Required Flags

| Switch | Function |
| :--- | :--- |
| `-a` | Displays **all** connections and listening ports. |
| `-n` | Forces numeric output (IP/Port) instead of resolving names; improves performance. |
| `-r` | Displays the IP routing table. |
| `-s` | Displays detailed protocol statistics (TCP, UDP, IP, ICMP). |
| `-p <proto>` | Filters output to a specific protocol (TCP, UDP, IP, or ICMP). |
| `-e` | Displays Ethernet interface statistics. |
| `-i <seconds>` | Refreshes statistics at a specified interval. |

### Network Topology & Service Relationships

*   **Local Host Identity**: The sample environment identifies the local host as `10.99.99.1`.
*   **Listening Services (TCP)**:
    *   **Standard Ports**: 42, 88, 135, 389, 445, 593, 1038, 1041, 1048, 1723, 3268.
    *   **Directory Services**: Ports 135 (RPC), 389 (LDAP), 445 (SMB), 593 (RPC-EPMA), and 3268 (Global Catalog) suggest an Active Directory or similar directory infrastructure role.
    *   **Remote Access**: Port 1723 indicates PPTP VPN capability.
*   **Listening Services (UDP)**:
    *   Ports 135, 445, 1087, 53 (DNS), 137, and 138 indicate NetBIOS/DNS traffic.
*   **Established Connections**:
    *   A bidirectional ESTABLISHED connection exists on port 389 (LDAP) between the local host and itself

## Document Structure & Key Topics
- netsat -a --numeric-ports
- netsat -a --numeric-hosts
- netsat -a --numeric-users

## Extracted Operational Steps & Workflows
- 1. List All Ports (both listening and non-listening ports)
- 2. List Sockets which are in Listening State
- 3. Show the statistics for each protocol
- 4. Display PID and program names in netstat output using netstat -p
- 5. Don’t resolve host, port and user name in netstat output
- 6. Print netstat information continuously
- 7. Find the non-supportive Address families in your system
- 8. Display the kernel routing information using netstat -r
- 9. Find out on which port a program is running
- 10. Show the list of network interfaces

