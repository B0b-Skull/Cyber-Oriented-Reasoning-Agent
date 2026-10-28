---
title: "Trained Command Playbook: CQC001_E030_M050_Auditing_Tools.pdf"
tags:
  - auditpol
  - credential_access
  - defense_evasion_firewall
  - https
  - mdp
  - pdf
  - trained
source_file: CQC001_E030_M050_Auditing_Tools.pdf
updated: 2026-10-24 00:57:38
---

# Trained Command Playbook: `CQC001_E030_M050_Auditing_Tools.pdf`

- **Source Document:** `~/Projects/CORA/Training/CQC001_E030_M050_Auditing_Tools.pdf`
- **CEGAR Verified Commands:** `9` (`0` malformed/unsafe snippets filtered)
- **MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`):** `9`
- **Discovered IPs/Subnets:** `None`
- **Discovered Interfaces:** `None`
- **Related Knowledge Note:** [[knowledge/trained_cqc001_e030_m050_auditing_tools]]

## Distilled MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`)
| Pre-State ($s$) | Tactic ($\tau$) | Technique ($k$) | Tool ($u$) | Post-State ($s'$) | Verified Command ($c$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `auditpol` | `s_firewall_or_acl_unlocked` | `Auditpol.exe (for Windows XP and 2003)` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `psloglist` | `s_credentials_or_certs_acquired` | `PsLogList dumps event logs on a local or remote NT system.` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `auditpol` | `s_firewall_or_acl_unlocked` | `AuditPol [\\computer] [/enable \| /disable] [/help \| /?] [/Category:Option]` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `auditpol` | `s_firewall_or_acl_unlocked` | `AUDITPOL \\MyComputer` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `auditpol` | `s_firewall_or_acl_unlocked` | `AUDITPOL \\MyComputer /enable /system:all /object:failure` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `auditpol` | `s_firewall_or_acl_unlocked` | `AUDITPOL \\MyComputer /disable` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `auditpol` | `s_firewall_or_acl_unlocked` | `AUDITPOL /logon:failure /system:all /sam:success /privilege:none` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `auditpol` | `s_firewall_or_acl_unlocked` | `AUDITPOL /HELP \| MORE displays Help one screen at a time.` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `auditpol` | `s_firewall_or_acl_unlocked` | `Auditpol.exe (for Windows 7)` |

## Verified Executable Commands (Grouped by Capability Layer)

### General_System (9 commands)
```bash
Auditpol.exe (for Windows XP and 2003)
AuditPol [\\computer] [/enable | /disable] [/help | /?] [/Category:Option]
AUDITPOL \\MyComputer
AUDITPOL \\MyComputer /enable /system:all /object:failure
AUDITPOL \\MyComputer /disable
AUDITPOL /logon:failure /system:all /sam:success /privilege:none
AUDITPOL /HELP | MORE displays Help one screen at a time.
Auditpol.exe (for Windows 7)
PsLogList dumps event logs on a local or remote NT system.
```

