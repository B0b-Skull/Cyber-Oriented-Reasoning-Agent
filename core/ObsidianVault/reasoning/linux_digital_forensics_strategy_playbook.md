---
title: linux_digital_forensics_strategy_playbook
category: reasoning
engine: team_strategy_arbiter
team_role: linux_forensics
os_platform: linux
domain_hub: "[[knowledge/10_digital_forensics_pe_reversing_and_threat_intel]]"
primary_tactic: Passive_Enum
summary: "Linux Digital Forensics (DFIR) Strategy & Techniques Playbook: complete native Linux forensic breakdown (/proc memory & deleted binary recovery, eBPF/LKM rootkit cross-checks, systemd/cron/ld.so.preload/PAM persistence, ext4/XFS MACB & debugfs inode forensics, journalctl/auditd/utmp/wtmp timelines) and open-source GitHub DFIR tools (UAC, AVML, LiME, Volatility 3 + dwarf2json, Velociraptor, SleuthKit/Autopsy, Plaso/log2timeline, Tracee, Unhide, YARA-X, Zeek)."
when_to_apply: "Apply whenever performing Linux or UNIX digital forensics, live incident response (DFIR), /proc process & fileless memfd investigation, deleted binary/inode recovery, rootkit & eBPF hook detection, systemd/auditd/wtmp log timeline correlation, or running open-source Linux forensic tools (UAC, AVML, LiME, Volatility 3, SleuthKit, Plaso, Velociraptor, Tracee)."
tags: [reasoning, linux_forensics, linux-forensics, dfir, forensics, linux, procfs, memfd, ebpf, systemd, journalctl, auditd, ausearch, wtmp, ext4, debugfs, uac, avml, lime, volatility3, sleuthkit, autopsy, plaso, log2timeline, tracee, unhide, yara-x, zeek]
updated: 2026-10-31 00:21:00
---
# Linux Digital Forensics (DFIR) Strategy & Techniques Playbook (`linux_digital_forensics_strategy_playbook`)

> **Team Role:** `LINUX_FORENSICS` (Linux/UNIX Live Response, `/proc` & Kernel Memory Forensics, Inode & Log Timeline Analysis)  
> **Target OS:** `Linux (Debian / Ubuntu / RHEL / CentOS / Rocky / Kali / Alpine / Embedded Linux)`  
> **Primary H-MDP Tactics:** `Passive_Enum` (Volatile `/proc`, RAM & Socket Acquisition) $\to$ `Enumeration` (Persistence, Inode MACB & Audit/Journal Parsing) $\to$ `Post_Exploitation_Verification` (Rootkit Cross-Check & Timeline Attribution)  
> **Recommended Console Posture:** `WHITE` (Air-Gapped Offline Forensic Analysis) or `BLUE` (Isolated Sensor NIC) | **Modes:** `Analyst` (Strict Read-Only Forensic Guardrail)  
> **Companion Command Playbook:** [[commands/linux_digital_forensics_playbook]]  
> **Backlinks:** [[00_MEMORY_INDEX]] | [[knowledge/10_digital_forensics_pe_reversing_and_threat_intel]] | [[knowledge/06_linux_unix_administration_processes_and_logging]] | [[knowledge/07_packet_capture_bpf_wireshark_and_passive_fingerprinting]] | [[reasoning/hunt_team_strategy_playbook]]

---

