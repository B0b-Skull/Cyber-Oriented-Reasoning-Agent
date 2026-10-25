---
title: "Trained Knowledge & Topology: AuditPol CMDs.txt"
tags:
  - auditpol
  - credential_access
  - defense_evasion_firewall
  - kerberos
  - mdp
  - passive_enum
  - text
  - trained
  - wevtutil
  - wmic
source_file: AuditPol CMDs.txt
doc_type: text
updated: 2026-10-25 00:56:13
---

# Trained Knowledge & Architecture: `AuditPol CMDs.txt`

- **Source Path:** `~/Projects/CORA/Training/AuditPol CMDs.txt` (`text`)
- **Extracted Technical Entities:** `auditpol, kerberos, wevtutil, wmic`
- **Extracted IPs / Subnets:** `None`
- **Extracted Interfaces:** `None`
- **Linked Command Playbook:** [[commands/trained_auditpol_cmds]] (`30` CEGAR-verified commands | `30` MDP transitions)

## Command & Tactic Coverage Summary
- **Total CEGAR-Verified Commands:** `30` (full executable list in [[commands/trained_auditpol_cmds]])
- **Tactic Distribution:** `Defense_Evasion_Firewall` (23), `Passive_Enum` (6), `Credential_Access` (1)
- **Top Extracted CLI Tools:** `auditpol` (23), `psloglist` (4), `wmic` (2), `wevtutil` (1)

## LLM Distilled Operational Summary
### Key Operational Techniques & Decision Workflows

*   **Log Retrieval & Filtering**: Use `psloglist` with specific flags (`-s`, `-t`, `-n`) to retrieve and format the last N security log entries. Combine with `findstr` to filter for specific keywords like "SID" or "Administrators" to identify privilege escalation events.
*   **Policy Verification**: Use `auditpol /list` commands to verify current audit configurations across categories, subcategories, and specific user accounts before or after changes.
*   **Policy Enforcement**: Apply `auditpol /set` commands to enable or disable auditing for specific subcategories (e.g., "User Account Management", "Sensitive Privilege Use") with defined success/failure triggers.
*   **Event Log Inspection**: Query the Windows Event Log using `wevtutil qe` to retrieve recent text-formatted logs from the System category for immediate analysis.
*   **User-to-SID Mapping**: Utilize `wmic useraccount` queries to retrieve Security Identifiers (SIDs) associated with specific usernames across different OS versions (Windows 7/XP).

### Critical Command Patterns and Required Flags

| Command Pattern | Purpose | Key Flags/Parameters |
| :--- | :--- | :--- |
| `psloglist -n <count>` | Retrieve last N log entries. | `-n`: Limit count (e.g., `-n 10`). |
| `psloglist -s -t "\t" -n <count> Security` | Format and filter Security logs. | `-s`: Show SID; `-t "\t"`: Tab delimiter; `-n`: Count. |
| `auditpol /list /category` | List audit categories. | `/category`: Scope to categories. |
| `auditpol /set /subcategory:"Name" /success:enable` | Enable auditing for a subcategory. | `/subcategory`: Target name; `/success:enable` or `/failure:enable`. |
| `wevtutil qe System /c:10 /f:text` | Query Event Log. | `/c`: Count; `/f:text`: Text format. |
| `wmic useraccount where name='X' get sid` | Get User SID. | `where name='X'`: Filter by username; `get sid`: Output SID. |

### Network Topology & Service Relationships

*   **Security Subcategory Dependencies**: Auditing is granularly configured per subcategory within the "Security" category. Key relationships include:
    *   **User Account Management**: Tracks creation, deletion, and privilege changes (e.g., adding users to Administrators).
    *   **Sensitive Privilege Use**: Monitors usage of high-privilege tokens.
    *   **Kerberos Services**: Includes "Service Ticket Operations" and "Authentication Service" for identity verification tracking.
    *   **File & Network**: Covers "File Share" and "Network Policy Server" for access control monitoring.
*   **OS-Specific Behavior**: Command syntax for SID retrieval varies slightly between Windows 7 (`get sid` required) and Windows XP (implicit in `get` output).

