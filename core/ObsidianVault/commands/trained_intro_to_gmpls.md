---
title: "Trained Command Playbook: Intro to GMPLS.pdf"
tags:
  - credential_access
  - mdp
  - passive_enum
  - pdf
  - trained
  - volatility
source_file: Intro to GMPLS.pdf
updated: 2026-10-25 00:58:39
---

# Trained Command Playbook: `Intro to GMPLS.pdf`

- **Source Document:** `~/Projects/CORA/Training/Intro to GMPLS.pdf`
- **CEGAR Verified Commands:** `3` (`0` malformed/unsafe snippets filtered)
- **MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`):** `3`
- **Discovered IPs/Subnets:** `172.24.0.1, 172.24.12.1, 172.24.16.1, 172.24.2.1, 172.24.24.1, 172.24.5.1, 172.24.8.1, 47.0.0.0/8, 47.80.55.3, 5.4.3.2`
- **Discovered Interfaces:** `None`
- **Related Knowledge Note:** [[knowledge/trained_intro_to_gmpls]]

## Distilled MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`)
| Pre-State ($s$) | Tactic ($\tau$) | Technique ($k$) | Tool ($u$) | Post-State ($s'$) | Verified Command ($c$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `type` | `s_passive_topology_mapped` | `type = 0x0400` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `ping` | `s_credentials_or_certs_acquired` | `ping -c 3 test messages sent across each bearer channel` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `type` | `s_passive_topology_mapped` | `type = 0x02  family=1(IPv4) prefix-length=16 prefix=192.115/16` |

## Verified Executable Commands (Grouped by Capability Layer)

### General_System (2 commands)
```bash
type = 0x0400
type = 0x02  family=1(IPv4) prefix-length=16 prefix=192.115/16
```

### L3_Routing_NAT (1 commands)
```bash
ping -c 3 test messages sent across each bearer channel
```

