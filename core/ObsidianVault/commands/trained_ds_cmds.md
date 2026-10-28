---
title: "Trained Command Playbook: DS CMDs.txt"
tags:
  - active_enum
  - credential_access
  - dsquery
  - http
  - mdp
  - privilege_escalation
  - text
  - trained
source_file: DS CMDs.txt
updated: 2026-10-24 00:58:21
---

# Trained Command Playbook: `DS CMDs.txt`

- **Source Document:** `~/Projects/CORA/Training/DS CMDs.txt`
- **CEGAR Verified Commands:** `27` (`0` malformed/unsafe snippets filtered)
- **MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`):** `27`
- **Discovered IPs/Subnets:** `None`
- **Discovered Interfaces:** `None`
- **Related Knowledge Note:** [[knowledge/trained_ds_cmds]]

## Distilled MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`)
| Pre-State ($s$) | Tactic ($\tau$) | Technique ($k$) | Tool ($u$) | Post-State ($s'$) | Verified Command ($c$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `dsadd` | `s_credentials_or_certs_acquired` | `dsadd user -samid prohenry -fn Peabody -mi R -ln OHenry -display prohenry -pwd S3@Ba$$  -memberof Managers  -email prohenry@ops.local -hometel 987-654-3210  -title "Infrastructure Technician" -pwdneverexpires  no  -disabled yes` |
| `s_passive_topology_mapped` | **`Active_Enum`** | Active Network, Cloud, Directory Service & Endpoint Probing | `dsquery` | `s_active_services_enumerated` | `dsquery ou dc=mydom,dc=com` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `dsmod` | `s_interactive_tty_or_priv_escalated` | `dsmod group CN=Managers,CN=users,DC=ops,DC=local -addmbr "CN=Mike Carpenter,OU=Customer Service,dc=ops,dc=local"` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `dsmod` | `s_credentials_or_certs_acquired` | `dsmod user "cn=guyt, ou=guyds, dc=cp, dc=com" -pwd a1yC24kg` |
| `s_passive_topology_mapped` | **`Active_Enum`** | Active Network, Cloud, Directory Service & Endpoint Probing | `dsquery` | `s_active_services_enumerated` | `dsquery ou domainroot` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `dsmod` | `s_interactive_tty_or_priv_escalated` | `dsmod group "CN=Managers,CN=Users,DC=ops,DC=local" -addmbr "CN=Your Name,CN=Users,DC=ops,DC=local"` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `dsadd` | `s_credentials_or_certs_acquired` | `dsadd user "cn=pault, ou=guyds, dc=cp, dc=com" -pwd a1yC24k` |
| `s_passive_topology_mapped` | **`Active_Enum`** | Active Network, Cloud, Directory Service & Endpoint Probing | `dsquery` | `s_active_services_enumerated` | `dsquery user cn=users,dc=cp,dc=com` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `dsmod` | `s_credentials_or_certs_acquired` | `dsmod user "CN=Mike Carpenter,OU=Customer Service,DC=ops,DC=local" -desc "Production Manager"` |
| `s_passive_topology_mapped` | **`Active_Enum`** | Active Network, Cloud, Directory Service & Endpoint Probing | `dsquery` | `s_active_services_enumerated` | `dsquery user domainroot -name smith*` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `dsadd` | `s_credentials_or_certs_acquired` | `dsadd user "CN=xxx xxx,CN=users,DC=ops,DC=local" -samid xxx -upn xxx@ops.local -fn "xxx" -ln "xxx" -display "xxx xxx" -pwd xxx -desc "xxxx" -disabled no` |
| `s_passive_topology_mapped` | **`Active_Enum`** | Active Network, Cloud, Directory Service & Endpoint Probing | `dsquery` | `s_active_services_enumerated` | `dsquery user dc=cp,dc=com -name smith* d` |
| `s_passive_topology_mapped` | **`Active_Enum`** | Active Network, Cloud, Directory Service & Endpoint Probing | `dsquery` | `s_active_services_enumerated` | `dsquery user -name *chris*` |
| `s_passive_topology_mapped` | **`Active_Enum`** | Active Network, Cloud, Directory Service & Endpoint Probing | `dsquery` | `s_active_services_enumerated` | `dsquery computer` |
| `s_passive_topology_mapped` | **`Active_Enum`** | Active Network, Cloud, Directory Service & Endpoint Probing | `dsquery` | `s_active_services_enumerated` | `dsquery computer -name *` |
| `s_passive_topology_mapped` | **`Active_Enum`** | Active Network, Cloud, Directory Service & Endpoint Probing | `dsquery` | `s_active_services_enumerated` | `dsquery computer domainroot -name "xp"` |
| `s_passive_topology_mapped` | **`Active_Enum`** | Active Network, Cloud, Directory Service & Endpoint Probing | `dsget` | `s_active_services_enumerated` | `dsget user "CN=Christopher Bryce,OU=Customer Service,DC=ops,DC=local"` |
| `s_passive_topology_mapped` | **`Active_Enum`** | Active Network, Cloud, Directory Service & Endpoint Probing | `dsquery` | `s_active_services_enumerated` | `dsquery user -name *Phillips* \| dsget user -samid` |
| `s_passive_topology_mapped` | **`Active_Enum`** | Active Network, Cloud, Directory Service & Endpoint Probing | `dsquery` | `s_active_services_enumerated` | `dsquery user -name *phillips* \| dsget user -desc` |
| `s_passive_topology_mapped` | **`Active_Enum`** | Active Network, Cloud, Directory Service & Endpoint Probing | `dsquery` | `s_active_services_enumerated` | `dsquery user -name *phillips* \| dsget user -memberof` |
| `s_passive_topology_mapped` | **`Active_Enum`** | Active Network, Cloud, Directory Service & Endpoint Probing | `dsquery` | `s_active_services_enumerated` | `dsquery group "cn=Domain Admins,cn=users,dc=ops,dc=local" \| dsget group -members` |
| `s_passive_topology_mapped` | **`Active_Enum`** | Active Network, Cloud, Directory Service & Endpoint Probing | `dsquery` | `s_active_services_enumerated` | `dsquery * -attr operatingSystem operatingSystemServicePack -filter "(\|(operatingSystem=*))"` |
| `s_passive_topology_mapped` | **`Active_Enum`** | Active Network, Cloud, Directory Service & Endpoint Probing | `dsquery` | `s_active_services_enumerated` | `dsquery user -name *carpenter*` |
| `s_passive_topology_mapped` | **`Active_Enum`** | Active Network, Cloud, Directory Service & Endpoint Probing | `dsquery` | `s_active_services_enumerated` | `dsquery user -name *carpenter* \| dsget user -memberof` |
| `s_passive_topology_mapped` | **`Active_Enum`** | Active Network, Cloud, Directory Service & Endpoint Probing | `dsquery` | `s_active_services_enumerated` | `dsquery user -name *carpenter* \| dsget user -dn -desc` |
| `s_passive_topology_mapped` | **`Active_Enum`** | Active Network, Cloud, Directory Service & Endpoint Probing | `dsquery` | `s_active_services_enumerated` | `dsquery group "CN=users,dc=ops,dc=local"` |
| `s_passive_topology_mapped` | **`Active_Enum`** | Active Network, Cloud, Directory Service & Endpoint Probing | `dsquery` | `s_active_services_enumerated` | `dsquery group "CN=Managers,CN=Users,DC=ops,DC=local" \| dsget group -members` |

## Verified Executable Commands (Grouped by Capability Layer)

### General_System (27 commands)
```bash
dsadd user -samid prohenry -fn Peabody -mi R -ln OHenry -display prohenry -pwd S3@Ba$$  -memberof Managers  -email prohenry@ops.local -hometel 987-654-3210  -title "Infrastructure Technician" -pwdneverexpires  no  -disabled yes
dsmod user "cn=guyt, ou=guyds, dc=cp, dc=com" -pwd a1yC24kg
dsadd user "cn=pault, ou=guyds, dc=cp, dc=com" -pwd a1yC24k
dsquery ou dc=mydom,dc=com
dsquery ou domainroot
dsquery user cn=users,dc=cp,dc=com
dsquery user domainroot -name smith*
dsquery user dc=cp,dc=com -name smith* d
dsquery user -name *chris*
dsquery computer
dsquery computer -name *
dsquery computer domainroot -name "xp"
dsget user "CN=Christopher Bryce,OU=Customer Service,DC=ops,DC=local"
dsquery user -name *Phillips* | dsget user -samid
dsquery user -name *phillips* | dsget user -desc
dsquery user -name *phillips* | dsget user -memberof
dsquery group "cn=Domain Admins,cn=users,dc=ops,dc=local" | dsget group -members
dsquery * -attr operatingSystem operatingSystemServicePack -filter "(|(operatingSystem=*))"
dsquery user -name *carpenter*
dsquery user -name *carpenter* | dsget user -memberof
dsquery user -name *carpenter* | dsget user -dn -desc
dsquery group "CN=users,dc=ops,dc=local"
dsquery group "CN=Managers,CN=Users,DC=ops,DC=local" | dsget group -members
dsmod user "CN=Mike Carpenter,OU=Customer Service,DC=ops,DC=local" -desc "Production Manager"
dsmod group CN=Managers,CN=users,DC=ops,DC=local -addmbr "CN=Mike Carpenter,OU=Customer Service,dc=ops,dc=local"
dsmod group "CN=Managers,CN=Users,DC=ops,DC=local" -addmbr "CN=Your Name,CN=Users,DC=ops,DC=local"
dsadd user "CN=xxx xxx,CN=users,DC=ops,DC=local" -samid xxx -upn xxx@ops.local -fn "xxx" -ln "xxx" -display "xxx xxx" -pwd xxx -desc "xxxx" -disabled no
```

