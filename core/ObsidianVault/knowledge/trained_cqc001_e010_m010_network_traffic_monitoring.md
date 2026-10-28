---
title: "Trained Knowledge & Topology: CQC001_E010_M010_Network_Traffic_Monitoring.pdf"
tags:
  - https
  - mdp
  - passive_enum
  - pdf
  - trained
source_file: CQC001_E010_M010_Network_Traffic_Monitoring.pdf
doc_type: pdf
updated: 2026-10-24 00:57:12
---

# Trained Knowledge & Architecture: `CQC001_E010_M010_Network_Traffic_Monitoring.pdf`

- **Source Path:** `~/Projects/CORA/Training/CQC001_E010_M010_Network_Traffic_Monitoring.pdf` (`pdf`)
- **Extracted Technical Entities:** `https`
- **Extracted IPs / Subnets:** `172.16.1.84, 172.16.1.85, 172.16.1.86, 172.16.10.2`
- **Extracted Interfaces:** `None`
- **Linked Command Playbook:** [[commands/trained_cqc001_e010_m010_network_traffic_monitoring]] (`1` CEGAR-verified commands | `1` MDP transitions)

## Command & Tactic Coverage Summary
- **Total CEGAR-Verified Commands:** `1` (full executable list in [[commands/trained_cqc001_e010_m010_network_traffic_monitoring]])
- **Tactic Distribution:** `Passive_Enum` (1)
- **Top Extracted CLI Tools:** `ip` (1)

## LLM Distilled Operational Summary
### Key Operational Techniques & Decision Workflows
*   **Flow Definition & Grouping**: Configure flows by matching unidirectional packet attributes: Source/Dest IP, Source/Dest Port, Class of Service, Layer 3 Protocol, and Interface. A new flow record is generated for any parameter variation.
*   **Sampling Strategy**: On high-traffic routers, enable sampled NetFlow (e.g., 1 in N packets) to reduce performance impact while maintaining visibility.
*   **Cache Management**: Monitor the NetFlow cache (default check interval: 1 second). Configure export timers to periodically flush expired flow records to a collector.
*   **Collector Architecture**: Deploy a NetFlow Collector server to receive and aggregate datagrams (max 30 flows per datagram) from multiple devices for analysis.

### Critical Command Patterns & Required Flags
*   **Enabling NetFlow on Cisco IOS**:
    ```bash
    Router(config)# ip flow-export version 5
    Router(config)# interface GigabitEthernet0/1
    Router(config-if)# ip flow-export version 5
    Router(config-if)# ip flow-cache timeout active 300 inactive 60
    ```
*   **Sampling Configuration**:
    ```bash
    Router(config)# ip flow-export version 5
    Router(config)# interface GigabitEthernet0/1
    Router(config-if)# ip flow-export sampling 1000  # Sample 1 in 1000 packets
    ```
*   **Version Selection**: Use `version 5` for legacy IPv4 compatibility or `version 9` (IPFIX) for IPv6 support and template extensibility.

### Network Topology & Device Relationships
*   **Supported Vendors & Models**:
    *   **Cisco**: Most IOS devices (excluding 2900, 3500, 3660, 3750 series).
    *   **Juniper**: M/T/MX-series (DPC), MX-series/FPC5 (T4000).
    *   **Alcatel-Lucent**: 7750SR.
    *   **Enterasys/Nortel**: S/N-Series, ERS5510/5520/5530/8600.
    *   **Huawei**: NE5000E, NE40E/X, NE80E.
    *   **Flowmon**: Probes 1000–100000 series.
*   **Protocol Evolution**:
    *   **v5**: Legacy standard, IPv4 only, widely deployed.
    *   **v9 (IPFIX)**: Current standard, template-based, supports IPv4/IPv6, extensible.
    *   **v7/v8**: Specialized for Catalyst switches and router aggregation respectively.

## Extracted Operational Steps & Workflows
- 3750. Moreover, NetFlow is available for many routers and switches of other vendors.

