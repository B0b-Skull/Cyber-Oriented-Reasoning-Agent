---
title: windows_kernel_and_userspace_enumeration_playbook
category: commands
os_platform: windows
domain_hub: "[[knowledge/01_windows_system_process_and_sysinternals]]"
primary_tactic: Passive_Enum
summary: "Complete Windows 7, 10, 11 & Windows Server (2008 R2–2025) Ring -3 (UEFI/TPM), Ring -1 (Hyper-V/VBS/VTL1/HVCI/Credential Guard), Ring 0 (Kernel/Drivers/Minifilters/Object Manager/Mitigations), and Ring 3 (Boot Lineage, LSASS/Kerberos/NTLM Auth, Tokens, SIDs, DACLs/SACLs/SDDL, Privileges) Enumeration Command Playbook."
when_to_apply: "Apply whenever enumerating Windows 7, Windows 10, Windows 11, or Windows Server (2008 R2–2025) hardware rings (Ring -3/Ring -1/Ring 0/Ring 3), VBS/HVCI/Credential Guard state, kernel drivers/minifilters/callbacks, boot-to-shell process lineage (smss/csrss/wininit/services/lsass/winlogon), authentication packages, or securable object permissions (Tokens, SIDs, DACLs, SDDL, Privileges)."
tags: [commands, windows_internals, windows-internals, windows, windows7, windows10, windows11, server2025, ring0, ring3, vbs, hvci, vtl1, ntoskrnl, ntdll, driverquery, fltmc, bcdedit, smss, csrss, wininit, services, lsass, lsaiso, winlogon, svchost, whoami, klist, icacls, accesschk, sddl, dacl, token, privilege]
updated: 2026-10-31 01:18:00
---
# Windows 7, 10, 11 & Server (2008 R2–2025) Kernel-Space & User-Space Enumeration Command Playbook (`windows_kernel_and_userspace_enumeration_playbook`)

> **Paired Strategy Playbook:** [[reasoning/windows_kernel_and_userspace_enumeration_strategy_playbook]]  
> **Domain Hubs:** [[knowledge/01_windows_system_process_and_sysinternals]] | [[knowledge/02_windows_registry_boot_and_persistence]] | [[knowledge/03_windows_security_acls_auditing_and_logs]] | [[knowledge/04_windows_powershell_wmi_cim_and_active_directory]]  
> **Backlinks:** [[00_MEMORY_INDEX]] | [[commands/windows_master_command_playbook]] | [[commands/windows_digital_forensics_playbook]]

---

## 1. Layer 1: OS Build, Ring `-3` (Firmware / UEFI / Secure Boot / TPM 2.0) & Ring `-1` (`VBS` / `VTL 1` / `HVCI` / `Credential Guard`)

### 1.1 OS Kernel Version, HAL, Edition & Hotfix Baseline (Win 7 / 10 / 11 / Server 2008 R2–2025)
```powershell
# PowerShell (Win 7 SP1+ / Win 10 / Win 11 / Server 2008 R2–2025): Exact NT Build, UBR patch level, HAL, and Architecture
powershell -NoProfile -Command "$os = Get-WmiObject Win32_OperatingSystem; $cv = Get-ItemProperty 'HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion'; [pscustomobject]@{ProductName=$os.Caption; EditionID=$cv.EditionID; DisplayVersion=$cv.DisplayVersion; BuildNumber=$os.BuildNumber; UBR=$cv.UBR; KernelBuildEx=$cv.BuildLabEx; Architecture=$os.OSArchitecture; LastBoot=$os.ConvertToDateTime($os.LastBootUpTime); SystemDirectory=$os.SystemDirectory}"
```
```cmd
:: Native CMD fallback (Works on all Windows 7 / 10 / 11 / Server editions)
systeminfo & reg query "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion" /v BuildLabEx & reg query "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion" /v UBR
```

