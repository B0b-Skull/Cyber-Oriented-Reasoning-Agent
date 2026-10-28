---
title: "Trained Command Playbook: Triage-Scripts.txt"
tags:
  - arp
  - enumeration
  - ipconfig
  - mdp
  - netstat
  - passive_enum
  - post_exploitation_verification
  - powershell
  - text
  - trained
  - wmic
source_file: Triage-Scripts.txt
updated: 2026-10-24 01:00:41
---

# Trained Command Playbook: `Triage-Scripts.txt`

- **Source Document:** `~/Projects/CORA/Training/Triage-Scripts.txt`
- **CEGAR Verified Commands:** `40` (`0` malformed/unsafe snippets filtered)
- **MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`):** `40`
- **Discovered IPs/Subnets:** `None`
- **Discovered Interfaces:** `None`
- **Related Knowledge Note:** [[knowledge/trained_triage-scripts]]

## Distilled MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`)
| Pre-State ($s$) | Tactic ($\tau$) | Technique ($k$) | Tool ($u$) | Post-State ($s'$) | Verified Command ($c$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `wmic` | `s_passive_topology_mapped` | `wmic process where "name='apnmcp.exe'" get ProcessID, ExecutablePath /FORMAT:LIST` |
| `s_cross_subnet_pivot_routed` | **`Post_Exploitation_Verification`** | Post-Action Host Identity, Privilege & Objective Verification | `hostname` | `s_goal_verified_complete` | `hostname` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `get-date` | `s_active_services_enumerated` | `$FindDate=Get-Date -Year 2016 -Month 06 -Day 24` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `get-process` | `s_passive_topology_mapped` | `get-process apnmcp \| select -expand modules` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `netstat` | `s_passive_topology_mapped` | `netstat -naob` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `date` | `s_passive_topology_mapped` | `date /t` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `t` | `s_passive_topology_mapped` | `time /t` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `dir` | `s_passive_topology_mapped` | `dir /t:c text.txt` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `ver` | `s_passive_topology_mapped` | `ver` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `net` | `s_passive_topology_mapped` | `net session` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `psloglist` | `s_passive_topology_mapped` | `psloglist "Security" -i 528 -s \| find /i "Logon Type: 10"` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `net` | `s_passive_topology_mapped` | `net statistics {Server\|Workstation}` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `systeminfo` | `s_passive_topology_mapped` | `systeminfo` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `ipconfig` | `s_passive_topology_mapped` | `ipconfig` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `arp` | `s_passive_topology_mapped` | `arp -a` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `route` | `s_passive_topology_mapped` | `route print` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `fport` | `s_passive_topology_mapped` | `fport` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `wmic` | `s_passive_topology_mapped` | `wmic datafile where name='c:\\windows\\system32\\calc.exe'` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `tasklist` | `s_passive_topology_mapped` | `tasklist` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `tasklist` | `s_passive_topology_mapped` | `tasklist /fi "PID eq xxxx"` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `wmic` | `s_passive_topology_mapped` | `wmic process list` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `netstat` | `s_passive_topology_mapped` | `netstat -anob` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `wmic` | `s_passive_topology_mapped` | `wmic process where (processid=xxxx) get parentprocessid` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `wmic` | `s_passive_topology_mapped` | `wmic process where "name='program.exe'" get ProcessID, ExecutablePath /FORMAT:LIST` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `wmic` | `s_passive_topology_mapped` | `wmic datafile where name='c:\\Program Files\\VMware\\VMware Tools\\vmtoolsd.exe'` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `wmic` | `s_passive_topology_mapped` | `wmic datafile where name='c:\\program files\\vmware\\vmware tools\\vmtoolsd.exe' get creationdate, installdate, lastmodified` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `get-childitem` | `s_passive_topology_mapped` | `Get-Childitem "C:\Program Files\Vmware\VMware tools\vmtoolsd.exe" \| Select Name, CreationTime, LastWriteTime, LastAccessTime` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `get-windowspackage` | `s_passive_topology_mapped` | `Get-WindowsPackage -Online \| ?{ $_.InstallTime -gt [datetime]::now.AddDays(-15) }` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `wmic` | `s_passive_topology_mapped` | `WMIC process where "name='explorer.exe'" get /FORMAT:list` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `netstat` | `s_passive_topology_mapped` | `netstat -naob \| findstr :23` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `dir` | `s_passive_topology_mapped` | `dir C:\ /s /b \| find /i "tlntsvr.exe"` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `dir` | `s_passive_topology_mapped` | `dir C:\ /s /b \| find /i "firefox.exe"` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `wmic` | `s_passive_topology_mapped` | `WMIC datafile where "name='C:\\Program Files (x86)\\Mozilla Firefox\\firefox.exe'" GET installdate, CREATIONDATE, lastmodified` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `get-childitem` | `s_passive_topology_mapped` | `Get-ChildItem -Path C:\ -Include *.doc,*.docx -Recurse -ErrorAction SilentlyContinue \| Where-Object { $_.LastWriteTime -ge $FindDate }` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `get-childitem` | `s_passive_topology_mapped` | `Get-ChildItem -Path C:\ -Include *.doc,*.docx -File -Recurse -ErrorAction SilentlyContinue \| Where-Object { $_.LastWriteTime -ge $FindDate -and $_.LastWriteTime -le $Finddate.adddays(1) }` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `dir` | `s_passive_topology_mapped` | `dir c:\users -recurse \| Select Fullname,CreationTime,LastWriteTime,	@{Name="Age";Expression={(Get-Date)-$_.LastWriteTime}},	@{Name="Days";Expression={[int]((Get-Date) -$_.LastWriteTime).TotalDays}}, @{Name="Owner";Expression={(Get-ACL $_.fullname).Owner}} \| Where {$_.Days -lt 40} \| Sort Days -Descending` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `dir` | `s_passive_topology_mapped` | `dir C:\users -recurse \| select Fullname,CreationDate,LastWriteTime, @{Name="Age";Expression={(Get-Date)-$_.LastWriteTime}},	@{Name="Days";Expression={[int]((Get-Date) -$_.LastWriteTime).TotalDays}}, @{Name="Owner";Expression={(Get-ACL $_.fullname).Owner}} \| Where {$_.Days -lt 40} \| Sort Days -Descending` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `dir` | `s_passive_topology_mapped` | `dir C:\users -recurse \| select fullname,CreationDate,LastWriteTime, @{Name="Age";Expression={(Get-Date)-$_.LastWriteTime}},	@{Name="Days";Expression={[int]((Get-Date) -$_.LastWriteTime).TotalDays}}, @{Name="Owner";Expression={(Get-ACL $_.fullname).Owner}} \| where {$_.CreationDate -gt "11/01/2017" -and $_.CreationDate -le "11/29/2017"} \| sort days -Descending` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `dir` | `s_passive_topology_mapped` | `dir C:\*.* /s /q /t:{c\|w\|a}\| find /i "username"` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `dir` | `s_passive_topology_mapped` | `dir c:\Users /s /t:{c\|w\|a} \| find "11/13/2009"` |

## Verified Executable Commands (Grouped by Capability Layer)

### General_System (33 commands)
```bash
wmic process where "name='apnmcp.exe'" get ProcessID, ExecutablePath /FORMAT:LIST
get-process apnmcp | select -expand modules
date /t
time /t
dir /t:c text.txt
ver
net session
psloglist "Security" -i 528 -s | find /i "Logon Type: 10"
net statistics {Server|Workstation}
systeminfo
hostname
wmic datafile where name='c:\\windows\\system32\\calc.exe'
tasklist
tasklist /fi "PID eq xxxx"
wmic process list
wmic process where (processid=xxxx) get parentprocessid
wmic process where "name='program.exe'" get ProcessID, ExecutablePath /FORMAT:LIST
wmic datafile where name='c:\\Program Files\\VMware\\VMware Tools\\vmtoolsd.exe'
wmic datafile where name='c:\\program files\\vmware\\vmware tools\\vmtoolsd.exe' get creationdate, installdate, lastmodified
Get-Childitem "C:\Program Files\Vmware\VMware tools\vmtoolsd.exe" | Select Name, CreationTime, LastWriteTime, LastAccessTime
Get-WindowsPackage -Online | ?{ $_.InstallTime -gt [datetime]::now.AddDays(-15) }
WMIC process where "name='explorer.exe'" get /FORMAT:list
dir C:\ /s /b | find /i "tlntsvr.exe"
dir C:\ /s /b | find /i "firefox.exe"
WMIC datafile where "name='C:\\Program Files (x86)\\Mozilla Firefox\\firefox.exe'" GET installdate, CREATIONDATE, lastmodified
$FindDate=Get-Date -Year 2016 -Month 06 -Day 24
Get-ChildItem -Path C:\ -Include *.doc,*.docx -Recurse -ErrorAction SilentlyContinue | Where-Object { $_.LastWriteTime -ge $FindDate }
Get-ChildItem -Path C:\ -Include *.doc,*.docx -File -Recurse -ErrorAction SilentlyContinue | Where-Object { $_.LastWriteTime -ge $FindDate -and $_.LastWriteTime -le $Finddate.adddays(1) }
dir c:\users -recurse | Select Fullname,CreationTime,LastWriteTime,	@{Name="Age";Expression={(Get-Date)-$_.LastWriteTime}},	@{Name="Days";Expression={[int]((Get-Date) -$_.LastWriteTime).TotalDays}}, @{Name="Owner";Expression={(Get-ACL $_.fullname).Owner}} | Where {$_.Days -lt 40} | Sort Days -Descending
dir C:\users -recurse | select Fullname,CreationDate,LastWriteTime, @{Name="Age";Expression={(Get-Date)-$_.LastWriteTime}},	@{Name="Days";Expression={[int]((Get-Date) -$_.LastWriteTime).TotalDays}}, @{Name="Owner";Expression={(Get-ACL $_.fullname).Owner}} | Where {$_.Days -lt 40} | Sort Days -Descending
dir C:\users -recurse | select fullname,CreationDate,LastWriteTime, @{Name="Age";Expression={(Get-Date)-$_.LastWriteTime}},	@{Name="Days";Expression={[int]((Get-Date) -$_.LastWriteTime).TotalDays}}, @{Name="Owner";Expression={(Get-ACL $_.fullname).Owner}} | where {$_.CreationDate -gt "11/01/2017" -and $_.CreationDate -le "11/29/2017"} | sort days -Descending
dir C:\*.* /s /q /t:{c|w|a}| find /i "username"
dir c:\Users /s /t:{c|w|a} | find "11/13/2009"
```

### L2_ARP_Link (1 commands)
```bash
arp -a
```

### L3_Routing_NAT (2 commands)
```bash
ipconfig
route print
```

### L4_Port_Service (4 commands)
```bash
netstat -naob
fport
netstat -anob
netstat -naob | findstr :23
```

