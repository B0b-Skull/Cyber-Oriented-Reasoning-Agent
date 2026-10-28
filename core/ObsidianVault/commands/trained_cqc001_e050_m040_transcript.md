---
title: "Trained Command Playbook: CQC001_E050_M040_transcript.pdf"
tags:
  - iptables
  - mdp
  - passive_enum
  - pdf
  - post_exploitation_verification
  - trained
source_file: CQC001_E050_M040_transcript.pdf
updated: 2026-10-24 00:58:00
---

# Trained Command Playbook: `CQC001_E050_M040_transcript.pdf`

- **Source Document:** `~/Projects/CORA/Training/CQC001_E050_M040_transcript.pdf`
- **CEGAR Verified Commands:** `3` (`0` malformed/unsafe snippets filtered)
- **MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`):** `3`
- **Discovered IPs/Subnets:** `None`
- **Discovered Interfaces:** `None`
- **Related Knowledge Note:** [[knowledge/trained_cqc001_e050_m040_transcript]]

## Distilled MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`)
| Pre-State ($s$) | Tactic ($\tau$) | Technique ($k$) | Tool ($u$) | Post-State ($s'$) | Verified Command ($c$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `runlevel` | `s_passive_topology_mapped` | `Runlevel Field: The init process determines which set of scripts to run based upon a runlevel. A` |
| `s_cross_subnet_pivot_routed` | **`Post_Exploitation_Verification`** | Post-Action Host Identity, Privilege & Objective Verification | `runlevel` | `s_goal_verified_complete` | `runlevel three (3), and graphical.target, which is similar to runlevel five (5). Additionally, akin` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `chkconfig` | `s_passive_topology_mapped` | `chkconfig commands under systemd systems, though the service and chkconfig tools have` |

## Verified Executable Commands (Grouped by Capability Layer)

### General_System (3 commands)
```bash
Runlevel Field: The init process determines which set of scripts to run based upon a runlevel. A
runlevel three (3), and graphical.target, which is similar to runlevel five (5). Additionally, akin
chkconfig commands under systemd systems, though the service and chkconfig tools have
```

