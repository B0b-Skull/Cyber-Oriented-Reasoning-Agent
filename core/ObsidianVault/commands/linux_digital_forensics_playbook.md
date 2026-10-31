---
title: linux_digital_forensics_playbook
category: commands
os_platform: linux
domain_hub: "[[knowledge/10_digital_forensics_pe_reversing_and_threat_intel]]"
primary_tactic: Passive_Enum
summary: "Master Linux Digital Forensics (DFIR) command reference covering native Linux forensic acquisition (/proc deleted binaries, rwxp memory, eBPF/LKM rootkits, systemd/cron/ld.so.preload/PAM, ext4 debugfs MACB, journalctl/auditd/wtmp) and open-source GitHub tools (UAC, AVML, LiME, Volatility 3, Velociraptor, SleuthKit, Plaso, Tracee, Unhide, Zeek)."
when_to_apply: "Apply when executing Linux live forensic triage, recovering deleted /proc/<PID>/exe or memfd binaries, hunting LKM/eBPF/LD_PRELOAD rootkits, extracting ext4 crtime/dtime inodes, or running UAC, AVML, LiME, Volatility 3, SleuthKit, Plaso, Velociraptor, or Unhide."
tags: [commands, linux_forensics, linux-forensics, dfir, forensics, linux, procfs, memfd, ebpf, systemd, journalctl, auditd, ausearch, wtmp, debugfs, uac, avml, lime, volatility3, sleuthkit, plaso, tracee, unhide, zeek]
updated: 2026-10-31 00:22:00
---
# Linux Digital Forensics (DFIR) Master Command Playbook (`linux_digital_forensics_playbook`)

> **Strategy Playbook:** [[reasoning/linux_digital_forensics_strategy_playbook]]  
> **Domain Knowledge Hub:** [[knowledge/10_digital_forensics_pe_reversing_and_threat_intel]]  
> **Backlinks:** [[00_MEMORY_INDEX]] | [[commands/linux_master_command_playbook]] | [[knowledge/06_linux_unix_administration_processes_and_logging]] | [[knowledge/07_packet_capture_bpf_wireshark_and_passive_fingerprinting]]

---

## 1. Native Linux Forensic Acquisition Commands (By Order of Volatility)
| Forensic Phase | Verified Native Linux Command (`Bash`) | Key Flags & Forensic Output |
| :--- | :--- | :--- |
| **1. Recover Deleted & Fileless (`/proc/*/exe`) Binaries** | `ls -la /proc/[0-9]*/exe 2>/dev/null \| grep -E '\(deleted\)\|memfd:'` $\to$ `cp /proc/<PID>/exe /tmp/recovered_<PID>.elf && sha256sum /tmp/recovered_<PID>.elf` | Recovers unlinked or `memfd_create()` fileless binaries directly from the live kernel inode before process exit. |
| **2. Raw `/proc` Process Tree, `cmdline` & `environ`** | `ps -eo pid,ppid,uid,user,lstart,etime,comm,args --forest && grep -zE "LD_PRELOAD\|SSH_CLIENT\|SSH_CONNECTION\|HISTFILE" /proc/[0-9]*/environ 2>/dev/null \| tr '\0' '\n'` | Exposes `argv[0]` masquerading, `LD_PRELOAD` injection, attacker `SSH_CONNECTION` source IP, and `HISTFILE=/dev/null`. |
| **3. Anonymous `rwxp` Injected Memory & FD Audit** | `grep -H "rwxp" /proc/[0-9]*/maps 2>/dev/null \| grep -v "\[" && ls -la /proc/<PID>/fd /proc/<PID>/cwd 2>/dev/null` | Detects shellcode/reflective loaders in anonymous `rwxp` pages and lists open socket/pipe/deleted file descriptors. |
| **4. Kernel `/proc/net/tcp`, `bpftool` & LKM Rootkit Check** | `ss -tanpi && cat /proc/sys/kernel/tainted && diff -u <(lsmod \| awk 'NR>1{print $1}' \| sort) <(ls /sys/module \| sort) && sudo bpftool prog list 2>/dev/null` | Cross-verifies userland `ss`/`lsmod` against `/sys/module` and inspects active eBPF hooks (`kprobe`/`tracepoint`/`xdp`). |
| **5. Persistence Audit (`ld.so.preload`, `systemd`, `cron`, `PAM`)** | `cat /etc/ld.so.preload 2>/dev/null; systemctl list-unit-files --type=service,timer --state=enabled; ls -la /etc/cron* /var/spool/cron/crontabs; awk -F: '($3==0){print}' /etc/passwd` | Audits linker hijacks, enabled services/timers, cron jobs, and UID `0` accounts. |
| **6. Inode MACB (`ctime`/`mtime`) & `debugfs` `crtime`/`dtime`** | `find /etc /bin /sbin /usr /var /tmp /dev/shm -ctime -3 -printf "%CY-%Cm-%Cd %CT [ctime] | %TY-%Tm-%Td %TT [mtime] | %M %u:%g %s %p\n" 2>/dev/null \| sort -r` & `sudo debugfs -R "stat <INODE_OR_PATH>" /dev/sda1` | Detects `touch -t` timestomping (`ctime > mtime`) and reads raw `ext4` birth (`crtime`) and deletion (`dtime`) timestamps. |
| **7. `journalctl`, `ausearch` & `utmpdump` Log Timelines** | `journalctl --verify && sudo ausearch -i -m EXECVE,USER_AUTH,USER_LOGIN --start today 2>/dev/null && last -aiF -n 40 && utmpdump /var/log/wtmp 2>/dev/null \| tail -n 40` | Verifies journal integrity, decodes `auditd` `EXECVE` syscalls, and inspects raw binary `wtmp` login records. |