## 1. When Engines & LLM Must Activate This Playbook
Activate `[[reasoning/linux_digital_forensics_strategy_playbook]]` and `[[commands/linux_digital_forensics_playbook]]` whenever the query, goal, or attached evidence in `Projects/<project>/Files/` involves:
- **Live Linux Volatile `/proc` & Fileless Malware Forensics:** Investigating running processes via `/proc/<PID>/exe`, recovering unlinked `(deleted)` binaries or `memfd_create` (`memfd:`) anonymous memory payloads directly from RAM, inspecting `/proc/<PID>/maps` (`rwxp` shellcode), `/proc/<PID>/environ`, `/proc/<PID>/fd/`, and `/proc/<PID>/stack`.
- **Kernel Rootkit, LKM & eBPF Hook Detection:** Cross-checking userland tools (`ps`, `ss`, `ls`) against raw kernel structures (`/proc/[0-9]*`, `/proc/net/tcp`, `/proc/modules`, `/sys/module`, `bpftool prog list`).
- **Linux Persistence & Account Forensics:** Auditing `systemd` services/timers/generators, `cron`/`anacron`/`at`, `/etc/ld.so.preload` shared-library hijacks, PAM modules (`/etc/pam.d/`), SSH `authorized_keys`, `sudoers`, and shell profiles.
- **Linux File System (`ext4`/`XFS`), MACB Timestamps & Deleted Inode Recovery:** Extracting full MACB (`Modify`, `Access`, `Change`, `Birth/crtime`) timelines via `stat` and `debugfs`, hunting SUID/SGID and Linux Capabilities (`getcap`), and recovering deleted files via SleuthKit (`mmls`, `fls`, `icat`).
- **Open-Source GitHub Linux DFIR Tooling:** Setting up or executing **UAC (Unix-like Artifacts Collector)**, **AVML (Microsoft Acquire Volatile Memory for Linux)**, **LiME**, **Volatility 3** (`dwarf2json`), **Velociraptor**, **The Sleuth Kit (`tsk`) / Autopsy**, **Plaso (`log2timeline`)**, **Tracee**, **Unhide-NG**, **YARA-X**, or **Zeek**.

---

## 2. 15-Engine Neuro-Symbolic Alignment for Linux Forensics
| Engine Layer | Engine Name | Linux Forensic Role & Decision Rule |
| :--- | :--- | :--- |
| **Layer 0** | **Engine 1 (`associative`) & Engine 9 (`temporal_fluents`)** | Activate `[[reasoning/linux_digital_forensics_strategy_playbook]]` and `[[commands/linux_digital_forensics_playbook]]`; track MACB (`mtime`, `atime`, `ctime`, `crtime`) and `journalctl`/`auditd` UTC timestamps as monotonic temporal fluents. |
| **Layer 1** | **Engine 12 (`cegar_verifier`) & Engine 20 (`spectral_manifold_pca`)** | Enforce RFC 3227 Order of Volatility (capture `/proc/<PID>/exe` and RAM before killing processes or unmounting filesystems); flag outlier sockets/processes via Mahalanobis distance ($D_M > 3.0$). |
| **Layer 2** | **Engine 4 (`bayesian`) & Engine 10 (`dempster_shafer`)** | Compute **Dempster-Shafer Epistemic Conflict ($K$)** between userland utilities (`ps`, `ss`, `lsmod`) and raw kernel procfs/sysfs (`/proc/[0-9]*`, `/proc/net/tcp`, `/sys/module`, `bpftool`); $K > 0.35$ proves an active userland `LD_PRELOAD` or LKM/eBPF rootkit! |
| **Layer 3/4** | **Engine 13 (`sygus_extractor`) & Engine 15 (`mdp_tactical`)** | Extract structured PIDs, inode numbers, SHA-256 hashes, and socket hex addresses; restrict H-MDP actions in `Analyst` mode to non-mutating forensic reads. |

---

## 3. PART I: Full Forensic Breakdown of Native Linux Commands (Zero-Dependency)

