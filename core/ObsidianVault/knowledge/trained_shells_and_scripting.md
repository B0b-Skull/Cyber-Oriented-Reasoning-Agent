---
title: "Trained Knowledge & Topology: Shells and Scripting"
category: knowledge
domain_hub: "[[knowledge/06_linux_unix_administration_processes_and_logging]]"
os_platform: linux
primary_tactic: Passive_Enum
summary: "Operational architecture, decision workflows & Windows/Linux command reference for Shells and Scripting: Linux (Debian/Ubuntu/CentOS/RHEL) and UNIX/Solaris system administration, kernel /proc & sysctl internals, ext4/xfs/procfs filesys"
when_to_apply: "Apply when working with Shells and Scripting (linux): Apply when enumerating a Linux/UNIX/Solaris host, inspecting `/proc/<PID>` or kernel modules, auditing mounted filesystems (`findmnt`/`lsblk`), managing `systemd` services or signals, hunting SUID/SGID/Capabilities/sudo privilege escalation vectors, reviewing `/var/log`/`journalctl` logs, or upgrading a dumb shell to a full interactive TTY."
tags: [credential_access, enumeration, http, https, mdp, passive_enum, pdf, trained, linux, unix, solaris, systemctl, journalctl, lsof, strace, findmnt, lsblk, sysctl, chmod, chown, sudo, getcap]
source_file: "Shells and Scripting"
updated: 2026-10-30
---

# Trained Knowledge & Architecture: `Shells_and_Scripting.pdf`

- **Source Path:** `~/Projects/CORA/Training/Shells_and_Scripting.pdf` (`pdf`)
- **Extracted Technical Entities:** `http, https`
- **Extracted IPs / Subnets:** `None`
- **Extracted Interfaces:** `None`
- **Linked Command Playbook:** [[commands/trained_shells_and_scripting]] (`8` CEGAR-verified commands | `8` MDP transitions)

## Command & Tactic Coverage Summary
- **Total CEGAR-Verified Commands:** `8` (full executable list in [[commands/trained_shells_and_scripting]])
- **Tactic Distribution:** `Enumeration` (6), `Credential_Access` (1), `Passive_Enum` (1)
- **Top Extracted CLI Tools:** `echo` (5), `cat` (1), `erase` (1), `history` (1)

## LLM Distilled Operational Summary
### Operational Techniques & Decision Workflows

*   **File I/O & Redirection**: Use `>` for output redirection, `<` for input redirection, and `>>` for appending. Combine stdout and stderr using `>file 2>&1` or `>&file`.
*   **Process Management**: Launch background processes with `&`, resume them with `fg`, list active jobs via `jobs`, and terminate with `kill`. Use `bg` to resume a job in the background and `wait` to synchronize completion.
*   **Shell Execution & Environment**: Execute commands in a subshell using `( )`, run a new shell with `exec`, and source files using `. file` or `source file`. Manage environment variables with `export` and unset them with `unset`.
*   **Loop Control**: Terminate loops with `break` (bash/ksh) or `end` (tcsh), and skip iterations with `continue`.
*   **Conditional Logic**: Evaluate conditions using `[ expression ]` or the preferred `[[ expression ]]` syntax for grouping and operator precedence. Use `&&` and `||` for logical AND/OR operations.

### Critical Command Patterns & Required Flags

*   **Variable Expansion**:
    *   Simple: `$VAR` or `${VAR}`
    *   Indirection: `${!VAR}`
    *   Default/Alternate: `${VAR:-default}` or `${VAR+alt}`
    *   Error on Null: `${VAR:?msg}`
    *   Substring/Removal: `${VAR#pattern}`, `${VAR%pattern}`
*   **String Manipulation**:
    *   Length: `${#VAR}`
    *   Slice: `${VAR:offset:length}`
    *   Replace: `${VAR/pattern/replacement}` (single) or `${VAR//pattern/replacement}` (all).
    *   Case Change: `${VAR^}` (first char), `${VAR^^}` (all upper), `${VAR,}` (first lower), `${VAR,,}` (all lower).
*   **Bash Specifics**:
    *   Grouping: `( expr )`
    *   Logical Ops: `expr1 && expr2`, `expr1 || expr2`
    *   Pattern Matching: `STRING == PATTERN`, `STRING != PATTERN`, `STRING =~ ERE`

### Network Topology & Service Relationships

*   **Directory Navigation**: Switch directories using `cd`, `cd ~-` (previous), and `popd/pushd` (stack-based).
*   **Command History & Editing**: List history with `history`, redo last command with `!!` or `fc -s`, and edit/redo specific commands with `fc -s str` or `!str`.
*   **Alias & Hashing**: Define aliases with `alias x=y`, display hashed commands with `hash`, and reset locations with `hash -r` or `unhash`.
*   **Resource Limits**: Set limits using `ulimit` (bash/ksh) or `limit` (tcsh).
*   **Input/Interrupt Handling**: Read from stdin with `read`, ignore interrupts via `trap INTR`, and handle signals with `onintr` (tcsh).

## Document Structure & Key Topics
- Background execution
- write the string “1234567890” to file output.txt
- open “output.txt” and assign fd 3 to it
- read 4 characters from open file with file descriptor (fd) 3. File
- write a decimal point at the file pointer position
- close fd 3
- output on the screen will be: 1234.67890

<!-- CORA-MAXIMIZED-COMMANDS-START -->
## Maximized Windows & Linux Command Examples for `Shells and Scripting`

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
