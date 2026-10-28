---
title: "Trained Knowledge & Topology: capture.sh.txt"
tags:
  - eth1
  - mdp
  - tcpdump
  - text
  - trained
source_file: capture.sh.txt
doc_type: text
updated: 2026-10-24 00:57:03
---

# Trained Knowledge & Architecture: `capture.sh.txt`

- **Source Path:** `~/Projects/CORA/Training/capture.sh.txt` (`text`)
- **Extracted Technical Entities:** `eth1, tcpdump`
- **Extracted IPs / Subnets:** `None`
- **Extracted Interfaces:** `eth1`

## Extracted Reference Excerpt
Script to capture traffic on eth1 interface
capture.sh
=======================================================================================================
	#!/bin/bash
	
	ip a | egrep -q "eth1.*state DOWN"
	
	if [ $? ]; then
		ifup eth1
	fi
	
	/usr/sbin/tcpdump -G 3000 -W 1 -w /var/log/captures/$(/bin/date +"%d-%b-%H:%M:%S")-capture.pcap -i eth1 
=======================================================================================================

