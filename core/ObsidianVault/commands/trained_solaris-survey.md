---
title: "Trained Command Playbook: Solaris-Survey"
category: commands
domain_hub: "[[knowledge/06_linux_unix_administration_processes_and_logging]]"
os_platform: linux
primary_tactic: Passive_Enum
summary: "Verified Windows & Linux command playbook for Solaris-Survey (Passive_Enum): Linux (Debian/Ubuntu/CentOS/RHEL) and UNIX/Solaris system administration, kernel /proc & sysctl internals, ext4/xfs/procfs filesystems,"
when_to_apply: "Apply when working with Solaris-Survey (linux): Apply when enumerating a Linux/UNIX/Solaris host, inspecting `/proc/<PID>` or kernel modules, auditing mounted filesystems (`findmnt`/`lsblk`), managing `systemd` services or signals, hunting SUID/SGID/Capabilities/sudo privilege escalation vectors, reviewing `/var/log`/`journalctl` logs, or upgrading a dumb shell to a full interactive TTY."
tags: [arp, credential_access, defense_evasion_firewall, enumeration, https, mdp, netstat, passive_enum, post_exploitation_verification, privilege_escalation, ssh, text, trained, linux, unix, solaris, systemctl, journalctl, lsof, strace, findmnt, lsblk]
source_file: "Solaris-Survey"
updated: 2026-10-30
---

