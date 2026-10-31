---
title: hunt_team_strategy_playbook
category: reasoning
engine: team_strategy_arbiter
team_role: hunt_team
os_platform: cross-platform
domain_hub: "[[knowledge/10_digital_forensics_pe_reversing_and_threat_intel]]"
primary_tactic: Passive_Enum
summary: "Hunt Team Hypothesis-Driven Threat Hunting & Forensics Playbook: assumed-breach anomaly detection, process/memory hollowing & /proc forensics, stealth persistence & LOLBin hunting, NTFS ADS/timestomp discovery, event log correlation, and BPF/PCAP C2 beacon analysis across Windows and Linux."
when_to_apply: "Apply when the operator or goal requires proactive threat hunting, assumed-breach investigation, Indicator of Compromise (IoC) or Indicator of Attack (IoA) sweeping, stealth persistence discovery, memory/process forensics, event log timeline correlation, or passive PCAP/BPF network anomaly analysis on Windows or Linux."
tags: [reasoning, hunt_team, hunt-team, threat-hunting, dfir, forensics, anomaly-detection, persistence, lolbin, autoruns, sysinternals, procfs, wevtutil, journalctl, tcpdump, tshark, bpf, p0f, windows, linux]
updated: 2026-10-30 23:44:00
---
# Hunt Team Strategy & Proactive Threat Hunting Playbook (`hunt_team_strategy_playbook`)

> **Team Role:** `HUNT_TEAM` (Hypothesis-Driven Threat Hunting, Anomaly Detection & Live Forensics)  
> **Primary H-MDP Tactics:** `Passive_Enum` $\to$ `Enumeration` $\to$ `Post_Exploitation_Verification`  
> **Recommended Console Posture:** `WHITE` (Air-Gapped Forensic Analysis) or `BLUE` (Sensor Interface) | **Modes:** `Analyst` (Read-Only Guardrail) / `Ninja` (Zero-Noise Inspection)  
> **Backlinks:** [[00_MEMORY_INDEX]] | [[commands/windows_master_command_playbook]] | [[commands/linux_master_command_playbook]] | [[knowledge/10_digital_forensics_pe_reversing_and_threat_intel]] | [[knowledge/07_packet_capture_bpf_wireshark_and_passive_fingerprinting]] | [[knowledge/01_windows_system_process_and_sysinternals]] | [[knowledge/06_linux_unix_administration_processes_and_logging]]

---

## 1. When Engines & LLM Must Activate This Playbook
Activate `[[reasoning/hunt_team_strategy_playbook]]` whenever the query, goal, or system state involves:
- **Assumed-Breach Hypothesis Testing:** Proactively searching for stealthy adversary tradecraft (LOLBins, process injection/hollowing, fileless WMI/Registry persistence, rootkits, or covert C2 channels) that evaded static signature alerts.
- **Process, Memory & `/proc` Forensics:** Hunting unbacked `rwxp` memory regions, deleted binaries still running in RAM (`/proc/*/exe -> (deleted)`), unsigned DLLs (`listdlls64.exe -u`), or anomalous parent-child process trees (`w3wp.exe` / `nginx` spawning `cmd.exe` / `powershell.exe` / `bash`).
- **Persistence & File System Artifact Hunting:** Auditing ASEPs (`autorunsc64.exe`), WMI `root\subscription` consumers, NTFS Alternate Data Streams (`dir /R`, `-Stream *`), `ShimCache`/`Amcache`/`BAM`, Linux `ld.so.preload`, systemd generators, or timestomped files.
- **Log Timeline & PCAP/BPF Traffic Hunting:** Correlating Windows Security/PowerShell Event IDs (`4624`, `4625`, `4672`, `4688`, `4697`, `4698`, `4104`, `1102`) or Linux `auditd`/`journalctl` logs alongside BPF packet captures (`tcpdump`, `tshark`, `p0f`) to detect C2 jitter/beaconing, DNS tunneling, or OS/User-Agent spoofing.