### 3.1 Order of Volatility Step 1: Live `/proc` Process, Memory & Fileless Payload Forensics
| Forensic Artifact | Native Linux Command (`Bash`) | What It Proves & Forensic Significance |
| :--- | :--- | :--- |
| **Recover Deleted / Fileless Binaries (`(deleted)` & `memfd:`)** | `ls -la /proc/[0-9]*/exe 2>/dev/null \| grep -E '\(deleted\)\|memfd:'` $\to$ **Recover binary:** `cp /proc/<PID>/exe /tmp/recovered_pid_<PID>.elf && sha256sum /tmp/recovered_pid_<PID>.elf` | Adversaries frequently delete their binary on disk immediately after launch or execute via `memfd_create()`. As long as the PID is alive, `/proc/<PID>/exe` is a live kernel symlink to the intact ELF inode in RAM! |
| **Full Process Lineage, Exact Start Time & Raw `cmdline`** | `ps -eo pid,ppid,uid,user,lstart,etime,stat,comm,args --forest` & `for p in /proc/[0-9]*; do printf "%s: " "${p#/proc/}"; tr '\0' ' ' < "$p/cmdline" 2>/dev/null; echo; done` | Cross-checks `ps` output against raw `/proc/<PID>/cmdline` (detects `argv[0]` process name masquerading where `comm` differs from `cmdline`). |
| **Process Environment Variables (`SSH_CONNECTION`, `LD_PRELOAD`)** | `tr '\0' '\n' < /proc/<PID>/environ` *(or scan all PIDs: `grep -zE "LD_PRELOAD\|SSH_CLIENT\|SSH_CONNECTION\|HISTFILE" /proc/[0-9]*/environ 2>/dev/null \| tr '\0' '\n'`)* | Reveals the attacker's origin IP (`SSH_CONNECTION=<SRC_IP> <SPORT> <DST_IP> 22`), `LD_PRELOAD` rootkits, or `HISTFILE=/dev/null` anti-forensics. |
| **Open File Descriptors, Deleted Log Locks & Socket Inodes** | `ls -la /proc/<PID>/fd 2>/dev/null && ls -ld /proc/<PID>/cwd /proc/<PID>/root 2>/dev/null` | Identifies open sockets (`socket:[inode]`), pipes, chroot jails (`/proc/<PID>/root`), and unlinked files still held open by the process. |
| **Hunt Anonymous `rwxp` Injected Shellcode Pages in RAM** | `grep -H "rwxp" /proc/[0-9]*/maps 2>/dev/null \| grep -v "\["` $\to$ **Dump memory region:** `dd if=/proc/<PID>/mem bs=1 skip=$((0x<START_HEX>)) count=$((0x<END_HEX>-0x<START_HEX>)) of=/tmp/rwx_<PID>.bin` | Legitimate compiled ELF binaries enforce `W^X` (`r-xp` code, `rw-p` data); anonymous `rwxp` regions with no backing file path indicate injected shellcode or JIT/reflective loaders. |
| **Inspect Process Kernel Stack, Capabilities & TracerPid** | `grep -E "Name:\|State:\|PPid:\|TracerPid:\|Uid:\|Gid:\|CapEff:" /proc/<PID>/status && cat /proc/<PID>/stack 2>/dev/null` | `TracerPid != 0` indicates `ptrace` process injection or debugging; `CapEff: 000001ffffffffff` indicates full root capabilities even if `Uid != 0`. |

