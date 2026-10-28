---
title: "Trained Command Playbook: Change System Files CMDs.txt"
tags:
  - bcdedit
  - cacls
  - defense_evasion_firewall
  - enumeration
  - icacls
  - ipconfig
  - mdp
  - passive_enum
  - privilege_escalation
  - text
  - trained
  - wmic
source_file: Change System Files CMDs.txt
updated: 2026-10-24 00:57:11
---

# Trained Command Playbook: `Change System Files CMDs.txt`

- **Source Document:** `~/Projects/CORA/Training/Change System Files CMDs.txt`
- **CEGAR Verified Commands:** `31` (`0` malformed/unsafe snippets filtered)
- **MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`):** `31`
- **Discovered IPs/Subnets:** `None`
- **Discovered Interfaces:** `None`
- **Related Knowledge Note:** [[knowledge/trained_change_system_files_cmds]]

## Distilled MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`)
| Pre-State ($s$) | Tactic ($\tau$) | Technique ($k$) | Tool ($u$) | Post-State ($s'$) | Verified Command ($c$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `dir` | `s_passive_topology_mapped` | `dir C:\ /s /b \| find "ipconfig.exe"` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `del` | `s_firewall_or_acl_unlocked` | `del %systemroot%\system32\ipconfig.exe & dir /on %systemroot%\system32\ipc*` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `copy` | `s_active_services_enumerated` | `copy c:\Solitaire.exe %systemroot%\system32\ipconfig.exe` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `icacls` | `s_interactive_tty_or_priv_escalated` | `icacls %systemroot%\notepad.exe /grant win7\administrator:(F)` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `reg` | `s_passive_topology_mapped` | `Reg query "hklm\system\currentcontrolset\control\session manager"` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `copy` | `s_firewall_or_acl_unlocked` | `copy %systemroot%\system32\ipconfig.exe "c:\documents and settings\administrator\desktop\ipconfig.bak"` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `copy` | `s_active_services_enumerated` | `copy "C:\Documents and Settings\administrator\desktop\ipconfig.bak" %systemroot%\system32\ipconfig.exe` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `cacls` | `s_interactive_tty_or_priv_escalated` | `cacls %systemroot%\notepad.exe` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `dir` | `s_passive_topology_mapped` | `dir C:\ /s /b \| find "notepad.exe"` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `copy` | `s_firewall_or_acl_unlocked` | `copy %systemroot%\system32\calc.exe %systemroot%\system32\ipconfig.exe` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `copy` | `s_active_services_enumerated` | `copy "C:\Documents and Settings\administrator\desktop\ipconfig.bak" "C:\Documents and Settings\administrator\desktop\ypconfig.exe"` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `takeown` | `s_interactive_tty_or_priv_escalated` | `takeown /f %systemroot%\system32\ipconfig.exe` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `dir` | `s_passive_topology_mapped` | `dir notepad*` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `del` | `s_firewall_or_acl_unlocked` | `del %systemroot%\system32\ipconfig.exe` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `copy` | `s_active_services_enumerated` | `copy "C:\Documents and Settings\administrator\desktop\ypconfig.exe" %systemroot%\system32\ypconfig.exe` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `icacls` | `s_interactive_tty_or_priv_escalated` | `icacls %systemroot%\system32\ipconfig.exe /grant win7\administrator:(F)` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `` | `s_passive_topology_mapped` | `sigcheck\ -i %systemroot%\notepad.exe -accepteula` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `copy` | `s_firewall_or_acl_unlocked` | `copy %systemroot%\system32\sfcfiles.dll "c:\Documents and Settings\administrator\desktop\sfcfiles.bak"` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `copy` | `s_active_services_enumerated` | `copy %systemroot%\notepad.exe "%username%\desktop\ipconfig.bak"` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `wmic` | `s_passive_topology_mapped` | `wmic OS Get DataExecutionPrevention_Availabl` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `copy` | `s_firewall_or_acl_unlocked` | `copy %systemroot%\system32\sfcfiles.dll %systemroot%\system32\mysfcfiles.dll` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `del` | `s_active_services_enumerated` | `del %systemroot%\notepad.bak` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `wmic` | `s_passive_topology_mapped` | `wmic OS Get DataExecutionPrevention_SupportPolicy` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `pechksum` | `s_firewall_or_acl_unlocked` | `PEChksum.exe %systemroot%\system32\mysfcfiles.dll` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `movelatr` | `s_firewall_or_acl_unlocked` | `Movelatr.exe %systemroot%\system32\mysfcfiles.dll %systemroot%\system32\sfcfiles.dll` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `del` | `s_firewall_or_acl_unlocked` | `del %systemroot%\system32\ipconfig.exe & del %systemroot%\system32\dllcache\ipconfig.exe %systemroot%\system32\ipconfig.exe` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `ren` | `s_firewall_or_acl_unlocked` | `ren c:\windows\notepad.exe notepad.bak` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `rename` | `s_firewall_or_acl_unlocked` | `rename %systemroot%\notepad.exe notepad.bak` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `sfc` | `s_firewall_or_acl_unlocked` | `sfc /SCANFILE=%systemroot%\notepad.exe` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `bcdedit` | `s_firewall_or_acl_unlocked` | `bcdedit /set nx OptOut` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `bcdedit` | `s_firewall_or_acl_unlocked` | `bcdedit /set nx [MODE]; where the [MODE] is either: AlwaysOff, AlwaysOn, OptOut, or OptIn` |

## Verified Executable Commands (Grouped by Capability Layer)

### General_System (31 commands)
```bash
dir C:\ /s /b | find "ipconfig.exe"
del %systemroot%\system32\ipconfig.exe & dir /on %systemroot%\system32\ipc*
copy %systemroot%\system32\ipconfig.exe "c:\documents and settings\administrator\desktop\ipconfig.bak"
copy c:\Solitaire.exe %systemroot%\system32\ipconfig.exe
copy %systemroot%\system32\calc.exe %systemroot%\system32\ipconfig.exe
del %systemroot%\system32\ipconfig.exe
copy "C:\Documents and Settings\administrator\desktop\ipconfig.bak" %systemroot%\system32\ipconfig.exe
copy %systemroot%\system32\sfcfiles.dll "c:\Documents and Settings\administrator\desktop\sfcfiles.bak"
copy %systemroot%\system32\sfcfiles.dll %systemroot%\system32\mysfcfiles.dll
PEChksum.exe %systemroot%\system32\mysfcfiles.dll
Reg query "hklm\system\currentcontrolset\control\session manager"
Movelatr.exe %systemroot%\system32\mysfcfiles.dll %systemroot%\system32\sfcfiles.dll
del %systemroot%\system32\ipconfig.exe & del %systemroot%\system32\dllcache\ipconfig.exe %systemroot%\system32\ipconfig.exe
copy "C:\Documents and Settings\administrator\desktop\ipconfig.bak" "C:\Documents and Settings\administrator\desktop\ypconfig.exe"
copy "C:\Documents and Settings\administrator\desktop\ypconfig.exe" %systemroot%\system32\ypconfig.exe
dir C:\ /s /b | find "notepad.exe"
copy %systemroot%\notepad.exe "%username%\desktop\ipconfig.bak"
ren c:\windows\notepad.exe notepad.bak
icacls %systemroot%\notepad.exe /grant win7\administrator:(F)
rename %systemroot%\notepad.exe notepad.bak
del %systemroot%\notepad.bak
dir notepad*
sfc /SCANFILE=%systemroot%\notepad.exe
cacls %systemroot%\notepad.exe
sigcheck\ -i %systemroot%\notepad.exe -accepteula
bcdedit /set nx OptOut
bcdedit /set nx [MODE]; where the [MODE] is either: AlwaysOff, AlwaysOn, OptOut, or OptIn
wmic OS Get DataExecutionPrevention_Availabl
wmic OS Get DataExecutionPrevention_SupportPolicy
takeown /f %systemroot%\system32\ipconfig.exe
icacls %systemroot%\system32\ipconfig.exe /grant win7\administrator:(F)
```

