---
title: "Trained Knowledge & Topology: Registry CMDs.txt"
tags:
  - defense_evasion_firewall
  - enumeration
  - mdp
  - out-of-band_access
  - text
  - trained
source_file: Registry CMDs.txt
doc_type: text
updated: 2026-10-24 01:00:18
---

# Trained Knowledge & Architecture: `Registry CMDs.txt`

- **Source Path:** `~/Projects/CORA/Training/Registry CMDs.txt` (`text`)
- **Extracted Technical Entities:** `general`
- **Extracted IPs / Subnets:** `None`
- **Extracted Interfaces:** `None`
- **Linked Command Playbook:** [[commands/trained_registry_cmds]] (`8` CEGAR-verified commands | `8` MDP transitions)

## Command & Tactic Coverage Summary
- **Total CEGAR-Verified Commands:** `8` (full executable list in [[commands/trained_registry_cmds]])
- **Tactic Distribution:** `Enumeration` (4), `Defense_Evasion_Firewall` (3), `Out-of-Band_Access` (1)
- **Top Extracted CLI Tools:** `reg` (8)

## LLM Distilled Operational Summary
### Operational Techniques & Decision Workflows
*   **Persistence Injection**: Use `reg add` to inject startup commands into `HKLM\...\CurrentVersion\RunOnce` for one-time execution on reboot.
*   **Persistence Verification**: Use `reg query` on the same key to confirm persistence entries (e.g., `RegisteredOwner`, `Test1`, `Test3`).
*   **Persistence Cleanup**: Use `reg delete` with the `/v` flag to remove specific values from the RunOnce key.
*   **RDP Configuration Audit**: Query `HKLM\System\ControlSet001\Control\Terminal Server\WinStations\RDP-Tcp` to inspect Remote Desktop settings.
*   **Firewall Policy Inspection**: Query `HKLM\SYSTEM\controlset001\services\sharedaccess\parameters\firewallpolicy\standardprofile\AuthorizedApplications\list` to verify allowed application paths and ports.

### Critical Command Patterns & Required Flags
*   **Add Value**: `reg add "<Path>" /v <Name> /d <Data> [/t <Type>]`
    *   `/v`: Specifies the value name.
    *   `/d`: Specifies the data string (default).
    *   `/t`: Specifies the type (e.g., `REG_BINARY`, `REG_DWORD`).
*   **Query Value**: `reg query "<Path>" [/v <Name>]`
    *   Omit `/v` to query all values in the key.
    *   Use `/v` to target a specific value.
*   **Delete Value**: `reg delete "<Path>" /v <Name>`
    *   `/v`: Required to specify which value to remove.

### Network Topology & Service Relationships
*   **RDP Port**: The `PortNumber` for RDP is identified as `0x22b8` (decimal 8860), indicating a non-standard RDP configuration or a specific service binding.
*   **Firewall Authorization**: The standard profile firewall policy explicitly authorizes applications via the `AuthorizedApplications\list` key, linking service execution to network egress/ingress rules.
*   **Service Registry Path**: Shared access parameters reside under `services\sharedaccess\parameters`, directly correlating service configuration with firewall policy enforcement.

