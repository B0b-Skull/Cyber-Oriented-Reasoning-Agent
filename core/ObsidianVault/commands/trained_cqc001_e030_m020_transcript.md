---
title: "Trained Command Playbook: CQC001_E030_M020_transcript.pdf"
tags:
  - active_enum
  - credential_access
  - dsquery
  - enumeration
  - mdp
  - passive_enum
  - pdf
  - privilege_escalation
  - trained
source_file: CQC001_E030_M020_transcript.pdf
updated: 2026-10-24 00:57:35
---

# Trained Command Playbook: `CQC001_E030_M020_transcript.pdf`

- **Source Document:** `~/Projects/CORA/Training/CQC001_E030_M020_transcript.pdf`
- **CEGAR Verified Commands:** `38` (`0` malformed/unsafe snippets filtered)
- **MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`):** `38`
- **Discovered IPs/Subnets:** `None`
- **Discovered Interfaces:** `None`
- **Related Knowledge Note:** [[knowledge/trained_cqc001_e030_m020_transcript]]

## Distilled MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`)
| Pre-State ($s$) | Tactic ($\tau$) | Technique ($k$) | Tool ($u$) | Post-State ($s'$) | Verified Command ($c$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `ldifde` | `s_credentials_or_certs_acquired` | `LDIFDE.exe (LDAP Data Interchange Format (LDIF) Data Exchange tool)` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `csvde` | `s_passive_topology_mapped` | `CSVDE cannot be used to modify or delete objects.` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `dsadd` | `s_active_services_enumerated` | `DSADD COMPUTER: Adds a computer to the directory` |
| `s_passive_topology_mapped` | **`Active_Enum`** | Active Network, Cloud, Directory Service & Endpoint Probing | `dsget` | `s_active_services_enumerated` | `DSGET COMPUTER: Displays properties of computers in the directory` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `dsmod` | `s_interactive_tty_or_priv_escalated` | `DSMOD GROUP: Modifies an existing group in the directory` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `csvde` | `s_credentials_or_certs_acquired` | `CSVDE.exe (Comma Separated Value Data Export tool)` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `dsadd` | `s_active_services_enumerated` | `DSADD CONTACT: Adds a contact to the directory` |
| `s_passive_topology_mapped` | **`Active_Enum`** | Active Network, Cloud, Directory Service & Endpoint Probing | `dsget` | `s_active_services_enumerated` | `DSGET CONTACT: Displays properties of contacts in the directory` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `dsadd` | `s_credentials_or_certs_acquired` | `DSADD USER: Adds a user to the directory` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `dsadd` | `s_active_services_enumerated` | `DSADD GROUP: Adds a group to the directory` |
| `s_passive_topology_mapped` | **`Active_Enum`** | Active Network, Cloud, Directory Service & Endpoint Probing | `dsget` | `s_active_services_enumerated` | `DSGET SUBNET: Displays properties of subnets in the directory` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `dsmod` | `s_credentials_or_certs_acquired` | `DSMOD USER: Modifies an existing user in the directory` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `dsadd` | `s_active_services_enumerated` | `DSADD OU: Adds an organizational unit to the directory` |
| `s_passive_topology_mapped` | **`Active_Enum`** | Active Network, Cloud, Directory Service & Endpoint Probing | `dsget` | `s_active_services_enumerated` | `DSGET GROUP: Displays properties of groups in the directory` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `dsadd` | `s_active_services_enumerated` | `DSADD QUOTA: Adds a quota specification to a directory partition` |
| `s_passive_topology_mapped` | **`Active_Enum`** | Active Network, Cloud, Directory Service & Endpoint Probing | `dsget` | `s_active_services_enumerated` | `DSGET OU: Displays properties of organizational units in the directory` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `dsmod` | `s_active_services_enumerated` | `DSMOD COMPUTER: Modifies an existing computer in the directory` |
| `s_passive_topology_mapped` | **`Active_Enum`** | Active Network, Cloud, Directory Service & Endpoint Probing | `dsget` | `s_active_services_enumerated` | `DSGET SERVER: Displays properties of servers in the directory` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `dsmod` | `s_active_services_enumerated` | `DSMOD CONTACT: Modifies an existing contact in the directory` |
| `s_passive_topology_mapped` | **`Active_Enum`** | Active Network, Cloud, Directory Service & Endpoint Probing | `dsget` | `s_active_services_enumerated` | `DSGET SITE: Displays properties of sites in the directory` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `dsmod` | `s_active_services_enumerated` | `DSMOD OU: Modifies an existing organizational unit in the directory` |
| `s_passive_topology_mapped` | **`Active_Enum`** | Active Network, Cloud, Directory Service & Endpoint Probing | `dsget` | `s_active_services_enumerated` | `DSGET USER: Displays properties of users in the directory` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `dsmod` | `s_active_services_enumerated` | `DSMOD SERVER: Modifies an existing domain controller in the directory` |
| `s_passive_topology_mapped` | **`Active_Enum`** | Active Network, Cloud, Directory Service & Endpoint Probing | `dsget` | `s_active_services_enumerated` | `DSGET QUOTA: Displays properties of quotas in the directory` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `dsmod` | `s_active_services_enumerated` | `DSMOD QUOTA: Modifies an existing quota specification in the directory` |
| `s_passive_topology_mapped` | **`Active_Enum`** | Active Network, Cloud, Directory Service & Endpoint Probing | `dsget` | `s_active_services_enumerated` | `DSGET PARTITION: Displays properties of partitions in the directory` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `dsmod` | `s_active_services_enumerated` | `DSMOD PARTITION: Modifies attributes of one or more existing partitions in the directory` |
| `s_passive_topology_mapped` | **`Active_Enum`** | Active Network, Cloud, Directory Service & Endpoint Probing | `dsquery` | `s_active_services_enumerated` | `DSQUERY COMPUTER: Finds computers in the directory` |
| `s_passive_topology_mapped` | **`Active_Enum`** | Active Network, Cloud, Directory Service & Endpoint Probing | `dsquery` | `s_active_services_enumerated` | `DSQUERY CONTACT: Finds contacts in the directory` |
| `s_passive_topology_mapped` | **`Active_Enum`** | Active Network, Cloud, Directory Service & Endpoint Probing | `dsquery` | `s_active_services_enumerated` | `DSQUERY SUBNET: Finds subnets in the directory` |
| `s_passive_topology_mapped` | **`Active_Enum`** | Active Network, Cloud, Directory Service & Endpoint Probing | `dsquery` | `s_active_services_enumerated` | `DSQUERY GROUP: Finds groups in the directory` |
| `s_passive_topology_mapped` | **`Active_Enum`** | Active Network, Cloud, Directory Service & Endpoint Probing | `dsquery` | `s_active_services_enumerated` | `DSQUERY OU: Finds organizational units in the directory` |
| `s_passive_topology_mapped` | **`Active_Enum`** | Active Network, Cloud, Directory Service & Endpoint Probing | `dsquery` | `s_active_services_enumerated` | `DSQUERY SITE: Finds sites in the directory` |
| `s_passive_topology_mapped` | **`Active_Enum`** | Active Network, Cloud, Directory Service & Endpoint Probing | `dsquery` | `s_active_services_enumerated` | `DSQUERY SERVER: Finds domain controllers in the directory` |
| `s_passive_topology_mapped` | **`Active_Enum`** | Active Network, Cloud, Directory Service & Endpoint Probing | `dsquery` | `s_active_services_enumerated` | `DSQUERY USER: Finds users in the directory` |
| `s_passive_topology_mapped` | **`Active_Enum`** | Active Network, Cloud, Directory Service & Endpoint Probing | `dsquery` | `s_active_services_enumerated` | `DSQUERY QUOTA: Finds quota specifications in the directory` |
| `s_passive_topology_mapped` | **`Active_Enum`** | Active Network, Cloud, Directory Service & Endpoint Probing | `dsquery` | `s_active_services_enumerated` | `DSQUERY PARTITION: Finds partitions in the directory` |
| `s_passive_topology_mapped` | **`Active_Enum`** | Active Network, Cloud, Directory Service & Endpoint Probing | `dsquery` | `s_active_services_enumerated` | `DSQUERY *: Finds any object in the directory by using a generic LDAP query` |

## Verified Executable Commands (Grouped by Capability Layer)

### General_System (38 commands)
```bash
LDIFDE.exe (LDAP Data Interchange Format (LDIF) Data Exchange tool)
CSVDE.exe (Comma Separated Value Data Export tool)
CSVDE cannot be used to modify or delete objects.
DSADD COMPUTER: Adds a computer to the directory
DSADD CONTACT: Adds a contact to the directory
DSADD GROUP: Adds a group to the directory
DSADD OU: Adds an organizational unit to the directory
DSADD USER: Adds a user to the directory
DSADD QUOTA: Adds a quota specification to a directory partition
DSGET COMPUTER: Displays properties of computers in the directory
DSGET CONTACT: Displays properties of contacts in the directory
DSGET SUBNET: Displays properties of subnets in the directory
DSGET GROUP: Displays properties of groups in the directory
DSGET OU: Displays properties of organizational units in the directory
DSGET SERVER: Displays properties of servers in the directory
DSGET SITE: Displays properties of sites in the directory
DSGET USER: Displays properties of users in the directory
DSGET QUOTA: Displays properties of quotas in the directory
DSGET PARTITION: Displays properties of partitions in the directory
DSMOD COMPUTER: Modifies an existing computer in the directory
DSMOD CONTACT: Modifies an existing contact in the directory
DSMOD GROUP: Modifies an existing group in the directory
DSMOD OU: Modifies an existing organizational unit in the directory
DSMOD SERVER: Modifies an existing domain controller in the directory
DSMOD USER: Modifies an existing user in the directory
DSMOD QUOTA: Modifies an existing quota specification in the directory
DSMOD PARTITION: Modifies attributes of one or more existing partitions in the directory
DSQUERY COMPUTER: Finds computers in the directory
DSQUERY CONTACT: Finds contacts in the directory
DSQUERY SUBNET: Finds subnets in the directory
DSQUERY GROUP: Finds groups in the directory
DSQUERY OU: Finds organizational units in the directory
DSQUERY SITE: Finds sites in the directory
DSQUERY SERVER: Finds domain controllers in the directory
DSQUERY USER: Finds users in the directory
DSQUERY QUOTA: Finds quota specifications in the directory
DSQUERY PARTITION: Finds partitions in the directory
DSQUERY *: Finds any object in the directory by using a generic LDAP query
```

