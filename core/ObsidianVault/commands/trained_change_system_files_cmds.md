---
title: "Trained Command Playbook: Change System Files CMDs"
category: commands
domain_hub: "[[knowledge/02_windows_registry_boot_and_persistence]]"
os_platform: windows
primary_tactic: Passive_Enum
summary: "Verified Windows & Linux command playbook for Change System Files CMDs (Passive_Enum): Windows Registry root keys (HKLM, HKCU, HKU, HKCR, HKCC), data types (REG_SZ, REG_DWORD, REG_BINARY), Run/RunOnce/Winlogon/Session Mana"
when_to_apply: "Apply when working with Change System Files CMDs (windows): Apply when auditing Windows persistence mechanisms, inspecting Registry hives (`HKLM`/`HKCU`/`HKU`), analyzing boot sequences (`SMSS` -> `CSRSS` -> `Wininit` -> `Services` -> `LSASS` -> `Winlogon`), or checking `bcdedit` DEP/signing settings."
tags: [bcdedit, cacls, defense_evasion_firewall, enumeration, icacls, ipconfig, mdp, passive_enum, privilege_escalation, text, trained, wmic, windows, registry, reg, autorunsc, schtasks, persistence, winlogon, boot, forensics, linux]
source_file: "Change System Files CMDs"
updated: 2026-10-30
---

