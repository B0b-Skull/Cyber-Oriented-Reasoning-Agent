---
title: "Trained Knowledge & Topology: APT28-FANCYBEAR-REPORT.pdf"
tags:
  - arp
  - cve-2015-1641
  - cve-2015-1701
  - cve-2017-11292
  - enumeration
  - http
  - https
  - mdp
  - mimikatz
  - passive_enum
  - pdf
  - post_exploitation_verification
  - responder
  - sysinternals
  - trained
source_file: APT28-FANCYBEAR-REPORT.pdf
doc_type: pdf
updated: 2026-10-25 00:56:13
---

# Trained Knowledge & Architecture: `APT28-FANCYBEAR-REPORT.pdf`

- **Source Path:** `~/Projects/CORA/Training/APT28-FANCYBEAR-REPORT.pdf` (`pdf`)
- **Extracted Technical Entities:** `arp, cve-2015-1641, cve-2015-1701, cve-2017-11292, http, https, mimikatz, responder, sysinternals`
- **Extracted IPs / Subnets:** `2.2.2.1, 2.2.2.2, 2.2.2.3, 2.2.2.4`
- **Extracted Interfaces:** `None`
- **Linked Command Playbook:** [[commands/trained_apt28-fancybear-report]] (`9` CEGAR-verified commands | `9` MDP transitions)

## Command & Tactic Coverage Summary
- **Total CEGAR-Verified Commands:** `9` (full executable list in [[commands/trained_apt28-fancybear-report]])
- **Tactic Distribution:** `Enumeration` (7), `Passive_Enum` (1), `Post_Exploitation_Verification` (1)
- **Top Extracted CLI Tools:** `kill` (6), `.` (2), `groups` (1)

## Document Structure & Key Topics
- Introduction (p. 7)
- Conceptualization and Contextualization (p. 7)
- Societal Dependence on Cyberspace (p. 7)
- Constructs of Technical and Cyber Risk (p. 8)
- Mitigation of Technical and Cyber Risk (p. 8)
- Advanced Persistent Threats (APTs) (p. 8)
- APT Threat Modeling (p. 9)
- Ethical Hacking and Red Teams (p. 9)
- Problem Description (p. 9)
- High Profile and Impactful APT Attacks (p. 9)
- Attribution and Relevance (p. 10)
- Red Team Threat Emulation and Attack Simulation (p. 10)
- Limitations of APT Threat Modeling (p. 10)
- Research Goal (p. 11)
- Levels of Abstraction (p. 11)
- Primary and Sub Questions (p. 12)
- Research Methodology (p. 12)
- Availability of Research Data (p. 12)
- Research Design and Approach (p. 13)
- Incorporating the Guidelines for Design Science (p. 15)
- Thesis Structure (p. 16)
- Modeling Framework (p. 17)
- The Cyber Kill Chain (CKC) (p. 18)
- The Origin of the Cyber Kill Chain (p. 18)
- The Cyber Kill Chain Phases (p. 19)
- The Attacker-Defender Balance (p. 19)
- Defensive Courses of Action (p. 20)
- Cyber Kill Chain variants (p. 20)
- Critiques of the Cyber Kill Chain (p. 20)
- Proposed Improvements and Amendments (p. 21)
- Convergences and Divergences Between Models (p. 23)
- Comparison with Kill Chain Models (p. 25)
- CORAS (p. 26)
- Uniting the Kill Chain Models (p. 27)
- Description of Formation Process (p. 27)
- Description of initial Unified Kill Chain (p. 28)
- Actor Description (p. 29)
- Case Study 1 (C1) (p. 30)
- Attack Visualization (p. 30)
- Attack Analysis (p. 31)
- Attack Specific Kill Chain Formation (p. 33)
- Attack Specific Kill Chains (p. 35)
- Case Study 2 (C2) (p. 36)
- Attack Visualization (p. 36)
- Attack Analysis (p. 37)
- Attack Specific Kill Chain Formation (p. 39)
- Attack Specific Kill Chains (p. 40)
- Case Study 3 (C3) (p. 41)
- Attack Visualization (p. 41)
- Attack Analysis (p. 42)
- Attack Specific Kill Chain Formation (p. 44)
- Attack Specific Kill Chains (p. 46)
- Red Team Actor Specific Kill Chain (p. 47)
- Red Team Kill Chain Formation (p. 47)
- The Red Team Kill Chain (p. 50)
- Validation of Red Team Case Studies (p. 51)
- Actor Description (p. 53)
- APT28 Tactics Analysis (p. 54)
- APT28 Attack Paths and Attack Specific Kill Chains (p. 61)
- APT28 Actor Specific Kill Chain Formation (p. 62)
- APT28 Actor Specific Kill Chain (p. 64)
- Validation of APT28 Case Study (p. 65)
- Results (p. 67)
- Applicability of the Cyber Kill Chain (CKC) (p. 67)
- The Development of the Unified Kill Chain (UKC) (p. 69)
- Applicability of the Unified Kill Chain (UKC) (p. 71)
- Comparison of Red Team and APT28 Attack Specific Kill Chains (p. 72)
- Methodology used to develop the UKC (p. 76)
- Added value of the UKC (p. 76)
- Potential difficulties for the UKC (p. 77)
- Level of abstraction of the UKC (p. 77)
- Broader applicability of the UKC (p. 78)
- Realigning defense strategies with the UKC (p. 79)
- Conclusion (p. 81)
- References (p. 82)
- Red Team Attack Specific Kill Chains (p. 88)
- APT28 Tactics References (p. 97)
- Semi-Structured Interviews (p. 103)
- Glossary (p. 104)
- Unified Kill Chain
- Cyber Kill Chain

