---
title: "Trained Knowledge & Topology: Empire.pdf"
tags:
  - credential_access
  - enumeration
  - http
  - https
  - initial_access_exploitation
  - ipconfig
  - kerberos
  - mdp
  - mimikatz
  - out-of-band_access
  - pdf
  - powershell
  - trained
source_file: Empire.pdf
doc_type: pdf
updated: 2026-10-25 00:58:23
---

# Trained Knowledge & Architecture: `Empire.pdf`

- **Source Path:** `~/Projects/CORA/Training/Empire.pdf` (`pdf`)
- **Extracted Technical Entities:** `http, https, ipconfig, kerberos, mimikatz, powershell`
- **Extracted IPs / Subnets:** `None`
- **Extracted Interfaces:** `None`
- **Linked Command Playbook:** [[commands/trained_empire]] (`9` CEGAR-verified commands | `9` MDP transitions)

## Command & Tactic Coverage Summary
- **Total CEGAR-Verified Commands:** `9` (full executable list in [[commands/trained_empire]])
- **Tactic Distribution:** `Enumeration` (4), `Credential_Access` (2), `Initial_Access_Exploitation` (2), `Out-of-Band_Access` (1)
- **Top Extracted CLI Tools:** `empire.db` (2), `kill` (2), `agent.log` (1), `file.txt` (1), `mimikatz` (1), `sekurlsa::logonpasswords` (1), `unset` (1)

## Extracted Reference Excerpt
--- [Page 1] ---
Version 1.0. Created by Will Schroeder (@harmj0y) and Matt Nelson (@enigma0x3) and released under the Creative Commons v3 "Attribution" License. 
           Empire Cheat Sheet 
 
Getting Started 
Get Empire: # git clone 
https://github.com/PowerShellEmpire/Empire or 
download the latest release from 
https://github.com/PowerShellEmpire/Empire/releases  
Run setup: # ./setup/install.sh 
Reset your installation: # ./setup/reset.sh 
Start Empire [in debug mode]: # ./empire [--debug] 
Documentation at: http://www.PowerShellEmpire.com  
Return back to the main Empire menu at any point with 
main, exit with exit (or Ctrl+C). Go back to the previous 
menu with back. Type help at any point for a list of 
commands and their descriptions. 
You can list all agents or listeners from any menu with 
list [agents/listeners] 
To manually edit the backend db: # sqlitebrowser 
./data/empire.db 
Empire has a heavy UI focus with lots of tab-completion. 
Logging and Downloads 
If –debug specified, info in ./empire.debug 
Each agent that checks in has a complete log of 
tasking/results located in: 
./downloads/AGENTNAME/agent.log 
Downloads/other module output for each agent are also 
stored in ./downloads/ AGENTNAME /* 
(Empire: listeners) > 
Change to the listeners menu from any menu location in 
Empire with listeners. This will show the currently active 
listeners (list also shows this). Listeners are preserved in 
./data./empire.db and start back up on Empire startup. 
See the current listener config options: info/options 
Set an option: set OPTION VALUE 
Unset an option: unset OPTION 
Use a particular stager for a given listener: usestager 
[tab] STAGERNAME LISTENER 
To generate a launcher one-liner: launcher LISTENER 
Start a listener with the currently set options: execute 
Kill one (or all) listeners: kill [tab] NAME/all 
KillDate 
Date for the listener to exit 
(MM/dd/yyyy) 
Name 
Name alias to give the 
listener 
DefaultLostLimit 
Number of missed checkins 
before exiting 
Type 
native, pivot, hop, foreign, 
meter 
DefaultDelay 
Agent delay/reach back 
interval (in seconds) 
WorkingHours 
Hours for the agent to 
operate (09:00-17:00) 
Host 
http[s]://HOSTNAME:PORT 
for staging (also takes IP) 
CertPath 
Path to .pem cert to HTTPS 
DefaultJitter 
Jitter in agent reachback 
interval (0.0-1.0). 
(Empire: stager/stager_name) > 
Empire has a modular approach to generating stagers 
(the way you’re going to get code execution on a remote 
machine). You can access these from main or listeners 
with usemodule [tab] STAGER [LISTENER_NAME] 
info/options will display the current option sets, and 
set/unset works similarly to the listener menu. generate 
will generate the current stager/options. 
launcher 
Command one-liner 
launcher_bat 
Self-deleting  .bat

