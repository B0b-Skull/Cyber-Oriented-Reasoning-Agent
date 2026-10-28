---
title: "Trained Knowledge & Topology: BPF syntax.pdf"
tags:
  - arp
  - http
  - https
  - mdp
  - pdf
  - tcpdump
  - trained
  - vlan
source_file: BPF syntax.pdf
doc_type: pdf
updated: 2026-10-24 00:57:01
---

# Trained Knowledge & Architecture: `BPF syntax.pdf`

- **Source Path:** `~/Projects/CORA/Training/BPF syntax.pdf` (`pdf`)
- **Extracted Technical Entities:** `arp, http, https, tcpdump, vlan`
- **Extracted IPs / Subnets:** `172.24.1.0, 192.9.200.1, 255.0.0.0, 255.255.0.0, 255.255.255.0, 255.255.255.255`
- **Extracted Interfaces:** `None`

## LLM Distilled Operational Summary
### Key Operational Techniques & Decision Workflows

*   **Expression Construction**: Build filters using one or more primitives combined with logical operators (`and`, `or`, `not`). Primitives follow the pattern: `[type] [dir] [proto] [id]`.
    *   *Type Qualifiers*: Define the scope (e.g., `host`, `net`, `port`, `portrange`). Default is `host` if omitted.
    *   *Direction Qualifiers*: Specify flow direction (`src`, `dst`, `src or dst`). Default is `src or dst`.
    *   *Protocol Qualifiers*: Restrict to specific layers (`ether`, `ip`, `tcp`, `udp`, `arp`, etc.). Default includes all protocols consistent with the type.
*   **Logical Simplification**: Omit identical qualifier lists in `or` conditions to reduce typing (e.g., `tcp dst port ftp or domain` implies `tcp` for both).
*   **Link Layer Handling**:
    *   `ether`, `fddi`, `tr`, and `wlan` are treated identically as the data link level.
    *   For 802.11 (`wlan`), only Destination Address (DA) and Source Address (SA) fields are testable; BSSID, RA, and TA are ignored.
*   **Gateway Detection**: Use `gateway host` to identify packets where the Ethernet header references a specific host, but the IP header does not (indicating a gateway role). Requires resolution via DNS/NIS and `/etc/ethers`.

### Critical Command Patterns and Required Flags

*   **Host Matching**:
    *   `dst host <addr>`: Match IPv4/v6 destination.
    *   `src host <addr>`: Match IPv4/v6 source.
    *   `host <addr>`: Match either source or destination.
    *   `ip host <addr>`: Explicitly restrict to IP layer (equivalent to `ether proto ip and host`).
*   **Network Matching**:
    *   `dst net <net>` / `src net <net>`: Match specific network numbers.
    *   `net <net> mask <mask>`: Match with a specific netmask (IPv4 only; IPv6 requires full address).
    *   `net <net>/<len>`: Match with CIDR-style length (e.g., `/24`).
*   **Port Matching**:
    *   `dst port <num>`: Match destination port.
    *   `portrange <start>-<end>`: Match a range of ports.
*   **Special Keywords**: `gateway`, `broadcast`, `less`, `greater`, and arithmetic expressions are valid primitives outside the standard type/dir/proto/id pattern.

### Network Topology & Service Relationships

*   **Address Resolution**: Host names require resolution via `/etc/hosts`, DNS, or NIS. Ethernet addresses can be resolved via `/etc/ethers`.
*   **Network Number Formats**:
    *   IPv4 supports dotted-quad, dotted-triple, dotted-pair, and single-number formats with implicit masks (e.g., `172.24.1` implies `/24`).
    *   IPv6 requires full address notation; "