---

## 2. 15-Engine Neuro-Symbolic Alignment for Hunt Team Operations
| Engine Layer | Engine Name | Hunt Team Strategic Role & Decision Rule |
| :--- | :--- | :--- |
| **Layer 0** | **Engine 1 (`associative`) & Engine 13 (`sygus_extractor`)** | Surface multi-hop lateral links across `[[knowledge/10_digital_forensics_pe_reversing_and_threat_intel]]`, `[[knowledge/07_packet_capture_bpf_wireshark_and_passive_fingerprinting]]`, and extract structured PIDs, sockets, and timestamps from raw forensic output. |
| **Layer 1** | **Engine 20 (`spectral_manifold_pca`) & Engine 12 (`cegar_verifier`)** | Use the **Mahalanobis Outlier Shield** ($D_M > 3.0$) and high PCA reconstruction residuals to flag anomalous host/network states; enforce strictly non-destructive read-only commands in `Analyst` mode. |
| **Layer 2** | **Engine 4 (`bayesian`) & Engine 10 (`dempster_shafer`)** | Rank competing intrusion hypotheses $P(H_i \mid E)$ and select the next forensic probe with maximum **Expected Information Gain (EIG)**; flag high **Dempster-Shafer Conflict ($K > 0.35$)** when userland tools (`ps`, `netstat`) disagree with kernel truth (`/proc/net/tcp`, raw `pktmon`/`tcpdump`). |
| **Layer 3/4** | **Engine 7 (`vsa`) & Engine 15 (`mdp_tactical`)** | Use 1,024-D VSA unbinding to detect deceptive/masquerading artifacts and restrict H-MDP selection to low-footprint `Passive_Enum` and `Enumeration` forensic probes. |
| **Layer 5** | **Engine 9 (`temporal_fluents`) & Engine 17 (`meta_learner`)** | Reconstruct the chronological attack timeline across Event-Calculus fluents (`T_initial_access` $\to$ `T_persistence` $\to$ `T_lateral_move`). |

---

## 3. Concise 5-Phase Threat Hunting Playbook (Windows & Linux)

### Phase 1: Process Lineage, Injection & `/proc` Memory Hunting (`Passive_Enum`)
| Hunt Hypothesis | Windows Command (`CMD` / `PowerShell` / `Sysinternals`) | Linux Command (`Bash`) | Anomaly Indicator (IoA) |
| :--- | :--- | :--- | :--- |
| **Anomalous Parent-Child Lineage & CLI Args** | `powershell -NoProfile -Command "Get-CimInstance Win32_Process \| Select-Object ProcessId,ParentProcessId,Name,ExecutablePath,CommandLine \| Format-List"` | `ps -eo pid,ppid,user,lstart,etime,cmd --forest` | Office/Web/DB daemons spawning shells (`powershell -enc`, `bash -i`, `rundll32`, `regsvr32`, `mshta`, `certutil`). |
| **Deleted Executables or Unbacked/Unsigned Modules** | `listdlls64.exe -u -nobanner & sigcheck64.exe -u -e C:\Windows\System32` | `ls -l /proc/[0-9]*/exe 2>/dev/null \| grep '(deleted)'` | Fileless/in-memory payloads executing from deleted binaries or unsigned DLLs side-loaded into trusted processes. |
| **RWX Injected Memory & Suspicious Environment/FDs** | `procdump64.exe -ma <SUSPICIOUS_PID> C:\Temp\proc_<PID>.dmp /accepteula` | `grep -H "rwxp" /proc/[0-9]*/maps 2>/dev/null \| grep -v "\[" && ls -l /proc/<PID>/fd` | Anonymous `rwxp` memory pages (shellcode/reflective DLL) or open sockets/memfd (`memfd:`) in `/proc/<PID>/fd`. |