### 3.2 Order of Volatility Step 2: Network Sockets, Kernel Modules, eBPF & Rootkit Cross-Verification
| Forensic Artifact | Native Linux Command (`Bash`) | What It Proves & Forensic Significance |
| :--- | :--- | :--- |
| **Active Sockets, TCP Timers & Owning PIDs** | `ss -tulpn && ss -tanpi && lsof -i -n -P` | Captures all listening and established TCP/UDP sockets, owning PIDs, UID, and internal kernel TCP congestion/retransmit timers. |
| **Kernel `/proc/net/tcp` vs. Userland `ss` Rootkit Diff** | `awk 'NR>1 {split($2,l,":"); split($3,r,":"); printf "Local:%d.%d.%d.%d:%d Remote:%d.%d.%d.%d:%d State:%s Inode:%s\n", strtonum("0x"substr(l[1],7,2)),strtonum("0x"substr(l[1],5,2)),strtonum("0x"substr(l[1],3,2)),strtonum("0x"substr(l[1],1,2)),strtonum("0x"l[2]), strtonum("0x"substr(r[1],7,2)),strtonum("0x"substr(r[1],5,2)),strtonum("0x"substr(r[1],3,2)),strtonum("0x"substr(r[1],1,2)),strtonum("0x"r[2]), $4, $10}' /proc/net/tcp` | Decodes little-endian hex IP:Port directly from `/proc/net/tcp` without calling `ss` or `netstat` (which may be trojanized or hooked via `LD_PRELOAD`). |
| **Loaded Kernel Modules (`LKM`) & Taint State** | `cat /proc/sys/kernel/tainted && lsmod && diff -u <(lsmod \| awk 'NR>1{print $1}' \| sort) <(ls /sys/module \| sort)` | Non-zero `/proc/sys/kernel/tainted` (e.g., `4096` = out-of-tree module, `8192` = unsigned module) or discrepancies between `/proc/modules` and `/sys/module` indicate LKM rootkits (e.g., Diamorphine, Reptile). |
| **eBPF Programs & Maps Inspection (`eBPF Rootkits`)** | `sudo bpftool prog list && sudo bpftool map list && sudo bpftool net list` | Detects modern eBPF rootkits (`kprobe`, `tracepoint`, `xdp`, `tc`, `raw_tracepoint` hooks on `sys_getdents64`, `tcp4_seq_show`, or `bpf`). |

### 3.3 Order of Volatility Step 3: Linux Persistence, PAM, SSH & Shared Library Hijacking
| Forensic Artifact | Native Linux Command (`Bash`) | What It Proves & Forensic Significance |
| :--- | :--- | :--- |
| **Shared Library Preload Hijacking (`ld.so.preload`)** | `cat /etc/ld.so.preload 2>/dev/null; ls -la /etc/ld.so.conf.d/; env \| grep -i ld_` | `/etc/ld.so.preload` forces the dynamic linker (`ld-linux.so`) to inject a shared object (`.so`) into every dynamically linked process on the host (classic userland rootkit). |
| **`systemd` Services, Timers & Generators** | `systemctl list-unit-files --type=service,timer --state=enabled,generated && find /etc/systemd/system /run/systemd/system /lib/systemd/system /etc/systemd/system-generators -mtime -14 -ls 2>/dev/null` | Detects recently created or modified `systemd` services, stealthy `.timer` units, and early-boot `system-generators` scripts. |
| **Cron, Anacron, At & Init Scripts** | `ls -la /etc/crontab /etc/cron* /var/spool/cron/crontabs /var/spool/anacron /etc/init.d /etc/rc.local 2>/dev/null && head -n 50 /etc/crontab /etc/cron.d/* /var/spool/cron/crontabs/* 2>/dev/null` | Audits all system-wide and per-user scheduled tasks. |
| **PAM Backdoors, `passwd`/`shadow` & `sudoers`** | `awk -F: '($3 == 0) {print}' /etc/passwd && grep -vE '^#\|^$' /etc/sudoers /etc/sudoers.d/* 2>/dev/null && ls -la --time-style=full-iso /etc/pam.d/ /lib/*/security/pam_*.so` | Detects rogue UID `0` accounts, `NOPASSWD` sudo rules, or modified `pam_unix.so` / `pam_exec.so` authentication backdoors. |
| **SSH Authorized Keys, `sshd_config` & RC Profiles** | `find /root /home -name "authorized_keys*" -o -name ".bashrc" -o -name ".profile" -o -name ".bash_history" -exec ls -la --time-style=full-iso {} + 2>/dev/null` | Identifies injected SSH keys (including `command="..."` forced-command options) and shell RC backdoors. |

