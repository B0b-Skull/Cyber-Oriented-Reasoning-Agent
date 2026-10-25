---
title: "Trained Command Playbook: Win Local CMDs.txt"
tags:
  - enumeration
  - lateral_movement_routing_pivot
  - listdlls
  - mdp
  - passive_enum
  - pslist
  - text
  - trained
  - wmic
source_file: Win Local CMDs.txt
updated: 2026-10-25 01:01:12
---

# Trained Command Playbook: `Win Local CMDs.txt`

- **Source Document:** `~/Projects/CORA/Training/Win Local CMDs.txt`
- **CEGAR Verified Commands:** `56` (`0` malformed/unsafe snippets filtered)
- **MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`):** `56`
- **Discovered IPs/Subnets:** `172.17.10.71, 172.17.10.78`
- **Discovered Interfaces:** `None`
- **Related Knowledge Note:** [[knowledge/trained_win_local_cmds]]

## Distilled MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`)
| Pre-State ($s$) | Tactic ($\tau$) | Technique ($k$) | Tool ($u$) | Post-State ($s'$) | Verified Command ($c$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `tasklist` | `s_passive_topology_mapped` | `tasklist` |
| `s_firewall_or_acl_unlocked` | **`Lateral_Movement_Routing_Pivot`** | Remote Host Execution, L2/L3 Route Injection & Subnet Pivot | `tasklist` | `s_cross_subnet_pivot_routed` | `tasklist /s xp.ops.local /u xp\administrator /p L33tHax0r` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `taskkill` | `s_active_services_enumerated` | `taskkill /im <imagename>` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `tasklist` | `s_passive_topology_mapped` | `tasklist /svc` |
| `s_firewall_or_acl_unlocked` | **`Lateral_Movement_Routing_Pivot`** | Remote Host Execution, L2/L3 Route Injection & Subnet Pivot | `taskkill` | `s_cross_subnet_pivot_routed` | `taskkill /pid 1187 /s xp.ops.local /u xp\administrator /p L33tHax0r` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `pskill` | `s_active_services_enumerated` | `pskill -t` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `tasklist` | `s_passive_topology_mapped` | `tasklist /m` |
| `s_firewall_or_acl_unlocked` | **`Lateral_Movement_Routing_Pivot`** | Remote Host Execution, L2/L3 Route Injection & Subnet Pivot | `pslist` | `s_cross_subnet_pivot_routed` | `pslist \\xp.ops.local -u xp\administrator -p L33tHax0r` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `tasklist` | `s_passive_topology_mapped` | `tasklist /fi "SESSION eq 1"` |
| `s_firewall_or_acl_unlocked` | **`Lateral_Movement_Routing_Pivot`** | Remote Host Execution, L2/L3 Route Injection & Subnet Pivot | `pskill` | `s_cross_subnet_pivot_routed` | `pskill - \\xp.ops.local /u xp\administrator /p L33tHax0r 2843` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `pslist` | `s_passive_topology_mapped` | `pslist /dm` |
| `s_firewall_or_acl_unlocked` | **`Lateral_Movement_Routing_Pivot`** | Remote Host Execution, L2/L3 Route Injection & Subnet Pivot | `pskill` | `s_cross_subnet_pivot_routed` | `pskill - \\xp.ops.local /u xp\administrator /p L33tHax0r "notepad.exe\|2843"` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `pslist` | `s_passive_topology_mapped` | `pslist /x` |
| `s_firewall_or_acl_unlocked` | **`Lateral_Movement_Routing_Pivot`** | Remote Host Execution, L2/L3 Route Injection & Subnet Pivot | `pslist` | `s_cross_subnet_pivot_routed` | `pslist \\172.17.10.71 -u drytortugas\administrator -p $eCret` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `pslist` | `s_passive_topology_mapped` | `pslist /s 120 /r 3` |
| `s_firewall_or_acl_unlocked` | **`Lateral_Movement_Routing_Pivot`** | Remote Host Execution, L2/L3 Route Injection & Subnet Pivot | `tasklist` | `s_cross_subnet_pivot_routed` | `tasklist /s 172.17.10.71 -u drytortugas\administrator -p $eCret` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `pslist` | `s_passive_topology_mapped` | `pslist /t` |
| `s_firewall_or_acl_unlocked` | **`Lateral_Movement_Routing_Pivot`** | Remote Host Execution, L2/L3 Route Injection & Subnet Pivot | `telnet` | `s_cross_subnet_pivot_routed` | `telnet 172.17.10.71 23` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `handle` | `s_passive_topology_mapped` | `handle -p notepad.exe` |
| `s_firewall_or_acl_unlocked` | **`Lateral_Movement_Routing_Pivot`** | Remote Host Execution, L2/L3 Route Injection & Subnet Pivot | `telnet` | `s_cross_subnet_pivot_routed` | `telnet win7.ops.local` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `handle` | `s_passive_topology_mapped` | `handle -p cmd.exe` |
| `s_firewall_or_acl_unlocked` | **`Lateral_Movement_Routing_Pivot`** | Remote Host Execution, L2/L3 Route Injection & Subnet Pivot | `tasklist` | `s_cross_subnet_pivot_routed` | `tasklist /s 172.17.10.78 /u administrator /p KeyF@rg0 /fi "session eq 0"` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `handle` | `s_passive_topology_mapped` | `handle notepad.exe` |
| `s_firewall_or_acl_unlocked` | **`Lateral_Movement_Routing_Pivot`** | Remote Host Execution, L2/L3 Route Injection & Subnet Pivot | `tasklist` | `s_cross_subnet_pivot_routed` | `tasklist /s 172.17.10.78 /u administrator /p KeyF@rg0 /m IIS*` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `handle` | `s_passive_topology_mapped` | `handle -a cmd.exe` |
| `s_firewall_or_acl_unlocked` | **`Lateral_Movement_Routing_Pivot`** | Remote Host Execution, L2/L3 Route Injection & Subnet Pivot | `tasklist` | `s_cross_subnet_pivot_routed` | `tasklist /S 172.17.10.78 /U Administrator /P KeyF@rg0 /SVC` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `handle` | `s_passive_topology_mapped` | `handle -a -p PID` |
| `s_firewall_or_acl_unlocked` | **`Lateral_Movement_Routing_Pivot`** | Remote Host Execution, L2/L3 Route Injection & Subnet Pivot | `tasklist` | `s_cross_subnet_pivot_routed` | `tasklist /S 172.17.10.78 /U Administrator /P KeyF@rg0` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `listdlls` | `s_passive_topology_mapped` | `listdlls` |
| `s_firewall_or_acl_unlocked` | **`Lateral_Movement_Routing_Pivot`** | Remote Host Execution, L2/L3 Route Injection & Subnet Pivot | `pslist` | `s_cross_subnet_pivot_routed` | `pslist \\www.ops.local -u administrator -p opsDMZ321!!!` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `pslist` | `s_passive_topology_mapped` | `pslist notepad` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `listdlls` | `s_passive_topology_mapped` | `listdlls 1140` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `listdlls` | `s_passive_topology_mapped` | `listdlls notepad.exe` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `listdlls` | `s_passive_topology_mapped` | `listdlls -d wow64.dll` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `tasklist` | `s_passive_topology_mapped` | `tasklist /fi "services eq bfe"` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `wmic` | `s_passive_topology_mapped` | `wmic process where (processid=1388) get parentprocessid` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `wmic` | `s_passive_topology_mapped` | `wmic cpu get numberoflogicalprocessors` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `wmic` | `s_passive_topology_mapped` | `wmic datafile where name='c:\\windows\\system32\\drivers\\mrxsmb10.sys' get creationdate` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `tasklist` | `s_passive_topology_mapped` | `tasklist /v` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `pslist` | `s_passive_topology_mapped` | `pslist -t` |

## Verified Executable Commands (Grouped by Capability Layer)

### General_System (54 commands)
```bash
tasklist
tasklist /svc
tasklist /m
tasklist /s xp.ops.local /u xp\administrator /p L33tHax0r
tasklist /fi "SESSION eq 1"
taskkill /im <imagename>
taskkill /pid 1187 /s xp.ops.local /u xp\administrator /p L33tHax0r
pslist /dm
pslist /x
pslist /s 120 /r 3
pslist \\xp.ops.local -u xp\administrator -p L33tHax0r
pslist /t
pskill -t
pskill - \\xp.ops.local /u xp\administrator /p L33tHax0r 2843
pskill - \\xp.ops.local /u xp\administrator /p L33tHax0r "notepad.exe|2843"
handle -p notepad.exe
handle -p cmd.exe
handle notepad.exe
handle -a cmd.exe
handle -a -p PID
listdlls
pslist notepad
listdlls 1140
listdlls notepad.exe
listdlls -d wow64.dll
pslist \\172.17.10.71 -u drytortugas\administrator -p $eCret
tasklist /s 172.17.10.71 -u drytortugas\administrator -p $eCret
tasklist /s 172.17.10.78 /u administrator /p KeyF@rg0 /fi "session eq 0"
tasklist /s 172.17.10.78 /u administrator /p KeyF@rg0 /m IIS*
tasklist /fi "services eq bfe"
wmic process where (processid=1388) get parentprocessid
wmic cpu get numberoflogicalprocessors
wmic datafile where name='c:\\windows\\system32\\drivers\\mrxsmb10.sys' get creationdate
tasklist /S 172.17.10.78 /U Administrator /P KeyF@rg0 /SVC
tasklist /S 172.17.10.78 /U Administrator /P KeyF@rg0
tasklist /v
pslist \\www.ops.local -u administrator -p opsDMZ321!!!
pslist -t
listdlls -d defender
listdlls |more
listdlls -d [dll-name]
listdlls -d C:\Windows\WinSxS\x86_microsoft.windows
listdlls cmd
listdlls -d dssenh.dll
listdlls -v -d gdi32.dll
listdlls -v -d pku2u.dll
listdlls -d sxssrv.dll
listdlls -u
listdlls msdtc
handle -p conhost
handle -a music
handle -a -p LogonUI | more
handle -a -p cmd
handle -s -p [PID of smss]
```

### L4_Port_Service (2 commands)
```bash
telnet 172.17.10.71 23
telnet win7.ops.local
```

