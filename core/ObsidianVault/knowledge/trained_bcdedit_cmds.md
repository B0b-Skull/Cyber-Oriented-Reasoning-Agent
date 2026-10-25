---
title: "Trained Knowledge & Topology: BcdEdit CMDs.txt"
tags:
  - bcdedit
  - defense_evasion_firewall
  - mdp
  - passive_enum
  - text
  - trained
source_file: BcdEdit CMDs.txt
doc_type: text
updated: 2026-10-25 00:56:14
---

# Trained Knowledge & Architecture: `BcdEdit CMDs.txt`

- **Source Path:** `~/Projects/CORA/Training/BcdEdit CMDs.txt` (`text`)
- **Extracted Technical Entities:** `bcdedit`
- **Extracted IPs / Subnets:** `None`
- **Extracted Interfaces:** `None`
- **Linked Command Playbook:** [[commands/trained_bcdedit_cmds]] (`8` CEGAR-verified commands | `8` MDP transitions)

## Command & Tactic Coverage Summary
- **Total CEGAR-Verified Commands:** `8` (full executable list in [[commands/trained_bcdedit_cmds]])
- **Tactic Distribution:** `Defense_Evasion_Firewall` (7), `Passive_Enum` (1)
- **Top Extracted CLI Tools:** `bcdedit` (6), `attrib` (1), `type` (1)

## Extracted Reference Excerpt
attrib -s -h boot.ini
type boot.ini
bcdedit /export C:\boot_backup
bcdedit /timeout 180
bcdedit /default {47af9428-3f7d-11e4-89de-806e6f6e6963}
bcdedit /set {47af9428-3f7d-11e4-89de-806e6f6e6963} description "Primary Operating System"
bcdedit /set {f7428705-3f60-11e4-ae6a-806e6f6e6963} description "Secondary Operating System"
bcdedit /displayorder {47af9428-3f7d-11e4-89de-806e6f6e6963} {f7428705-3f60-11e4-ae6a-806e6f6e6963}

