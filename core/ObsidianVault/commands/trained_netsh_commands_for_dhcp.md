---
title: "Trained Command Playbook: Netsh commands for DHCP.pdf"
tags:
  - enumeration
  - https
  - mdp
  - netsh
  - passive_enum
  - pdf
  - trained
source_file: Netsh commands for DHCP.pdf
updated: 2026-10-25 00:59:23
---

# Trained Command Playbook: `Netsh commands for DHCP.pdf`

- **Source Document:** `~/Projects/CORA/Training/Netsh commands for DHCP.pdf`
- **CEGAR Verified Commands:** `14` (`0` malformed/unsafe snippets filtered)
- **MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`):** `14`
- **Discovered IPs/Subnets:** `10.0.0.0, 10.0.0.1, 10.1.1.1, 10.1.1.2, 10.1.1.3, 10.1.1.50, 10.2.1.10, 10.2.1.32, 10.2.1.5, 10.2.2.0, 10.2.2.10, 10.2.2.100, 10.2.2.2, 10.2.2.20, 10.2.2.32, 172.24.0.0, 172.24.0.100, 224.0.0.0, 224.2.2.10, 224.2.2.20, 239.255.255.255, 255.255.255.0`
- **Discovered Interfaces:** `None`
- **Related Knowledge Note:** [[knowledge/trained_netsh_commands_for_dhcp]]

## Distilled MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`)
| Pre-State ($s$) | Tactic ($\tau$) | Technique ($k$) | Tool ($u$) | Post-State ($s'$) | Verified Command ($c$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `netsh` | `s_active_services_enumerated` | `Netsh commands for DHCP` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `ip` | `s_passive_topology_mapped` | `IP address 10.2.2.2 to the list of authorized servers in Active Directory.` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `netsh` | `s_active_services_enumerated` | `Netsh DHCP` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `ip` | `s_passive_topology_mapped` | `IP address 10.0.0.1.` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `del` | `s_active_services_enumerated` | `del class "Default Routing and Remote Access Class"` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `ip` | `s_passive_topology_mapped` | `IP address.` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `del` | `s_active_services_enumerated` | `del class "Default BOOTP Class"` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `del` | `s_active_services_enumerated` | `del class "Microsoft Windows 2000 Options"` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `del` | `s_active_services_enumerated` | `del class "Microsoft Windows 98 Options"` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `del` | `s_active_services_enumerated` | `del class "Microsoft Options"` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `netsh` | `s_active_services_enumerated` | `netsh exec dhcpcfg.dmp` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `netsh` | `s_active_services_enumerated` | `Netsh DHCP server` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `netsh` | `s_active_services_enumerated` | `Netsh DHCP server scope` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `netsh` | `s_active_services_enumerated` | `Netsh DHCP server mscope` |

## Verified Executable Commands (Grouped by Capability Layer)

### General_System (5 commands)
```bash
del class "Default Routing and Remote Access Class"
del class "Default BOOTP Class"
del class "Microsoft Windows 2000 Options"
del class "Microsoft Windows 98 Options"
del class "Microsoft Options"
```

### L3_Routing_NAT (9 commands)
```bash
Netsh commands for DHCP
Netsh DHCP
IP address 10.2.2.2 to the list of authorized servers in Active Directory.
netsh exec dhcpcfg.dmp
IP address 10.0.0.1.
Netsh DHCP server
IP address.
Netsh DHCP server scope
Netsh DHCP server mscope
```

