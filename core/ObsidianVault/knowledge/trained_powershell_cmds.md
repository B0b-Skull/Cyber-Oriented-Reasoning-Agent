---
title: "Trained Knowledge & Topology: PowerShell CMDs.txt"
tags:
  - mdp
  - passive_enum
  - powershell
  - text
  - trained
source_file: PowerShell CMDs.txt
doc_type: text
updated: 2026-10-24 01:00:06
---

# Trained Knowledge & Architecture: `PowerShell CMDs.txt`

- **Source Path:** `~/Projects/CORA/Training/PowerShell CMDs.txt` (`text`)
- **Extracted Technical Entities:** `powershell`
- **Extracted IPs / Subnets:** `None`
- **Extracted Interfaces:** `None`
- **Linked Command Playbook:** [[commands/trained_powershell_cmds]] (`4` CEGAR-verified commands | `4` MDP transitions)

## Command & Tactic Coverage Summary
- **Total CEGAR-Verified Commands:** `4` (full executable list in [[commands/trained_powershell_cmds]])
- **Tactic Distribution:** `Passive_Enum` (4)
- **Top Extracted CLI Tools:** `get-service` (4)

## Extracted Reference Excerpt
Powershell

Get-Service | Where-Object {$_.displayName.StartsWith("NATION-")} | Select name

	Get-Service | Where-Object {$_.displayName.StartsWith("NATION-")} | Stop-Service
	Get-Service | Where-Object {$_.displayName.StartsWith("NATION-")} | Start-Service
	Get-Service | Where-Object {$_.displayName.StartsWith("NATION-")} | Restart-Service

