---
title: "curl, OpenSSL & PowerShell HTTP/API/mTLS Reconnaissance Playbook"
category: commands
domain_hub: "[[knowledge/08_web_api_sql_injection_and_active_reconnaissance]]"
os_platform: cross-platform
primary_tactic: Active_Enum
summary: "Cross-platform Linux curl, openssl s_client, and Windows PowerShell Invoke-WebRequest/Invoke-RestMethod playbook for HTTP/HTTPS/REST/GraphQL probing, mTLS client certificates, reverse-proxy bypass headers, and appliance firmware fingerprinting."
when_to_apply: "Apply whenever probing web servers, REST/GraphQL APIs, network appliances (FortiGate, routers, switches), inspecting TLS certificates/firmware timestamps, or testing authentication, mTLS, cookies, JWTs, and X-Forwarded-For bypasses on Linux or Windows."
tags: [curl, http, https, api, scanning, openssl, tls, mtls, bearer, jwt, cookie, csrf, x-forwarded-for, reverse_proxy, powershell, invoke-webrequest, active_enum, cross-platform]
updated: 2026-10-30
---

# `curl`, `openssl` & PowerShell HTTP / API / mTLS Playbook

> **Summary:** Non-hanging Linux `curl` / `openssl` and Windows `curl.exe` / `Invoke-WebRequest` patterns for web, API, mTLS, and appliance firmware fingerprinting.  
> **Backlinks:** [[00_MEMORY_INDEX]] | [[commands/linux_master_command_playbook]] | [[commands/windows_master_command_playbook]] | [[knowledge/08_web_api_sql_injection_and_active_reconnaissance]]

---

## When to Apply (LLM & 15-Engine Decision Matrix)

| Symptom / Operational Goal | Bayesian Root Cause (`Engine 4`) | H-MDP State Transition | Recommended `curl` / `openssl` Action |
| :--- | :--- | :--- | :--- |
| **Identify Appliance Model & Firmware Build Window** | `service_on_nonstandard_port_or_tls` | `s_l2_l3_verified -> s_active_services_enumerated` | `curl -sS -k -L -i --max-time 15` + `openssl s_client` to extract `Server`, `Last-Modified`, `ETag`, and TLS `Subject CN` serial number |
| **`HTTP 401 Unauthorized` / `403 Forbidden`** | `missing_auth_or_mtls_cert` | `s_active_services_enumerated -> s_credentials_or_certs_acquired` | Add `-H "Authorization: Bearer <TOKEN>"`, `-b cookies.txt`, or `--cert client.crt --key client.key` |
| **`HTTP 403` Behind Reverse Proxy (`Nginx`/`Envoy`)** | `reverse_proxy_ip_acl_block` | `s_active_services_enumerated -> s_initial_shell_or_api_access` | Add `-H "X-Forwarded-For: 127.0.0.1" -H "X-Real-IP: 127.0.0.1" -H "X-Forwarded-Host: localhost"` |
| **`curl: (60) SSL certificate problem`** | `self_signed_or_expired_tls_cert` | `s_l2_l3_verified -> s_active_services_enumerated` | Always include `-k` (`--insecure`) when probing internal lab or appliance endpoints |
| **`curl: (7) Failed to connect` / `(28) Timed out`** | `service_bound_to_loopback` or `host_firewall_drop` | `s_l2_l3_verified -> s_oob_serial_enumerated` | Pivot to `nmap` port scan, L2/L3 routing check (`ip route get`), or OOB serial (`[[commands/tio_serial_playbook]]`) |

---

## 1. Mandatory `curl` Safety Flags for Non-Interactive Agent Execution
- Always include **`-sS`** (suppress progress meter while preserving error messages), **`-k`** (accept self-signed/appliance TLS certificates), and **`-L`** (follow `301`/`302`/`307` redirects).
- Always include **`--connect-timeout 5 --max-time 15`** so blackholed or tarpitted endpoints never hang execution.
- On Windows PowerShell where `curl` may alias `Invoke-WebRequest`, explicitly invoke **`curl.exe`** for native libcurl flags.

---

## 2. Linux & Windows `curl` / `openssl` Command Reference

