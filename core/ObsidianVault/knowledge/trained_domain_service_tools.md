---
title: "Trained Knowledge & Topology: Domain_Service_Tools.pdf"
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
doc_type: pdf
updated: 2026-10-24 00:58:21
---

# Trained Knowledge & Architecture: `Domain_Service_Tools.pdf`

- **Source Path:** `~/Projects/CORA/Training/Domain_Service_Tools.pdf` (`pdf`)
- **Extracted Technical Entities:** `dsquery`
- **Extracted IPs / Subnets:** `None`
- **Extracted Interfaces:** `None`
- **Linked Command Playbook:** [[commands/trained_domain_service_tools]] (`35` CEGAR-verified commands | `35` MDP transitions)

## Command & Tactic Coverage Summary
- **Total CEGAR-Verified Commands:** `35` (full executable list in [[commands/trained_domain_service_tools]])
- **Tactic Distribution:** `Active_Enum` (21), `Enumeration` (11), `Credential_Access` (2), `Privilege_Escalation` (1)
- **Top Extracted CLI Tools:** `dsquery` (11), `dsget` (10), `dsmod` (8), `dsadd` (6)

## LLM Distilled Operational Summary
### Key Operational Techniques & Decision Workflows

*   **Object Lifecycle Management**: Follow a strict Create-Modify-Query-Move/Delete workflow using the corresponding tool prefixes (`DSADD`, `DSMOD`, `DSQUERY`, `DSMOVE`, `DSRM`).
*   **Targeted Property Inspection**: Use `DSGET` to verify specific attributes (e.g., `DSGET USER` for account status, `DSGET SITE` for topology) before performing modifications or moves.
*   **Generic LDAP Querying**: Utilize `DSQUERY *` for broad directory searches when specific object type filters are unavailable or insufficient.
*   **Partition & Quota Management**: Treat Directory Partitions and Quota specifications as distinct object types requiring dedicated tools (`DSMOD PARTITION`, `DSADD QUOTA`) separate from standard user/computer objects.

### Critical Command Patterns and Required Flags

*   **Add Objects**: `DSADD <TYPE>` (e.g., `DSADD USER`, `DSADD OU`). Requires object name, parent container, and specific attribute flags (e.g., `/Password` for users).
*   **Modify Objects**: `DSMOD <TYPE> /<Attribute>=<Value>`. Common flags include `/Password`, `/Name`, `/OU`, and `/Server`.
*   **Query Objects**: `DSQUERY <TYPE> /<Filter>`. Supports LDAP-style filters (e.g., `/SamAccountName:admin`, `/OU:Default-First-Organizational Unit`).
*   **Move/Rename**: `DSMOVE <TYPE> /TargetOU` or `/NewName`.
*   **Remove Objects**: `DSRM <TYPE> /<ObjectDN>` or `/<ObjectName>`.

### Network Topology & Service Relationships

*   **Domain Controller (DC) Identification**: `DSQUERY SERVER` and `DSMOD SERVER` interact directly with Domain Controllers. `DSGET SERVER` retrieves DC properties like site membership and replication status.
*   **Site & Subnet Mapping**: `DSGET SITE` and `DSGET SUBNET` define the physical and logical network topology, linking IP subnets to Active Directory sites for replication and client location awareness.
*   **Partition Hierarchy**: `DSGET PARTITION` and `DSMOD PARTITION` manage the schema and configuration partitions, which dictate how data is stored and replicated across the forest.
*   **Service Dependencies**:
    *   **Quotas**: Managed via `DSADD/DSMOD/DSQUERY QUOTA`, these define storage limits for specific directory partitions.
    *   **Organizational Units (OU)**: Managed via `DSADD/DSMOD/DSQUERY OU`, OUs serve as containers for users, groups, and computers to facilitate Group Policy application and delegation.