reg query "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Run" && reg query "HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Run"
# Trained Command Playbook: `Change System Files CMDs.txt`
reg query "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Run" && reg query "HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Run"
- **Source Document:** `~/Projects/CORA/Training/Change System Files CMDs.txt`
- **CEGAR Verified Commands:** `31` (`0` malformed/unsafe snippets filtered)
- **MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`):** `31`
- **Discovered IPs/Subnets:** `None`
- **Discovered Interfaces:** `None`
- **Related Knowledge Note:** [[knowledge/trained_change_system_files_cmds]]
reg query "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Run" && reg query "HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Run"
## Distilled MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`)
| Pre-State ($s$) | Tactic ($\tau$) | Technique ($k$) | Tool ($u$) | Post-State ($s'$) | Verified Command ($c$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `dir` | `s_passive_topology_mapped` | `dir C:\ /s /b \| find "ipconfig.exe"` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `del` | `s_firewall_or_acl_unlocked` | `del %systemroot%\system32\ipconfig.exe & dir /on %systemroot%\system32\ipc*` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `copy` | `s_active_services_enumerated` | `copy c:\Solitaire.exe %systemroot%\system32\ipconfig.exe` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `icacls` | `s_interactive_tty_or_priv_escalated` | `icacls %systemroot%\notepad.exe /grant win7\administrator:(F)` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `reg` | `s_passive_topology_mapped` | `Reg query "hklm\system\currentcontrolset\control\session manager"` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `copy` | `s_firewall_or_acl_unlocked` | `copy %systemroot%\system32\ipconfig.exe "c:\documents and settings\administrator\desktop\ipconfig.bak"` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `copy` | `s_active_services_enumerated` | `copy "C:\Documents and Settings\administrator\desktop\ipconfig.bak" %systemroot%\system32\ipconfig.exe` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `cacls` | `s_interactive_tty_or_priv_escalated` | `cacls %systemroot%\notepad.exe` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `dir` | `s_passive_topology_mapped` | `dir C:\ /s /b \| find "notepad.exe"` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `copy` | `s_firewall_or_acl_unlocked` | `copy %systemroot%\system32\calc.exe %systemroot%\system32\ipconfig.exe` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `copy` | `s_active_services_enumerated` | `copy "C:\Documents and Settings\administrator\desktop\ipconfig.bak" "C:\Documents and Settings\administrator\desktop\ypconfig.exe"` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `takeown` | `s_interactive_tty_or_priv_escalated` | `takeown /f %systemroot%\system32\ipconfig.exe` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `dir` | `s_passive_topology_mapped` | `dir notepad*` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `del` | `s_firewall_or_acl_unlocked` | `del %systemroot%\system32\ipconfig.exe` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `copy` | `s_active_services_enumerated` | `copy "C:\Documents and Settings\administrator\desktop\ypconfig.exe" %systemroot%\system32\ypconfig.exe` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `icacls` | `s_interactive_tty_or_priv_escalated` | `icacls %systemroot%\system32\ipconfig.exe /grant win7\administrator:(F)` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `` | `s_passive_topology_mapped` | `sigcheck\ -i %systemroot%\notepad.exe -accepteula` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `copy` | `s_firewall_or_acl_unlocked` | `copy %systemroot%\system32\sfcfiles.dll "c:\Documents and Settings\administrator\desktop\sfcfiles.bak"` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `copy` | `s_active_services_enumerated` | `copy %systemroot%\notepad.exe "%username%\desktop\ipconfig.bak"` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `wmic` | `s_passive_topology_mapped` | `wmic OS Get DataExecutionPrevention_Availabl` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `copy` | `s_firewall_or_acl_unlocked` | `copy %systemroot%\system32\sfcfiles.dll %systemroot%\system32\mysfcfiles.dll` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `del` | `s_active_services_enumerated` | `del %systemroot%\notepad.bak` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `wmic` | `s_passive_topology_mapped` | `wmic OS Get DataExecutionPrevention_SupportPolicy` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `pechksum` | `s_firewall_or_acl_unlocked` | `PEChksum.exe %systemroot%\system32\mysfcfiles.dll` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `movelatr` | `s_firewall_or_acl_unlocked` | `Movelatr.exe %systemroot%\system32\mysfcfiles.dll %systemroot%\system32\sfcfiles.dll` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `del` | `s_firewall_or_acl_unlocked` | `del %systemroot%\system32\ipconfig.exe & del %systemroot%\system32\dllcache\ipconfig.exe %systemroot%\system32\ipconfig.exe` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `ren` | `s_firewall_or_acl_unlocked` | `ren c:\windows\notepad.exe notepad.bak` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `rename` | `s_firewall_or_acl_unlocked` | `rename %systemroot%\notepad.exe notepad.bak` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `sfc` | `s_firewall_or_acl_unlocked` | `sfc /SCANFILE=%systemroot%\notepad.exe` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `bcdedit` | `s_firewall_or_acl_unlocked` | `bcdedit /set nx OptOut` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `bcdedit` | `s_firewall_or_acl_unlocked` | `bcdedit /set nx [MODE]; where the [MODE] is either: AlwaysOff, AlwaysOn, OptOut, or OptIn` |
reg query "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Run" && reg query "HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Run"
## Verified Executable Commands (Grouped by Capability Layer)
reg query "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Run" && reg query "HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Run"
### General_System (31 commands)
```bash
dir C:\ /s /b | find "ipconfig.exe"
del %systemroot%\system32\ipconfig.exe & dir /on %systemroot%\system32\ipc*
copy %systemroot%\system32\ipconfig.exe "c:\documents and settings\administrator\desktop\ipconfig.bak"
copy c:\Solitaire.exe %systemroot%\system32\ipconfig.exe
copy %systemroot%\system32\calc.exe %systemroot%\system32\ipconfig.exe
del %systemroot%\system32\ipconfig.exe
copy "C:\Documents and Settings\administrator\desktop\ipconfig.bak" %systemroot%\system32\ipconfig.exe
copy %systemroot%\system32\sfcfiles.dll "c:\Documents and Settings\administrator\desktop\sfcfiles.bak"
copy %systemroot%\system32\sfcfiles.dll %systemroot%\system32\mysfcfiles.dll
PEChksum.exe %systemroot%\system32\mysfcfiles.dll
Reg query "hklm\system\currentcontrolset\control\session manager"
Movelatr.exe %systemroot%\system32\mysfcfiles.dll %systemroot%\system32\sfcfiles.dll
del %systemroot%\system32\ipconfig.exe & del %systemroot%\system32\dllcache\ipconfig.exe %systemroot%\system32\ipconfig.exe
copy "C:\Documents and Settings\administrator\desktop\ipconfig.bak" "C:\Documents and Settings\administrator\desktop\ypconfig.exe"
copy "C:\Documents and Settings\administrator\desktop\ypconfig.exe" %systemroot%\system32\ypconfig.exe
dir C:\ /s /b | find "notepad.exe"
copy %systemroot%\notepad.exe "%username%\desktop\ipconfig.bak"
ren c:\windows\notepad.exe notepad.bak
icacls %systemroot%\notepad.exe /grant win7\administrator:(F)
rename %systemroot%\notepad.exe notepad.bak
del %systemroot%\notepad.bak
dir notepad*
sfc /SCANFILE=%systemroot%\notepad.exe
cacls %systemroot%\notepad.exe
sigcheck\ -i %systemroot%\notepad.exe -accepteula
bcdedit /set nx OptOut
bcdedit /set nx [MODE]; where the [MODE] is either: AlwaysOff, AlwaysOn, OptOut, or OptIn
wmic OS Get DataExecutionPrevention_Availabl
wmic OS Get DataExecutionPrevention_SupportPolicy
takeown /f %systemroot%\system32\ipconfig.exe
icacls %systemroot%\system32\ipconfig.exe /grant win7\administrator:(F)
```
reg query "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Run" && reg query "HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Run"

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
