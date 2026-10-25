---
title: "Trained Command Playbook: BCF_Windows Live Response.pdf"
tags:
  - auditpol
  - covert_infil
  - defense_evasion_firewall
  - enumeration
  - ipconfig
  - lateral_movement_routing_pivot
  - mdp
  - netsh
  - netstat
  - passive_enum
  - pdf
  - post_exploitation_verification
  - powershell
  - reconnaissance
  - responder
  - trained
  - wevtutil
source_file: BCF_Windows Live Response.pdf
updated: 2026-10-25 00:56:53
---

# Trained Command Playbook: `BCF_Windows Live Response.pdf`

- **Source Document:** `~/Projects/CORA/Training/BCF_Windows Live Response.pdf`
- **CEGAR Verified Commands:** `52` (`0` malformed/unsafe snippets filtered)
- **MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`):** `52`
- **Discovered IPs/Subnets:** `None`
- **Discovered Interfaces:** `None`
- **Related Knowledge Note:** [[knowledge/trained_bcf_windows_live_response]]

## Distilled MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`)
| Pre-State ($s$) | Tactic ($\tau$) | Technique ($k$) | Tool ($u$) | Post-State ($s'$) | Verified Command ($c$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `ipconfig` | `s_active_services_enumerated` | `ipconfig.exe > e:\target1\incidentresponse.txt` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `netstat` | `s_passive_topology_mapped` | `netstat.exe >> e:\target1\incidentresponse.txt` |
| `s_init_unknown` | **`Reconnaissance`** | Domain, DNS, OSINT & Target Footprint Reconnaissance | `copy-item` | `s_passive_topology_mapped` | `Copy-Item <item_to_copy> <desired_location>` |
| `s_cross_subnet_pivot_routed` | **`Post_Exploitation_Verification`** | Post-Action Host Identity, Privilege & Objective Verification | `get-date` | `s_goal_verified_complete` | `Get-Date` |
| `s_protocol_chain_established` | **`Covert_Infil`** | Staged Artifact / Encapsulated Ingress Delivery | `who` | `s_covert_infil_channel_ready` | `Who - Determine what user we are running as.` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `auditpol` | `s_firewall_or_acl_unlocked` | `auditpol /get /category:*` |
| `s_firewall_or_acl_unlocked` | **`Lateral_Movement_Routing_Pivot`** | Remote Host Execution, L2/L3 Route Injection & Subnet Pivot | `net` | `s_cross_subnet_pivot_routed` | `net use \\<ip_address>\<share>` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `set-location` | `s_active_services_enumerated` | `Set-Location <desired_directory>` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `get-help` | `s_passive_topology_mapped` | `Get-Help <command>` |
| `s_init_unknown` | **`Reconnaissance`** | Domain, DNS, OSINT & Target Footprint Reconnaissance | `xcopy` | `s_passive_topology_mapped` | `xcopy /e c:\tools\* i:\evidence` |
| `s_cross_subnet_pivot_routed` | **`Post_Exploitation_Verification`** | Post-Action Host Identity, Privilege & Objective Verification | `whoami` | `s_goal_verified_complete` | `whoami` |
| `s_protocol_chain_established` | **`Covert_Infil`** | Staged Artifact / Encapsulated Ingress Delivery | `get-eventlog` | `s_covert_infil_channel_ready` | `Get-EventLog Security -Newest 20` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `get-netfirewallprofile` | `s_firewall_or_acl_unlocked` | `Get-NetFirewallProfile` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `get-itemproperty` | `s_active_services_enumerated` | `Get-ItemProperty HKLM:\SOFTWARE\MalwareBytes\Antimalware` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `get-help` | `s_passive_topology_mapped` | `Get-Help <command> -Examples` |
| `s_protocol_chain_established` | **`Covert_Infil`** | Staged Artifact / Encapsulated Ingress Delivery | `netstat` | `s_covert_infil_channel_ready` | `netstat -ano` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `netsh` | `s_firewall_or_acl_unlocked` | `netsh advfirewall show allprofiles` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `get-logproperties` | `s_active_services_enumerated` | `Get-LogProperties Security \| Format-List enabled` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `get-help` | `s_passive_topology_mapped` | `Get-Help <command> -Full` |
| `s_protocol_chain_established` | **`Covert_Infil`** | Staged Artifact / Encapsulated Ingress Delivery | `netstat` | `s_covert_infil_channel_ready` | `netstat -anob` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `get-computerinfo` | `s_active_services_enumerated` | `Get-ComputerInfo` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `get-childitem` | `s_passive_topology_mapped` | `Get-ChildItem <desired_directory>` |
| `s_protocol_chain_established` | **`Covert_Infil`** | Staged Artifact / Encapsulated Ingress Delivery | `get-childitem` | `s_covert_infil_channel_ready` | `Get-ChildItem -Path C:\ -recurse \| where-Object {` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `get-nettcpconnection` | `s_active_services_enumerated` | `Get-NetTCPConnection` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `dir` | `s_passive_topology_mapped` | `Dir <desired_directory>` |
| `s_protocol_chain_established` | **`Covert_Infil`** | Staged Artifact / Encapsulated Ingress Delivery | `new-psdrive` | `s_covert_infil_channel_ready` | `New-PSDrive -Name S -PSProvider` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `fsutil` | `s_active_services_enumerated` | `fsutil fsinfo drives` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `get-childitem` | `s_passive_topology_mapped` | `Get-ChildItem <desired_directory> \| sort-object` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `dir` | `s_passive_topology_mapped` | `Dir /od <desired_directory>` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `dir` | `s_passive_topology_mapped` | `Dir /o-d <desired_directory>` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `get-childitem` | `s_passive_topology_mapped` | `Get-ChildItem <desired_directory> \| select-object Name,` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `dir` | `s_passive_topology_mapped` | `Dir /tc <desired_directory>` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `date` | `s_passive_topology_mapped` | `Date /t` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `t` | `s_passive_topology_mapped` | `Time /t` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `systeminfo` | `s_passive_topology_mapped` | `systeminfo` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `dir` | `s_passive_topology_mapped` | `dir /a /s c:\` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `get-process` | `s_passive_topology_mapped` | `Get-Process` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `tasklist` | `s_passive_topology_mapped` | `Tasklist` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `reg` | `s_passive_topology_mapped` | `reg query HKLM\SOFTWARE\KasperskyLab` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `get-childitem` | `s_passive_topology_mapped` | `Get-ChildItem HKLM:\SOFTWARE\KasperskyLab` |

## Verified Executable Commands (Grouped by Capability Layer)

### General_System (47 commands)
```bash
Get-Help <command>
Get-Help <command> -Examples
Get-Help <command> -Full
Set-Location <desired_directory>
Get-ChildItem <desired_directory>
Dir <desired_directory>
Get-ChildItem <desired_directory> | sort-object
Dir /od <desired_directory>
Dir /o-d <desired_directory>
Get-ChildItem <desired_directory> | select-object Name,
Dir /tc <desired_directory>
Copy-Item <item_to_copy> <desired_location>
xcopy /e c:\tools\* i:\evidence
Get-Date
Date /t
Time /t
Who - Determine what user we are running as.
whoami
systeminfo
dir /a /s c:\
Get-Process
Tasklist
Get-ItemProperty HKLM:\SOFTWARE\MalwareBytes\Antimalware
reg query HKLM\SOFTWARE\KasperskyLab
Get-ChildItem HKLM:\SOFTWARE\KasperskyLab
reg query HKLM\SOFTWARE\MalwareBytes\Antimalware
Get-Service | where-object { $_.status -eq 'running'}
Net start
Get-LogProperties Security | Format-List enabled
wevtutil gl security | findstr enabled
Get-EventLog Security -Newest 20
wevtutil qe security /rd:true /c:20 /f:text
auditpol /get /category:*
Get-ComputerInfo
Get-NetTCPConnection
Get-wmiobject Win32_LogicalDisk -Filter 'DriveType=3'
fsutil fsinfo drives
Get-Wmiobject Win32_Processor | select LoadPercentage
Get-wmiobject win32_Service | where-object {
schtasks /query /v /fo list
$names = Get-ChildItem C:\Users | where {$_.name -ne
Get-ChildItem -Path C:\ -recurse | where-Object {
Get-NetFirewallProfile
net use R: \\<ip_address>\<share>
net use * \\<ip_address>\<share>
net use \\<ip_address>\<share>
New-PSDrive -Name S -PSProvider
```

### L3_Routing_NAT (2 commands)
```bash
ipconfig.exe > e:\target1\incidentresponse.txt
netsh advfirewall show allprofiles
```

### L4_Port_Service (3 commands)
```bash
netstat.exe >> e:\target1\incidentresponse.txt
netstat -ano
netstat -anob
```

