---
title: "Trained Command Playbook: Domain_Service_Tools.pdf"
tags:
  - active_enum
  - credential_access
  - dsquery
  - enumeration
  - mdp
  - pdf
  - privilege_escalation
  - trained
source_file: Domain_Service_Tools.pdf
updated: 2026-10-24 00:58:21
---

# Trained Command Playbook: `Domain_Service_Tools.pdf`

- **Source Document:** `~/Projects/CORA/Training/Domain_Service_Tools.pdf`
- **CEGAR Verified Commands:** `35` (`0` malformed/unsafe snippets filtered)
- **MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`):** `35`
- **Discovered IPs/Subnets:** `None`
- **Discovered Interfaces:** `None`
- **Related Knowledge Note:** [[knowledge/trained_domain_service_tools]]

## Distilled MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`)
| Pre-State ($s$) | Tactic ($\tau$) | Technique ($k$) | Tool ($u$) | Post-State ($s'$) | Verified Command ($c$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `dsadd` | `s_active_services_enumerated` | `DSADD COMPUTER` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `dsadd` | `s_credentials_or_certs_acquired` | `DSADD USER` |
| `s_passive_topology_mapped` | **`Active_Enum`** | Active Network, Cloud, Directory Service & Endpoint Probing | `dsget` | `s_active_services_enumerated` | `DSGET COMPUTER` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `dsmod` | `s_interactive_tty_or_priv_escalated` | `DSMOD GROUP` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `dsadd` | `s_active_services_enumerated` | `DSADD CONTACT` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `dsmod` | `s_credentials_or_certs_acquired` | `DSMOD USER` |
| `s_passive_topology_mapped` | **`Active_Enum`** | Active Network, Cloud, Directory Service & Endpoint Probing | `dsget` | `s_active_services_enumerated` | `DSGET CONTACT` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `dsadd` | `s_active_services_enumerated` | `DSADD GROUP` |
| `s_passive_topology_mapped` | **`Active_Enum`** | Active Network, Cloud, Directory Service & Endpoint Probing | `dsget` | `s_active_services_enumerated` | `DSGET SUBNET` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `dsadd` | `s_active_services_enumerated` | `DSADD OU` |
| `s_passive_topology_mapped` | **`Active_Enum`** | Active Network, Cloud, Directory Service & Endpoint Probing | `dsget` | `s_active_services_enumerated` | `DSGET GROUP` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `dsadd` | `s_active_services_enumerated` | `DSADD QUOTA` |
| `s_passive_topology_mapped` | **`Active_Enum`** | Active Network, Cloud, Directory Service & Endpoint Probing | `dsget` | `s_active_services_enumerated` | `DSGET OU` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `dsmod` | `s_active_services_enumerated` | `DSMOD COMPUTER` |
| `s_passive_topology_mapped` | **`Active_Enum`** | Active Network, Cloud, Directory Service & Endpoint Probing | `dsget` | `s_active_services_enumerated` | `DSGET SERVER` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `dsmod` | `s_active_services_enumerated` | `DSMOD CONTACT` |
| `s_passive_topology_mapped` | **`Active_Enum`** | Active Network, Cloud, Directory Service & Endpoint Probing | `dsget` | `s_active_services_enumerated` | `DSGET SITE` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `dsmod` | `s_active_services_enumerated` | `DSMOD OU` |
| `s_passive_topology_mapped` | **`Active_Enum`** | Active Network, Cloud, Directory Service & Endpoint Probing | `dsget` | `s_active_services_enumerated` | `DSGET USER` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `dsmod` | `s_active_services_enumerated` | `DSMOD SERVER` |
| `s_passive_topology_mapped` | **`Active_Enum`** | Active Network, Cloud, Directory Service & Endpoint Probing | `dsget` | `s_active_services_enumerated` | `DSGET QUOTA` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `dsmod` | `s_active_services_enumerated` | `DSMOD QUOTA` |
| `s_passive_topology_mapped` | **`Active_Enum`** | Active Network, Cloud, Directory Service & Endpoint Probing | `dsget` | `s_active_services_enumerated` | `DSGET PARTITION` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `dsmod` | `s_active_services_enumerated` | `DSMOD PARTITION` |
| `s_passive_topology_mapped` | **`Active_Enum`** | Active Network, Cloud, Directory Service & Endpoint Probing | `dsquery` | `s_active_services_enumerated` | `DSQUERY COMPUTER` |
| `s_passive_topology_mapped` | **`Active_Enum`** | Active Network, Cloud, Directory Service & Endpoint Probing | `dsquery` | `s_active_services_enumerated` | `DSQUERY CONTACT` |
| `s_passive_topology_mapped` | **`Active_Enum`** | Active Network, Cloud, Directory Service & Endpoint Probing | `dsquery` | `s_active_services_enumerated` | `DSQUERY SUBNET` |
| `s_passive_topology_mapped` | **`Active_Enum`** | Active Network, Cloud, Directory Service & Endpoint Probing | `dsquery` | `s_active_services_enumerated` | `DSQUERY GROUP` |
| `s_passive_topology_mapped` | **`Active_Enum`** | Active Network, Cloud, Directory Service & Endpoint Probing | `dsquery` | `s_active_services_enumerated` | `DSQUERY OU` |
| `s_passive_topology_mapped` | **`Active_Enum`** | Active Network, Cloud, Directory Service & Endpoint Probing | `dsquery` | `s_active_services_enumerated` | `DSQUERY SITE` |
| `s_passive_topology_mapped` | **`Active_Enum`** | Active Network, Cloud, Directory Service & Endpoint Probing | `dsquery` | `s_active_services_enumerated` | `DSQUERY SERVER` |
| `s_passive_topology_mapped` | **`Active_Enum`** | Active Network, Cloud, Directory Service & Endpoint Probing | `dsquery` | `s_active_services_enumerated` | `DSQUERY USER` |
| `s_passive_topology_mapped` | **`Active_Enum`** | Active Network, Cloud, Directory Service & Endpoint Probing | `dsquery` | `s_active_services_enumerated` | `DSQUERY QUOTA` |
| `s_passive_topology_mapped` | **`Active_Enum`** | Active Network, Cloud, Directory Service & Endpoint Probing | `dsquery` | `s_active_services_enumerated` | `DSQUERY PARTITION` |
| `s_passive_topology_mapped` | **`Active_Enum`** | Active Network, Cloud, Directory Service & Endpoint Probing | `dsquery` | `s_active_services_enumerated` | `DSQUERY *` |

## Verified Executable Commands (Grouped by Capability Layer)

### General_System (35 commands)
```bash
DSADD COMPUTER
DSADD CONTACT
DSADD GROUP
DSADD OU
DSADD USER
DSADD QUOTA
DSGET COMPUTER
DSGET CONTACT
DSGET SUBNET
DSGET GROUP
DSGET OU
DSGET SERVER
DSGET SITE
DSGET USER
DSGET QUOTA
DSGET PARTITION
DSMOD COMPUTER
DSMOD CONTACT
DSMOD GROUP
DSMOD OU
DSMOD SERVER
DSMOD USER
DSMOD QUOTA
DSMOD PARTITION
DSQUERY COMPUTER
DSQUERY CONTACT
DSQUERY SUBNET
DSQUERY GROUP
DSQUERY OU
DSQUERY SITE
DSQUERY SERVER
DSQUERY USER
DSQUERY QUOTA
DSQUERY PARTITION
DSQUERY *
```

