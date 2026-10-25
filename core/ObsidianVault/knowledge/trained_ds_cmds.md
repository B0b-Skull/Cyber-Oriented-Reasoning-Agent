---
title: "Trained Knowledge & Topology: DS CMDs.txt"
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
doc_type: text
updated: 2026-10-25 00:58:21
---

# Trained Knowledge & Architecture: `DS CMDs.txt`

- **Source Path:** `~/Projects/CORA/Training/DS CMDs.txt` (`text`)
- **Extracted Technical Entities:** `dsquery, http`
- **Extracted IPs / Subnets:** `None`
- **Extracted Interfaces:** `None`
- **Linked Command Playbook:** [[commands/trained_ds_cmds]] (`27` CEGAR-verified commands | `27` MDP transitions)

## Command & Tactic Coverage Summary
- **Total CEGAR-Verified Commands:** `27` (full executable list in [[commands/trained_ds_cmds]])
- **Tactic Distribution:** `Active_Enum` (20), `Credential_Access` (5), `Privilege_Escalation` (2)
- **Top Extracted CLI Tools:** `dsquery` (19), `dsmod` (4), `dsadd` (3), `dsget` (1)

## LLM Distilled Operational Summary
### Key Operational Techniques & Decision Workflows
*   **User Creation Workflow**: Use `dsadd user` with explicit `-samid` (e.g., `prohenry`) and `-pwd` flags. Always specify `-disabled yes` for temporary accounts or `-pwdneverexpires no` to enforce password rotation policies.
*   **Attribute Population**: Populate critical attributes like `-email`, `-title`, and `-hometel` directly during creation. Use `-memberof` to assign users to groups (e.g., `Managers`) immediately.
*   **Group Management**: Create groups in the `Users` container. Modify descriptions using `dsmod group -desc`. Add members dynamically using `dsmod group -addmbr` with full Distinguished Names (DN).
*   **Query & Verification**: Chain commands to extract specific attributes (e.g., `dsquery user -name *Phillips* | dsget user -samid`). Use `dsquery` for filtering by name, container, or attributes, and `dsget` for retrieving detailed object properties.

### Critical Command Patterns & Required Flags
*   **Creation**: `dsadd user <DN> [-samid <ID>] [-pwd <Pass>] [-disabled <yes/no>] [-pwdneverexpires <yes/no>]`
*   **Modification**: `dsmod user <DN> -desc "<Text>"` | `dsmod group <DN> -addmbr "<DN>"`
*   **Querying**: `dsquery user -name "*<keyword>*"` | `dsquery computer -name "*<keyword>*"`
*   **Chaining**: Pipe output from `dsquery` to `dsget` (e.g., `| dsget user -memberof`) to retrieve nested attributes.

### Network Topology & Relationships
*   **Domain Structure**: Objects reside in specific OUs (e.g., `OU=Customer Service,DC=ops,DC=local`) or containers (`CN=Users`).
*   **Naming Conventions**: SAMIDs follow the pattern `FirstInitialMiddleInitialLastName` (e.g., `prohenry`). UPNs follow `<SAMID>@<Domain>` (e.g., `prohenry@ops.local`).
*   **Service Relationships**: Users are linked to groups (`Managers`, `Domain Admins`) for access control. Computer objects are queried separately from user objects.
*   **Reference Resources**: Utilize external documentation (e.g., `computerperformance.co.uk`) for advanced query filters like operating system versions.

