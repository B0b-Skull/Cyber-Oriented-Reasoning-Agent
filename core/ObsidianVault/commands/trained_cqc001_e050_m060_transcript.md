---
title: "Trained Command Playbook: CQC001_E050_M060_transcript.pdf"
tags:
  - arp
  - eth0
  - http
  - https
  - mdp
  - netstat
  - passive_enum
  - pdf
  - reconnaissance
  - ssh
  - trained
source_file: CQC001_E050_M060_transcript.pdf
updated: 2026-10-25 00:58:02
---

# Trained Command Playbook: `CQC001_E050_M060_transcript.pdf`

- **Source Document:** `~/Projects/CORA/Training/CQC001_E050_M060_transcript.pdf`
- **CEGAR Verified Commands:** `4` (`0` malformed/unsafe snippets filtered)
- **MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`):** `4`
- **Discovered IPs/Subnets:** `0.0.0.0, 127.0.0.1, 172.24.11.13, 172.24.11.14, 255.255.255.0`
- **Discovered Interfaces:** `eth0, lo`
- **Related Knowledge Note:** [[knowledge/trained_cqc001_e050_m060_transcript]]

## Distilled MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`)
| Pre-State ($s$) | Tactic ($\tau$) | Technique ($k$) | Tool ($u$) | Post-State ($s'$) | Verified Command ($c$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `ip` | `s_passive_topology_mapped` | `IP address associated with a hostname, and to invoke the command with the target hostname as a` |
| `s_init_unknown` | **`Reconnaissance`** | Domain, DNS, OSINT & Target Footprint Reconnaissance | `nslookup` | `s_passive_topology_mapped` | `nslookup tool has two modes: interactive and non-interactive. Interactive mode allows the user` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `netstat` | `s_passive_topology_mapped` | `netstat -nat (Linux), and` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `netstat` | `s_passive_topology_mapped` | `netstat -an -P tcp (Solaris).` |

## Verified Executable Commands (Grouped by Capability Layer)

### General_System (1 commands)
```bash
nslookup tool has two modes: interactive and non-interactive. Interactive mode allows the user
```

### L3_Routing_NAT (1 commands)
```bash
IP address associated with a hostname, and to invoke the command with the target hostname as a
```

### L4_Port_Service (2 commands)
```bash
netstat -nat (Linux), and
netstat -an -P tcp (Solaris).
```

