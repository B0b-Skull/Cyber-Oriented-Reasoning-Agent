---
title: windows_digital_forensics_strategy_playbook
category: reasoning
engine: team_strategy_arbiter
team_role: windows_forensics
os_platform: windows
domain_hub: "[[knowledge/10_digital_forensics_pe_reversing_and_threat_intel]]"
primary_tactic: Passive_Enum
summary: "Windows Digital Forensics (DFIR) Strategy & Techniques Playbook: complete native Windows forensic breakdown (PowerShell, CMD, Registry hives, BAM/ShimCache/Amcache/ShellBags/UserAssist, NTFS $MFT/$UsnJrnl/VSS/Prefetch/LNK/JumpLists, Event Logs, SRUM) and open-source GitHub DFIR tools (Velociraptor, Hayabusa, Chainsaw, Zimmerman Tools, Volatility 3, MemProcFS, WinPmem, HollowsHunter, Capa, FLOSS, YARA-X)."
when_to_apply: "Apply whenever performing Windows digital forensics, incident response (DFIR), live triage, memory dump analysis, Registry hive examination, NTFS $MFT/$UsnJrnl/Prefetch/VSS timeline reconstruction, .evtx event log correlation, or running open-source Windows forensic tools (Velociraptor, Hayabusa, Chainsaw, Zimmerman Tools, Volatility 3, MemProcFS, HollowsHunter)."
tags: [reasoning, windows_forensics, windows-forensics, dfir, forensics, windows, mft, usnjrnl, prefetch, amcache, shimcache, bam, shellbags, srum, evtx, wevtutil, velociraptor, hayabusa, chainsaw, zimmerman, volatility3, memprocfs, winpmem, hollowshunter, yara-x, capa, floss]
updated: 2026-10-31 00:18:00
---
# Windows Digital Forensics (DFIR) Strategy & Techniques Playbook (`windows_digital_forensics_strategy_playbook`)

> **Team Role:** `WINDOWS_FORENSICS` (Windows Host Forensics, Artifact Timeline Reconstruction & Memory Analysis)  
> **Target OS:** `Windows (Windows 10 / 11 / Windows Server 2016–2025)`  
> **Primary H-MDP Tactics:** `Passive_Enum` (Order-of-Volatility Acquisition) $\to$ `Enumeration` (Registry, NTFS & `.evtx` Parsing) $\to$ `Post_Exploitation_Verification` (Timeline & IOC Attribution)  
> **Recommended Console Posture:** `WHITE` (Air-Gapped Offline Forensic Analysis) or `BLUE` (Isolated Acquisition NIC) | **Modes:** `Analyst` (Strict Read-Only Forensic Guardrail)  
> **Companion Command Playbook:** [[commands/windows_digital_forensics_playbook]]  
> **Backlinks:** [[00_MEMORY_INDEX]] | [[knowledge/10_digital_forensics_pe_reversing_and_threat_intel]] | [[knowledge/01_windows_system_process_and_sysinternals]] | [[knowledge/02_windows_registry_boot_and_persistence]] | [[knowledge/03_windows_security_acls_auditing_and_logs]] | [[reasoning/hunt_team_strategy_playbook]]

---

