---
title: "Trained Knowledge & Topology: PON-GPON.pdf"
tags:
  - http
  - mdp
  - pdf
  - trained
source_file: PON-GPON.pdf
doc_type: pdf
updated: 2026-10-25 01:00:05
---

# Trained Knowledge & Architecture: `PON-GPON.pdf`

- **Source Path:** `~/Projects/CORA/Training/PON-GPON.pdf` (`pdf`)
- **Extracted Technical Entities:** `http`
- **Extracted IPs / Subnets:** `None`
- **Extracted Interfaces:** `None`

### Visual & Network Diagram Intelligence (`PON-GPON.pdf#page1`)
- **Spatially Grouped Diagram Nodes (Box/Component Clusters):**
  1. `[TONEX]`
  2. `[PON | GPON]`

### Visual & Network Diagram Intelligence (`PON-GPON.pdf#page4`)
- **Spatially Grouped Diagram Nodes (Box/Component Clusters):**
  1. `[ONU | ONU | SPLITTER]`
  2. `[ONU]`
  3. `[ONU]`
  4. `[ONU]`
  5. `[ONU]`
  6. `[SPUTTER | SPLTTER]`
  7. `[OLT | DATA | VOICE | 三0 | SPLITTER | VIDEO]`
  8. `[ONU]`
  9. `[GPON (Gigabit Ethernet Passive Optical]`
  10. `[Network)]`

### Visual & Network Diagram Intelligence (`PON-GPON.pdf#page5`)
- **Spatially Grouped Diagram Nodes (Box/Component Clusters):**
  1. `[GPON(GIGABITPASSIVEOPTICAL | NETWORK)]`

## LLM Distilled Operational Summary
### Key Operational Techniques & Decision Workflows
*   **Technology Selection**: Choose **GPON** (ITU-T G.984) for high-efficiency triple-play services (Data, Voice, Video) requiring native TDM/Ethernet transport. Select **EPON** (IEEE 802.3ah/av) if the primary focus is symmetric Ethernet transport at lower costs.
*   **Topology Design**: Utilize passive splitters to support up to **64 ONTs** per fiber (standard) or **128 ONTs** (extended), enabling high-density urban deployment without active equipment in the access network.
*   **Bandwidth Allocation**: Implement **Time Division Multiplexing (TDM)** for upstream channels with dynamic bandwidth allocation, while broadcasting the downstream channel to all ONTs.
*   **Service Convergence**: Adapt metropolitan ring traffic (Voice/Data/Video) into the PON transport layer using an **OLT** at the Central Office (CO).
*   **Security Implementation**: Enforce **128-bit AES encryption** on the downstream channel to guarantee security.

### Critical Command Patterns and Required Flags
*   **Wavelength Configuration**:
    *   **Downstream**: `1490 nm` (2.488 Gbps)
    *   **Upstream**: `1310 nm` (1.244 Gbps)
    *   *Note*: Some variants may use `1550 nm` for downstream video transport.
*   **Standard Compliance Flags**:
    *   **ITU-T G.984** (Class B+ recommended for standard deployments).
    *   **IEEE 802.3ah** (EPON 1.25G) or **IEEE 802.3av** (10G EPON).
*   **Physical Layer Constraints**: Ensure fiber span distance does not exceed **20 km**.

### Network Topology & Relationships
*   **Core Components**:
    *   **OLT (Optical Line Terminal)**: Located at the CO; interfaces with the metro ring and manages traffic adaptation.
    *   **ONU/ONT (Optical Network Unit/Termination)**: Located at customer premises (ONT) or outside the home (ONU); converts optical signals to electrical signals.
    *   **PON Splitters**: Passive components arranged in star, ring, or tree configurations to serve multiple subscribers.
*   **Service Mapping**:
    *   **Data**: IP/Ethernet transport.
    *   **Voice**: Native TDM formats.
    *   **Video**: Delivered via 1490/1550 nm wavelengths.
*   **Architecture Context**: GPON fits within Carrier Ethernet architectures (E-Line, E-LAN) and supports migration from copper to fiber, including legacy ATM-based PONs (APON/BPON) evolution paths.

## Document Structure & Key Topics
- Visual & Network Diagram Intelligence (`PON-GPON.pdf#page1`)
- Visual & Network Diagram Intelligence (`PON-GPON.pdf#page4`)
- Visual & Network Diagram Intelligence (`PON-GPON.pdf#page5`)

