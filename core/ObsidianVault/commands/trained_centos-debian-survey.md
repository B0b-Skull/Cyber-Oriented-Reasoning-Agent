---
title: "Trained Command Playbook: CentOS-Debian-Survey"
category: commands
domain_hub: "[[knowledge/06_linux_unix_administration_processes_and_logging]]"
os_platform: linux
primary_tactic: Passive_Enum
summary: "Verified Windows & Linux command playbook for CentOS-Debian-Survey (Passive_Enum): Linux (Debian/Ubuntu/CentOS/RHEL) and UNIX/Solaris system administration, kernel /proc & sysctl internals, ext4/xfs/procfs filesystems,"
when_to_apply: "Apply when working with CentOS-Debian-Survey (linux): Apply when enumerating a Linux/UNIX/Solaris host, inspecting `/proc/<PID>` or kernel modules, auditing mounted filesystems (`findmnt`/`lsblk`), managing `systemd` services or signals, hunting SUID/SGID/Capabilities/sudo privilege escalation vectors, reviewing `/var/log`/`journalctl` logs, or upgrading a dumb shell to a full interactive TTY."
tags: [active_enum, arp, credential_access, defense_evasion_firewall, enumeration, eth0, eth1, https, iptables, john, mdp, netstat, passive_enum, post_exploitation_verification, privilege_escalation, ssh, text, trained, linux, unix, solaris, systemctl]
source_file: "CentOS-Debian-Survey"
updated: 2026-10-30
---

