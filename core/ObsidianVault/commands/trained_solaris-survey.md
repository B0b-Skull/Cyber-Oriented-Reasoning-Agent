---
title: "Trained Command Playbook: Solaris-Survey.txt"
tags:
  - arp
  - credential_access
  - defense_evasion_firewall
  - enumeration
  - https
  - mdp
  - netstat
  - passive_enum
  - post_exploitation_verification
  - privilege_escalation
  - ssh
  - text
  - trained
source_file: Solaris-Survey.txt
updated: 2026-10-25 01:00:33
---

# Trained Command Playbook: `Solaris-Survey.txt`

- **Source Document:** `~/Projects/CORA/Training/Solaris-Survey.txt`
- **CEGAR Verified Commands:** `71` (`0` malformed/unsafe snippets filtered)
- **MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`):** `71`
- **Discovered IPs/Subnets:** `None`
- **Discovered Interfaces:** `None`
- **Related Knowledge Note:** [[knowledge/trained_solaris-survey]]

## Distilled MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`)
| Pre-State ($s$) | Tactic ($\tau$) | Technique ($k$) | Tool ($u$) | Post-State ($s'$) | Verified Command ($c$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `date` | `s_passive_topology_mapped` | `date` |
| `s_cross_subnet_pivot_routed` | **`Post_Exploitation_Verification`** | Post-Action Host Identity, Privilege & Objective Verification | `uname` | `s_goal_verified_complete` | `uname -a` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `locate` | `s_active_services_enumerated` | `Locate Files` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `pfiles` | `s_interactive_tty_or_priv_escalated` | `pfiles <PID> \| grep AF_INET` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `cat` | `s_credentials_or_certs_acquired` | `cat /var/adm/sulog` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `cat` | `s_firewall_or_acl_unlocked` | `cat /etc/nsswitch.conf \| grep "hosts"` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `psrinfo` | `s_passive_topology_mapped` | `psrinfo -v` |
| `s_cross_subnet_pivot_routed` | **`Post_Exploitation_Verification`** | Post-Action Host Identity, Privilege & Objective Verification | `who` | `s_goal_verified_complete` | `who -r` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `cp` | `s_active_services_enumerated` | `cp -p` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `pfiles` | `s_interactive_tty_or_priv_escalated` | `pfiles /proc/*` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `crontab` | `s_credentials_or_certs_acquired` | `crontab -e` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `ipfstat` | `s_firewall_or_acl_unlocked` | `ipfstat -io` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `uptime` | `s_passive_topology_mapped` | `uptime` |
| `s_cross_subnet_pivot_routed` | **`Post_Exploitation_Verification`** | Post-Action Host Identity, Privilege & Objective Verification | `groups` | `s_goal_verified_complete` | `groups` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `which` | `s_active_services_enumerated` | `which sudo` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `rpcinfo` | `s_interactive_tty_or_priv_escalated` | `rpcinfo -p` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `cat` | `s_firewall_or_acl_unlocked` | `cat /etc/ipf/ipf.conf` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `sysdef` | `s_passive_topology_mapped` | `sysdef -h` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `cat` | `s_active_services_enumerated` | `cat /export/<username>/.bash_history` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `find` | `s_interactive_tty_or_priv_escalated` | `find / -perm -u=s 2>/dev/null \| xargs ls -la \| more` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `cat` | `s_firewall_or_acl_unlocked` | `cat /etc/syslog.conf` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `modinfo` | `s_passive_topology_mapped` | `modinfo -c \| grep ' LOADED' \| more` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `grep` | `s_interactive_tty_or_priv_escalated` | `grep ops.local `find /etc -name \*.conf`` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `svcs` | `s_firewall_or_acl_unlocked` | `svcs \| wc -1` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `vmstat` | `s_passive_topology_mapped` | `vmstat` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `grep` | `s_interactive_tty_or_priv_escalated` | `grep ops.local $(find /etc -name '*.conf')` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `crontab` | `s_firewall_or_acl_unlocked` | `crontab -l <username>` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `find` | `s_passive_topology_mapped` | `find . -mtime $(date +%s -d"Aug 10, 2013 23:59:59") -mtime $(date +%s -d"Aug 1, 2013 23:59:59")` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `ls` | `s_interactive_tty_or_priv_escalated` | `ls -l` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `ls` | `s_firewall_or_acl_unlocked` | `ls -l /var/spool/cron/crontabs` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `find` | `s_passive_topology_mapped` | `find / -type f -name ".*" \| grep <username>` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `chown` | `s_interactive_tty_or_priv_escalated` | `chown <NewOwnerUsername> <Filename>` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `crontab` | `s_firewall_or_acl_unlocked` | `crontab -l` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `find` | `s_passive_topology_mapped` | `find / -type d -name ".*" \| grep <username>` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `chgrp` | `s_interactive_tty_or_priv_escalated` | `chgrp <newOwnerGroup> <Filename>` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `find` | `s_passive_topology_mapped` | `find ~/ -mtime $(echo $(date +%s) - $(date +%s -d"Dec 31, 2009 23:59:59") \| bc -l \| awk '{print $1 / 86400}' \| bc -l)` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `chmod` | `s_interactive_tty_or_priv_escalated` | `chmod symbolic-mode-list <Filename>` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `ps` | `s_passive_topology_mapped` | `ps -efj \| grep 711` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `chmod` | `s_interactive_tty_or_priv_escalated` | `chmod u+rw,g=w,go-wx /home/hohnd/script.sh` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `ps` | `s_passive_topology_mapped` | `ps -efj \| grep ssh` |

## Verified Executable Commands (Grouped by Capability Layer)

### General_System (64 commands)
```bash
date
uname -a
psrinfo -v
uptime
sysdef -h
modinfo -c | grep ' LOADED' | more
vmstat
who -r
Locate Files
find . -mtime $(date +%s -d"Aug 10, 2013 23:59:59") -mtime $(date +%s -d"Aug 1, 2013 23:59:59")
find / -type f -name ".*" | grep <username>
find / -type d -name ".*" | grep <username>
find ~/ -mtime $(echo $(date +%s) - $(date +%s -d"Dec 31, 2009 23:59:59") | bc -l | awk '{print $1 / 86400}' | bc -l)
ps -efj | grep 711
ps -efj | grep ssh
ps -ajf
fuser .
fuser /folder/location 22/tcp
ptree <PID>
pfiles `ls /proc` 2>/dev/null | awk "/^ [^ \\t]/{smatch=\$0;next}/port:[ \\t]*${1}/{print smatch, \$0}{next}"
ps -ef| awk '{print $2}'| xargs -I '{}' sh -c 'echo Examining process: {}; pfiles {}| grep "port: *"'
pfiles <PID> | grep AF_INET
pfiles /proc/*
find / -perm -u=s 2>/dev/null | xargs ls -la | more
grep ops.local `find /etc -name \*.conf`
grep ops.local $(find /etc -name '*.conf')
grep 'This I\$ Y\*ur File' /root/*
stat /tmp
ls -al /tmp
ls -l
ls -lu
ls -lc
cp -p
which sudo
strings `which sudo`
groups
cat /var/adm/sulog
ls -iRl | grep <inode number>
cat /etc/resolv.conf
cat /etc/nsswitch.conf | grep "hosts"
cat /etc/ipf/ipf.conf
cat /etc/syslog.conf
svcs | wc -1
crontab -l <username>
ls -l /var/spool/cron/crontabs
cat /var/spool/cron/crontabs/<name>
cat /etc/init.d/<file>
inetadm | grep enabled
df -t
df -k -l
chown <NewOwnerUsername> <Filename>
chgrp <newOwnerGroup> <Filename>
chmod symbolic-mode-list <Filename>
chmod u+rw,g=w,go-wx /home/hohnd/script.sh
chmod ugo=r /file/location
chmod 653 /home/johnd/comments.txt
chown fred:staff helloscript.sh
chmod o+rx /tmp/movelog.sh
cat /etc/security/policy.conf | grep -v "#"
cat /etc/user_attr
cat /.bash_history | grep "telnet"
cat /export/<username>/.bash_history
crontab -l
crontab -e
```

### L2_ARP_Link (1 commands)
```bash
arp -na
```

### L3_Routing_NAT (2 commands)
```bash
ping -c 3 `cat /etc/resolv.conf | grep nameserver | awk '{print $2}' | head -n 1`
ipfstat -io
```

### L4_Port_Service (4 commands)
```bash
rpcinfo -p
netstat -rn
netstat -anf inet -P tcp | more
netstat -anf inet -P udp | more
```

