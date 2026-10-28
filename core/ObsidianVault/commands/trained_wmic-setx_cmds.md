---
title: "Trained Command Playbook: WMIC-Setx CMDs.txt"
tags:
  - credential_access
  - enumeration
  - lateral_movement_routing_pivot
  - mdp
  - passive_enum
  - powershell
  - text
  - trained
  - wireshark
  - wmic
source_file: WMIC-Setx CMDs.txt
updated: 2026-10-24 01:01:12
---

# Trained Command Playbook: `WMIC-Setx CMDs.txt`

- **Source Document:** `~/Projects/CORA/Training/WMIC-Setx CMDs.txt`
- **CEGAR Verified Commands:** `15` (`0` malformed/unsafe snippets filtered)
- **MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`):** `15`
- **Discovered IPs/Subnets:** `172.24.11.11, 172.24.11.12`
- **Discovered Interfaces:** `None`
- **Related Knowledge Note:** [[knowledge/trained_wmic-setx_cmds]]

## Distilled MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`)
| Pre-State ($s$) | Tactic ($\tau$) | Technique ($k$) | Tool ($u$) | Post-State ($s'$) | Verified Command ($c$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `type` | `s_credentials_or_certs_acquired` | `type dependent.list && dir "c:\Program Files(x86)\Mozilla Firefox"` |
| `s_firewall_or_acl_unlocked` | **`Lateral_Movement_Routing_Pivot`** | Remote Host Execution, L2/L3 Route Injection & Subnet Pivot | `psexec` | `s_cross_subnet_pivot_routed` | `psexec \\172.24.11.12 -accepteula -u xp\administrator -p L33tHax0r cmd.exe` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `dir` | `s_passive_topology_mapped` | `dir C:\windows /on /ah > PRN` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `del` | `s_active_services_enumerated` | `del c:\data\kubeans\*.*` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `wmic` | `s_credentials_or_certs_acquired` | `WMIC USERACCOUNT WHERE Name='username' SET PasswordExpires=FALSE.` |
| `s_firewall_or_acl_unlocked` | **`Lateral_Movement_Routing_Pivot`** | Remote Host Execution, L2/L3 Route Injection & Subnet Pivot | `psexec` | `s_cross_subnet_pivot_routed` | `psexec \\172.24.11.12 -accepteula -u xp\administrator -p L33tHax0r powershell.exe` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `dir` | `s_passive_topology_mapped` | `dir C:\windows /on /ah > c:\data\directories\windows.txt` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `setx` | `s_active_services_enumerated` | `setx /s xp.ops.local /u xp\administrator /p L33tHax0r PATH "C:\systempath" /M` |
| `s_firewall_or_acl_unlocked` | **`Lateral_Movement_Routing_Pivot`** | Remote Host Execution, L2/L3 Route Injection & Subnet Pivot | `wmic` | `s_cross_subnet_pivot_routed` | `wmic /node:172.24.11.11 /user:xp\administrator computersystem list brief /format:list` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `dir` | `s_passive_topology_mapped` | `dir c:\windows\system /on /ah >> c:\data\directores\windows.txt` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `setx` | `s_active_services_enumerated` | `setx /s xp.ops.local /u xp\administrator /p L33tHax0r PATH "C:\Program Files\Wireshark;%PATH%"` |
| `s_firewall_or_acl_unlocked` | **`Lateral_Movement_Routing_Pivot`** | Remote Host Execution, L2/L3 Route Injection & Subnet Pivot | `wmic` | `s_cross_subnet_pivot_routed` | `wmic /node:172.24.11.12 /user:xp\administrator computersystem list brief /format:list` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `dir` | `s_passive_topology_mapped` | `dir c:\data\kubeans \| sort /+39` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `setx` | `s_active_services_enumerated` | `setx /s xp.ops.local /u xp\administrator /p L33tHax0r DOWNLOAD "C:\Documents and Settings\Administrator\My Documents\Downloads"` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `setx` | `s_passive_topology_mapped` | `setx /s xp.ops.local /u xp\administrator /p L33tHax0r PROMPT $D$T$P` |

## Verified Executable Commands (Grouped by Capability Layer)

### General_System (15 commands)
```bash
type dependent.list && dir "c:\Program Files(x86)\Mozilla Firefox"
WMIC USERACCOUNT WHERE Name='username' SET PasswordExpires=FALSE.
psexec \\172.24.11.12 -accepteula -u xp\administrator -p L33tHax0r cmd.exe
psexec \\172.24.11.12 -accepteula -u xp\administrator -p L33tHax0r powershell.exe
wmic /node:172.24.11.11 /user:xp\administrator computersystem list brief /format:list
wmic /node:172.24.11.12 /user:xp\administrator computersystem list brief /format:list
dir C:\windows /on /ah > PRN
dir C:\windows /on /ah > c:\data\directories\windows.txt
dir c:\windows\system /on /ah >> c:\data\directores\windows.txt
dir c:\data\kubeans | sort /+39
del c:\data\kubeans\*.*
setx /s xp.ops.local /u xp\administrator /p L33tHax0r PATH "C:\systempath" /M
setx /s xp.ops.local /u xp\administrator /p L33tHax0r PROMPT $D$T$P
setx /s xp.ops.local /u xp\administrator /p L33tHax0r PATH "C:\Program Files\Wireshark;%PATH%"
setx /s xp.ops.local /u xp\administrator /p L33tHax0r DOWNLOAD "C:\Documents and Settings\Administrator\My Documents\Downloads"
```

