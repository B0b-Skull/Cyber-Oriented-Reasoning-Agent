---
title: "Trained Knowledge & Topology: SD-WAN ATT.pdf"
tags:
  - mdp
  - pdf
  - trained
source_file: SD-WAN ATT.pdf
doc_type: pdf
updated: 2026-10-24 01:00:24
---

# Trained Knowledge & Architecture: `SD-WAN ATT.pdf`

- **Source Path:** `~/Projects/CORA/Training/SD-WAN ATT.pdf` (`pdf`)
- **Extracted Technical Entities:** `general`
- **Extracted IPs / Subnets:** `None`
- **Extracted Interfaces:** `None`

## LLM Distilled Operational Summary
### Key Operational Techniques & Decision Workflows
*   **Topology Selection**: Choose between Over-the-Top (OTT) models using VeloCloud Appliances or Network-Based models utilizing the AT&T FlexWare Device for hosting Virtual Network Functions (VNFs).
*   **Link Aggregation Strategy**: Implement transport-agnostic overlays by mixing and matching link types (MPLS, Ethernet, Broadband/DIA, 4G/LTE) to optimize cost and performance.
*   **Dynamic Bandwidth Adjustment**: Leverage Software-Defined Networking (SDN) capabilities on AT&T Integrated Cloud nodes to automatically adjust gateway bandwidth in response to site capacity changes.
*   **Hybrid Deployment**: Seamlessly integrate SD-WAN sites with existing non-SD-WAN sites within the same network fabric.

### Critical Command Patterns and Required Flags
*   **Device Provisioning**: Deploy either a physical **VeloCloud Appliance** or a **1G/10M Device** running the **VeloCloud SD-WAN VNF** on FlexWare hardware.
*   **Security Integration**: Configure **vFirewall VNF** and **vRouter VNF** instances directly on the FlexWare platform for unified security and routing.
*   **Tunnel Termination**: Establish **IPSec Tunnels** between the SD-WAN Gateway and cloud providers or remote sites over public or private transports.
*   **Service Orchestration**: Utilize the **AT&T NetBond©** service to manage and adjust bandwidth dynamically across the network.

### Network Topology, IP/Subnet, Serial, and Service Relationships
*   **Primary Hardware**: The **AT&T FlexWare Device** serves as the universal CPE (Customer Premises Equipment), supporting multiple VNFs including SD-WAN, Firewall, and Router functions.
*   **Transport Links**: Supports four primary link types: **MPLS**, **Ethernet** (Broadband/DIA), **Dual Internet**, and **Mobile (4G/LTE)**.
*   **Service Models**:
    *   **Hosted SD-WAN Gateway**: Centralized management point for the overlay network.
    *   **SD-WAN OTT**: Software-defined overlay running on top of any transport (public or private).
    *   **AT&T VPN**: Provides secure connectivity alongside Internet links.
*   **Geographic Scope**: Solutions are available in over 200 countries and territories, with specific focus on the US midmarket segment for high growth potential.
*   **Key Benefits Alignment**: Deployments target cost savings, agility, improved application performance, faster time-to-market, visibility/control, security, mobility, and unified communications.

## Extracted Operational Steps & Workflows
- 1. Cost Savings
- 2. Agility and Flexibility
- 3. Improved Application Performance
- 4. Faster time-to-market
- 5. Visibility & Control
- 1. Over the top model
- 2. Network-based model

