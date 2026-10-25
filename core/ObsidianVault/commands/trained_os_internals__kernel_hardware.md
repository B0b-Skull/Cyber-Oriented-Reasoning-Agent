---
title: "Trained Command Playbook: _OS Internals__Kernel & Hardware.pdf"
tags:
  - mdp
  - passive_enum
  - pdf
  - serial
  - trained
source_file: _OS Internals__Kernel & Hardware.pdf
updated: 2026-10-25 00:56:06
---

# Trained Command Playbook: `_OS Internals__Kernel & Hardware.pdf`

- **Source Document:** `~/Projects/CORA/Training/_OS Internals__Kernel & Hardware.pdf`
- **CEGAR Verified Commands:** `1` (`0` malformed/unsafe snippets filtered)
- **MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`):** `1`
- **Discovered IPs/Subnets:** `0.0.1.33, 0.0.100.4, 0.15.0.2`
- **Discovered Interfaces:** `None`
- **Related Knowledge Note:** [[knowledge/trained_os_internals__kernel_hardware]]

## Distilled MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`)
| Pre-State ($s$) | Tactic ($\tau$) | Technique ($k$) | Tool ($u$) | Post-State ($s'$) | Verified Command ($c$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `openssl` | `s_passive_topology_mapped` | `openssl asn1parse -inform der -in nvme0n2  \|grep -A 1 IM4P \| grep -v IM4P` |

## Verified Executable Commands (Grouped by Capability Layer)

### L7_HTTP_Web (1 commands)
```bash
openssl asn1parse -inform der -in nvme0n2  |grep -A 1 IM4P | grep -v IM4P
```

