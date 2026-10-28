---
title: "Trained Command Playbook: CQC001_E050_M020_transcript.pdf"
tags:
  - enumeration
  - http
  - mdp
  - passive_enum
  - pdf
  - ssh
  - trained
source_file: CQC001_E050_M020_transcript.pdf
updated: 2026-10-24 00:57:59
---

# Trained Command Playbook: `CQC001_E050_M020_transcript.pdf`

- **Source Document:** `~/Projects/CORA/Training/CQC001_E050_M020_transcript.pdf`
- **CEGAR Verified Commands:** `5` (`0` malformed/unsafe snippets filtered)
- **MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`):** `5`
- **Discovered IPs/Subnets:** `None`
- **Discovered Interfaces:** `None`
- **Related Knowledge Note:** [[knowledge/trained_cqc001_e050_m020_transcript]]

## Distilled MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`)
| Pre-State ($s$) | Tactic ($\tau$) | Technique ($k$) | Tool ($u$) | Post-State ($s'$) | Verified Command ($c$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `echo` | `s_active_services_enumerated` | `echo hello > output.txt` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `strings` | `s_passive_topology_mapped` | `strings within the braces separated by commas, and ending with postscript, in this example "d". The` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `script` | `s_active_services_enumerated` | `script name, $2 is the second argument after the script name and so on. So line 39 can be read as "if the command line arguments are greater than 1, use the second argument as the new value for the port variable, if not, then the port variable stays set at 8080."` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `strings` | `s_passive_topology_mapped` | `Strings within single quotes escape every character in quotes without exception. In the` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `strings` | `s_passive_topology_mapped` | `Strings within double quotes escape every character except dollar sign $, backtick `, backslash` |

## Verified Executable Commands (Grouped by Capability Layer)

### General_System (5 commands)
```bash
echo hello > output.txt
strings within the braces separated by commas, and ending with postscript, in this example "d". The
Strings within single quotes escape every character in quotes without exception. In the
Strings within double quotes escape every character except dollar sign $, backtick `, backslash
script name, $2 is the second argument after the script name and so on. So line 39 can be read as "if the command line arguments are greater than 1, use the second argument as the new value for the port variable, if not, then the port variable stays set at 8080."
```

