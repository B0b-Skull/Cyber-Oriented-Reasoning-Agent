---
title: "Trained Command Playbook: linux-user"
category: commands
domain_hub: "[[knowledge/06_linux_unix_administration_processes_and_logging]]"
os_platform: linux
primary_tactic: Passive_Enum
summary: "Verified Windows & Linux command playbook for linux-user (Passive_Enum): Linux (Debian/Ubuntu/CentOS/RHEL) and UNIX/Solaris system administration, kernel /proc & sysctl internals, ext4/xfs/procfs filesystems,"
when_to_apply: "Apply when working with linux-user (linux): Apply when enumerating a Linux/UNIX/Solaris host, inspecting `/proc/<PID>` or kernel modules, auditing mounted filesystems (`findmnt`/`lsblk`), managing `systemd` services or signals, hunting SUID/SGID/Capabilities/sudo privilege escalation vectors, reviewing `/var/log`/`journalctl` logs, or upgrading a dumb shell to a full interactive TTY."
tags: [adb, arp, credential_access, enumeration, eth0, http, https, john, lateral_movement_routing_pivot, mdp, out-of-band_access, passive_enum, pdf, post_exploitation_verification, privilege_escalation, reconnaissance, serial, ssh, trained, ttyusb0, ttyusb1, linux]
source_file: "linux-user"
updated: 2026-10-30
---

