---
title: "Trained Knowledge & Topology: Net CMDs 1.txt"
tags:
  - defense_evasion_firewall
  - enumeration
  - lateral_movement_routing_pivot
  - mdp
  - netsh
  - passive_enum
  - text
  - trained
  - wmic
source_file: Net CMDs 1.txt
doc_type: text
updated: 2026-10-24 00:59:23
---

# Trained Knowledge & Architecture: `Net CMDs 1.txt`

- **Source Path:** `~/Projects/CORA/Training/Net CMDs 1.txt` (`text`)
- **Extracted Technical Entities:** `netsh, wmic`
- **Extracted IPs / Subnets:** `None`
- **Extracted Interfaces:** `None`
- **Linked Command Playbook:** [[commands/trained_net_cmds_1]] (`13` CEGAR-verified commands | `13` MDP transitions)

## Command & Tactic Coverage Summary
- **Total CEGAR-Verified Commands:** `13` (full executable list in [[commands/trained_net_cmds_1]])
- **Tactic Distribution:** `Passive_Enum` (6), `Defense_Evasion_Firewall` (5), `Enumeration` (1), `Lateral_Movement_Routing_Pivot` (1)
- **Top Extracted CLI Tools:** `net` (3), `nbtstat` (2), `reg` (2), `wmic` (2), `netsh` (1), `openfiles` (1), `systeminfo` (1), `telnet` (1)

## Extracted Reference Excerpt
netsh firewall set portopening tcp 445 smb enable

net view \\xp

net share SharedResources=c:\Resources /remark:"Beware the Ghost!"

net use k: \\xp.ops.local\SharedResources /u:xp\Administrator

nbtstat -s sessions	<Lists the NetBIOS sessions table converting destination IP addresses to computer NetBIOS names>
nbtstat -S sessions <Lists the current NetBIOS sessions and their status , with the IP address>

openfiles /query

telnet \\xp.ops.local /u xp\Administrator

wmic useraccount get name,sid

reg query hku | find "HKEY_USERS\S-1-5-21-" | find /v "_Classes"
reg query HKEY_USERS

systeminfo | findstr /B /C:"Domain"

wmic computersystem get domain

