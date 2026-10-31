---
title: windows_digital_forensics_playbook
category: commands
os_platform: windows
domain_hub: "[[knowledge/10_digital_forensics_pe_reversing_and_threat_intel]]"
primary_tactic: Passive_Enum
summary: "Master Windows Digital Forensics (DFIR) command reference covering native Windows forensic acquisition (PowerShell, CMD, Registry, NTFS $MFT/$UsnJrnl/VSS/Prefetch, .evtx, SRUM) and open-source GitHub tools (Velociraptor, Hayabusa, Chainsaw, Zimmerman Tools, Volatility 3, MemProcFS, WinPmem, HollowsHunter)."
when_to_apply: "Apply when executing Windows live forensic triage, dumping process/physical memory, exporting Registry hives, parsing $MFT/$UsnJrnl/Prefetch/Amcache/ShimCache/BAM/SRUM, or running Velociraptor, Hayabusa, Chainsaw, Zimmerman Tools, Volatility 3, MemProcFS, or HollowsHunter."
tags: [commands, windows_forensics, windows-forensics, dfir, forensics, windows, mft, usnjrnl, prefetch, amcache, shimcache, bam, srum, wevtutil, velociraptor, hayabusa, chainsaw, zimmerman, volatility3, memprocfs, hollowshunter]
updated: 2026-10-31 00:19:00
---
# Windows Digital Forensics (DFIR) Master Command Playbook (`windows_digital_forensics_playbook`)

> **Strategy Playbook:** [[reasoning/windows_digital_forensics_strategy_playbook]]  
> **Domain Knowledge Hub:** [[knowledge/10_digital_forensics_pe_reversing_and_threat_intel]]  
> **Backlinks:** [[00_MEMORY_INDEX]] | [[commands/windows_master_command_playbook]] | [[knowledge/01_windows_system_process_and_sysinternals]] | [[knowledge/02_windows_registry_boot_and_persistence]] | [[knowledge/03_windows_security_acls_auditing_and_logs]]

---

## 1. Native Windows Forensic Acquisition Commands (By Order of Volatility)
| Forensic Phase | Verified Native Windows Command (`CMD` / `PowerShell` / `Sysinternals`) | Key Flags & Forensic Output |
| :--- | :--- | :--- |
| **1. Volatile Process & Command-Line Snapshot** | `powershell -NoProfile -Command "Get-CimInstance Win32_Process \| Select-Object ProcessId,ParentProcessId,Name,CreationDate,SessionId,ExecutablePath,CommandLine \| Export-Csv -NoTypeInformation C:\Temp\processes.csv"` | Captures full PPID tree, UTC creation timestamp, and command line before process termination. |
| **2. Volatile Sockets, DNS Cache & SMB Sessions** | `powershell -NoProfile -Command "Get-NetTCPConnection \| Select-Object LocalAddress,LocalPort,RemoteAddress,RemotePort,State,OwningProcess,CreationTime; Get-DnsClientCache; Get-SmbSession; Get-SmbOpenFile"` | Captures active/listening sockets with `CreationTime`, cached DNS lookups, and lateral SMB sessions. |
| **3. Process Memory, Unsigned DLLs & Handles** | `procdump64.exe -ma <PID> C:\Temp\proc_<PID>.dmp /accepteula & listdlls64.exe -u -nobanner & handle64.exe -a -u -nobanner` | `-ma`: Full memory dump; `-u`: Unsigned DLLs only; `-a -u`: All handles with owning user. |
| **4. Safe Registry Hive Acquisition (`Locked`)** | `reg save HKLM\SAM C:\Temp\SAM.hiv /y & reg save HKLM\SYSTEM C:\Temp\SYSTEM.hiv /y & reg save HKLM\SECURITY C:\Temp\SECURITY.hiv /y & reg save HKLM\SOFTWARE C:\Temp\SOFTWARE.hiv /y` | Exports locked Registry hives cleanly with unallocated cell slack intact. |
| **5. BAM, ShimCache, USBSTOR & NetworkList** | `reg query "HKLM\SYSTEM\CurrentControlSet\Services\bam\State\UserSettings" /s & reg query "HKLM\SYSTEM\CurrentControlSet\Enum\USBSTOR" /s & reg query "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\NetworkList\Profiles" /s` | Queries binary execution timestamps (`BAM`), USB hardware serials (`USBSTOR`), and connected networks. |
| **6. NTFS `$UsnJrnl:$J`, VSS & Prefetch Triage** | `fsutil usn readjournal C: csv \| findstr /i ".exe .dll .ps1" & vssadmin list shadows & dir /o:-d C:\Windows\Prefetch\*.pf` | Reads NTFS change journal records, lists Volume Shadow Copies, and orders Prefetch `.pf` files by last execution. |
| **7. High-Signal `.evtx` & SRUM Acquisition** | `wevtutil epl Security C:\Temp\Security_backup.evtx & wevtutil epl System C:\Temp\System_backup.evtx & esentutl /y C:\Windows\System32\sru\SRUDB.dat /d C:\Temp\SRUDB.dat /vss` | Exports `.evtx` logs (`wevtutil epl`) and copies locked `SRUDB.dat` via VSS (`esentutl /y /vss`). |