### Phase 2: Stealth Persistence & ASEP Hunting (`Enumeration`)
| Hunt Hypothesis | Windows Command (`CMD` / `PowerShell` / `Sysinternals`) | Linux Command (`Bash`) | Anomaly Indicator (IoA) |
| :--- | :--- | :--- | :--- |
| **Comprehensive Autostart & Hash Verification** | `autorunsc64.exe -a * -c -h -s -v -nobanner` | `systemctl list-timers --all --no-pager && ls -la /etc/cron* /var/spool/cron/crontabs /etc/systemd/system` | Unsignedostart entries, high-entropy command strings, or binaries executing from `%TEMP%`, `%APPDATA%`, `/tmp`, or `/dev/shm`. |
| **Fileless WMI Event Subscription / `ld.so.preload` Rootkit** | `powershell -NoProfile -Command "Get-CimInstance -Namespace root\subscription -ClassName __EventFilter; Get-CimInstance -Namespace root\subscription -ClassName CommandLineEventConsumer; Get-CimInstance -Namespace root\subscription -ClassName __FilterToConsumerBinding"` | `cat /etc/ld.so.preload 2>/dev/null; env \| grep -i ld_preload; ls -la /etc/profile.d/ ~/.bashrc ~/.ssh/authorized_keys` | Persistent WMI consumers firing on timer/logon events on Windows, or shared-library hijacking (`ld.so.preload` / `LD_PRELOAD`) on Linux. |
| **Registry Run Keys, IFEO & Execution Artifacts (`BAM`)** | `reg query "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Run" /s & reg query "HKLM\SYSTEM\CurrentControlSet\Services\bam\State\UserSettings" /s` | `find /etc/systemd/system-generators /lib/systemd/system-generators -type f -exec ls -la {} +` | Unauthorized `Run`/`RunOnce` values, `Image File Execution Options` `Debugger` hijacks, or rogue systemd generators. |

### Phase 3: File System, NTFS ADS & Timestomp Hunting (`Enumeration`)
| Hunt Hypothesis | Windows Command (`CMD` / `PowerShell`) | Linux Command (`Bash`) | Anomaly Indicator (IoA) |
| :--- | :--- | :--- | :--- |
| **Hidden NTFS Alternate Data Streams (ADS) / World-Writable Staging** | `powershell -NoProfile -Command "Get-ChildItem -Path C:\Users,C:\ProgramData -Recurse -ErrorAction SilentlyContinue \| ForEach-Object { Get-Item $_.FullName -Stream * -ErrorAction SilentlyContinue } \| Where-Object { $_.Stream -ne ':$DATA' }"` | `find /tmp /var/tmp /dev/shm -type f -ls 2>/dev/null` | Payloads concealed inside NTFS `file.txt:payload.exe` streams or hidden dot-files staged in `/dev/shm` and `/tmp`. |
| **Timestomping ($STANDARD_INFORMATION vs Creation) & Rogue SUIDs** | `powershell -NoProfile -Command "Get-ChildItem C:\Windows\System32 -File \| Where-Object { $_.LastWriteTime -lt $_.CreationTime } \| Select-Object Name,CreationTime,LastWriteTime"` | `find / -perm -4000 -type f -ctime -30 2>/dev/null && getcap -r / 2>/dev/null` | Binaries in `System32` where `LastWriteTime` predates `CreationTime` (timestomping), or newly created SUID/capability binaries. |

