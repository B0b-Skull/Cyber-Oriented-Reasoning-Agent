---
title: "Trained Knowledge & Topology: recognizing-suspicious-network-connections-python_12515.pdf"
tags:
  - arp
  - defense_evasion_firewall
  - enumeration
  - http
  - https
  - ipconfig
  - mdp
  - netsh
  - netstat
  - pdf
  - powershell
  - ssh
  - trained
source_file: recognizing-suspicious-network-connections-python_12515.pdf
doc_type: pdf
updated: 2026-10-24 01:00:17
---

# Trained Knowledge & Architecture: `recognizing-suspicious-network-connections-python_12515.pdf`

- **Source Path:** `~/Projects/CORA/Training/recognizing-suspicious-network-connections-python_12515.pdf` (`pdf`)
- **Extracted Technical Entities:** `arp, http, https, ipconfig, netsh, netstat, powershell, ssh`
- **Extracted IPs / Subnets:** `None`
- **Extracted Interfaces:** `None`
- **Linked Command Playbook:** [[commands/trained_recognizing-suspicious-network-connections-python_12515]] (`3` CEGAR-verified commands | `3` MDP transitions)

## Command & Tactic Coverage Summary
- **Total CEGAR-Verified Commands:** `3` (full executable list in [[commands/trained_recognizing-suspicious-network-connections-python_12515]])
- **Tactic Distribution:** `Defense_Evasion_Firewall` (2), `Enumeration` (1)
- **Top Extracted CLI Tools:** `get-content` (1), `netsh` (1), `script` (1)

## Document Structure & Key Topics
- DNS parsing for to record multiple DNS entries and extract/normalize
- Without this loop only the first DNS entry will be returned and the
- signal.signal(signal.SIGINT, signal_handler)

## Extracted Operational Steps & Workflows
- 1. Introduction
- 2. DNS
- 3. TCP Network Connections
- 4. Blocking Direct IP Calls as a Theory
- 5. Scapy and Python
- 6. Simulation
- 7. Proof of Concept Walkthrough and Demonstration
- 8. Conclusion

## Extracted Reference Excerpt
--- [Page 1] ---
Global Information Assurance Certification Paper
Copyright SANS Institute
Author Retains Full Rights
This paper is taken from the GIAC directory of certified professionals. Reposting is not permited without express written permission.
Interested in learning more?
Check out the list of upcoming events offering
"Intrusion Detection In-Depth (Security 503)"
at http://www.giac.org/registration/gcia

--- [Page 2] ---
© 2020 The SANS Institute, Author Retains Full Rights
© 2020 The SANS Institute
Author retains full rights. 
Recognizing Suspicious Network Connections 
with Python 
 GIAC (GCIA) Gold Certification 
Author: Gregory Melton, Gregory.Melton@student.sans.edu 
Advisor: Clay Risenhoover 
Accepted: May 10, 2020 
Abstract 
Endpoint protection solutions tend to focus on system indicators and known malicious 
code to defend both enterprise and Small Office-Home Office (SOHO) users.  In the 
absence of a Security Operations Center (SOC) or paid antivirus services, there are few 
proactive defense options for hobbyists and SOHO owners. A significant problem is how 
advanced persistent threat (APT) actors’ Tactics, Techniques, and Procedures (TTPs) 
have changed over the years; it is common for advanced actors to exploit poorly defended 
subcontractors and seemingly less relevant targets. This brings the Small Office-Home 
Office into the picture as a pivotal defense point against advanced attackers. This 
research intends to focus on attackers using Shell, terminal, or Remote Access Tool 
(RAT) connections to SOHO endpoints. This research seeks to block interactive 
connections with system-level network logging and blacklist automation. This method 
will recognize malicious connections and automatically block them in near real-time.

--- [Page 3] ---
© 2020 The SANS Institute, Author Retains Full Rights
© 2020 The SANS Institute
Author retains full rights. 
 
Recognizing Suspicious Network Connections with Python 
 
2 
 
Melton, Gregory [USA] 
 
1. Introduction 
Meaningful endpoint security against interactive threats is a difficult security 
challenge to manage. Typically, if an attacker obtains a Shell or terminal connection, they 
have already defeated the system’s security protocols. From a developer’s standpoint, it 
may not be worth the effort to wrangle Windows Application Programming Interfaces 
(APIs) against the unlikely occurrence of an interactive threat to home or small office 
users. Unfortunately, APT groups commonly target smaller entities and search for 
backend routes into larger targets by abusing contractor access. By focusing a defensive 
posture on network connections as a chokepoint, it may be possible to create a module 
that recognizes suspicious IP connections and adds said IP address to the system’s 
firewall b

