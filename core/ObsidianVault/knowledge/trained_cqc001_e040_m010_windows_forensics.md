---
title: "Trained Knowledge & Topology: CQC001 E040 M010 Windows Forensics"
category: knowledge
domain_hub: "[[knowledge/02_windows_registry_boot_and_persistence]]"
os_platform: windows
primary_tactic: Passive_Enum
summary: "Operational architecture, decision workflows & Windows/Linux command reference for CQC001 E040 M010 Windows Forensics: Windows Registry root keys (HKLM, HKCU, HKU, HKCR, HKCC), data types (REG_SZ, REG_DWORD, REG_BINARY), Run/RunOnce/Winlogon/Session"
when_to_apply: "Apply when working with CQC001 E040 M010 Windows Forensics (windows): Apply when auditing Windows persistence mechanisms, inspecting Registry hives (`HKLM`/`HKCU`/`HKU`), analyzing boot sequences (`SMSS` -> `CSRSS` -> `Wininit` -> `Services` -> `LSASS` -> `Winlogon`), or checking `bcdedit` DEP/signing settings."
tags: [http, https, mdp, netstat, passive_enum, pdf, pslist, sysinternals, trained, wmic, windows, registry, reg, bcdedit, autorunsc, schtasks, persistence, winlogon, boot, forensics, linux]
source_file: "CQC001 E040 M010 Windows Forensics"
updated: 2026-10-30
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

<!-- CORA-MAXIMIZED-COMMANDS-START -->
## Maximized Windows & Linux Command Examples for `CQC001 E040 M010 Windows Forensics`

> **Domain Hub:** [[knowledge/02_windows_registry_boot_and_persistence|Domain Hub 02: Windows Registry Architecture, Boot Configuration (bcdedit), Startup & Persistence]]  
> **Master Playbooks:** [[commands/windows_master_command_playbook]] | [[commands/linux_master_command_playbook]] | [[commands/curl_playbook]] | [[commands/tio_serial_playbook]]  
> **When to Apply:** Apply when auditing Windows persistence mechanisms, inspecting Registry hives (`HKLM`/`HKCU`/`HKU`), analyzing boot sequences (`SMSS` -> `CSRSS` -> `Wininit` -> `Services` -> `LSASS` -> `Winlogon`), or checking `bcdedit` DEP/signing settings.  
> **15-Engine H-MDP State Transition:** `s_passive_topology_mapped` $\xrightarrow{\text{Passive_Enum}}$ `s_active_services_enumerated` | **Bayesian Root-Cause Triggers:** `registry_autorun_persistence, winlogon_shell_hijack, boot_bcd_tampering, scheduled_task_persistence` | **Isolation:** `RED, BLUE, WHITE (100% local host telemetry compatible)`

