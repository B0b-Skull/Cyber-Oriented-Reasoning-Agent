---
title: "Trained Knowledge & Topology: Intro to GMPLS.pdf"
tags:
  - credential_access
  - mdp
  - passive_enum
  - pdf
  - trained
  - volatility
source_file: Intro to GMPLS.pdf
doc_type: pdf
updated: 2026-10-25 00:58:39
---

# Trained Knowledge & Architecture: `Intro to GMPLS.pdf`

- **Source Path:** `~/Projects/CORA/Training/Intro to GMPLS.pdf` (`pdf`)
- **Extracted Technical Entities:** `volatility`
- **Extracted IPs / Subnets:** `172.24.0.1, 172.24.12.1, 172.24.16.1, 172.24.2.1, 172.24.24.1, 172.24.5.1, 172.24.8.1, 47.0.0.0/8, 47.80.55.3, 5.4.3.2`
- **Extracted Interfaces:** `None`
- **Linked Command Playbook:** [[commands/trained_intro_to_gmpls]] (`3` CEGAR-verified commands | `3` MDP transitions)

## Command & Tactic Coverage Summary
- **Total CEGAR-Verified Commands:** `3` (full executable list in [[commands/trained_intro_to_gmpls]])
- **Tactic Distribution:** `Passive_Enum` (2), `Credential_Access` (1)
- **Top Extracted CLI Tools:** `type` (2), `ping` (1)

### Visual & Network Diagram Intelligence (`Intro to GMPLS.pdf#page1`)
- **Spatially Grouped Diagram Nodes (Box/Component Clusters):**
  1. `[TONEX]`
  2. `[Generalized Multiprotocol | Label Switching (GMPLS)]`

## LLM Distilled Operational Summary
### Operational Techniques & Decision Workflows
*   **Control/Data Plane Separation:** Architect GMPLS networks by decoupling control logic from data forwarding to enable seamless convergence between legacy (TDM, ATM) and modern (IP, Optical) domains.
*   **Interface Switching Capability (ISC) Categorization:** Classify heterogeneous Label Switching Routers (LSRs) based on their switching type (Packet, TDM, Lambda, or Fiber) to ensure correct label interpretation and cross-connect programming.
*   **LSP Nesting & Hierarchy:** Design multi-layer paths where Packet LSPs are nested within Layer 2 LSPs, which may be further nested inside TDM LSPs, ensuring interfaces at each tunnel level share identical switching capabilities.
*   **Constraint-Based Routing:** Utilize Enhanced Interior Gateway Protocols (IGPs) like OSPF-TE or IS-IS-TE to distribute topology data alongside constraints (capacity, utilization, resource class, priority, pre-emption) for Traffic Engineering.
*   **Explicit Path Setup:** Employ RSVP-TE or CR-LDP to establish paths where the route is determined by the ingress LSR based on a global topology view and specific QoS/CoS requirements, enabling fast rerouting (target <50ms).

### Critical Command Patterns & Required Flags
*   **Label Advertisement Modes:**
    *   *Downstream Unsolicited:* LSR sends labels without prior request.
    *   *Downstream On-Demand:* LSR sends labels only after receiving a specific request from the upstream neighbor.
*   **Distribution Ordering:** Configure label distribution as either **Ordered** (labels sent only after receiving upstream labels) or **Unordered** (labels sent immediately upon LSP setup).
*   **Protocol Enhancements:**
    *   `OSPF-TE` / `IS-IS-TE`: Add constraint data (Link capacity, Link utilization, Resource class, Priority, Pre-emption) to standard IGP updates.
    *   `RSVP-TE` / `CR-LDP`: Enable explicit constraint-based routing and hop-by-hop binding verification.

### Network Topology & Relationships
*   **Switching Domains:** The control plane must support four distinct switching types: Packet, Time-Division (TDM/SONET/SDH), Wavelength (Lambda/Optical), and Spatial (Fiber/Port).
*   **Reference Points (ASON Framework):**
    *   **UNI (User-Network Interface):** Interaction point for clients (IP, ATM, SONET/SDH) to request switched connections.
    *   **E-NNI (External Network-Network Interface):** Interaction between different administrative domains or operators.
    *   **I-NNI (Internal Network-Network Interface):** Interaction within the same domain.
*   **Generalized Labels:** Extend traditional in-band labels (VCI/VPI) to include time slots, wavelengths, and fiber ports, with node context determining the specific label type expected.

## Document Structure & Key Topics
- Visual & Network Diagram Intelligence (`Intro to GMPLS.pdf#page1`)

## Extracted Operational Steps & Workflows
- Step 1:  LSR creates binding
- Step 2:  LSR communicates
- Step 3:  LSR inserts label
- 1. Liberal Retention Mode
- 2. Conservative Retention Mode