## Extracted Operational Steps & Workflows
- 1. To what extent does the CKC allow for a comprehensive tactical comparison of attacker
- 2. What modifications to the CKC are expected to be required to allow for a comprehensive
- 3. To what extent can the tactical MO of Fox-IT’s Red Team be modeled using the UKC?
- 4. To what extent can the tactical MO of APT28 be modeled using the UKC? (chapter 4)
- 5. What are notable convergences or divergences between the CKC, UKC and the tactical MO of
- 6. How can the CKC and Red Team modeling of APT28 attacks be improved? (chapters 5 and 6)
- 1. Design as an Artifact: this research study aims to (re)design purposeful artifacts, namely kill
- 2. Problem Relevance: the goal for the (re)design of the kill chain artifacts is utility, in the form
- 3. Design Evaluation: the UKC that is first (re)designed through a literature study is evaluated
- 4. Research Contributions: the (re)designed kill chain models enable the solution of a
- 5. Research Vigor: to approach the (re)design rigorously, the (re)design process is approached
- 6. Design as a Search Process: the research design allows for the iterative improvement of the
- 7. Communication of Research: this thesis aims to describe the search process for (re)designed
- 1. A threat simulation using Tactics, Techniques and Procedures (TTPs) of real-world attackers;
- 2. A maturity assessment of an organization’s security posture to improve resilience;
- 3. A detectability analysis of actions that were detectable on hosts or the network level;
- 4. A risk analysis of identified vulnerabilities with detailed recommendations for improvements.
- 1. First, the target organization was passively researched through open source intelligence
- 2. The customer specific attack infrastructure was set-up, which included:
- 3. Previously identified employees were targeted via e-mail (a technique known as phishing)
- 4. The targeted employees were enticed to open and enable macro’s in a document that
- 5. The first stage of the payload consisted of a dropper, which downloaded the second stage
- 6. The RAT was dropped into the Startup folder of the affected user, to ensure that the RAT was
- 7. Once the RAT was executed, it connected back to the command and control server and
- 8. Remote access to the compromised workstation allowed the Red Team to actively
- 9. The RAT was initially running with the privileges of a regular user. Through the discovery
- 10. As a local system administrator on a Windows machine, it was possible to extract password
- 11. The compromised workstation was used to tunnel traffic towards other workstations in the
- 12. The compromised local administrator credentials were used to authenticate to other
- 13. Using the information obtained in step 8, the workstation of a specific employee was
- 14. The plain text user level credentials to the supporting asset were extracted from memory on
- 15. The credentials provided the Red Team with remote user level access to the critical
- 16. Command and control of the initially compromised workstation, as obtained in step 7,
- 17. Network segments that contained servers were scanned for open TCP ports, which indicated
- 18. After the discovery of an administrative web interface of a JBoss application server, factory
- 19. Standard functionality in the JBoss application was used to deploy a Web Application
- 20. As a local system administrator on a Windows machine, it was possible to extract password
- 21. The compromised local administrator credentials were used to authenticate to other servers.
- 22. Based on the descriptive hostnames of the affected servers, it could be determined that at
- 23. The administrative access to at least 70 servers, as obtained in step 21, was also used in an
- 24. A Domain Administrator was logged into at least one of the affected servers. Using the local
- 25. The RAT was leveraged to obtain passwords from system memory using the built in mimikatz
- 26. The acquired domain administrator privileges provided administrative access to any
- 1. Phishing foothold – paving a path for user-level access to supporting asset (C1-1)
- 2. Phishing foothold – paving a path for admin-level access to supporting asset (C1-2)

