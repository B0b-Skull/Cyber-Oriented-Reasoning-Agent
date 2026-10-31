---
title: "Trained Knowledge & Topology: Solaris-Survey"
category: knowledge
domain_hub: "[[knowledge/06_linux_unix_administration_processes_and_logging]]"
os_platform: linux
primary_tactic: Passive_Enum
summary: "Operational architecture, decision workflows & Windows/Linux command reference for Solaris-Survey: Linux (Debian/Ubuntu/CentOS/RHEL) and UNIX/Solaris system administration, kernel /proc & sysctl internals, ext4/xfs/procfs filesys"
when_to_apply: "Apply when working with Solaris-Survey (linux): Apply when enumerating a Linux/UNIX/Solaris host, inspecting `/proc/<PID>` or kernel modules, auditing mounted filesystems (`findmnt`/`lsblk`), managing `systemd` services or signals, hunting SUID/SGID/Capabilities/sudo privilege escalation vectors, reviewing `/var/log`/`journalctl` logs, or upgrading a dumb shell to a full interactive TTY."
tags: [arp, credential_access, defense_evasion_firewall, enumeration, https, mdp, netstat, passive_enum, post_exploitation_verification, privilege_escalation, ssh, text, trained, linux, unix, solaris, systemctl, journalctl, lsof, strace, findmnt, lsblk]
source_file: "Solaris-Survey"
updated: 2026-10-30
---

# Trained Knowledge & Architecture: `Solaris-Survey.txt`

- **Source Path:** `~/Projects/CORA/Training/Solaris-Survey.txt` (`text`)
- **Extracted Technical Entities:** `arp, https, netstat, ssh`
- **Extracted IPs / Subnets:** `None`
- **Extracted Interfaces:** `None`
- **Linked Command Playbook:** [[commands/trained_solaris-survey]] (`71` CEGAR-verified commands | `71` MDP transitions)

## Command & Tactic Coverage Summary
- **Total CEGAR-Verified Commands:** `71` (full executable list in [[commands/trained_solaris-survey]])
- **Tactic Distribution:** `Passive_Enum` (39), `Privilege_Escalation` (15), `Defense_Evasion_Firewall` (8), `Enumeration` (4), `Post_Exploitation_Verification` (3), `Credential_Access` (2)
- **Top Extracted CLI Tools:** `cat` (11), `ls` (6), `chmod` (5), `find` (5), `ps` (4), `crontab` (3), `grep` (3), `netstat` (3), `pfiles` (3), `chown` (2), `df` (2), `fuser` (2), `arp` (1), `chgrp` (1), `cp` (1), `date` (1), `groups` (1), `inetadm` (1), `ipfstat` (1), `locate` (1), `modinfo` (1), `ping` (1), `psrinfo` (1), `ptree` (1), `rpcinfo` (1)

## Extracted Reference Excerpt
Solaris

Solaris 10+ = SMF 
Solaris <9  = SysVinit
=======================================================================================================
System Identification
	date
	uname -a
	w 
	psrinfo -v
	uptime
	sysdef -h
	modinfo -c | grep ' LOADED' | more		:Shows loaded kernel modules
	vmstat									:Memory level for virtual environment
	who -r 									:Current run level
=======================================================================================================
Locate Files
	find . -mtime $(date +%s -d"Aug 10, 2013 23:59:59") -mtime $(date +%s -d"Aug 1, 2013 23:59:59")			:Finds files between a set of dates
	find / -type f -name ".*" | grep <username>			:Searches for all hidden files in usernames folders
	find / -type d -name ".*" | grep <username>			:Searches for hidden directories with user name in them
	find . -mtime $(date +%s -d"Aug 10, 2013 23:59:59") -mtime $(date +%s -d"Aug 1, 2013 23:59:59")								:Find files between two dates
	find ~/ -mtime $(echo $(date +%s) - $(date +%s -d"Dec 31, 2009 23:59:59") | bc -l | awk '{print $1 / 86400}' | bc -l)		:Find files before specific date 
=======================================================================================================
Port and Process ENUMERATION
	ps -efj | grep 711 							:Shows where PID 711 is exectuting from
	ps -efj | grep ssh							:searches process list for ssh 
	ps -ajf
	fuser . 									:Shows contents of folder being accessed by what processes
	fuser /folder/location 22/tcp 				:Shows contents of folder using port 22 with protocol tcp
	ptree <PID>
*   pfiles `ls /proc` 2>/dev/null | awk "/^ [^ \\t]/{smatch=\$0;next}/port:[ \\t]*${1}/{print smatch, \$0}{next}"		:Solaris - finds ports and associates with PIDs
*	ps -ef| awk '{print $2}'| xargs -I '{}' sh -c 'echo Examining process: {}; pfiles {}| grep "port: *"'				:Solaris - finds ports and pids, can specify port.
	pfiles <PID> | grep AF_INET				:Solaris - Shows all ports that PID is associated with 
	pfiles /proc/* 							:Solaris - Display list of services running
	rpcinfo -p 
=======================================================================================================
Find files with SUID bit set 
	find / -perm -u=s 2>/dev/null | xargs ls -la | more 
	grep ops.local `find /etc -name \*.conf`		:CSH - Searches contents of all files in /etc that end in ".conf" and contain the string "ops.local"
	grep ops.local $(find /etc -name '*.conf')		:BASH - Searches contents of all files in /etc that end in ".conf" and contain the string "ops.local"
	grep 'This I\$ Y\*ur File' /root/* 				:Searches all folders/directories in /root/ for the string indicated.
=======================================================================================================
Time Stamps
	stat /tmp
	ls -al /tmp 
	ls -

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
