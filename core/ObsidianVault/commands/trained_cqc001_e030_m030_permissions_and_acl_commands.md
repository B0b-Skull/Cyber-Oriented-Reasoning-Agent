---
title: "Trained Command Playbook: CQC001_E030_M030_Permissions_and_ACL_Commands.pdf"
tags:
  - cacls
  - credential_access
  - enumeration
  - http
  - https
  - icacls
  - mdp
  - passive_enum
  - pdf
  - privilege_escalation
  - trained
source_file: CQC001_E030_M030_Permissions_and_ACL_Commands.pdf
updated: 2026-10-24 00:57:38
---

# Trained Command Playbook: `CQC001_E030_M030_Permissions_and_ACL_Commands.pdf`

- **Source Document:** `~/Projects/CORA/Training/CQC001_E030_M030_Permissions_and_ACL_Commands.pdf`
- **CEGAR Verified Commands:** `32` (`0` malformed/unsafe snippets filtered)
- **MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`):** `32`
- **Discovered IPs/Subnets:** `None`
- **Discovered Interfaces:** `None`
- **Related Knowledge Note:** [[knowledge/trained_cqc001_e030_m030_permissions_and_acl_commands]]

## Distilled MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`)
| Pre-State ($s$) | Tactic ($\tau$) | Technique ($k$) | Tool ($u$) | Post-State ($s'$) | Verified Command ($c$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `net` | `s_credentials_or_certs_acquired` | `Net user` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `net` | `s_active_services_enumerated` | `net help user \| more` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `net` | `s_passive_topology_mapped` | `Net localgroup` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `cacls` | `s_interactive_tty_or_priv_escalated` | `cacls FileName [/t] [/e] [/c] [/g User:permission] [/r User [...]] [/p User:permission [...]] [/d User [...]]` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `net` | `s_credentials_or_certs_acquired` | `net user [username [password \| *] [options]] [/domain]` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `net` | `s_active_services_enumerated` | `net help command: Displays help for the specified net command.` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `net` | `s_passive_topology_mapped` | `net localgroup [GroupName [/comment:"text"]] [/domain]` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `icacls` | `s_interactive_tty_or_priv_escalated` | `icacls <FileName> [/grant[:r] <Sid>:<Perm>[...]] [/deny <Sid>:<Perm>[...]] [/remove[:g\|:d]]` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `net` | `s_credentials_or_certs_acquired` | `Net user https://web.archive.org/web/20160804124854/https://technet.microsoft.com/en-us/library/Cc771865.aspx` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `write-only` | `s_active_services_enumerated` | `write-only access` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `net` | `s_passive_topology_mapped` | `net localgroup [GroupName {/add [/comment:"text"] \| /delete} [/domain]]` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `icacls` | `s_interactive_tty_or_priv_escalated` | `icacls <Directory> [/substitute <SidOld> <SidNew> [...]] [/restore <ACLfile> [/c] [/l] [/q]]` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `net` | `s_credentials_or_certs_acquired` | `Net localgroup https://web.archive.org/web/20160804124941/https://technet.microsoft.com/en-` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `net` | `s_passive_topology_mapped` | `net localgroup [GroupName name [ ...] {/add \| /delete} [/domain]]` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `icacls` | `s_interactive_tty_or_priv_escalated` | `icacls c:\windows\* /save aclfile /t` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `net` | `s_passive_topology_mapped` | `net localgroup` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `icacls` | `s_interactive_tty_or_priv_escalated` | `icacls c:\windows\ /restore aclfile` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `net` | `s_passive_topology_mapped` | `net localgroup exec /add` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `icacls` | `s_interactive_tty_or_priv_escalated` | `icacls test1 /grant User1:(d,wdac)` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `net` | `s_passive_topology_mapped` | `net localgroup exec /add /domain` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `icacls` | `s_interactive_tty_or_priv_escalated` | `icacls test2 /grant *S-1-1-0:(d,wdac)` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `net` | `s_passive_topology_mapped` | `net localgroup exec stevev sales\ralphr jennyt /add` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `runas` | `s_interactive_tty_or_priv_escalated` | `runas [{/profile\|/noprofile}] [/env] [/netonly] [/smartcard] [/showtrustlevels] [/trustlevel] /user:UserAccountName program` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `net` | `s_passive_topology_mapped` | `net localgroup exec stevev ralphr jennyt /add /domain` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `runas` | `s_interactive_tty_or_priv_escalated` | `runas /user:localmachinename\administrator cmd` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `net` | `s_passive_topology_mapped` | `net localgroup exec` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `runas` | `s_interactive_tty_or_priv_escalated` | `runas /user:companydomain\domainadmin "mmc %windir%\system32\compmgmt.msc"` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `net` | `s_passive_topology_mapped` | `net localgroup exec /comment:"The executive staff."` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `runas` | `s_interactive_tty_or_priv_escalated` | `runas /user:user@domain.microsoft.com "notepad my_file.txt"` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `runas` | `s_interactive_tty_or_priv_escalated` | `runas /netonly /user:domain\username "command"` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `cacls` | `s_interactive_tty_or_priv_escalated` | `CACLS https://web.archive.org/web/20160804125059/https://technet.microsoft.com/en-us/library/bb490872.aspx` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `icacls` | `s_interactive_tty_or_priv_escalated` | `ICACLS https://web.archive.org/web/20160611031312/https://technet.microsoft.com/en-` |

## Verified Executable Commands (Grouped by Capability Layer)

### General_System (28 commands)
```bash
Net user
net user [username [password | *] [options]] [/domain]
net help user | more
Net localgroup
net localgroup [GroupName [/comment:"text"]] [/domain]
net localgroup [GroupName {/add [/comment:"text"] | /delete} [/domain]]
net localgroup [GroupName name [ ...] {/add | /delete} [/domain]]
net help command: Displays help for the specified net command.
net localgroup
net localgroup exec /add
net localgroup exec /add /domain
net localgroup exec stevev sales\ralphr jennyt /add
net localgroup exec stevev ralphr jennyt /add /domain
net localgroup exec
net localgroup exec /comment:"The executive staff."
cacls FileName [/t] [/e] [/c] [/g User:permission] [/r User [...]] [/p User:permission [...]] [/d User [...]]
icacls <FileName> [/grant[:r] <Sid>:<Perm>[...]] [/deny <Sid>:<Perm>[...]] [/remove[:g|:d]]
icacls <Directory> [/substitute <SidOld> <SidNew> [...]] [/restore <ACLfile> [/c] [/l] [/q]]
write-only access
icacls c:\windows\* /save aclfile /t
icacls c:\windows\ /restore aclfile
icacls test1 /grant User1:(d,wdac)
icacls test2 /grant *S-1-1-0:(d,wdac)
runas [{/profile|/noprofile}] [/env] [/netonly] [/smartcard] [/showtrustlevels] [/trustlevel] /user:UserAccountName program
runas /user:localmachinename\administrator cmd
runas /user:companydomain\domainadmin "mmc %windir%\system32\compmgmt.msc"
runas /user:user@domain.microsoft.com "notepad my_file.txt"
runas /netonly /user:domain\username "command"
```

### L7_HTTP_Web (4 commands)
```bash
Net user https://web.archive.org/web/20160804124854/https://technet.microsoft.com/en-us/library/Cc771865.aspx
Net localgroup https://web.archive.org/web/20160804124941/https://technet.microsoft.com/en-
CACLS https://web.archive.org/web/20160804125059/https://technet.microsoft.com/en-us/library/bb490872.aspx
ICACLS https://web.archive.org/web/20160611031312/https://technet.microsoft.com/en-
```