### 1.2 Ring `-3` Enumeration: UEFI vs. Legacy BIOS, Secure Boot (`PK`/`KEK`/`db`/`dbx`), TPM 2.0 & Boot Configuration (`BCD`)
```powershell
# Check Firmware Type (UEFI vs BIOS), Secure Boot State, and TPM 2.0 Status (Win 10 / 11 / Server 2016–2025)
powershell -NoProfile -Command "[pscustomobject]@{FirmwareType=$env:firmware_type; SecureBootEnabled=( try { Confirm-SecureBootUEFI } catch { 'BIOS_or_Unsupported' } ); TpmPresent=( try { (Get-Tpm).TpmPresent } catch { $false } ); TpmReady=( try { (Get-Tpm).TpmReady } catch { $false } )}"
```
```cmd
:: Inspect Boot Configuration Data (BCD): DEP (nx), Driver Signature Enforcement (testsigning/nointegritychecks), Kernel Debug, Hypervisor Launch
bcdedit /enum all
```
```cmd
:: Check Early Launch Anti-Malware (ELAM) & Boot Execute native NT binaries (smss.exe Phase)
reg query "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager" /v BootExecute
reg query "HKLM\ELAM" /s
```

### 1.3 Ring `-1` & `VTL 1` Enumeration: Hyper-V, Virtualization-Based Security (`VBS`), `HVCI` & `Credential Guard` (`LsaIso.exe`)
```powershell
# Query Win32_DeviceGuard for VBS Status, HVCI (KMCI), Credential Guard, and System Guard Secure Launch (Win 10 / 11 / Server 2016–2025)
# VirtualizationBasedSecurityStatus: 0 = Not Enabled, 1 = Enabled not running, 2 = Enabled and running in VTL 1
# SecurityServicesRunning: 1 = Credential Guard (LsaIso.exe), 2 = HVCI (Hypervisor-Protected Code Integrity), 3 = System Guard Secure Launch
powershell -NoProfile -Command "Get-CimInstance -ClassName Win32_DeviceGuard -Namespace root\Microsoft\Windows\DeviceGuard -EA 0 | Select-Object VirtualizationBasedSecurityStatus,SecurityServicesConfigured,SecurityServicesRunning,AvailableSecurityProperties,RequiredSecurityProperties,CodeIntegrityPolicyEnforcementStatus,UsermodeCodeIntegrityPolicyEnforcementStatus"
```
```cmd
:: Registry verification of DeviceGuard (VBS / HVCI), Vulnerable Driver Blocklist, and LSA Credential Guard (LsaCfgFlags)
reg query "HKLM\SYSTEM\CurrentControlSet\Control\DeviceGuard" /s
reg query "HKLM\SYSTEM\CurrentControlSet\Control\CI\Config" /v VulnerableDriverBlocklistEnable
reg query "HKLM\SYSTEM\CurrentControlSet\Control\Lsa" /v LsaCfgFlags
tasklist /v /fi "imagename eq Secure System" & tasklist /v /fi "imagename eq LsaIso.exe"
```

---

## 2. Layer 2: Ring `0` Kernel Space, Drivers (`.sys`), Minifilters (`FltMgr`), Memory Mitigations & Object Manager

### 2.1 Enumerate All Loaded Ring `0` Kernel Drivers (`ntoskrnl.exe`, `hal.dll`, `ci.dll`, WDM/KMDF `.sys`)
```powershell
# List all Running Kernel & FileSystem Drivers with StartMode, PathName, and ServiceType
powershell -NoProfile -Command "Get-WmiObject Win32_SystemDriver | Where-Object { $_.State -eq 'Running' } | Select-Object Name,DisplayName,ServiceType,StartMode,State,PathName | Sort-Object StartMode,Name | Format-Table -AutoSize"
```
```cmd
:: Native CMD verbose driver enumeration (includes Link Date timestamp, Driver Type, Paged/Non-Paged Pool usage)
driverquery /v /fo table
sc query type= driver state= active
```
```cmd
:: Sysinternals: Scan C:\Windows\System32\drivers for Unsigned, Test-Signed, or Non-Microsoft Ring 0 .sys Drivers (BYOVD / Rootkit Hunt)
sigcheck64.exe -accepteula -e -u -vr C:\Windows\System32\drivers
```

