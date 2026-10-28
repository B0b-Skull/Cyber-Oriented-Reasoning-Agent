---
title: "Trained Command Playbook: APT28-FANCYBEAR-REPORT.pdf"
tags:
  - arp
  - cve-2015-1641
  - cve-2015-1701
  - cve-2017-11292
  - enumeration
  - http
  - https
  - mdp
  - mimikatz
  - passive_enum
  - pdf
  - post_exploitation_verification
  - responder
  - sysinternals
  - trained
source_file: APT28-FANCYBEAR-REPORT.pdf
updated: 2026-10-24 00:56:13
---

# Trained Command Playbook: `APT28-FANCYBEAR-REPORT.pdf`

- **Source Document:** `~/Projects/CORA/Training/APT28-FANCYBEAR-REPORT.pdf`
- **CEGAR Verified Commands:** `9` (`0` malformed/unsafe snippets filtered)
- **MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`):** `9`
- **Discovered IPs/Subnets:** `2.2.2.1, 2.2.2.2, 2.2.2.3, 2.2.2.4`
- **Discovered Interfaces:** `None`
- **Related Knowledge Note:** [[knowledge/trained_apt28-fancybear-report]]

## Distilled MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`)
| Pre-State ($s$) | Tactic ($\tau$) | Technique ($k$) | Tool ($u$) | Post-State ($s'$) | Verified Command ($c$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `kill` | `s_active_services_enumerated` | `kill chain models. The first proposal for a kill chain is developed through literature study,` |
| `s_cross_subnet_pivot_routed` | **`Post_Exploitation_Verification`** | Post-Action Host Identity, Privilege & Objective Verification | `groups` | `s_goal_verified_complete` | `groups within the organization, the roles of individual employees and where active users` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `kill` | `s_passive_topology_mapped` | `kill chains, even though proving access may not entail taking any other actions towards the objectives` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `kill` | `s_active_services_enumerated` | `kill chains in a way that allows both technology- and management-orientated readers to` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `kill` | `s_active_services_enumerated` | `kill chain of that attack (or: an attack specific kill chain).` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `kill` | `s_active_services_enumerated` | `kill chain, phases that may occur more than once in an attack are generally modeled in the position in` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `kill` | `s_active_services_enumerated` | `kill chains can be compared to show how these attacks converge or diverge on a tactical level and to` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `.` | `s_active_services_enumerated` | `update-the-cyber-kill-chain-for-better-defense/. [Accessed: 10-May-2017].` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `.` | `s_active_services_enumerated` | `test-persistence-method-used-in-recent-sofacy-attacks/. [Accessed: 24-Oct-2017].` |

## Verified Executable Commands (Grouped by Capability Layer)

### General_System (9 commands)
```bash
kill chain models. The first proposal for a kill chain is developed through literature study,
kill chains in a way that allows both technology- and management-orientated readers to
kill chain of that attack (or: an attack specific kill chain).
groups within the organization, the roles of individual employees and where active users
kill chain, phases that may occur more than once in an attack are generally modeled in the position in
kill chains, even though proving access may not entail taking any other actions towards the objectives
kill chains can be compared to show how these attacks converge or diverge on a tactical level and to
update-the-cyber-kill-chain-for-better-defense/. [Accessed: 10-May-2017].
test-persistence-method-used-in-recent-sofacy-attacks/. [Accessed: 24-Oct-2017].
```

