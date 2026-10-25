---
title: "Trained Command Playbook: AuditPol CMDs.txt"
tags:
  - auditpol
  - credential_access
  - defense_evasion_firewall
  - kerberos
  - mdp
  - passive_enum
  - text
  - trained
  - wevtutil
  - wmic
source_file: AuditPol CMDs.txt
updated: 2026-10-25 00:56:13
---

# Trained Command Playbook: `AuditPol CMDs.txt`

- **Source Document:** `~/Projects/CORA/Training/AuditPol CMDs.txt`
- **CEGAR Verified Commands:** `30` (`0` malformed/unsafe snippets filtered)
- **MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`):** `30`
- **Discovered IPs/Subnets:** `None`
- **Discovered Interfaces:** `None`
- **Related Knowledge Note:** [[knowledge/trained_auditpol_cmds]]

## Distilled MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`)
| Pre-State ($s$) | Tactic ($\tau$) | Technique ($k$) | Tool ($u$) | Post-State ($s'$) | Verified Command ($c$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `psloglist` | `s_passive_topology_mapped` | `psloglist -n 10` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `auditpol` | `s_firewall_or_acl_unlocked` | `auditpol /list /category` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `wevtutil` | `s_credentials_or_certs_acquired` | `wevtutil qe System /c:10 /f:text` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `psloglist` | `s_passive_topology_mapped` | `psloglist -s -t "\t" -n 20 Security \| findstr /n /i .*SID.* \| findstr /n /i "Administrators"` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `auditpol` | `s_firewall_or_acl_unlocked` | `auditpol /list /subcategory:*` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `wmic` | `s_passive_topology_mapped` | `wmic useraccount where name='username'` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `auditpol` | `s_firewall_or_acl_unlocked` | `auditpol /list /user` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `psloglist` | `s_passive_topology_mapped` | `psloglist -s -t "\t" -n 20 Security \| findstr /n /i .*SID.*` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `auditpol` | `s_firewall_or_acl_unlocked` | `auditpol /get /category:*` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `wmic` | `s_passive_topology_mapped` | `wmic useraccount where name='username' get sid` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `auditpol` | `s_firewall_or_acl_unlocked` | `auditpol /set /subcategory:"Sensitive Privilege Use" /success:enable` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `psloglist` | `s_passive_topology_mapped` | `psloglist -s -t "\t" Security \| findstr /n /i .* SID .*` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `auditpol` | `s_firewall_or_acl_unlocked` | `auditpol /set /subcategory:"user account management"` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `auditpol` | `s_firewall_or_acl_unlocked` | `auditpol /set /subcategory:"IPsec Driver" /success:disable` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `auditpol` | `s_firewall_or_acl_unlocked` | `Auditpol /set /subcategory:"Account Lockout" /success:disable` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `auditpol` | `s_firewall_or_acl_unlocked` | `Auditpol /set /subcategory:"Registry" /success:enable /failure:enable` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `auditpol` | `s_firewall_or_acl_unlocked` | `Auditpol /set /subcategory:"Kernel Object" /success:enable` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `auditpol` | `s_firewall_or_acl_unlocked` | `Auditpol /set /subcategory:"Audit Policy Change" /success:enable /failure:enable` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `auditpol` | `s_firewall_or_acl_unlocked` | `Auditpol /set /subcategory:"Directory Service Changes" /success:enable` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `auditpol` | `s_firewall_or_acl_unlocked` | `Auditpol /set /subcategory:"Kerberos Service Ticket Operations" /success:enable` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `auditpol` | `s_firewall_or_acl_unlocked` | `Auditpol /set /subcategory:"Security System Extension" /success:disable` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `auditpol` | `s_firewall_or_acl_unlocked` | `Auditpol /set /subcategory:"IPsec Extended Mode" /success:disable` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `auditpol` | `s_firewall_or_acl_unlocked` | `Auditpol /set /subcategory:"Network Policy Server" /success:enable /failure:enable` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `auditpol` | `s_firewall_or_acl_unlocked` | `Auditpol /set /subcategory:"SAM" /success:enable` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `auditpol` | `s_firewall_or_acl_unlocked` | `Auditpol /set /subcategory:"File Share" /success:enable /failure:enable` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `auditpol` | `s_firewall_or_acl_unlocked` | `Auditpol /set /subcategory:"Sensitive Privilege Use" /success:enable /failure:enable` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `auditpol` | `s_firewall_or_acl_unlocked` | `Auditpol /set /subcategory:"User Account Management" /success:enable` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `auditpol` | `s_firewall_or_acl_unlocked` | `Auditpol /set /subcategory:"Computer Account Management" /success:enable` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `auditpol` | `s_firewall_or_acl_unlocked` | `Auditpol /set /subcategory:"Kerberos Authentication Service" /failure:enable` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `auditpol` | `s_firewall_or_acl_unlocked` | `Auditpol /set /subcategory:"Credential Validation" /success:enable` |

## Verified Executable Commands (Grouped by Capability Layer)

### General_System (30 commands)
```bash
psloglist -n 10
psloglist -s -t "\t" -n 20 Security | findstr /n /i .*SID.* | findstr /n /i "Administrators"
auditpol /list /category
auditpol /list /subcategory:*
auditpol /list /user
auditpol /get /category:*
auditpol /set /subcategory:"Sensitive Privilege Use" /success:enable
auditpol /set /subcategory:"user account management"
auditpol /set /subcategory:"IPsec Driver" /success:disable
Auditpol /set /subcategory:"Account Lockout" /success:disable
Auditpol /set /subcategory:"Registry" /success:enable /failure:enable
Auditpol /set /subcategory:"Kernel Object" /success:enable
Auditpol /set /subcategory:"Audit Policy Change" /success:enable /failure:enable
Auditpol /set /subcategory:"Directory Service Changes" /success:enable
Auditpol /set /subcategory:"Kerberos Service Ticket Operations" /success:enable
Auditpol /set /subcategory:"Security System Extension" /success:disable
Auditpol /set /subcategory:"IPsec Extended Mode" /success:disable
Auditpol /set /subcategory:"Network Policy Server" /success:enable /failure:enable
Auditpol /set /subcategory:"SAM" /success:enable
Auditpol /set /subcategory:"File Share" /success:enable /failure:enable
Auditpol /set /subcategory:"Sensitive Privilege Use" /success:enable /failure:enable
Auditpol /set /subcategory:"User Account Management" /success:enable
Auditpol /set /subcategory:"Computer Account Management" /success:enable
Auditpol /set /subcategory:"Kerberos Authentication Service" /failure:enable
Auditpol /set /subcategory:"Credential Validation" /success:enable
wevtutil qe System /c:10 /f:text
wmic useraccount where name='username'
psloglist -s -t "\t" -n 20 Security | findstr /n /i .*SID.*
wmic useraccount where name='username' get sid
psloglist -s -t "\t" Security | findstr /n /i .* SID .*
```

