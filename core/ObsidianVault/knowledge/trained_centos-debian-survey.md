---
title: "Trained Knowledge & Topology: CentOS-Debian-Survey.txt"
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
source_file: CentOS-Debian-Survey.txt
doc_type: text
updated: 2026-10-24 00:57:11
---

# Trained Knowledge & Architecture: `CentOS-Debian-Survey.txt`

- **Source Path:** `~/Projects/CORA/Training/CentOS-Debian-Survey.txt` (`text`)
- **Extracted Technical Entities:** `arp, eth0, eth1, https, iptables, john, netstat, ssh`
- **Extracted IPs / Subnets:** `10.10.10.10/24, 10.18.80.64/26, 172.24.11.0/24, 172.24.11.13, 172.24.111.112/29, 172.24.2.2/24`
- **Extracted Interfaces:** `eth0, eth1`
- **Linked Command Playbook:** [[commands/trained_centos-debian-survey]] (`182` CEGAR-verified commands | `182` MDP transitions)

## Command & Tactic Coverage Summary
- **Total CEGAR-Verified Commands:** `182` (full executable list in [[commands/trained_centos-debian-survey]])
- **Tactic Distribution:** `Passive_Enum` (93), `Defense_Evasion_Firewall` (43), `Enumeration` (19), `Privilege_Escalation` (13), `Post_Exploitation_Verification` (7), `Credential_Access` (6), `Active_Enum` (1)
- **Top Extracted CLI Tools:** `ls` (29), `iptables` (24), `find` (15), `cat` (13), `netstat` (7), `chmod` (5), `ps` (5), `df` (4), `echo` (4), `grep` (4), `last` (4), `lsof` (4), `chkconfig` (3), `dd` (3), `ip` (3), `mount` (3), `tar` (3), `arp` (2), `auditctl` (2), `ausearch` (2), `chown` (2), `dpkg` (2), `egrep` (2), `ip6tables` (2), `kill` (2)

## Extracted Reference Excerpt
CentOS - Debian Survey

Sysvinit
=======================================================================================================
Initial CMDs
	w						:Displays uptime and any users logged on with TTY
	date					:Displays local zulu time of when the target was accessed
	uptime 					:Displays system uptime since last shutdown/reboot/poweroff
	id						:Shows user id, group id, GID, UID
	uname -a				:Displays info about kernel and processor
	hostname
	sestatus				:Shows status of SELinux on target		- Look in /etc/selinux/config 
=======================================================================================================
Kernel Modules
	rmmod power_meter		:Removes modudle "power_meter" if not running or loaded in kernel
	modinfo dm_zero			:Shows kernel module dm_zero
	insmod
	lsmod 					:Show status of modules in kernel 
	sysctl -a				:Linux - displays all kernel parameters set in current running configuration
=======================================================================================================
View Process and Network info
	ps -ef --sort start_time	:Displays process list by start time 
	ps -elf 					:Use this if above CMD doesn't work
	ps auxwww					:Same as above
	ps -axjf
	netstat -natup				:Displays all TCP and UDP network sockets. The -p option may log if you are not root
	netstat -rn					:Displays routing table
	arp -v						:Displays current ARP cache
	df -h 						:Dsiplays system hard drive utilization
	df -i 						:Displays system inode utilization
	sudo ls -l /proc/<pid>/exe	:Linux - Searches where binary is loaded from 
	cat /etc/services | grep <port>
	strace <name>				:Traces execution of program in memory 
		Example: strace -o /tmp/strace.txt cat group passwd
=======================================================================================================
ID system with cron jobs - Could potentially be logged
	ls -latrd /etc/cron*						:List all cron directories including cron.hourly and cron.daily - We want to inspect the content of these files
	ls -latr /var/spool/cron /var/spool/at		:Lists additional locations for con and at jobs - We want to inspect the content of these files
	ls -latr /root
	ls -latr /home/*
	ls -latr /export/home/*
	less <user_path>/.bash_history			:Displays user command history
	less <user_path>/.history				:Displays user command history
	ls -latr /tmp							:Displays contents of /tmp directory
	ls -latr /								:Displays contents of root directory
=======================================================================================================
Startup Scripts & Cron Jobs
	crontab -l <username>						:Verify crontab for user 
	ls -l /var/spool/cron/crontabs 				:Verify crontabs exist
	cat /var/spool/cron/crontabs/<name>			:View cron jobs for that user or set to run at sta