| Primary Command (`Windows` / `Linux`) | OS / Shell | What It Does & Key Flags | When to Apply & Expected Output | Cross-Platform Equivalent |
| :--- | :--- | :--- | :--- | :--- |
| `reg query "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Run" && reg query "HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Run"` | **Windows CMD** | Queries machine-wide (`HKLM`) and current-user (`HKCU`) Registry `Run` keys executed automatically at logon. | Apply during every Windows persistence sweep (also check `RunOnce` and `Wow6432Node\...\Run`). | `ls -la /etc/xdg/autostart ~/.config/autostart /etc/rc.local` |
| `reg query "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon" /v Userinit && reg query "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon" /v Shell` | **Windows CMD** | Inspects `Userinit` (default `userinit.exe,`) and `Shell` (default `explorer.exe`) under `Winlogon`. | Apply to detect Winlogon helper DLL/binary hijacking that executes at interactive logon. | `cat /etc/profile /etc/bash.bashrc ~/.bashrc` |
| `reg query "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager" /v BootExecute` | **Windows CMD** | Reads native NT boot-time executable list (`BootExecute`, default `autocheck autochk *`) and `KnownDLLs`. | Apply to detect early-boot persistence executed by `smss.exe` before Win32 starts. | `systemctl list-dependencies sysinit.target` |
| `reg query "HKLM\SYSTEM\CurrentControlSet\Control\hivelist"` | **Windows CMD** | Maps loaded Registry hive paths (`\REGISTRY\MACHINE\SAM`, `SYSTEM`, `SOFTWARE`, `SECURITY`) to physical disk files. | Apply to verify loaded registry hives and locate user `NTUSER.DAT` paths. | `findmnt && mount` |
| `reg query "HKU" \| findstr /i "S-1-5-21-" \| findstr /v "_Classes"` | **Windows CMD** | Lists the Security Identifiers (`SIDs`) of all domain/local user profiles currently loaded in `HKEY_USERS`. | Apply to identify which users have active loaded registry hives and query `HKU\<SID>\Software\Microsoft\Windows\CurrentVersion\Run`. | `loginctl list-users && w` |
| `reg query "HKLM\SYSTEM\CurrentControlSet\Enum\USBSTOR" /s` | **Windows CMD** | Recursively dumps historical USB storage device vendor, model, revision, and serial numbers from the Registry. | Apply during forensic investigations to identify every USB drive ever plugged into the host. | `lsusb -v && journalctl -k \| grep -i usb` |
| `autorunsc -accepteula -a * -c -h -s -v` | **Sysinternals** | Comprehensive CSV dump of all Windows auto-start extension points (`Run`, Services, Drivers, Scheduled Tasks, WMI, Print Monitors) with SHA256 hashes and Authenticode status. | Apply as the definitive persistence audit across all Registry and filesystem startup locations. | `systemctl list-unit-files --state=enabled && crontab -l` |
| `bcdedit /enum all` | **Windows CMD (Admin)** | Displays Windows Boot Manager and OS Loader entries (`nx` DEP policy, `testsigning`, `nointegritychecks`, `debug`, `safeboot`). | Apply to verify Data Execution Prevention (`nx AlwaysOn`/`OptOut`) and check if driver signature enforcement was disabled (`testsigning Yes`). | `cat /proc/cmdline && mokutil --sb-state` |
| `bcdedit /set {current} nx AlwaysOn` | **Windows CMD (Admin)** | Enforces hardware-assisted Data Execution Prevention (`DEP`) across all 32-bit and 64-bit processes on the current boot entry. | Apply when hardening a Windows host against stack/heap shellcode execution (`s_oob_serial_enumerated -> s_firewall_or_acl_unlocked`). | `sudo sysctl -w kernel.randomize_va_space=2` |
| `reg save HKLM\SAM C:\Temp\sam.hiv && reg save HKLM\SYSTEM C:\Temp\system.hiv` | **Windows CMD (Admin)** | Exports live locked Registry hives (`SAM`, `SYSTEM`, `SECURITY`) to disk files for offline forensic inspection. | Apply during authorized forensic collection or credential auditing when raw `C:\Windows\System32\config\SAM` is locked by the kernel. | `sudo cp /etc/shadow /tmp/shadow.bak` |

### Copy-Pasteable Execution Block (Windows & Linux)
```bash
# [Windows CMD] Queries machine-wide (`HKLM`) and current-user (`HKCU`) Registry `Run` keys executed automatically at logon.
reg query "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Run" && reg query "HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Run"
# [Windows CMD] Inspects `Userinit` (default `userinit.exe,`) and `Shell` (default `explorer.exe`) under `Winlogon`.
reg query "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon" /v Userinit && reg query "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon" /v Shell
# [Windows CMD] Reads native NT boot-time executable list (`BootExecute`, default `autocheck autochk *`) and `KnownDLLs`.
reg query "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager" /v BootExecute
# [Windows CMD] Maps loaded Registry hive paths (`\REGISTRY\MACHINE\SAM`, `SYSTEM`, `SOFTWARE`, `SECURITY`) to physical disk files.
reg query "HKLM\SYSTEM\CurrentControlSet\Control\hivelist"
# [Windows CMD] Lists the Security Identifiers (`SIDs`) of all domain/local user profiles currently loaded in `HKEY_USERS`.
reg query "HKU" | findstr /i "S-1-5-21-" | findstr /v "_Classes"
# [Windows CMD] Recursively dumps historical USB storage device vendor, model, revision, and serial numbers from the Registry.
reg query "HKLM\SYSTEM\CurrentControlSet\Enum\USBSTOR" /s
```
<!-- CORA-MAXIMIZED-COMMANDS-END -->
