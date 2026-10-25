---
title: "Trained Knowledge & Topology: IPtables-Snort-CMDs.txt"
tags:
  - defense_evasion_firewall
  - eth0
  - eth1
  - iptables
  - mdp
  - nmap
  - snort
  - ssh
  - tcpdump
  - text
  - trained
source_file: IPtables-Snort-CMDs.txt
doc_type: text
updated: 2026-10-25 00:58:43
---

# Trained Knowledge & Architecture: `IPtables-Snort-CMDs.txt`

- **Source Path:** `~/Projects/CORA/Training/IPtables-Snort-CMDs.txt` (`text`)
- **Extracted Technical Entities:** `eth0, eth1, iptables, nmap, snort, ssh, tcpdump`
- **Extracted IPs / Subnets:** `10.18.80.64/26, 172.24.0.0/24, 172.24.1.0/24, 172.24.11.0/24, 172.24.11.13, 172.24.11.15, 172.24.11.254, 192.18.31.253, 198.18.31.253`
- **Extracted Interfaces:** `eth0, eth1, lo`
- **Linked Command Playbook:** [[commands/trained_iptables-snort-cmds]] (`42` CEGAR-verified commands | `42` MDP transitions)

## Command & Tactic Coverage Summary
- **Total CEGAR-Verified Commands:** `42` (full executable list in [[commands/trained_iptables-snort-cmds]])
- **Tactic Distribution:** `Defense_Evasion_Firewall` (42)
- **Top Extracted CLI Tools:** `iptables` (37), `nmap` (2), `service` (1), `ssh` (1), `tcpdump` (1)

## Extracted Reference Excerpt
IPTables & Snort
=======================================================================================================
nmap -n -Pn -sS -p 21,22,23,25,80,110,111,443 198.18.31.253
tcpdump -vv src 192.18.31.253 and dst 172.24.11.15
nmap -n -Pn -sU -p 53,67,123,135,137,138,161,445,631,1434 198.18.31.253
=======================================================================================================
IPTables
	iptables -A INPUT -p udp -j REJECT --reject-with icmp-net-prohibited
	iptables -A INPUT -p tcp -j REJECT --reject-with tcp-reset
	iptables -A INPUT -p icmp -j DROP
	iptables -A INPUT -d 172.24.11.13 \! -i eth0 -j DROP						:Example rule, "\! -e eth0" matches interfaces not eth0
	iptables -A INPUT -p tcp -m state --state ESTABLISHED, RELATED -j ACCEPT	:Rule accepts any incoming TCP packet part of an already ESTABLISHED or RELATED connection. Does NOT allow new connections
	iptables -P INPUT DROP														:Applies to only the filter table
	iptables -t filter -F 				:(Flush all rules from the filter table)
	iptables -t nat -F 					:(Flush all rules from the NAT table)
	iptables -X 						:(Remove all user-defined chains from the filter table)
	iptables -P INPUT ACCEPT 			:(Set the default policy on the INPUT chain of the filter table)
	iptables -P OUTPUT ACCEPT 			:(Set the default policy on the OUTPUT chain of the filter table)
	iptables -P FORWARD ACCEPT 			:(Set the default policy on the FORWARD chain of the filter table)
	iptables -t filter -A FORWARD -s 172.24.0.0/24 -d 172.24.1.0/24 -i eth0 -o eth1 -j ACCEPT 
=======================================================================================================
	iptables -A INPUT -i lo -j ACCEPT
	iptables -A OUTPUT -o lo -j ACCEPT
	
	iptables -t filter -A INPUT -p tcp --dport 22 -s 10.18.80.64/26 -j ACCEPT		:This rule must be paired with rule below
	iptables -t filter -A OUTPUT -p tcp --sport 22 -d 10.18.80.64/26 -j ACCEPT		:to properly allow SSH traffic on FW.
	
	iptables -t filter -A INPUT -p tcp --dport 22 -s 10.18.80.64/26 -m state --state NEW,ESTABLISHED,RELATED -j ACCEPT
	iptables -t filter -A OUTPUT -p tcp --sport 22 -d 10.18.80.64/26 -m state --state ESTABLISHED,RELATED -j ACCEPT
=======================================================================================================
	sudo iptables -A INPUT -s 172.24.11.13 -p tcp --dport 22 -j ACCEPT		:Create rule to maintain ssh
	sudo iptables -A OUTPUT -d 172.24.11.13 -p tcp --sport 22 -j ACCEPT	:Create rule to re-establish ssh
	sudo iptables -A INPUT -i lo -j ACCEPT									:loopback rule to communicate with itself
	sudo iptables -A OUTPUT -o lo -j ACCEPT									:
=======================================================================================================
	iptables -I INPUT 1 -s 172.24.11.13 -p tcp --dport 

