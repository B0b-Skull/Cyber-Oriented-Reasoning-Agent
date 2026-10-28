---
title: "Trained Knowledge & Topology: Netsh FW CMDs.txt"
tags:
  - defense_evasion_firewall
  - mdp
  - netsh
  - text
  - trained
source_file: Netsh FW CMDs.txt
doc_type: text
updated: 2026-10-24 00:59:23
---

# Trained Knowledge & Architecture: `Netsh FW CMDs.txt`

- **Source Path:** `~/Projects/CORA/Training/Netsh FW CMDs.txt` (`text`)
- **Extracted Technical Entities:** `netsh`
- **Extracted IPs / Subnets:** `172.24.11.14, 212.54.40.25`
- **Extracted Interfaces:** `None`
- **Linked Command Playbook:** [[commands/trained_netsh_fw_cmds]] (`27` CEGAR-verified commands | `27` MDP transitions)

## Command & Tactic Coverage Summary
- **Total CEGAR-Verified Commands:** `27` (full executable list in [[commands/trained_netsh_fw_cmds]])
- **Tactic Distribution:** `Defense_Evasion_Firewall` (27)
- **Top Extracted CLI Tools:** `netsh` (27)

## LLM Distilled Operational Summary
### Key Operational Techniques & Decision Workflows

*   **Profile Management**: Determine the active profile using `show currentprofile`. Toggle firewall state globally (`set allprofiles`) or per-profile (`set currentprofile`) to `on` or `off`.
*   **Rule Inspection**: List all rules (`show rule name=all`) or filter by specific profile (e.g., `profile=private`). Use `verbose` for detailed inspection. Export rules to `.wfw` files for backup before bulk changes.
*   **Group Control**: Enable/disable predefined groups (e.g., "File and Printer Sharing") via `set rule group`. Note that group settings can be overridden by specific rule names.
*   **Custom Rule Lifecycle**:
    1.  **Add**: Define name, direction (`dir=in/out`), protocol, port, remote IP (optional), and action (`allow/block`).
    2.  **Modify**: Use `set rule name` to toggle specific rules on/off.
    3.  **Delete**: Remove rules using `delete rule name`.
*   **Service Integration**: Bind rules to specific services (e.g., `service=ftpsvc`) or executable paths (e.g., `firefox.exe`).

### Critical Command Patterns & Required Flags

*   **Syntax Structure**: `netsh advfirewall firewall [action] [parameters]`
*   **Action Verbs**: `add rule`, `set rule`, `delete rule`, `show rule`.
*   **Essential Parameters**:
    *   `name="RuleName"`: Unique identifier.
    *   `dir=in|out`: Traffic direction.
    *   `protocol=tcp|udp|any`.
    *   `localport=XXXX` or `service=svcname`.
    *   `remoteip=IP_ADDRESS` (for specific allow-listing).
    *   `profile=private|domain|public`.
    *   `action=allow|block`.
    *   `enable=yes|no`: Runtime toggle.

### Network Topology & Service Relationships

*   **Profile Context**: Rules apply differently based on the active profile (`private`, `domain`, `public`). A rule added without a profile flag applies only to the current profile.
*   **Stateful FTP**: Disabling `StatefulFTP` (`set global StatefulFTP disable`) allows non-standard FTP ports to be managed individually via `localport`.
*   **Specific Allow-List Example**:
    *   Target: `172.24.11.14` on TCP `31337` (Local) <-> `6666` (Remote).
    *   Context: Private profile only.
*   **Standard Services**:
    *   **RDP**: Typically mapped to dynamic ports (e.g., `31669`) or standard `3389`.
    *   **HTTP/HTTPS**: Ports `80` and `443` often require explicit outbound rules if not covered by default groups.
*   **Backup Path**: Rules are stored in `.wfw` files, supporting version control via paths like `C:\FW-Before-Changes.wfw`.