## 1. When Engines & LLM Must Activate This Playbook
Activate `[[reasoning/windows_digital_forensics_strategy_playbook]]` and `[[commands/windows_digital_forensics_playbook]]` whenever the query, goal, or attached evidence in `Projects/<project>/Files/` involves:
- **Live Windows Forensic Triage (Order of Volatility — RFC 3227):** Capturing volatile RAM, process trees, injected DLLs, open handles, network connections, DNS cache, SMB sessions, or BITS jobs using native Windows commands.
- **Windows Execution & Persistence Artifact Reconstruction:** Analyzing **Prefetch** (`*.pf`), **Amcache** (`Amcache.hve`), **ShimCache / AppCompatCache**, **BAM/DAM** (Background Activity Moderator), **UserAssist**, **ShellBags**, **LNK** shortcuts, **JumpLists**, or **SRUM** (`SRUDB.dat`).
- **NTFS File System & Timeline Forensics:** Parsing `$MFT` (Master File Table), `$UsnJrnl:$J` (Update Sequence Number Change Journal), `$LogFile`, Volume Shadow Copies (`vssadmin`), Alternate Data Streams (`ADS`), `$Recycle.Bin` (`$I`/`$R`), or detecting `$STANDARD_INFORMATION` vs `$FILE_NAME` timestomping.
- **Open-Source GitHub DFIR Tooling on Windows:** Setting up or executing **Velociraptor**, **Hayabusa**, **Chainsaw**, **Eric Zimmerman's Tools** (`MFTECmd`, `PECmd`, `AmcacheParser`, `AppCompatCacheParser`, `RECmd`, `LECmd`, `JLECmd`, `SBECmd`, `EvtxECmd`, `SrumECmd`), **Volatility 3**, **MemProcFS**, **WinPmem**, **HollowsHunter** / **PE-sieve**, **Capa**, **FLOSS**, or **YARA-X**.

---

## 2. 15-Engine Neuro-Symbolic Alignment for Windows Forensics
| Engine Layer | Engine Name | Windows Forensic Role & Decision Rule |
| :--- | :--- | :--- |
| **Layer 0** | **Engine 1 (`associative`) & Engine 9 (`temporal_fluents`)** | Activate `[[reasoning/windows_digital_forensics_strategy_playbook]]` and `[[commands/windows_digital_forensics_playbook]]`; anchor Event-Calculus fluents to UTC timestamps across `$MFT`, Registry `LastWriteTime`, Prefetch run times, and `.evtx` `TimeCreated`. |
| **Layer 1** | **Engine 12 (`cegar_verifier`) & Engine 20 (`spectral_manifold_pca`)** | Enforce RFC 3227 Order of Volatility (memory & network state before disk reads) and prevent evidence modification in `Analyst` mode; flag anomalous process/network states via Mahalanobis distance ($D_M > 3.0$). |
| **Layer 2** | **Engine 4 (`bayesian`) & Engine 10 (`dempster_shafer`)** | Cross-correlate independent Windows evidence sources (e.g., Prefetch vs. Amcache vs. Event ID `4688` vs. `$UsnJrnl`); high Dempster-Shafer conflict ($K > 0.35$) indicates log clearing (`Event ID 1102`/`104`), timestomping, or anti-forensic wiping. |
| **Layer 3/4** | **Engine 13 (`sygus_extractor`) & Engine 15 (`mdp_tactical`)** | Parse structured PIDs, SHA-256 hashes, SIDs, and timestamps from CLI outputs; prioritize non-destructive `Passive_Enum` and `Enumeration` actions. |

---

## 3. PART I: Full Forensic Breakdown of Native Windows Commands (Zero-Dependency)

### 3.1 Order of Volatility Step 1: System Time, Volatile Network, DNS, SMB & BITS State
| Forensic Artifact | Native Windows Command (`CMD` / `PowerShell`) | What It Proves & Forensic Significance |
| :--- | :--- | :--- |
| **UTC Time, Boot Time & OS Baseline** | `powershell -NoProfile -Command "[pscustomobject]@{UTC=(Get-Date).ToUniversalTime().ToString('o'); Local=(Get-Date).ToString('o'); TZ=(Get-TimeZone).Id; LastBoot=(Get-CimInstance Win32_OperatingSystem).LastBootUpTime}"` | Establishes exact skew between host clock and UTC before correlating `.evtx`, `$MFT`, and Registry timestamps. |
| **Active TCP/UDP Sockets & Owning Process Lineage** | `powershell -NoProfile -Command "Get-NetTCPConnection \| Select-Object LocalAddress,LocalPort,RemoteAddress,RemotePort,State,OwningProcess,CreationTime,@{N='Name';E={(Get-Process -Id $_.OwningProcess -EA 0).ProcessName}},@{N='Path';E={(Get-Process -Id $_.OwningProcess -EA 0).Path}} \| Format-Table -AutoSize"` | Captures volatile `CreationTime` of every TCP connection and maps it directly to the executable path on disk. |
| **Volatile DNS Resolver Cache** | `powershell -NoProfile -Command "Get-DnsClientCache \| Select-Object Entry,RecordName,RecordType,Status,Data,TimeToLive"` *(or `ipconfig /displaydns`)* | Reveals recently resolved C2 domains even after the network connection has closed. |
| **Active SMB Sessions, Shares & Open Files** | `powershell -NoProfile -Command "Get-SmbSession; Get-SmbOpenFile; Get-SmbShare"` *(or `net session` & `net file`)* | Identifies active lateral movement (`PsExec`, `SMBExec`, admin share `C$`/`ADMIN$` staging) and source IP/username. |
| **BITS Transfer Persistence Jobs** | `bitsadmin /list /allusers /verbose` *(or `powershell -NoProfile -Command "Get-BitsTransfer -AllUsers \| Select-Object JobId,DisplayName,OwnerAccount,JobState,FileList"`)* | Detects stealthy Living-off-the-Land background downloads or notify-command persistence via Background Intelligent Transfer Service. |

