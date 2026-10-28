---
title: "Trained Knowledge & Topology: PsService CMDs.txt"
tags:
  - mdp
  - passive_enum
  - text
  - trained
source_file: PsService CMDs.txt
doc_type: text
updated: 2026-10-24 01:00:11
---

# Trained Knowledge & Architecture: `PsService CMDs.txt`

- **Source Path:** `~/Projects/CORA/Training/PsService CMDs.txt` (`text`)
- **Extracted Technical Entities:** `general`
- **Extracted IPs / Subnets:** `None`
- **Extracted Interfaces:** `None`
- **Linked Command Playbook:** [[commands/trained_psservice_cmds]] (`12` CEGAR-verified commands | `12` MDP transitions)

## Command & Tactic Coverage Summary
- **Total CEGAR-Verified Commands:** `12` (full executable list in [[commands/trained_psservice_cmds]])
- **Tactic Distribution:** `Passive_Enum` (12)
- **Top Extracted CLI Tools:** `psservice` (12)

## Extracted Reference Excerpt
PSService

psservice \\xp.ops.local -u xp\Administrator -p L33tHax0r
psservice \\xp.ops.local -u xp\Administrator -p L33tHax0r query "Security Center"
psservice \\xp.ops.local -u xp\Administrator -p L33tHax0r query wscsvc
 psservice \\xp.ops.local -u xp\administrator -p L33tHax0r query -s all

psservice stop W32time
psservice query W32time
psservice start W32time

psservice config "Windows Event Collector"
psservice config "Windows Update"
psservice config "Security Center"
psservice config "Parental Control"

psservice setconfig wpcsvc auto  -> sets start-type to auto for Parental Controls service

