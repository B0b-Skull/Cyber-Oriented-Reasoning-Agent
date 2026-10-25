---
title: "Trained Knowledge & Topology: Netsh commands for DHCP.pdf"
tags:
  - enumeration
  - https
  - mdp
  - netsh
  - passive_enum
  - pdf
  - trained
source_file: Netsh commands for DHCP.pdf
doc_type: pdf
updated: 2026-10-25 00:59:23
---

# Trained Knowledge & Architecture: `Netsh commands for DHCP.pdf`

- **Source Path:** `~/Projects/CORA/Training/Netsh commands for DHCP.pdf` (`pdf`)
- **Extracted Technical Entities:** `https, netsh`
- **Extracted IPs / Subnets:** `10.0.0.0, 10.0.0.1, 10.1.1.1, 10.1.1.2, 10.1.1.3, 10.1.1.50, 10.2.1.10, 10.2.1.32, 10.2.1.5, 10.2.2.0, 10.2.2.10, 10.2.2.100, 10.2.2.2, 10.2.2.20, 10.2.2.32, 172.24.0.0, 172.24.0.100, 224.0.0.0, 224.2.2.10, 224.2.2.20, 239.255.255.255, 255.255.255.0`
- **Extracted Interfaces:** `None`
- **Linked Command Playbook:** [[commands/trained_netsh_commands_for_dhcp]] (`14` CEGAR-verified commands | `14` MDP transitions)

## Command & Tactic Coverage Summary
- **Total CEGAR-Verified Commands:** `14` (full executable list in [[commands/trained_netsh_commands_for_dhcp]])
- **Tactic Distribution:** `Enumeration` (11), `Passive_Enum` (3)
- **Top Extracted CLI Tools:** `netsh` (6), `del` (5), `ip` (3)

## LLM Distilled Operational Summary
### Operational Techniques & Decision Workflows

*   **Environment Selection**: Use `netsh dhcp` for managing servers in Wide Area Networks (WANs) or when scripting batch operations for automation. Note that these commands require Windows 2000 Server or later; they are not available on local Windows XP Professional/Home editions without Remote Desktop Connection to a Terminal Server.
*   **Server Authorization Workflow**:
    *   **Add**: Use `add server <DNS> <IP>` to authorize a new DHCP server in Active Directory.
    *   **Delete**: Use `delete server <DNS> <IP>` to remove a server from the authorized list.
*   **Configuration Migration (Clone) Workflow**:
    1.  **Prepare Source**: Reconcile scopes and fix inconsistencies on the source server.
    2.  **Dump**: Execute `[{\\ServerName | IPAddress}] dump > FileName` to export the configuration (e.g., `dhcpcfg.dmp`).
    3.  **Prepare Destination**: Close the DHCP console, delete all default option definitions (`delete optiondef 01`, `76`), and remove user/vendor classes (`del class "..."`).
    4.  **Execute**: Transfer the dump file and run `netsh exec FileName` on the destination server.
    5.  **Finalize**: Reconcile scopes, stop the DHCP service (`net stop dhcpserver`), and restart it (`net start dhcpserver`) to apply changes.

### Critical Command Patterns & Required Flags

*   **Server Management**:
    *   `add server <ServerDNS> <ServerIP>` (Both parameters required).
    *   `delete server <ServerDNS> <ServerIP>` (Both parameters required).
*   **Configuration Export**:
    *   `[{\\ServerName | IPAddress}] dump > [FileName]`.
        *   *Flag/Param*: `[\\ServerName | IPAddress]` specifies the remote target; omit for local.
        *   *Flag/Param*: `> [FileName]` redirects output to a file (e.g., `.dmp`).
*   **Configuration Import**:
    *   `netsh exec <FileName>` (Requires a clean destination state).
*   **Cleanup Prerequisites (for Import)**:
    *   `delete optiondef 01`
    *   `delete optiondef 76`
    *   `del class "Default Routing and Remote Access Class"`
    *   `del class "Default BOOTP Class"`
    *   `del class "Microsoft Windows 2000 Options"`
    *   `del class "Microsoft Windows 98 Options"`
    *   `del class "Microsoft Options"`

### Network Topology & Service Relationships

*   **Active Directory Integration**: Authorization commands (`add server`, `delete server`) interact directly with Active Directory to manage the list of trusted DHCP servers.
*   **Service Lifecycle**: The `exec` command modifies the DHCP database; changes only take effect after the `dhcpserver` service is restarted using `net stop dhcpserver` and `net start dhcpserver`.
*   **Remote Management**: Commands support remote execution via `\\ServerName` or `IPAddress`, enabling management of non-local servers provided the connection (e.g., R

## Extracted Operational Steps & Workflows
- 1. Close the DHCP console at the destination server. Do not reopen the console until after you use
- 2. Delete all default option definitions and any user and vendor classes at the destination server.
- 255.
Examples

