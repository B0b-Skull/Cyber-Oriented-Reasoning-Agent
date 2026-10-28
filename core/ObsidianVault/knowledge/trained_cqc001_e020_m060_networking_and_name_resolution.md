---
title: "Trained Knowledge & Topology: CQC001_E020_M060_Networking_and_Name_Resolution.pdf"
tags:
  - arp
  - credential_access
  - enumeration
  - http
  - https
  - ipconfig
  - listdlls
  - mdp
  - netsh
  - netstat
  - passive_enum
  - pdf
  - sysinternals
  - trained
source_file: CQC001_E020_M060_Networking_and_Name_Resolution.pdf
doc_type: pdf
updated: 2026-10-24 00:57:34
---

# Trained Knowledge & Architecture: `CQC001_E020_M060_Networking_and_Name_Resolution.pdf`

- **Source Path:** `~/Projects/CORA/Training/CQC001_E020_M060_Networking_and_Name_Resolution.pdf` (`pdf`)
- **Extracted Technical Entities:** `arp, http, https, ipconfig, listdlls, netsh, netstat, sysinternals`
- **Extracted IPs / Subnets:** `None`
- **Extracted Interfaces:** `None`
- **Linked Command Playbook:** [[commands/trained_cqc001_e020_m060_networking_and_name_resolution]] (`22` CEGAR-verified commands | `22` MDP transitions)

## Command & Tactic Coverage Summary
- **Total CEGAR-Verified Commands:** `22` (full executable list in [[commands/trained_cqc001_e020_m060_networking_and_name_resolution]])
- **Tactic Distribution:** `Passive_Enum` (11), `Credential_Access` (6), `Enumeration` (5)
- **Top Extracted CLI Tools:** `net` (18), `listdlls` (2), `handle` (1), `ipconfig` (1)

### Visual & Network Diagram Intelligence (`CQC001_E020_M060_Networking_and_Name_Resolution.pdf#page8`)
- **Spatially Grouped Diagram Nodes (Box/Component Clusters):**
  1. `[NETWORKING ANDNAME RESOLUTION]`
  2. `[8]`

## LLM Distilled Operational Summary
### Key Operational Techniques & Decision Workflows

*   **Service Management Workflow**: Use `net` commands to inspect, start, stop, pause, or reactivate services. Verify running services with `net start` and manage user accounts via `net user` or `net accounts`.
*   **Connectivity Verification**: Establish IP-level reachability using `ping`. For complex path analysis, utilize `pathping` to compute results over time, or `tracert` to determine the specific hop-by-hop route.
*   **Port & Service Discovery**: Identify active TCP connections and listening ports using `netstat`. Cross-reference with known port services to infer running applications.
*   **Name Resolution Troubleshooting**: Diagnose DNS issues using `nslookup`. Investigate NetBIOS name cache and WINS registration via `nbtstat`. Verify IP-to-Physical address translation tables using `arp`.
*   **Remote Execution**: Leverage `psexec` to execute interactive processes (like `ipconfig`) on remote systems without manual client installation.
*   **Routing & Interface Configuration**: Modify local IP routing tables with `route` and configure interfaces, routes, or filters using `netsh`.

### Critical Command Patterns and Required Flags

*   **`ipconfig`**:
    *   Default: Displays IP address, subnet mask, and default gateway for all adapters.
    *   `ipconfig /all`: Displays full TCP/IP configuration values.
    *   `ipconfig /flushdns`: Refreshes DNS resolver cache.
    *   `ipconfig /registerdns`: Registers DNS names.
*   **`netstat`**:
    *   Default: Lists active TCP connections.
    *   `netstat -a`: Displays all connections and listening ports.
    *   `netstat -n`: Shows addresses and port numbers numerically (no name resolution).
    *   `netstat -e`: Displays Ethernet statistics.
*   **`ping`**:
    *   Default: Sends ICMP Echo Requests.
    *   `ping -t`: Continuously pings until stopped.
    *   `ping -n <count>`: Specifies the number of echo requests.
*   **`nslookup`**:
    *   Default: Interactive mode for DNS testing.
    *   `nslookup <hostname>`: Resolves a specific hostname.
    *   `nslookup -type=<type> <hostname>`: Queries specific record types (A, AAAA, MX, etc.).
*   **`nbtstat`**:
    *   Default: Displays help.
    *   `nbtstat -a <IP>`: Displays NetBIOS name table for a remote computer by IP.
    *   `nbtstat -n`: Displays local NetBIOS name table.
    *   `nbtstat -r`: Displays statistics on NetBIOS name hits (cache).
*   **`arp`**:
    *   Default: Displays current ARP cache.
    *   `arp -d`: Deletes entries from the ARP cache.
    *   `arp -s <IP> <MAC>`: Adds a static entry to the ARP cache.

### Network Topology & Service Relationships

*   **Protocol Stack**: Tools interact with the TCP/IP stack, specifically ICMP (

## Document Structure & Key Topics
- Visual & Network Diagram Intelligence (`CQC001_E020_M060_Networking_and_Name_Resolution.pdf#page8`)

## Extracted Operational Steps & Workflows
- 1. The client application calls a local stub procedure instead of the actual code implementing the procedure. Stubs are
- 2. The server performs the following steps to call the remote procedure:
- 3. The remote procedure then runs, possibly generating output parameters and a return value.
- 4. When the remote procedure is complete, a similar sequence of steps returns the data to the client.
- 5. The client completes the process by accepting the data over the network and returning it to the calling function.

