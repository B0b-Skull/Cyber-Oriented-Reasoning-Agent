---
title: "Trained Knowledge & Topology: Using Netsh.pdf"
tags:
  - enumeration
  - https
  - mdp
  - netsh
  - passive_enum
  - pdf
  - trained
source_file: Using Netsh.pdf
doc_type: pdf
updated: 2026-10-24 01:01:10
---

# Trained Knowledge & Architecture: `Using Netsh.pdf`

- **Source Path:** `~/Projects/CORA/Training/Using Netsh.pdf` (`pdf`)
- **Extracted Technical Entities:** `https, netsh`
- **Extracted IPs / Subnets:** `10.0.0.1, 10.0.0.9, 255.0.0.0`
- **Extracted Interfaces:** `None`
- **Linked Command Playbook:** [[commands/trained_using_netsh]] (`12` CEGAR-verified commands | `12` MDP transitions)

## Command & Tactic Coverage Summary
- **Total CEGAR-Verified Commands:** `12` (full executable list in [[commands/trained_using_netsh]])
- **Tactic Distribution:** `Enumeration` (11), `Passive_Enum` (1)
- **Top Extracted CLI Tools:** `netsh` (11), `prompt` (1)

## Extracted Reference Excerpt
--- [Page 1] ---
11/13/2017
Using Netsh
https://technet.microsoft.com/en­us/library/bb490939(d=printer).aspx
1/10
Using Netsh
Netsh is a command­line scripting utility that allows you to, either locally or remotely, display or modify the
network configuration of a computer that is currently running. Netsh also provides a scripting feature that allows
you to run a group of commands in batch mode against a specified computer. Netsh can also save a
configuration script in a text file for archival purposes or to help you configure other servers.
Netsh contexts
Netsh interacts with other operating system components using dynamic­link library (DLL) files. Each Netsh
helper DLL provides an extensive set of features called a context, which is a group of commands specific to a
networking component. These contexts extend the functionality of netsh by providing configuration and
monitoring support for one or more services, utilities, or protocols. For example, Dhcpmon.dll
provides netsh the context and set of commands necessary to configure and manage DHCP servers.
To run a netsh command, you must start netsh from the Cmd.exe prompt and change to the context that contains
the command you want to use. The contexts that are available to you depend on which networking components
you have installed. For example, if you type dhcp at the Netsh command prompt, you change to the DHCP
context, but if you do not have DHCP installed the following message appears:
The following command was not found: dhcp.
For more information about Netsh contexts, see the following topics:
Netsh commands for AAAA 
Netsh commands for DHCP 
Netsh diagnostic (diag) commands 
Netsh commands for Interface IP 
Netsh commands for RAS 
Netsh commands for Routing 
Netsh commands for WINS 
Top of page 
Using multiple contexts
A context can exist within a context. For example, within the Routing context, you can change to the IP and IPX
subcontexts.
To display a list of commands and subcontexts that you can use within a context, at the netsh prompt, type the
context name, and then type either /? or help. For example, to display a list of subcontexts and commands that
you can use in the Routing context, at the netsh prompt (that is, netsh>), type either of the following:
routing /?
routing help

--- [Page 2] ---
11/13/2017
Using Netsh
https://technet.microsoft.com/en­us/library/bb490939(d=printer).aspx
2/10
To perform tasks in another context without changing from your current context, type the context path of the
command you want to use at the netsh prompt. For example, to add the Local Area Connection interface in the
IGMP context without changing to the IGMP context, at the netsh prompt, type:
routing ip igmp add interface "Local Area Connection" startupqueryinterval=21
Top of page 
Running Netsh 

