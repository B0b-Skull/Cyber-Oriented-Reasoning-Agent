---
title: "Trained Command Playbook: Survey CMDs.txt"
tags:
  - arp
  - credential_access
  - defense_evasion_firewall
  - enumeration
  - https
  - iptables
  - mdp
  - netstat
  - passive_enum
  - post_exploitation_verification
  - text
  - trained
source_file: Survey CMDs.txt
updated: 2026-10-24 01:00:37
---

# Trained Command Playbook: `Survey CMDs.txt`

- **Source Document:** `~/Projects/CORA/Training/Survey CMDs.txt`
- **CEGAR Verified Commands:** `89` (`0` malformed/unsafe snippets filtered)
- **MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`):** `89`
- **Discovered IPs/Subnets:** `1.0.0.1, 126.255.255.254, 128.1.0.1, 191.255.255.254, 192.0.1.1, 223.255.254.254, 224.0.0.0, 239.255.255.255`
- **Discovered Interfaces:** `None`
- **Related Knowledge Note:** [[knowledge/trained_survey_cmds]]

## Distilled MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`)
| Pre-State ($s$) | Tactic ($\tau$) | Technique ($k$) | Tool ($u$) | Post-State ($s'$) | Verified Command ($c$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `unset` | `s_firewall_or_acl_unlocked` | `unset HISTFILE` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `script` | `s_credentials_or_certs_acquired` | `script surveyTranscript.txt` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `last` | `s_passive_topology_mapped` | `last` |
| `s_cross_subnet_pivot_routed` | **`Post_Exploitation_Verification`** | Post-Action Host Identity, Privilege & Objective Verification | `hostid` | `s_goal_verified_complete` | `hostid` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `find` | `s_active_services_enumerated` | `find search/path/ -newermt 20130801 \! -newermt 20130831` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `strings` | `s_firewall_or_acl_unlocked` | `strings /location/of/binary` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `uname` | `s_credentials_or_certs_acquired` | `uname -a` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `uptime` | `s_passive_topology_mapped` | `uptime` |
| `s_cross_subnet_pivot_routed` | **`Post_Exploitation_Verification`** | Post-Action Host Identity, Privilege & Objective Verification | `hostname` | `s_goal_verified_complete` | `hostname` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `cp` | `s_active_services_enumerated` | `cp -p` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `grep` | `s_firewall_or_acl_unlocked` | `grep mingetty /etc/init.d/*` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `date` | `s_credentials_or_certs_acquired` | `date` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `psrinfo` | `s_passive_topology_mapped` | `psrinfo -v` |
| `s_cross_subnet_pivot_routed` | **`Post_Exploitation_Verification`** | Post-Action Host Identity, Privilege & Objective Verification | `runlevel` | `s_goal_verified_complete` | `runlevel` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `history` | `s_firewall_or_acl_unlocked` | `history` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `find` | `s_credentials_or_certs_acquired` | `find / -name password.txt > /tmp/pwdfiles &` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `cat` | `s_passive_topology_mapped` | `cat /proc/cpuinfo` |
| `s_cross_subnet_pivot_routed` | **`Post_Exploitation_Verification`** | Post-Action Host Identity, Privilege & Objective Verification | `uname` | `s_goal_verified_complete` | `uname -r` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `ip` | `s_firewall_or_acl_unlocked` | `ip addr show` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `ps` | `s_credentials_or_certs_acquired` | `ps -efh` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `modinfo` | `s_passive_topology_mapped` | `modinfo -c` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `lsmod` | `s_firewall_or_acl_unlocked` | `lsmod` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `ptree` | `s_credentials_or_certs_acquired` | `ptree ps` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `vmstat` | `s_passive_topology_mapped` | `vmstat` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `who` | `s_firewall_or_acl_unlocked` | `who -r` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `netstat` | `s_credentials_or_certs_acquired` | `netstat -anP [tcp\|udp]` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `ifconfig` | `s_passive_topology_mapped` | `ifconfig -a` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `cat` | `s_firewall_or_acl_unlocked` | `cat /etc/inittab` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `type` | `s_credentials_or_certs_acquired` | `type -a ls` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `arp` | `s_passive_topology_mapped` | `arp -an` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `cat` | `s_firewall_or_acl_unlocked` | `cat /etc/rc2.d` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `ps` | `s_credentials_or_certs_acquired` | `ps -auxwe \| grep <PID>` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `netstat` | `s_passive_topology_mapped` | `netstat -rn` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `iptables` | `s_firewall_or_acl_unlocked` | `iptables -nvL` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `ps` | `s_credentials_or_certs_acquired` | `ps -ef` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `ip` | `s_passive_topology_mapped` | `ip route show` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `echo` | `s_firewall_or_acl_unlocked` | `echo $0` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `ls` | `s_credentials_or_certs_acquired` | `ls -Rltu /etc/rc.d/init.d` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `find` | `s_passive_topology_mapped` | `find / -type f -newermt 2017-01-20` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `cat` | `s_firewall_or_acl_unlocked` | `cat /etc/passwd` |

## Verified Executable Commands (Grouped by Capability Layer)

### General_System (76 commands)
```bash
unset HISTFILE
script surveyTranscript.txt
uname -a
date
find / -name password.txt > /tmp/pwdfiles &
ps -efh
ptree ps
type -a ls
ps -auxwe | grep <PID>
strings /location/of/binary
grep mingetty /etc/init.d/*
history
lsmod
who -r
cat /etc/inittab
cat /etc/rc2.d
echo $0
cat /etc/passwd
ps -p $$
last
uptime
psrinfo -v
cat /proc/cpuinfo
hostid
modinfo -c
vmstat
hostname
find / -type f -newermt 2017-01-20
find / -type f -newermt 2017-01-20 | xargs ls -lt
find / -type f -newermt 2017-01-20 | xargs ls -ltr
find ~/ -mtime $(echo $(date +%s) - $(date +%s -d"Dec 31, 2009 23:59:59") | bc -l | awk '{print $1 / 86400}' | bc -l)
find . -mtime $(date +%s -d"Aug 10, 2013 23:59:59") -mtime $(date +%s -d"Aug 1, 2013 23:59:59")
find . -maxdepth 1 -mmin -$(echo $(date +%s) - $(date +%s -d"Sep 9, 2015 15:03:00") | bc -l | awk '{print $1 / 60}' ) -mmin +$(echo $(date +%s) - $(date +%s -d"Sep 9, 2015 16:21:00") | bc -l | awk '{print $1 / 60}' ) -exec ls -ld --time-style=full-iso {} \;
find search/path/ -newermt 20130801 \! -newermt 20130831
ls -al /etc/cron*
ps -efH
runlevel
lsof
ls -l /etc/*-release
uname -r
sestatus
getenforce
cat /etc/passwd | grep /bin/bash
service --status-all
chkconfig --list
ls -l /proc/<PID>/exe
fuser . 22/tcp
ls -l /proc/1279/exe
pwdx <pid>
ps aux | grep <PID>
find / -type f -name ".*" | grep <username>
find / -type d -name ".*" | grep <username>
file /usr/bin/..687-2550/data/survey-new
cat /etc/sudoers
ps -ef
cat /root/.bash_history
run-parts
ls -Rlt /etc/rc.d/cron.daily
ls -Rltc /etc/cron.daily
ls -Rltu /etc/cron.daily
ls -Rltc /etc/rc.d/init.d
ls -Rltc /etc/rc.d/rc3.d
ls -Rlt /etc/rc.d/init.d
ls -Rlt /etc/rc.d/rc3.d
ls -Rltu /etc/rc.d/init.d
ls -Rltu /etc/rc.d/rc3.d
cat /etc/shadow
cat /etc/group
cat /var/log/messages
cat /proc/version
stat /tmp
ls -al /tmp
ls -l
ls -lu
ls -lc
cp -p
```

### L2_ARP_Link (1 commands)
```bash
arp -an
```

### L3_Routing_NAT (5 commands)
```bash
ip addr show
iptables -nvL
ifconfig -a
ip route show
iptables -L
```

### L4_Port_Service (7 commands)
```bash
netstat -anP [tcp|udp]
netstat -rn
netstat -natup
ss -l
ss -e
netstat -lptun
netstat -anpt
```

