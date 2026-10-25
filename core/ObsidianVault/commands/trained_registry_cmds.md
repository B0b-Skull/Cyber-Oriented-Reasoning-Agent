---
title: "Trained Command Playbook: Registry CMDs.txt"
tags:
  - defense_evasion_firewall
  - enumeration
  - mdp
  - out-of-band_access
  - text
  - trained
source_file: Registry CMDs.txt
updated: 2026-10-25 01:00:18
---

# Trained Command Playbook: `Registry CMDs.txt`

- **Source Document:** `~/Projects/CORA/Training/Registry CMDs.txt`
- **CEGAR Verified Commands:** `8` (`0` malformed/unsafe snippets filtered)
- **MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`):** `8`
- **Discovered IPs/Subnets:** `None`
- **Discovered Interfaces:** `None`
- **Related Knowledge Note:** [[knowledge/trained_registry_cmds]]

## Distilled MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`)
| Pre-State ($s$) | Tactic ($\tau$) | Technique ($k$) | Tool ($u$) | Post-State ($s'$) | Verified Command ($c$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `reg` | `s_active_services_enumerated` | `reg add "HKLM\Software\Microsoft\Windows\CurrentVersion\RunOnce" /v RegisteredOwner /d computer11` |
| `s_l2_l3_verified` | **`Out-of-Band_Access`** | UART/Serial Console Out-of-Band Enumeration & Control | `reg` | `s_oob_serial_enumerated` | `reg query "HKLM\System\ControlSet001\Control\Terminal Server\WinStations\RDP-Tcp"` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `reg` | `s_firewall_or_acl_unlocked` | `reg query hkcu\software\microsoft\windows\currentversion\run` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `reg` | `s_active_services_enumerated` | `reg add "HKLM\Software\Microsoft\Windows\CurrentVersion\RunOnce" /v Test3 /t REG_BINARY /d aaaaaaaaaa` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `reg` | `s_firewall_or_acl_unlocked` | `reg query HKLM\SYSTEM\controlset001\services\sharedaccess\parameters\firewallpolicy\standardprofile\AuthorizedApplications\list` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `reg` | `s_active_services_enumerated` | `reg add "HKLM\Software\Microsoft\Windows\CurrentVersion\RunOnce" /v Test1 /t REG_BINARY /d bbbbbbbbbb` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `reg` | `s_firewall_or_acl_unlocked` | `reg query "HKLM\Software\Microsoft\Windows\CurrentVersion\RunOnce"` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `reg` | `s_active_services_enumerated` | `reg delete "HKLM\Software\Microsoft\Windows\CurrentVersion\RunOnce" /v Test2` |

## Verified Executable Commands (Grouped by Capability Layer)

### General_System (8 commands)
```bash
reg add "HKLM\Software\Microsoft\Windows\CurrentVersion\RunOnce" /v RegisteredOwner /d computer11
reg query "HKLM\System\ControlSet001\Control\Terminal Server\WinStations\RDP-Tcp"
reg query hkcu\software\microsoft\windows\currentversion\run
reg query HKLM\SYSTEM\controlset001\services\sharedaccess\parameters\firewallpolicy\standardprofile\AuthorizedApplications\list
reg query "HKLM\Software\Microsoft\Windows\CurrentVersion\RunOnce"
reg add "HKLM\Software\Microsoft\Windows\CurrentVersion\RunOnce" /v Test3 /t REG_BINARY /d aaaaaaaaaa
reg add "HKLM\Software\Microsoft\Windows\CurrentVersion\RunOnce" /v Test1 /t REG_BINARY /d bbbbbbbbbb
reg delete "HKLM\Software\Microsoft\Windows\CurrentVersion\RunOnce" /v Test2
```