## Extracted Reference Excerpt
--- [Page 1] ---
MODELING 
FANCY BEAR 
CYBER ATTACKS 
Designing a Unified Kill Chain for analyzing, 
comparing and defending against cyber attacks 
 
Author:  
Mr. drs. Paul Pols 
Student ID:  
S1806084 
Date:  
December 7, 2017 
Supervisor:  
Dr. ir. Pieter Burghouwt 
Second Reader:  
Prof. dr. ir. Jan van den Berg 
Institution:  
Cyber Security Academy (CSA) 
 
 
[1]

--- [Page 2] ---
PAUL POLS – MODELING FANCY BEAR CYBER ATTACKS                        . 
p a g e 2 | 104 
Abstract 
Organizations increasingly rely on Information and Communication Technology (ICT), exposing them 
to increasing risks from cyber attacks from a range of threat actors. The term Advanced Persistent 
Threats (APTs) is used to refer to particularly capable threat actors, that are typically backed by 
nation-states. To raise their resilience, organizations can model APT cyber attacks using Lockheed 
Martin’s Cyber Kill Chain® (CKC) or ethical hacking assessments by Red Teams. The modus operandi 
(MO) of APTs does not necessarily coincide with these models, which can limit their predictive value 
and lead to misaligned defensive capabilities and investments. 
In this thesis, a Unified Kill Chain (UKC) model is developed that focuses on the tactics that form the 
consecutive phases of cyber attacks (Table 1). A hybrid research approach is used to develop the 
UKC, combining design science with qualitative research methods. The UKC is first developed through 
literature study, extending the CKC by uniting improvements that were previously proposed by other 
authors with the tactics of MITRE’s ATT&CK™ model. The UKC is subsequently iteratively evaluated 
and improved through case studies of attacks by Fox-IT’s Red Team and APT28 (alias Fancy Bear). The 
resulting UKC is a meta model that supports the development of end-to-end attack specific kill chains 
and actor specific kill chains, that can subsequently be analyzed, compared and defended against. 
 
Table 1 - Overview of the development of the Unified Kill Chain (UKC) 
Cyber Kill Chain® (CKC) 
Laliberte 
Nachreiner 
Bryant 
Malone 
MITRE ATT&CK™ 
UKC after literature study 
UKC after Red Team C1 
UKC after Red Team C2 
UKC after Red Team C3 
UKC after Red Team KC 
UKC after APT28 C4 & KC 
# 
Unified Kill Chain 
1 
Reconnaissance 
1 
1 
1 
1 
1 
1 
1 
1 
1 
1 
1 
2 
Weaponization 
2 
3 
3 
3 
2 
2 
2 
2 
2 
2 
2 
3 
Delivery 
3 
5 
5 
6 
3 
7 
7 
3 
3 
3 
3 
4 
Social Engineering 
5 
6 
6 
11 
5 
3 
3 
4 
4 
4 
4 
5 
Exploitation 
6 
8 
8 
14 
6 
5 
4 
5 
5 
5 
5 
6 
Persistence 
8 
14 
9 
18 
8 
6 
6 
5 
6 
6 
6 
6 
7 
Defense Evasion 
18 
18 
14 
16 
10 
11 
8 
6 
7 
7 
7 
7 
8 
Command & Control  
 
18 
 
5 
7 
9 
8 
8 
8 
8 
8 
9 
Pivoting 
 
 
 
 
11 
13 
11 
9 
9 
9 
9 
9 
10 Discovery 
 
 
 
 
14 
10 
10 
11 
11 
11 
1

