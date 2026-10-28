---
title: "Trained Command Playbook: CQC001_E020_M010_Root_Keys_and_Registry_Types.pdf"
tags:
  - bcdedit
  - enumeration
  - http
  - https
  - mdp
  - passive_enum
  - pdf
  - trained
source_file: CQC001_E020_M010_Root_Keys_and_Registry_Types.pdf
updated: 2026-10-24 00:57:31
---

# Trained Command Playbook: `CQC001_E020_M010_Root_Keys_and_Registry_Types.pdf`

- **Source Document:** `~/Projects/CORA/Training/CQC001_E020_M010_Root_Keys_and_Registry_Types.pdf`
- **CEGAR Verified Commands:** `17` (`0` malformed/unsafe snippets filtered)
- **MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`):** `17`
- **Discovered IPs/Subnets:** `None`
- **Discovered Interfaces:** `None`
- **Related Knowledge Note:** [[knowledge/trained_cqc001_e020_m010_root_keys_and_registry_types]]

## Distilled MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`)
| Pre-State ($s$) | Tactic ($\tau$) | Technique ($k$) | Tool ($u$) | Post-State ($s'$) | Verified Command ($c$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `reg` | `s_passive_topology_mapped` | `Reg query` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `reg` | `s_active_services_enumerated` | `Reg add` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `reg` | `s_passive_topology_mapped` | `reg query <KeyName> [{/v <ValueName> \| /ve}] [/s] [/se <Separator>] [/f <Data>] [{/k \| /d}] [/c] [/e] [/t <Type>] [/z]` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `reg` | `s_active_services_enumerated` | `reg add <KeyName> [{/v ValueName \| /ve}] [/t DataType] [/s Separator] [/d Data] [/f]` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `reg` | `s_passive_topology_mapped` | `REG Query HKLM\Software /F "C:\Program Files (x86)\Cisco" /S` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `reg` | `s_active_services_enumerated` | `Reg save` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `reg` | `s_passive_topology_mapped` | `Reg query https://web.archive.org/web/20160721105928/https://technet.microsoft.com/en-us/library/cc742028.aspx` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `reg` | `s_active_services_enumerated` | `reg save <KeyName> <FileName> [/y]` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `reg` | `s_active_services_enumerated` | `REG SAVE HKLM\Software\MyCo\MyProgram ProgramBkUp.hiv` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `reg` | `s_active_services_enumerated` | `Reg export` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `reg` | `s_active_services_enumerated` | `Reg export KeyName FileName [/y]` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `reg` | `s_active_services_enumerated` | `reg export HKLM\Software\MyCo\MyProgram ProgramBkUp.reg` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `reg` | `s_active_services_enumerated` | `Reg import` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `reg` | `s_active_services_enumerated` | `REG IMPORT FileName.reg` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `reg` | `s_active_services_enumerated` | `Reg restore` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `reg` | `s_active_services_enumerated` | `REG RESTORE \\MachineName\[ROOT]\KeyName FileName.hiv` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `reg` | `s_active_services_enumerated` | `Reg add https://web.archive.org/web/20160721105853/https://technet.microsoft.com/en-us/library/cc742162.aspx` |

## Verified Executable Commands (Grouped by Capability Layer)

### General_System (15 commands)
```bash
Reg query
reg query <KeyName> [{/v <ValueName> | /ve}] [/s] [/se <Separator>] [/f <Data>] [{/k | /d}] [/c] [/e] [/t <Type>] [/z]
REG Query HKLM\Software /F "C:\Program Files (x86)\Cisco" /S
Reg add
reg add <KeyName> [{/v ValueName | /ve}] [/t DataType] [/s Separator] [/d Data] [/f]
Reg save
reg save <KeyName> <FileName> [/y]
REG SAVE HKLM\Software\MyCo\MyProgram ProgramBkUp.hiv
Reg export
Reg export KeyName FileName [/y]
reg export HKLM\Software\MyCo\MyProgram ProgramBkUp.reg
Reg import
REG IMPORT FileName.reg
Reg restore
REG RESTORE \\MachineName\[ROOT]\KeyName FileName.hiv
```

### L7_HTTP_Web (2 commands)
```bash
Reg add https://web.archive.org/web/20160721105853/https://technet.microsoft.com/en-us/library/cc742162.aspx
Reg query https://web.archive.org/web/20160721105928/https://technet.microsoft.com/en-us/library/cc742028.aspx
```

