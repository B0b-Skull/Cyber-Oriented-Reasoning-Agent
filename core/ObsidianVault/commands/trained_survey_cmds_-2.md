---
title: "Trained Command Playbook: Survey CMDs -2.txt"
tags:
  - active_enum
  - arp
  - credential_access
  - defense_evasion_firewall
  - enumeration
  - eth0
  - eth1
  - https
  - iptables
  - john
  - mdp
  - netstat
  - passive_enum
  - post_exploitation_verification
  - privilege_escalation
  - ssh
  - text
  - trained
source_file: Survey CMDs -2.txt
updated: 2026-10-25 01:00:36
---

# Trained Command Playbook: `Survey CMDs -2.txt`

- **Source Document:** `~/Projects/CORA/Training/Survey CMDs -2.txt`
- **CEGAR Verified Commands:** `190` (`0` malformed/unsafe snippets filtered)
- **MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`):** `190`
- **Discovered IPs/Subnets:** `10.10.10.10/24, 10.18.80.64/26, 172.24.11.0/24, 172.24.11.13, 172.24.111.112/29, 172.24.2.2/24`
- **Discovered Interfaces:** `eth0, eth1`
- **Related Knowledge Note:** [[knowledge/trained_survey_cmds_-2]]

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

## Verified Executable Commands (Grouped by Capability Layer)

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

### L2_ARP_Link (3 commands)
```bash
arp -v
arp -an
ip neigh show
```

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

