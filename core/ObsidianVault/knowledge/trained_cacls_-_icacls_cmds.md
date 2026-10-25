---
title: "Trained Knowledge & Topology: Cacls - Icacls CMDs.txt"
tags:
  - cacls
  - credential_access
  - icacls
  - mdp
  - privilege_escalation
  - text
  - trained
source_file: Cacls - Icacls CMDs.txt
doc_type: text
updated: 2026-10-25 00:57:01
---

# Trained Knowledge & Architecture: `Cacls - Icacls CMDs.txt`

- **Source Path:** `~/Projects/CORA/Training/Cacls - Icacls CMDs.txt` (`text`)
- **Extracted Technical Entities:** `cacls, icacls`
- **Extracted IPs / Subnets:** `None`
- **Extracted Interfaces:** `None`
- **Linked Command Playbook:** [[commands/trained_cacls_-_icacls_cmds]] (`21` CEGAR-verified commands | `21` MDP transitions)

## Command & Tactic Coverage Summary
- **Total CEGAR-Verified Commands:** `21` (full executable list in [[commands/trained_cacls_-_icacls_cmds]])
- **Tactic Distribution:** `Privilege_Escalation` (12), `Credential_Access` (9)
- **Top Extracted CLI Tools:** `icacls` (9), `net` (8), `cacls` (3), `echo` (1)

## LLM Distilled Operational Summary
### Operational Techniques & Decision Workflows
*   **Isolate Scope**: When assigning permissions, focus exclusively on the specific users and groups defined in the current task; ignore existing built-in Windows accounts or groups unless explicitly required.
*   **User Creation**: Create new local users using `net user` with a specified password and `/add` flag.
*   **Group Management**: Add users to local groups using `net localgroup` with the `/add` flag.
*   **Permission Assignment**: Use `icacls` (preferred over legacy `cacls`) to grant specific access rights (e.g., Full Control `:F`) to users or groups.
*   **Inheritance Control**: Modify inheritance settings using flags like `(OI)(R)` for object and inherited, or `/inheritance:D` to disable inheritance.
*   **Permission Removal**: Explicitly remove permissions from specific users or groups using the `/remove` flag.
*   **Verification**: Validate final ACL configurations by viewing all permissions recursively with `icacls <path> /t`.

### Critical Command Patterns & Required Flags
*   **User Creation**: `net user <Username> <Password> /add`
*   **Group Membership**: `net localgroup <GroupName> <User1> <User2> /add`
*   **Grant Permissions**: `icacls <Path> /grant <Principal>:<Rights>` (e.g., `Orange:F`)
*   **Modify Inheritance**: `icacls <Path> /inheritance:D` (Disable) or `/grant <Principal>:(OI)(R)` (Enable/Modify).
*   **Remove Permissions**: `icacls <Path> /remove <Principal>`
*   **View Permissions**: `icacls <Path> /t` (Recursively view all).

### Network Topology & Service Relationships
*   **File System Scope**: Operations are confined to the `C:\Ledge` directory structure, specifically targeting subdirectories like `Old` and `Bold`.
*   **Logical Grouping**: Users (`Orange`, `Blue`, `Banana`) are logically grouped into `Fruit` and `Color` groups to manage access control lists (ACLs) hierarchically.
*   **Service Context**: The workflow assumes a local Windows environment where `net` commands manage local security principals and `icacls` manages local file system ACLs.

## Extracted Operational Steps & Workflows
- 1. Add users to appropriate groups and assign appropriate permissions to the designated directories/files. For this question only concern yourself with the users/groups you create. For instance, if the directions say only a specific user should have access to a specific file/directory, ignore existing/built-in users/groups.

