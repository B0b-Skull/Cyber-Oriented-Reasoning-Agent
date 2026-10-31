---
title: "Trained Knowledge & Topology: CQC001 E020 M010 Root Keys and Registry Types"
category: knowledge
domain_hub: "[[knowledge/02_windows_registry_boot_and_persistence]]"
os_platform: windows
primary_tactic: Passive_Enum
summary: "Operational architecture, decision workflows & Windows/Linux command reference for CQC001 E020 M010 Root Keys and Registry Types: Windows Registry root keys (HKLM, HKCU, HKU, HKCR, HKCC), data types (REG_SZ, REG_DWORD, REG_BINARY), Run/RunOnce/Winlogon/Session"
when_to_apply: "Apply when working with CQC001 E020 M010 Root Keys and Registry Types (windows): Apply when auditing Windows persistence mechanisms, inspecting Registry hives (`HKLM`/`HKCU`/`HKU`), analyzing boot sequences (`SMSS` -> `CSRSS` -> `Wininit` -> `Services` -> `LSASS` -> `Winlogon`), or checking `bcdedit` DEP/signing settings."
tags: [bcdedit, enumeration, http, https, mdp, passive_enum, pdf, trained, windows, registry, reg, autorunsc, schtasks, persistence, winlogon, boot, forensics, linux]
source_file: "CQC001 E020 M010 Root Keys and Registry Types"
updated: 2026-10-30
---

# Trained Knowledge & Architecture: `CQC001_E020_M010_Root_Keys_and_Registry_Types.pdf`

- **Source Path:** `~/Projects/CORA/Training/CQC001_E020_M010_Root_Keys_and_Registry_Types.pdf` (`pdf`)
- **Extracted Technical Entities:** `bcdedit, http, https`
- **Extracted IPs / Subnets:** `None`
- **Extracted Interfaces:** `None`
- **Linked Command Playbook:** [[commands/trained_cqc001_e020_m010_root_keys_and_registry_types]] (`17` CEGAR-verified commands | `17` MDP transitions)

## Command & Tactic Coverage Summary
- **Total CEGAR-Verified Commands:** `17` (full executable list in [[commands/trained_cqc001_e020_m010_root_keys_and_registry_types]])
- **Tactic Distribution:** `Enumeration` (13), `Passive_Enum` (4)
- **Top Extracted CLI Tools:** `reg` (17)

## LLM Distilled Operational Summary
### Key Operational Techniques & Decision Workflows

*   **Root Key Selection Strategy**:
    *   Use **HKCR** for file extension associations and COM/ActiveX object registration. Note that HKCR is a virtualized view combining per-user (`HKCU\Software\Classes`) and system-wide (`HKLM\Software\Classes`) data.
    *   Use **HKCU** for current user preferences and configuration; it dynamically points to the active profile (`ntuser.dat`).
    *   Use **HKLM** for system-wide, persistent configuration (booting, hardware, software installs) that survives reboots.
    *   Use **HKU** to inspect all loaded user profiles, including `.DEFAULT` for system account processes.
    *   Use **HKCC** only when troubleshooting specific hardware profile conflicts.
    *   Use **HKPD** programmatically to query performance counters (data resides outside the registry).

*   **Version-Specific Path Mapping**:
    *   Distinguish between Windows XP/2003 paths (e.g., `\Documents and Settings\`) and Vista/2008+ paths (e.g., `\Users\`) when correlating registry keys to physical files like `ntuser.dat` or `UsrClass.dat`.

### Critical Command Patterns and Required Flags

*   **Registry Enumeration**:
    *   `reg query HKLM\SYSTEM\CurrentControlSet\HardwareProfiles\Current /v CurrentProfile` (Retrieves current hardware profile ID via HKCC link).
    *   `reg query HKCR /v ""` (Lists file extension associations and COM classes).
    *   `reg query HKU /s` (Scans all loaded user profiles under HKU).

### Network Topology, IP/Subnet, Serial, or Service Relationships

*   **Service & Database Relationships**:
    *   **HKLM\SAM**: Directly linked to the **Security Accounts Manager** database; contains account/group data replicated across **Domain Controllers**.
    *   **HKLM\SECURITY**: Stores system-wide security policies enforced by **Domain Controllers**.
    *   **HKCR**: Serves as the bridge for **COM/ActiveX** interprocess communication, replacing legacy DDE mechanisms.

*   **Hardware Profile Linkage**:
    *   **HKCC** acts as a pointer to `HKLM\System\CurrentControlSet\HardwareProfiles\Current`, linking software configuration to specific hardware states.

<!-- CORA-MAXIMIZED-COMMANDS-START -->
## Maximized Windows & Linux Command Examples for `CQC001 E020 M010 Root Keys and Registry Types`

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