### 3.2 Order of Volatility Step 2: Process Tree, Command Lines, Modules, Handles & Memory
| Forensic Artifact | Native Windows Command (`CMD` / `PowerShell` / `Sysinternals`) | What It Proves & Forensic Significance |
| :--- | :--- | :--- |
| **Full Process Tree, PPID, Hash & Command Line** | `powershell -NoProfile -Command "Get-CimInstance Win32_Process \| Select-Object ProcessId,ParentProcessId,Name,CreationDate,SessionId,ExecutablePath,CommandLine \| Export-Csv -NoTypeInformation C:\Temp\forensic_processes.csv"` | Captures full parent-child lineage, exact creation timestamp, and command-line arguments (which are lost on reboot). |
| **Unsigned Loaded DLLs & Module Paths** | `listdlls64.exe -u -v -nobanner` *(or `tasklist /m`)* | Detects DLL search-order hijacking, side-loading, and unbacked/unsigned modules loaded into legitimate processes. |
| **Open File, Mutant (Mutex) & Section Handles** | `handle64.exe -a -u -nobanner` | Reveals malware installation mutexes (`Mutant`), named pipes (`\Device\NamedPipe\`), and locked log/staging files. |
| **Full Process Memory Dump for Offline Analysis** | `procdump64.exe -ma <PID> C:\Temp\proc_<PID>.dmp /accepteula` *(or native `rundll32.exe C:\Windows\System32\comsvcs.dll, MiniDump <PID> C:\Temp\proc.dmp full`)* | Preserves unpacked process memory, heap strings, decrypted configs, and injected shellcode. |

### 3.3 Order of Volatility Step 3: Windows Registry Forensics & Execution Artifacts
| Forensic Artifact | Native Windows Command (`CMD` / `PowerShell`) | What It Proves & Forensic Significance |
| :--- | :--- | :--- |
| **Acquire Offline Registry Hives Safely (Locked Files)** | `reg save HKLM\SAM C:\Temp\SAM.hiv /y & reg save HKLM\SYSTEM C:\Temp\SYSTEM.hiv /y & reg save HKLM\SECURITY C:\Temp\SECURITY.hiv /y & reg save HKLM\SOFTWARE C:\Temp\SOFTWARE.hiv /y` | Exports live locked registry hives (`SAM`, `SYSTEM`, `SECURITY`, `SOFTWARE`) with full cell/slack metadata for offline examination. |
| **BAM / DAM (Background Activity Moderator)** | `reg query "HKLM\SYSTEM\CurrentControlSet\Services\bam\State\UserSettings" /s` | **Evidence of Execution:** Records full binary path and exact 64-bit Windows `FILETIME` (UTC) of last execution per User SID. |
| **AppCompatCache (ShimCache) & Amcache** | `reg query "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\AppCompatCache" /v AppCompatCache` & `reg save "HKLM\ROOT\InventoryApplicationFile" C:\Temp\Amcache_export.hiv /y` *(or copy `C:\Windows\AppCompat\Programs\Amcache.hve` via VSS)* | Tracks executables inspected/run by Windows Application Compatibility; `Amcache.hve` stores SHA-1 hashes, file sizes, and compile timestamps even after the binary is deleted. |
| **UserAssist (GUI Program Execution & Run Count)** | `powershell -NoProfile -Command "Get-ItemProperty 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Explorer\UserAssist\*\Count' \| ForEach-Object { $_.PSObject.Properties \| Where-Object { $_.Name -notmatch '^PS' } \| ForEach-Object { $n = ($_.Name.ToCharArray() \| ForEach-Object { if($_ -ge 'a' -and $_ -le 'z'){[char](([int]$_-97+13)%26+97)} elseif($_ -ge 'A' -and $_ -le 'Z'){[char](([int]$_-65+13)%26+65)} else {$_} }) -join ''; [pscustomobject]@{DecodedPath=$n} } }"` | Decodes ROT13-encoded `UserAssist` entries proving a user interactively launched a program via Explorer/LNK. |
| **ShellBags (`BagMRU` / `Bags`) & RecentDocs** | `reg query "HKCU\Software\Classes\Local Settings\Software\Microsoft\Windows\Shell\BagMRU" /s & reg query "HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\RecentDocs" /s` | Proves a user browsed a local, removable USB, or network UNC directory even after the folder or USB drive was removed. |
| **USB Storage History (`USBSTOR` & `MountedDevices`)** | `reg query "HKLM\SYSTEM\CurrentControlSet\Enum\USBSTOR" /s & reg query "HKLM\SYSTEM\MountedDevices"` | Identifies vendor, product, hardware serial number, and drive letter/GUID of every USB storage device connected to the host. |
| **Network Profile & First/Last Connected Timestamps** | `reg query "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\NetworkList\Profiles" /s & reg query "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\NetworkList\Signatures\Unmanaged" /s` | Records SSIDs, default gateway MAC addresses (`DefaultGatewayMac`), DNS suffixes, and `DateCreated` / `DateLastConnected`. |

### 3.4 Order of Volatility Step 4: NTFS Internals (`$MFT`, `$UsnJrnl`, VSS, Prefetch, Recycle Bin & ADS)
| Forensic Artifact | Native Windows Command (`CMD` / `PowerShell`) | What It Proves & Forensic Significance |
| :--- | :--- | :--- |
| **NTFS USN Change Journal (`$UsnJrnl:$J`)** | `fsutil usn readjournal C: csv \| findstr /i ".exe .dll .ps1 .bat .zip .7z .rar"` | Queries the live NTFS Update Sequence Number journal for recent file creations, deletions (`0x80000200`), and renames. |
| **Volume Shadow Copies (`VSS`) Inspection & Mount** | `vssadmin list shadows` $\to$ `cmd /c mklink /d C:\VSS_Shadow1 \\?\GLOBALROOT\Device\HarddiskVolumeShadowCopy1\` | Exposes historical Volume Shadow Copy snapshots to recover deleted malware, wiped `.evtx` logs, or locked `$MFT` / `NTUSER.DAT` / `SRUDB.dat` files. |
| **Windows Prefetch (`C:\Windows\Prefetch\*.pf`)** | `powershell -NoProfile -Command "Get-ChildItem C:\Windows\Prefetch\*.pf \| Sort-Object LastWriteTime -Descending \| Select-Object Name,Length,CreationTimeUtc,LastWriteTimeUtc -First 40"` | **Evidence of Execution:** Proves binary execution (`CreationTimeUtc` = first run, `LastWriteTimeUtc` = last run, plus up to 8 historical run timestamps and loaded files/directories inside the `.pf` body). |
| **Recycle Bin (`$Recycle.Bin` `$I` Metadata & `$R` Data)** | `powershell -NoProfile -Command "Get-ChildItem 'C:\$Recycle.Bin' -Recurse -Force -EA 0 \| Select-Object FullName,Length,CreationTimeUtc,LastWriteTimeUtc"` | `$Ixxxxxx` files contain the original full file path, original file size, and deletion timestamp in UTC; `$Rxxxxxx` holds the deleted file contents. |
| **LNK Shortcuts & JumpLists (`Recent`)** | `powershell -NoProfile -Command "Get-ChildItem \"$env:APPDATA\Microsoft\Windows\Recent\" -Recurse -Force \| Select-Object FullName,CreationTimeUtc,LastWriteTimeUtc"` | `.lnk` and `.automaticDestinations-ms` / `.customDestinations-ms` files record volume serial numbers, NetBIOS hostname, MAC address, and target MACB timestamps of opened files. |
| **Timestomp Detection (`$SI` < CreationTime)** | `powershell -NoProfile -Command "Get-ChildItem C:\Windows\System32,C:\ProgramData -File -Recurse -EA 0 \| Where-Object { $_.LastWriteTimeUtc -lt $_.CreationTimeUtc } \| Select-Object FullName,CreationTimeUtc,LastWriteTimeUtc"` | Identifies files whose `$STANDARD_INFORMATION` modification timestamp was backdated (`timestomped`) earlier than their creation timestamp. |

### 3.5 Order of Volatility Step 5: Windows Event Logs (`.evtx`) & SRUM Forensics
| Forensic Artifact | Native Windows Command (`CMD` / `PowerShell`) | High-Signal Event IDs & Forensic Meaning |
| :--- | :--- | :--- |
| **Authentication, Logon Types & Lateral Movement** | `wevtutil qe Security "/q:*[System[(EventID=4624 or EventID=4625 or EventID=4648 or EventID=4672 or EventID=4776)]]" /c:50 /rd:true /f:text` | `4624` (Logon Type `2`=Interactive, `3`=Network/SMB, `7`=Unlock, `9`=NewCredentials/RunAs, `10`=RDP), `4625` (Failed logon), `4648` (Explicit credentials), `4672` (Admin privileges assigned). |
| **Process Creation (`4688`), Services (`7045`/`4697`) & Tasks (`4698`)** | `wevtutil qe Security "/q:*[System[(EventID=4688 or EventID=4697 or EventID=4698 or EventID=4720 or EventID=1102)]]" /c:50 /rd:true /f:text & wevtutil qe System "/q:*[System[(EventID=7045 or EventID=104)]]" /c:30 /rd:true /f:text` | `4688` (Process creation + CLI), `7045`/`4697` (New service installed), `4698` (Scheduled task created), `4720` (User created), `1102`/`104` (Security/System Event Log cleared). |
| **PowerShell ScriptBlock (`4104`) & RDP Sessions (`21`–`25`)** | `wevtutil qe "Microsoft-Windows-PowerShell/Operational" "/q:*[System[(EventID=4104)]]" /c:30 /rd:true /f:text & wevtutil qe "Microsoft-Windows-TerminalServices-LocalSessionManager/Operational" "/q:*[System[(EventID=21 or EventID=24 or EventID=25)]]" /c:30 /rd:true /f:text` | `4104` captures deobfuscated PowerShell script blocks; `21`/`24`/`25` record RDP session logon, disconnect, and reconnection with source IP. |
| **Query Offline `.evtx` Evidence File** | `powershell -NoProfile -Command "Get-WinEvent -Path 'C:\Evidence\Security.evtx' -MaxEvents 50 \| Select-Object TimeCreated,Id,LevelDisplayName,Message"` | Parses acquired `.evtx` files from another host without importing them into the local Event Viewer. |
| **SRUM (`SRUDB.dat` Network & Execution History)** | `esentutl /y C:\Windows\System32\sru\SRUDB.dat /d C:\Temp\SRUDB_copy.dat /vss` | Copies the locked ESE database `SRUDB.dat` via VSS; records 30–60 days of per-process network bytes sent/received, User SID, and CPU runtime even if `.evtx` logs were cleared! |

---

## 4. PART II: Latest Open-Source & GitHub Windows Forensics Tools

### 4.1 Open-Source Windows DFIR GitHub Repository Directory & Setup
| Tool Name | Official GitHub URL | Core Forensic Capability | Quick Installation / Setup Command |
| :--- | :--- | :--- | :--- |
| **Velociraptor** | `https://github.com/Velocidex/velociraptor` | VQL live endpoint query engine, NTFS `$MFT`/`$UsnJrnl` parser, and offline KAPE-target triage collector. | Download `velociraptor-v*-windows-amd64.exe` from `https://github.com/Velocidex/velociraptor/releases`. |
| **Hayabusa** | `https://github.com/Yamato-Security/hayabusa` | Ultra-fast Rust Windows `.evtx` threat hunter and Sigma CSV/JSON timeline generator. | Download `hayabusa-*-win-x64.zip` from `https://github.com/Yamato-Security/hayabusa/releases` $\to$ `hayabusa.exe update-rules`. |
| **Chainsaw** | `https://github.com/WithSecureLabs/chainsaw` | Rust rapid forensic search & Sigma hunting across `.evtx`, `$MFT`, Registry hives, and ShimCache. | Download `chainsaw_x86_64-pc-windows-msvc.zip` from `https://github.com/WithSecureLabs/chainsaw/releases`. |
| **Eric Zimmerman Tools** | `https://github.com/EricZimmerman` | Gold-standard CLI parsers: `MFTECmd`, `PECmd`, `AmcacheParser`, `AppCompatCacheParser`, `RECmd`, `LECmd`, `JLECmd`, `SBECmd`, `RBCmd`, `EvtxECmd`, `SrumECmd`. | `powershell -NoProfile -Command "Invoke-WebRequest https://f001.backblazeb2.com/file/EricZimmermanTools/Get-ZimmermanTools.ps1 -OutFile Get-ZimmermanTools.ps1; .\Get-ZimmermanTools.ps1 -Dest C:\Tools\EZTools"` |
| **Volatility 3** | `https://github.com/volatilityfoundation/volatility3` | Next-generation Python memory forensics framework for Windows `.dmp` / `.raw` / `.vmem` RAM images. | `python -m pip install --upgrade volatility3` *(or `git clone https://github.com/volatilityfoundation/volatility3.git`)* |
| **MemProcFS** | `https://github.com/ufrisk/MemProcFS` | Mounts physical Windows RAM dumps as a virtual filesystem (`M:\`) with automated forensic CSV timelines (`-forensic 1`). | Download `MemProcFS_files_and_binaries-v*-win_x64.zip` from `https://github.com/ufrisk/MemProcFS/releases`. |
| **WinPmem** | `https://github.com/Velocidex/WinPmem` | Physical RAM acquisition driver & CLI dumper for live 64-bit Windows hosts. | Download `winpmem_mini_x64_rc2.exe` from `https://github.com/Velocidex/WinPmem/releases`. |
| **HollowsHunter & PE-sieve** | `https://github.com/hasherezade/hollows_hunter` / `https://github.com/hasherezade/pe-sieve` | Scans live Windows processes for process hollowing, reflective DLLs, inline hooks, and unbacked shellcode, dumping unpacked PEs. | Download `hollows_hunter64.exe` and `pe-sieve64.exe` from GitHub Releases. |
| **Capa & FLOSS** | `https://github.com/mandiant/capa` / `https://github.com/mandiant/flare-floss` | Mandiant FLARE binary capability mapper (ATT&CK/MBC) and stack/encrypted string deobfuscator. | Download `capa-v*-windows.zip` & `floss-v*-windows.zip` from GitHub Releases. |
| **YARA-X** | `https://github.com/VirusTotal/yara-x` | VirusTotal's next-generation Rust YARA engine for scanning memory dumps and disk artifacts. | Download `yara-x-v*-x86_64-pc-windows-msvc.zip` from `https://github.com/VirusTotal/yara-x/releases`. |

### 4.2 High-Efficiency Execution Commands for Open-Source Windows Forensic Tools
| Tool | Verified Forensic Command Syntax | Expected Output & When to Apply |
| :--- | :--- | :--- |
| **Velociraptor (VQL Live Query)** | `velociraptor.exe query "SELECT Pid, Ppid, Name, Exe, CommandLine, Hash.SHA256 FROM pslist() WHERE Authenticode.Trusted != 'trusted'" --format json` | Immediately enumerates all running Windows processes whose binary lacks a trusted Authenticode signature. |
| **Velociraptor (NTFS `$MFT` Hunt)** | `velociraptor.exe query "SELECT EntryNumber, FullPath, FileSize, Created0x10, Created0x30, LastModified0x10, LastModified0x30 FROM Artifact.Windows.NTFS.MFT(MFTDrive='C:') WHERE Created0x10 < Created0x30"` | Hunts `$MFT` records directly on `C:` where `$STANDARD_INFORMATION` (`0x10`) timestamp predates `$FILE_NAME` (`0x30`) — definitive proof of **timestomping**. |
| **Hayabusa (`.evtx` Sigma Timeline)** | `hayabusa.exe csv-timeline -d "C:\Windows\System32\winevt\Logs" -o C:\Temp\hayabusa_timeline.csv --no-wizard -p timesketch-verbose` | Scans all local or offline `.evtx` logs against thousands of Sigma rules and generates a unified CSV incident timeline in seconds. |
| **Chainsaw (`.evtx` & ShimCache Hunt)** | `chainsaw.exe hunt "C:\Windows\System32\winevt\Logs" -s sigma/ --mapping mappings/sigma-event-logs-all.yml --csv --output C:\Temp\chainsaw_out` | Performs multi-threaded Sigma rule & keyword hunting across `.evtx` files and outputs structured CSV detections. |
| **Zimmerman `MFTECmd` (`$MFT` & `$J`)** | `MFTECmd.exe -f "C:\Temp\$MFT" --csv C:\Temp\out --csvf mft_parsed.csv` & `MFTECmd.exe -f "C:\Temp\$J" -m "C:\Temp\$MFT" --csv C:\Temp\out --csvf usnjrnl_parsed.csv` | Parses raw NTFS `$MFT` and `$UsnJrnl:$J` into full-path CSV timelines resolving parent MFT reference numbers. |
| **Zimmerman `PECmd`, `AmcacheParser` & `AppCompatCacheParser`** | `PECmd.exe -d "C:\Windows\Prefetch" --csv C:\Temp\out -q` & `AmcacheParser.exe -f "C:\Windows\AppCompat\Programs\Amcache.hve" --csv C:\Temp\out -i` & `AppCompatCacheParser.exe -f C:\Temp\SYSTEM.hiv --csv C:\Temp\out` | Reconstructs complete historical binary execution timelines across Prefetch, Amcache (with SHA-1 hashes), and ShimCache. |
| **Zimmerman `RECmd`, `LECmd`, `JLECmd` & `SrumECmd`** | `RECmd.exe -d C:\Temp\Hives --bn BatchExamples\Kroll_Batch.reb --csv C:\Temp\out` & `SrumECmd.exe -f C:\Temp\SRUDB_copy.dat -r C:\Temp\SOFTWARE.hiv --csv C:\Temp\out` | Extracts hundreds of forensic Registry artifacts automatically via `Kroll_Batch.reb` and correlates `SRUDB.dat` network/process usage with `SOFTWARE` hive profiles. |
| **Volatility 3 (Windows RAM Analysis)** | `vol -f C:\Temp\physmem.raw windows.pstree` && `vol -f C:\Temp\physmem.raw windows.malfind` && `vol -f C:\Temp\physmem.raw windows.netscan` && `vol -f C:\Temp\physmem.raw windows.cmdline` | Analyzes a Windows physical RAM image to uncover hidden/unlinked processes, `PAGE_EXECUTE_READWRITE` injected memory (`malfind`), and closed/active sockets (`netscan`). |
| **MemProcFS (Mount RAM + Auto-Forensics)** | `memprocfs.exe -device C:\Temp\physmem.raw -forensic 1` | Mounts the RAM image as `M:\` and generates `M:\forensic\csv\` timelines (`timeline_all.csv`, `process.csv`, `net.csv`, `ntfs.csv`, `reg.csv`). |
| **HollowsHunter (Live Process Injection Scan)** | `hollows_hunter64.exe /hooks /shellc /dir C:\Temp\hollows_dumps` | Scans all running processes in RAM for hollowed PEs, inline API hooks, and unbacked shellcode threads, automatically dumping unpacked modules to disk. |