### 2.2 Enumerate File System Minifilter Drivers & Altitudes (`FltMgr.sys`)
```cmd
:: List all registered Ring 0 Minifilter drivers, their instance counts, and their deterministic Altitude (Requires Admin)
:: Altitudes: 360000-389999 = Activity Monitor (Sysmon/Procmon), 320000-329999 = Antivirus/EDR, 140000 = Encryption
fltmc filters
fltmc instances
fltmc volumes
```

### 2.3 Enumerate Ring `0` & Ring `3` Exploit Mitigations (`DEP`, `ASLR`, `CFG`, `CET Shadow Stacks`, `SEHOP`, `KVAS`)
```powershell
# System-wide Exploit Mitigations (Win 10 1709+ / Win 11 / Server 2019–2025)
powershell -NoProfile -Command "Get-ProcessMitigation -System"
```
```cmd
:: Check Kernel Virtual Address Shadow (KVAS / Meltdown) & Speculative Execution Mitigations, Session Manager Kernel Protection, and CrashControl
reg query "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Memory Management" /v FeatureSettingsOverride
reg query "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Memory Management" /v FeatureSettingsOverrideMask
reg query "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\kernel" /v DisableExceptionChainValidation
reg query "HKLM\SYSTEM\CurrentControlSet\Control\CrashControl"
```

### 2.4 Enumerate Ring `0` Object Manager Namespace (`\GLOBAL??`, `\Device`, `\BaseNamedObjects`, `\\.\pipe\`)
```powershell
# Enumerate all Named Pipes (\\.\pipe\*) exposed by Ring 0 / Ring 3 processes and inspect their DACL owners
powershell -NoProfile -Command "Get-ChildItem '\\.\pipe\' -EA 0 | ForEach-Object { $acl = try { Get-Acl $_.FullName -EA 0 } catch { $null }; [pscustomobject]@{PipeName=$_.Name; Owner=if($acl){$acl.Owner}else{'Protected/Denied'}; Access=if($acl){($acl.Access | ForEach-Object { $_.IdentityReference.Value + ':' + $_.FileSystemRights }) -join '; '}else{''}} } | Format-Table -AutoSize"
```
```cmd
:: Sysinternals WinObj / AccessChk: Inspect Ring 0 Object Manager directories (\Device, \Driver, \KernelObjects, \BaseNamedObjects)
accesschk64.exe -accepteula -o -q \Device
accesschk64.exe -accepteula -o -q \BaseNamedObjects
```

---

## 3. Layer 3: Boot-to-Logon Process Lineage (`System` $\to$ `smss` $\to$ `csrss`/`wininit`/`winlogon` $\to$ `services`/`lsass`/`svchost` $\to$ `explorer`) & Syscall Boundary

