---
title: "Trained Knowledge & Topology: Metro Ethernet Training_Day_2_MPLS.pdf"
tags:
  - enumeration
  - eth0
  - eth1
  - mdp
  - passive_enum
  - pdf
  - trained
source_file: Metro Ethernet Training_Day_2_MPLS.pdf
doc_type: pdf
updated: 2026-10-25 00:59:01
---

# Trained Knowledge & Architecture: `Metro Ethernet Training_Day_2_MPLS.pdf`

- **Source Path:** `~/Projects/CORA/Training/Metro Ethernet Training_Day_2_MPLS.pdf` (`pdf`)
- **Extracted Technical Entities:** `eth0, eth1`
- **Extracted IPs / Subnets:** `10.1.0.0/24, 10.1.2.0/24, 10.2.1.0/24, 10.2.12.0/24, 10.22.12.0/24, 10.3.0.0/16, 10.3.1.0/24, 10.3.3.0/24, 10.4.12.0/24, 134.5.1.5, 134.5.6.1, 137.204.0.0/16, 149.27.2.0/24, 149.27.2.27, 172.16.1.0, 172.26.1.0, 192.4.2.10, 197.26.15.0/24, 197.26.15.1, 197.26.15.1/32, 20.1.0.0/16, 20.2.0.0/16, 20.2.1.0/28, 20.2.1.2, 20.2.1.2/28, 200.3.2.1, 200.3.2.7, 30.0.0.2, 30.1.1.0/28, 47.1.1.1`
- **Extracted Interfaces:** `eth0, eth1`
- **Linked Command Playbook:** [[commands/trained_metro_ethernet_training_day_2_mpls]] (`4` CEGAR-verified commands | `4` MDP transitions)

## Command & Tactic Coverage Summary
- **Total CEGAR-Verified Commands:** `4` (full executable list in [[commands/trained_metro_ethernet_training_day_2_mpls]])
- **Tactic Distribution:** `Passive_Enum` (3), `Enumeration` (1)
- **Top Extracted CLI Tools:** `ip` (3), `new-generation` (1)

### Visual & Network Diagram Intelligence (`Metro Ethernet Training_Day_2_MPLS.pdf#page1`)
- **Spatially Grouped Diagram Nodes (Box/Component Clusters):**
  1. `[TONEX]`
  2. `[METRO ETHERNET]`
  3. `[PART 2]`

### Visual & Network Diagram Intelligence (`Metro Ethernet Training_Day_2_MPLS.pdf#page4`)
- **Spatially Grouped Diagram Nodes (Box/Component Clusters):**
  1. `[QUESTION AND ANSWER]`
  2. `[Q&A]`

### Visual & Network Diagram Intelligence (`Metro Ethernet Training_Day_2_MPLS.pdf#page5`)
- **Spatially Grouped Diagram Nodes (Box/Component Clusters):**
  1. `[INTRODUCTION TO MPLS]`

## LLM Distilled Operational Summary
### Operational Techniques & Decision Workflows
*   **Layer 2.5 Forwarding Logic**: Decide to operate between OSI Layer 2 and 3 to combine data link switching performance with network layer routing scalability.
*   **Flow Setup & Signaling**: Execute a flow setup process using signaling protocols (e.g., RSVP) before forwarding traffic, as MPLS requires explicit path establishment.
*   **Recursive Label Lookup**: Perform recursive lookups on next-hop addresses to resolve VPN labels from MP-BGP announcements, linking them to specific egress interfaces on originating Provider Routers (PR).
*   **Hierarchical Domain Forwarding**: Utilize label stacking (LIFO) to manage multiple forwarding domains, where higher-level labels aggregate LSPs into tunnels.
*   **Traffic Engineering (TE)**: Apply MPLS to steer traffic along specific paths defined by RSVP TE tunnels, distinct from standard L3 routing tables.

### Critical Command Patterns & Required Flags
*   **Label Format Structure**: Ensure the 32-bit MPLS header contains:
    *   **Label Value (20 bits)**: The actual forwarding label.
    *   **Exp (3 bits)**: Experimental/CoS bits for service class identification.
    *   **S (Stacking Bit, 1 bit)**: Set to `1` if no further labels exist beneath; set to `0` for stacked labels.
    *   **TTL (8 bits)**: Time-to-live value (often initialized to 255 in specific network contexts like GX).
*   **Header Placement**: Insert the MPLS header between the Data-Link (L2) and IP (L3) headers.
*   **Tagging Operations**: Perform "Tag in" at the Ingress Provider Edge (PE) and "Tag out" at the Egress PE, ensuring the label stack is maintained across core routers (P).

### Network Topology & Relationships
*   **Device Roles**:
    *   **PE (Provider Edge)**: Handles ingress/egress tagging, recursive label lookups, and POP (Pop of Packet) operations for VPN labels.
    *   **P (Provider Core)**: Performs label swapping based on the top label without inspecting L3 headers.
*   **Protocol Support**: Compatible with ATM, FR, Ethernet (L2), and all L3 protocols.
*   **Topology Types**: Supports Virtual Private Networking (VPN) and Multi-Protocol Label Switching (MPLS) across Metro Ethernet and Optical/DWDM environments.
*   **Routing Interaction**: MPLS paths may differ from L3 forwarding paths; the "Path Label" is derived from RSVP TE tunnels to the originating PR device.

## Document Structure & Key Topics
- Visual & Network Diagram Intelligence (`Metro Ethernet Training_Day_2_MPLS.pdf#page1`)
- Visual & Network Diagram Intelligence (`Metro Ethernet Training_Day_2_MPLS.pdf#page4`)
- Visual & Network Diagram Intelligence (`Metro Ethernet Training_Day_2_MPLS.pdf#page5`)

