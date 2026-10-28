---
title: "Trained Command Playbook: Net CMDs 1.txt"
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
updated: 2026-10-24 00:59:23
---

# Trained Command Playbook: `Net CMDs 1.txt`

- **Source Document:** `~/Projects/CORA/Training/Net CMDs 1.txt`
- **CEGAR Verified Commands:** `13` (`0` malformed/unsafe snippets filtered)
- **MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`):** `13`
- **Discovered IPs/Subnets:** `None`
- **Discovered Interfaces:** `None`
- **Related Knowledge Note:** [[knowledge/trained_net_cmds_1]]

## Distilled MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`)
| Pre-State ($s$) | Tactic ($\tau$) | Technique ($k$) | Tool ($u$) | Post-State ($s'$) | Verified Command ($c$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `netsh` | `s_firewall_or_acl_unlocked` | `netsh firewall set portopening tcp 445 smb enable` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `nbtstat` | `s_passive_topology_mapped` | `nbtstat -S sessions <Lists the current NetBIOS sessions and their status , with the IP address>` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `openfiles` | `s_active_services_enumerated` | `openfiles /query` |
| `s_firewall_or_acl_unlocked` | **`Lateral_Movement_Routing_Pivot`** | Remote Host Execution, L2/L3 Route Injection & Subnet Pivot | `telnet` | `s_cross_subnet_pivot_routed` | `telnet \\xp.ops.local /u xp\Administrator` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `net` | `s_firewall_or_acl_unlocked` | `net view \\xp` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `wmic` | `s_passive_topology_mapped` | `wmic useraccount get name,sid` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `net` | `s_firewall_or_acl_unlocked` | `net share SharedResources=c:\Resources /remark:"Beware the Ghost!"` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `reg` | `s_passive_topology_mapped` | `reg query hku \| find "HKEY_USERS\S-1-5-21-" \| find /v "_Classes"` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `net` | `s_firewall_or_acl_unlocked` | `net use k: \\xp.ops.local\SharedResources /u:xp\Administrator` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `reg` | `s_passive_topology_mapped` | `reg query HKEY_USERS` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `nbtstat` | `s_firewall_or_acl_unlocked` | `nbtstat -s sessions	<Lists the NetBIOS sessions table converting destination IP addresses to computer NetBIOS names>` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `systeminfo` | `s_passive_topology_mapped` | `systeminfo \| findstr /B /C:"Domain"` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `wmic` | `s_passive_topology_mapped` | `wmic computersystem get domain` |

## Verified Executable Commands (Grouped by Capability Layer)

### General_System (9 commands)
```bash
net view \\xp
net share SharedResources=c:\Resources /remark:"Beware the Ghost!"
net use k: \\xp.ops.local\SharedResources /u:xp\Administrator
openfiles /query
wmic useraccount get name,sid
reg query hku | find "HKEY_USERS\S-1-5-21-" | find /v "_Classes"
reg query HKEY_USERS
systeminfo | findstr /B /C:"Domain"
wmic computersystem get domain
```

### L3_Routing_NAT (1 commands)
```bash
netsh firewall set portopening tcp 445 smb enable
```

### L4_Port_Service (3 commands)
```bash
nbtstat -s sessions	<Lists the NetBIOS sessions table converting destination IP addresses to computer NetBIOS names>
nbtstat -S sessions <Lists the current NetBIOS sessions and their status , with the IP address>
telnet \\xp.ops.local /u xp\Administrator
```