uname -a; cat /etc/os-release; hostnamectl; uptime; id
# Trained Command Playbook: `linux-user.pdf`
uname -a; cat /etc/os-release; hostnamectl; uptime; id
- **Source Document:** `~/Projects/CORA/Training/linux-user.pdf`
- **CEGAR Verified Commands:** `136` (`0` malformed/unsafe snippets filtered)
- **MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`):** `136`
- **Discovered IPs/Subnets:** `0.0.0.0/0, 127.0.0.1, 172.24.0.0/16`
- **Discovered Interfaces:** `eth0, ttyACM0, ttyACM1, ttyUSB0, ttyUSB1`
- **Related Knowledge Note:** [[knowledge/trained_linux-user]]
uname -a; cat /etc/os-release; hostnamectl; uptime; id
## Distilled MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`)
| Pre-State ($s$) | Tactic ($\tau$) | Technique ($k$) | Tool ($u$) | Post-State ($s'$) | Verified Command ($c$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `make` | `s_active_services_enumerated` | `sudo make O=/home/name/build/kernel modules_install install` |
| `s_l2_l3_verified` | **`Out-of-Band_Access`** | UART/Serial Console Out-of-Band Enumeration & Control | `unset` | `s_oob_serial_enumerated` | `unset - Disable the BAU.` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `objdump` | `s_passive_topology_mapped` | `objdump -r -S -l --disassemble net/dccp/ipv4.o` |
| `s_firewall_or_acl_unlocked` | **`Lateral_Movement_Routing_Pivot`** | Remote Host Execution, L2/L3 Route Injection & Subnet Pivot | `mkdir` | `s_cross_subnet_pivot_routed` | `mkdir /tmp/imagefile` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `chmod` | `s_interactive_tty_or_priv_escalated` | `chmod 400 /dev/initrd` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `openssl` | `s_credentials_or_certs_acquired` | `openssl req -new -nodes -utf8 -sha256 -days 36500 -batch -x509 -config x509.genkey -outform PEM -out kernel_key.pem -keyout kernel_key.pem` |
| `s_cross_subnet_pivot_routed` | **`Post_Exploitation_Verification`** | Post-Action Host Identity, Privilege & Objective Verification | `echo` | `s_goal_verified_complete` | `echo $key > /sys/bus/thunderbolt/devices/0-3/key` |
| `s_init_unknown` | **`Reconnaissance`** | Domain, DNS, OSINT & Target Footprint Reconnaissance | `dd` | `s_passive_topology_mapped` | `dd if=KYK_TBT_FW_0018.bin of=/sys/bus/thunderbolt/devices/0-0/nvm_non_active0/nvmem` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `modprobe` | `s_active_services_enumerated` | `modprobe looks through the kernel command line (/proc/cmdline) and collects module parameters when` |
| `s_l2_l3_verified` | **`Out-of-Band_Access`** | UART/Serial Console Out-of-Band Enumeration & Control | `echo` | `s_oob_serial_enumerated` | `echo "number" >/proc/sys/kernel/sysrq` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `tail` | `s_passive_topology_mapped` | `tail /mnt/ftrace-ramoops` |
| `s_firewall_or_acl_unlocked` | **`Lateral_Movement_Routing_Pivot`** | Remote Host Execution, L2/L3 Route Injection & Subnet Pivot | `gzip` | `s_cross_subnet_pivot_routed` | `gzip -cd /boot/imagefile.img \| cpio -imd --quiet` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `chmod` | `s_interactive_tty_or_priv_escalated` | `chmod 755 HelloWorld.class` |
| `s_cross_subnet_pivot_routed` | **`Post_Exploitation_Verification`** | Post-Action Host Identity, Privilege & Objective Verification | `echo` | `s_goal_verified_complete` | `echo 2 > /sys/bus/thunderbolt/devices/0-3/authorized` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `ip` | `s_active_services_enumerated` | `IP DHCP, BOOTP, or RARP is enabled.` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `file` | `s_passive_topology_mapped` | `file /usr/src/packages/BUILD/sgi-enhancednfs-1.4/default/net/sunrpc/svcsock.c` |
| `s_firewall_or_acl_unlocked` | **`Lateral_Movement_Routing_Pivot`** | Remote Host Execution, L2/L3 Route Injection & Subnet Pivot | `mkdir` | `s_cross_subnet_pivot_routed` | `mkdir /initrd` |
| `s_cross_subnet_pivot_routed` | **`Post_Exploitation_Verification`** | Post-Action Host Identity, Privilege & Objective Verification | `cat` | `s_goal_verified_complete` | `cat /sys/bus/thunderbolt/devices/0-0/nvm_authenticate` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `unset` | `s_active_services_enumerated` | `unset - kernel audit is initialized but disabled and` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `find` | `s_passive_topology_mapped` | `find . \| cpio --quiet -H newc -o \| gzip -9 -n > /boot/imagefile.img` |
| `s_firewall_or_acl_unlocked` | **`Lateral_Movement_Routing_Pivot`** | Remote Host Execution, L2/L3 Route Injection & Subnet Pivot | `umount` | `s_cross_subnet_pivot_routed` | `umount /mnt` |
| `s_cross_subnet_pivot_routed` | **`Post_Exploitation_Verification`** | Post-Action Host Identity, Privilege & Objective Verification | `cat` | `s_goal_verified_complete` | `cat /sys/bus/thunderbolt/devices/0-0/nvm_version` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `cut` | `s_active_services_enumerated` | `cut the overhead, others just disable the usage. So` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `mkdir` | `s_passive_topology_mapped` | `mkdir /mnt/dev` |
| `s_firewall_or_acl_unlocked` | **`Lateral_Movement_Routing_Pivot`** | Remote Host Execution, L2/L3 Route Injection & Subnet Pivot | `gzip` | `s_cross_subnet_pivot_routed` | `gzip -9 initrd` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `start-[end]` | `s_active_services_enumerated` | `start-[end] where start and end are both` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `handle` | `s_passive_topology_mapped` | `handle 256-character (U+F000..U+F0FF) or 512-character (U+F000..U+F1FF) fonts.` |
| `s_firewall_or_acl_unlocked` | **`Lateral_Movement_Routing_Pivot`** | Remote Host Execution, L2/L3 Route Injection & Subnet Pivot | `mkdir` | `s_cross_subnet_pivot_routed` | `mkdir /new-root` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `suspend-to-ram` | `s_active_services_enumerated` | `suspend-to-ram transitions, only during s2r` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `echo` | `s_passive_topology_mapped` | `echo " $FQCLASS should be in a file called $GOODNAME"` |
| `s_firewall_or_acl_unlocked` | **`Lateral_Movement_Routing_Pivot`** | Remote Host Execution, L2/L3 Route Injection & Subnet Pivot | `mount` | `s_cross_subnet_pivot_routed` | `mount -o ro /dev/hda1 /new-root` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `unset` | `s_active_services_enumerated` | `unset - Use IOMMU translation for DMA.` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `type` | `s_passive_topology_mapped` | `Type Detail: Synchronous` |
| `s_firewall_or_acl_unlocked` | **`Lateral_Movement_Routing_Pivot`** | Remote Host Execution, L2/L3 Route Injection & Subnet Pivot | `mkdir` | `s_cross_subnet_pivot_routed` | `mkdir initrd` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `gdb` | `s_active_services_enumerated` | `gdb or control-c on the dbgp connection.` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `type` | `s_passive_topology_mapped` | `Type Detail: Synchronous Registered (Buffered)` |
| `s_firewall_or_acl_unlocked` | **`Lateral_Movement_Routing_Pivot`** | Remote Host Execution, L2/L3 Route Injection & Subnet Pivot | `umount` | `s_cross_subnet_pivot_routed` | `umount /initrd` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `echo` | `s_active_services_enumerated` | `echo 0 > /proc/sys/kernel/randomize_va_space` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `strings` | `s_passive_topology_mapped` | `Strings written to the energy_performance_preference attribute are internally translated to integer val-` |
| `s_firewall_or_acl_unlocked` | **`Lateral_Movement_Routing_Pivot`** | Remote Host Execution, L2/L3 Route Injection & Subnet Pivot | `echo` | `s_cross_subnet_pivot_routed` | `echo 0x301 >/proc/sys/kernel/real-root-dev` |
uname -a; cat /etc/os-release; hostnamectl; uptime; id
## Verified Executable Commands (Grouped by Capability Layer)
uname -a; cat /etc/os-release; hostnamectl; uptime; id
### General_System (135 commands)
```bash
sudo make O=/home/name/build/kernel modules_install install
modprobe looks through the kernel command line (/proc/cmdline) and collects module parameters when
IP DHCP, BOOTP, or RARP is enabled.
unset - kernel audit is initialized but disabled and
unset - Disable the BAU.
cut the overhead, others just disable the usage. So
start-[end] where start and end are both
suspend-to-ram transitions, only during s2r
unset - Use IOMMU translation for DMA.
gdb or control-c on the dbgp connection.
echo 0 > /proc/sys/kernel/randomize_va_space
defaults to the square root of the number of
Write-side holdoff between grace periods,
update-side primitives, if available.
echo 0 > /proc/sys/kernel/tracepoint_printk
perl scripts/get_maintainer.pl -f <filename>
WC O 4.8.4-build.1 #1
./scripts/config -d COMPILE_TEST -e DEBUG_KERNEL -e DEBUG_INFO
gdb vmlinux
gdb drivers/tty/vt/vt_ioctl.o
gdb fs/jbd/jbd.ko
gdb drivers/media/usb/dvb-usb/dvb-usb.o
objdump -r -S -l --disassemble net/dccp/ipv4.o
./scripts/get_maintainer.pl -f drivers/media/usb/gspca/sonixj.c
git bisect start
git bisect bad [commit]
git bisect good [commit]
git bisect good
git bisect bad
git bisect good v4.8
mount -t debugfs debugfs /sys/kernel/debug/
echo 1 > /sys/kernel/debug/pstore/record_ftrace
mount -t pstore pstore /mnt/
tail /mnt/ftrace-ramoops
file /usr/src/packages/BUILD/sgi-enhancednfs-1.4/default/net/sunrpc/svcsock.c
modprobe foo dyndbg==pmf # override previous settings
modprobe args to override both.
echo "module module_name -p" > <debugfs>/dynamic_debug/control
find . | cpio --quiet -H newc -o | gzip -9 -n > /boot/imagefile.img
mkdir /tmp/imagefile
gzip -cd /boot/imagefile.img | cpio -imd --quiet
mkdir /initrd
chmod 400 /dev/initrd
dd if=/dev/zero of=initrd bs=300k count=1
mount -t ext2 -o loop initrd /mnt
mkdir /mnt/dev
umount /mnt
gzip -9 initrd
mkdir /new-root
mount -o ro /dev/hda1 /new-root
mkdir initrd
umount /initrd
echo 0x301 >/proc/sys/kernel/real-root-dev
mount -n -t proc proc /proc
echo 0x0100 >/proc/sys/kernel/real-root-dev
umount -n /proc
rm -f console tty0
insmod parport
insmod parport_pc io=0x3bc,0x378,0x278 irq=none,7,auto
insmod lp parport=0,2
md device no.
write-pending clean, but writes are blocked waiting for active to be written.
cat /sys/block/md*/md/rd*/state
echo "number" >/proc/sys/kernel/sysrq
echo t > /proc/sysrq-trigger
echo 8 > /proc/sysrq-trigger
handle 256-character (U+F000..U+F0FF) or 512-character (U+F000..U+F1FF) fonts.
echo -e '\033[?2c'
echo -e '\033[?6c'
echo -e '\033[?17;0;64c'
mount binfmt_misc -t binfmt_misc /proc/sys/fs/binfmt_misc
echo ':i386:M::\x7fELF\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x00\x03: ,→\xff\xff\xff\xff\xff\xfe\xfe\xff\xff\xff\xff\xff\xff\xff\xff\xff\xfb\xff\xff:/bin/em86:'␣
echo ':i486:M::\x7fELF\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x00\x06: ,→\xff\xff\xff\xff\xff\xfe\xfe\xff\xff\xff\xff\xff\xff\xff\xff\xff\xfb\xff\xff:/bin/em86:'␣
echo ':DEXE:M::\x0eDEX::/usr/bin/dosexec:' > register
echo ':DOSWin:M::MZ::/usr/local/bin/wine:' > register
mount -t binfmt_misc none /proc/sys/fs/binfmt_misc
echo ':CLR:M::MZ::/usr/bin/mono:' > /proc/sys/fs/binfmt_misc/register
echo "No binfmt_misc support"
gcc -O2 -o javaclassname javaclassname.c
echo Usage: $0 class-file
unset CLASSBASE
echo " $CLASS should be in a" "directory tree called $FQCLASSP"
echo " Too many symbolic links encountered"
echo " $FQCLASS should be in a file called $GOODNAME"
export CLASSPATH=$CLASSBASE
export CLASSPATH=$CLASSBASE:$CLASSPATH
chmod 755 HelloWorld.class
./HelloWorld.class
./Application.jar
./Applet.html
Type Detail: Synchronous
Type Detail: Synchronous Registered (Buffered)
modprobe amd76x_edac
echo "1" >/sys/devices/system/edac/pci/check_pci_parity
echo "0" >/sys/devices/system/edac/pci/check_pci_parity
echo "1" > /sys/module/edac_core/parameters/edac_mc_panic_on_ue
echo "1" > /sys/module/edac_core/parameters/edac_mc_log_ue
echo "1" > /sys/module/edac_core/parameters/edac_mc_log_ce
echo "1000" > /sys/module/edac_core/parameters/edac_mc_poll_msec
echo "1" > /sys/module/edac_core/parameters/edac_panic_on_pci_pe
echo "0" > /sys/module/edac_core/parameters/edac_panic_on_pci_pe
out-of-tree driver uses controls here to allow for ERROR INJECTION operations to
test-instance0
test-block0
test-block-bits-
echo 2 >/sys/devices/system/edac/mc/mc0/inject_addrmatch/dimm
echo 1 >/sys/devices/system/edac/mc/mc0/inject_addrmatch/rank
echo any >/sys/devices/system/edac/mc/mc0/inject_addrmatch/dimm
echo any >/sys/devices/system/edac/mc/mc0/inject_addrmatch/rank
echo 2 >/sys/devices/system/edac/mc/mc0/inject_addrmatch/channel
echo 2 >/sys/devices/system/edac/mc/mc0/inject_type
echo 64 >/sys/devices/system/edac/mc/mc0/inject_eccmask
echo 3 >/sys/devices/system/edac/mc/mc0/inject_section
echo 1 >/sys/devices/system/edac/mc/mc0/inject_enable
dd if=/dev/mem of=/dev/null seek=16k bs=4k count=1 >& /dev/null
echo `$(($(cat cpuinfo_transition_latency) * 750 / 1000)) > ondemand/sampling_rate
Strings written to the energy_performance_preference attribute are internally translated to integer val-
echo 1 > events/power/pstate_sample/enable
echo 1 > events/power/cpu_frequency/enable
cat available_filter_functions | grep -i pstate
echo intel_pstate_set_pstate > set_ftrace_filter
echo function > current_tracer
cat trace | head -15
echo 1 > /sys/bus/thunderbolt/devices/0-1/authorized
echo $key > /sys/bus/thunderbolt/devices/0-3/key
echo 1 > /sys/bus/thunderbolt/devices/0-3/authorized
echo 2 > /sys/bus/thunderbolt/devices/0-3/authorized
dd if=KYK_TBT_FW_0018.bin of=/sys/bus/thunderbolt/devices/0-0/nvm_non_active0/nvmem
echo 1 > /sys/bus/thunderbolt/devices/0-0/nvm_authenticate
cat /sys/bus/thunderbolt/devices/0-0/nvm_authenticate
cat /sys/bus/thunderbolt/devices/0-0/nvm_version
echo 127.0.0.1 -CIPSO > /sys/fs/smackfs/netlabel
echo 0.0.0.0/0 @
echo 172.24.0.0/16 -CIPSO > /sys/fs/smackfs/netlabel
echo 0.0.0.0/0
```
uname -a; cat /etc/os-release; hostnamectl; uptime; id
### L7_HTTP_Web (1 commands)
```bash
openssl req -new -nodes -utf8 -sha256 -days 36500 -batch -x509 -config x509.genkey -outform PEM -out kernel_key.pem -keyout kernel_key.pem
```
uname -a; cat /etc/os-release; hostnamectl; uptime; id

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
