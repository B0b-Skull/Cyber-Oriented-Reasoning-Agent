---
title: "Trained Command Playbook: Cacls - Icacls CMDs 2.txt"
tags:
  - cacls
  - credential_access
  - enumeration
  - icacls
  - mdp
  - passive_enum
  - privilege_escalation
  - text
  - trained
source_file: Cacls - Icacls CMDs 2.txt
updated: 2026-10-24 00:57:01
---

# Trained Command Playbook: `Cacls - Icacls CMDs 2.txt`

- **Source Document:** `~/Projects/CORA/Training/Cacls - Icacls CMDs 2.txt`
- **CEGAR Verified Commands:** `40` (`0` malformed/unsafe snippets filtered)
- **MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`):** `40`
- **Discovered IPs/Subnets:** `None`
- **Discovered Interfaces:** `None`
- **Related Knowledge Note:** [[knowledge/trained_cacls_-_icacls_cmds_2]]

## Distilled MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`)
| Pre-State ($s$) | Tactic ($\tau$) | Technique ($k$) | Tool ($u$) | Post-State ($s'$) | Verified Command ($c$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `net` | `s_interactive_tty_or_priv_escalated` | `net localgroup "Power Users" larry moe /add` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `net` | `s_passive_topology_mapped` | `net localgroup users larry moe /delete` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `net` | `s_credentials_or_certs_acquired` | `net user larry 3st00g3s /add` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `md` | `s_active_services_enumerated` | `md "C:\The Stooges\Larry" "C:\The Stooges\Curly" "C:\The Stooges\Moe" "C:\The Stooges\Joe"` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `cacls` | `s_interactive_tty_or_priv_escalated` | `cacls c:\ /t /e /g Administrators:f` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `mkdir` | `s_passive_topology_mapped` | `mkdir "C:\The Stooges"` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `net` | `s_credentials_or_certs_acquired` | `net user Moe 3st00g3s /add` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `echo` | `s_active_services_enumerated` | `echo 'Hello Huey' > "c:\The Ducks\Huey\Hello-Huey.txt" & echo 'Hello Fred' > "c:\The Ducks\Fred\Hello-Fred.txt"` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `cacls` | `s_interactive_tty_or_priv_escalated` | `cacls "C:\The Stooges" /P user1:permissions  user2:permissions user3:permissions` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `net` | `s_passive_topology_mapped` | `net share sharename=drive:path /GRANT:user,[READ \| CHANGE \| FULL] /GRANT:user,[READ \| CHANGE \| FULL]` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `net` | `s_credentials_or_certs_acquired` | `net user Curly 3st00g3s /add` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `cacls` | `s_interactive_tty_or_priv_escalated` | `cacls "C:\The Stooges" /E /P /G "Power Users":f` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `net` | `s_credentials_or_certs_acquired` | `net user Joe 3st00g3s /add` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `cacls` | `s_interactive_tty_or_priv_escalated` | `cacls "C:\The Stooges\Larry" /E /G Larry:f & cacls "C:\The Stooges\Moe" /E /G Moe:f & cacls "C:\The Stooges\Curly" /E /G Curly:f & cacls "C:\The Stooges\Joe" /E /G Joe:f` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `echo` | `s_credentials_or_certs_acquired` | `echo 'Hello Joe' > "c:\The Stooges\Joe\Hello.txt" & echo 'Hello Moe' > "c:\The Stooges\Moe\Hello.txt"` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `cacls` | `s_interactive_tty_or_priv_escalated` | `cacls "C:\The Stooges\Larry" /E /R Users & cacls "C:\The Stooges\Moe" /E /R Users & cacls "C:\The Stooges\Curly" /E /R Users & cacls "C:\The Stooges\Joe" /E /R Users` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `net` | `s_credentials_or_certs_acquired` | `net user Larry /Time:M-F,1am-9am` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `cacls` | `s_interactive_tty_or_priv_escalated` | `cacls "C:\The Stooges\Moe\Hello.txt" /E /R Moe & cacls "C:\The Stooges\Joe\Hello.txt" /E /R Joe` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `net` | `s_credentials_or_certs_acquired` | `net user Huey $Password! /add` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `cacls` | `s_interactive_tty_or_priv_escalated` | `cacls "C:\The Stooges\Joe\Hello.txt" /E /g Joe:F & cacls "C:\The Stooges\Moe" /E /g Joe:W` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `net` | `s_credentials_or_certs_acquired` | `net user Dewey $Password! /add` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `icacls` | `s_interactive_tty_or_priv_escalated` | `icacls "d:\users" /grant "domain admins":(OI)(CI)F /inheritance:r` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `net` | `s_credentials_or_certs_acquired` | `net user Louie $Password! /add` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `icacls` | `s_interactive_tty_or_priv_escalated` | `icacls "d:\users" /grant "everyone":R /inheritance:r` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `net` | `s_credentials_or_certs_acquired` | `net user Fred $Password! /add` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `icacls` | `s_interactive_tty_or_priv_escalated` | `icacls "d:\profiles" /grant "domain admins":(OI)(CI)F /inheritance:r` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `net` | `s_credentials_or_certs_acquired` | `net localgroup Ducks /add` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `icacls` | `s_interactive_tty_or_priv_escalated` | `icacls "d:\profiles" /grant "everyone":R /inheritance:r` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `md` | `s_credentials_or_certs_acquired` | `md "C:\The Ducks\Huey" "C:\The Ducks\Dewey" "C:\The Ducks\Louie" "C:\The Ducks\Fred"` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `cacls` | `s_interactive_tty_or_priv_escalated` | `cacls "c:\The Ducks" /t /e /g Ducks:f` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `icacls` | `s_interactive_tty_or_priv_escalated` | `icacls "c:\The Ducks" /grant Ducks:(CI)(F)` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `icacls` | `s_interactive_tty_or_priv_escalated` | `icacls "c:\The Ducks\Huey" /grant Huey:F /remove "Users" & icacls "c:\The Ducks\Dewey" /grant Dewey:F /remove "Users" & icacls "c:\The Ducks\Louie" /grant Louie:F /remove "Users" & icacls "c:\The Ducks\Fred" /grant Fred:F /remove "Users"` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `icacls` | `s_interactive_tty_or_priv_escalated` | `icacls "c:\The Ducks" /inheritance:d` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `icacls` | `s_interactive_tty_or_priv_escalated` | `icacls "c:\The Ducks" /remove "Authenticated Users"` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `icacls` | `s_interactive_tty_or_priv_escalated` | `icacls "c:\The Ducks" /remove "Users"` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `icacls` | `s_interactive_tty_or_priv_escalated` | `icacls "c:\The Ducks\Huey" /grant Huey:F /remove "Users" /inheritance:e /t & icacls "c:\The Ducks\Dewey" /grant Dewey:F /remove "Users" /inheritance:e /t & icacls "c:\The Ducks\Louie" /grant Louie:F /remove "Users" /inheritance:e /t & icacls "c:\The Ducks\Fred" /grant Fred:F /remove "Users" /inheritance:e /t` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `icacls` | `s_interactive_tty_or_priv_escalated` | `icacls "c:\The Ducks\Huey" /grant Huey:F /remove "Users" /inheritance:d & icacls "c:\The Ducks\Dewey" /grant Dewey:F /remove "Users" /inheritance:d & icacls "c:\The Ducks\Louie" /grant Louie:F /remove "Users" /inheritance:d & icacls "c:\The Ducks\Fred" /grant Fred:F /remove "Users" /inheritance:d` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `icacls` | `s_interactive_tty_or_priv_escalated` | `icacls "c:\The Ducks\Huey" /remove "NT Authority\Authenticated Users" & icacls "c:\The Ducks\Dewey" /remove "NT Authority\Authenticated Users" & icacls "c:\The Ducks\Louie" /remove "NT Authority\Authenticated Users" & icacls "c:\The Ducks\Fred" /remove "NT Authority\Authenticated Users"` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `icacls` | `s_interactive_tty_or_priv_escalated` | `icacls "c:\The Ducks\fred" /grant fred:(F)` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `icacls` | `s_interactive_tty_or_priv_escalated` | `icacls "c:\The Ducks\Huey" /grant fred:(M) /t` |

## Verified Executable Commands (Grouped by Capability Layer)

### General_System (40 commands)
```bash
net localgroup "Power Users" larry moe /add
net localgroup users larry moe /delete
net user larry 3st00g3s /add
net user Moe 3st00g3s /add
net user Curly 3st00g3s /add
net user Joe 3st00g3s /add
mkdir "C:\The Stooges"
cacls c:\ /t /e /g Administrators:f
cacls "C:\The Stooges" /P user1:permissions  user2:permissions user3:permissions
cacls "C:\The Stooges" /E /P /G "Power Users":f
cacls "C:\The Stooges\Larry" /E /G Larry:f & cacls "C:\The Stooges\Moe" /E /G Moe:f & cacls "C:\The Stooges\Curly" /E /G Curly:f & cacls "C:\The Stooges\Joe" /E /G Joe:f
cacls "C:\The Stooges\Larry" /E /R Users & cacls "C:\The Stooges\Moe" /E /R Users & cacls "C:\The Stooges\Curly" /E /R Users & cacls "C:\The Stooges\Joe" /E /R Users
cacls "C:\The Stooges\Moe\Hello.txt" /E /R Moe & cacls "C:\The Stooges\Joe\Hello.txt" /E /R Joe
cacls "C:\The Stooges\Joe\Hello.txt" /E /g Joe:F & cacls "C:\The Stooges\Moe" /E /g Joe:W
md "C:\The Stooges\Larry" "C:\The Stooges\Curly" "C:\The Stooges\Moe" "C:\The Stooges\Joe"
icacls "d:\users" /grant "domain admins":(OI)(CI)F /inheritance:r
icacls "d:\users" /grant "everyone":R /inheritance:r
icacls "d:\profiles" /grant "domain admins":(OI)(CI)F /inheritance:r
icacls "d:\profiles" /grant "everyone":R /inheritance:r
net share sharename=drive:path /GRANT:user,[READ | CHANGE | FULL] /GRANT:user,[READ | CHANGE | FULL]
echo 'Hello Joe' > "c:\The Stooges\Joe\Hello.txt" & echo 'Hello Moe' > "c:\The Stooges\Moe\Hello.txt"
net user Larry /Time:M-F,1am-9am
net user Huey $Password! /add
net user Dewey $Password! /add
net user Louie $Password! /add
net user Fred $Password! /add
net localgroup Ducks /add
md "C:\The Ducks\Huey" "C:\The Ducks\Dewey" "C:\The Ducks\Louie" "C:\The Ducks\Fred"
cacls "c:\The Ducks" /t /e /g Ducks:f
icacls "c:\The Ducks" /grant Ducks:(CI)(F)
icacls "c:\The Ducks\Huey" /grant Huey:F /remove "Users" & icacls "c:\The Ducks\Dewey" /grant Dewey:F /remove "Users" & icacls "c:\The Ducks\Louie" /grant Louie:F /remove "Users" & icacls "c:\The Ducks\Fred" /grant Fred:F /remove "Users"
icacls "c:\The Ducks" /inheritance:d
icacls "c:\The Ducks" /remove "Authenticated Users"
icacls "c:\The Ducks" /remove "Users"
icacls "c:\The Ducks\Huey" /grant Huey:F /remove "Users" /inheritance:e /t & icacls "c:\The Ducks\Dewey" /grant Dewey:F /remove "Users" /inheritance:e /t & icacls "c:\The Ducks\Louie" /grant Louie:F /remove "Users" /inheritance:e /t & icacls "c:\The Ducks\Fred" /grant Fred:F /remove "Users" /inheritance:e /t
icacls "c:\The Ducks\Huey" /grant Huey:F /remove "Users" /inheritance:d & icacls "c:\The Ducks\Dewey" /grant Dewey:F /remove "Users" /inheritance:d & icacls "c:\The Ducks\Louie" /grant Louie:F /remove "Users" /inheritance:d & icacls "c:\The Ducks\Fred" /grant Fred:F /remove "Users" /inheritance:d
icacls "c:\The Ducks\Huey" /remove "NT Authority\Authenticated Users" & icacls "c:\The Ducks\Dewey" /remove "NT Authority\Authenticated Users" & icacls "c:\The Ducks\Louie" /remove "NT Authority\Authenticated Users" & icacls "c:\The Ducks\Fred" /remove "NT Authority\Authenticated Users"
echo 'Hello Huey' > "c:\The Ducks\Huey\Hello-Huey.txt" & echo 'Hello Fred' > "c:\The Ducks\Fred\Hello-Fred.txt"
icacls "c:\The Ducks\fred" /grant fred:(F)
icacls "c:\The Ducks\Huey" /grant fred:(M) /t
```