uname -a; cat /etc/os-release; hostnamectl; uptime; id
# Trained Command Playbook: `CentOS-Debian-Survey.txt`
uname -a; cat /etc/os-release; hostnamectl; uptime; id
- **Source Document:** `~/Projects/CORA/Training/CentOS-Debian-Survey.txt`
- **CEGAR Verified Commands:** `182` (`0` malformed/unsafe snippets filtered)
- **MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`):** `182`
- **Discovered IPs/Subnets:** `10.10.10.10/24, 10.18.80.64/26, 172.24.11.0/24, 172.24.11.13, 172.24.111.112/29, 172.24.2.2/24`
- **Discovered Interfaces:** `eth0, eth1`
- **Related Knowledge Note:** [[knowledge/trained_centos-debian-survey]]
uname -a; cat /etc/os-release; hostnamectl; uptime; id
## Distilled MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`)
| Pre-State ($s$) | Tactic ($\tau$) | Technique ($k$) | Tool ($u$) | Post-State ($s'$) | Verified Command ($c$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `date` | `s_passive_topology_mapped` | `date` |
| `s_cross_subnet_pivot_routed` | **`Post_Exploitation_Verification`** | Post-Action Host Identity, Privilege & Objective Verification | `uname` | `s_goal_verified_complete` | `uname -a` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `strace` | `s_active_services_enumerated` | `strace <name>` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `modinfo` | `s_firewall_or_acl_unlocked` | `modinfo \| grep -i " loaded"` |
| `s_passive_topology_mapped` | **`Active_Enum`** | Active Network, Cloud, Directory Service & Endpoint Probing | `rpcinfo` | `s_active_services_enumerated` | `rpcinfo -p` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `cat` | `s_credentials_or_certs_acquired` | `cat /etc/shadow` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `grep` | `s_interactive_tty_or_priv_escalated` | `grep 'This I\$ Y\*ur File' /root/*` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `uptime` | `s_passive_topology_mapped` | `uptime` |
| `s_cross_subnet_pivot_routed` | **`Post_Exploitation_Verification`** | Post-Action Host Identity, Privilege & Objective Verification | `hostname` | `s_goal_verified_complete` | `hostname` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `last` | `s_active_services_enumerated` | `last -i` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `lsof` | `s_firewall_or_acl_unlocked` | `lsof` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `cat` | `s_credentials_or_certs_acquired` | `cat /etc/group` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `find` | `s_interactive_tty_or_priv_escalated` | `find / -perm -u=s 2>/dev/null \| xargs ls -la \| more` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `sestatus` | `s_passive_topology_mapped` | `sestatus` |
| `s_cross_subnet_pivot_routed` | **`Post_Exploitation_Verification`** | Post-Action Host Identity, Privilege & Objective Verification | `rmmod` | `s_goal_verified_complete` | `rmmod power_meter` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `tar` | `s_active_services_enumerated` | `tar -cf /location/name.tar` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `lsmod` | `s_firewall_or_acl_unlocked` | `lsmod \| grep  tables` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `lastlog` | `s_credentials_or_certs_acquired` | `lastlog \| grep -v "*"` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `cat` | `s_interactive_tty_or_priv_escalated` | `cat -n /home/morty/.bash_history \| grep 76` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `modinfo` | `s_passive_topology_mapped` | `modinfo dm_zero` |
| `s_cross_subnet_pivot_routed` | **`Post_Exploitation_Verification`** | Post-Action Host Identity, Privilege & Objective Verification | `id` | `s_goal_verified_complete` | `ID system` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `tar` | `s_active_services_enumerated` | `tar -tf name.tar` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `echo` | `s_firewall_or_acl_unlocked` | `echo "Modules dir: /lib/modules/$(uname -r) for kernel version $(uname -r)"` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `grep` | `s_credentials_or_certs_acquired` | `grep -v "^#" /etc/inittab \| grep -v "^$" \| more` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `find` | `s_interactive_tty_or_priv_escalated` | `find . -mtime $(date +%s -d"Aug 10, 2013 23:59:59") -mtime $(date +%s -d"Aug 1, 2013 23:59:59")` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `lsmod` | `s_passive_topology_mapped` | `lsmod` |
| `s_cross_subnet_pivot_routed` | **`Post_Exploitation_Verification`** | Post-Action Host Identity, Privilege & Objective Verification | `dpkg` | `s_goal_verified_complete` | `dpkg -l` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `ls` | `s_active_services_enumerated` | `ls a[b-d]e` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `ifconfig` | `s_firewall_or_acl_unlocked` | `ifconfig -a` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `ln` | `s_credentials_or_certs_acquired` | `ln -s /usr/sbin/sysloger /root/examine/sysloger_executable` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `find` | `s_interactive_tty_or_priv_escalated` | `find ~/ -mtime $(echo $(date +%s) - $(date +%s -d"Dec 31, 2018 23:59:59") \| bc -l \| awk '{print $1 / 86400}' \| bc -l)` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `ps` | `s_passive_topology_mapped` | `ps -ef --sort start_time` |
| `s_cross_subnet_pivot_routed` | **`Post_Exploitation_Verification`** | Post-Action Host Identity, Privilege & Objective Verification | `echo` | `s_goal_verified_complete` | `echo $0` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `ls` | `s_active_services_enumerated` | `ls !(*.jpb\|*.gif)` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `ip` | `s_firewall_or_acl_unlocked` | `ip addr show` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `ls` | `s_credentials_or_certs_acquired` | `ls -lhartF /etc/rc.d/rc*.d/` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `chown` | `s_interactive_tty_or_priv_escalated` | `chown <NewOwnerUsername> <Filename>` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `ps` | `s_passive_topology_mapped` | `ps -elf` |
| `s_cross_subnet_pivot_routed` | **`Post_Exploitation_Verification`** | Post-Action Host Identity, Privilege & Objective Verification | `echo` | `s_goal_verified_complete` | `echo BOO! > /dev/pts/1` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `dd` | `s_active_services_enumerated` | `dd if=/dev/sda1 bs=512 skip=2 count=2 \| od -t x1` |
uname -a; cat /etc/os-release; hostnamectl; uptime; id
## Verified Executable Commands (Grouped by Capability Layer)
uname -a; cat /etc/os-release; hostnamectl; uptime; id
### General_System (143 commands)
```bash
date
uptime
uname -a
hostname
sestatus
rmmod power_meter
modinfo dm_zero
lsmod
ps -ef --sort start_time
ps -elf
df -h
df -i
sudo ls -l /proc/<pid>/exe
cat /etc/services | grep <port>
strace <name>
ls -latrd /etc/cron*
ls -latr /var/spool/cron /var/spool/at
ls -latr /root
ls -latr /home/*
ls -latr /export/home/*
ls -latr /tmp
ls -latr /
crontab -l <username>
ls -l /var/spool/cron/crontabs
cat /var/spool/cron/crontabs/<name>
cat /etc/init.d/<file>
ls -l /etc/cron.weekly
ls -l /etc/cron.daily
ID system
cat /etc/*elease
dpkg -l
dpkg -l | grep "sys"
stat /proc/1/exe
stat /sbin/init
echo $0
cat /etc/passwd
ps -p $$
echo BOO! > /dev/pts/1
modinfo | grep -i " loaded"
lsof
lsmod | grep  tables
echo "Modules dir: /lib/modules/$(uname -r) for kernel version $(uname -r)"
lsof -i TCP:<port>
lsof -t TCP:1-1024
lsof -i -u^root
kill -9 `lsof -t -u tecminst`
ps -ef | grep ssh
ps -efj
cat /etc/services | grep <PORT>
last show
cat /etc/sysconfig/iptables
cat /etc/sysconfig/ip6tables
sudo iptables -A FORWARD -i eth0 -o eth1 -j ACCEPT
sudo iptables -A FORWARD -i eth1 -o eth0 -j ACCEPT
sudo iptables -A FORWARD -s 172.24.11.0/24 -d 172.24.111.112/29 -j ACCEPT
sudo iptables -A FORWARD -d 172.24.11.0/24 -s 172.24.111.112/29 -j ACCEPT
cat /etc/shadow
cat /etc/group
lastlog | grep -v "*"
grep -v "^#" /etc/inittab | grep -v "^$" | more
service --status-all
ls -al /etc/rc<#>.d/
ls -al /etc/rc3.d/ | grep " S" | wc -l
chkconfig --list
getenforce
last
ls -latr /bin
ls -latr /sbin
ls -latr /usr/bin
ls -latr /usr/sbin
ls -latr /usr/local/bin
ls -latr /usr/local/sbin
ls -latr /var/log /var/log/audit
ls -latr /var/adm
last -i
egrep "kernel|dbus" /var/log/messages
egrep -v "kernel|dbus" /var/log/messages | tail -50
find /var/log -name '*.log'
tar -cf /location/name.tar
tar -tf name.tar
tar -xf name.tar 'tar -tf name.tar | head -n 17 | tail -n 1'
ls a[b-d]e
ls -l !(*.txt|*.exe)
cat /etc/hosts*
ls -l /etc/pam.d/[^pf]*
find / -type f -name ".*" | grep <username>
find / -type d -name ".*" | grep <username>
find / -daystart
find /etc -type d
file /usr/bin/..687-2550/data/survey-new
ls !(*.jpb|*.gif)
ls -l +(install|uninstall).*(log|sh)
grep ops.local `find /etc -name \*.conf`
grep ops.local $(find /etc -name '*.conf')
grep 'This I\$ Y\*ur File' /root/*
find / -perm -u=s 2>/dev/null | xargs ls -la | more
cat -n /home/morty/.bash_history | grep 76
find . -mtime $(date +%s -d"Aug 10, 2013 23:59:59") -mtime $(date +%s -d"Aug 1, 2013 23:59:59")
find ~/ -mtime $(echo $(date +%s) - $(date +%s -d"Dec 31, 2018 23:59:59") | bc -l | awk '{print $1 / 86400}' | bc -l)
find . -maxdepth 1 -mmin -$(echo $(date +%s) - $(date +%s -d"Sep 9, 2015 15:03:00") | bc -l | awk '{print $1 / 60}' ) -mmin +$(echo $(date +%s) - $(date +%s -d"Sep 9, 2018 16:21:00") | bc -l | awk '{print $1 / 60}' ) -exec ls -ld --time-style=full-iso {} \;
find /var/tmp -mtime +2 -a -mtime -8 -ls
find / -name ".*" -a \! -wholename "/sys/*" | xargs ls -la | egrep -v "000"
ls -iRl
df -T
df -k -l
dd if=/dev/sda1 bs=512 skip=2 count=2 | od -t x1
dd if=/dev/sda1 bs=1k skip=1 count=1 | hexdump -C
dd if=/dev/zero of=/tmp/my_stuff.img bs=2M count=125
ls -i /
mount -t iso9660 /dev/loop1 /media
mount /dev/loop1 /media
mount -t ext3 /dev/loop0 /mnt
umount /mnt /media
echo $variable
unset variable-name
cat /etc/resolv.conf
chown <NewOwnerUsername> <Filename>
chgrp <newOwnerGroup> <Filename>
chmod symbolic-mode-list <Filename>
chmod u+rw,g=w,go-wx /home/hohnd/script.sh
chmod ugo=r /file/location
chmod 653 /home/johnd/comments.txt
chown fred:staff helloscript.sh
chmod o+rx /tmp/movelog.sh
last | grep "<date/time>" | grep <username>
ausearch --just-one
cp /usr/share/doc/audit-<version> /stig.rules /etc/audit/audit.rules
sed -i -e '/b64/ s/^/#/' /etc/audit/audit.rules
sed -i -e '/b32/ s/^#//' /etc/audit/audit.rules
auditctl -l
auditctl -l | wc -l
ausearch -x useradd -i | grep haxor
find / -name *sysloger*
chkconfig --del sysloger
chkconfig sysloger off
kill -9 <pid>
find -type p
find -samefile <nameoffile>
find -L <name>
ln -s TARGET_FILE LINK_NAME
ln -s /usr/sbin/sysloger /root/examine/sysloger_executable
ls -lhartF /etc/rc.d/rc*.d/
vi message
```
uname -a; cat /etc/os-release; hostnamectl; uptime; id
### L2_ARP_Link (3 commands)
```bash
arp -v
arp -an
ip neigh show
```
uname -a; cat /etc/os-release; hostnamectl; uptime; id
### L3_Routing_NAT (27 commands)
```bash
ip route show
ifconfig -a
ip addr show
iptables -L
iptables -nvL --line-numbers | more
iptables --list
iptables --list -t nat
ip6tables --list
ip6tables --list -t nat
iptables -t filter -L
iptables -nL
iptables -A INPUT -p udp -j REJECT --reject-with icmp-net-prohibited
iptables -A INPUT -p icmp -j DROP
iptables -A INPUT -d 172.24.11.13 \! -i eth0 -j DROP
iptables -A INPUT -p tcp -m state --state ESTABLISHED, RELATED -j ACCEPT
iptables -t filter -F
iptables -t nat -F
iptables -X
iptables -P INPUT ACCEPT
iptables -P OUTPUT ACCEPT
iptables -P FORWARD ACCEPT
iptables -t filter -A INPUT -p tcp --dport 22 -s 10.10.10.10/24 -j ACCEPT
iptables -t filter -A OUTPUT -p tcp --sport 22 -d 172.24.2.2/24 -j ACCEPT
iptables -t filter -A INPUT -p tcp --dport 22 -s 10.18.80.64/26 -m state --state NEW,ESTABLISHED,RELATED -j ACCEPT
iptables -t filter -A OUTPUT -p tcp --sport 22 -d 10.18.80.64/26 -m state --state ESTABLISHED,RELATED -j ACCEPT
ping -c 3 `cat /etc/resolv.conf | grep nameserver | awk '{print $2}' | head -n 1`
ping -c 3 `cat /etc/resolv.conf | grep nameserver | cut -d " " -f 2`
```
uname -a; cat /etc/os-release; hostnamectl; uptime; id
### L4_Port_Service (9 commands)
```bash
netstat -natup
netstat -rn
netstat -atnp | more
netstat -aunp | more
netstat -atn | more
netstat -aun | more
ss -natup
netstat -an | more
rpcinfo -p
```
uname -a; cat /etc/os-release; hostnamectl; uptime; id

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
