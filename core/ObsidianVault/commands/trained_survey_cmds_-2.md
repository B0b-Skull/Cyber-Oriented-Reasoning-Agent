---
title: "Trained Command Playbook: Survey CMDs -2"
category: commands
domain_hub: "[[knowledge/01_windows_system_process_and_sysinternals]]"
os_platform: windows
primary_tactic: Passive_Enum
summary: "Verified Windows & Linux command playbook for Survey CMDs -2 (Passive_Enum): Windows live incident response, process tree/PPID investigation, service binary auditing, kernel architecture, file searching (findstr/"
when_to_apply: "Apply when working with Survey CMDs -2 (windows): Apply when performing initial Windows host triage (s_init_unknown), investigating running processes/PPIDs, mapping svchost.exe services, hunting unsigned/injected DLLs, searching files by timestamp/content, or executing Sysinternals live response."
tags: [active_enum, arp, credential_access, defense_evasion_firewall, enumeration, eth0, eth1, https, iptables, john, mdp, netstat, passive_enum, post_exploitation_verification, privilege_escalation, ssh, text, trained, windows, sysinternals, pslist, listdlls]
source_file: "Survey CMDs -2"
updated: 2026-10-30
---

systeminfo && whoami /all
# Trained Command Playbook: `Survey CMDs -2.txt`
systeminfo && whoami /all
- **Source Document:** `~/Projects/CORA/Training/Survey CMDs -2.txt`
- **CEGAR Verified Commands:** `190` (`0` malformed/unsafe snippets filtered)
- **MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`):** `190`
- **Discovered IPs/Subnets:** `10.10.10.10/24, 10.18.80.64/26, 172.24.11.0/24, 172.24.11.13, 172.24.111.112/29, 172.24.2.2/24`
- **Discovered Interfaces:** `eth0, eth1`
- **Related Knowledge Note:** [[knowledge/trained_survey_cmds_-2]]
systeminfo && whoami /all
## Distilled MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`)
| Pre-State ($s$) | Tactic ($\tau$) | Technique ($k$) | Tool ($u$) | Post-State ($s'$) | Verified Command ($c$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `date` | `s_passive_topology_mapped` | `date` |
| `s_cross_subnet_pivot_routed` | **`Post_Exploitation_Verification`** | Post-Action Host Identity, Privilege & Objective Verification | `uname` | `s_goal_verified_complete` | `uname -a` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `modprobe` | `s_active_services_enumerated` | `modprobe -l` |
| `s_passive_topology_mapped` | **`Active_Enum`** | Active Network, Cloud, Directory Service & Endpoint Probing | `rpcinfo` | `s_active_services_enumerated` | `rpcinfo -p` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `ls` | `s_credentials_or_certs_acquired` | `ls -latr /tmp` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `modinfo` | `s_firewall_or_acl_unlocked` | `modinfo -c \| grep -i " loaded"` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `cat` | `s_interactive_tty_or_priv_escalated` | `cat /etc/shadow` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `uptime` | `s_passive_topology_mapped` | `uptime` |
| `s_cross_subnet_pivot_routed` | **`Post_Exploitation_Verification`** | Post-Action Host Identity, Privilege & Objective Verification | `hostname` | `s_goal_verified_complete` | `hostname` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `strace` | `s_active_services_enumerated` | `strace <name>` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `crontab` | `s_credentials_or_certs_acquired` | `crontab -l` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `lsmod` | `s_firewall_or_acl_unlocked` | `lsmod` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `cat` | `s_interactive_tty_or_priv_escalated` | `cat /etc/group` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `psrinfo` | `s_passive_topology_mapped` | `psrinfo` |
| `s_cross_subnet_pivot_routed` | **`Post_Exploitation_Verification`** | Post-Action Host Identity, Privilege & Objective Verification | `rmmod` | `s_goal_verified_complete` | `rmmod power_meter` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `last` | `s_active_services_enumerated` | `last -i` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `crontab` | `s_credentials_or_certs_acquired` | `crontab -e` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `lsof` | `s_firewall_or_acl_unlocked` | `lsof` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `find` | `s_interactive_tty_or_priv_escalated` | `find / -perm -u=s 2>/dev/null \| xargs ls -la \| more` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `sestatus` | `s_passive_topology_mapped` | `sestatus` |
| `s_cross_subnet_pivot_routed` | **`Post_Exploitation_Verification`** | Post-Action Host Identity, Privilege & Objective Verification | `id` | `s_goal_verified_complete` | `ID system` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `last` | `s_active_services_enumerated` | `last -25` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `ls` | `s_credentials_or_certs_acquired` | `ls -lhartF /etc/rc*.d` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `lsmod` | `s_firewall_or_acl_unlocked` | `lsmod \| grep  tables` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `grep` | `s_interactive_tty_or_priv_escalated` | `grep -v "^#" /etc/inittab \| grep -v "^$" \| more` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `modinfo` | `s_passive_topology_mapped` | `modinfo dm_zero` |
| `s_cross_subnet_pivot_routed` | **`Post_Exploitation_Verification`** | Post-Action Host Identity, Privilege & Objective Verification | `echo` | `s_goal_verified_complete` | `echo $0` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `tar` | `s_active_services_enumerated` | `tar -cf /location/name.tar` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `ls` | `s_credentials_or_certs_acquired` | `ls -lhartF /init.d/ e/tc/rc.d/init.d/` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `echo` | `s_firewall_or_acl_unlocked` | `echo "Modules dir: /lib/modules/$(uname -r) for kernel version $(uname -r)"` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `chown` | `s_interactive_tty_or_priv_escalated` | `chown <NewOwnerUsername> <Filename>` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `ps` | `s_passive_topology_mapped` | `ps -ef --sort start_time` |
| `s_cross_subnet_pivot_routed` | **`Post_Exploitation_Verification`** | Post-Action Host Identity, Privilege & Objective Verification | `echo` | `s_goal_verified_complete` | `echo BOO! > /dev/pts/1` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `tar` | `s_active_services_enumerated` | `tar -tf name.tar` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `ip` | `s_firewall_or_acl_unlocked` | `ip addr show` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `chgrp` | `s_interactive_tty_or_priv_escalated` | `chgrp <newOwnerGroup> <Filename>` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `ps` | `s_passive_topology_mapped` | `ps -elf` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `ls` | `s_active_services_enumerated` | `ls a[b-d]e` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `ss` | `s_firewall_or_acl_unlocked` | `ss -natup` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `chmod` | `s_interactive_tty_or_priv_escalated` | `chmod symbolic-mode-list <Filename>` |
systeminfo && whoami /all
## Verified Executable Commands (Grouped by Capability Layer)
systeminfo && whoami /all
### General_System (147 commands)
```bash
date
uptime
psrinfo
uname -a
hostname
sestatus
rmmod power_meter
modinfo dm_zero
modprobe -l
ps -ef --sort start_time
ps -elf
sudo netstat -rn
df -h
df -i
sudo ls -l /proc/<pid>/exe
ps -axjf
sudo pfiles `ls /proc` 2>/dev/null | awk "/^[^ \\t]/{smatch=\$0;next}/port:[ \\t]*${1}/{print smatch, \$0}{next}"
sudo ps -ef| awk '{print $2}'| xargs -I '{}' sh -c 'echo Examining process: {}; pfiles {}| grep "port: <Port number>"'
sudo pfiles <PID> | grep AF_INET
cat /etc/services | grep <port>
strace <name>
ls -latrd /etc/cron*
ls -latr /var/spool/cron /var/spool/at
ls -latr /root
ls -latr /home/
ls -latr /home/*
ls -latr /export/home/
ls -latr /export/home/*
ls -latr /tmp
ls -latr /
crontab -l
crontab -e
ID system
cat /etc/*elease
psrinfo -v
echo $0
cat /etc/passwd
ps -p $$
echo BOO! > /dev/pts/1
modinfo -c | grep -i " loaded"
lsmod
lsof
lsmod | grep  tables
echo "Modules dir: /lib/modules/$(uname -r) for kernel version $(uname -r)"
pfiles <PID> | grep AF_INET
lsof -i TCP:<port>
lsof -t TCP:1-1024
lsof -i -u^root
kill -9 `lsof -t -u tecminst`
ps -ef | grep ssh
ps -efj
pfiles `ls /proc` 2>/dev/null | awk "/^[^ \\t]/{smatch=\$0;next}/port:[ \\t]*${1}/{print smatch, \$0}{next}"
ps -ef| awk '{print $2}'| xargs -I '{}' sh -c 'echo Examining process: {}; pfiles {}| grep "port: *"'
cat /etc/services | grep <PORT>
svcs | more
svcs | awk 'NR > 1 {print}' | wc -l
inetadm
last show
cat /etc/sysconfig/iptables
cat /etc/sysconfig/ip6tables
sudo iptables -A FORWARD -i eth0 -o eth1 -j ACCEPT
sudo iptables -A FORWARD -i eth1 -o eth0 -j ACCEPT
sudo iptables -A FORWARD -s 172.24.11.0/24 -d 172.24.111.112/29 -j ACCEPT
sudo iptables -A FORWARD -d 172.24.11.0/24 -s 172.24.111.112/29 -j ACCEPT
cat /etc/shadow
cat /etc/group
find / -perm -u=s 2>/dev/null | xargs ls -la | more
grep -v "^#" /etc/inittab | grep -v "^$" | more
service --status-all
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
last -25
ps -ef
ls -la /usr/bin
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
ls -lhartF /etc/rc*.d
ls -lhartF /init.d/ e/tc/rc.d/init.d/
vi message
```
systeminfo && whoami /all
### L2_ARP_Link (3 commands)
```bash
arp -v
arp -an
ip neigh show
```
systeminfo && whoami /all
### L3_Routing_NAT (27 commands)
```bash
ip route show
ifconfig -a
ifconfig -gw
ip addr show
iptables -L
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
systeminfo && whoami /all
### L4_Port_Service (13 commands)
```bash
rpcinfo -p
netstat -rn
netstat -atnp | more
netstat -aunp | more
netstat -atn | more
netstat -aun | more
netstat -anf inet -P tcp | more
netstat -anf inet -P udp | more :Solaris
netstat -natup
ss -natup
netstat -an | more
netstat -nr
netstat -na
```
systeminfo && whoami /all

<!-- CORA-MAXIMIZED-COMMANDS-START -->
## Maximized Windows & Linux Command Examples for `Survey CMDs -2`

> **Domain Hub:** [[knowledge/01_windows_system_process_and_sysinternals|Domain Hub 01: Windows Live Response, Processes, Services, Kernel & Sysinternals Suite]]  
> **Master Playbooks:** [[commands/windows_master_command_playbook]] | [[commands/linux_master_command_playbook]] | [[commands/curl_playbook]] | [[commands/tio_serial_playbook]]  
> **When to Apply:** Apply when performing initial Windows host triage (s_init_unknown), investigating running processes/PPIDs, mapping svchost.exe services, hunting unsigned/injected DLLs, searching files by timestamp/content, or executing Sysinternals live response.  
> **15-Engine H-MDP State Transition:** `s_init_unknown` $\xrightarrow{\text{Passive_Enum}}$ `s_passive_topology_mapped` | **Bayesian Root-Cause Triggers:** `suspicious_process_lineage, service_misconfiguration, unsigned_dll_injection, resource_exhaustion` | **Isolation:** `RED, BLUE, WHITE (100% local host telemetry compatible)`

| Primary Command (`Windows` / `Linux`) | OS / Shell | What It Does & Key Flags | When to Apply & Expected Output | Cross-Platform Equivalent |
| :--- | :--- | :--- | :--- | :--- |
| `systeminfo && whoami /all` | **Windows CMD** | Displays OS build, patch hotfixes (KBs), boot time, current user SID, group memberships, and token privileges (`SeDebugPrivilege`, `SeImpersonatePrivilege`). | Apply first on any Windows host (`s_init_unknown`) to establish OS baseline and privilege level. | `uname -a && id && sudo -l` |
| `tasklist /v && tasklist /svc` | **Windows CMD** | Lists all running processes with user context, memory, window titles (`/v`), and maps every `svchost.exe` PID to hosted Windows Service names (`/svc`). | Apply to identify which service inside `svchost.exe` owns a socket or high CPU thread. | `ps auxef && systemctl list-units --type=service --state=running` |
| `wmic process get ProcessId,ParentProcessId,Name,ExecutablePath,CommandLine /format:list` | **Windows CMD** | Extracts full process lineage (`PID` + `PPID`), binary disk path, and full command-line arguments for every process. | Apply to uncover hidden/encoded PowerShell arguments and anomalous parent-child process trees (e.g., `cmd.exe` spawned by `w3wp.exe`). | `ps -eo pid,ppid,user,args --forest` |
| `pslist -accepteula -t && psloggedon -accepteula` | **Sysinternals** | Prints hierarchical parent-child process tree (`-t`) and enumerates both local interactive and SMB network logon sessions. | Apply during live response to trace process trees and active user sessions. | `pstree -p -a && w` |
| `listdlls -accepteula -u && sigcheck -accepteula -e -u -vr C:\Windows\System32` | **Sysinternals** | Lists all unsigned DLLs (`listdlls -u`) loaded into running processes and scans `System32` for unsigned executables (`sigcheck -e -u`). | Apply when hunting DLL hijacking, process hollowing, or trojanized system binaries. | `grep -E '\.so' /proc/*/maps && debsums -c` |
| `handle -accepteula -a -u && tcpvcon -accepteula -a -c -n` | **Sysinternals** | Enumerates all open file/registry/mutant handles (`handle -a -u`) and dumps CSV socket-to-process mappings (`tcpvcon`). | Apply to identify malware mutexes (`BaseNamedObjects`), locked files, or进程-bound network sockets. | `lsof -i -P -n && lsof` |
| `sc query state= all && sc qc <ServiceName>` | **Windows CMD** | Lists all installed services (running/stopped) and inspects `BINARY_PATH_NAME`, `START_TYPE`, and `SERVICE_START_NAME`. | Apply to audit service binaries and check for unquoted service paths or writable service executables. | `systemctl status <service> && systemctl cat <service>` |
| `forfiles /p C:\ /s /m *.exe /d -7 /c "cmd /c echo @path @fdate @ftime"` | **Windows CMD** | Recursively (`/s`) locates executables modified within the last 7 days (`/d -7`) across drive `C:\`. | Apply during incident triage to find recently dropped binaries or staging scripts. | `find / -xdev -mtime -7 -type f -ls 2>/dev/null` |
| `findstr /s /i /n "password secret connectionString" C:\Users\*.txt C:\Users\*.ps1 C:\inetpub\*.config` | **Windows CMD** | Recursive (`/s`), case-insensitive (`/i`), line-numbered (`/n`) string search across text, script, and web config files. | Apply when auditing configuration files for plaintext credentials or API keys. | `grep -rnI -iE 'password\|secret' /var/www /home /etc 2>/dev/null` |
| `procdump -accepteula -ma <PID> C:\Temp\proc_<PID>.dmp` | **Sysinternals** | Captures a complete memory dump (`-ma`) of target process `<PID>` for strings/YARA/reverse engineering. | Apply before terminating a suspicious in-memory process so volatile unpacked strings and keys are preserved. | `gcore -o /tmp/proc_<PID> <PID>` |

### Copy-Pasteable Execution Block (Windows & Linux)
```bash
# [Windows CMD] Displays OS build, patch hotfixes (KBs), boot time, current user SID, group memberships, and token privileges (`SeDebugPrivilege`, `SeImpersonatePrivilege`).
systeminfo && whoami /all
# [Windows CMD] Lists all running processes with user context, memory, window titles (`/v`), and maps every `svchost.exe` PID to hosted Windows Service names (`/svc`).
tasklist /v && tasklist /svc
# [Windows CMD] Extracts full process lineage (`PID` + `PPID`), binary disk path, and full command-line arguments for every process.
wmic process get ProcessId,ParentProcessId,Name,ExecutablePath,CommandLine /format:list
# [Sysinternals] Prints hierarchical parent-child process tree (`-t`) and enumerates both local interactive and SMB network logon sessions.
pslist -accepteula -t && psloggedon -accepteula
# [Sysinternals] Lists all unsigned DLLs (`listdlls -u`) loaded into running processes and scans `System32` for unsigned executables (`sigcheck -e -u`).
listdlls -accepteula -u && sigcheck -accepteula -e -u -vr C:\Windows\System32
# [Sysinternals] Enumerates all open file/registry/mutant handles (`handle -a -u`) and dumps CSV socket-to-process mappings (`tcpvcon`).
handle -accepteula -a -u && tcpvcon -accepteula -a -c -n
```
<!-- CORA-MAXIMIZED-COMMANDS-END -->
