---
title: "Trained Command Playbook: CQC001 E020 M010 Root Keys and Registry Types"
category: commands
domain_hub: "[[knowledge/02_windows_registry_boot_and_persistence]]"
os_platform: windows
primary_tactic: Passive_Enum
summary: "Verified Windows & Linux command playbook for CQC001 E020 M010 Root Keys and Registry Types (Passive_Enum): Windows Registry root keys (HKLM, HKCU, HKU, HKCR, HKCC), data types (REG_SZ, REG_DWORD, REG_BINARY), Run/RunOnce/Winlogon/Session Mana"
when_to_apply: "Apply when working with CQC001 E020 M010 Root Keys and Registry Types (windows): Apply when auditing Windows persistence mechanisms, inspecting Registry hives (`HKLM`/`HKCU`/`HKU`), analyzing boot sequences (`SMSS` -> `CSRSS` -> `Wininit` -> `Services` -> `LSASS` -> `Winlogon`), or checking `bcdedit` DEP/signing settings."
tags: [bcdedit, enumeration, http, https, mdp, passive_enum, pdf, trained, windows, registry, reg, autorunsc, schtasks, persistence, winlogon, boot, forensics, linux]
source_file: "CQC001 E020 M010 Root Keys and Registry Types"
updated: 2026-10-30
---

reg query "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Run" && reg query "HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Run"
# Trained Command Playbook: `CQC001_E020_M010_Root_Keys_and_Registry_Types.pdf`
reg query "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Run" && reg query "HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Run"
- **Source Document:** `~/Projects/CORA/Training/CQC001_E020_M010_Root_Keys_and_Registry_Types.pdf`
- **CEGAR Verified Commands:** `17` (`0` malformed/unsafe snippets filtered)
- **MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`):** `17`
- **Discovered IPs/Subnets:** `None`
- **Discovered Interfaces:** `None`
- **Related Knowledge Note:** [[knowledge/trained_cqc001_e020_m010_root_keys_and_registry_types]]
reg query "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Run" && reg query "HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Run"
## Distilled MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`)
| Pre-State ($s$) | Tactic ($\tau$) | Technique ($k$) | Tool ($u$) | Post-State ($s'$) | Verified Command ($c$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `reg` | `s_passive_topology_mapped` | `Reg query` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `reg` | `s_active_services_enumerated` | `Reg add` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `reg` | `s_passive_topology_mapped` | `reg query <KeyName> [{/v <ValueName> \| /ve}] [/s] [/se <Separator>] [/f <Data>] [{/k \| /d}] [/c] [/e] [/t <Type>] [/z]` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `reg` | `s_active_services_enumerated` | `reg add <KeyName> [{/v ValueName \| /ve}] [/t DataType] [/s Separator] [/d Data] [/f]` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `reg` | `s_passive_topology_mapped` | `REG Query HKLM\Software /F "C:\Program Files (x86)\Cisco" /S` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `reg` | `s_active_services_enumerated` | `Reg save` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `reg` | `s_passive_topology_mapped` | `Reg query https://web.archive.org/web/20160721105928/https://technet.microsoft.com/en-us/library/cc742028.aspx` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `reg` | `s_active_services_enumerated` | `reg save <KeyName> <FileName> [/y]` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `reg` | `s_active_services_enumerated` | `REG SAVE HKLM\Software\MyCo\MyProgram ProgramBkUp.hiv` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `reg` | `s_active_services_enumerated` | `Reg export` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `reg` | `s_active_services_enumerated` | `Reg export KeyName FileName [/y]` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `reg` | `s_active_services_enumerated` | `reg export HKLM\Software\MyCo\MyProgram ProgramBkUp.reg` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `reg` | `s_active_services_enumerated` | `Reg import` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `reg` | `s_active_services_enumerated` | `REG IMPORT FileName.reg` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `reg` | `s_active_services_enumerated` | `Reg restore` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `reg` | `s_active_services_enumerated` | `REG RESTORE \\MachineName\[ROOT]\KeyName FileName.hiv` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `reg` | `s_active_services_enumerated` | `Reg add https://web.archive.org/web/20160721105853/https://technet.microsoft.com/en-us/library/cc742162.aspx` |
reg query "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Run" && reg query "HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Run"
## Verified Executable Commands (Grouped by Capability Layer)
reg query "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Run" && reg query "HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Run"
### General_System (15 commands)
```bash
Reg query
reg query <KeyName> [{/v <ValueName> | /ve}] [/s] [/se <Separator>] [/f <Data>] [{/k | /d}] [/c] [/e] [/t <Type>] [/z]
REG Query HKLM\Software /F "C:\Program Files (x86)\Cisco" /S
Reg add
reg add <KeyName> [{/v ValueName | /ve}] [/t DataType] [/s Separator] [/d Data] [/f]
Reg save
reg save <KeyName> <FileName> [/y]
REG SAVE HKLM\Software\MyCo\MyProgram ProgramBkUp.hiv
Reg export
Reg export KeyName FileName [/y]
reg export HKLM\Software\MyCo\MyProgram ProgramBkUp.reg
Reg import
REG IMPORT FileName.reg
Reg restore
REG RESTORE \\MachineName\[ROOT]\KeyName FileName.hiv
```
reg query "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Run" && reg query "HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Run"
### L7_HTTP_Web (2 commands)
```bash
Reg add https://web.archive.org/web/20160721105853/https://technet.microsoft.com/en-us/library/cc742162.aspx
Reg query https://web.archive.org/web/20160721105928/https://technet.microsoft.com/en-us/library/cc742028.aspx
```
reg query "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Run" && reg query "HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Run"

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