---

## 2. Open-Source GitHub Windows Forensics Tool Commands
| Open-Source Tool (`GitHub`) | Verified CLI Command | Flag Breakdown & When to Apply |
| :--- | :--- | :--- |
| **WinPmem** (`Velocidex/WinPmem`) | `winpmem_mini_x64_rc2.exe C:\Temp\physmem.raw` | Acquires a complete physical RAM dump (`physmem.raw`) from a live 64-bit Windows host. |
| **Volatility 3** (`volatilityfoundation/volatility3`) | `vol -f C:\Temp\physmem.raw windows.pstree` && `vol -f C:\Temp\physmem.raw windows.malfind` && `vol -f C:\Temp\physmem.raw windows.netscan` | `-f`: RAM image path; `windows.pstree`: process lineage; `windows.malfind`: injected RWX memory; `windows.netscan`: TCP/UDP endpoints. |
| **MemProcFS** (`ufrisk/MemProcFS`) | `memprocfs.exe -device C:\Temp\physmem.raw -forensic 1` | `-device`: RAM image; `-forensic 1`: runs full automated memory forensics and writes CSV timelines to `M:\forensic\csv\`. |
| **HollowsHunter** (`hasherezade/hollows_hunter`) | `hollows_hunter64.exe /hooks /shellc /dir C:\Temp\hollows_dumps` | `/hooks`: detect inline patches; `/shellc`: scan for unbacked shellcode threads; `/dir`: output directory for unpacked PEs. |
| **Velociraptor** (`Velocidex/velociraptor`) | `velociraptor.exe query "SELECT Pid, Ppid, Name, Exe, CommandLine FROM pslist()" --format json` | Executes live VQL forensic queries without requiring a server deployment. |
| **Hayabusa** (`Yamato-Security/hayabusa`) | `hayabusa.exe csv-timeline -d "C:\Windows\System32\winevt\Logs" -o C:\Temp\hayabusa.csv --no-wizard` | `-d`: `.evtx` directory; `-o`: output CSV timeline; `--no-wizard`: non-interactive batch mode for CORA CLI/WebGUI execution. |
| **Chainsaw** (`WithSecureLabs/chainsaw`) | `chainsaw.exe hunt "C:\Windows\System32\winevt\Logs" -s sigma/ --mapping mappings/sigma-event-logs-all.yml --csv --output C:\Temp\chainsaw` | `-s`: Sigma rules path; `--mapping`: field mapping YAML; `--csv`: structured CSV output. |
| **Zimmerman `MFTECmd`** (`EricZimmerman/MFTECmd`) | `MFTECmd.exe -f "C:\Temp\$MFT" --csv C:\Temp\out --csvf mft.csv` | `-f`: input `$MFT`, `$J`, `$LogFile`, or `$Boot`; `--csv`: output directory; `--csvf`: filename. |
| **Zimmerman `PECmd` & `AmcacheParser`** (`EricZimmerman`) | `PECmd.exe -d "C:\Windows\Prefetch" --csv C:\Temp\out -q` & `AmcacheParser.exe -f "C:\Windows\AppCompat\Programs\Amcache.hve" --csv C:\Temp\out -i` | Parses all Prefetch `.pf` files (`PECmd -d`) and `Amcache.hve` (`AmcacheParser -f`) into forensic CSV timelines. |
| **Zimmerman `RECmd` & `SrumECmd`** (`EricZimmerman`) | `RECmd.exe -d C:\Temp\Hives --bn BatchExamples\Kroll_Batch.reb --csv C:\Temp\out` & `SrumECmd.exe -f C:\Temp\SRUDB.dat -r C:\Temp\SOFTWARE.hiv --csv C:\Temp\out` | Batch-extracts Registry persistence/execution keys (`RECmd`) and 30-day per-app network/CPU metrics (`SrumECmd`). |
| **Capa & FLOSS** (`mandiant/capa`, `mandiant/flare-floss`) | `capa.exe -v C:\Temp\suspect.exe` & `floss.exe -n 6 C:\Temp\suspect.exe` | Maps binary capabilities to MITRE ATT&CK (`capa`) and decodes stack/tight/obfuscated strings (`floss`). |
