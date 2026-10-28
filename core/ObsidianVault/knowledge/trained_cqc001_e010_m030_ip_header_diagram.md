---
title: "Trained Knowledge & Topology: CQC001_E010_M030_IP_Header_Diagram.pdf"
tags:
  - mdp
  - pdf
  - trained
source_file: CQC001_E010_M030_IP_Header_Diagram.pdf
doc_type: pdf
updated: 2026-10-24 00:57:12
---

# Trained Knowledge & Architecture: `CQC001_E010_M030_IP_Header_Diagram.pdf`

- **Source Path:** `~/Projects/CORA/Training/CQC001_E010_M030_IP_Header_Diagram.pdf` (`pdf`)
- **Extracted Technical Entities:** `general`
- **Extracted IPs / Subnets:** `None`
- **Extracted Interfaces:** `None`

## LLM Distilled Operational Summary
### Key Operational Techniques & Decision Workflows
*   **Header Parsing Workflow**: Analyze the 20-byte minimum IPv4 header structure sequentially: Version/IHL, Type of Service, Total Length, Identification, Flags/Fragment Offset, TTL, Protocol, and Header Checksum.
*   **Fragmentation Logic**: Verify that fragmented datagrams have a `Total Length` divisible by 8 bytes. Use the `Fragment Offset` field (measured in 8-byte increments) to reassemble packets at the destination.
*   **Protocol Identification**: Map the `Protocol` field value to the upper-layer transport or routing protocol (e.g., 1=ICMP, 6=TCP, 17=UDP, 89=OSPF).
*   **Flag Evaluation**: Check the `More Fragments` (M) and `Do Not Fragment` (D) bits to determine reassembly requirements or path constraints.

### Critical Command Patterns and Required Flags
*   **Version Field**: Must be `4` for standard IPv4 operations; `6` is valid but outside this specific diagram's scope.
*   **Header Length (IHL)**: Represents the number of 32-bit words in the header. Minimum value is `5` (20 bytes). Multiply by 4 to calculate the exact byte count.
*   **Flags Bitwise Operations**:
    *   `M` bit (More Fragments): Set to `1` if more fragments follow; `0` indicates the last fragment.
    *   `D` bit (Do Not Fragment): Set to `1` to prevent fragmentation of the datagram.
    *   `x` bit: Reserved (historically referred to as the "evil bit").
*   **Checksum Validation**: The `Header Checksum` field must cover the entire IP header; any modification to the header invalidates this checksum.

### Network Topology & Service Relationships
*   **IP Protocol Mappings**:
    *   **1**: ICMP (Internet Control Message Protocol)
    *   **6**: TCP (Transmission Control Protocol)
    *   **17**: UDP (User Datagram Protocol)
    *   **47**: IGMP (Internet Group Management Protocol)
    *   **50**: GRE (Generic Routing Encapsulation)
    *   **51**: ESP (Encapsulating Security Payload)
    *   **57**: AH (Authentication Header)
    *   **88**: EIGRP (Enhanced Interior Gateway Routing Protocol)
    *   **89**: OSPF (Open Shortest Path First)
    *   **115**: L2TP (Layer 2 Tunneling Protocol)
*   **Addressing Structure**: The header contains fixed fields for `Source Address` and `Destination Address`, defining the endpoints of the datagram.
*   **Reference Standard**: All operations align with **RFC 791**, the foundational specification for the Internet Protocol.