### 3.1 Reconstruct & Validate the Canonical Boot Process Lineage Tree
```powershell
# Inspect Core System Processes: Verify PID, PPID, Parent Name, SessionId, ExecutablePath, CommandLine, and Start Time
powershell -NoProfile -Command "$procs = Get-WmiObject Win32_Process; $map = @{}; foreach($p in $procs){ $map[$p.ProcessId] = $p.Name }; $procs | Where-Object { $_.Name -match '^(System|Registry|MemCompression|Secure System|smss\.exe|csrss\.exe|wininit\.exe|services\.exe|lsass\.exe|LsaIso\.exe|lsm\.exe|svchost\.exe|winlogon\.exe|LogonUI\.exe|dwm\.exe|fontdrvhost\.exe|userinit\.exe|explorer\.exe)$' } | Select-Object ProcessId,ParentProcessId,@{N='ParentName';E={$map[$_.ParentProcessId]}},SessionId,Name,ExecutablePath,CommandLine | Sort-Object SessionId,ProcessId | Format-Table -AutoSize"
```
```powershell
# Automated Anomaly Check on System Process Lineage (Flags any rogue path, wrong PPID, or wrong SessionId)
powershell -NoProfile -Command "$procs = Get-WmiObject Win32_Process; $byPid = @{}; foreach($p in $procs){ $byPid[$p.ProcessId] = $p }; foreach($p in $procs){ $n = $p.Name.ToLower(); $parent = $byPid[$p.ParentProcessId]; $pName = if($parent){$parent.Name.ToLower()}else{'<exited>'}; if($n -eq 'lsass.exe' -and ($p.SessionId -ne 0 -or $pName -ne 'wininit.exe' -or $p.ExecutablePath -ne 'C:\Windows\System32\lsass.exe')){ Write-Warning \"ANOMALY: lsass.exe PID=$($p.ProcessId) PPID=$($p.ParentProcessId)($pName) Session=$($p.SessionId) Path=$($p.ExecutablePath)\" }; if($n -eq 'services.exe' -and ($p.SessionId -ne 0 -or $pName -ne 'wininit.exe')){ Write-Warning \"ANOMALY: services.exe PID=$($p.ProcessId) PPID=$($p.ParentProcessId)($pName)\" }; if($n -eq 'svchost.exe' -and $pName -ne 'services.exe' -and $pName -ne 'MsMpEng.exe'){ Write-Warning \"ANOMALY: svchost.exe PID=$($p.ProcessId) Parent=$pName Cmd=$($p.CommandLine)\" } }"
```

### 3.2 Inspect Protected Process / Protected Process Light (`PPL` / `RunAsPPL`) & `KnownDLLs` (`ntdll.dll`)
```cmd
:: Check if LSA Protection (RunAsPPL) is enabled (1 = Enabled with UEFI lock, 2 = Enabled without UEFI lock)
reg query "HKLM\SYSTEM\CurrentControlSet\Control\Lsa" /v RunAsPPL
reg query "HKLM\SYSTEM\CurrentControlSet\Control\Lsa" /v RunAsPPLBoot
```
```cmd
:: Inspect Session Manager KnownDLLs pre-mapped into Ring 0 Section Objects (\KnownDlls) at boot
reg query "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\KnownDLLs"
```
```cmd
:: Sysinternals PSList & ListDLLs: Check process trees and detect any unsigned or unbacked DLLs in user space
pslist64.exe -accepteula -t
listdlls64.exe -accepteula -u
```

---

## 4. Layer 4: Windows Authentication Subsystem (`LSASS`, `SAM`, `NTLM`, `Kerberos`, `CloudAP`, `WDigest`, `DPAPI`)

### 4.1 Enumerate Active Logon Sessions (`LUIDs`), Authentication Packages & Kerberos Tickets
```cmd
:: List all active Logon Sessions (LUIDs), User, Auth Package (Kerberos / NTLM / Negotiate / CloudAP), and Logon Type
klist sessions
:: List cached Kerberos TGT and Service Tickets (TGS) in the current logon session (Encryption Type, Flags, Start/End Time)
klist
klist tgt
```
```powershell
# Correlate Win32_LogonSession (LogonType 2=Interactive, 3=Network, 4=Batch, 5=Service, 7=Unlock, 9=NewCredentials, 10=RDP, 11=CachedInteractive) with LoggedOnUser
powershell -NoProfile -Command "Get-WmiObject Win32_LogonSession | Select-Object LogonId,AuthenticationPackage,LogonType,StartTime | Sort-Object LogonType | Format-Table -AutoSize"
```

