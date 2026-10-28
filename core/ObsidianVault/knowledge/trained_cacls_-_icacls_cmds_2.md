---
title: "Trained Knowledge & Topology: Cacls - Icacls CMDs 2.txt"
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
doc_type: text
updated: 2026-10-24 00:57:01
---

# Trained Knowledge & Architecture: `Cacls - Icacls CMDs 2.txt`

- **Source Path:** `~/Projects/CORA/Training/Cacls - Icacls CMDs 2.txt` (`text`)
- **Extracted Technical Entities:** `cacls, icacls`
- **Extracted IPs / Subnets:** `None`
- **Extracted Interfaces:** `None`
- **Linked Command Playbook:** [[commands/trained_cacls_-_icacls_cmds_2]] (`40` CEGAR-verified commands | `40` MDP transitions)

## Command & Tactic Coverage Summary
- **Total CEGAR-Verified Commands:** `40` (full executable list in [[commands/trained_cacls_-_icacls_cmds_2]])
- **Tactic Distribution:** `Privilege_Escalation` (23), `Credential_Access` (12), `Passive_Enum` (3), `Enumeration` (2)
- **Top Extracted CLI Tools:** `icacls` (14), `net` (13), `cacls` (8), `echo` (2), `md` (2), `mkdir` (1)

## LLM Distilled Operational Summary
### Key Operational Techniques & Decision Workflows

*   **User & Group Lifecycle Management**: Create local users (`net user`) and add them to specific security groups (e.g., `Power Users`, `Ducks`) using `net localgroup`. Use `/add` for inclusion and `/delete` for removal.
*   **Directory Structure Initialization**: Establish parent directories (e.g., `C:\The Stooges`) and subdirectories for individual users (`mkdir`, `md`) before applying permissions.
*   **Inheritance Strategy Selection**:
    *   **Full Inheritance**: Use `/t` (traverse) with `icacls` to apply permissions recursively to all subfolders/files.
    *   **Selective Inheritance**: Use `/inheritance:r` (remove) on the parent folder to break inheritance, then explicitly grant permissions to specific users on child objects.
    *   **Explicit vs. Inherited**: Apply `/inheritance:d` (deny) to override inherited permissions for specific users or groups.
*   **Permission Assignment Patterns**:
    *   **Full Control (`F`)**: Typically assigned to the user's own folder (`/grant Username:F`).
    *   **Remove Default Groups**: Explicitly remove `Users`, `Authenticated Users`, or `NT Authority\Authenticated Users` from specific folders to restrict access.
    *   **Recursive Application**: Combine `/t` (traverse) with `/inheritance:e` (explicit) to ensure permissions apply to all descendants while maintaining explicit control.

### Critical Command Patterns and Required Flags

*   **`cacls` Syntax**: `cacls <Path> /E /P <User>:<Perm>`
    *   `/E`: Edit (add) permissions.
    *   `/P`: Set specific permissions (e.g., `User:F`).
    *   `/G`: Grant access (similar to `/P` but often used with groups).
    *   `/R`: Remove access.
    *   `/T`: Traverse subdirectories (recursive).
*   **`icacls` Syntax**: `icacls <Path> /grant <User>:<Perm> /inheritance:<Action>`
    *   `/grant`: Add a specific user/group with defined permissions.
    *   `/remove`: Remove specific user/group access.
    *   `/inheritance:r`: Remove inherited permissions from parent.
    *   `/inheritance:d`: Deny inherited permissions.
    *   `/inheritance:e`: Explicitly set permissions (often used with `/t`).
    *   `/t`: Traverse subdirectories.
*   **`net share` Syntax**: `net share <Name>=<Path> /GRANT:<User>,<Level>`
    *   Defines network shares and assigns read/change/full access levels.

### Network Topology & Service Relationships

*   **Local vs. Domain Context**: Commands reference both local groups (`Power Users`, `Users`) and domain groups (`domain admins`), indicating a hybrid environment where local security policies interact with domain identity.
*   **Share Mapping**: The `net share` command maps logical share names to physical drive paths, creating a network-accessible entry point for defined user groups.
*   **Service Relationships**: Permissions are tightly scoped to specific user folders (e.g., `C:\The Stooges\Larry`), suggesting

