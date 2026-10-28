---
title: "Trained Command Playbook: Shells_and_Scripting.pdf"
tags:
  - credential_access
  - enumeration
  - http
  - https
  - mdp
  - passive_enum
  - pdf
  - trained
source_file: Shells_and_Scripting.pdf
updated: 2026-10-24 01:00:25
---

# Trained Command Playbook: `Shells_and_Scripting.pdf`

- **Source Document:** `~/Projects/CORA/Training/Shells_and_Scripting.pdf`
- **CEGAR Verified Commands:** `8` (`0` malformed/unsafe snippets filtered)
- **MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`):** `8`
- **Discovered IPs/Subnets:** `None`
- **Discovered Interfaces:** `None`
- **Related Knowledge Note:** [[knowledge/trained_shells_and_scripting]]

## Distilled MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`)
| Pre-State ($s$) | Tactic ($\tau$) | Technique ($k$) | Tool ($u$) | Post-State ($s'$) | Verified Command ($c$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `history` | `s_passive_topology_mapped` | `history` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `erase` | `s_active_services_enumerated` | `Erase variable or function definitions` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `echo` | `s_credentials_or_certs_acquired` | `echo -E` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `echo` | `s_active_services_enumerated` | `echo `expr $1 + $2`` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `echo` | `s_active_services_enumerated` | `echo $sum` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `echo` | `s_active_services_enumerated` | `echo "Helloworld" 3<> echo_output.txt 1>&3` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `echo` | `s_active_services_enumerated` | `echo -n . >&3` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `cat` | `s_active_services_enumerated` | `cat output.txt` |

## Verified Executable Commands (Grouped by Capability Layer)

### General_System (8 commands)
```bash
history
Erase variable or function definitions
echo -E
echo `expr $1 + $2`
echo $sum
echo "Helloworld" 3<> echo_output.txt 1>&3
echo -n . >&3
cat output.txt
```

