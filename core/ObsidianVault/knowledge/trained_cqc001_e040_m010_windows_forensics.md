---
title: "Trained Knowledge & Topology: CQC001_E040_M010_Windows_Forensics.pdf"
tags:
  - http
  - https
  - mdp
  - netstat
  - passive_enum
  - pdf
  - pslist
  - sysinternals
  - trained
  - wmic
source_file: CQC001_E040_M010_Windows_Forensics.pdf
doc_type: pdf
updated: 2026-10-25 00:57:54
---

# Trained Knowledge & Architecture: `CQC001_E040_M010_Windows_Forensics.pdf`

- **Source Path:** `~/Projects/CORA/Training/CQC001_E040_M010_Windows_Forensics.pdf` (`pdf`)
- **Extracted Technical Entities:** `http, https, netstat, pslist, sysinternals, wmic`
- **Extracted IPs / Subnets:** `None`
- **Extracted Interfaces:** `None`
- **Linked Command Playbook:** [[commands/trained_cqc001_e040_m010_windows_forensics]] (`10` CEGAR-verified commands | `10` MDP transitions)

## Command & Tactic Coverage Summary
- **Total CEGAR-Verified Commands:** `10` (full executable list in [[commands/trained_cqc001_e040_m010_windows_forensics]])
- **Tactic Distribution:** `Passive_Enum` (10)
- **Top Extracted CLI Tools:** `sc` (4), `net` (2), `date` (1), `dir` (1), `psloglist` (1), `systeminfo` (1)

## LLM Distilled Operational Summary
### Windows Forensics Survey Methodology Playbook

#### 1. Key Operational Techniques & Decision Workflows
*   **System Characterization**: Establish baseline system state using `date /t` (preserve time), `ver`, `net session` (active users), `psloglist` (recent logons), `net statistics` (uptime), `systeminfo` (CPU/RAM), and `lm` (kernel modules).
*   **Process Anomaly Detection**: Investigate processes starting from unexpected locations (e.g., `%WINDIR%\temp`), appearing too early in the boot cycle alongside core services (`svchost.exe`, `smss.exe`, `winlogon.exe`), or possessing unusual arguments.
*   **Process Lineage Analysis**: Use `wmic process list` to inspect Parent Process IDs (PPIDs) and verify if high-privilege processes (e.g., `lsass.exe`) descend from legitimate services.
*   **User Context Verification**: Confirm that processes like `explorer.exe` or `cmd.exe` are running under expected users; flag instances where they run as `SYSTEM`.
*   **Name Obfuscation Checks**: Scrutinize executable names for intentional misspellings mimicking legitimate binaries (e.g., `WINW0RD.EXE`, `iexplorer.exe`, `svchst.exe`, `csrss .exe`).
*   **Network State Assessment**: Execute `netstat -anob` to capture all active TCP/UDP connections, numerical addresses, PIDs, and associated executable names in a single operation.
*   **Timestamp Forensics**: Analyze NTFS MAC times (Modified, Accessed, Created) noting that NTFS stores values in UTC, whereas FAT uses local time. Be aware of resolution differences: FAT creation time is 10ms, write time is 2s, and access time is 1 day.

#### 2. Critical Command Patterns & Flags
*   **`netstat -anob`**: The primary command for network surveying.
    *   `-a`: Show all connections and listening ports.
    *   `-n`: Display numerical addresses (IP/Port) instead of resolving names.
    *   `-o`: Include Process ID (PID) for each connection.
    *   `-b`: Display the full executable name involved in the connection.
*   **`psloglist "Security" -i 528 -s | find /i "Logon Type: 10"`**: Filters security logs to identify recent interactive logons (Logon Type 10).
*   **`date /t`**: Displays current time without modifying the system clock.
*   **`wmic process list`**: Retrieves detailed process lists including PPIDs for lineage tracing.

#### 3. Network Topology & Common Locations
*   **Executable Locations (Legitimate)**:
    *   `C:\Windows\System32`
    *   `C:\Program Files`
    *   `C:\Windows`
*   **Executable Locations (Suspicious/Anomalous)**:
    *   `C:\Windows\Temp`
    *   `C:\Windows\User`
*   **Network Protocol Focus**: While UDP is less frequently targeted, it should be reviewed via `netstat -p UDP` if

