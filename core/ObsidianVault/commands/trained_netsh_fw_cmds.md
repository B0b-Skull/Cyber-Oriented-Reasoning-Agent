---
title: "Trained Command Playbook: Netsh FW CMDs.txt"
tags:
  - defense_evasion_firewall
  - mdp
  - netsh
  - text
  - trained
source_file: Netsh FW CMDs.txt
updated: 2026-10-25 00:59:23
---

# Trained Command Playbook: `Netsh FW CMDs.txt`

- **Source Document:** `~/Projects/CORA/Training/Netsh FW CMDs.txt`
- **CEGAR Verified Commands:** `27` (`0` malformed/unsafe snippets filtered)
- **MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`):** `27`
- **Discovered IPs/Subnets:** `172.24.11.14, 212.54.40.25`
- **Discovered Interfaces:** `None`
- **Related Knowledge Note:** [[knowledge/trained_netsh_fw_cmds]]

## Distilled MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`)
| Pre-State ($s$) | Tactic ($\tau$) | Technique ($k$) | Tool ($u$) | Post-State ($s'$) | Verified Command ($c$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `netsh` | `s_firewall_or_acl_unlocked` | `netsh advfirewall firewall set rule group="File and Printer Sharing" new enable=no` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `netsh` | `s_firewall_or_acl_unlocked` | `netsh advfirewall firewall set rule group="File and Printer Sharing" new enable=yes` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `netsh` | `s_firewall_or_acl_unlocked` | `netsh advfirewall set allprofiles state off` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `netsh` | `s_firewall_or_acl_unlocked` | `netsh advfirewall show currentprofile` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `netsh` | `s_firewall_or_acl_unlocked` | `netsh advfirewall show currentprofile state off` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `netsh` | `s_firewall_or_acl_unlocked` | `netsh advfirewall show currentprofile state on` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `netsh` | `s_firewall_or_acl_unlocked` | `netsh advfirewall firewall show rule profile=private name=all` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `netsh` | `s_firewall_or_acl_unlocked` | `netsh advfirewall firewall show rule profile=private name=all > fwrules.txt` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `netsh` | `s_firewall_or_acl_unlocked` | `netsh advfirewall firewall show rule name=all verbose` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `netsh` | `s_firewall_or_acl_unlocked` | `netsh advfirewall set Domain state off` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `netsh` | `s_firewall_or_acl_unlocked` | `Netsh advfirewall firewall add rule name="1337 h4x " dir=in protocol=tcp localport=31337 remoteport=6666 remoteip=172.24.11.14 profile=private action=allow` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `netsh` | `s_firewall_or_acl_unlocked` | `netsh advfirewall firewall delete rule name ="1337H4X"` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `netsh` | `s_firewall_or_acl_unlocked` | `netsh advfirewall firewall show rule name="svchost service"` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `netsh` | `s_firewall_or_acl_unlocked` | `netsh advfirewall firewall add rule name="svchost service" dir=in protocol=tcp localport=443 profile=any action=allow` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `netsh` | `s_firewall_or_acl_unlocked` | `netsh advfirewall firewall add rule name="Fox" dir=in action=allow program="C:\Programs Files (x86)\Mozilla Firefox\firefox.exe" enable=yes` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `netsh` | `s_firewall_or_acl_unlocked` | `Netsh advfirewall firewall show rule name=all \| find /I "File and Printer Sharing" \| find /I "rule name"` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `netsh` | `s_firewall_or_acl_unlocked` | `netsh advfirewall firewall set rule name="File and Printer Sharing (NB-Session-In)" new enable=yes profile=domain,public` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `netsh` | `s_firewall_or_acl_unlocked` | `netsh advfirewall firewall set rule name="File and Printer Sharing" profile=Domain,Public new enable=yes` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `netsh` | `s_firewall_or_acl_unlocked` | `netsh advfirewall export "C:\FW-Before-Changes.wfw"` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `netsh` | `s_firewall_or_acl_unlocked` | `netsh advfirewall export "%userprofile%\Desktop\FirewallPolicy.wfw"` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `netsh` | `s_firewall_or_acl_unlocked` | `netsh advfirewall import "X:\Path\to\FirewallPolicy.wfw"` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `netsh` | `s_firewall_or_acl_unlocked` | `netsh advfirewall firewall add rule name="FTP Service" action=block service=ftpsvc protocol=TCP dir=in` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `netsh` | `s_firewall_or_acl_unlocked` | `netsh advfirewall set global StatefulFTP disable` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `netsh` | `s_firewall_or_acl_unlocked` | `netsh advfirewall firewall add rule name="Block FTP" protocol=TCP localport=21 action=block dir=in` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `netsh` | `s_firewall_or_acl_unlocked` | `netsh advfirewall firewall add rule name="Remote Desktop" protocol=TCP localport=31669 action=allow dir=in` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `netsh` | `s_firewall_or_acl_unlocked` | `netsh advfirewall firewall add rule name="Open port 80" protocol=TCP localport=80 action=allow dir=OUT remoteip=212.54.40.25` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `netsh` | `s_firewall_or_acl_unlocked` | `netsh advfirewall firewall add rule name="Open port 443" protocol=TCP localport=443 action=allow dir=OUT remoteip=212.54.40.25` |

## Verified Executable Commands (Grouped by Capability Layer)

### L3_Routing_NAT (27 commands)
```bash
netsh advfirewall firewall set rule group="File and Printer Sharing" new enable=no
netsh advfirewall firewall set rule group="File and Printer Sharing" new enable=yes
netsh advfirewall set allprofiles state off
netsh advfirewall show currentprofile
netsh advfirewall show currentprofile state off
netsh advfirewall show currentprofile state on
netsh advfirewall firewall show rule profile=private name=all
netsh advfirewall firewall show rule profile=private name=all > fwrules.txt
netsh advfirewall firewall show rule name=all verbose
netsh advfirewall set Domain state off
Netsh advfirewall firewall add rule name="1337 h4x " dir=in protocol=tcp localport=31337 remoteport=6666 remoteip=172.24.11.14 profile=private action=allow
netsh advfirewall firewall delete rule name ="1337H4X"
netsh advfirewall firewall show rule name="svchost service"
netsh advfirewall firewall add rule name="svchost service" dir=in protocol=tcp localport=443 profile=any action=allow
netsh advfirewall firewall add rule name="Fox" dir=in action=allow program="C:\Programs Files (x86)\Mozilla Firefox\firefox.exe" enable=yes
Netsh advfirewall firewall show rule name=all | find /I "File and Printer Sharing" | find /I "rule name"
netsh advfirewall firewall set rule name="File and Printer Sharing (NB-Session-In)" new enable=yes profile=domain,public
netsh advfirewall firewall set rule name="File and Printer Sharing" profile=Domain,Public new enable=yes
netsh advfirewall export "C:\FW-Before-Changes.wfw"
netsh advfirewall export "%userprofile%\Desktop\FirewallPolicy.wfw"
netsh advfirewall import "X:\Path\to\FirewallPolicy.wfw"
netsh advfirewall firewall add rule name="FTP Service" action=block service=ftpsvc protocol=TCP dir=in
netsh advfirewall set global StatefulFTP disable
netsh advfirewall firewall add rule name="Block FTP" protocol=TCP localport=21 action=block dir=in
netsh advfirewall firewall add rule name="Remote Desktop" protocol=TCP localport=31669 action=allow dir=in
netsh advfirewall firewall add rule name="Open port 80" protocol=TCP localport=80 action=allow dir=OUT remoteip=212.54.40.25
netsh advfirewall firewall add rule name="Open port 443" protocol=TCP localport=443 action=allow dir=OUT remoteip=212.54.40.25
```

