---
title: "Trained Knowledge & Topology: Logging-CMDs.txt"
tags:
  - defense_evasion_firewall
  - enumeration
  - mdp
  - netstat
  - passive_enum
  - post_exploitation_verification
  - reconnaissance
  - text
  - trained
source_file: Logging-CMDs.txt
doc_type: text
updated: 2026-10-24 00:58:52
---

# Trained Knowledge & Architecture: `Logging-CMDs.txt`

- **Source Path:** `~/Projects/CORA/Training/Logging-CMDs.txt` (`text`)
- **Extracted Technical Entities:** `netstat`
- **Extracted IPs / Subnets:** `172.24.11.13`
- **Extracted Interfaces:** `None`
- **Linked Command Playbook:** [[commands/trained_logging-cmds]] (`27` CEGAR-verified commands | `27` MDP transitions)

## Command & Tactic Coverage Summary
- **Total CEGAR-Verified Commands:** `27` (full executable list in [[commands/trained_logging-cmds]])
- **Tactic Distribution:** `Passive_Enum` (14), `Defense_Evasion_Firewall` (6), `Enumeration` (3), `Reconnaissance` (3), `Post_Exploitation_Verification` (1)
- **Top Extracted CLI Tools:** `ps` (3), `auditctl` (2), `cat` (2), `sed` (2), `service` (2), `tail` (2), `aureport` (1), `ausearch` (1), `dmesg` (1), `echo` (1), `id` (1), `logger` (1), `ls` (1), `lsof` (1), `netstat` (1), `sestatus` (1), `setenforce` (1), `svcadm` (1), `svcs` (1), `vi` (1)

## Extracted Reference Excerpt
Unix Logging

ps -ef | grep syslog				:Shows type of syslog being used
ls /etc/syslog*						:Shows all files in /etc that begin with syslog
=======================================================================================================
/etc/syslong.conf					:Config file for syslogs
/var/adm/sulog						:SU command has its own log location
=======================================================================================================
Configure linux to be a syslog server and receive syslog messages
	vi /etc/sysconfig/syslog			:edit syslog file 
		SYSLOGD_OPTIONS="-m 0 -r"		:Modify this line to start remote server capabilities
	service syslog restart				:Restarts syslog service
	netstat -ulnp						:Verifies system is listening on UDP port 514
=======================================================================================================
Configure Solaris to send syslog info
	/etc/hosts
	echo 172.24.11.13 linux.ops.local loghost >> /etc/hosts		:appends the info to the /etc/hosts file to send log info currently configured to go to /var/log/syslog to another logging server named "linux.ops.local"
	svcadm restart system/system-log								:restarts syslog process
=======================================================================================================
Testing log setup
	On Solaris or remote server
		logger -p auth.notice tst msg			:Need to create a message that logs to LOGHOST as defined in /etc/syslog.conf. Facility "auth" and priority "notice" will do this
	On Linux local server
		tail /var/log/messages					:Will show the last message received by the server. 
=======================================================================================================
svcs utmp									:Starts utmpd daemon to track logs for /var/adm/wtmpx and /var/adm/utmpx
cat /var/adm/messages | grep Copyright		:Solaris, SunOS and Copyright are always right after a reboot. Also try "ID 540533 kern.notice" and "ID 218167 kern.notice"
cat /var/log/authlog | grep console			:This log file shows console logon
dmesg										:Very close as reading directly from /var/adm/messages as dmesg reads directly from /var/adm/messages*
=======================================================================================================
ps -C auditd				:Displays only the PID for the audit daemon
id daemon					:Displays uid and gid of daemon process
ps awx|grep auditd			:Displays all PIDs where auditd is used
lsof -p <PID>				:List of open files only for a specific PID
tail -n2 /var/log/messages	:Shows last two logs from /var/log/messages file
=======================================================================================================
Log locations
	Linux
		/var/log/utmp		:Shows user logins,logouts,system boot time, system events
		/var/log/wtm

