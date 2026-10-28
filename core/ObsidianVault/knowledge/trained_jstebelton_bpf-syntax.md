---
title: "Trained Knowledge & Topology: JStebelton_BPF-Syntax.pdf"
tags:
  - active_enum
  - eth0
  - http
  - mdp
  - pdf
  - tcpdump
  - trained
source_file: JStebelton_BPF-Syntax.pdf
doc_type: pdf
updated: 2026-10-24 00:58:43
---

# Trained Knowledge & Architecture: `JStebelton_BPF-Syntax.pdf`

- **Source Path:** `~/Projects/CORA/Training/JStebelton_BPF-Syntax.pdf` (`pdf`)
- **Extracted Technical Entities:** `eth0, http, tcpdump`
- **Extracted IPs / Subnets:** `10.10.1.1`
- **Extracted Interfaces:** `eth0`
- **Linked Command Playbook:** [[commands/trained_jstebelton_bpf-syntax]] (`1` CEGAR-verified commands | `1` MDP transitions)

## Command & Tactic Coverage Summary
- **Total CEGAR-Verified Commands:** `1` (full executable list in [[commands/trained_jstebelton_bpf-syntax]])
- **Tactic Distribution:** `Active_Enum` (1)
- **Top Extracted CLI Tools:** `tcpdump` (1)

## LLM Distilled Operational Summary
### 1. Key Operational Techniques & Decision Workflows

*   **Primitive Filtering**: Use high-level primitives (`src`, `dst`, `net`, `port`, `ip`, `tcp`, `icmp`) to quickly isolate traffic by IP address, subnet, or protocol type.
*   **Byte Offset Access**: Access specific fields within a protocol header using the syntax `protocol[byte_offset]`. For example, `ip[9]` accesses the protocol field in the IP header.
*   **Bitmasking for Granularity**: When primitives are insufficient, use bitwise AND operations to isolate specific nibbles or bits within a byte.
    *   **Masking**: Apply a hex mask (e.g., `& 0xF0`) to retain only the high-order nibble or specific bits while discarding others.
    *   **Comparison**: Combine masking with equality checks (e.g., `ip[0] & 0xF0 = 0x04`) to verify specific field values like IP version.
*   **Multi-Byte/Bit Spanning**: Use the `spanning` syntax (e.g., `tcp[2:2]`) to inspect fields that cross byte boundaries or require specific bit counts within a byte.
*   **TCP Flag Analysis**: Target the TCP flags field at byte offset 13. Use masks to isolate specific flags (SYN, FIN, ACK) for anomaly detection, such as identifying simultaneous SYN+FIN packets indicative of port scanning.

### 2. Critical Command Patterns and Required Flags

*   **Exact Byte Match**: `protocol[offset] = hex_value`
    *   Example: `ip[9] = 0x11` (Matches UDP).
*   **Bitwise Masking & Comparison**: `protocol[offset] & hex_mask = hex_value`
    *   Example: `ip[0] & 0xF0 = 0x04` (Matches IPv4).
*   **Range/Comparison Operators**: `<`, `>`, `<=`, `>=`
    *   Example: `tcp[2:2] < 0x14` (TCP destination port less than 20).
*   **Spanning Syntax**: `protocol[offset:span_length]`
    *   Example: `tcp[2:2]` (Accesses 2 bytes starting at offset 2).

### 3. Network Topology & Header Relationships

*   **IP Header Structure**:
    *   **Byte 0**: Contains IP Version (high-order nibble) and Header Length (low-order nibble).
    *   **Byte 9**: Contains the Protocol field (e.g., 6 for TCP, 17 for UDP, 1 for ICMP).
*   **TCP Header Structure**:
    *   **Byte 13**: Contains the Flags field.
        *   **Lower Nibble**: Holds standard flags (FIN, SYN, RST, PSH, ACK, URG).
        *   **High Nibble (Lower 2 bits)**: Holds ECN (Explicit Congestion Notification) flags (CWR, ECE).
*   **Anomaly Detection Context**: Simultaneous setting of SYN and FIN flags (`tcp[13] & 0x3F = 0x03`)

## Extracted Operational Steps & Workflows
- 1. http://en.wikipedia.org/wiki/Berkeley_Packet_Filter
- 2. http://www.gsp.com/cgi‐bin/man.cgi?section=4&topic=bpf
- 3. http://en.wikipedia.org/wiki/IPv4

