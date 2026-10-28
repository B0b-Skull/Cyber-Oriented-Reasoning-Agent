---
title: "Trained Knowledge & Topology: CQC001_E010_M060_Spanning_Tree_Protocol.pdf"
tags:
  - enumeration
  - mdp
  - pdf
  - trained
  - vlan
source_file: CQC001_E010_M060_Spanning_Tree_Protocol.pdf
doc_type: pdf
updated: 2026-10-24 00:57:30
---

# Trained Knowledge & Architecture: `CQC001_E010_M060_Spanning_Tree_Protocol.pdf`

- **Source Path:** `~/Projects/CORA/Training/CQC001_E010_M060_Spanning_Tree_Protocol.pdf` (`pdf`)
- **Extracted Technical Entities:** `vlan`
- **Extracted IPs / Subnets:** `None`
- **Extracted Interfaces:** `None`
- **Linked Command Playbook:** [[commands/trained_cqc001_e010_m060_spanning_tree_protocol]] (`1` CEGAR-verified commands | `1` MDP transitions)

## Command & Tactic Coverage Summary
- **Total CEGAR-Verified Commands:** `1` (full executable list in [[commands/trained_cqc001_e010_m060_spanning_tree_protocol]])
- **Tactic Distribution:** `Enumeration` (1)
- **Top Extracted CLI Tools:** `interface` (1)

## LLM Distilled Operational Summary
### 1. Key Operational Techniques & Decision Workflows

*   **Root Bridge Election**: The switch with the lowest Bridge ID (Priority + System ID Extension + MAC Address) becomes the Root. Tie-breaking follows: Lowest Priority → Lowest System ID (VLAN ID for PVST+/RPVST+) → Lowest MAC.
*   **Port Role Selection**:
    *   **Root Port**: Selected on non-root bridges as the path with the lowest cumulative cost to the Root.
    *   **Designated Port**: Selected per segment; if costs are equal, the lowest sender Bridge ID and Port ID break ties.
    *   **Blocking/Alternate/Backup**: All other ports block to prevent loops. RSTP adds Alternate (alternate root path) and Backup (loop-back to same root) roles.
*   **Topology Convergence**:
    *   **Legacy STP (802.1D)**: Slow convergence (Listening 15s + Learning 15s).
    *   **RSTP (802.1w)**: Fast convergence using Discarding/Listening/Learning states mapped to Blocking/Listening/Learning. Uses Point-to-Point/Shared link types and Edge ports.
    *   **MST (802.1s)**: Maps multiple VLANs to a single MST Instance (MSTI); election happens per instance.

### 2. Critical Command Patterns & Required Flags

**PVST+/RPVST+ Configuration (Cisco IOS)**
```bash
spanning-tree mode {pvst | rapid-pvst}
spanning-tree vlan 1-4094 priority 32768
spanning-tree vlan 1-4094 hello-time 2 forward-time 15 max-age 20
spanning-tree backbonefast
spanning-tree uplinkfast
interface FastEthernet0/1
  spanning-tree [vlan 1-4094] port-priority 128
  spanning-tree [vlan 1-4094] cost 19
  spanning-tree link-type point-to-point
  spanning-tree portfast
  spanning-tree guard {loop | root | none}
  spanning-tree bpduguard enable
  spanning-tree bpdufilter enable
```

**MST Configuration**
```bash
spanning-tree mode mst
spanning-tree mst configuration
  name MyTree
  revision 1
  instance 1 vlan 20,30
  instance 2 vlan 40,50
  exit
spanning-tree mst 1 priority 32768
spanning-tree mst hello-time 2 forward-time 15 max-age 20 max-hops 20
interface FastEthernet0/1
  spanning-tree mst 1 port-priority 128
  spanning-tree mst 1 cost 19
```

**Troubleshooting**
```bash
show spanning-tree [summary | detail | root]
show spanning-tree [interface | vlan]
show spanning-tree mst [...]
```

### 3. Network Topology & Parameter Relationships

*   **Bridge ID Structure**: 4-bit Priority + 12-bit System ID Extension (VLAN ID for PVST+/RPVST

