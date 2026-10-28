---
title: "Trained Knowledge & Topology: Survey CMDs -2.txt"
tags:
  - active_enum
  - arp
  - credential_access
  - defense_evasion_firewall
  - enumeration
  - eth0
  - eth1
  - https
  - iptables
  - john
  - mdp
  - netstat
  - passive_enum
  - post_exploitation_verification
  - privilege_escalation
  - ssh
  - text
  - trained
source_file: Survey CMDs -2.txt
doc_type: text
updated: 2026-10-24 01:00:36
---

# Trained Knowledge & Architecture: `Survey CMDs -2.txt`

- **Source Path:** `~/Projects/CORA/Training/Survey CMDs -2.txt` (`text`)
- **Extracted Technical Entities:** `arp, eth0, eth1, https, iptables, john, netstat, ssh`
- **Extracted IPs / Subnets:** `10.10.10.10/24, 10.18.80.64/26, 172.24.11.0/24, 172.24.11.13, 172.24.111.112/29, 172.24.2.2/24`
- **Extracted Interfaces:** `eth0, eth1`
- **Linked Command Playbook:** [[commands/trained_survey_cmds_-2]] (`190` CEGAR-verified commands | `190` MDP transitions)

## Command & Tactic Coverage Summary
- **Total CEGAR-Verified Commands:** `190` (full executable list in [[commands/trained_survey_cmds_-2]])
- **Tactic Distribution:** `Passive_Enum` (102), `Defense_Evasion_Firewall` (42), `Enumeration` (22), `Privilege_Escalation` (12), `Post_Exploitation_Verification` (6), `Credential_Access` (5), `Active_Enum` (1)
- **Top Extracted CLI Tools:** `ls` (29), `iptables` (23), `netstat` (12), `find` (11), `cat` (10), `ps` (9), `chmod` (5), `df` (4), `echo` (4), `grep` (4), `last` (4), `lsof` (4), `pfiles` (4), `chkconfig` (3), `dd` (3), `ip` (3), `mount` (3), `tar` (3), `arp` (2), `auditctl` (2), `ausearch` (2), `chown` (2), `crontab` (2), `egrep` (2), `ifconfig` (2)

## LLM Distilled Operational Summary
### Key Operational Techniques & Decision Workflows

*   **System Identification & Fingerprinting**:
    *   Determine OS type by checking `/etc/*release`, `uname -a`, and `lsb_release -a`.
    *   Verify specific OS variants: Use `psrinfo` for Solaris uptime; use `uptime` for Linux.
    *   Identify the active shell via `echo $0` or inspecting `/etc/passwd`.
*   **Process & Network Enumeration**:
    *   List processes: Use `ps -ef --sort start_time` (primary) or fallbacks like `ps -elf`/`ps auxwww`.
    *   Map network sockets: Run `sudo netstat -natup` (requires root for process association).
    *   Analyze open files/ports: Use `lsof` (Linux) or `pfiles <PID>` to correlate PIDs with open ports and binaries.
    *   Trace execution: Utilize `strace` to monitor program memory activity (e.g., `strace -o /tmp/strace.txt cat group passwd`).
*   **Kernel & Module Management**:
    *   List loaded modules: `lsmod` (Linux) or `modinfo -c | grep -i " loaded"` (Solaris).
    *   Inspect module details: `modinfo <module_name>` or `sysctl -a` for Linux kernel parameters.
    *   Remove modules: `rmmod <module_name>` (ensure not currently in use).
*   **Persistence & Scheduling Checks**:
    *   Inspect cron jobs: Scan `/etc/cron*`, `/var/spool/cron`, and `/var/spool/at`.
    *   Review user history: Check `~/.bash_history` or `~/.history`.
    *   Examine startup scripts: Review `/etc/inittab` (Solaris) and `/etc/vfstab` (Solaris).

### Critical Command Patterns & Required Flags

*   **Root Privileges**: Commands requiring process/network visibility (e.g., `netstat -p`, `pfiles`, `lsof`) typically require `sudo` or `su`.
*   **File System Analysis**:
    *   Disk usage: `df -h` (human-readable) or `df -i` (inode usage).
    *   Binary location: `ls -l /proc/<pid>/exe`.
*   **Solaris Specifics**:
    *   System info: `/usr/sbin/prtconf` (full output) or with `head` for brevity.
    *   Patch management: `showrev -p` (list) or `showrev -p | grep <patch#>` (search).
    *   Package info: `pkginfo` (list) or `pkginfo -l <PackageName>`.

### Network Topology & Service Relationships

*   **Service Port Mapping**: Cross-reference open ports with `/etc/services` to identify running services (e.g., `cat /etc/services | grep <port>`).
*   **Routing & ARP**:
    *   Routing table: `sudo netstat -rn`.
    *   ARP cache: `arp -v`.
*   **Network Configuration Files**:
    *

