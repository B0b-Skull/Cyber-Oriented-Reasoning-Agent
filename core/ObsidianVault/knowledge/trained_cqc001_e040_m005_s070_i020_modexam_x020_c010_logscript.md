---
title: "Trained Knowledge & Topology: CQC001_E040_M005_S070_I020_ModExam_X020_C010_LogScript.txt"
tags:
  - http
  - lateral_movement_routing_pivot
  - mdp
  - text
  - trained
source_file: CQC001_E040_M005_S070_I020_ModExam_X020_C010_LogScript.txt
doc_type: text
updated: 2026-10-25 00:57:52
---

# Trained Knowledge & Architecture: `CQC001_E040_M005_S070_I020_ModExam_X020_C010_LogScript.txt`

- **Source Path:** `~/Projects/CORA/Training/CQC001_E040_M005_S070_I020_ModExam_X020_C010_LogScript.txt` (`text`)
- **Extracted Technical Entities:** `http`
- **Extracted IPs / Subnets:** `None`
- **Extracted Interfaces:** `None`
- **Linked Command Playbook:** [[commands/trained_cqc001_e040_m005_s070_i020_modexam_x020_c010_logscript]] (`1` CEGAR-verified commands | `1` MDP transitions)

## Command & Tactic Coverage Summary
- **Total CEGAR-Verified Commands:** `1` (full executable list in [[commands/trained_cqc001_e040_m005_s070_i020_modexam_x020_c010_logscript]])
- **Tactic Distribution:** `Lateral_Movement_Routing_Pivot` (1)
- **Top Extracted CLI Tools:** `get-wmiobject` (1)

## Document Structure & Key Topics
- Script: Query-EventLog.ps1
- Date: 30.May.2007
- Version: 1.0
- Author: Jason Fossen, Perimeter Consulting LLC (http://www.sans.org/sec505)
- Purpose: Demo how to search remote event logs with *server-side* WMI queries.
- Legal: Script provided "AS IS" without warranties or guarantees of any
- kind.  USE AT YOUR OWN RISK.  Public domain, no rights reserved.
- $query = "SELECT * FROM Win32_NTLogEvent WHERE logfile = 'Security' AND EventCode = '528' OR EventCode = '4624'"     # Successful logons.
- $query = "SELECT * FROM Win32_NTLogEvent WHERE logfile = 'Security' AND EventCode = '644'"       # Account lockout.
- $query = "SELECT * FROM Win32_NTLogEvent WHERE logfile = 'Security' AND EventCode = '624'"       # User account created.
- $query = "SELECT * FROM Win32_NTLogEvent WHERE logfile = 'Security' AND EventCode = '627'"       # Password change attempted.
- $query = "SELECT * FROM Win32_NTLogEvent WHERE logfile = 'Security' AND EventCode = '628'"       # Password change successful.
- $query = "SELECT * FROM Win32_NTLogEvent WHERE logfile = 'Security' AND EventCode = '629'"       # User account disabled.
- $query = "SELECT * FROM Win32_NTLogEvent WHERE logfile = 'Security' AND EventCode = '517'"       # Security log cleared.
- $query = "SELECT * FROM Win32_NTLogEvent WHERE logfile = 'Security' AND Type = 'audit failure'"  # Security log failed events.
- $query = "SELECT * FROM Win32_NTLogEvent WHERE logfile = 'System' AND Type = 'Error'"            # System log errors.
- $query = "SELECT * FROM Win32_NTLogEvent WHERE logfile = 'System' AND EventCode = '6008'"        # System log unexpected shutdowns.

## Extracted Reference Excerpt
##############################################################################
#  Script: Query-EventLog.ps1
#    Date: 30.May.2007
# Version: 1.0
#  Author: Jason Fossen, Perimeter Consulting LLC (http://www.sans.org/sec505)
# Purpose: Demo how to search remote event logs with *server-side* WMI queries.
#   Legal: Script provided "AS IS" without warranties or guarantees of any
#          kind.  USE AT YOUR OWN RISK.  Public domain, no rights reserved.
##############################################################################


$computer = "."     # A period indicates the local machine, the default.

$query = "SELECT * FROM Win32_NTLogEvent WHERE logfile = 'Security' AND EventCode = '529' OR EventCode = '4625'"       # Bad username/password.
# $query = "SELECT * FROM Win32_NTLogEvent WHERE logfile = 'Security' AND EventCode = '528' OR EventCode = '4624'"     # Successful logons.
# $query = "SELECT * FROM Win32_NTLogEvent WHERE logfile = 'Security' AND EventCode = '644'"       # Account lockout.
# $query = "SELECT * FROM Win32_NTLogEvent WHERE logfile = 'Security' AND EventCode = '624'"       # User account created.
# $query = "SELECT * FROM Win32_NTLogEvent WHERE logfile = 'Security' AND EventCode = '627'"       # Password change attempted.
# $query = "SELECT * FROM Win32_NTLogEvent WHERE logfile = 'Security' AND EventCode = '628'"       # Password change successful.
# $query = "SELECT * FROM Win32_NTLogEvent WHERE logfile = 'Security' AND EventCode = '629'"       # User account disabled.
# $query = "SELECT * FROM Win32_NTLogEvent WHERE logfile = 'Security' AND EventCode = '517'"       # Security log cleared.
# $query = "SELECT * FROM Win32_NTLogEvent WHERE logfile = 'Security' AND Type = 'audit failure'"  # Security log failed events.
# $query = "SELECT * FROM Win32_NTLogEvent WHERE logfile = 'System' AND Type = 'Error'"            # System log errors.
# $query = "SELECT * FROM Win32_NTLogEvent WHERE logfile = 'System' AND EventCode = '6008'"        # System log unexpected shutdowns.

get-wmiobject -query $query -computername $computer |
select-object RecordNumber,TimeGenerated,ComputerName,LogFile,User,SourceName,EventCode,Type,Message