---

## 2. Open-Source GitHub Linux Forensics Tool Commands
| Open-Source Tool (`GitHub`) | Verified CLI Command | Flag Breakdown & When to Apply |
| :--- | :--- | :--- |
| **AVML** (`microsoft/avml`) | `sudo ./avml --compress /tmp/linux_ram.lime && sha256sum /tmp/linux_ram.lime` | `--compress`: Acquires physical RAM in compressed LiME format using a zero-dependency static Rust binary (no kernel module compilation). |
| **LiME** (`504ensicsLabs/LiME`) | `sudo insmod lime-$(uname -r).ko "path=/tmp/linux_ram.lime format=lime"` | Acquires physical RAM via LKM (`lime.ko`) into `lime` format for Volatility 3. |
| **`dwarf2json`** (`volatilityfoundation/dwarf2json`) | `./dwarf2json linux --elf /usr/lib/debug/boot/vmlinux-$(uname -r) --system-map /boot/System.map-$(uname -r) \| xz -c > kernel_isf.json.xz` | Builds the kernel Intermediate Symbol File (`isf.json.xz`) required by Volatility 3 for custom Linux kernels. |
| **Volatility 3** (`volatilityfoundation/volatility3`) | `vol -f /tmp/linux_ram.lime linux.pstree && vol -f /tmp/linux_ram.lime linux.bash && vol -f /tmp/linux_ram.lime linux.malfind && vol -f /tmp/linux_ram.lime linux.check_syscall && vol -f /tmp/linux_ram.lime linux.check_modules` | Extracts in-memory `bash` history, process tree, injected `rwx` regions (`malfind`), syscall table hooks, and hidden LKM rootkits. |
| **UAC** (`tclahr/uac`) | `sudo ./uac -p ir_triage /tmp/uac_output` | `-p ir_triage`: Runs agentless live response collection across `/proc`, network, logs, and persistence into a hashed `.tar.gz` archive. |
| **Velociraptor** (`Velocidex/velociraptor`) | `./velociraptor-linux-amd64 query "SELECT Pid, Ppid, Name, Exe, CommandLine FROM pslist()" --format json` | Runs live VQL queries across Linux processes, sockets, crontabs, and SSH keys. |
| **The Sleuth Kit** (`sleuthkit/sleuthkit`) | `mmls disk.dd && fls -r -m "/" /dev/sda1 > /tmp/bodyfile && mactime -b /tmp/bodyfile -d -z UTC > /tmp/macb_timeline.csv` | `mmls`: partition layout; `fls -r -m`: recursive bodyfile; `mactime -d`: generates CSV MACB filesystem timeline. |
| **SleuthKit Deleted File Recovery** (`icat`) | `fls -r -d /dev/sda1` $\to$ `icat /dev/sda1 <DELETED_INODE> > /tmp/recovered.bin` | `fls -r -d`: lists unallocated/deleted inodes; `icat`: extracts raw data blocks of `<DELETED_INODE>`. |
| **Plaso / `log2timeline`** (`log2timeline/plaso`) | `log2timeline.py --storage-file /tmp/case.plaso /var/log && psort.py -o l2tcsv -w /tmp/supertimeline.csv /tmp/case.plaso` | Aggregates all `/var/log`, `journald`, `auditd`, and `wtmp` records into a unified chronological super-timeline CSV. |
| **Unhide-NG** (`YJesus/Unhide-NG`) | `sudo unhide sys proc brute && sudo unhide-tcp` | Brute-forces PIDs (`1..max_pid`) and TCP/UDP ports (`1..65535`) to reveal processes and listeners hidden by rootkits. |
| **Zeek** (`zeek/zeek`) | `zeek -C -r /tmp/capture.pcap && head -n 40 conn.log dns.log http.log ssl.log files.log 2>/dev/null` | `-C`: ignore checksum offload errors; `-r`: parses `.pcap` into structured network forensic logs. |
