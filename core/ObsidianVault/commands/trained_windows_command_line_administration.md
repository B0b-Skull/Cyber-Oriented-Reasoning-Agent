---
title: "Trained Command Playbook: windows_command_line_Administration.pdf"
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
updated: 2026-10-25 01:16:25
---

# Trained Command Playbook: `windows_command_line_Administration.pdf`

- **Source Document:** `~/Projects/CORA/Training/windows_command_line_Administration.pdf`
- **CEGAR Verified Commands:** `332` (`0` malformed/unsafe snippets filtered)
- **MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`):** `332`
- **Discovered IPs/Subnets:** `127.0.0.1, 172.24.0.244`
- **Discovered Interfaces:** `None`
- **Related Knowledge Note:** [[knowledge/trained_windows_command_line_administration]]

## Distilled MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`)
| Pre-State ($s$) | Tactic ($\tau$) | Technique ($k$) | Tool ($u$) | Post-State ($s'$) | Verified Command ($c$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `locate` | `s_active_services_enumerated` | `Locate Information in Files` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `prompt` | `s_passive_topology_mapped` | `prompt so you have a blank prompt to use.` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `takeown` | `s_interactive_tty_or_priv_escalated` | `TakeOwn utility described in the "Take Ownership of Files" section of` |
| `s_cross_subnet_pivot_routed` | **`Post_Exploitation_Verification`** | Post-Action Host Identity, Privilege & Objective Verification | `openfiles` | `s_goal_verified_complete` | `OpenFiles utility. The following sections describe this utility in more` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `type` | `s_credentials_or_certs_acquired` | `type /MinPWAge:0.` |
| `s_passive_topology_mapped` | **`Active_Enum`** | Active Network, Cloud, Directory Service & Endpoint Probing | `pathping` | `s_active_services_enumerated` | `PathPing to perform an IPv6 test by using the -6 command line switch.` |
| `s_interactive_tty_or_priv_escalated` | **`Covert_Exfil`** | Encapsulated / Low-Signature Data Telemetry Transfer | `ntdsutil` | `s_covert_exfil_verified` | `NTDSUtil prompt always exits the application.` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `bcdedit` | `s_firewall_or_acl_unlocked` | `BCDEdit Help (Page 316)` |
| `s_init_unknown` | **`Reconnaissance`** | Domain, DNS, OSINT & Target Footprint Reconnaissance | `cscript` | `s_passive_topology_mapped` | `CScript and WScript Utilities` |
| `s_firewall_or_acl_unlocked` | **`Lateral_Movement_Routing_Pivot`** | Remote Host Execution, L2/L3 Route Injection & Subnet Pivot | `route` | `s_cross_subnet_pivot_routed` | `Route Add command, 181–182` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `locate` | `s_active_services_enumerated` | `Locate Bad Sectors` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `type` | `s_passive_topology_mapped` | `type Set฀PATH=฀%PATH%;C:\ and press Enter.` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `echo` | `s_interactive_tty_or_priv_escalated` | `Echo Command (Page 406)` |
| `s_cross_subnet_pivot_routed` | **`Post_Exploitation_Verification`** | Post-Action Host Identity, Privilege & Objective Verification | `groups` | `s_goal_verified_complete` | `Groups make it simpler to manage security and perform other user-` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `type` | `s_credentials_or_certs_acquired` | `type Net฀Accounts฀/MinPWLen:7฀/MaxPWAge:90฀/MinPWAge:30฀/` |
| `s_passive_topology_mapped` | **`Active_Enum`** | Active Network, Cloud, Directory Service & Endpoint Probing | `rpcping` | `s_active_services_enumerated` | `RPCPing to check connectivity to the Exchange Server installed` |
| `s_interactive_tty_or_priv_escalated` | **`Covert_Exfil`** | Encapsulated / Low-Signature Data Telemetry Transfer | `script` | `s_covert_exfil_verified` | `script related, 507–510` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `bcdedit` | `s_firewall_or_acl_unlocked` | `BCDEdit incorrectly can cause signiﬁcant` |
| `s_init_unknown` | **`Reconnaissance`** | Domain, DNS, OSINT & Target Footprint Reconnaissance | `cscript` | `s_passive_topology_mapped` | `CScript and WScript use the same command line. You must provide` |
| `s_firewall_or_acl_unlocked` | **`Lateral_Movement_Routing_Pivot`** | Remote Host Execution, L2/L3 Route Injection & Subnet Pivot | `route` | `s_cross_subnet_pivot_routed` | `Route Change command, 182–183` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `locate` | `s_active_services_enumerated` | `Locate and Fix Minor Problems` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `type` | `s_passive_topology_mapped` | `type ShutDown฀/G and press Enter. Most applications will automatically` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `dsmod` | `s_interactive_tty_or_priv_escalated` | `DSMod Group command, 246` |
| `s_cross_subnet_pivot_routed` | **`Post_Exploitation_Verification`** | Post-Action Host Identity, Privilege & Objective Verification | `groups` | `s_goal_verified_complete` | `Groups help organize users and make it easier to perform tasks such as` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `groups` | `s_credentials_or_certs_acquired` | `Groups come in two forms for the Net utility. You can either work with` |
| `s_passive_topology_mapped` | **`Active_Enum`** | Active Network, Cloud, Directory Service & Endpoint Probing | `dsquery` | `s_active_services_enumerated` | `DSQuery Utility` |
| `s_interactive_tty_or_priv_escalated` | **`Covert_Exfil`** | Encapsulated / Low-Signature Data Telemetry Transfer | `ntdsutil` | `s_covert_exfil_verified` | `NTDSUtil (NT Directory Services utility),` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `type` | `s_firewall_or_acl_unlocked` | `type BCDEdit฀/Set฀{bootmgr}฀default฀{ntldr} and press Enter.` |
| `s_init_unknown` | **`Reconnaissance`** | Domain, DNS, OSINT & Target Footprint Reconnaissance | `script` | `s_passive_topology_mapped` | `Script Host Resources site at http://labmice.techtarget.com/script-` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `script` | `s_active_services_enumerated` | `Script the Command Line and System Environment` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `wmic` | `s_passive_topology_mapped` | `WMIC command is one of the most powerful con-` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `icacls` | `s_interactive_tty_or_priv_escalated` | `ICACLS utility, 127–128, 128` |
| `s_cross_subnet_pivot_routed` | **`Post_Exploitation_Verification`** | Post-Action Host Identity, Privilege & Objective Verification | `groups` | `s_goal_verified_complete` | `groups manually, except when you rely on one of the built-in groups` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `groups` | `s_credentials_or_certs_acquired` | `groups at the domain level using the Net฀Group subcommand or the` |
| `s_passive_topology_mapped` | **`Active_Enum`** | Active Network, Cloud, Directory Service & Endpoint Probing | `ping` | `s_active_services_enumerated` | `ping -c 3 utility. A special NetSH฀Diag฀GUI command` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `type` | `s_firewall_or_acl_unlocked` | `type AuditPol฀/Remove฀/User:Username, where Username is a particular` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `script` | `s_active_services_enumerated` | `Script the Registry` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `schtasks` | `s_passive_topology_mapped` | `SchTasks command.` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `icacls` | `s_interactive_tty_or_priv_escalated` | `ICACLS /Deny command, 131` |
| `s_cross_subnet_pivot_routed` | **`Post_Exploitation_Verification`** | Post-Action Host Identity, Privilege & Objective Verification | `groups` | `s_goal_verified_complete` | `groups` |

## Verified Executable Commands (Grouped by Capability Layer)

### General_System (304 commands)
```bash
Locate Information in Files
Locate Bad Sectors
Locate and Fix Minor Problems
Script the Command Line and System Environment
Script the Registry
Script Registry Entries
Script Networking Solutions
prompt so you have a blank prompt to use.
type Set฀PATH=฀%PATH%;C:\ and press Enter.
type ShutDown฀/G and press Enter. Most applications will automatically
WMIC command is one of the most powerful con-
SchTasks command.
locate any directory that begins with Win starting from the current location.
Type .. to move to the parent level of the current directory.
type Dir฀/A–D and press Enter.
XCopy to perform a basic file copy. XCopy is a relatively complex com-
XCopy copies them.
XCopy copies the files from the source directory to the target.
type Ren฀Temp.TXT฀NewName.TXT and press Enter.
handle certain kinds of files. The following sections describe these two
type FindStr฀/M฀/S฀"Microsoft"฀*.EXE฀>฀MicrosoftEXE.TXT and press
type FSUtil฀FSInfo฀VolumeInfo฀C: and press Enter, you see the statistics
type FSUtil฀Quota฀Query฀C: and press Enter, you see the current quota
prompt extends to request any additional information. Figure 5.2 shows
type Compact฀/C฀/S฀/I฀C:\MyDir\*.* and press Enter.
type Label฀D:฀Accounting and press Enter. You can change the label
mount points by specifying the /M command line switch.
type Cipher฀/E฀C:\MyDir and press Enter. However, this command only
Write-only access
TakeOwn utility described in the "Take Ownership of Files" section of
OpenFiles utility. The following sections describe this utility in more
type /MinPWAge:0.
type Net฀Accounts฀/MinPWLen:7฀/MaxPWAge:90฀/MinPWAge:30฀/
Groups come in two forms for the Net utility. You can either work with
groups at the domain level using the Net฀Group subcommand or the
Groups make it simpler to manage security and perform other user-
type Net฀LocalGroup฀MyGroup฀/Delete and press Enter.
type Net฀LocalGroup฀MyGroup฀John฀/Delete and press Enter.
type Net฀Config฀Server฀/SrvComment:"" and press Enter.
type Net฀File and press Enter. The output of this subcommand displays
Type Y and press Enter to complete the task.
Type IPConfig฀/? and press Enter to see a complete list of display options.
type PathPing฀www.mwt.net and press Enter. Figure 9.4 shows typical
locate specific issues, such as checking DNS for problems. In fact,
type NetDiag and press Enter. You might decide that you want the utility
type Route฀Delete฀172.24.0.244 and press Enter.
type WinRM฀Delete฀WinRM/Config/Listener?Address=*+Transport=HTT
WMIC NTDomain Alias
WMIC outputs the usual help information. In addition, at the bottom
DSQuery Utility
type DSQuery฀Server and press Enter. DSQuery will output a list of all of
Locate a Hidden Server
Echo when working with scripts
Groups help organize users and make it easier to perform tasks such as
NTDSUtil prompt always exits the application.
DSAdd commands work with remote systems as
groups manually, except when you rely on one of the built-in groups
type them together as a single entry, such as JSmith@MyDomain.com.
type DSGet฀Server฀DN฀-topobjowner฀Display, where Display is the number
DSMod commands work with remote systems as
DSRm utility. Type DSRm฀/? and press Enter to see a complete list of these
type LogMan฀Delete฀MyCounter and press Enter.
WMIC (Page 287)
WMIC (Page 290)
WMIC (Page 302)
WMIC (Page 306)
WMIC (Page 310)
BCDEdit Help (Page 316)
type WMIC฀Product฀Where฀Name="Microsoft฀Help฀Viewer฀1.0"฀List
type WMIC฀OS฀GET฀Caption,฀BuildNumber and press Enter.
type WMIC฀Product฀Where฀Name="ProductName"฀Call฀Configure and
type WMIC฀CPU฀LIST฀/Format:HTable฀>฀MyCPU2.HTML and press Enter instead
BCDEdit incorrectly can cause signiﬁcant
type BCDEdit฀/Set฀{bootmgr}฀default฀{ntldr} and press Enter.
Prompt shortcut and choose Run as Administrator from the
type AuditPol฀/Remove฀/User:Username, where Username is a particular
TaskKill and TaskList Filters (Page 347)
SFC utility presented in this chapter
type SecEdit฀/Export฀/Cfg฀Cfg.TXT฀/MergedPolicy and press Enter.
type SecEdit฀/Import฀/DB฀SecEdit.SDB฀/Cfg฀CFG.TXT and press Enter to
locate applications that have just
type CScript฀%WinDir%\System32\SCRegEdit.WSF฀/AR฀/V and press Enter.
type CScript฀%WinDir%\System32\SCRegEdit.WSF฀/AR฀0 and press Enter.
type CScript฀%WinDir%\System32\SCRegEdit.WSF฀/AR฀1 and press Enter.
type Reg฀Query฀/? and press Enter to learn more about the Query opera-
type Reg฀Query฀"HKCU\Control฀Panel\Colors"฀/V฀ActiveTitle and press
type Reg฀Compare฀HKCU\Software\MyData฀HKCU\Software\MyData2 and
type REG_DWORD.
prompt or by using any of the usual techniques, such as the Start menu.
Type field output when you list credentials for your system. The follow-
CmdKey also supports smartcards. In this case, you use the CmdKey฀/
type CmdKey฀/Delete:Aux to remove the credential.
type Time฀12:01฀PM and press Enter.
prompt window you create. The title that a command window displays
Echo Command (Page 406)
ForFiles Utility (Page 407)
Prompt Command (Page 418)
echo off, type Echo฀Off and press Enter. Type Echo and press Enter to
XCopy error levels shown in Table 21.1.
Echo command to display an error message to the user—Echo works not
echo on is the default setting.
PushD and PopD Commands
PopD command treats the networked drive as it would any other mapped
CScript and WScript Utilities
type library file appears. The <reference> element accesses the external
script file you create.
CScript and WScript use the same command line. You must provide
type CSript฀//I฀Test.JS.
script one command at a time to see how it works. There are actu-
Script Host Settings dialog box shown in Figure 22.1. Type WScript and
WSCRIPT OBJECT (Pages 449–454)
WScript Properties (Page 449)
WScript Methods (Page 451)
script at the command line. The following sections tell you about the
script engines is outside the scope of this book.
type ChgPort฀/D฀LocalName and press Enter.
script useful for everyone. Notice how the code detects the number of
script version of the CSV output example.
PopD Commands
TaskList
Ver
DSQuery utility, 218–224
groups
AuditPol /Get /Subcategory command, 322,
AuditPol /Get /User command, 321–323
AuditPol /List command, 321
AuditPol /List /Category command, 321
AuditPol /List /Subcategory, 322
AuditPol /List /User command, 321
AuditPol /Remove /AllUsers command, 328
AuditPol /Remove /User command, 328
AuditPol /Restore /File command, 327
AuditPol /Set /Category command, 326–327
AuditPol /Set /Option command, 327
AuditPol /Set /Subcategory command, 327
AuditPol /Set /User command, 326
ForFiles loops, 407
Echo command, 220, 406
AuditPol utility, 320
AuditPol /Backup command, 327
AuditPol /Clear command, 328
AuditPol /Get /Category command,
AuditPol /Get /Option command, 324, 326
CmdKey utility
CMD /C command, 372–373
CMD /K command, 373
CmdKey utility, 393
BCDEdit /Enum command, 315
BCDEdit /Export command, 315
BCDEdit /Set command, 317–318
BCDEdit help, 316–317
script related, 507–510
CmdKey /Add command, 394
CmdKey /Delete command, 394–395
CmdKey /List command, 393–394, 393
CScript utility, 27, 442
Dir /A command, 65–66
Dir /AD command, 58–59
Dir /O command, 65
DSRm utility, 248–249
Echo command, 220, 426
Echo method in WScript, 453
DSAdd (Directory Services Add) utility, 230
DSAdd Computer command, 231
DSAdd Contact command, 231–237
DSAdd DomainRoute command, 224
DSAdd Group command, 224, 233–234
DSAdd OU command, 224, 234
DSGet utility, 218, 220–221, 238
DSGet Computer command, 238–239
DSGet Contact command, 239–240
DSGet Group command, 240–241
DSGet OU command, 241
DSGet Server command, 241
DSGet User command, 221–222, 242–243
DSMod utility, 222, 243–244
DSMod Computer command, 244–245
DSMod Contact command, 245
DSMod Group command, 246
DSMod OU command, 246
DSMod User command, 222, 246–248
DSQuery (Directory Services Query) utility,
DSQuery Computer command, 223
DSQuery Contact command, 223
DSQuery DomainRoot command, 224
DSQuery Group command, 224
DSQuery OU command, 224
DSQuery Server /Domain command, 219
DSQuery Server /Forest command, 218
DSQuery User command, 220–222
SetX utility, 13–15
Erase command
GPResult command, 328–330
GPUpdate command, 330
TaskKill and TaskList, 347–350, 348
FindStr utility, 82–83
ForFiles utility, 407–409
FSUtil (File System Utility), 83
FSUtil Behavior command, 83–86
FSUtil Behavior QuotaNotify command, 90
FSUtil Dirty command, 86–87
FSUtil FSInfo command, 87–88
FSUtil Hardlink command, 75
FSUtil Quota command, 89–90
FSUtil Repair command, 84, 86, 90–91
CScript and WScript, 442
ICACLS utility, 127–128, 128
ICACLS /Deny command, 131
ICACLS /FindSID command, 130
ICACLS /Grant command, 130–131
ICACLS /Remove command, 131
ICACLS /SetOwner command, 132
ICACLS /Verify command, 132
Net Group command, 146–147
Net Help command, 156
Net Helpmsg command, 157
Net LocalGroup command, 25, 146–148
Net LocalGroup /Add command, 148
Net LocalGroup /Delete command, 148–149
Net Pause command, 155
Net Session command, 149–150
Net Session /Delete command, 150
Net Share command, 159
Net Share /Delete, 161
Net Share Drive command, 160
Net Start command, 154
Net Start W32Time command, 313–314
Net Statistics Server command, 161
Net Statistics Workstation command, 163
Net Stop command, 154
Net Stop W32Time command, 313–314
Net Time command, 163, 312
Net Use command, 160–161
Net Use /Delete command, 161
Net Use LocalDevice RemoteShare
Net User /Add command, 25, 141–143
Net User /Delete command, 143
Net Accounts command, 143, 143, 145–146
Net Accounts /ForceLogoff command, 144
Net Computer command, 149
Net Computer /Add command, 149
Net Computer /Delete command, 149
Net Continue command, 155
Net File command, 155
Net File /Close command, 156
OpenFiles utility
OpenFiles /Disconnect command, 133
OpenFiles /Local command, 134
OpenFiles /Query command, 132–133
NTDSUtil (NT Directory Services utility),
PopD command
Prompt command
Prompt $P$G command, 60
Reg Add command, 364–365
Reg Compare command, 366–367
Reg Copy command, 366
Reg Delete command, 365
Reg Export command, 367
Reg Query command, 363–364
Reg Restore command, 367–368
Reg Save command, 367
script access, 466–468
PushD command
QUser utility, 333
QWinSta utility, 207
RmDir command, 62
RunAs command, 480
SchTasks utility, 51
SchTasks /Change command, 54
SchTasks /Create command, 51–53
SchTasks /Delete command, 53
SchTasks /End command, 54
SchTasks /Query command, 53
SchTasks /Run command, 54
Script tab, 445
SFC (System File Scan) utility, 339, 340
SFC /ScanFile command, 340
SFC /ScanNow command, 339
SFC /VerifyFile command, 340
SFC /VerifyOnly command, 339
TakeOwn utility, 132, 134–135
TaskKill ﬁlters, 347–350, 348
TaskList utility
WEvtUtil utility, 262
WEvtUtil AL command, 270
WEvtUtil CL command, 270
WEvtUtil EL command, 263
WEvtUtil EP command, 262
WEvtUtil EPL command, 269
WEvtUtil GL command, 267
WEvtUtil GLI command, 267
WEvtUtil GP command, 262–263
WEvtUtil QE command, 264, 266
WEvtUtil SL command, 267, 269
WhoAmI utility, 333
Ver command, 16
WMIC CPU LIST command, 304–307, 305
WMIC NTDomain ASSOC command, 218
WMIC NTDomain GET command,
WMIC NTDomain LIST command, 215
WMIC NTDomain SET command, 217
WMIC RDToggle command, 27
WScript object, 449
XCopy command
```

### L3_Routing_NAT (25 commands)
```bash
IP address of the URL changes before the DNS resolver cache purges
PathPing to perform an IPv6 test by using the -6 command line switch.
IpConfig
IP address conﬁguration test
IP address loopback ping test
NetSH Helper List (Page 473)
NetSH Help (Page 474)
NetSH Commands (Page 476)
NetSH Contexts (Page 476)
NetSH utility into a different context. The use of helper DLLs theoretically
NetSH utility in more detail.
IP address, type NetSH฀Interface฀IP฀Add฀Address฀/? at the command
ping -c 3 utility. A special NetSH฀Diag฀GUI command
NetSH provide commands to display both the list of aliases and the
IPConfig
NetSH command, 474–475, 475
NetSH (Network Command Shell) utility, 26
NetSH Interface command, 473–475
ping -c 3 (Packet Internet Groper) utility,
PathPing utility, 171–172, 171
Route Add command, 181–182
Route Change command, 182–183
Route Delete command, 183
Route Print command, 180–181
TraceRt utility, 172, 172
```

### L4_Port_Service (2 commands)
```bash
RPCPing to check connectivity to the Exchange Server installed
RPCPing utility, 173
```

### L7_HTTP_Web (1 commands)
```bash
Script Host Resources site at http://labmice.techtarget.com/script-
```