### 3.4 Order of Volatility Step 4: File System (`ext4`/`XFS`), MACB Timestamps & Inode Forensics
| Forensic Artifact | Native Linux Command (`Bash`) | What It Proves & Forensic Significance |
| :--- | :--- | :--- |
| **Full 4-Timestamp MACB (`Modify/Access/Change/Birth`) Audit** | `stat <FILE_PATH>` *(or batch scan recent inode metadata changes: `find /etc /bin /sbin /usr /var /tmp /dev/shm -ctime -3 -printf "%CY-%Cm-%Cd %CT [ctime] | %TY-%Tm-%Td %TT [mtime] | %M %u:%g %s %p\n" 2>/dev/null \| sort -r`)* | Adversaries can fake `mtime` and `atime` using `touch -t`, but kernel inode status change `ctime` updates automatically and cannot be backdated without raw disk/clock manipulation! |
| **Extract `ext4` Inode Birth Time (`crtime`) & Deletion Time (`dtime`)** | `df -T <FILE_PATH>` $\to$ `sudo debugfs -R "stat <FILE_PATH_OR_INODE>" /dev/<BLOCK_DEV>` | Queries the raw `ext4` on-disk inode structure for `crtime` (true creation timestamp) and `dtime` (exact deletion timestamp). |
| **SUID/SGID, File Capabilities (`getcap`) & `chattr` Flags** | `find / -perm /6000 -type f -ls 2>/dev/null && getcap -r / 2>/dev/null && lsattr /etc/passwd /etc/shadow /etc/ld.so.preload 2>/dev/null` | Detects SUID/SGID backdoors, `cap_setuid+ep` capability backdoors, and immutable (`+i`) or append-only (`+a`) rootkit files. |

### 3.5 Order of Volatility Step 5: `journalctl`, `auditd`, `utmp`/`wtmp`/`btmp` & Syslog Forensics
| Forensic Artifact | Native Linux Command (`Bash`) | What It Proves & Forensic Significance |
| :--- | :--- | :--- |
| **Verify `systemd-journald` Integrity & Export JSON Timeline** | `journalctl --verify && journalctl --since "48 hours ago" -o short-iso-precise --no-pager \| tail -n 200` | Verifies journal file integrity against tampering and outputs microsecond-precision ISO-8601 UTC event logs. |
| **Linux Audit Daemon (`auditd`) Syscall & Execution Forensics** | `sudo ausearch -i -m EXECVE,USER_AUTH,USER_LOGIN,USER_CMD,ADD_USER,DEL_USER,PROCTITLE --start today 2>/dev/null` & `sudo aureport --summary -i && sudo aureport -x --summary -i` | Reconstructs every `execve()` system call (including full hex-decoded `PROCTITLE` arguments), authentication event, and user modification. |
| **Binary Login Accounting (`wtmp`, `btmp`, `utmp`, `lastlog`)** | `last -aiF -n 50 && sudo lastb -aiF -n 50 && lastlog && utmpdump /var/log/wtmp 2>/dev/null \| tail -n 50` | Parses `/var/log/wtmp` (historical logons/reboots), `/var/log/btmp` (failed brute-force logons), and `/var/run/utmp` (currently logged-in sessions); `utmpdump` exposes raw records to spot `wtmp` wiping gaps. |
| **Authentication, Sudo & SSH Log Correlation** | `grep -aE "Accepted\|Failed\|Invalid user\|session opened\|sudo:\|COMMAND=" /var/log/auth.log /var/log/secure 2>/dev/null \| tail -n 100` | Correlates SSH password/publickey logons, source IPs, and executed `sudo` commands across Debian/Ubuntu (`auth.log`) and RHEL/CentOS (`secure`). |

---

## 4. PART II: Latest Open-Source & GitHub Linux Forensics Tools

