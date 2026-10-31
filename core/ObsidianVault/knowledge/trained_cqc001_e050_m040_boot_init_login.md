---
title: "Trained Knowledge & Topology: CQC001 E050 M040 Boot Init Login"
category: knowledge
domain_hub: "[[knowledge/06_linux_unix_administration_processes_and_logging]]"
os_platform: linux
primary_tactic: Passive_Enum
summary: "Operational architecture, decision workflows & Windows/Linux command reference for CQC001 E050 M040 Boot Init Login: Linux (Debian/Ubuntu/CentOS/RHEL) and UNIX/Solaris system administration, kernel /proc & sysctl internals, ext4/xfs/procfs filesys"
when_to_apply: "Apply when working with CQC001 E050 M040 Boot Init Login (linux): Apply when enumerating a Linux/UNIX/Solaris host, inspecting `/proc/<PID>` or kernel modules, auditing mounted filesystems (`findmnt`/`lsblk`), managing `systemd` services or signals, hunting SUID/SGID/Capabilities/sudo privilege escalation vectors, reviewing `/var/log`/`journalctl` logs, or upgrading a dumb shell to a full interactive TTY."
tags: [http, https, mdp, pdf, trained, linux, unix, solaris, systemctl, journalctl, lsof, strace, findmnt, lsblk, sysctl, chmod, chown, sudo, getcap, suid, find, grep]
source_file: "CQC001 E050 M040 Boot Init Login"
updated: 2026-10-30
---

# Trained Knowledge & Architecture: `CQC001_E050_M040_Boot_Init_Login.pdf`

- **Source Path:** `~/Projects/CORA/Training/CQC001_E050_M040_Boot_Init_Login.pdf` (`pdf`)
- **Extracted Technical Entities:** `http, https`
- **Extracted IPs / Subnets:** `None`
- **Extracted Interfaces:** `None`

## LLM Distilled Operational Summary
### Key Operational Techniques & Decision Workflows

*   **Boot Process Analysis**: Understand the boot sequence to determine process initiation triggers and implement application persistence (ensuring processes restart after a reboot).
*   **Runlevel Management**: Recognize that runlevels drive program execution via initialization scripts. Note that some `/etc/inittab` lines execute regardless of runlevel, while others are runlevel-specific.
*   **Service State vs. Startup Configuration**:
    *   Use `service <name> <start|stop|status>` to manage the *current runtime state* of a service.
    *   Use `chkconfig` to modify `/etc/rc.d` directories, affecting which services run at *startup* without changing the immediate running state.
*   **Manual File Management**: Be prepared to manually edit configuration files, as automated tools vary between UNIX versions and Linux distributions.

### Critical Command Patterns and Required Flags

*   **Service Control**: `service [service_name] [start|stop|restart|status]`
*   **Startup Configuration**: `chkconfig [service_name] [on|off]` (or `--level <runlevel>`)
*   **Documentation Lookup**:
    *   Manual pages: `[Topic] man page`
    *   RFCs: `RFC [RFC NUMBER]`

### Network Topology & Service Relationships

*   **Initialization Scripts**: Services interact with scripts located in `/etc/rc.d/init.d`.
*   **Configuration Files**:
    *   `/etc/inittab`: Contains lines processed at boot or regardless of runlevel.
    *   `/etc/rc.d`: Directory modified by `chkconfig` to define startup behaviors.
*   **Hardware/Partition Context**:
    *   **Master Boot Record (MBR)**: Defines the initial layout for booting.
    *   **Disk Partitions**: Critical for understanding where initialization scripts and services reside.
*   **Distribution Variance**: While core concepts apply, specific management tools and runlevel behaviors differ across UNIX versions and Linux distributions.

<!-- CORA-MAXIMIZED-COMMANDS-START -->
## Maximized Windows & Linux Command Examples for `CQC001 E050 M040 Boot Init Login`

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
