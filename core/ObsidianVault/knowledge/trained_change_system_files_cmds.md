---
title: "Trained Knowledge & Topology: Change System Files CMDs"
category: knowledge
domain_hub: "[[knowledge/02_windows_registry_boot_and_persistence]]"
os_platform: windows
primary_tactic: Passive_Enum
summary: "Operational architecture, decision workflows & Windows/Linux command reference for Change System Files CMDs: Windows Registry root keys (HKLM, HKCU, HKU, HKCR, HKCC), data types (REG_SZ, REG_DWORD, REG_BINARY), Run/RunOnce/Winlogon/Session"
when_to_apply: "Apply when working with Change System Files CMDs (windows): Apply when auditing Windows persistence mechanisms, inspecting Registry hives (`HKLM`/`HKCU`/`HKU`), analyzing boot sequences (`SMSS` -> `CSRSS` -> `Wininit` -> `Services` -> `LSASS` -> `Winlogon`), or checking `bcdedit` DEP/signing settings."
tags: [bcdedit, cacls, defense_evasion_firewall, enumeration, icacls, ipconfig, mdp, passive_enum, privilege_escalation, text, trained, wmic, windows, registry, reg, autorunsc, schtasks, persistence, winlogon, boot, forensics, linux]
source_file: "Change System Files CMDs"
updated: 2026-10-30
---

# Trained Knowledge & Architecture: `Change System Files CMDs.txt`

- **Source Path:** `~/Projects/CORA/Training/Change System Files CMDs.txt` (`text`)
- **Extracted Technical Entities:** `bcdedit, cacls, icacls, ipconfig, wmic`
- **Extracted IPs / Subnets:** `None`
- **Extracted Interfaces:** `None`
- **Linked Command Playbook:** [[commands/trained_change_system_files_cmds]] (`31` CEGAR-verified commands | `31` MDP transitions)

## Command & Tactic Coverage Summary
- **Total CEGAR-Verified Commands:** `31` (full executable list in [[commands/trained_change_system_files_cmds]])
- **Tactic Distribution:** `Defense_Evasion_Firewall` (14), `Passive_Enum` (7), `Enumeration` (6), `Privilege_Escalation` (4)
- **Top Extracted CLI Tools:** `copy` (9), `del` (4), `dir` (3), `bcdedit` (2), `icacls` (2), `wmic` (2), `cacls` (1), `movelatr` (1), `pechksum` (1), `reg` (1), `ren` (1), `rename` (1), `sfc` (1), `shell` (1), `takeown` (1)

## LLM Distilled Operational Summary
### Operational Techniques & Decision Workflows
*   **File Discovery & Verification**: Use `dir C:\ /s /b | find "filename.exe"` to locate executables recursively. Verify directory contents after deletions using `dir /on` to ensure no orphaned files remain.
*   **Backup & Restore Workflow**: Establish a backup before modification (e.g., `copy %systemroot%\system32\ipconfig.exe "C:\...\ipconfig.bak"`), perform the operation, then restore from the backup if needed.
*   **DLL Cache Manipulation**: When modifying system DLLs, check the `dllcache` folder (`cd %systemroot%\system32\dllcache`) and ensure consistency between the live file and the cache to prevent boot issues.
*   **Permission Management**: Use `takeown` followed by `icacls` to grant specific user groups (e.g., `win7\administrator`) full control (`(F)`) over system files before modification.
*   **System File Checker (SFC)**: Run `sfc /SCANFILE=<path>` to verify file integrity post-modification, or `sfc /scannow` for a full system check.
*   **Data Execution Prevention (DEP) Configuration**: Modify OS security policies using `bcdedit /set nx <MODE>` where modes include `AlwaysOff`, `AlwaysOn`, `OptOut`, or `OptIn`. Verify changes with `wmic OS Get DataExecutionPrevention_*`.

### Critical Command Patterns & Required Flags
*   **Recursive Directory Search**: `dir <Path> /s /b | find "<Target>"`
*   **File Backup**: `copy <Source> "<Destination>.bak"`
*   **File Replacement**: `del <OldPath> & copy <NewPath> <OldPath>`
*   **Permission Granting**: `icacls <Path> /grant <User>:(F)`
*   **BCD Configuration**: `bcdedit /set nx <MODE>` (Requires reboot for effect).
*   **Checksum Verification**: `PEChksum.exe <Path>` (Custom tool usage).

### Network Topology & Service Relationships
*   **System Root**: All operations target `%systemroot%\system32\` (typically `C:\Windows\System32`).
*   **DLL Cache**: Critical relationship exists between `%systemroot%\system32\` and `%systemroot%\system32\dllcache\`. Modifications to one must reflect in the other to maintain system stability.
*   **User Context**: Backups are often stored in user-specific directories like `C:\Documents and Settings\administrator\desktop\`.
*   **Service Impact**: Modifying `ipconfig.exe` or `notepad.exe` directly affects network diagnostics and user interface services respectively. Changing `sfcfiles.dll` impacts the System File Checker utility.

<!-- CORA-MAXIMIZED-COMMANDS-START -->
## Maximized Windows & Linux Command Examples for `Change System Files CMDs`

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