| Purpose | Linux (`bash`) Command | Windows (`CMD` / `PowerShell`) Command | Key Output to Inspect |
| :--- | :--- | :--- | :--- |
| **1. Full Headers + Body (`GET`)** | `curl -sS -k -L -i --connect-timeout 5 --max-time 15 "https://<TARGET_IP>/"` | `curl.exe -sS -k -L -i --connect-timeout 5 --max-time 15 "https://<TARGET_IP>/"` | `HTTP/` status code, `Server:`, `Last-Modified:`, `Set-Cookie:`, HTML `<title>` |
| **2. Headers Only (`HEAD` + `GET` fallback)** | `curl -sS -k -L -I --max-time 15 "https://<TARGET_IP>/"` | `curl.exe -sS -k -L -I --max-time 15 "https://<TARGET_IP>/"` | `ETag`, `Last-Modified` (reveals exact firmware compile date on FortiGate/embedded appliances!), `Strict-Transport-Security` |
| **3. TLS Certificate Subject, Serial & SAN Extraction** | `echo \| openssl s_client -connect <TARGET_IP>:443 -servername <TARGET_IP> 2>/dev/null \| openssl x509 -noout -subject -issuer -dates -serial -ext subjectAltName` | `echo "" \| openssl.exe s_client -connect <TARGET_IP>:443 2>NUL \| openssl.exe x509 -noout -subject -issuer -dates -serial` | Hardware model & serial in `subject=CN = FG...`, issuer CA, validity dates, internal DNS names in `subjectAltName` |
| **4. JSON REST API (`GET` with Bearer Token)** | `curl -sS -k -L --max-time 15 -H "Accept: application/json" -H "Authorization: Bearer <TOKEN>" "https://<TARGET_IP>/api/v1/status"` | `curl.exe -sS -k -L --max-time 15 -H "Accept: application/json" -H "Authorization: Bearer <TOKEN>" "https://<TARGET_IP>/api/v1/status"` | JSON schema keys, version strings, role/permission fields |
| **5. JSON REST API (`POST` Login / Action)** | `curl -sS -k -L -i --max-time 15 -X POST -H "Content-Type: application/json" -d '{"username":"admin","password":"<PASS>"}' "https://<TARGET_IP>/api/v1/login"` | `curl.exe -sS -k -L -i --max-time 15 -X POST -H "Content-Type: application/json" -d "{\"username\":\"admin\",\"password\":\"<PASS>\"}" "https://<TARGET_IP>/api/v1/login"` | `Set-Cookie` session token, JWT `access_token`, or error message |
| **6. Cookie Jar Capture & Authenticated Replay** | `curl -sS -k -L -c /tmp/cookies.txt -b /tmp/cookies.txt --max-time 15 -X POST -d "username=admin&password=<PASS>" "https://<TARGET_IP>/login"` | `curl.exe -sS -k -L -c C:\Temp\cookies.txt -b C:\Temp\cookies.txt --max-time 15 -X POST -d "username=admin&password=<PASS>" "https://<TARGET_IP>/login"` | Persists session & CSRF cookies across multi-step login workflows |
| **7. Mutual TLS (`mTLS`) Client Certificate Auth** | `curl -sS -k -L --max-time 15 --cert client.crt --key client.key --cacert ca.crt "https://<TARGET_IP>:8443/api/admin"` | `curl.exe -sS -k -L --max-time 15 --cert client.crt --key client.key "https://<TARGET_IP>:8443/api/admin"` | Resolves `SSLV3_ALERT_BAD_CERTIFICATE` / `400 No required SSL certificate was sent` (`CBR-004`) |
| **8. Reverse Proxy Localhost Spoofing Headers** | `curl -sS -k -L -i --max-time 15 -H "X-Forwarded-For: 127.0.0.1" -H "X-Real-IP: 127.0.0.1" -H "X-Original-URL: /admin" "https://<TARGET_IP>/"` | `curl.exe -sS -k -L -i --max-time 15 -H "X-Forwarded-For: 127.0.0.1" -H "X-Real-IP: 127.0.0.1" "https://<TARGET_IP>/"` | Tests whether upstream reverse proxy trusts client-supplied `X-Forwarded-For` headers |

---

## 3. Native Windows PowerShell Web & API Probing (`Invoke-WebRequest` / `Invoke-RestMethod`)
When `curl.exe` is unavailable on an older Windows host, use PowerShell with TLS 1.2/1.3 and self-signed certificate bypass enabled:
```powershell
powershell -NoProfile -Command "[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; $ resp = Invoke-WebRequest -Uri 'https://<TARGET_IP>/' -UseBasicParsing -TimeoutSec 15; $resp.StatusCode; $resp.Headers"
```
