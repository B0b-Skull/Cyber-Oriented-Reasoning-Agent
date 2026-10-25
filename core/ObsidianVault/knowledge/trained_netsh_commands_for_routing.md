---
title: "Trained Knowledge & Topology: Netsh commands for Routing.pdf"
tags:
  - enumeration
  - https
  - mdp
  - netsh
  - passive_enum
  - pdf
  - trained
source_file: Netsh commands for Routing.pdf
doc_type: pdf
updated: 2026-10-25 00:59:23
---

# Trained Knowledge & Architecture: `Netsh commands for Routing.pdf`

- **Source Path:** `~/Projects/CORA/Training/Netsh commands for Routing.pdf` (`pdf`)
- **Extracted Technical Entities:** `https, netsh`
- **Extracted IPs / Subnets:** `0.0.0.0, 10.0.0.2, 10.10.1.100, 10.10.10.0, 10.10.10.1, 10.11.11.1, 10.11.21.154, <LOCAL_HOST_IP>, 255.255.255.0`
- **Extracted Interfaces:** `None`
- **Linked Command Playbook:** [[commands/trained_netsh_commands_for_routing]] (`16` CEGAR-verified commands | `16` MDP transitions)

## Command & Tactic Coverage Summary
- **Total CEGAR-Verified Commands:** `16` (full executable list in [[commands/trained_netsh_commands_for_routing]])
- **Tactic Distribution:** `Enumeration` (14), `Passive_Enum` (2)
- **Top Extracted CLI Tools:** `netsh` (14), `ip` (2)

## LLM Distilled Operational Summary
### Operational Techniques & Workflows
*   **Context Switching**: Access the `netsh routing ip igmp` context via command prompt (distinct from standard Windows prompts). For remote Windows 2000 Server administration, establish a Remote Desktop Connection to a Terminal Server instance first.
*   **Scripting for Consistency**: Utilize command-line commands within scripts to apply identical IGMP configurations across multiple servers, ensuring operational consistency.
*   **WAN Optimization**: Prefer command-line administration over GUI consoles when managing servers over slow-speed Wide Area Network (WAN) links to reduce latency and improve speed.
*   **Interface Identification**: Always verify the exact interface name as displayed in the "Network Connections" GUI. If the name contains spaces, enclose it in quotation marks (e.g., `"Local Area Connection"`).

### Critical Command Patterns & Flags
*   **`add interface`**: Configures IGMP on a specific interface.
    *   *Required*: `InterfaceName`.
    *   *Optional Flags*: `IgmpPrototype` (default: `igmprtrv2`), `IfEnabled` (default: `enable`), `RobustVar`, `GenQueryInterval`, `GenQueryRespTime`, `StartUpQueryCount`, `StartUpQueryInterval`, `LastMemQueryCount`, `LastMemQueryInterval`, `AccNonRtrAlertPkts`.
*   **`install`**: Installs the IGMP router/proxy and configures global logging.
    *   *Optional Flag*: `LogLevel` (`none`, `error`, `warn`, `info`). Default behavior logs only errors.
*   **`delete interface`**: Removes an IGMP router/proxy from a specific interface.
    *   *Required*: `InterfaceName`.
*   **`uninstall`**: Removes the IGMP router/proxy from all interfaces.
    *   *Parameters*: None.
*   **`set interface`**: Modifies existing interface configuration parameters (syntax mirrors `add interface`).

### Network Topology & Relationships
*   **Protocol Support**: The commands support IGMPv1, IGMPv2, IGMPv3, and IGMP Proxy modes.
*   **Platform Compatibility**: Functional differences exist between Windows 2000 Server and Windows XP implementations; ensure the target OS matches the documentation context.
*   **Logging Scope**: The `install` command controls the scope of IGMP-related event logging (ranging from error-only to full info) globally for the routing server.

