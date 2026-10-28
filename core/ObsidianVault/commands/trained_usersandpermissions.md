---
title: "Trained Command Playbook: UsersAndPermissions.txt"
tags:
  - credential_access
  - enumeration
  - john
  - mdp
  - passive_enum
  - privilege_escalation
  - text
  - trained
source_file: UsersAndPermissions.txt
updated: 2026-10-24 01:01:08
---

# Trained Command Playbook: `UsersAndPermissions.txt`

- **Source Document:** `~/Projects/CORA/Training/UsersAndPermissions.txt`
- **CEGAR Verified Commands:** `39` (`0` malformed/unsafe snippets filtered)
- **MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`):** `39`
- **Discovered IPs/Subnets:** `None`
- **Discovered Interfaces:** `None`
- **Related Knowledge Note:** [[knowledge/trained_usersandpermissions]]

## Distilled MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`)
| Pre-State ($s$) | Tactic ($\tau$) | Technique ($k$) | Tool ($u$) | Post-State ($s'$) | Verified Command ($c$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `chown` | `s_interactive_tty_or_priv_escalated` | `chown -R --from=userA UserB /usr/directory` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `find` | `s_passive_topology_mapped` | `find / -xdev -group <group>` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `cp` | `s_credentials_or_certs_acquired` | `cp -r /etc/skel /home/freddo` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `cp` | `s_active_services_enumerated` | `cp /tmp/helloscript.sh .` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `chown` | `s_interactive_tty_or_priv_escalated` | `chown newOwnerUsername Filename` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `ls` | `s_passive_topology_mapped` | `ls -l /home/johnd/comments.txt` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `cp` | `s_active_services_enumerated` | `cp /tmp/helloscript.sh ~fred` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `chown` | `s_interactive_tty_or_priv_escalated` | `chown newOnwerUsername:newOwnerGroup Filename` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `mkdir` | `s_passive_topology_mapped` | `mkdir /stooge /stooge/larry /stooge/moe /stooge/shemp /stooge/curly /stooge/joe; cd /stooge` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `cp` | `s_active_services_enumerated` | `cp /etc/passwd /stooge` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `chmod` | `s_interactive_tty_or_priv_escalated` | `chmod symbolic-mode-list filename` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `ls` | `s_active_services_enumerated` | `ls /stooge` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `chmod` | `s_interactive_tty_or_priv_escalated` | `chmod u+rw,g=x,go-wx /home/johnd/script.sh` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `chmod` | `s_interactive_tty_or_priv_escalated` | `chmod u+rw,g=,o=u /home/johnd/pod.txt` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `chmod` | `s_interactive_tty_or_priv_escalated` | `chmod a=r /home/johnd/pod.txt` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `chmod` | `s_interactive_tty_or_priv_escalated` | `chmod ugo=r	/home/johnd/pod.txt` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `chmod` | `s_interactive_tty_or_priv_escalated` | `chmod absolute-mode filename` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `chmod` | `s_interactive_tty_or_priv_escalated` | `chmod 653 /home/johnd/comments` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `chmod` | `s_interactive_tty_or_priv_escalated` | `chmod u+x,g-x,o= /home/johnd/comments.txt` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `chmod` | `s_interactive_tty_or_priv_escalated` | `chmod 650 /tmp/comments.txt` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `chmod` | `s_interactive_tty_or_priv_escalated` | `chmod u-x,g=rx,o-r /tmp/comments.txt` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `chmod` | `s_interactive_tty_or_priv_escalated` | `chmod u=rw,g+x,g-w,o-r /tmp/comments.txt` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `chmod` | `s_interactive_tty_or_priv_escalated` | `chmod ugo-rwx,u-x,g-w,o-rwx /tmp/comments.txt` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `chown` | `s_interactive_tty_or_priv_escalated` | `chown -R fred:staff /home/freddo` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `chmod` | `s_interactive_tty_or_priv_escalated` | `chmod 6640 /home/johnd/scripts/*.sh` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `-u` | `s_interactive_tty_or_priv_escalated` | `sudo -u root ./setup.sh` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `chown` | `s_interactive_tty_or_priv_escalated` | `chown fred:staff helloscript.sh` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `chown` | `s_interactive_tty_or_priv_escalated` | `chown fred helloscript.sh` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `chgrp` | `s_interactive_tty_or_priv_escalated` | `chgrp staff helloscript.sh` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `chmod` | `s_interactive_tty_or_priv_escalated` | `chmod 750 helloscript.sh` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `chown` | `s_interactive_tty_or_priv_escalated` | `chown :staff helloprog` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `chgrp` | `s_interactive_tty_or_priv_escalated` | `chgrp staff helloprog` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `chmod` | `s_interactive_tty_or_priv_escalated` | `chmod g-r helloscript.sh` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `chmod` | `s_interactive_tty_or_priv_escalated` | `chmod go-r helloprog` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `chgrp` | `s_interactive_tty_or_priv_escalated` | `chgrp -R stooges /stooge` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `chmod` | `s_interactive_tty_or_priv_escalated` | `chmod 710 /stooge` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `chmod` | `s_interactive_tty_or_priv_escalated` | `chmod 750 curly larry moe joe shemp` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `chmod` | `s_interactive_tty_or_priv_escalated` | `chmod g+rw /stooge` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `chmod` | `s_interactive_tty_or_priv_escalated` | `chmod +t /stooge` |

## Verified Executable Commands (Grouped by Capability Layer)

### General_System (39 commands)
```bash
chown -R --from=userA UserB /usr/directory
find / -xdev -group <group>
chown newOwnerUsername Filename
chown newOnwerUsername:newOwnerGroup Filename
chmod symbolic-mode-list filename
chmod u+rw,g=x,go-wx /home/johnd/script.sh
chmod u+rw,g=,o=u /home/johnd/pod.txt
chmod a=r /home/johnd/pod.txt
chmod ugo=r	/home/johnd/pod.txt
chmod absolute-mode filename
ls -l /home/johnd/comments.txt
chmod 653 /home/johnd/comments
chmod u+x,g-x,o= /home/johnd/comments.txt
chmod 650 /tmp/comments.txt
chmod u-x,g=rx,o-r /tmp/comments.txt
chmod u=rw,g+x,g-w,o-r /tmp/comments.txt
chmod ugo-rwx,u-x,g-w,o-rwx /tmp/comments.txt
cp -r /etc/skel /home/freddo
chown -R fred:staff /home/freddo
chmod 6640 /home/johnd/scripts/*.sh
sudo -u root ./setup.sh
cp /tmp/helloscript.sh .
cp /tmp/helloscript.sh ~fred
chown fred:staff helloscript.sh
chown fred helloscript.sh
chgrp staff helloscript.sh
chmod 750 helloscript.sh
chown :staff helloprog
chgrp staff helloprog
chmod g-r helloscript.sh
chmod go-r helloprog
mkdir /stooge /stooge/larry /stooge/moe /stooge/shemp /stooge/curly /stooge/joe; cd /stooge
cp /etc/passwd /stooge
chgrp -R stooges /stooge
chmod 710 /stooge
chmod 750 curly larry moe joe shemp
ls /stooge
chmod g+rw /stooge
chmod +t /stooge
```

