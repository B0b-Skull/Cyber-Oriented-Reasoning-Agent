---
title: "Trained Knowledge & Topology: CentOS-Debian-Survey"
category: knowledge
domain_hub: "[[knowledge/06_linux_unix_administration_processes_and_logging]]"
os_platform: linux
primary_tactic: Passive_Enum
summary: "Operational architecture, decision workflows & Windows/Linux command reference for CentOS-Debian-Survey: Linux (Debian/Ubuntu/CentOS/RHEL) and UNIX/Solaris system administration, kernel /proc & sysctl internals, ext4/xfs/procfs filesys"
when_to_apply: "Apply when working with CentOS-Debian-Survey (linux): Apply when enumerating a Linux/UNIX/Solaris host, inspecting `/proc/<PID>` or kernel modules, auditing mounted filesystems (`findmnt`/`lsblk`), managing `systemd` services or signals, hunting SUID/SGID/Capabilities/sudo privilege escalation vectors, reviewing `/var/log`/`journalctl` logs, or upgrading a dumb shell to a full interactive TTY."
tags: [active_enum, arp, credential_access, defense_evasion_firewall, enumeration, eth0, eth1, https, iptables, john, mdp, netstat, passive_enum, post_exploitation_verification, privilege_escalation, ssh, text, trained, linux, unix, solaris, systemctl]
source_file: "CentOS-Debian-Survey"
updated: 2026-10-30
---

# Trained Knowledge & Architecture: `CentOS-Debian-Survey.txt`

- **Source Path:** `~/Projects/CORA/Training/CentOS-Debian-Survey.txt` (`text`)
- **Extracted Technical Entities:** `arp, eth0, eth1, https, iptables, john, netstat, ssh`
- **Extracted IPs / Subnets:** `10.10.10.10/24, 10.18.80.64/26, 172.24.11.0/24, 172.24.11.13, 172.24.111.112/29, 172.24.2.2/24`
- **Extracted Interfaces:** `eth0, eth1`
- **Linked Command Playbook:** [[commands/trained_centos-debian-survey]] (`182` CEGAR-verified commands | `182` MDP transitions)

## Command & Tactic Coverage Summary
- **Total CEGAR-Verified Commands:** `182` (full executable list in [[commands/trained_centos-debian-survey]])
- **Tactic Distribution:** `Passive_Enum` (93), `Defense_Evasion_Firewall` (43), `Enumeration` (19), `Privilege_Escalation` (13), `Post_Exploitation_Verification` (7), `Credential_Access` (6), `Active_Enum` (1)
- **Top Extracted CLI Tools:** `ls` (29), `iptables` (24), `find` (15), `cat` (13), `netstat` (7), `chmod` (5), `ps` (5), `df` (4), `echo` (4), `grep` (4), `last` (4), `lsof` (4), `chkconfig` (3), `dd` (3), `ip` (3), `mount` (3), `tar` (3), `arp` (2), `auditctl` (2), `ausearch` (2), `chown` (2), `dpkg` (2), `egrep` (2), `ip6tables` (2), `kill` (2)

## Extracted Reference Excerpt
CentOS - Debian Survey

Sysvinit
=======================================================================================================
Initial CMDs
	w						:Displays uptime and any users logged on with TTY
	date					:Displays local zulu time of when the target was accessed
	uptime 					:Displays system uptime since last shutdown/reboot/poweroff
	id						:Shows user id, group id, GID, UID
	uname -a				:Displays info about kernel and processor
	hostname
	sestatus				:Shows status of SELinux on target		- Look in /etc/selinux/config 
=======================================================================================================
Kernel Modules
	rmmod power_meter		:Removes modudle "power_meter" if not running or loaded in kernel
	modinfo dm_zero			:Shows kernel module dm_zero
	insmod
	lsmod 					:Show status of modules in kernel 
	sysctl -a				:Linux - displays all kernel parameters set in current running configuration
=======================================================================================================
View Process and Network info
	ps -ef --sort start_time	:Displays process list by start time 
	ps -elf 					:Use this if above CMD doesn't work
	ps auxwww					:Same as above
	ps -axjf
	netstat -natup				:Displays all TCP and UDP network sockets. The -p option may log if you are not root
	netstat -rn					:Displays routing table
	arp -v						:Displays current ARP cache
	df -h 						:Dsiplays system hard drive utilization
	df -i 						:Displays system inode utilization
	sudo ls -l /proc/<pid>/exe	:Linux - Searches where binary is loaded from 
	cat /etc/services | grep <port>
	strace <name>				:Traces execution of program in memory 
		Example: strace -o /tmp/strace.txt cat group passwd
=======================================================================================================
ID system with cron jobs - Could potentially be logged
	ls -latrd /etc/cron*						:List all cron directories including cron.hourly and cron.daily - We want to inspect the content of these files
	ls -latr /var/spool/cron /var/spool/at		:Lists additional locations for con and at jobs - We want to inspect the content of these files
	ls -latr /root
	ls -latr /home/*
	ls -latr /export/home/*
	less <user_path>/.bash_history			:Displays user command history
	less <user_path>/.history				:Displays user command history
	ls -latr /tmp							:Displays contents of /tmp directory
	ls -latr /								:Displays contents of root directory
=======================================================================================================
Startup Scripts & Cron Jobs
	crontab -l <username>						:Verify crontab for user 
	ls -l /var/spool/cron/crontabs 				:Verify crontabs exist
	cat /var/spool/cron/crontabs/<name>			:View cron jobs for that user or set to run at sta

<!-- CORA-MAXIMIZED-COMMANDS-START -->
## Maximized Windows & Linux Command Examples for `CentOS-Debian-Survey`

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
