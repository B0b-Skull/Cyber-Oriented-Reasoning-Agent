---
title: "Trained Knowledge & Topology: Windows XP  Explaining the Startup Process"
category: knowledge
domain_hub: "[[knowledge/02_windows_registry_boot_and_persistence]]"
os_platform: windows
primary_tactic: Passive_Enum
summary: "Operational architecture, decision workflows & Windows/Linux command reference for Windows XP  Explaining the Startup Process: Windows Registry root keys (HKLM, HKCU, HKU, HKCR, HKCC), data types (REG_SZ, REG_DWORD, REG_BINARY), Run/RunOnce/Winlogon/Session"
when_to_apply: "Apply when working with Windows XP  Explaining the Startup Process (windows): Apply when auditing Windows persistence mechanisms, inspecting Registry hives (`HKLM`/`HKCU`/`HKU`), analyzing boot sequences (`SMSS` -> `CSRSS` -> `Wininit` -> `Services` -> `LSASS` -> `Winlogon`), or checking `bcdedit` DEP/signing settings."
tags: [http, mdp, pdf, serial, trained, windows, registry, reg, bcdedit, autorunsc, schtasks, persistence, winlogon, boot, forensics, passive_enum, linux]
source_file: "Windows XP  Explaining the Startup Process"
updated: 2026-10-30
---

# Trained Knowledge & Architecture: `Windows XP_ Explaining the Startup Process.pdf`

- **Source Path:** `~/Projects/CORA/Training/Windows XP_ Explaining the Startup Process.pdf` (`pdf`)
- **Extracted Technical Entities:** `http, serial`
- **Extracted IPs / Subnets:** `None`
- **Extracted Interfaces:** `None`

## LLM Distilled Operational Summary
### Key Operational Techniques & Decision Workflows

*   **Five-Stage Startup Architecture**: The system progresses through five distinct phases: Preboot Sequence, Boot Sequence, Kernel Load, Kernel Initialization, and Logon.
*   **Preboot Sequence Workflow**:
    *   Executes Power-On Self-Test (POST) to verify hardware presence and memory.
    *   BIOS locates the boot device and loads the Master Boot Record (MBR).
    *   MBR identifies the active partition, loads the boot sector, and executes it.
    *   Loads and initializes `NTLDR` (NT Loader).
    *   *Troubleshooting*: If POST fails, check hardware; if MBR is corrupt, use the Recovery Console; if a non-system disk is detected, remove floppy/USB media as BIOS prioritizes these drives.
*   **Boot Sequence Workflow**:
    *   **Initial Boot Loader**: `NTLDR` switches the CPU from real mode to 32-bit flat memory mode and loads minifile system drivers to support FAT, FAT32, or NTFS partitions.
    *   **Operating System Selection**: `NTLDR` reads `BOOT.INI`. If multiple OSes exist, a selection menu appears; otherwise, the default (most recent) installation loads automatically. If `BOOT.INI` is missing, `NTLDR` defaults to the first partition of the first disk.
    *   **Hardware Detection**: `NTDETECT.COM` and `NTOSKRNL.EXE` detect hardware components (bus types, ports, adapters, etc.) and populate `HKEY_LOCAL_MACHINE\HARDWARE` in the Registry.
    *   **Configuration Selection**: Prepares the environment for user interaction and final kernel loading.

### Critical Command Patterns and Required Flags

*   **Primary Loader**: `NTLDR` (NT Loader) is the core executable responsible for transitioning the system state and managing OS selection.
*   **Configuration File**: `BOOT.INI` defines the boot menu, default OS, and timeout settings.
*   **Detection Utility**: `NTDETECT.COM` performs hardware enumeration.
*   **Kernel Image**: `NTOSKRNL.EXE` contains the core kernel logic executed after detection.
*   **Legacy Support**: `BOOTSECT.DOS` is loaded only if a non-Windows XP OS (e.g., Windows 98) is selected from the menu.

### Network Topology, IP/Subnet, Serial, or Service Relationships

*   **Service Dependencies**: The startup process relies on the BIOS for initial hardware enumeration and the MBR for partition activation before `NTLDR` takes control.
*   **Hardware Enumeration Scope**: `NTDETECT.COM` dynamically scans for physical interfaces including SCSI adapters, communication ports (serial/parallel), video adapters, and pointing devices, mapping them into the system registry rather than relying on static network topology definitions at this stage.
*   **Boot Device Priority**: The BIOS configuration dictates the boot order, typically prioritizing floppy drives and USB flash drives over hard drives, which can interrupt the standard hard disk boot path if media is present.

## Extracted Operational Steps & Workflows
- 1. The computer runs power­on self test (POST) routines to determine the amount of
- 2. The computer BIOS locates the boot device, and then loads and runs the Master
- 3. The MBR scans the partition table to locate the active partition, loads the boot sec­
- 4. The computer loads and initializes the NTLDR file, which is the operating system

<!-- CORA-MAXIMIZED-COMMANDS-START -->
## Maximized Windows & Linux Command Examples for `Windows XP  Explaining the Startup Process`

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
