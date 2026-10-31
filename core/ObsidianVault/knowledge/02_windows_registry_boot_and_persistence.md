---
title: "Domain Hub 02: Windows Registry Architecture, Boot Configuration (bcdedit), Startup & Persistence"
category: knowledge
domain_hub: "[[knowledge/02_windows_registry_boot_and_persistence]]"
os_platform: windows
primary_tactic: Passive_Enum
summary: "Windows Registry root keys (HKLM, HKCU, HKU, HKCR, HKCC), data types (REG_SZ, REG_DWORD, REG_BINARY), Run/RunOnce/Winlogon/Session Manager persistence keys, Boot Configuration Data (bcdedit), and startup forensics."
when_to_apply: "Apply when auditing Windows persistence mechanisms, inspecting Registry hives (`HKLM`/`HKCU`/`HKU`), analyzing boot sequences (`SMSS` -> `CSRSS` -> `Wininit` -> `Services` -> `LSASS` -> `Winlogon`), or checking `bcdedit` DEP/signing settings."
tags: [windows, registry, reg, bcdedit, autorunsc, schtasks, persistence, winlogon, boot, forensics, passive_enum]
updated: 2026-10-30
---

# Domain Hub 02: Windows Registry Architecture, Boot Configuration (bcdedit), Startup & Persistence

> **Summary:** Windows Registry root keys (HKLM, HKCU, HKU, HKCR, HKCC), data types (REG_SZ, REG_DWORD, REG_BINARY), Run/RunOnce/Winlogon/Session Manager persistence keys, Boot Configuration Data (bcdedit), and startup forensics.  
> **When to Apply:** Apply when auditing Windows persistence mechanisms, inspecting Registry hives (`HKLM`/`HKCU`/`HKU`), analyzing boot sequences (`SMSS` -> `CSRSS` -> `Wininit` -> `Services` -> `LSASS` -> `Winlogon`), or checking `bcdedit` DEP/signing settings.  
> **Target OS Platform:** `windows` | **Primary H-MDP Tactic:** `Passive_Enum` (`s_passive_topology_mapped -> s_active_services_enumerated`)  
> **Bayesian Root-Cause Alignment (`Engine 4`):** `registry_autorun_persistence, winlogon_shell_hijack, boot_bcd_tampering, scheduled_task_persistence`  
> **Network Isolation Compatibility:** `RED, BLUE, WHITE (100% local host telemetry compatible)`  
> **Backlinks:** [[00_MEMORY_INDEX]] | [[00_TRAINED_INDEX]] | [[commands/windows_master_command_playbook]] | [[commands/linux_master_command_playbook]]

---

## 1. Master Windows & Linux Command Matrix for This Domain

| Command Syntax (`Windows` / `Linux`) | OS / Shell | Operational Purpose & Key Flags | When to Apply & Expected Output | Cross-Platform Equivalent |
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

---

## 2. Organized Domain Knowledge Notes & Paired Command Playbooks (10 Notes)

| Topic | Knowledge Note (`knowledge/`) | Paired Command Playbook (`commands/`) | OS | Primary Tactic | When to Apply & Operational Summary |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **BcdEdit CMDs** | [[knowledge/trained_bcdedit_cmds]] | [[commands/trained_bcdedit_cmds]] | `windows` | `Passive_Enum` | Apply when working with BcdEdit CMDs (windows): Apply when auditing Windows persistence mechanisms, inspecting Registry hives (`HKLM`/`HKCU` |
| **Change System Files CMDs** | [[knowledge/trained_change_system_files_cmds]] | [[commands/trained_change_system_files_cmds]] | `windows` | `Passive_Enum` | Apply when working with Change System Files CMDs (windows): Apply when auditing Windows persistence mechanisms, inspecting Registry hives (` |
| **CQC001 E020 M010 Root Keys and Registry Types** | [[knowledge/trained_cqc001_e020_m010_root_keys_and_registry_types]] | [[commands/trained_cqc001_e020_m010_root_keys_and_registry_types]] | `windows` | `Passive_Enum` | Apply when working with CQC001 E020 M010 Root Keys and Registry Types (windows): Apply when auditing Windows persistence mechanisms, inspect |
| **CQC001 E020 M030 Boot and Logon Resource - Windows 7 - 2008** | [[knowledge/trained_cqc001_e020_m030_boot_and_logon_resource_-_windows_7_-_2008]] | [[commands/trained_cqc001_e020_m030_boot_and_logon_resource_-_windows_7_-_2008]] | `windows` | `Passive_Enum` | Apply when working with CQC001 E020 M030 Boot and Logon Resource - Windows 7 - 2008 (windows): Apply when auditing Windows persistence mecha |
| **CQC001 E020 M030 Boot and Logon Resource - Windows XP - 2003** | [[knowledge/trained_cqc001_e020_m030_boot_and_logon_resource_-_windows_xp_-_2003]] | [[commands/trained_cqc001_e020_m030_boot_and_logon_resource_-_windows_xp_-_2003]] | `windows` | `Passive_Enum` | Apply when working with CQC001 E020 M030 Boot and Logon Resource - Windows XP - 2003 (windows): Apply when auditing Windows persistence mech |
| **CQC001 E040 M010 transcript** | [[knowledge/trained_cqc001_e040_m010_transcript]] | [[commands/trained_cqc001_e040_m010_transcript]] | `windows` | `Passive_Enum` | Apply when working with CQC001 E040 M010 transcript (windows): Apply when auditing Windows persistence mechanisms, inspecting Registry hives |
| **CQC001 E040 M010 Windows Forensics** | [[knowledge/trained_cqc001_e040_m010_windows_forensics]] | [[commands/trained_cqc001_e040_m010_windows_forensics]] | `windows` | `Passive_Enum` | Apply when working with CQC001 E040 M010 Windows Forensics (windows): Apply when auditing Windows persistence mechanisms, inspecting Registr |
| **CQC001 E040 M010 Windows Startup Locations** | [[knowledge/trained_cqc001_e040_m010_windows_startup_locations]] | [[commands/windows_master_command_playbook]] / [[commands/linux_master_command_playbook]] | `windows` | `Passive_Enum` | Apply when working with CQC001 E040 M010 Windows Startup Locations (windows): Apply when auditing Windows persistence mechanisms, inspecting |
| **Registry CMDs** | [[knowledge/trained_registry_cmds]] | [[commands/trained_registry_cmds]] | `windows` | `Passive_Enum` | Apply when working with Registry CMDs (windows): Apply when auditing Windows persistence mechanisms, inspecting Registry hives (`HKLM`/`HKCU |
| **Windows XP  Explaining the Startup Process** | [[knowledge/trained_windows_xp__explaining_the_startup_process]] | [[commands/windows_master_command_playbook]] / [[commands/linux_master_command_playbook]] | `windows` | `Passive_Enum` | Apply when working with Windows XP  Explaining the Startup Process (windows): Apply when auditing Windows persistence mechanisms, inspecting |
