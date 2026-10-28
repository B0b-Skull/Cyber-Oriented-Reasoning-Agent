---
title: "Trained Knowledge & Topology: Tasklist.pdf"
tags:
  - credential_access
  - https
  - lateral_movement_routing_pivot
  - mdp
  - passive_enum
  - pdf
  - trained
source_file: Tasklist.pdf
doc_type: pdf
updated: 2026-10-24 01:00:39
---

# Trained Knowledge & Architecture: `Tasklist.pdf`

- **Source Path:** `~/Projects/CORA/Training/Tasklist.pdf` (`pdf`)
- **Extracted Technical Entities:** `https`
- **Extracted IPs / Subnets:** `None`
- **Extracted Interfaces:** `None`
- **Linked Command Playbook:** [[commands/trained_tasklist]] (`7` CEGAR-verified commands | `7` MDP transitions)

## Command & Tactic Coverage Summary
- **Total CEGAR-Verified Commands:** `7` (full executable list in [[commands/trained_tasklist]])
- **Tactic Distribution:** `Lateral_Movement_Routing_Pivot` (3), `Passive_Enum` (3), `Credential_Access` (1)
- **Top Extracted CLI Tools:** `tasklist` (7)

## Extracted Reference Excerpt
--- [Page 1] ---
11/2/2017
Tasklist
https://technet.microsoft.com/en­us/library/bb491010(d=printer).aspx
1/3
Tasklist
Displays a list of applications and services with their Process ID ﴾PID﴿ for all tasks running on either a local or a remote computer.
Syntax
tasklist[.exe] [/s computer] [/u domain\user [/p password]] [/fo {TABLE|LIST|CSV}] [/nh] [/fi FilterName [/fi FilterName2 [ ...
]]] [/m [ModuleName] | /svc | /v] 
Top of page 
Parameters
/s   Computer   : Specifies the name or IP address of a remote computer ﴾do not use backslashes﴿. The default is the local
computer.
/u   Domain \ User   : Runs the command with the account permissions of the user specified by User or Domain\User. The
default is the permissions of the current logged on user on the computer issuing the command.
/p   Password   : Specifies the password of the user account that is specified in the /u parameter.
/fo { TABLE | LIST | CSV } : Specifies the format to use for the output. Valid values are TABLE, LIST, and CSV. The default format
for output is TABLE.
/nh   : Suppresses column headers in the output. Valid when the /fo parameter is set to TABLE or CSV.
/fi   FilterName   : Specifies the types of process﴾es﴿ to include in or exclude from the query. The following table lists valid filter
names, operators, and values.
Name
Operators
Value
Status
eq, ne
RUNNING|NOT RESPONDING
Imagename
eq, ne
Any valid string.
PID
eq, ne, gt, lt,
ge, le
Any valid positive integer.
Session
eq, ne, gt, lt,
ge, le
Any valid session number.
SessionNam
e
eq, ne
Any valid string.
CPUTime
eq, ne, gt, lt,
ge, le
Valid time in the format of hh:mm:ss. The mm and ss parameters should be between 0 and
59 and hh can be any valid unsigned numeric value.
Memusage
eq, ne, gt, lt,
ge, le
Any valid integer.

--- [Page 2] ---
11/2/2017
Tasklist
https://technet.microsoft.com/en­us/library/bb491010(d=printer).aspx
2/3
Username
eq, ne
Any valid user name ﴾[Domain\]User﴿.
Services
eq, ne
Any valid string.
Windowtitle
eq, ne
Any valid string.
Modules
eq, ne
Any valid string.
/m [ ModuleName ] : Specifies to show module information for each process. When a module is specified, all the processes
using that module are shown. When a module is not specified, all the processes for all the modules are shown. Cannot be used
with the /svc or the /v parameter.
/svc   : Lists all the service information for each process without truncation. Valid when the /fo parameter is set to TABLE.
Cannot be used with the /m or the /v parameter.
/v   : Specifies that verbose task information be displayed in the output. Cannot be used with the /svc or the /m parameter.
/? : Displays help at the command prompt.
Top of page 
Remarks
Tasklist is a replacement for the TList tool.
Top of page 
Examples
The following examples show how you can use th

