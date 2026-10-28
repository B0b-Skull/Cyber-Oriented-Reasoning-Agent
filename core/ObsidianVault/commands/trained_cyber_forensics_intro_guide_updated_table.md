---
title: "Trained Command Playbook: Cyber Forensics Intro Guide_updated_table.pdf"
tags:
  - active_enum
  - arp
  - credential_access
  - defense_evasion_firewall
  - enumeration
  - http
  - https
  - iptables
  - john
  - kerberos
  - mdp
  - netstat
  - nmap
  - passive_enum
  - pdf
  - powershell
  - privilege_escalation
  - pslist
  - responder
  - serial
  - trained
source_file: Cyber Forensics Intro Guide_updated_table.pdf
updated: 2026-10-24 00:58:20
---

# Trained Command Playbook: `Cyber Forensics Intro Guide_updated_table.pdf`

- **Source Document:** `~/Projects/CORA/Training/Cyber Forensics Intro Guide_updated_table.pdf`
- **CEGAR Verified Commands:** `17` (`0` malformed/unsafe snippets filtered)
- **MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`):** `17`
- **Discovered IPs/Subnets:** `172.16.157.136`
- **Discovered Interfaces:** `None`
- **Related Knowledge Note:** [[knowledge/trained_cyber_forensics_intro_guide_updated_table]]

## Distilled MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`)
| Pre-State ($s$) | Tactic ($\tau$) | Technique ($k$) | Tool ($u$) | Post-State ($s'$) | Verified Command ($c$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `volatility` | `s_passive_topology_mapped` | `volatility framework.  The below section will cover some of the most common plugins an` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `chmod` | `s_interactive_tty_or_priv_escalated` | `chmod g+r file` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `crontab` | `s_active_services_enumerated` | `crontab file, usually by running the crontab command. For example, the crontab entry` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `find` | `s_credentials_or_certs_acquired` | `find injected code.` |
| `s_passive_topology_mapped` | **`Active_Enum`** | Active Network, Cloud, Directory Service & Endpoint Probing | `traceroute` | `s_active_services_enumerated` | `Traceroute Attack` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `tracert` | `s_firewall_or_acl_unlocked` | `tracert command in Windows.` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `volatility` | `s_passive_topology_mapped` | `volatility plugin, filescan, parses for the file object tag in memory and lists all the opened` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `chmod` | `s_interactive_tty_or_priv_escalated` | `chmod o+r file` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `at` | `s_active_services_enumerated` | `At 22:30` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `volatility` | `s_passive_topology_mapped` | `volatility plugin can provide more information about VADs in one process.` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `chmod` | `s_interactive_tty_or_priv_escalated` | `chmod go+r file` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `crontab` | `s_passive_topology_mapped` | `crontab file to install file as your current crontab. The crontab command checks the file` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `chmod` | `s_interactive_tty_or_priv_escalated` | `chmod 644 file` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `crontab` | `s_passive_topology_mapped` | `crontab -l. To remove the crontab, use crontab -r.` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `and` | `s_interactive_tty_or_priv_escalated` | `SUDO AND /ETC/SUDOERS` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `find` | `s_passive_topology_mapped` | `find traces on the file system. To mitigate this challenge, use all of the information` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `find` | `s_interactive_tty_or_priv_escalated` | `find /mnt/evidence -user root -perm -04000 -print` |

## Verified Executable Commands (Grouped by Capability Layer)

### General_System (15 commands)
```bash
volatility framework.  The below section will cover some of the most common plugins an
volatility plugin, filescan, parses for the file object tag in memory and lists all the opened
volatility plugin can provide more information about VADs in one process.
chmod g+r file
chmod o+r file
chmod go+r file
chmod 644 file
SUDO AND /ETC/SUDOERS
crontab file, usually by running the crontab command. For example, the crontab entry
crontab file to install file as your current crontab. The crontab command checks the file
crontab -l. To remove the crontab, use crontab -r.
At 22:30
find /mnt/evidence -user root -perm -04000 -print
find traces on the file system. To mitigate this challenge, use all of the information
find injected code.
```

### L3_Routing_NAT (2 commands)
```bash
Traceroute Attack
tracert command in Windows.
```