### Phase 4: High-Signal Event Log & Authentication Correlation (`Passive_Enum`)
| Hunt Hypothesis | Windows Command (`CMD` / `PowerShell`) | Linux Command (`Bash`) | High-Signal Event IDs / Patterns |
| :--- | :--- | :--- | :--- |
| **Lateral Logons (`4624` Type 3/10), Failed Brute-Force (`4625`) & Special Privs (`4672`)** | `wevtutil qe Security "/q:*[System[(EventID=4624 or EventID=4625 or EventID=4672)]]" /c:40 /rd:true /f:text` | `journalctl -u ssh -u sshd --since "24 hours ago" --no-pager \| grep -E "Accepted\|Failed\|Invalid"` | Logon Type `3` (SMB/WinRM network) or Type `10` (RDP) from workstation-to-workstation IPs, or anomalous SSH key logons. |
| **New Service (`7045`/`4697`), Scheduled Task (`4698`) & Audit Clear (`1102`)** | `wevtutil qe System "/q:*[System[(EventID=7045)]]" /c:25 /rd:true /f:text & wevtutil qe Security "/q:*[System[(EventID=1102 or EventID=4697 or EventID=4698)]]" /c:25 /rd:true /f:text` | `sudo ausearch -m EXECVE,USER_AUTH,ADD_USER --start today 2>/dev/null \| tail -n 60` | Service installation with `cmd.exe /c` / `powershell` (`PsExec`/SMBExec), or Event ID `1102` (Security audit log cleared). |
| **Malicious PowerShell ScriptBlock (`4104`) Hunting** | `powershell -NoProfile -Command "Get-WinEvent -FilterHashtable @{LogName='Microsoft-Windows-PowerShell/Operational';Id=4104} -MaxEvents 30 \| Where-Object { $_.Message -match 'FromBase64String\|DownloadString\|Invoke-Expression\|IEX\|Net.WebClient\|AmsiUtils' } \| Select-Object TimeCreated,Id,Message"` | `grep -rnaE "curl.*\|.*sh\|wget.*\|.*sh\|base64 -d\|/dev/tcp/" /var/log /home/*/.bash_history 2>/dev/null` | Obfuscated Base64 cradles, reflective `AmsiUtils` patching, or `/dev/tcp/` reverse shell invocations. |

### Phase 5: Network Beaconing, BPF Packet Capture & Passive Fingerprinting (`Passive_Enum`)
| Hunt Hypothesis | Windows Command (`CMD` / `PowerShell`) | Linux Command (`Bash`) | Anomaly Indicator (IoA) |
| :--- | :--- | :--- | :--- |
| **Outbound C2 Connections & Kernel Socket Cross-Check** | `powershell -NoProfile -Command "Get-NetTCPConnection -State Established,SynSent \| Select-Object LocalAddress,LocalPort,RemoteAddress,RemotePort,OwningProcess,@{N='ProcName';E={(Get-Process -Id $_.OwningProcess).ProcessName}}"` | `ss -tanpi state established && wc -l /proc/net/tcp` | Non-browser processes (`svchost`, `rundll32`, `python3`, `cron`) holding persistent outbound connections; mismatch between `ss` and `/proc/net/tcp`. |
| **BPF Packet Capture for C2 Beaconing & DNS Tunneling** | `pktmon start --etw -p 0 -f C:\Temp\hunt.etl && timeout /t 30 && pktmon stop && pktmon etl2pcap C:\Temp\hunt.etl -o C:\Temp\hunt.pcapng` | `sudo tcpdump -nn -i any -s 0 -c 500 -w /tmp/hunt.pcap 'tcp or udp port 53 or icmp'` | Periodic fixed-interval or low-jitter HTTPS/DNS beacons, high-entropy TXT/CNAME DNS queries, or ICMP payload tunneling. |
| **Deep PCAP Inspection (`tshark`) & OS Spoofing (`p0f`)** | `tshark -r C:\Temp\hunt.pcapng -Y "http.request or tls.handshake.type == 1 or dns.qry.name" -T fields -e ip.src -e ip.dst -e tls.handshake.extensions_server_name -e http.user_agent -e dns.qry.name` | `tshark -r /tmp/hunt.pcap -Y "http.request or tls.handshake.type == 1 or dns.qry.name" -T fields -e ip.src -e ip.dst -e tls.handshake.extensions_server_name -e http.user_agent && p0f -r /tmp/hunt.pcap` | Suspicious SNI/User-Agent strings, direct-to-IP TLS handshakes (no SNI), or `p0f` TCP SYN TTL/Window fingerprint contradicting HTTP `User-Agent` OS. |
