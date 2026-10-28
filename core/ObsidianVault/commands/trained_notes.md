---
title: "Trained Command Playbook: Notes.txt"
tags:
  - https
  - mdp
  - netstat
  - passive_enum
  - text
  - trained
source_file: Notes.txt
updated: 2026-10-24 00:59:25
---

# Trained Command Playbook: `Notes.txt`

- **Source Document:** `~/Projects/CORA/Training/Notes.txt`
- **CEGAR Verified Commands:** `2` (`0` malformed/unsafe snippets filtered)
- **MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`):** `2`
- **Discovered IPs/Subnets:** `None`
- **Discovered Interfaces:** `None`
- **Related Knowledge Note:** [[knowledge/trained_notes]]

## Distilled MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`)
| Pre-State ($s$) | Tactic ($\tau$) | Technique ($k$) | Tool ($u$) | Post-State ($s'$) | Verified Command ($c$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `echo` | `s_passive_topology_mapped` | `echo "[ solaris netstat ]" && pfiles `ls /proc` 2>/dev/null \| awk "/^ [^ \\t]/{smatch=\$0;next}/port:[ \\t]*${1}/{print smatch, \$0}{next}" \| awk '{printf "PID %-5s %-30s Port %-5s \n",$1,$2,$NF}' \| grep -v "Port 0"` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `strings` | `s_passive_topology_mapped` | `strings <FILE> \| grep --color -En 'AF\|INET\|SOCK'` |

## Verified Executable Commands (Grouped by Capability Layer)

### General_System (2 commands)
```bash
echo "[ solaris netstat ]" && pfiles `ls /proc` 2>/dev/null | awk "/^ [^ \\t]/{smatch=\$0;next}/port:[ \\t]*${1}/{print smatch, \$0}{next}" | awk '{printf "PID %-5s %-30s Port %-5s \n",$1,$2,$NF}' | grep -v "Port 0"
strings <FILE> | grep --color -En 'AF|INET|SOCK'
```

