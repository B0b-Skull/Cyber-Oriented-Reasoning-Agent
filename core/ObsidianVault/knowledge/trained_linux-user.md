---
title: "Trained Knowledge & Topology: linux-user"
category: knowledge
domain_hub: "[[knowledge/06_linux_unix_administration_processes_and_logging]]"
os_platform: linux
primary_tactic: Passive_Enum
summary: "Operational architecture, decision workflows & Windows/Linux command reference for linux-user: Linux (Debian/Ubuntu/CentOS/RHEL) and UNIX/Solaris system administration, kernel /proc & sysctl internals, ext4/xfs/procfs filesys"
when_to_apply: "Apply when working with linux-user (linux): Apply when enumerating a Linux/UNIX/Solaris host, inspecting `/proc/<PID>` or kernel modules, auditing mounted filesystems (`findmnt`/`lsblk`), managing `systemd` services or signals, hunting SUID/SGID/Capabilities/sudo privilege escalation vectors, reviewing `/var/log`/`journalctl` logs, or upgrading a dumb shell to a full interactive TTY."
tags: [adb, arp, credential_access, enumeration, eth0, http, https, john, lateral_movement_routing_pivot, mdp, out-of-band_access, passive_enum, pdf, post_exploitation_verification, privilege_escalation, reconnaissance, serial, ssh, trained, ttyusb0, ttyusb1, linux]
source_file: "linux-user"
updated: 2026-10-30
---

# Trained Knowledge & Architecture: `linux-user.pdf`

- **Source Path:** `~/Projects/CORA/Training/linux-user.pdf` (`pdf`)
- **Extracted Technical Entities:** `adb, arp, eth0, http, https, john, serial, ssh, ttyusb0, ttyusb1`
- **Extracted IPs / Subnets:** `0.0.0.0/0, 127.0.0.1, 172.24.0.0/16`
- **Extracted Interfaces:** `eth0, ttyACM0, ttyACM1, ttyUSB0, ttyUSB1`
- **Linked Command Playbook:** [[commands/trained_linux-user]] (`136` CEGAR-verified commands | `136` MDP transitions)

## Command & Tactic Coverage Summary
- **Total CEGAR-Verified Commands:** `136` (full executable list in [[commands/trained_linux-user]])
- **Tactic Distribution:** `Enumeration` (101), `Lateral_Movement_Routing_Pivot` (13), `Passive_Enum` (12), `Post_Exploitation_Verification` (4), `Out-of-Band_Access` (2), `Privilege_Escalation` (2), `Credential_Access` (1), `Reconnaissance` (1)
- **Top Extracted CLI Tools:** `echo` (53), `mount` (7), `git` (6), `cat` (5), `gdb` (5), `mkdir` (5), `modprobe` (4), `unset` (4), `dd` (3), `insmod` (3), `umount` (3), `chmod` (2), `export` (2), `gzip` (2), `type` (2), `applet.html` (1), `application.jar` (1), `config` (1), `cut` (1), `defaults` (1), `file` (1), `find` (1), `gcc` (1), `get_maintainer.pl` (1), `handle` (1)

### Visual & Network Diagram Intelligence (`linux-user.pdf#page2`)

### Visual & Network Diagram Intelligence (`linux-user.pdf#page6`)
- **Spatially Grouped Diagram Nodes (Box/Component Clusters):**
  1. `[Linux Kernel User Documentation, Release 4.13.0-rc4+]`
  2. `[2]`
  3. `[CONTENTS]`

## LLM Distilled Operational Summary
### Key Operational Techniques & Decision Workflows
- **Source Installation Location**: Always extract kernel source tarballs into a dedicated directory (e.g., `~/src`) with write permissions. Avoid `/usr/src/linux` to prevent conflicts with system library headers.
- **Upgrade Workflow**: For 4.x releases, apply incremental patches sequentially using the `patch -p1` command. Clean up backup files (`.~`, `.orig`) and check for failures (`.#`, `.rej`) after each patch.
- **Documentation Strategy**: Consult `Documentation/00-INDEX` for driver-specific notes and `Documentation/process/changes.rst` to assess upgrade risks before applying new kernel versions.

### Critical Command Patterns & Required Flags
- **Extract Kernel Source**:
  ```bash
  xz -cd linux-4.X.tar.xz | tar xvf -
  ```
  *Flag Note*: `xz -cd` decompresses and pipes directly to `tar`, avoiding intermediate files.
- **Apply Patches**:
  ```bash
  xz -cd ../patch-4.x.xz | patch -p1
  ```
  *Flag Note*: `-p1` specifies the path strip level for patch application.

### Network Topology & Service Relationships
- **Architecture Support**: The kernel supports multi-stack networking including **IPv4 and IPv6**, running across diverse architectures (x86, ARM, PowerPC, etc.) provided a paged memory management unit (PMMU) and GCC are present.
- **UserMode Linux (UML)**: A unique topology where the kernel runs as a userspace application, enabling virtualization without dedicated hardware.
- **Release Resources**: Primary release notes and patch distributions are hosted at `http://kernel.org/`.

