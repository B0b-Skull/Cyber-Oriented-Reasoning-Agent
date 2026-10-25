---
title: "Trained Knowledge & Topology: Systeminfo.pdf"
tags:
  - credential_access
  - https
  - mdp
  - passive_enum
  - pdf
  - trained
source_file: Systeminfo.pdf
doc_type: pdf
updated: 2026-10-25 01:00:38
---

# Trained Knowledge & Architecture: `Systeminfo.pdf`

- **Source Path:** `~/Projects/CORA/Training/Systeminfo.pdf` (`pdf`)
- **Extracted Technical Entities:** `https`
- **Extracted IPs / Subnets:** `None`
- **Extracted Interfaces:** `None`
- **Linked Command Playbook:** [[commands/trained_systeminfo]] (`4` CEGAR-verified commands | `4` MDP transitions)

## Command & Tactic Coverage Summary
- **Total CEGAR-Verified Commands:** `4` (full executable list in [[commands/trained_systeminfo]])
- **Tactic Distribution:** `Credential_Access` (3), `Passive_Enum` (1)
- **Top Extracted CLI Tools:** `systeminfo` (4)

## Extracted Reference Excerpt
--- [Page 1] ---
11/13/2017
Systeminfo
https://technet.microsoft.com/en­us/library/bb491007.aspx
1/1
Systeminfo
Displays detailed configuration information about a computer and its operating system, including operating
system configuration, security information, product ID, and hardware properties, such as RAM, disk space, and
network cards.
Syntax
systeminfo[.exe] [/s Computer [/u Domain\User [/p Password]]] [/fo {TABLE|LIST|CSV}] [/nh]
Top of page 
Parameters
/s   Computer   : Specifies the name or IP address of a remote computer (do not use backslashes). The default is
the local computer.
/u   Domain \ User   : Runs the command with the account permissions of the user specified
by User or Domain\User. The default is the permissions of the current logged on user on the computer issuing
the command.
/p   Password   : Specifies the password of the user account that is specified in the /u parameter.
/fo { TABLE | LIST | CSV } : Specifies the format to use for the output. Valid values are TABLE, LIST,
and CSV. The default format for output is LIST.
/nh   : Suppresses column headers in the output. Valid when the /fo parameter is set to TABLE or CSV.
/? : Displays help at the command prompt.
Top of page 
Examples
The following examples show how you can use the systeminfo command:
systeminfo.exe /s srvmain 
systeminfo.exe /s srvmain /u maindom\hiropln 
systeminfo /s srvmain /u maindom\hiropln /p p@ssW23 /fo table

