---
title: "Trained Knowledge & Topology: CQC001_E020_M060_S010_I020_BypassExam_X060_C010_exhibit2.pdf"
tags:
  - mdp
  - pdf
  - trained
source_file: CQC001_E020_M060_S010_I020_BypassExam_X060_C010_exhibit2.pdf
doc_type: pdf
updated: 2026-10-24 00:57:34
---

# Trained Knowledge & Architecture: `CQC001_E020_M060_S010_I020_BypassExam_X060_C010_exhibit2.pdf`

- **Source Path:** `~/Projects/CORA/Training/CQC001_E020_M060_S010_I020_BypassExam_X060_C010_exhibit2.pdf` (`pdf`)
- **Extracted Technical Entities:** `general`
- **Extracted IPs / Subnets:** `0.0.0.0, 104.64.57.171, 127.0.0.1, 172.16.1.168, 172.24.1.120, 172.24.1.243, 172.24.2.112, 172.24.5.1, 172.24.56.1, 31.13.73.1, 54.88.232.60`
- **Extracted Interfaces:** `None`

## LLM Distilled Operational Summary
### Key Operational Techniques & Decision Workflows

*   **Process Identification via PID Mapping**: Correlate high-risk ports (e.g., 135, 445) with specific PIDs to identify the owning service.
    *   `PID 4` owns critical SMB/NetBIOS services (Ports 135, 445, 139, 137, 138).
    *   `PID 1096` handles multiple active HTTPS connections (Port 443).
    *   `PID 1616` manages dynamic high ports (47163, 49152+) and IPv6 equivalents.
*   **Connection State Analysis**: Differentiate between active data transfer (`ESTABLISHED`) and potential zombie processes or connection leaks (`CLOSE_WAIT`, `SYN_SENT`).
    *   Multiple `CLOSE_WAIT` states on Port 443 (e.g., to `104.64.57.171`) indicate a specific application failing to close sockets properly.
*   **Network Segmentation Verification**: Confirm traffic flow between distinct subnets.
    *   Internal-to-Internal: `172.24.1.120` ↔ `172.24.1.243` (SMB).
    *   Internal-to-External: `172.24.1.120` ↔ `31.13.73.1` (HTTPS).

### Critical Command Patterns and Required Flags

*   **Port Scanning & Service Enumeration**:
    *   `netstat -ano` (Windows): Displays active connections with Process IDs (PID) for immediate process lookup via Task Manager.
    *   `netstat -aon | findstr "ESTABLISHED"`: Isolates active sessions for analysis.
*   **Process Investigation**:
    *   `tasklist | findstr <PID>`: Identifies the executable name associated with a specific PID (e.g., PID 4 is typically `svchost.exe` hosting `LSASS` or `SPSVC`).
*   **IPv6/Loopback Verification**:
    *   Check `[::]` and `[::1]` bindings to ensure services are listening on all interfaces or restricted to localhost.

### Network Topology, IP/Subnet, and Service Relationships

*   **Primary Host**: `172.24.1.120` (Likely a Domain Controller or File Server given the SMB stack).
*   **Key Subnets**:
    *   `172.24.1.x`: Primary internal network segment.
    *   `172.24.5.x`: Secondary internal segment (Port 139 listening).
    *   `172.24.56.x`: Tertiary internal segment (UDP 137/138/1900).
*   **External Services**:
    *   `31.13.73.1:443` & `104.64.57.171:443`: Active HTTPS clients (Potential web

