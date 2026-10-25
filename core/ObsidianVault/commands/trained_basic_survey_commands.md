---
title: "Trained Command Playbook: Basic Survey Commands.txt"
tags:
  - arp
  - auditpol
  - autorunsc
  - defense_evasion_firewall
  - ipconfig
  - listdlls
  - mdp
  - netstat
  - passive_enum
  - powershell
  - pslist
  - sysinternals
  - text
  - trained
  - wmic
source_file: Basic Survey Commands.txt
updated: 2026-10-25 00:56:13
---

# Trained Command Playbook: `Basic Survey Commands.txt`

- **Source Document:** `~/Projects/CORA/Training/Basic Survey Commands.txt`
- **CEGAR Verified Commands:** `39` (`0` malformed/unsafe snippets filtered)
- **MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`):** `39`
- **Discovered IPs/Subnets:** `None`
- **Discovered Interfaces:** `None`
- **Related Knowledge Note:** [[knowledge/trained_basic_survey_commands]]

## Distilled MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`)
| Pre-State ($s$) | Tactic ($\tau$) | Technique ($k$) | Tool ($u$) | Post-State ($s'$) | Verified Command ($c$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `prompt` | `s_passive_topology_mapped` | `prompt $P$B$D$B$T$G` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `auditpol` | `s_firewall_or_acl_unlocked` | `auditpol /get /category:*` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `date` | `s_passive_topology_mapped` | `date /t && time/t` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `ipconfig` | `s_passive_topology_mapped` | `ipconfig /all` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `tasklist` | `s_passive_topology_mapped` | `tasklist /v` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `tasklist` | `s_passive_topology_mapped` | `Tasklist /svc` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `psloggedon` | `s_passive_topology_mapped` | `psloggedon` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `systeminfo` | `s_passive_topology_mapped` | `systeminfo` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `listdlls` | `s_passive_topology_mapped` | `listdlls \| find /I "Command"` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `wmic` | `s_passive_topology_mapped` | `wmic process get executablepath, processid, parentprocessid \| more` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `wmic` | `s_passive_topology_mapped` | `wmic process get commandline \| more` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `wmic` | `s_passive_topology_mapped` | `wmic os get servicepackmajorversion` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `wmic` | `s_passive_topology_mapped` | `wmic useraccount get name,sid` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `wmic` | `s_passive_topology_mapped` | `wmic qfe list full` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `nbtstat` | `s_passive_topology_mapped` | `nbtstat -n` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `nbtstat` | `s_passive_topology_mapped` | `nbtstat -s` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `route` | `s_passive_topology_mapped` | `route -reg` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `netstat` | `s_passive_topology_mapped` | `netstat -ano \| findstr EST` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `netstat` | `s_passive_topology_mapped` | `netstat -ano \| findstr LIST` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `net` | `s_passive_topology_mapped` | `net users` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `net` | `s_passive_topology_mapped` | `net use` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `net` | `s_passive_topology_mapped` | `net share` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `net` | `s_passive_topology_mapped` | `net start` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `dir` | `s_passive_topology_mapped` | `dir /tc /od C:\windows\system32` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `autorunsc` | `s_passive_topology_mapped` | `autorunsc -b` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `autorunsc` | `s_passive_topology_mapped` | `autorunsc -l` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `reg` | `s_passive_topology_mapped` | `reg query hklm\software\microsoft\windows\currentversion\run` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `reg` | `s_passive_topology_mapped` | `reg query hkcu\software\microsoft\windows\currentversion\run` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `reg` | `s_passive_topology_mapped` | `reg query hklm\software\microsoft\windows\currentversion\runonce` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `reg` | `s_passive_topology_mapped` | `reg query hkcu\software\microsoft\windows\currentversion\runonce` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `reg` | `s_passive_topology_mapped` | `reg query "hklm\software\microsoft\windows nt\currentversion\winlogon" /v shell` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `reg` | `s_passive_topology_mapped` | `reg query "hklm\system\currentcontrolset\control\session manager"` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `reg` | `s_passive_topology_mapped` | `reg query hklm\system\currentcontrolset\control\windows` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `reg` | `s_passive_topology_mapped` | `reg query hklm\system\currentcontrolset\control\hivelist` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `reg` | `s_passive_topology_mapped` | `reg query hklm\system\currentcontrolset\services\tcpip\parameters` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `reg` | `s_passive_topology_mapped` | `reg query hku \| find "HKEY_USERS\S-1-5-21-" \| find /v "_Classes"` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `wmic` | `s_passive_topology_mapped` | `wmic fsdir where name="C:\\DirectoryOfInterest" get creationdate,lastmodified,lastaccessed /format:list` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `wmic` | `s_passive_topology_mapped` | `wmic datafile where name="C:\\FileOfInterest" get creationdate,lastmodified,lastaccessed /format:list` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `date` | `s_passive_topology_mapped` | `date /t >> C:\sysinfo.txt && time/t >> C:\sysinfo.txt && systeminfo >> C:\sysinfo.txt && ver >> C:\sysinfo.txt && net session >> C:\sysinfo.txt && net statistics >> C:\sysinfo.txt && ipconfig /all >> C:\sysinfo.txt && arp -a >> C:\sysinfo.txt && route print >> C:\sysinfo.txt` |

## Verified Executable Commands (Grouped by Capability Layer)

### General_System (33 commands)
```bash
prompt $P$B$D$B$T$G
date /t && time/t
tasklist /v
Tasklist /svc
psloggedon
systeminfo
listdlls | find /I "Command"
wmic process get executablepath, processid, parentprocessid | more
wmic process get commandline | more
wmic os get servicepackmajorversion
wmic useraccount get name,sid
wmic qfe list full
auditpol /get /category:*
net users
net use
net share
net start
dir /tc /od C:\windows\system32
autorunsc -b
autorunsc -l
reg query hklm\software\microsoft\windows\currentversion\run
reg query hkcu\software\microsoft\windows\currentversion\run
reg query hklm\software\microsoft\windows\currentversion\runonce
reg query hkcu\software\microsoft\windows\currentversion\runonce
reg query "hklm\software\microsoft\windows nt\currentversion\winlogon" /v shell
reg query "hklm\system\currentcontrolset\control\session manager"
reg query hklm\system\currentcontrolset\control\windows
reg query hklm\system\currentcontrolset\control\hivelist
reg query hklm\system\currentcontrolset\services\tcpip\parameters
reg query hku | find "HKEY_USERS\S-1-5-21-" | find /v "_Classes"
wmic fsdir where name="C:\\DirectoryOfInterest" get creationdate,lastmodified,lastaccessed /format:list
wmic datafile where name="C:\\FileOfInterest" get creationdate,lastmodified,lastaccessed /format:list
date /t >> C:\sysinfo.txt && time/t >> C:\sysinfo.txt && systeminfo >> C:\sysinfo.txt && ver >> C:\sysinfo.txt && net session >> C:\sysinfo.txt && net statistics >> C:\sysinfo.txt && ipconfig /all >> C:\sysinfo.txt && arp -a >> C:\sysinfo.txt && route print >> C:\sysinfo.txt
```

### L3_Routing_NAT (2 commands)
```bash
ipconfig /all
route -reg
```

### L4_Port_Service (4 commands)
```bash
nbtstat -n
nbtstat -s
netstat -ano | findstr EST
netstat -ano | findstr LIST
```