### 4.2 Audit LSA Authentication Packages, Security Packages, SSPs, `WDigest` & NTLM Policy
```cmd
:: Inspect all packages loaded into lsass.exe (Security Packages, Authentication Packages, Notification Packages / Password Filters)
reg query "HKLM\SYSTEM\CurrentControlSet\Control\Lsa" /v "Authentication Packages"
reg query "HKLM\SYSTEM\CurrentControlSet\Control\Lsa" /v "Security Packages"
reg query "HKLM\SYSTEM\CurrentControlSet\Control\Lsa" /v "Notification Packages"
reg query "HKLM\SYSTEM\CurrentControlSet\Control\Lsa\OSConfig" /v "Security Packages"
```
```cmd
:: Check WDigest Cleartext Password Caching (UseLogonCredential: 0 or absent = Disabled, 1 = Cleartext enabled in LSASS)
reg query "HKLM\SYSTEM\CurrentControlSet\Control\SecurityProviders\WDigest" /v UseLogonCredential
```
```cmd
:: Check NTLM Compatibility Level (LmCompatibilityLevel: 3-5 = NTLMv2 only; 5 = Refuse LM & NTLMv1) and NTLM Auditing/Restrictions
reg query "HKLM\SYSTEM\CurrentControlSet\Control\Lsa" /v LmCompatibilityLevel
reg query "HKLM\SYSTEM\CurrentControlSet\Control\Lsa\MSV1_0" /s
reg query "HKLM\SYSTEM\CurrentControlSet\Control\Lsa" /v CachedLogonsCount
```

### 4.3 Enumerate Windows Credential Manager, DPAPI MasterKeys, Vault & Entra ID / Azure AD State (`dsregcmd`)
```cmd
:: List saved credentials in Windows Credential Manager and Windows Vault
cmdkey /list
vaultcmd /list
vaultcmd /listcreds:"Windows Credentials" /all
vaultcmd /listcreds:"Web Credentials" /all
```
```cmd
:: Inspect Domain Join, Entra ID (Azure AD) Join, Primary Refresh Token (PRT), and TPM NGC state (Win 10 / 11 / Server 2016–2025)
dsregcmd /status
nltest /dsgetdc:%USERDOMAIN%
```

---

## 5. Layer 5: Access Control, Security Tokens (`_TOKEN`), UAC Split-Token & Privileges

### 5.1 Inspect Current Process Token (`SID`, `Group SIDs`, `Mandatory Integrity Level`, `Privileges`)
```cmd
:: Complete dump of current effective token: User SID, Group SIDs (including USE_FOR_DENY_ONLY), Integrity Level, and Privileges
whoami /all
whoami /groups
whoami /priv
```

### 5.2 Audit User Account Control (`UAC`) Split-Token & Local Account Token Filter Policies
```cmd
:: EnableLUA (1 = UAC Active), ConsentPromptBehaviorAdmin (0 = Elevate without prompt, 2 = Prompt on Secure Desktop, 5 = Default),
:: FilterAdministratorToken (0 = RID 500 un-filtered), LocalAccountTokenFilterPolicy (1 = Remote SMB/WMI Admin Token NOT filtered!)
reg query "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System" /v EnableLUA
reg query "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System" /v ConsentPromptBehaviorAdmin
reg query "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System" /v FilterAdministratorToken
reg query "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System" /v LocalAccountTokenFilterPolicy
```

### 5.3 Enumerate Local Users, Local Groups (`Administrators`, `Remote Desktop Users`, `Backup Operators`) & Account Policy
```cmd
net user
net accounts
net localgroup
net localgroup Administrators
net localgroup "Remote Desktop Users"
net localgroup "Backup Operators"
net localgroup "Remote Management Users"
```

---

## 6. Layer 6: Securable Object Permission (`DACL` / `SACL` / `SDDL`) Enumeration Across OS Subsystems

