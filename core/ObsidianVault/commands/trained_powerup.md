---
title: "Trained Command Playbook: PowerUp.pdf"
tags:
  - credential_access
  - http
  - john
  - mdp
  - pdf
  - powershell
  - privilege_escalation
  - trained
source_file: PowerUp.pdf
updated: 2026-10-24 01:00:08
---

# Trained Command Playbook: `PowerUp.pdf`

- **Source Document:** `~/Projects/CORA/Training/PowerUp.pdf`
- **CEGAR Verified Commands:** `13` (`0` malformed/unsafe snippets filtered)
- **MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`):** `13`
- **Discovered IPs/Subnets:** `None`
- **Discovered Interfaces:** `None`
- **Related Knowledge Note:** [[knowledge/trained_powerup]]

## Distilled MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`)
| Pre-State ($s$) | Tactic ($\tau$) | Technique ($k$) | Tool ($u$) | Post-State ($s'$) | Verified Command ($c$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `import-module` | `s_interactive_tty_or_priv_escalated` | `Import-Module PowerUp.ps1` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `install-servicebinary` | `s_credentials_or_certs_acquired` | `Install-ServiceBinary backs up the original service path to` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `invoke-privescaudit` | `s_interactive_tty_or_priv_escalated` | `Invoke-PrivescAudit (old Invoke-AllChecks) will run all` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `get-webconfig` | `s_credentials_or_certs_acquired` | `Get-Webconfig` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `get-modifiableservice` | `s_interactive_tty_or_priv_escalated` | `Get-ModifiableService` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `strings` | `s_credentials_or_certs_acquired` | `strings from all web.configs.` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `get-` | `s_interactive_tty_or_priv_escalated` | `Get-` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `get-sitelistpassword` | `s_credentials_or_certs_acquired` | `Get-SiteListPassword` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `get-serviceunquoted` | `s_interactive_tty_or_priv_escalated` | `Get-ServiceUnquoted` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `enable-privilege` | `s_credentials_or_certs_acquired` | `Enable-Privilege` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `install-servicebinary` | `s_interactive_tty_or_priv_escalated` | `Install-ServiceBinary installs a malicious C# binary for a` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `write-hijackdll` | `s_interactive_tty_or_priv_escalated` | `Write-HijackDll writes out a self-deleting .bat file to` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `invoke-` | `s_interactive_tty_or_priv_escalated` | `Invoke-` |

## Verified Executable Commands (Grouped by Capability Layer)

### General_System (13 commands)
```bash
Import-Module PowerUp.ps1
Invoke-PrivescAudit (old Invoke-AllChecks) will run all
Get-ModifiableService
Get-
Get-ServiceUnquoted
Install-ServiceBinary installs a malicious C# binary for a
Install-ServiceBinary backs up the original service path to
Write-HijackDll writes out a self-deleting .bat file to
Get-Webconfig
strings from all web.configs.
Get-SiteListPassword
Enable-Privilege
Invoke-
```

