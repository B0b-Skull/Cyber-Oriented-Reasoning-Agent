---
title: "Trained Knowledge & Topology: Hot Potato – Windows Privilege Escalation.pdf"
tags:
  - http
  - https
  - mdp
  - netsh
  - pdf
  - trained
source_file: Hot Potato – Windows Privilege Escalation.pdf
doc_type: pdf
updated: 2026-10-23 22:55:46
---

# Trained Knowledge & Architecture: `Hot Potato – Windows Privilege Escalation.pdf`

- **Source Path:** `~/Projects/CORA/Training/Hot Potato – Windows Privilege Escalation.pdf` (`pdf`)
- **Extracted Technical Entities:** `http, https, netsh`
- **Extracted IPs / Subnets:** `10.0.0.0/24, 10.0.1.0, 127.0.0.1`
- **Extracted Interfaces:** `None`

### Visual & Network Diagram Intelligence (`Hot Potato – Windows Privilege Escalation.pdf#page8`)
- **Spatially Grouped Diagram Nodes (Box/Component Clusters):**
  1. `[page：]`
  2. `[https: / /github.com/foxglovesec/Potato]`

## LLM Distilled Operational Summary
### 1. Key Operational Techniques & Decision Workflows

*   **Objective:** Elevate local privileges from low-level user to `NT AUTHORITY\SYSTEM` on Windows 7/8/10/Server 2008/2012.
*   **Core Mechanism:** Combine three legacy attacks into a single chain: Local NBNS Spoofing, Fake WPAD Proxy, and HTTP->SMB NTLM Relay.
*   **Workflow Step 1: Force NBNS Fallback via UDP Exhaustion**
    *   Since local admin access is often required to sniff traffic for standard spoofing, use **UDP Port Exhaustion** to force DNS failures.
    *   Bind to all UDP ports to deplete the source port pool, causing DNS lookups to fail.
    *   Trigger fallback to NBNS (NetBIOS Name Service) for hostname resolution.
*   **Workflow Step 2: Local NBNS Spoofing**
    *   Target `127.0.0.1` (localhost) with a fake response for the hostname `WPAD`.
    *   Iterate through all 65,536 TXID values to match the request/response pair, as the original request is invisible.
    *   Flood the target rapidly; this affects all users on the machine, including high-privilege accounts.
*   **Workflow Step 3: Fake WPAD Proxy Injection**
    *   Run a local HTTP server on `127.0.0.1`.
    *   Respond to `http://wpad/wpad.dat` requests with a JavaScript proxy script redirecting traffic through the local server.
*   **Workflow Step 4: HTTP->SMB NTLM Relay**
    *   Intercept HTTP traffic via the WPAD proxy.
    *   Relay the NTLM authentication hash from the HTTP request to an SMB share, escalating privileges if the SMB service accepts the relayed credentials.

### 2. Critical Command Patterns & Required Flags

*   **UDP Port Exhaustion:** Bind to all UDP ports to force DNS failure.
    *   *Concept:* `netsh interface ipv4 set dynamicport udp=0-65535` (or equivalent binding logic).
*   **NBNS Spoofing (Local):** Flood `127.0.0.1` with NBNS responses for `WPAD`.
    *   *Concept:* `python -m hotpotato --nbns-spoof localhost --target localhost --txid-iter 65536`
*   **WPAD Proxy Injection:** Serve a specific proxy script.
    *   *Script Content:*
        ```javascript
        FindProxyForURL(url,host){
          if (dnsDomainIs(host, "localhost")) return "DIRECT";
          return "PROXY 127.0.0.1:80";
        }
        ```
*   **HTTP->SMB Relay:** Capture NTLM hashes and relay to SMB.
    *   *Concept:* `python -m hotpotato --http-relay localhost --smb-target <SMB_IP>`

### 3. Network Topology & Service Relationships

*   **Target Host:** Any Windows 7/8/10/Server

## Document Structure & Key Topics
- Visual & Network Diagram Intelligence (`Hot Potato – Windows Privilege Escalation.pdf#page8`)

## Extracted Operational Steps & Workflows
- 1. Local NBNS Spoofer
- 2. Fake WPAD Proxy Server
- 3. HTTP -> SMB NTLM Relay

