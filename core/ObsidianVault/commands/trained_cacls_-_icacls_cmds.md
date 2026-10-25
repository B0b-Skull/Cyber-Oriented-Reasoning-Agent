---
title: "Trained Command Playbook: Cacls - Icacls CMDs.txt"
tags:
  - cacls
  - credential_access
  - icacls
  - mdp
  - privilege_escalation
  - text
  - trained
source_file: Cacls - Icacls CMDs.txt
updated: 2026-10-25 00:57:01
---

# Trained Command Playbook: `Cacls - Icacls CMDs.txt`

- **Source Document:** `~/Projects/CORA/Training/Cacls - Icacls CMDs.txt`
- **CEGAR Verified Commands:** `21` (`0` malformed/unsafe snippets filtered)
- **MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`):** `21`
- **Discovered IPs/Subnets:** `None`
- **Discovered Interfaces:** `None`
- **Related Knowledge Note:** [[knowledge/trained_cacls_-_icacls_cmds]]

## Distilled MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`)
| Pre-State ($s$) | Tactic ($\tau$) | Technique ($k$) | Tool ($u$) | Post-State ($s'$) | Verified Command ($c$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `net` | `s_credentials_or_certs_acquired` | `net user Orange $Password! /add` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `cacls` | `s_interactive_tty_or_priv_escalated` | `cacls c:\Ledge\Old\Orange.txt /g Orange:F` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `net` | `s_credentials_or_certs_acquired` | `net user Blue $Password! /add` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `cacls` | `s_interactive_tty_or_priv_escalated` | `cacls c:\Ledge\Old\Blue.txt /g Blue:F` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `net` | `s_credentials_or_certs_acquired` | `net user Banana $Password! /add` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `cacls` | `s_interactive_tty_or_priv_escalated` | `cacls c:\Ledge\Old\Banana.txt /g Banana:F` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `net` | `s_credentials_or_certs_acquired` | `net localgroup Fruit /add` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `icacls` | `s_interactive_tty_or_priv_escalated` | `icacls C:\Ledge\Old\Orange.txt /grant Orange:F` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `net` | `s_credentials_or_certs_acquired` | `net localgroup Color /add` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `icacls` | `s_interactive_tty_or_priv_escalated` | `icacls C:\Ledge\Old\Blue.txt /grant Blue:F` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `net` | `s_credentials_or_certs_acquired` | `net localgroup Fruit Banana Orange /add` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `icacls` | `s_interactive_tty_or_priv_escalated` | `icacls C:\Ledge\Old\Banana.txt /grant Banana:F` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `echo` | `s_credentials_or_certs_acquired` | `echo 'Hello Orange' > "c:\Ledge\Old\Orange.txt" & echo 'Hello Blue' > "c:\Ledge\Old\Blue.txt" & echo 'Hello Banana' > "c:\Ledge\Old\Banana.txt"` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `icacls` | `s_interactive_tty_or_priv_escalated` | `icacls C:\Ledge\Bold /grant Color:(OI)(R)` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `net` | `s_credentials_or_certs_acquired` | `net localgroup Fruit Orange Banana /add` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `icacls` | `s_interactive_tty_or_priv_escalated` | `icacls C:\Ledge\Bold\Leaf.txt /inheritance:D` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `net` | `s_credentials_or_certs_acquired` | `net localgroup Color Orange Blue /add` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `icacls` | `s_interactive_tty_or_priv_escalated` | `icacls C:\Ledge\Bold\Leaf.txt /remove Color` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `icacls` | `s_interactive_tty_or_priv_escalated` | `icacls C:\Ledge /grant Fruit:(CI)(W)` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `icacls` | `s_interactive_tty_or_priv_escalated` | `icacls C:\Ledge\Bold\Leaf.txt /remove Fruit` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `icacls` | `s_interactive_tty_or_priv_escalated` | `icacls C:\Ledge\Bold\Leaf.txt /remove Blue` |

## Verified Executable Commands (Grouped by Capability Layer)

### General_System (21 commands)
```bash
net user Orange $Password! /add
net user Blue $Password! /add
net user Banana $Password! /add
net localgroup Fruit /add
net localgroup Color /add
net localgroup Fruit Banana Orange /add
cacls c:\Ledge\Old\Orange.txt /g Orange:F
cacls c:\Ledge\Old\Blue.txt /g Blue:F
cacls c:\Ledge\Old\Banana.txt /g Banana:F
echo 'Hello Orange' > "c:\Ledge\Old\Orange.txt" & echo 'Hello Blue' > "c:\Ledge\Old\Blue.txt" & echo 'Hello Banana' > "c:\Ledge\Old\Banana.txt"
net localgroup Fruit Orange Banana /add
net localgroup Color Orange Blue /add
icacls C:\Ledge\Old\Orange.txt /grant Orange:F
icacls C:\Ledge\Old\Blue.txt /grant Blue:F
icacls C:\Ledge\Old\Banana.txt /grant Banana:F
icacls C:\Ledge\Bold /grant Color:(OI)(R)
icacls C:\Ledge\Bold\Leaf.txt /inheritance:D
icacls C:\Ledge\Bold\Leaf.txt /remove Color
icacls C:\Ledge /grant Fruit:(CI)(W)
icacls C:\Ledge\Bold\Leaf.txt /remove Fruit
icacls C:\Ledge\Bold\Leaf.txt /remove Blue
```

