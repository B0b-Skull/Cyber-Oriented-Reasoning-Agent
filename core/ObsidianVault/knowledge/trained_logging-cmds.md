---
title: "Trained Knowledge & Topology: Logging-CMDs"
category: knowledge
domain_hub: "[[knowledge/06_linux_unix_administration_processes_and_logging]]"
os_platform: linux
primary_tactic: Passive_Enum
summary: "Operational architecture, decision workflows & Windows/Linux command reference for Logging-CMDs: Linux (Debian/Ubuntu/CentOS/RHEL) and UNIX/Solaris system administration, kernel /proc & sysctl internals, ext4/xfs/procfs filesys"
when_to_apply: "Apply when working with Logging-CMDs (linux): Apply when enumerating a Linux/UNIX/Solaris host, inspecting `/proc/<PID>` or kernel modules, auditing mounted filesystems (`findmnt`/`lsblk`), managing `systemd` services or signals, hunting SUID/SGID/Capabilities/sudo privilege escalation vectors, reviewing `/var/log`/`journalctl` logs, or upgrading a dumb shell to a full interactive TTY."
tags: [defense_evasion_firewall, enumeration, mdp, netstat, passive_enum, post_exploitation_verification, reconnaissance, text, trained, linux, unix, solaris, systemctl, journalctl, lsof, strace, findmnt, lsblk, sysctl, chmod, chown, sudo]
source_file: "Logging-CMDs"
updated: 2026-10-30
---

# Trained Knowledge & Architecture: `Logging-CMDs.txt`

- **Source Path:** `~/Projects/CORA/Training/Logging-CMDs.txt` (`text`)
- **Extracted Technical Entities:** `netstat`
- **Extracted IPs / Subnets:** `172.24.11.13`
- **Extracted Interfaces:** `None`
- **Linked Command Playbook:** [[commands/trained_logging-cmds]] (`27` CEGAR-verified commands | `27` MDP transitions)

## Command & Tactic Coverage Summary
- **Total CEGAR-Verified Commands:** `27` (full executable list in [[commands/trained_logging-cmds]])
- **Tactic Distribution:** `Passive_Enum` (14), `Defense_Evasion_Firewall` (6), `Enumeration` (3), `Reconnaissance` (3), `Post_Exploitation_Verification` (1)
- **Top Extracted CLI Tools:** `ps` (3), `auditctl` (2), `cat` (2), `sed` (2), `service` (2), `tail` (2), `aureport` (1), `ausearch` (1), `dmesg` (1), `echo` (1), `id` (1), `logger` (1), `ls` (1), `lsof` (1), `netstat` (1), `sestatus` (1), `setenforce` (1), `svcadm` (1), `svcs` (1), `vi` (1)

## Extracted Reference Excerpt
Unix Logging

ps -ef | grep syslog				:Shows type of syslog being used
ls /etc/syslog*						:Shows all files in /etc that begin with syslog
=======================================================================================================
/etc/syslong.conf					:Config file for syslogs
/var/adm/sulog						:SU command has its own log location
=======================================================================================================
Configure linux to be a syslog server and receive syslog messages
	vi /etc/sysconfig/syslog			:edit syslog file 
		SYSLOGD_OPTIONS="-m 0 -r"		:Modify this line to start remote server capabilities
	service syslog restart				:Restarts syslog service
	netstat -ulnp						:Verifies system is listening on UDP port 514
=======================================================================================================
Configure Solaris to send syslog info
	/etc/hosts
	echo 172.24.11.13 linux.ops.local loghost >> /etc/hosts		:appends the info to the /etc/hosts file to send log info currently configured to go to /var/log/syslog to another logging server named "linux.ops.local"
	svcadm restart system/system-log								:restarts syslog process
=======================================================================================================
Testing log setup
	On Solaris or remote server
		logger -p auth.notice tst msg			:Need to create a message that logs to LOGHOST as defined in /etc/syslog.conf. Facility "auth" and priority "notice" will do this
	On Linux local server
		tail /var/log/messages					:Will show the last message received by the server. 
=======================================================================================================
svcs utmp									:Starts utmpd daemon to track logs for /var/adm/wtmpx and /var/adm/utmpx
cat /var/adm/messages | grep Copyright		:Solaris, SunOS and Copyright are always right after a reboot. Also try "ID 540533 kern.notice" and "ID 218167 kern.notice"
cat /var/log/authlog | grep console			:This log file shows console logon
dmesg										:Very close as reading directly from /var/adm/messages as dmesg reads directly from /var/adm/messages*
=======================================================================================================
ps -C auditd				:Displays only the PID for the audit daemon
id daemon					:Displays uid and gid of daemon process
ps awx|grep auditd			:Displays all PIDs where auditd is used
lsof -p <PID>				:List of open files only for a specific PID
tail -n2 /var/log/messages	:Shows last two logs from /var/log/messages file
=======================================================================================================
Log locations
	Linux
		/var/log/utmp		:Shows user logins,logouts,system boot time, system events
		/var/log/wtm

<!-- CORA-MAXIMIZED-COMMANDS-START -->
## Maximized Windows & Linux Command Examples for `Logging-CMDs`

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