uname -a; cat /etc/os-release; hostnamectl; uptime; id
# Trained Command Playbook: `Solaris-Survey.txt`
uname -a; cat /etc/os-release; hostnamectl; uptime; id
- **Source Document:** `~/Projects/CORA/Training/Solaris-Survey.txt`
- **CEGAR Verified Commands:** `71` (`0` malformed/unsafe snippets filtered)
- **MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`):** `71`
- **Discovered IPs/Subnets:** `None`
- **Discovered Interfaces:** `None`
- **Related Knowledge Note:** [[knowledge/trained_solaris-survey]]
uname -a; cat /etc/os-release; hostnamectl; uptime; id
## Distilled MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`)
| Pre-State ($s$) | Tactic ($\tau$) | Technique ($k$) | Tool ($u$) | Post-State ($s'$) | Verified Command ($c$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `date` | `s_passive_topology_mapped` | `date` |
| `s_cross_subnet_pivot_routed` | **`Post_Exploitation_Verification`** | Post-Action Host Identity, Privilege & Objective Verification | `uname` | `s_goal_verified_complete` | `uname -a` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `locate` | `s_active_services_enumerated` | `Locate Files` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `pfiles` | `s_interactive_tty_or_priv_escalated` | `pfiles <PID> \| grep AF_INET` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `cat` | `s_credentials_or_certs_acquired` | `cat /var/adm/sulog` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `cat` | `s_firewall_or_acl_unlocked` | `cat /etc/nsswitch.conf \| grep "hosts"` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `psrinfo` | `s_passive_topology_mapped` | `psrinfo -v` |
| `s_cross_subnet_pivot_routed` | **`Post_Exploitation_Verification`** | Post-Action Host Identity, Privilege & Objective Verification | `who` | `s_goal_verified_complete` | `who -r` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `cp` | `s_active_services_enumerated` | `cp -p` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `pfiles` | `s_interactive_tty_or_priv_escalated` | `pfiles /proc/*` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `crontab` | `s_credentials_or_certs_acquired` | `crontab -e` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `ipfstat` | `s_firewall_or_acl_unlocked` | `ipfstat -io` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `uptime` | `s_passive_topology_mapped` | `uptime` |
| `s_cross_subnet_pivot_routed` | **`Post_Exploitation_Verification`** | Post-Action Host Identity, Privilege & Objective Verification | `groups` | `s_goal_verified_complete` | `groups` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `which` | `s_active_services_enumerated` | `which sudo` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `rpcinfo` | `s_interactive_tty_or_priv_escalated` | `rpcinfo -p` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `cat` | `s_firewall_or_acl_unlocked` | `cat /etc/ipf/ipf.conf` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `sysdef` | `s_passive_topology_mapped` | `sysdef -h` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `cat` | `s_active_services_enumerated` | `cat /export/<username>/.bash_history` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `find` | `s_interactive_tty_or_priv_escalated` | `find / -perm -u=s 2>/dev/null \| xargs ls -la \| more` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `cat` | `s_firewall_or_acl_unlocked` | `cat /etc/syslog.conf` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `modinfo` | `s_passive_topology_mapped` | `modinfo -c \| grep ' LOADED' \| more` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `grep` | `s_interactive_tty_or_priv_escalated` | `grep ops.local `find /etc -name \*.conf`` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `svcs` | `s_firewall_or_acl_unlocked` | `svcs \| wc -1` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `vmstat` | `s_passive_topology_mapped` | `vmstat` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `grep` | `s_interactive_tty_or_priv_escalated` | `grep ops.local $(find /etc -name '*.conf')` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `crontab` | `s_firewall_or_acl_unlocked` | `crontab -l <username>` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `find` | `s_passive_topology_mapped` | `find . -mtime $(date +%s -d"Aug 10, 2013 23:59:59") -mtime $(date +%s -d"Aug 1, 2013 23:59:59")` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `ls` | `s_interactive_tty_or_priv_escalated` | `ls -l` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `ls` | `s_firewall_or_acl_unlocked` | `ls -l /var/spool/cron/crontabs` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `find` | `s_passive_topology_mapped` | `find / -type f -name ".*" \| grep <username>` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `chown` | `s_interactive_tty_or_priv_escalated` | `chown <NewOwnerUsername> <Filename>` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `crontab` | `s_firewall_or_acl_unlocked` | `crontab -l` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `find` | `s_passive_topology_mapped` | `find / -type d -name ".*" \| grep <username>` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `chgrp` | `s_interactive_tty_or_priv_escalated` | `chgrp <newOwnerGroup> <Filename>` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `find` | `s_passive_topology_mapped` | `find ~/ -mtime $(echo $(date +%s) - $(date +%s -d"Dec 31, 2009 23:59:59") \| bc -l \| awk '{print $1 / 86400}' \| bc -l)` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `chmod` | `s_interactive_tty_or_priv_escalated` | `chmod symbolic-mode-list <Filename>` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `ps` | `s_passive_topology_mapped` | `ps -efj \| grep 711` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `chmod` | `s_interactive_tty_or_priv_escalated` | `chmod u+rw,g=w,go-wx /home/hohnd/script.sh` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `ps` | `s_passive_topology_mapped` | `ps -efj \| grep ssh` |
uname -a; cat /etc/os-release; hostnamectl; uptime; id
## Verified Executable Commands (Grouped by Capability Layer)
uname -a; cat /etc/os-release; hostnamectl; uptime; id
### General_System (64 commands)
```bash
date
uname -a
psrinfo -v
uptime
sysdef -h
modinfo -c | grep ' LOADED' | more
vmstat
who -r
Locate Files
find . -mtime $(date +%s -d"Aug 10, 2013 23:59:59") -mtime $(date +%s -d"Aug 1, 2013 23:59:59")
find / -type f -name ".*" | grep <username>
find / -type d -name ".*" | grep <username>
find ~/ -mtime $(echo $(date +%s) - $(date +%s -d"Dec 31, 2009 23:59:59") | bc -l | awk '{print $1 / 86400}' | bc -l)
ps -efj | grep 711
ps -efj | grep ssh
ps -ajf
fuser .
fuser /folder/location 22/tcp
ptree <PID>
pfiles `ls /proc` 2>/dev/null | awk "/^ [^ \\t]/{smatch=\$0;next}/port:[ \\t]*${1}/{print smatch, \$0}{next}"
ps -ef| awk '{print $2}'| xargs -I '{}' sh -c 'echo Examining process: {}; pfiles {}| grep "port: *"'
pfiles <PID> | grep AF_INET
pfiles /proc/*
find / -perm -u=s 2>/dev/null | xargs ls -la | more
grep ops.local `find /etc -name \*.conf`
grep ops.local $(find /etc -name '*.conf')
grep 'This I\$ Y\*ur File' /root/*
stat /tmp
ls -al /tmp
ls -l
ls -lu
ls -lc
cp -p
which sudo
strings `which sudo`
groups
cat /var/adm/sulog
ls -iRl | grep <inode number>
cat /etc/resolv.conf
cat /etc/nsswitch.conf | grep "hosts"
cat /etc/ipf/ipf.conf
cat /etc/syslog.conf
svcs | wc -1
crontab -l <username>
ls -l /var/spool/cron/crontabs
cat /var/spool/cron/crontabs/<name>
cat /etc/init.d/<file>
inetadm | grep enabled
df -t
df -k -l
chown <NewOwnerUsername> <Filename>
chgrp <newOwnerGroup> <Filename>
chmod symbolic-mode-list <Filename>
chmod u+rw,g=w,go-wx /home/hohnd/script.sh
chmod ugo=r /file/location
chmod 653 /home/johnd/comments.txt
chown fred:staff helloscript.sh
chmod o+rx /tmp/movelog.sh
cat /etc/security/policy.conf | grep -v "#"
cat /etc/user_attr
cat /.bash_history | grep "telnet"
cat /export/<username>/.bash_history
crontab -l
crontab -e
```
uname -a; cat /etc/os-release; hostnamectl; uptime; id
### L2_ARP_Link (1 commands)
```bash
arp -na
```
uname -a; cat /etc/os-release; hostnamectl; uptime; id
### L3_Routing_NAT (2 commands)
```bash
ping -c 3 `cat /etc/resolv.conf | grep nameserver | awk '{print $2}' | head -n 1`
ipfstat -io
```
uname -a; cat /etc/os-release; hostnamectl; uptime; id
### L4_Port_Service (4 commands)
```bash
rpcinfo -p
netstat -rn
netstat -anf inet -P tcp | more
netstat -anf inet -P udp | more
```
uname -a; cat /etc/os-release; hostnamectl; uptime; id

<!-- CORA-MAXIMIZED-COMMANDS-START -->
## Maximized Windows & Linux Command Examples for `Solaris-Survey`

> **Domain Hub:** [[knowledge/06_linux_unix_administration_processes_and_logging|Domain Hub 06: Linux, UNIX & Solaris Administration, Kernel (/proc & sysctl), Filesystems, Boot/systemd, Processes, Permissions/SUID & Logging]]  
> **Master Playbooks:** [[commands/windows_master_command_playbook]] | [[commands/linux_master_command_playbook]] | [[commands/curl_playbook]] | [[commands/tio_serial_playbook]]  
> **When to Apply:** Apply when enumerating a Linux/UNIX/Solaris host, inspecting `/proc/<PID>` or kernel modules, auditing mounted filesystems (`findmnt`/`lsblk`), managing `systemd` services or signals, hunting SUID/SGID/Capabilities/sudo privilege escalation vectors, reviewing `/var/log`/`journalctl` logs, or upgrading a dumb shell to a full interactive TTY.  
> **15-Engine H-MDP State Transition:** `s_init_unknown` $\xrightarrow{\text{Passive_Enum}}$ `s_interactive_tty_or_priv_escalated` | **Bayesian Root-Cause Triggers:** `suid_or_capability_privesc_vector, writable_systemd_or_cron_script, unlinked_proc_binary_execution, dumb_shell_missing_pty` | **Isolation:** `RED, BLUE, WHITE (100% local host telemetry compatible)`

| Primary Command (`Windows` / `Linux`) | OS / Shell | What It Does & Key Flags | When to Apply & Expected Output | Cross-Platform Equivalent |
| :--- | :--- | :--- | :--- | :--- |
| `uname -a; cat /etc/os-release; hostnamectl; uptime; id` | **Linux Bash** | Collects kernel version, architecture, OS distribution, hostname, system load, and current user UID/GID/groups (`[[commands/trained_centos-debian-survey]]`). | Apply first on any Linux/UNIX system (`s_init_unknown`) to establish OS and privilege baseline. | `systeminfo && whoami /all` |
| `ps auxef && ps -eo pid,ppid,user,stat,lstart,args --forest` | **Linux Bash** | Displays full process tree (`--forest`), UID, PID, PPID, start timestamp, and full command line (`[[commands/trained_cqc001_e050_m050_process_and_signals]]`). | Apply to identify running daemons, abnormal child processes, or processes executing from `/tmp` or `/dev/shm`. | `wmic process get ProcessId,ParentProcessId,ExecutablePath,CommandLine` |
| `sudo ls -la /proc/<PID>/exe /proc/<PID>/cwd /proc/<PID>/fd && tr '\0' '\n' < /proc/<PID>/environ` | **Linux Bash** | Inspects the live kernel `/proc/<PID>` binary link (`exe`), working directory (`cwd`), open descriptors (`fd`), and environment variables (`environ`). | Apply during Linux live forensics: recovers deleted binaries (`cp /proc/<PID>/exe /tmp/recovered`) and exposes secrets in process environments. | `handle -accepteula -a -p <PID>` |
| `systemctl list-units --type=service --state=running && systemctl list-timers --all` | **Linux Bash** | Lists all active `systemd` services and scheduled timers (`[[commands/trained_cqc001_e050_m040_boot_init_login]]`). | Apply to audit running services and periodic scheduled tasks on modern `systemd` distributions. | `sc query state= active && schtasks /query` |
| `df -hT && lsblk -f && findmnt` | **Linux Bash** | Lists mounted filesystems with filesystem type (`ext4`, `xfs`, `tmpfs`), block device hierarchy, UUIDs, and mount flags (`noexec`, `nosuid`) (`[[knowledge/trained_cqc001_e050_m030_filesystems]]`). | Apply to inspect storage layout and verify which writable directories (`/tmp`, `/var/tmp`, `/dev/shm`) allow binary execution. | `wmic logicaldisk get DeviceID,FileSystem,FreeSpace,Size` |
| `sudo -l && find / -perm -4000 -type f -exec ls -la {} + 2>/dev/null && getcap -r / 2>/dev/null` | **Linux Bash** | Audits allowed `sudo` commands, SUID root binaries (`-perm -4000`), and POSIX file capabilities (`getcap -r /`) (`[[commands/trained_cqc001_e060_m010_users_and_permissions]]`). | Apply immediately during Linux privilege escalation (`s_initial_shell_or_api_access -> s_interactive_tty_or_priv_escalated`). | `whoami /priv && accesschk -accepteula -uwcqv *` |
| `find / -writable -type f \( -path "/etc/*" -o -path "/usr/*" -o -path "/opt/*" -o -path "/var/spool/cron/*" \) 2>/dev/null` | **Linux Bash** | Finds misconfigured world- or group-writable config files, service units, and scripts across system directories. | Apply to detect writable `/etc/passwd`, `/etc/systemd/system/*.service`, or cron jobs executed by root. | `accesschk -accepteula -uwqv "Users" C:\Windows\*` |
| `journalctl -xe --no-pager -n 100 && sudo grep -E "Accepted\|Failed\|sudo\|session opened" /var/log/auth.log /var/log/secure 2>/dev/null \| tail -n 50` | **Linux Bash** | Queries `systemd-journald` and `rsyslog` auth logs (`auth.log` on Debian/Ubuntu, `secure` on RHEL/CentOS) (`[[commands/trained_logging-cmds]]`). | Apply when auditing SSH logins, `sudo` usage, or service startup failures. | `wevtutil qe Security /c:30 /rd:true /f:text` |
| `python3 -c 'import pty; pty.spawn("/bin/bash")' \|\| script -qc /bin/bash /dev/null` | **Linux Bash** | Allocates a kernel pseudo-terminal (`PTY`) to upgrade a non-interactive netcat/reverse shell into a full interactive TTY (`[[knowledge/trained_upgrading_shells_to_fully_interactive_ttys]]`). | Apply whenever `sudo`, `su`, `ssh`, or `vim` fails with `standard in must be a tty` or `no tty present`. | `Enter-PSSession` |
| `uname -a; showrev -p; ifconfig -a; netstat -rn; ps -ef; svcs -a` | **Solaris / UNIX** | Solaris (`SunOS`) system, patch (`showrev -p`), interface (`ifconfig -a`), routing (`netstat -rn`), and SMF service (`svcs -a`) survey (`[[commands/trained_solaris-survey]]`). | Apply when operating on legacy Solaris / SunOS UNIX enterprise servers. | `systeminfo && ipconfig /all && sc query` |

### Copy-Pasteable Execution Block (Windows & Linux)
```bash
# [Linux Bash] Collects kernel version, architecture, OS distribution, hostname, system load, and current user UID/GID/groups (`[[commands/trained_centos-debian-survey]]`).
uname -a; cat /etc/os-release; hostnamectl; uptime; id
# [Linux Bash] Displays full process tree (`--forest`), UID, PID, PPID, start timestamp, and full command line (`[[commands/trained_cqc001_e050_m050_process_and_signals]]`).
ps auxef && ps -eo pid,ppid,user,stat,lstart,args --forest
# [Linux Bash] Inspects the live kernel `/proc/<PID>` binary link (`exe`), working directory (`cwd`), open descriptors (`fd`), and environment variables (`environ`).
sudo ls -la /proc/<PID>/exe /proc/<PID>/cwd /proc/<PID>/fd && tr '\0' '\n' < /proc/<PID>/environ
# [Linux Bash] Lists all active `systemd` services and scheduled timers (`[[commands/trained_cqc001_e050_m040_boot_init_login]]`).
systemctl list-units --type=service --state=running && systemctl list-timers --all
# [Linux Bash] Lists mounted filesystems with filesystem type (`ext4`, `xfs`, `tmpfs`), block device hierarchy, UUIDs, and mount flags (`noexec`, `nosuid`) (`[[knowledge/trained_cqc001_e050_m030_filesystems]]`).
df -hT && lsblk -f && findmnt
# [Linux Bash] Audits allowed `sudo` commands, SUID root binaries (`-perm -4000`), and POSIX file capabilities (`getcap -r /`) (`[[commands/trained_cqc001_e060_m010_users_and_permissions]]`).
sudo -l && find / -perm -4000 -type f -exec ls -la {} + 2>/dev/null && getcap -r / 2>/dev/null
```
<!-- CORA-MAXIMIZED-COMMANDS-END -->