### 4.1 Open-Source Linux DFIR GitHub Repository Directory & Setup
| Tool Name | Official GitHub URL | Core Forensic Capability | Quick Installation / Setup Command |
| :--- | :--- | :--- | :--- |
| **UAC (Unix-like Artifacts Collector)** | `https://github.com/tclahr/uac` | Zero-dependency agentless live response & forensic artifact collector for Linux, Solaris, macOS, AIX, and ESXi. | `git clone https://github.com/tclahr/uac.git && chmod +x uac/uac` |
| **AVML (Microsoft Acquire Volatile Memory)** | `https://github.com/microsoft/avml` | Standalone static Rust binary by Microsoft that acquires Linux physical RAM (`/dev/crash`, `/proc/kcore`, `/dev/mem`) without compiling kernel modules! | Download static binary `avml` from `https://github.com/microsoft/avml/releases` $\to$ `chmod +x avml`. |
| **LiME (Linux Memory Extractor)** | `https://github.com/504ensicsLabs/LiME` | Loadable Kernel Module (`lime.ko`) for acquiring full physical RAM over disk or TCP socket in `lime` / `raw` format. | `git clone https://github.com/504ensicsLabs/LiME.git && cd LiME/src && make` |
| **Volatility 3 & `dwarf2json`** | `https://github.com/volatilityfoundation/volatility3` / `https://github.com/volatilityfoundation/dwarf2json` | Linux physical RAM forensics (`linux.pslist`, `linux.bash`, `linux.malfind`, `linux.check_modules`, `linux.check_syscall`, `linux.sockstat`) + kernel ISF symbol generator. | `python3 -m pip install --upgrade volatility3` & download `dwarf2json` from GitHub Releases. |
| **Velociraptor (Linux)** | `https://github.com/Velocidex/velociraptor` | VQL live endpoint query engine and automated Linux triage collector (`Linux.Sys.*`, `Linux.Forensics.*`, `Linux.Detection.*`). | Download `velociraptor-v*-linux-amd64` from `https://github.com/Velocidex/velociraptor/releases` $\to$ `chmod +x`. |
| **The Sleuth Kit (`tsk`) & Autopsy** | `https://github.com/sleuthkit/sleuthkit` / `https://github.com/sleuthkit/autopsy` | Disk image partition analysis (`mmls`), `ext4`/`XFS` inode inspection (`istat`, `fls`), deleted file recovery (`icat`), and MACB timeline generation (`mactime`). | `sudo apt-get install -y sleuthkit` *(or `sudo dnf install -y sleuthkit`)* |
| **Plaso (`log2timeline`)** | `https://github.com/log2timeline/plaso` | Super-timeline engine parsing Linux `syslog`, `auth.log`, `journald`, `auditd`, `utmp`/`wtmp`, `ext4` filestats, Docker/K8s logs, and browser history. | `sudo docker pull log2timeline/plaso` *(or `pip install plaso`)* |
| **Tracee (Aqua Security)** | `https://github.com/aquasecurity/tracee` | eBPF runtime security & forensic tracer capturing fileless `memfd` execution, `ptrace`, LKM loads, and credential access. | `sudo docker run --name tracee --rm -it --pid=host --cgroupns=host --privileged -v /etc/os-release:/etc/os-release-host:ro aquasec/tracee:latest` |
| **Unhide-NG & Chkrootkit** | `https://github.com/YJesus/Unhide-NG` | Brute-forces PID and TCP/UDP port spaces to uncover processes and listeners hidden by LKM or `LD_PRELOAD` rootkits. | `sudo apt-get install -y unhide chkrootkit rkhunter` |
| **YARA-X & Zeek** | `https://github.com/VirusTotal/yara-x` / `https://github.com/zeek/zeek` | Rust YARA scanner for `/proc/<PID>/mem` & disk scanning (`yr`), and Zeek network security monitor for `.pcap` protocol log extraction. | Download `yr` from `https://github.com/VirusTotal/yara-x/releases`; `sudo apt-get install -y zeek`. |

