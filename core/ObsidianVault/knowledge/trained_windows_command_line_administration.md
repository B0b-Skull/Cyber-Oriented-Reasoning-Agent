---
title: "Trained Knowledge & Topology: windows_command_line_Administration.pdf"
tags:
  - active_enum
  - auditpol
  - bcdedit
  - covert_exfil
  - credential_access
  - defense_evasion_firewall
  - dsquery
  - enumeration
  - http
  - https
  - icacls
  - ipconfig
  - john
  - kerberos
  - lateral_movement_routing_pivot
  - mdp
  - netsh
  - netstat
  - passive_enum
  - pdf
  - post_exploitation_verification
  - serial
  - trained
source_file: windows_command_line_Administration.pdf
doc_type: pdf
updated: 2026-10-25 01:16:25
---

# Trained Knowledge & Architecture: `windows_command_line_Administration.pdf`

- **Source Path:** `~/Projects/CORA/Training/windows_command_line_Administration.pdf` (`pdf`)
- **Extracted Technical Entities:** `auditpol, bcdedit, dsquery, http, https, icacls, ipconfig, john, kerberos, netsh, netstat, serial, ssl, wevtutil, wmic`
- **Extracted IPs / Subnets:** `127.0.0.1, 172.24.0.244`
- **Extracted Interfaces:** `None`
- **Linked Command Playbook:** [[commands/trained_windows_command_line_administration]] (`332` CEGAR-verified commands | `332` MDP transitions)

## Command & Tactic Coverage Summary
- **Total CEGAR-Verified Commands:** `332` (full executable list in [[commands/trained_windows_command_line_administration]])
- **Tactic Distribution:** `Passive_Enum` (123), `Enumeration` (91), `Defense_Evasion_Firewall` (35), `Credential_Access` (27), `Active_Enum` (24), `Post_Exploitation_Verification` (12), `Privilege_Escalation` (12), `Covert_Exfil` (3), `Reconnaissance` (3), `Lateral_Movement_Routing_Pivot` (2)
- **Top Extracted CLI Tools:** `type` (48), `net` (32), `auditpol` (18), `script` (15), `wmic` (14), `dsquery` (11), `wevtutil` (11), `netsh` (10), `echo` (8), `fsutil` (8), `prompt` (8), `reg` (8), `schtasks` (8), `dsadd` (7), `dsget` (7), `dsmod` (7), `icacls` (7), `locate` (7), `bcdedit` (6), `cmdkey` (6), `groups` (6), `sfc` (6), `openfiles` (5), `xcopy` (5), `cscript` (4)

### Visual & Network Diagram Intelligence (`windows_command_line_Administration.pdf#page1`)
- **Spatially Grouped Diagram Nodes (Box/Component Clusters):**
  1. `[John Mueller | Microsoft" | Windows]`
  2. `[Command-Line | Administration]`
  3. `[INSTANT | REFERENCE]`
  4. `[Quick&EasyLookup | ·Real-World Solutions | Answers onthe Spot]`
  5. `[55 | 5 | 50]`
  6. `[40 | 35 | 30]`
  7. `[SYBEX]`
  8. `[SERIOUS SKILLS.]`

### Visual & Network Diagram Intelligence (`windows_command_line_Administration.pdf#page2`)

### Visual & Network Diagram Intelligence (`windows_command_line_Administration.pdf#page3`)
- **Spatially Grouped Diagram Nodes (Box/Component Clusters):**
  1. `[Windows? Command Line | Administration | Instant Reference]`
  2. `[JohnPaul Mueller]`
  3. `[WILEY | Wiley Publishing, Inc.]`

## Document Structure & Key Topics
- Visual & Network Diagram Intelligence (`windows_command_line_Administration.pdf#page1`)
- Visual & Network Diagram Intelligence (`windows_command_line_Administration.pdf#page2`)
- Visual & Network Diagram Intelligence (`windows_command_line_Administration.pdf#page3`)

