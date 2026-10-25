---
title: "Trained Command Playbook: CQC001_E010_M030_transcript.pdf"
tags:
  - active_enum
  - eth0
  - mdp
  - passive_enum
  - pdf
  - tcpdump
  - trained
  - wireshark
source_file: CQC001_E010_M030_transcript.pdf
updated: 2026-10-25 00:57:13
---

# Trained Command Playbook: `CQC001_E010_M030_transcript.pdf`

- **Source Document:** `~/Projects/CORA/Training/CQC001_E010_M030_transcript.pdf`
- **CEGAR Verified Commands:** `7` (`0` malformed/unsafe snippets filtered)
- **MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`):** `7`
- **Discovered IPs/Subnets:** `0.0.0.0, 1.1.1.1, 1.2.3.4, 1.2.3.4/8, 10.0.0.0/8, 10.11.12.0/25, 127.0.0.0/8, 127.0.0.1, 130.1.0.0, 130.1.1.1, 169.254.0.0/16, 172.16.0.0/12, 172.24.0.0/16, 172.24.11.110, 172.24.111.0/24, 172.24.111.4, 172.24.15.0/24, 172.24.15.64/26, 172.24.200.15, 2.2.2.2, 255.255.255.255`
- **Discovered Interfaces:** `eth0`
- **Related Knowledge Note:** [[knowledge/trained_cqc001_e010_m030_transcript]]

## Distilled MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`)
| Pre-State ($s$) | Tactic ($\tau$) | Technique ($k$) | Tool ($u$) | Post-State ($s'$) | Verified Command ($c$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `ip` | `s_passive_topology_mapped` | `IP address is the network ID. In the original Internet implementation, the first octet was always the` |
| `s_passive_topology_mapped` | **`Active_Enum`** | Active Network, Cloud, Directory Service & Endpoint Probing | `tcpdump` | `s_active_services_enumerated` | `tcpdump -vnni eth0 host 1.1.1.1` |
| `s_passive_topology_mapped` | **`Active_Enum`** | Active Network, Cloud, Directory Service & Endpoint Probing | `tcpdump` | `s_active_services_enumerated` | `tcpdump -vnni eth0 ip` |
| `s_passive_topology_mapped` | **`Active_Enum`** | Active Network, Cloud, Directory Service & Endpoint Probing | `tcpdump` | `s_active_services_enumerated` | `tcpdump -vnni eth0 dst host 2.2.2.2` |
| `s_passive_topology_mapped` | **`Active_Enum`** | Active Network, Cloud, Directory Service & Endpoint Probing | `tcpdump` | `s_active_services_enumerated` | `tcpdump -vnni eth0 host 172.24.11.110 and 172.24.111.4` |
| `s_passive_topology_mapped` | **`Active_Enum`** | Active Network, Cloud, Directory Service & Endpoint Probing | `tcpdump` | `s_active_services_enumerated` | `tcpdump -vnni eth0 host 172.24.11.110 and host 172.24.111.4` |
| `s_passive_topology_mapped` | **`Active_Enum`** | Active Network, Cloud, Directory Service & Endpoint Probing | `tcpdump` | `s_active_services_enumerated` | `tcpdump -vnni eth0 host 172.24.11.110 and net 172.24.111.0/24` |

## Verified Executable Commands (Grouped by Capability Layer)

### L3_Routing_NAT (1 commands)
```bash
IP address is the network ID. In the original Internet implementation, the first octet was always the
```

### L4_Port_Service (6 commands)
```bash
tcpdump -vnni eth0 host 1.1.1.1
tcpdump -vnni eth0 ip
tcpdump -vnni eth0 dst host 2.2.2.2
tcpdump -vnni eth0 host 172.24.11.110 and 172.24.111.4
tcpdump -vnni eth0 host 172.24.11.110 and host 172.24.111.4
tcpdump -vnni eth0 host 172.24.11.110 and net 172.24.111.0/24
```