### 4.2 High-Efficiency Execution Commands for Open-Source Linux Forensic Tools
| Tool | Verified Forensic Command Syntax | Expected Output & When to Apply |
| :--- | :--- | :--- |
| **AVML (Zero-Compile Linux RAM Dump)** | `sudo ./avml --compress /tmp/linux_memory.lime && sha256sum /tmp/linux_memory.lime` | Acquires compressed physical memory in LiME format without compiling a kernel module (`0` kernel taint) and computes chain-of-custody SHA-256. |
| **LiME (Kernel Module RAM Dump)** | `sudo insmod lime-$(uname -r).ko "path=/tmp/ram.lime format=lime"` | Acquires physical RAM via LKM on older kernels or custom embedded Linux appliances. |
| **`dwarf2json` (Generate Kernel ISF Symbol Table)** | `./dwarf2json linux --elf /usr/lib/debug/boot/vmlinux-$(uname -r) --system-map /boot/System.map-$(uname -r) \| xz -c > linux_kernel_isf.json.xz` | Generates the exact Volatility 3 Intermediate Symbol File (`isf.json.xz`) for the target Linux kernel. |
| **Volatility 3 (Linux RAM Forensics)** | `vol -f /tmp/linux_memory.lime linux.pstree && vol -f /tmp/linux_memory.lime linux.bash && vol -f /tmp/linux_memory.lime linux.malfind && vol -f /tmp/linux_memory.lime linux.check_syscall && vol -f /tmp/linux_memory.lime linux.check_modules` | Recovers in-memory `bash` command history (even when `HISTFILE=/dev/null`), detects hooked syscall table entries (`check_syscall`), hidden kernel modules (`check_modules`), and injected `rwx` memory (`malfind`). |
| **UAC (Full Linux IR Triage Collection)** | `sudo ./uac -p ir_triage /tmp/uac_out` *(or `--artifacts live_response/process/*,live_response/network/*,files/logs/*`)* | Collects a standardized `.tar.gz` forensic triage package with SHA-256 manifest and acquisition log. |
| **Velociraptor (Linux VQL Triage)** | `./velociraptor-linux-amd64 query "SELECT Pid, Ppid, Name, Exe, CommandLine FROM pslist()" --format json` | Runs VQL queries across Linux processes, network sockets, SSH keys, and systemd units. |
| **SleuthKit (`fls` + `mactime` Super-Timeline & `icat` Recovery)** | `fls -r -m "/" /dev/sda1 > /tmp/bodyfile.txt && mactime -b /tmp/bodyfile.txt -d -z UTC > /tmp/fs_timeline.csv` & `fls -r -d /dev/sda1` $\to$ `icat /dev/sda1 <DELETED_INODE> > /tmp/recovered_file` | Generates a full UTC MACB filesystem CSV timeline (`mactime`) and recovers deleted files by inode number (`icat`). |
| **Plaso (`log2timeline` Unified Timeline)** | `log2timeline.py --storage-file /tmp/linux_case.plaso /var/log && psort.py -o l2tcsv -w /tmp/supertimeline.csv /tmp/linux_case.plaso` | Parses all `/var/log` files (`journal`, `audit.log`, `auth.log`, `wtmp`, `syslog`) into a single chronological super-timeline CSV. |
| **Unhide (Hidden Rootkit PID & Port Brute-Force)** | `sudo unhide sys proc brute && sudo unhide-tcp` | Compares `procfs`, `sysfs`, `ps`, and brute-forced `kill(pid,0)` / `getpriority()` syscalls to expose rootkit-cloaked PIDs and TCP/UDP ports. |
| **Zeek (`.pcap` Forensic Transaction Extraction)** | `zeek -C -r /tmp/capture.pcap && head -n 40 conn.log dns.log http.log ssl.log files.log 2>/dev/null` | Converts a raw `.pcap` into structured forensic logs (`conn.log`, `dns.log`, `http.log`, `ssl.log`, `files.log`). |
