---
title: "Trained Knowledge & Topology: Solaris-Survey.txt"
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
doc_type: text
updated: 2026-10-24 01:00:33
---

# Trained Knowledge & Architecture: `Solaris-Survey.txt`

- **Source Path:** `~/Projects/CORA/Training/Solaris-Survey.txt` (`text`)
- **Extracted Technical Entities:** `arp, https, netstat, ssh`
- **Extracted IPs / Subnets:** `None`
- **Extracted Interfaces:** `None`
- **Linked Command Playbook:** [[commands/trained_solaris-survey]] (`71` CEGAR-verified commands | `71` MDP transitions)

## Command & Tactic Coverage Summary
- **Total CEGAR-Verified Commands:** `71` (full executable list in [[commands/trained_solaris-survey]])
- **Tactic Distribution:** `Passive_Enum` (39), `Privilege_Escalation` (15), `Defense_Evasion_Firewall` (8), `Enumeration` (4), `Post_Exploitation_Verification` (3), `Credential_Access` (2)
- **Top Extracted CLI Tools:** `cat` (11), `ls` (6), `chmod` (5), `find` (5), `ps` (4), `crontab` (3), `grep` (3), `netstat` (3), `pfiles` (3), `chown` (2), `df` (2), `fuser` (2), `arp` (1), `chgrp` (1), `cp` (1), `date` (1), `groups` (1), `inetadm` (1), `ipfstat` (1), `locate` (1), `modinfo` (1), `ping` (1), `psrinfo` (1), `ptree` (1), `rpcinfo` (1)

## Extracted Reference Excerpt
Solaris

Solaris 10+ = SMF 
Solaris <9  = SysVinit
=======================================================================================================
System Identification
	date
	uname -a
	w 
	psrinfo -v
	uptime
	sysdef -h
	modinfo -c | grep ' LOADED' | more		:Shows loaded kernel modules
	vmstat									:Memory level for virtual environment
	who -r 									:Current run level
=======================================================================================================
Locate Files
	find . -mtime $(date +%s -d"Aug 10, 2013 23:59:59") -mtime $(date +%s -d"Aug 1, 2013 23:59:59")			:Finds files between a set of dates
	find / -type f -name ".*" | grep <username>			:Searches for all hidden files in usernames folders
	find / -type d -name ".*" | grep <username>			:Searches for hidden directories with user name in them
	find . -mtime $(date +%s -d"Aug 10, 2013 23:59:59") -mtime $(date +%s -d"Aug 1, 2013 23:59:59")								:Find files between two dates
	find ~/ -mtime $(echo $(date +%s) - $(date +%s -d"Dec 31, 2009 23:59:59") | bc -l | awk '{print $1 / 86400}' | bc -l)		:Find files before specific date 
=======================================================================================================
Port and Process ENUMERATION
	ps -efj | grep 711 							:Shows where PID 711 is exectuting from
	ps -efj | grep ssh							:searches process list for ssh 
	ps -ajf
	fuser . 									:Shows contents of folder being accessed by what processes
	fuser /folder/location 22/tcp 				:Shows contents of folder using port 22 with protocol tcp
	ptree <PID>
*   pfiles `ls /proc` 2>/dev/null | awk "/^ [^ \\t]/{smatch=\$0;next}/port:[ \\t]*${1}/{print smatch, \$0}{next}"		:Solaris - finds ports and associates with PIDs
*	ps -ef| awk '{print $2}'| xargs -I '{}' sh -c 'echo Examining process: {}; pfiles {}| grep "port: *"'				:Solaris - finds ports and pids, can specify port.
	pfiles <PID> | grep AF_INET				:Solaris - Shows all ports that PID is associated with 
	pfiles /proc/* 							:Solaris - Display list of services running
	rpcinfo -p 
=======================================================================================================
Find files with SUID bit set 
	find / -perm -u=s 2>/dev/null | xargs ls -la | more 
	grep ops.local `find /etc -name \*.conf`		:CSH - Searches contents of all files in /etc that end in ".conf" and contain the string "ops.local"
	grep ops.local $(find /etc -name '*.conf')		:BASH - Searches contents of all files in /etc that end in ".conf" and contain the string "ops.local"
	grep 'This I\$ Y\*ur File' /root/* 				:Searches all folders/directories in /root/ for the string indicated.
=======================================================================================================
Time Stamps
	stat /tmp
	ls -al /tmp 
	ls -

