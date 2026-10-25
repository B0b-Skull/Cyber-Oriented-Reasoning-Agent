---
title: "Trained Command Playbook: README.md"
tags:
  - cegar
  - enumeration
  - mdp
  - powershell
  - sysinternals
  - text
  - trained
source_file: README.md
updated: 2026-10-25 01:00:16
---

# Trained Command Playbook: `README.md`

- **Source Document:** `~/Projects/CORA/Training/README.md`
- **CEGAR Verified Commands:** `2` (`0` malformed/unsafe snippets filtered)
- **MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`):** `2`
- **Discovered IPs/Subnets:** `None`
- **Discovered Interfaces:** `None`
- **Related Knowledge Note:** [[knowledge/trained_readme]]

## Distilled MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`)
| Pre-State ($s$) | Tactic ($\tau$) | Technique ($k$) | Tool ($u$) | Post-State ($s'$) | Verified Command ($c$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `run_cora_NIX.sh` | `s_active_services_enumerated` | `./run_cora_NIX.sh -train Training` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `train_llm_NIX.sh` | `s_active_services_enumerated` | `./Training/train_llm_NIX.sh Training` |

## Verified Executable Commands (Grouped by Capability Layer)

### General_System (2 commands)
```bash
./run_cora_NIX.sh -train Training
./Training/train_llm_NIX.sh Training
```
