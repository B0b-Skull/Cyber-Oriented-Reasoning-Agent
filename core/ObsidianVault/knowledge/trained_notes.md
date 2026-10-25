---
title: "Trained Knowledge & Topology: Notes.txt"
tags:
  - https
  - mdp
  - netstat
  - passive_enum
  - text
  - trained
source_file: Notes.txt
doc_type: text
updated: 2026-10-25 00:59:25
---

# Trained Knowledge & Architecture: `Notes.txt`

- **Source Path:** `~/Projects/CORA/Training/Notes.txt` (`text`)
- **Extracted Technical Entities:** `https, netstat`
- **Extracted IPs / Subnets:** `None`
- **Extracted Interfaces:** `None`
- **Linked Command Playbook:** [[commands/trained_notes]] (`2` CEGAR-verified commands | `2` MDP transitions)

## Command & Tactic Coverage Summary
- **Total CEGAR-Verified Commands:** `2` (full executable list in [[commands/trained_notes]])
- **Tactic Distribution:** `Passive_Enum` (2)
- **Top Extracted CLI Tools:** `echo` (1), `strings` (1)

## Extracted Reference Excerpt
Verify Netstat
	file `which netstat`
=======================================================================================================
MD5SUM
	Linux
		md5sum `which netstat`

	Solaris
		digest -a md5 `which netstat`
=======================================================================================================
Enum Processes
	Solaris
		echo "[ solaris netstat ]" && pfiles `ls /proc` 2>/dev/null | awk "/^ [^ \\t]/{smatch=\$0;next}/port:[ \\t]*${1}/{print smatch, \$0}{next}" | awk '{printf "PID %-5s %-30s Port %-5s \n",$1,$2,$NF}' | grep -v "Port 0"
		rpcbind -p 
		
Check Ports URL
	https://en.wikipedia.org/wiki/List_of_TCP_and_UDP_port_numbers
	
String inidicators
	Solaris
		strings <FILE> | grep --color -En 'AF|INET|SOCK'

Files Modified on same date
	Linux 
		for i in FILE; do touch -d `ls -lah --time-style=long-iso $i | awk '{print $6}'` /dev/shm/tl; touch -d `ls -lah --time-style=long-iso $i | awk '{print $6}' | sed -e 's/-//g' | awk '{print $1+1}'` /dev/shm/t2; find / -newer /dev/shm/tl -and -not newer /dev/shm/t2 -and -not -samefile /dev/shm/t2 2>/dev/null | xargs ls -lahF --color; rm -f /dev/shm/t1; rm -f /dev/shm/t2; done | more
		

Viewing txt files in Notepad ++
	Use replace option and put \n in second line