### 6.1 Audit Windows Service Permissions (`SDDL` & `AccessChk`) & Unquoted Service Paths
```cmd
:: Display raw SDDL security descriptor for a specific service (Look for DC=ChangeConfig, WD=WriteDAC, WO=WriteOwner, RP/WP=Start/Stop granted to BU/AU/WD/IU)
sc sdshow <ServiceName>
```
```powershell
# Scan ALL Windows Services for Unquoted Service Paths with spaces (excluding System32)
powershell -NoProfile -Command "Get-WmiObject Win32_Service | Where-Object { $_.PathName -and $_.PathName -notmatch '^\"' -and $_.PathName -notmatch '^C:\\Windows\\System32' -and ($_.PathName -split '\.exe')[0] -match ' ' } | Select-Object Name,DisplayName,StartMode,StartName,PathName | Format-Table -AutoSize"
```
```powershell
# Convert any Service SDDL string into human-readable Principal, AccessControlType, and Service Rights bitmask
powershell -NoProfile -Command "$sddl = (sc.exe sdshow Schedule | Where-Object { $_ -match '^D:' }).Trim(); $sd = New-Object System.Security.AccessControl.RawSecurityDescriptor($sddl); $sd.DiscretionaryAcl | Select-Object AceType,AceFlags,SecurityIdentifier,@{N='Principal';E={try{$_.SecurityIdentifier.Translate([System.Security.Principal.NTAccount]).Value}catch{$_.SecurityIdentifier.Value}}},@{N='AccessMaskHex';E={'0x{0:X8}' -f $_.AccessMask}}"
```
```cmd
:: Sysinternals AccessChk: Find all Windows Services writable by non-admin groups (Users, Authenticated Users, Everyone)
accesschk64.exe -accepteula -uwcqv "Users" *
accesschk64.exe -accepteula -uwcqv "Authenticated Users" *
accesschk64.exe -accepteula -uwcqv "Everyone" *
```

### 6.2 Audit File & Directory `DACLs` / `SACLs` (`icacls` & `Get-Acl`)
```cmd
:: Inspect NTFS DACL and Mandatory Integrity Label on critical directories and service binaries
icacls "C:\Program Files"
icacls "C:\Windows\Temp"
```
```powershell
# Check if any directory in the system %PATH% grants Write/Modify/FullControl to BUILTIN\Users, Everyone, or Authenticated Users
powershell -NoProfile -Command "($env:Path -split ';') | Where-Object { $_ -and (Test-Path $_) } | ForEach-Object { $dir = $_; (Get-Acl $dir -EA 0).Access | Where-Object { $_.IdentityReference -match 'Users|Everyone|Authenticated Users' -and $_.FileSystemRights -match 'Write|Modify|FullControl' } | Select-Object @{N='PathDir';E={$dir}},IdentityReference,FileSystemRights,AccessControlType }"
```

### 6.3 Audit Registry Key `DACLs` (`HKLM\SYSTEM\CurrentControlSet\Services` & `Run` Keys)
```powershell
# Scan HKLM\SYSTEM\CurrentControlSet\Services\* Registry keys for non-admin WriteKey / FullControl permissions
powershell -NoProfile -Command "Get-ChildItem 'HKLM:\SYSTEM\CurrentControlSet\Services' -EA 0 | ForEach-Object { $k = $_.Name; (Get-Acl $_.PSPath -EA 0).Access | Where-Object { $_.IdentityReference -match 'Users|Everyone|Authenticated Users|INTERACTIVE' -and $_.RegistryRights -match 'WriteKey|SetValue|FullControl|ChangePermissions|TakeOwnership' } | Select-Object @{N='ServiceKey';E={$k}},IdentityReference,RegistryRights }"
```
```cmd
:: Sysinternals AccessChk: Scan Registry Services hive for keys writable by Users or Authenticated Users
accesschk64.exe -accepteula -uwqk "Users" HKLM\SYSTEM\CurrentControlSet\Services
accesschk64.exe -accepteula -uwqk "Authenticated Users" HKLM\SYSTEM\CurrentControlSet\Services
```

### 6.4 Audit Process & Thread Security Descriptors (`_EPROCESS` / `_ETHREAD` Ring `0` Object Headers)
```cmd
:: Sysinternals AccessChk: Check which running processes grant PROCESS_ALL_ACCESS or PROCESS_VM_WRITE to current user/Users
accesschk64.exe -accepteula -uwqp "Users" *
accesschk64.exe -accepteula -qp -v lsass.exe
```
