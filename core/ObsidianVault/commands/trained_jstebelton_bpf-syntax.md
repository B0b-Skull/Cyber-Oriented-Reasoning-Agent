---
title: "Trained Command Playbook: JStebelton_BPF-Syntax.pdf"
tags:
  - active_enum
  - eth0
  - http
  - mdp
  - pdf
  - tcpdump
  - trained
source_file: JStebelton_BPF-Syntax.pdf
updated: 2026-10-25 00:58:43
---

# Trained Command Playbook: `JStebelton_BPF-Syntax.pdf`

- **Source Document:** `~/Projects/CORA/Training/JStebelton_BPF-Syntax.pdf`
- **CEGAR Verified Commands:** `1` (`0` malformed/unsafe snippets filtered)
- **MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`):** `1`
- **Discovered IPs/Subnets:** `10.10.1.1`
- **Discovered Interfaces:** `eth0`
- **Related Knowledge Note:** [[knowledge/trained_jstebelton_bpf-syntax]]

## Distilled MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`)
| Pre-State ($s$) | Tactic ($\tau$) | Technique ($k$) | Tool ($u$) | Post-State ($s'$) | Verified Command ($c$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `s_passive_topology_mapped` | **`Active_Enum`** | Active Network, Cloud, Directory Service & Endpoint Probing | `tcpdump` | `s_active_services_enumerated` | `tcpdump -nn -i eth0 'tcp[13] & 0x02 = 2 and ip[2:2] > 0x86 and ip[0] & 0xF0 != 4'` |

## Verified Executable Commands (Grouped by Capability Layer)

### L4_Port_Service (1 commands)
```bash
tcpdump -nn -i eth0 'tcp[13] & 0x02 = 2 and ip[2:2] > 0x86 and ip[0] & 0xF0 != 4'
```

