---
title: "Trained Knowledge & Topology: PS Get-CIM.txt"
tags:
  - credential_access
  - lateral_movement_routing_pivot
  - mdp
  - passive_enum
  - text
  - trained
source_file: PS Get-CIM.txt
doc_type: text
updated: 2026-10-25 01:00:10
---

# Trained Knowledge & Architecture: `PS Get-CIM.txt`

- **Source Path:** `~/Projects/CORA/Training/PS Get-CIM.txt` (`text`)
- **Extracted Technical Entities:** `general`
- **Extracted IPs / Subnets:** `None`
- **Extracted Interfaces:** `None`
- **Linked Command Playbook:** [[commands/trained_ps_get-cim]] (`17` CEGAR-verified commands | `17` MDP transitions)

## Command & Tactic Coverage Summary
- **Total CEGAR-Verified Commands:** `17` (full executable list in [[commands/trained_ps_get-cim]])
- **Tactic Distribution:** `Credential_Access` (7), `Lateral_Movement_Routing_Pivot` (5), `Passive_Enum` (5)
- **Top Extracted CLI Tools:** `get-ciminstance` (8), `get-wmiobject` (3), `get-credential` (2), `new-cimsession` (2), `get-cimclass` (1), `new-cimsessionoption` (1)

## Extracted Reference Excerpt
Get-CimInstance Win32_Process			:Lists processes and PIDS
Get-CimInstance Win32_bios
Get-CimInstance Win32_Service -Filter "State='Running'"
Get-CimInstance -ClassName Win32_Service -filter "State like 'Running'" | select name
winrm quickconfig -q
Get-CimClass | Where {$_.CimClassName -match 'User'}
Get-CimInstance -ClassName Win32_bios | Get-Member
==================================================================================

$c = New-CimSession -ComputerName win10 -Credential fred
$c | Get-CimInstance -ClassName Win32_Service -filter "State like 'Running'"
==================================================================================
$dopt = New-CimSessionOption -Protocol Dcom										:Creates a variable to contain the option for using the DCOM protocol
$d = New-CimSession -ComputerName win7 -Credential fred -SessionOption $dopt	:Create the variable containing the session declaring the protocol to use
==================================================================================
Get-CimInstance -query "select * from Win32_Service where startmode='disabled'" | select name
==================================================================================
$c = Get-Credential
	fred/Gr@vel
$p = Get-Credential
	barney/Rubbl3
==================================================================================
Uninstall 'Google update Helper'
	$appToRemove = Get-WmiObject Win32_Product -computername win7 -credential $c -Filter "Name like '%Helper'"
	$appToRemove.Uninstall()
	OR
	(Get-WmiObject Win32_Product -computername win7 -credential $c -filter "Name like '%Helper'").Uninstall()

-Verify removed:
	Get-WmiObject Win32_Product -computername Win7 -credential $c -Filter "Name like '%Helper'"
	Get-CimInstance Win32_Process -Filter "Name='Spooler'"
	
	$service = Get-CimInstance Win32_Process -Filter "Name='Spooler'"
	$service.state
	$service.startservice()

