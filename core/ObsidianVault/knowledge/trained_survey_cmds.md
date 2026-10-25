---
title: "Trained Knowledge & Topology: Survey CMDs.txt"
tags:
  - arp
  - credential_access
  - defense_evasion_firewall
  - enumeration
  - https
  - iptables
  - mdp
  - netstat
  - passive_enum
  - post_exploitation_verification
  - text
  - trained
source_file: Survey CMDs.txt
doc_type: text
updated: 2026-10-25 01:00:37
---

# Trained Knowledge & Architecture: `Survey CMDs.txt`

- **Source Path:** `~/Projects/CORA/Training/Survey CMDs.txt` (`text`)
- **Extracted Technical Entities:** `arp, https, iptables, netstat`
- **Extracted IPs / Subnets:** `1.0.0.1, 126.255.255.254, 128.1.0.1, 191.255.255.254, 192.0.1.1, 223.255.254.254, 224.0.0.0, 239.255.255.255`
- **Extracted Interfaces:** `None`
- **Linked Command Playbook:** [[commands/trained_survey_cmds]] (`89` CEGAR-verified commands | `89` MDP transitions)

## Command & Tactic Coverage Summary
- **Total CEGAR-Verified Commands:** `89` (full executable list in [[commands/trained_survey_cmds]])
- **Tactic Distribution:** `Passive_Enum` (38), `Defense_Evasion_Firewall` (25), `Credential_Access` (20), `Post_Exploitation_Verification` (4), `Enumeration` (2)
- **Top Extracted CLI Tools:** `ls` (17), `cat` (11), `find` (10), `ps` (6), `netstat` (5), `ip` (2), `iptables` (2), `ss` (2), `uname` (2), `arp` (1), `chkconfig` (1), `cp` (1), `date` (1), `echo` (1), `file` (1), `fuser` (1), `getenforce` (1), `grep` (1), `history` (1), `hostid` (1), `hostname` (1), `ifconfig` (1), `last` (1), `lsmod` (1), `lsof` (1)

## LLM Distilled Operational Summary
### Operational Techniques & Decision Workflows

*   **Session Hygiene:** Disable command history logging (`unset HISTFILE`) and capture the transcript to a file (`script`) before execution; clean up post-survey.
*   **Process Analysis Workflow:**
    *   Identify running processes (`ps -ef`, `ps -auxwe`).
    *   Trace execution paths using `/proc/<PID>/exe` or `strings` on binaries.
    *   Verify user context and working directories (`pwdx`, `ps -p $$`).
*   **Startup & Persistence Hunting:**
    *   Inspect init scripts via `/etc/rc*.d`, `/etc/init.d/*`, and `run-parts`.
    *   Review cron jobs across `/etc/cron*` and `/etc/crontab`.
    *   Check system release info (`/etc/*-release`) and kernel modules (`lsmod`, `modinfo`).
*   **Network Topology & Connections:**
    *   Map active connections (`netstat -anpt`, `ss -lne`).
    *   Identify listening services and bound ports (`ifconfig`, `ip addr`).
    *   Resolve reverse mappings for specific PIDs or ports (`fuser`, `/proc/<PID>/fd`).
*   **File System Anomalies:**
    *   Search for recently modified files (`find ... -newermt`) or hidden files/directories containing specific usernames.
    *   Verify binary types and execution contexts (`file`, `type -a`).

### Critical Command Patterns & Required Flags

| Goal | Command Pattern | Key Flags/Notes |
| :--- | :--- | :--- |
| **Process Tree** | `ps -efh` / `ptree` | `ptree` is Solaris-specific. |
| **Network State** | `netstat -anpt` / `ss -lne` | `-p` (PID), `-t` (TCP), `-u` (UDP), `-n` (numeric). |
| **Init Scripts** | `ls -Rltc /etc/rc.d/init.d` | `-R` (recursive), `-l` (long), `-t` (time), `-c` (change time). |
| **Cron Jobs** | `ls -al /etc/cron*` | Checks all cron-related directories. |
| **User Context** | `cat /etc/passwd` / `who -r` | Verify shell assignment and run level. |
| **Binary Path** | `ps -auxwe \| grep <PID>` | Shows full path and environment. |
| **Hidden Files** | `find / -type f -name ".*"` | Locate hidden artifacts. |

### Network Topology & Service Relationships

*   **OS Specifics:** Commands like `ptree`, `psrinfo`, and `modinfo` indicate **Solaris** environments, while `lsmod`, `ss`, and `/proc/cpuinfo` indicate **Linux**.
*   **Service Discovery:** Services are often defined in `/etc/rc*.d` (S-prefixed scripts execute on boot) and managed via `chkconfig` (Linux) or `service --status-all`.
*   **Port Binding:** Use `fuser <port>/tcp` to find the Process

