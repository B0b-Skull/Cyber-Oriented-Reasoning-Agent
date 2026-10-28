---
title: "Trained Knowledge & Topology: Penetration Testing Tools Cheat Sheet.html"
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
doc_type: html
updated: 2026-10-24 01:00:01
---

# Trained Knowledge & Architecture: `Penetration Testing Tools Cheat Sheet.html`

- **Source Path:** `~/Projects/CORA/Training/Penetration Testing Tools Cheat Sheet.html` (`html`)
- **Extracted Technical Entities:** `arp, cve-2014-6271, eth0, hashcat, http, https, impacket, john, mimikatz, netstat, nmap, powershell, responder, sqlmap, ssh, ssl, tcpdump, tls, vlan`
- **Extracted IPs / Subnets:** `0.0.0.0, 10.0.0.0, 10.255.255.255, 127.0.0.0, 127.0.0.1, 127.255.255.255, 128.0.0.0, 172.16.0.0, 172.31.255.255, 191.255.255.255, 192.0.0.0, 172.24.0.0, 172.24.0.1, 172.24.1.0/24, 172.24.1.1, 172.24.1.100, 172.24.1.108, 172.24.1.156, 172.24.1.200, 172.24.11.200, 172.24.2.1, 172.24.255.255, 172.24.99.131, 223.255.255.255, 224.0.0.0, 239.255.255.255, 240.0.0.0, 255.0.0.0, 255.128.0.0, 255.192.0.0, 255.224.0.0, 255.240.0.0, 255.248.0.0, 255.252.0.0, 255.254.0.0, 255.255.0.0, 255.255.128.0, 255.255.192.0, 255.255.224.0, 255.255.240.0, 255.255.248.0, 255.255.252.0, 255.255.254.0, 255.255.255.0, 255.255.255.128, 255.255.255.192, 255.255.255.224, 255.255.255.240, 255.255.255.249, 255.255.255.252, 255.255.255.254, 255.255.255.255, 77.1.2.25`
- **Extracted Interfaces:** `eth0`
- **Linked Command Playbook:** [[commands/trained_penetration_testing_tools_cheat_sheet]] (`148` CEGAR-verified commands | `148` MDP transitions)

## Command & Tactic Coverage Summary
- **Total CEGAR-Verified Commands:** `148` (full executable list in [[commands/trained_penetration_testing_tools_cheat_sheet]])
- **Tactic Distribution:** `Credential_Access` (43), `Active_Enum` (31), `Passive_Enum` (17), `Reconnaissance` (12), `Covert_Exfil` (11), `Enumeration` (11), `Privilege_Escalation` (8), `Lateral_Movement_Routing_Pivot` (6), `Initial_Access_Exploitation` (5), `Protocol_Chaining` (4)
- **Top Extracted CLI Tools:** `nmap` (16), `apt-get` (10), `sqlmap` (10), `gcc` (7), `git` (7), `python` (7), `searchsploit` (5), `dig` (4), `echo` (4), `hydra` (4), `john` (4), `snmpwalk` (4), `udp-protocol-scanner.pl` (4), `enum4linux` (3), `mount` (3), `nbtscan` (3), `nc` (3), `net` (3), `show` (3), `smbclient` (3), `wget` (3), `dir` (2), `grep` (2), `ikeforce.py` (2), `plink` (2)

## Document Structure & Key Topics
- show startup-config
- show version
- show session
- show interface e0
- show access-lists
- dir file systems
- terminal length 0
- copy running-config tftp
- copy running-config startup-config
- dnsrecon -d TARGET -D /usr/share/wordlists/dnsmap.txt -t std --xml ouput.xml
- x24

## Extracted Operational Steps & Workflows
- Step 1: Idenitfy IKE Servers
- Step 2: Enumerate group name with IKEForce
- Step 3: Use ike-scan to capture the PSK hash
- Step 4: Use psk-crack to crack the PSK hash
- Step 1: Idenitfy IKE Servers
- Step 2: Enumerate group name with IKEForce
- Step 3: Use ike-scan to capture the PSK hash
- Step 4: Use psk-crack to crack the PSK hash