## Extracted Operational Steps & Workflows
- 1. Command languages (Computer science)—Handbooks, manuals, etc. 2.  Microsoft Windows
- 1. Click the box in the upper left corner of the command window
- 2. Set the properties on each tab to meet speciﬁc needs, such as dis-
- 1. Open a command window.
- 2. Type a command such as CLS or Dir and press Enter.
- 3. Press the Up arrow.
- 4. Press Esc. The command processor clears the command from the
- 5. Type Cmd and press Enter. You’ve just created a new command pro-
- 6. Press the Up arrow. You don’t see anything because this command
- 7. Now, type a different command (such as CLS or Dir) and press
- 8. Press the Up arrow. You’ll see the command you just typed, but
- 9. Press Esc to clear the command.
- 10. Type Exit and press Enter to close the current command proces-
- 11. Press the Up arrow twice and you’ll see whatever command you
- 12. Press Esc to clear the command.
- 13. Type Cmd and press Enter. This action creates a new command pro-
- 14. Press the Up arrow.
- 15. Type Exit and press Enter. You return to the first command
- 16. Type Exit again and press Enter; the command processor window
- 1. Type Net฀User฀YourLoginName฀YourPassword฀/Add and press Enter.
- 2. Type Net฀LocalGroup฀“Administrators”฀YourLoginName฀/Add and
- 3. Type WMIC฀ComputerSystem฀Where฀Name=”%COMPUTERNAME%”฀Call฀
- 4. Type WMIC฀ComputerSystem฀Where฀Name=”%COMPUTERNAME%”฀Call฀
- 5. Type WMIC฀RDToggle฀Where฀ServerName=”%COMPUTERNAME%”฀Call฀
- 6. Type NetSH฀Firewall฀Set฀PortOpening฀TCP฀3389฀“Remote฀Desktop”
- 7. Type Net฀Share฀“Drive_C”=C:\ and press Enter.
- 8. Type CScript฀//H:CScript and press Enter.
- 9. Type SLMGR฀–ATO and press Enter.
- 10. Type Shutdown฀/r and press Enter.
- 1. Choose Start ➢ Control Panel or Start ➢ Settings ➢ Control
- 2. Click System and Security, and then Allow Remote Access in the
- 3. On older systems, check the Enable Remote Desktop on
- 4. Click OK. Windows makes Remote Desktop access available to
- 1. Start the application and click Options.
- 2. Type the server name or select it from the drop-down list in the
- 3. Type your account name on the server in the User Name ﬁeld.
- 4. (Optional) Type your password in the Password ﬁeld (when this
- 5. (Optional) Type the name of the server in the Domain ﬁeld when
- 6. (Optional) Check Allow Me to Save Credentials (or Save My
- 7. Select the Display tab.
- 8. (Optional) Select the Local Resource tab. Make any settings
- 9. (Optional) Select the Programs tab. Check Start the Following
- 10. Select the Experience tab. Choose the connection speed for your
- 11. Clear the checkmarks next to every feature you don’t really need,
- 12. Select the Advanced tab, if your version of Remote Desktop pro-

## Extracted Reference Excerpt
John Mueller
Microsoft"
Windows
Command-Line
Administration
INSTANT
REFERENCE
Quick&EasyLookup
55
5
50
·Real-World Solutions
Answers onthe Spot
40
35
30
SYBEX
SERIOUS SKILLS.

--- [Page 3] ---
Windows
® Command Line 
Administration
Instant Reference
John Paul Mueller

Windows? Command Line
Administration
Instant Reference
JohnPaul Mueller
WILEY
Wiley Publishing, Inc.

--- [Page 4] ---
Acquisitions Editor: Agatha Kim
Development Editor: Jennifer Leland
Technical Editor: Russ Mullen
Production Editor: Liz Britten, Eric Charbonneau
Copy Editor: Cheryl Hauser
Editorial Manager: Pete Gaughan
Production Manager: Tim Tate
Vice President and Executive Group Publisher: Richard Swadley
Vice President and Publisher: Neil Edde
Book Designer: Maureen Forys, Happenstance Type-O-Rama
Compositor: JoAnn Kolonick, Happenstance Type-O-Rama
Proofreader: Jen Larsen, Word One
Indexer: Ted Laux
Project Coordinator, Cover: Lynsey Stanford
Cover Designer: Ryan Sneed
Cover Image: iStockphoto
Copyright © 2010 by Wiley Publishing, Inc., Indianapolis, Indiana
Published simultaneously in Canada
ISBN: 978-0-470-65046-2
No part of this publication may be reproduced, stored in a retrieval system or transmitted in any 
form or by any means, electronic, mechanical, photocopying, recording, scanning or otherwise, 
except as permitted under Sections 107 or 108 of the 1976 United States Copyright Act, without 
either the prior written permission of the Publisher, or authorization through payment of the 
appropriate per-copy fee to the Copyright Clearance Center, 222 Rosewood Drive, Danvers, MA 
01923, (978) 750-8400, fax (978) 646-8600. Requests to the Publisher for permission should be 
addressed to the Permissions Department, John Wiley & Sons, Inc., 111 River Street, Hoboken, NJ 
07030, (201) 748-6011, fax (201) 748-6008, or online at http://www.wiley.com/go/permissions.
Limit of Liability/Disclaimer of Warranty: The publisher and the author make no representations 
or warranties with respect to the accuracy or completeness of the contents of this work and 
speciﬁcally disclaim all warranties, including without limitation warranties of ﬁtness for a particular 
purpose. No warranty may be created or extended by sales or promotional materials. The advice 
and strategies contained herein may not be suitable for every situation. This work is sold with the 
understanding that the publisher is not engaged in rendering legal, accounting, or other professional 
services. If professional assistance is required, the services of a competent professional person should 
be sought. Neither the publisher nor the author shall be liable for damages arising herefrom. The 
fact that an organization or Web site is referred to in this work as a citation and/or a potential source 
of further information do

