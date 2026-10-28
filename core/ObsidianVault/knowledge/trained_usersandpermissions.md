---
title: "Trained Knowledge & Topology: UsersAndPermissions.txt"
tags:
  - credential_access
  - enumeration
  - john
  - mdp
  - passive_enum
  - privilege_escalation
  - text
  - trained
source_file: UsersAndPermissions.txt
doc_type: text
updated: 2026-10-24 01:01:08
---

# Trained Knowledge & Architecture: `UsersAndPermissions.txt`

- **Source Path:** `~/Projects/CORA/Training/UsersAndPermissions.txt` (`text`)
- **Extracted Technical Entities:** `john`
- **Extracted IPs / Subnets:** `None`
- **Extracted Interfaces:** `None`
- **Linked Command Playbook:** [[commands/trained_usersandpermissions]] (`39` CEGAR-verified commands | `39` MDP transitions)

## Command & Tactic Coverage Summary
- **Total CEGAR-Verified Commands:** `39` (full executable list in [[commands/trained_usersandpermissions]])
- **Tactic Distribution:** `Privilege_Escalation` (31), `Enumeration` (4), `Passive_Enum` (3), `Credential_Access` (1)
- **Top Extracted CLI Tools:** `chmod` (20), `chown` (7), `cp` (4), `chgrp` (3), `ls` (2), `-u` (1), `find` (1), `mkdir` (1)

## LLM Distilled Operational Summary
### Key Operational Techniques & Decision Workflows

*   **User & Group Lifecycle Management**:
    *   **Creation**: Use `useradd` with flags `-g` (primary group), `-s` (shell), and `-d` (home directory).
    *   **Password Setup**: Run `passwd <username>` to set or modify passwords.
    *   **Group Administration**: Use `gpasswd -A <user> <group>` to add administrators; `gpasswd <group>` to change group passwords.
    *   **Deactivation**: Change default shell to `/bin/false` (graceful denial) or `/bin/nologin` (login message) via `usermod`.
    *   **Deletion**: Use `userdel -r <username>` to remove the user and their home directory.
    *   **Batch Operations**: Utilize `for` loops with `useradd` and `passwd` to create multiple users efficiently.

*   **Ownership & Permission Modification**:
    *   **Ownership**: Change owner with `chown <user>:<group> <file>` or `chown <user> <file>`; change group with `chgrp`.
    *   **Recursive Changes**: Apply `-R` flag to `chown` and `chgrp` for subdirectories.
    *   **Absolute Mode (`chmod`)**: Define permissions numerically (e.g., `650`, `750`). Add extra digits for SUID/SGID/Sticky bits (e.g., `6640`).
    *   **Symbolic Mode (`chmod`)**: Use `u`, `g`, `o`, `a` prefixes with `+`, `-`, or `=` operators to add, remove, or set exact permissions.
    *   **Default Permissions**: Check `umask` to understand default file creation masks (e.g., `0022`).

*   **File & Directory Creation**:
    *   Use `touch` for creation; apply `-c` (conditional), `-a` (update timestamp), or `-t` (specific date/time) flags as needed.

### Critical Command Patterns & Required Flags

*   **`chown`**: `-R` (recursive), `user:group` syntax.
*   **`chmod`**: `u+rw,g=x,go-wx` (symbolic), `653` (absolute), `a=r` (all read).
*   **`useradd`**: `-g`, `-s`, `-d`.
*   **`usermod`**: `-s` (shell change).
*   **`userdel`**: `-r` (remove home).
*   **`gpasswd`**: `-A` (add admin).
*   **`touch`**: `-c` (conditional), `-a` (update time), `-t` (timestamp), `-r` (copy time).

### Network Topology & Service Relationships

*   **System Files**:
    *   `/etc/passwd`: Stores user account details (e.g., `fred:x:501:501:Fred Flintstone:/home/freddo:/bin/bash`).
    *   `/etc/group`: Defines group memberships (e.g., `staff:x:501`,

