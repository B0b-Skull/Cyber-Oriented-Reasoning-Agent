---
title: "Trained Knowledge & Topology: Solaris-Network-Enum-Script.txt"
tags:
  - active_enum
  - enumeration
  - mdp
  - passive_enum
  - text
  - trained
source_file: Solaris-Network-Enum-Script.txt
doc_type: text
updated: 2026-10-24 01:00:32
---

# Trained Knowledge & Architecture: `Solaris-Network-Enum-Script.txt`

- **Source Path:** `~/Projects/CORA/Training/Solaris-Network-Enum-Script.txt` (`text`)
- **Extracted Technical Entities:** `general`
- **Extracted IPs / Subnets:** `None`
- **Extracted Interfaces:** `None`
- **Linked Command Playbook:** [[commands/trained_solaris-network-enum-script]] (`4` CEGAR-verified commands | `4` MDP transitions)

## Command & Tactic Coverage Summary
- **Total CEGAR-Verified Commands:** `4` (full executable list in [[commands/trained_solaris-network-enum-script]])
- **Tactic Distribution:** `Enumeration` (2), `Active_Enum` (1), `Passive_Enum` (1)
- **Top Extracted CLI Tools:** `echo` (3), `pfiles` (1)

## Document Structure & Key Topics
- Get the process which listens on port
- $1 is the port we are looking for

## Extracted Reference Excerpt
#!/bin/bash
# Get the process which listens on port
# $1 is the port we are looking for
if [ $# -lt 1 ]
then
echo "Please provide a port number parameter for this script"
echo "e.g. $0 22"
exit
fi
echo "Greping for your port, please be patient (CTRL+C breaks) ... "
for i in `ls /proc`
do
pfiles $i | grep AF_INET | grep $1
if [ $? -eq 0 ]
then
echo Is owned by pid $i
fi
done

