---
title: "Trained Knowledge & Topology: CQC001 E020 M030 Boot and Logon Resource - Windows XP - 2003"
category: knowledge
domain_hub: "[[knowledge/02_windows_registry_boot_and_persistence]]"
os_platform: windows
primary_tactic: Passive_Enum
summary: "Operational architecture, decision workflows & Windows/Linux command reference for CQC001 E020 M030 Boot and Logon Resource - Windows XP - 2003: Windows Registry root keys (HKLM, HKCU, HKU, HKCR, HKCC), data types (REG_SZ, REG_DWORD, REG_BINARY), Run/RunOnce/Winlogon/Session"
when_to_apply: "Apply when working with CQC001 E020 M030 Boot and Logon Resource - Windows XP - 2003 (windows): Apply when auditing Windows persistence mechanisms, inspecting Registry hives (`HKLM`/`HKCU`/`HKU`), analyzing boot sequences (`SMSS` -> `CSRSS` -> `Wininit` -> `Services` -> `LSASS` -> `Winlogon`), or checking `bcdedit` DEP/signing settings."
tags: [mdp, pdf, trained, windows, registry, reg, bcdedit, autorunsc, schtasks, persistence, winlogon, boot, forensics, passive_enum, linux]
source_file: "CQC001 E020 M030 Boot and Logon Resource - Windows XP - 2003"
updated: 2026-10-30
---

# Trained Knowledge & Architecture: `CQC001_E020_M030_Boot_and_Logon_Resource_-_Windows_XP_-_2003.pdf`

- **Source Path:** `~/Projects/CORA/Training/CQC001_E020_M030_Boot_and_Logon_Resource_-_Windows_XP_-_2003.pdf` (`pdf`)
- **Extracted Technical Entities:** `general`
- **Extracted IPs / Subnets:** `None`
- **Extracted Interfaces:** `None`

## LLM Distilled Operational Summary
### Key Operational Techniques & Decision Workflows

*   **Boot Sequence Execution**: The system initializes via the Master Boot Record (MBR) and Partition Boot Sector (PBS), loading the `NTLDR` bootloader. `NTLDR` reads `boot.ini` to determine the OS load path, checks for hibernation status, and transfers control to `Winload.exe`.
*   **Kernel Initialization (Phase 0 & 1)**: `Ntoskrnl.exe` initializes core subsystems (HAL, Memory Manager, Plug and Play) and loads `BOOT_START` drivers. In Phase 1, it loads `SYSTEM_START` drivers and launches the Session Manager (`Smss.exe`).
*   **Session & Logon Orchestration**: `Smss.exe` starts `Win32k.sys`, `Csrss.exe`, and `Winlogon.exe`. `Winlogon` loads the GINA (Graphical Identification and Authentication) module to present the logon dialog.
*   **Secure Attention Sequence (SAS)**: Upon receiving a keystroke combination (e.g., Ctrl+Alt+Del), `Winlogon` displays the Secure Desktop and loads the GINA to collect credentials.
*   **Authentication Workflow**: Credentials are passed via secure ALPC to `Lsass.exe`. `Lsass` invokes an Authentication Package (AP) to hash the entered password and compare it against the stored hash in the SAM/AD database, while checking for policy restrictions.

### Critical Command Patterns and Required Flags

*   **Boot Configuration**: `NTLDR` reads `boot.ini` to select the OS. If multiple OSes exist, it presents a Boot Selection Menu.
*   **Hibernation Recovery**: If hibernation is detected, `NTLDR` loads `Hiberfil.sys` and `resume.exe`; otherwise, it loads the standard `Winload.exe`.
*   **Session Initialization**: `Smss.exe` executes programs specified in the `BootExecute` registry key and processes delayed file operations.
*   **Service Loading**: `Winlogon` starts the Service Control Manager (`Services.exe`) to load `AUTO_START` services and device drivers.

### Network Topology, IP/Subnet, Serial, or Service Relationships

*   **Service Dependencies**:
    *   `Ntoskrnl.exe` pairs with `HAL.dll` (Hardware Abstraction Layer).
    *   `Smss.exe` launches `Win32k.sys`, `Csrss.exe`, and `Winlogon.exe`.
    *   `Winlogon.exe` launches `Services.exe` and `Lsass.exe`.
    *   `Userinit.exe` is the first process launched in the user session, loading the user profile and shell.
*   **Data Flow**:
    *   `Ntdetect.com` populates the `HKLM\HARDWARE` registry hive during kernel initialization.
    *   `Winlogon` communicates with `Lsass.exe` via a secure Advanced Local Procedure Call (ALPC) connection.
    *   Authentication Packages interact with the Security Accounts Manager (SAM) or Active Directory (AD) database to retrieve account information and stored password hashes.

<!-- CORA-MAXIMIZED-COMMANDS-START -->
## Maximized Windows & Linux Command Examples for `CQC001 E020 M030 Boot and Logon Resource - Windows XP - 2003`

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