## Extracted Reference Excerpt
```bash
ifconfig eth0 xxx.xxx.xxx.xxx/24
```

```bash
ifconfig eth0 xxx.xxx.xxx.xxx/24
```

```bash
ipcalc xxx.xxx.xxx.xxx/24 
ipcalc xxx.xxx.xxx.xxx 255.255.255.0
```

```bash
ipcalc xxx.xxx.xxx.xxx/24 
ipcalc xxx.xxx.xxx.xxx 255.255.255.0
```

```bash
whois domain-name-here.com
```

```bash
whois domain-name-here.com
```

```bash
dig a domain-name-here.com @nameserver
```

```bash
dig a domain-name-here.com @nameserver
```

```bash
dig mx domain-name-here.com @nameserver
```

```bash
dig mx domain-name-here.com @nameserver
```

```bash
dig axfr domain-name-here.com @nameserver
```

```bash
dig axfr domain-name-here.com @nameserver
```

```bash
nslookup -> set type=any -> ls -d blah.com
```

```bash
dig axfr blah.com @ns1.blah.com
```

```bash
git clone https://github.com/killswitch-GUI/SimplyEmail.git
./SimplyEmail.py -all -e TARGET-DOMAIN
```

```bash
git clone https://github.com/killswitch-GUI/SimplyEmail.git
./SimplyEmail.py -all -e TARGET-DOMAIN
```

```bash
nc -v 172.24.1.1 25
```

```bash
telnet 172.24.1.1 25
```

```bash
nc TARGET-IP 80
GET / HTTP/1.1
Host: TARGET-IP
User-Agent: Mozilla/5.0
Referrer: meh-domain
<enter>
```

```bash
nc TARGET-IP 80
GET / HTTP/1.1
Host: TARGET-IP
User-Agent: Mozilla/5.0
Referrer: meh-domain
<enter>
```

```bash
nmap -v -sS -A -T4 target
```

```bash
nmap -v -sS -p--A -T4 target
```

```bash
nmap -v -sU -sS -p- -A -T4 target
```

```bash
nmap -v -p 445 --script=smb-check-vulns --script-args=unsafe=1 172.24.1.X
```

```bash
ls /usr/share/nmap/scripts/* | grep ftp
```

```bash
nmap -sU TARGET
```

```bash
nmap -sU TARGET
```

```bash
git clone https://github.com/portcullislabs/udp-proto-scanner.git
```

```bash
git clone https://github.com/portcullislabs/udp-proto-scanner.git
```

```bash
./udp-protocol-scanner.pl -f ip.txt
```

```bash
./udp-protocol-scanner.pl -f ip.txt
```

```bash
udp-proto-scanner.pl -p ntp -f ips.txt
```

```bash
udp-proto-scanner.pl -p ntp -f ips.txt
```

```bash
netdiscover -r 172.24.1.0/24
```

```bash
nmblookup -A target
smbclient //MOUNT/share -I target -N
rpcclient -U "" target
enum4linux target
```

```bash
nmblookup -A target
smbclient //MOUNT/share -I target -N
rpcclient -U "" target
enum4linux target
```

```bash
nbtscan 172.24.1.0/24
```

```bash
enum4linux -a target-ip
```

```bash
smbclient -L //172.24.1.100
```

```bash
smbclient -L //172.24.1.100
```

```bash
nmap -T4 -v -oA shares --script smb-enum-shares --script-args smbuser=username,smbpass=password -p445 172.24.1.0/24
```

```bash
nmap -T4 -v -oA shares --script smb-enum-shares --script-args smbuser=username,smbpass=password -p445 172.24.1.0/24
```

```bash
nmap -sU -sS --script=smb-enum-users -p U:137,T:139 172.24.11.200-254
```

```bash
nmap -sU -sS --script=smb-enum-users -p U:137,T:139 172.24.11.200-254
``

