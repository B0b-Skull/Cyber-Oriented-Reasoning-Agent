---
title: "Trained Knowledge & Topology: CQC001_E030_M030_Permissions_and_ACL_Commands.pdf"
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
doc_type: pdf
updated: 2026-10-24 00:57:38
---

# Trained Knowledge & Architecture: `CQC001_E030_M030_Permissions_and_ACL_Commands.pdf`

- **Source Path:** `~/Projects/CORA/Training/CQC001_E030_M030_Permissions_and_ACL_Commands.pdf` (`pdf`)
- **Extracted Technical Entities:** `cacls, http, https, icacls`
- **Extracted IPs / Subnets:** `None`
- **Extracted Interfaces:** `None`
- **Linked Command Playbook:** [[commands/trained_cqc001_e030_m030_permissions_and_acl_commands]] (`32` CEGAR-verified commands | `32` MDP transitions)

## Command & Tactic Coverage Summary
- **Total CEGAR-Verified Commands:** `32` (full executable list in [[commands/trained_cqc001_e030_m030_permissions_and_acl_commands]])
- **Tactic Distribution:** `Privilege_Escalation` (14), `Passive_Enum` (11), `Credential_Access` (4), `Enumeration` (3)
- **Top Extracted CLI Tools:** `net` (17), `icacls` (7), `runas` (5), `cacls` (2), `write-only` (1)

### Visual & Network Diagram Intelligence (`CQC001_E030_M030_Permissions_and_ACL_Commands.pdf#page6`)
- **Spatially Grouped Diagram Nodes (Box/Component Clusters):**
  1. `[PERMISSIONS AND ACLS]`
  2. `[6]`

### Visual & Network Diagram Intelligence (`CQC001_E030_M030_Permissions_and_ACL_Commands.pdf#page8`)
- **Spatially Grouped Diagram Nodes (Box/Component Clusters):**
  1. `[PERMISSIONS AND ACLS]`
  2. `[8]`

## LLM Distilled Operational Summary
### Key Operational Techniques & Decision Workflows

*   **User Account Lifecycle Management:**
    *   **Creation/Modification:** Use `net user` with `/add` to create accounts or omit `/delete` to modify existing ones. Always verify password policy compliance (min length, complexity) before assignment.
    *   **Deactivation:** Set `/active:no` to disable access without deleting the account, preserving historical data.
    *   **Expiration:** Apply `/expires:MM/DD/YY` to enforce time-limited access; use `never` for permanent accounts.
    *   **Domain Context:** Append `/domain` to target the Primary Domain Controller (PDC) instead of the local machine, ensuring changes propagate to the domain-wide user database.
*   **Group Membership Administration:**
    *   **Local Group Management:** Use `net localgroup` to add (`/add`) or remove (`/delete`) users from local security groups.
    *   **Workflow:** Establish user accounts first, then modify group membership. Use `/comment` to document group purpose (max 48 chars).

### Critical Command Patterns and Required Flags

*   **`net user` Syntax:**
    ```cmd
    net user [username] [password | *] [options] [/domain]
    ```
    *   **Key Flags:** `/add`, `/delete`, `/active:{yes|no}`, `/expires:{date|never}`, `/domain`, `/fullname:"text"`, `/homedir:pathname`.
    *   **Password Handling:** Use `*` to prompt for a password interactively; omit to use the provided string.
*   **`net localgroup` Syntax:**
    ```cmd
    net localgroup [GroupName] [/comment:"text"] [/domain]
    net localgroup [GroupName] {/add | /delete} [/domain]
    ```
    *   **Key Flags:** `/add`, `/delete`, `/domain`, `/comment:"text"`.

### Network Topology & Service Relationships

*   **Domain Architecture:** Operations involving `/domain` target the **Primary Domain Controller (PDC)**. This implies a client-server model where user databases are centralized on the PDC for domain members, while local operations affect only the specific server's local security database.
*   **Logon Constraints:** The `/workstations` parameter defines a whitelist of up to eight specific computer names (or `*` for any) from which a user may authenticate, effectively segmenting access based on device identity.
*   **Profile & Scripting:** The `/profilepath` and `/scriptpath` flags link user accounts to specific file system paths and logon scripts, establishing the relationship between identity and environment provisioning.

## Document Structure & Key Topics
- Visual & Network Diagram Intelligence (`CQC001_E030_M030_Permissions_and_ACL_Commands.pdf#page6`)
- Visual & Network Diagram Intelligence (`CQC001_E030_M030_Permissions_and_ACL_Commands.pdf#page8`)