## Document Structure & Key Topics
- Visual & Network Diagram Intelligence (`linux-user.pdf#page2`)
- Visual & Network Diagram Intelligence (`linux-user.pdf#page6`)
- add string1
- remove string2
- remove all strings
- disable all built-in OS vendor
- enable all built-in OS vendor
- disable all strings
- Current version is bad
- reboot -f
- filename:lineno [module]function flags format
- mknod /dev/initrd b 1 250
- mke2fs -F -m0 initrd
- mknod /mnt/dev/console c 5 1
- chroot /mnt /sbin/init
- pivot_root . initrd
- exec chroot . what-follows <dev/console >dev/console 2>&1
- blockdev --flushbufs /dev/ram0
- Insert BINFMT_MISC module into the kernel
- Some distributions, like Fedora Core, perform
- the following command automatically when the
- binfmt_misc module is loaded into the kernel
- or during normal boot up (systemd-based systems).
- Thus, it is possible that the following line
- is not needed at all.
- Register support for .NET CLR binaries
- Replace /usr/bin/mono with the correct pathname to
- the Mono CLR runtime (usually /usr/local/bin/mono
- when compiling from sources or CVS).
- /usr/local/bin/javawrapper - the wrapper for binfmt_misc/java
- for example:
- CLASS=Test.class
- FQCLASS=foo.bar.Test
- FQCLASSN=Test
- FQCLASSP=foo/bar
- See if this directory works straight off
- Try dereferencing the directory name
- If no other possible filename exists
- Go down one more level of symbolic links
- class is not in CLASSPATH, so prepend dir of class to CLASSPATH
- /usr/local/java/bin/jarwrapper - the wrapper for binfmt_misc/jar
- cat trace
- tracer: function
- / _----=> need-resched
- | / _---=> hardirq/softirq
- || / _--=> preempt-depth
- ||| /
- TASK-PID
- | |
- key=$(openssl rand -hex 32)
- attr -S -s SMACK64 -V "value" path
- chsmack -a value path

## Extracted Operational Steps & Workflows
- 1. `acpi_osi=! acpi_osi=''Windows 2000''' is equivalent
- 1. `acpi_osi=' can make `CondRefOf(_OSI, Local1)'
- 1. `acpi_osi=''Module Device'' acpi_osi=!*' can make
- 2. `acpi_osi=!* acpi_osi=''Module Device''' can make
- 3. `acpi_osi=! acpi_osi=!* acpi_osi=''Windows 2000''' is
- 1. Resume from suspend/hibernate depends on CPU0.
- 2. PIC interrupts also depend on CPU0. CPU0 can't be
- 1. The symbolic link name, if any (/var/lock/LCK..modem)
- 2. The “tty” name (/var/lock/LCK..ttyS2)
- 3. The alternate device name (/var/lock/LCK..cua2)
- 1. Hand copy the text from the screen and type it in after the machine has restarted. Messy but it is the
- 2. Boot with a serial console (see Documentation/admin-guide/serial-console.rst ), run a null modem
- 3. Use Kdump (see Documentation/kdump/kdump.txt), extract the kernel ring buﬀer from old memory
- 1. ‘G’ if all modules loaded have a GPL or compatible license, ‘P’ if any proprietary module has
- 2. F if any module was force loaded by insmod -f, ' ' if all modules were loaded normally.
- 3. S if the oops occurred on an SMP kernel running on hardware that hasn’t been certiﬁed as
- 4. R if a module was force unloaded by rmmod -f, ' ' if all modules were unloaded normally.
- 5. M if any processor has reported a Machine Check Exception, ' ' if no Machine Check Ex-
- 6. B if a page-release function has found a bad page reference or some unexpected page ﬂags.
- 7. U if a user or user application speciﬁcally requested that the Tainted ﬂag be set, ' ' other-
- 8. D if the kernel has died recently, i.e. there was an OOPS or BUG.
- 9. A if the ACPI table has been overridden.
- 10. W if a warning has previously been issued by the kernel. (Though some warnings may set
- 11. C if a staging driver has been loaded.
- 12. I if the kernel is working around a severe bug in the platform ﬁrmware (BIOS or similar).
- 13. O if an externally-built (“out-of-tree”) module has been loaded.
- 14. E if an unsigned module has been loaded in a kernel supporting module signature.
- 15. L if a soft lockup has previously occurred on the system.
- 16. K if the kernel has been live patched.
- 1. parameters given via /etc/modprobe.d/*.conf:
- 2. foo.dyndbg as given in boot args, foo. is stripped and passed:
- 3. args to modprobe:
- 1. Unable to mount root FS
- 2. init binary doesn’t exist on rootfs
- 3. broken console device
- 4. binary exists but dependencies not available
- 5. binary cannot be loaded
- 1. Set “debug” kernel parameter (in bootloader conﬁg ﬁle or CONFIG_CMDLINE) to get more detailed
- 2. make sure you have the correct root FS type (and root= kernel parameter points to the correct
- 3. Possibly a conﬂict in console= setup –> initial console unavailable. E.g. some serial consoles are
- 4. e.g. required library dependencies of the init binary such as /lib/ld-linux.so.2 missing or broken.
- 5. make sure the binary’s architecture matches your hardware. E.g. i386 vs. x86_64 mismatch, or
- 1. the boot loader loads the kernel and the initial RAM disk
- 2. the kernel converts initrd into a “normal” RAM disk and frees the memory used by initrd
- 3. if the root device is not /dev/ram0, the old (deprecated) change_root procedure is followed. see the

<!-- CORA-MAXIMIZED-COMMANDS-START -->
## Maximized Windows & Linux Command Examples for `linux-user`

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
