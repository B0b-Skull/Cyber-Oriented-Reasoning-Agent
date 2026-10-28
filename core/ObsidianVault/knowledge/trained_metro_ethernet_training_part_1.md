---
title: "Trained Knowledge & Topology: Metro Ethernet Training_Part_1.pdf"
tags:
  - arp
  - enumeration
  - http
  - https
  - mdp
  - passive_enum
  - pdf
  - ssl
  - tls
  - trained
  - vlan
source_file: Metro Ethernet Training_Part_1.pdf
doc_type: pdf
updated: 2026-10-24 00:59:10
---

# Trained Knowledge & Architecture: `Metro Ethernet Training_Part_1.pdf`

- **Source Path:** `~/Projects/CORA/Training/Metro Ethernet Training_Part_1.pdf` (`pdf`)
- **Extracted Technical Entities:** `arp, http, https, ssl, tls, vlan`
- **Extracted IPs / Subnets:** `1.0.0.0, 1.1.1.2/32, 1.1.1.4/32, 10.0.0.0/30, 127.255.255.255, 128.0.0.0, 191.255.255.255, 192.0.0.0, 223.255.255.255, 224.0.0.0, 239.255.255.255, 240.0.0.0, 255.255.255.255, 6.3.1.2`
- **Extracted Interfaces:** `LO, Lo`
- **Linked Command Playbook:** [[commands/trained_metro_ethernet_training_part_1]] (`4` CEGAR-verified commands | `4` MDP transitions)

## Command & Tactic Coverage Summary
- **Total CEGAR-Verified Commands:** `4` (full executable list in [[commands/trained_metro_ethernet_training_part_1]])
- **Tactic Distribution:** `Enumeration` (3), `Passive_Enum` (1)
- **Top Extracted CLI Tools:** `locate` (2), `ip` (1), `out-of-band` (1)

### Visual & Network Diagram Intelligence (`Metro Ethernet Training_Part_1.pdf#page1`)
- **Spatially Grouped Diagram Nodes (Box/Component Clusters):**
  1. `[TONEX]`
  2. `[METROETHERNET]`
  3. `[PART 1]`

### Visual & Network Diagram Intelligence (`Metro Ethernet Training_Part_1.pdf#page5`)
- **Spatially Grouped Diagram Nodes (Box/Component Clusters):**
  1. `[METROETHERNET | BASICS]`
  2. `[T]`

### Visual & Network Diagram Intelligence (`Metro Ethernet Training_Part_1.pdf#page9`)
- **Spatially Grouped Diagram Nodes (Box/Component Clusters):**
  1. `[THEMETROBOTTLENECK]`
  2. `[Other Sites]`
  3. `[Access]`
  4. `[Metro]`
  5. `[Core Network]`
  6. `[End User]`
  7. `[Access]`
  8. `[Metro]`
  9. `[Core]`

## LLM Distilled Operational Summary
### Operational Techniques & Decision Workflows
- **Service Selection Logic**: Evaluate cost-effectiveness, flexibility, and simplicity when selecting Ethernet services for business, residential, or mobile subscribers.
- **Network Scope Differentiation**: Distinguish between **Metro Ethernet** (point-to-point/multipoint over a MAN) and **Carrier Ethernet** (versatile, evolved scope including MAN/WAN infrastructure).
- **Architecture Design Principles**: Apply the "SIMPLE, SCALABLE, AUTOMATABLE" triad when designing fabric networks (CLOS, Metro/Access, Core).
- **Protocol Hierarchy Implementation**:
  - **Access Layer**: Utilize IS-IS L1 for fixed/mobile access networks.
  - **Aggregation Layer**: Deploy IS-IS L2 for routing within aggregation networks.
  - **Core Layer**: Implement eBGP/iBGP with IPv4+label stacks for hierarchical LSPs and peering fabrics.
- **BGP Configuration Workflow**: Configure `next-hop-self` on Provider Autonomous System Border Routers (ASBRs) and Route Reflectors (RRs) to ensure proper route propagation in hierarchical MPLS environments.

### Critical Command Patterns & Required Flags
- **BGP Next-Hop Self**:
  - Context: Provider Edge (PE) or ASBR interfaces connecting to customer sites.
  - Pattern: `neighbor <IP> next-hop-self`
  - Purpose: Ensures the next-hop attribute remains reachable for downstream routers in iBGP/eBGP hierarchies.
- **Protocol Selection**:
  - Access/Mobile Aggregation: `protocol isis level-1`
  - Core/Aggregation Interconnect: `protocol isis level-2` or `protocol bgp` (depending on LSP type: iBGP or eBGP).

### Network Topology & Relationships
- **Logical Layers**:
  - **End User**: Connects via Access networks.
  - **Access Network**: Typically IS-IS L1 (Fixed/Mobile).
  - **Metro/Aggregation Network**: IS-IS L2 or MPLS LDP/LSP.
  - **Core Network**: eBGP/iBGP with hierarchical LSPs; includes Peering Fabrics.
- **Key Components**:
  - **UNI (User-Network Interface)**: The demarcation point between the service provider and the customer (e.g., 256 Kb to 10 Gbps Ethernet).
  - **FABRIC DESIGNS**: CLOS fabrics for Metro/Access and Core fabrics for scalability.
  - **BGP Roles**:
    - **CN-ASBR**: Core Network AS Border Router.
    - **AGN-ASBR**: Aggregation Network AS Border Router.
    - **RR (Route Reflector)**: Used for iBGP scale (CN-RR, AGN-RR, Inline RR).
- **Transport Technologies**: Frame Relay (legacy/connected branches), Fast Ethernet, and 10 Gbps Ethernet.

## Document Structure & Key Topics
- Visual & Network Diagram Intelligence (`Metro Ethernet Training_Part_1.pdf#page1`)
- Visual & Network Diagram Intelligence (`Metro Ethernet Training_Part_1.pdf#page5`)
- Visual & Network Diagram Intelligence (`Metro Ethernet Training_Part_1.pdf#page9`)

## Extracted Operational Steps & Workflows
- 3. In the middle of the wire between
- 1. At the port of the service provider equipment
- 2. At the port of the customer’s equipment
- 1.
Point to Point EVC: each EVC associates
- 2.
Multipoint to Multipoint EVC: each EVC
- 3.
Rooted Multipoint EVC : each EVC
- 4. In general, E-NNI is represented by the physical Ethernet port on the service provider access

