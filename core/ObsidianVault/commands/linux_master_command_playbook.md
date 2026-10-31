---
title: "Linux & UNIX Master Command Playbook (iproute2, ss, iptables/nftables, sysctl, systemd, tcpdump/BPF, nmap, curl, tio & Privilege Escalation)"
category: commands
domain_hub: "[[knowledge/06_linux_unix_administration_processes_and_logging]]"
os_platform: linux
primary_tactic: Passive_Enum
summary: "Comprehensive Linux and UNIX operational command playbook covering iproute2, ss sockets, iptables/nftables firewalls, sysctl forwarding, systemd/journalctl, procfs, SUID/capabilities, tcpdump/BPF, nmap, curl, and tio UART serial consoles with flag explanations and When-to-Apply rules."
when_to_apply: "Apply whenever operating on, enumerating, routing through, hardening, capturing traffic on, or troubleshooting a Linux/UNIX host, network appliance, or serial OOB console."
tags: [linux, unix, iproute2, ss, netstat, iptables, nftables, sysctl, ip_forward, masquerade, tcpdump, bpf, tshark, p0f, snort, nmap, curl, tio, serial, ttyusb0, systemctl, journalctl, lsof, strace, findmnt, lsblk, getcap, sudo, chmod, find, grep, passive_enum, active_enum, l2_l3_pivot_routing, defense_evasion_firewall, privilege_escalation, oob_serial_access]
updated: 2026-10-30
---

# Linux & UNIX Master Command Playbook (`iproute2`, `ss`, `iptables`/`nftables`, `sysctl`, `systemd`, `tcpdump`, `nmap`, `curl` & `tio`)

> **Summary:** Authoritative Linux/UNIX command reference with flag-by-flag breakdowns, expected outputs, 15-Engine H-MDP state triggers, and Windows cross-platform equivalents.  
> **Backlinks:** [[00_MEMORY_INDEX]] | [[00_TRAINED_INDEX]] | [[commands/windows_master_command_playbook]] | [[commands/curl_playbook]] | [[commands/tio_serial_playbook]]  
> **Domain Knowledge Hubs:** [[knowledge/05_windows_and_linux_networking_routing_and_firewalls]] | [[knowledge/06_linux_unix_administration_processes_and_logging]] | [[knowledge/07_packet_capture_bpf_wireshark_and_passive_fingerprinting]] | [[knowledge/08_web_api_sql_injection_and_active_reconnaissance]] | [[knowledge/09_hardware_uart_serial_oob_and_telecom_wan]]

---

## When to Apply (LLM & 15-Engine Decision Matrix)

| Operational Scenario / Symptom | H-MDP Pre-State ($s$) | Optimal Tactic ($\tau$) | Primary Linux Tools | Isolation Compatibility |
| :--- | :--- | :--- | :--- | :--- |
| **Initial Host, Kernel & Privilege Survey** | `s_init_unknown` | `Passive_Enum` | `uname -a`, `id`, `hostnamectl`, `cat /etc/os-release`, `sudo -l` | `RED`, `BLUE`, `WHITE` |
| **L2/L3 Interfaces, Subnets, Routes & ARP Neighbors** | `s_init_unknown` | `Passive_Enum` | `ip -4 -br addr show`, `ip route show`, `ip neigh show`, `ip -d link show` | `RED`, `BLUE`, `WHITE` |
| **L4 Listening Sockets & Process-to-Port Attribution** | `s_passive_topology_mapped` | `Passive_Enum` | `ss -tulpn`, `ss -tanp`, `lsof -i -P -n`, `fuser -v <port>/tcp` | `RED`, `BLUE`, `WHITE` |
| **Cross-Subnet Static Routing, IP Forwarding & NAT** | `s_passive_topology_mapped` | `L2_L3_Pivot_Routing` | `ip route replace`, `sysctl -w net.ipv4.ip_forward=1`, `iptables -t nat -A POSTROUTING -j MASQUERADE` | `RED`, `BLUE` (Allowed NICs) |
| **Active Host Discovery, Port/Service & TLS Recon** | `s_l2_l3_verified` | `Active_Enum` | `ping -c 2 -W 1`, `nmap -sV -sC -Pn`, `curl -sS -k -L -i`, `openssl s_client` | `RED`, `BLUE` (Allowed NICs) |
| **Hardware UART Serial Out-of-Band (`OOB`) Console** | `s_l2_l3_verified` | `OOB_Serial_Access` | `tio -b 115200 -o 15 -O 120 --mute --script-run once --script '<lua>' /dev/ttyUSB0` | `RED`, `BLUE` |
| **Host Firewall (`iptables`/`nftables`) & IDS Unlock** | `s_oob_serial_enumerated` | `Defense_Evasion_Firewall` | `iptables -L -n -v`, `iptables -I INPUT 1 -j ACCEPT`, `nft list ruleset`, `snort` | `RED`, `BLUE`, `WHITE` |
| **SUID/SGID, Linux Capabilities, `sudo` & TTY Upgrade** | `s_initial_shell_or_api_access` | `Privilege_Escalation` | `find / -perm -4000`, `getcap -r /`, `sudo -l`, `python3 -c 'import pty; pty.spawn("/bin/bash")'` | `RED`, `BLUE`, `WHITE` |
| **Packet Capture (`tcpdump`), BPF & Passive OS (`p0f`)** | `s_passive_topology_mapped` | `Passive_Enum` | `tcpdump -ni <IFACE>`, `tshark -r`, `p0f -i <IFACE>` | `RED`, `BLUE` |

---

## 1. Host Identity, Kernel, Hardware & Privilege Context (`Passive_Enum`)

| Linux Command | Description & Key Flags | When to Apply & Expected Output | Windows Equivalent |
| :--- | :--- | :--- | :--- |
| `uname -a && cat /etc/os-release` | Prints kernel release, CPU architecture (`x86_64`/`aarch64`), build date, and Linux distribution name/version. | **Apply first** on any Linux host (`s_init_unknown`) to establish OS distribution and kernel version (`[[commands/trained_centos-debian-survey]]`). | `systeminfo && ver` |
| `id && groups && whoami` | Shows effective/real UID, GID, supplementary groups (`sudo`, `wheel`, `docker`, `adm`, `dialout`, `llm-local`), and SELinux/AppArmor context (`Z`). | **Apply immediately** to check current privilege level and whether the user is in `dialout` (serial access) or `sudo`/`docker`. | `whoami /all` |
| `w && last -a -n 15` | Lists currently logged-in users (`w`), their TTY/PTS, source IPs, active commands, and the last 15 login sessions (`last -a`). | Apply during live response to identify concurrent operator or attacker sessions (`[[commands/trained_linux-user]]`). | `psloggedon && query user` |
| `lscpu && free -h && lsusb && lspci` | Summarizes CPU cores/NUMA topology, RAM/swap utilization, USB peripherals (`FTDI`/`CP210x` UART adapters), and PCI devices. | Apply to verify hardware resources and detect attached USB-to-Serial adapters (`/dev/ttyUSB*`). | `wmic cpu && wmic memorychip` |
| `lsmod && cat /proc/cmdline` | Lists loaded Linux kernel modules (`lsmod`) and kernel boot parameters (`/proc/cmdline`). | Apply when auditing kernel drivers or checking for rootkit/custom modules (`[[knowledge/trained_l-linux-kernel-pdf]]`). | `driverquery /v && bcdedit /enum` |

---

## 2. `iproute2` L2/L3 Networking: Interfaces, Neighbor/ARP Table, VLANs & Bridges (`Passive_Enum`)

| Linux Command | Description & Key Flags | When to Apply & Expected Output | Windows Equivalent |
| :--- | :--- | :--- | :--- |
| `ip -4 -br addr show; ip route show; ip neigh show` | **CORA Canonical 3-in-1 Passive L2/L3 Probe**: prints brief IPv4 addresses (`-4 -br`), active routing table, and L2 ARP neighbor cache (`REACHABLE`/`STALE`/`FAILED`). | **Engine 1/15 Consensus Probe (`s_init_unknown -> s_passive_topology_mapped`)**: maps all local interfaces, subnets, gateways, and ARP neighbors in `< 15 ms` with zero network noise. | `ipconfig /all & route print -4 & arp -a` |
| `ip -d link show` | Displays detailed (`-d`) L2 link attributes: MAC address, MTU, `UP`/`LOWER_UP` carrier state, `PROMISC` flag, `802.1Q` VLAN IDs, and bridge master bindings. | Apply to detect VLAN tags, promiscuous interfaces (packet sniffers), or missing physical link carrier (`NO-CARRIER`). | `Get-NetAdapter \| Format-List *` |
| `ip neigh show <TARGET_IP>` | Checks the kernel L2 ARP table entry for `<TARGET_IP>` (`lladdr <MAC> REACHABLE` vs `INCOMPLETE`/`FAILED`). | Apply before active scanning to verify if `<TARGET_IP>` is resolved at Layer 2. | `arp -a <TARGET_IP>` |
| `arping -c 2 -w 2 -I <IFACE> <TARGET_IP>` | Sends 2 Layer-2 ARP Who-Has requests directly out `<IFACE>` for `<TARGET_IP>`. | **Apply when ICMP `ping` is blocked by a host firewall** on the local subnet: L2 ARP replies even when ICMP is dropped! | `arp -d <TARGET_IP> && ping -n 1 <TARGET_IP> && arp -a <TARGET_IP>` |
| `bridge link show && ip -d link show type bridge` | Lists L2 software bridge ports, STP (`Spanning Tree Protocol`) states (`forwarding`/`blocking`), and VLAN filtering (`[[knowledge/trained_cqc001_e010_m060_spanning_tree_protocol]]`). | Apply on Linux routers, hypervisors, or appliances bridging multiple NICs. | `Get-NetAdapterBinding` |

---

## 3. L3 Routing, Policy Routing, `sysctl` Forwarding & Cross-Subnet Pivoting (`L2_L3_Pivot_Routing`)

| Linux Command | Description & Key Flags | When to Apply & Expected Output | Windows Equivalent |
| :--- | :--- | :--- | :--- |
| `ip route get <TARGET_IP>` | Asks the Linux kernel FIB (`Forwarding Information Base`) which exact output interface (`dev`), source IP (`src`), and gateway (`via`) will be used to reach `<TARGET_IP>`. | **Apply whenever `Network is unreachable` or `No route to host` occurs**: proves exactly how the kernel routes to `<TARGET_IP>`. | `Find-NetRoute -RemoteIPAddress <TARGET_IP>` |
| `ip route show table all && ip rule show` | Dumps all routing tables (`local`, `main`, `default`, custom policy tables) and RPDB policy routing rules (`ip rule`). | Apply when standard `ip route show` looks normal but traffic is blackholed by a policy rule or VPN/SD-WAN table. | `route print -4` |
| `sudo ip route replace <REMOTE_SUBNET> via <GATEWAY_IP> dev <IFACE>` | Atomically adds or updates an L3 static route to `<REMOTE_SUBNET>` through next-hop router `<GATEWAY_IP>` on `<IFACE>`. | **Engine 2/6/15/19 Consensus Action** when `<TARGET_IP>` is in a disjoint subnet (`C2_CROSS_SUBNET_L3_PIVOT`) reachable via `<GATEWAY_IP>`. | `route add <REMOTE_SUBNET> mask 255.255.255.0 <GATEWAY_IP>` |
| `sudo sysctl -w net.ipv4.ip_forward=1` | Enables IPv4 packet forwarding across interfaces in the Linux kernel (`0 -> 1`). | **Apply on any dual-homed pivot host or router appliance** when transit packets between subnets are being dropped (`Pivot_IP_Forward_Sysctl`). | `Set-NetIPInterface -Forwarding Enabled` |
| `sudo sysctl -w net.ipv4.conf.all.rp_filter=0 net.ipv4.conf.default.rp_filter=0` | Disables strict Reverse Path Filtering (`rp_filter`) so asymmetric cross-subnet routes are not silently dropped by the kernel. | **Apply when asymmetric routing is suspected** (`asymmetric_missing_return_route_or_nat` in `Engine 4`). | `netsh interface ipv4 set global sourceroutingbehavior=forward` |
| `sudo sysctl -w net.ipv4.conf.all.proxy_arp=1` | Enables Proxy ARP so the router answers ARP requests on behalf of hosts on another interface. | Apply when bridging disjoint L2 segments that share an overlapping IPv4 prefix without changing host gateways. | `netsh interface ipv4 set interface <Idx> arpproxy=enabled` |

---

## 4. L4 Sockets (`ss`), Listening Services & Process-to-Socket Attribution (`Passive_Enum`)

| Linux Command | Description & Key Flags | When to Apply & Expected Output | Windows Equivalent |
| :--- | :--- | :--- | :--- |
| `ss -tulpn` | Lists all TCP (`-t`) and UDP (`-u`) listening (`-l`) sockets with numerical ports (`-n`) and owning process/PID (`-p`). | **Primary Linux L4 socket discovery command**: identifies whether a service is listening on `0.0.0.0:*`, `[::]:*`, or bound exclusively to `127.0.0.1` (`service_bound_to_loopback`). | `netstat -abno` |
| `ss -tanp` | Lists all TCP sockets in all states (`LISTEN`, `ESTAB`, `SYN-SENT`, `TIME-WAIT`) with process PIDs and send/recv queue sizes. | Apply to spot active outbound connections, stuck `SYN-SENT` handshakes (firewall drop), or non-zero Recv-Q (hung daemon). | `netstat -ano -p tcp` |
| `sudo lsof -i -P -n` | Lists all open network files/sockets (`-i`) with raw port numbers (`-P`), numeric IPs (`-n`), user, PID, and binary name. | Apply to cross-verify socket ownership or find processes holding raw/packet sockets (`SOCK_RAW`). | `tcpvcon -a -c -n` |
| `sudo fuser -v 80/tcp 443/tcp 8080/tcp` | Identifies the exact PID, user, and command bound to specific TCP ports. | Apply before restarting a web/API daemon or resolving `Address already in use` conflicts. | `Get-NetTCPConnection -LocalPort 80,443,8080` |
| `resolvectl status \|\| cat /etc/resolv.conf /etc/hosts` | Displays active DNS resolvers, search domains, and local `/etc/hosts` static hostname mappings. | Apply when diagnosing hostname resolution failures (`[[commands/trained_cqc001_e050_m060_network_and_name_resolution]]`). | `ipconfig /all && type C:\Windows\System32\drivers\etc\hosts` |

---

## 5. Host Firewalls (`iptables`, `nftables`, `ufw`) & NAT Masquerading (`Defense_Evasion_Firewall`)

| Linux Command | Description & Key Flags | When to Apply & Expected Output | Windows Equivalent |
| :--- | :--- | :--- | :--- |
| `sudo iptables -L -n -v --line-numbers && sudo iptables -t nat -L -n -v` | Lists all `filter` (`INPUT`, `FORWARD`, `OUTPUT`) and `nat` (`PREROUTING`, `POSTROUTING`) rules with packet/byte counters (`-v`), numeric IPs (`-n`), and rule numbers. | **Apply whenever connections time out (`Exit 28`) or return `ICMP Administratively Prohibited`** (`[[commands/trained_iptables-snort-cmds]]`): non-zero packet counters on a `DROP`/`REJECT` rule prove the firewall is blocking traffic! | `netsh advfirewall firewall show rule name=all` |
| `sudo nft list ruleset` | Dumps the complete `nftables` ruleset (tables, chains, sets, counters, NAT hooks) on modern Debian/Ubuntu/RHEL kernels. | **Always run alongside `iptables -L`** on modern Linux kernels where `nftables` may drop packets independently of legacy `iptables`. | `Get-NetFirewallRule -Enabled True` |
| `sudo iptables -I INPUT 1 -p tcp --dport <PORT> -j ACCEPT && sudo iptables -I FORWARD 1 -j ACCEPT` | Inserts (`-I ... 1`) a top-priority allow rule at the head of `INPUT` and `FORWARD` chains so subsequent `DROP` rules are bypassed. | **Apply when unlocking a firewalled service (`s_oob_serial_enumerated -> s_firewall_or_acl_unlocked`)** discovered via OOB serial or local shell. | `netsh advfirewall firewall add rule name="AllowPort" dir=in action=allow protocol=TCP localport=<PORT>` |
| `sudo iptables -t nat -A POSTROUTING -s <LOCAL_SUBNET> -d <REMOTE_SUBNET> -o <OUT_IFACE> -j MASQUERADE` | Appends a Source NAT (`MASQUERADE`) rule on `<OUT_IFACE>` so traffic routed to `<REMOTE_SUBNET>` appears to originate from the pivot router's own IP. | **Engine 6/15/19 Consensus Fix when downstream target lacks a return route** (`Return_Route_Or_MASQUERADE`): solves asymmetric routing blackholes immediately without touching the remote host! | `New-NetNat -Name "PivotNAT" -InternalIPInterfaceAddressPrefix <LOCAL_SUBNET>` |
| `sudo iptables -t nat -A PREROUTING -p tcp --dport 8443 -j REDIRECT --to-ports 8080` (with `route_localnet=1`) | Redirects external TCP port `8443` traffic to a loopback-bound service on `127.0.0.1:8080`. | Apply when a web/API daemon on an appliance is bound only to `127.0.0.1:8080` and `socat` is unavailable. | `netsh interface portproxy add v4tov4 listenport=8443 connectaddress=127.0.0.1 connectport=8080` |

---

## 6. Processes, Signals, `/proc` Forensics, `systemd` Services & Cron (`Passive_Enum`)

| Linux Command | Description & Key Flags | When to Apply & Expected Output | Windows Equivalent |
| :--- | :--- | :--- | :--- |
| `ps auxef` / `ps -eo pid,ppid,user,stat,lstart,args --forest` | Displays full process hierarchy (`--forest`), UID, PID, PPID, start timestamp, environment (`e`), and full command line (`[[commands/trained_cqc001_e050_m050_process_and_signals]]`). | **Apply during every Linux live response** to spot abnormal child processes (e.g., `sh -i` spawned by `nginx`/`apache2`/`python`) or processes running from `/tmp` or `/dev/shm`. | `wmic process get ProcessId,ParentProcessId,ExecutablePath,CommandLine` |
| `sudo ls -la /proc/<PID>/exe /proc/<PID>/cwd /proc/<PID>/fd && tr '\0' ' ' < /proc/<PID>/environ` | Inspects the actual binary symlink (`exe`, including `(deleted)` unlinked binaries!), working directory (`cwd`), open file descriptors (`fd`), and environment variables (`environ`) in `/proc`. | **Essential Linux memory forensics technique**: even if a malware binary deleted itself from disk (`/tmp/bot (deleted)`), `/proc/<PID>/exe` still points to the in-memory inode and can be copied with `cp /proc/<PID>/exe /tmp/recovered_bin`! | `handle -a -p <PID> && listdlls <PID>` |
| `sudo strace -f -p <PID> -e trace=network,file,process -s 256` | Traces system calls (`connect`, `bind`, `openat`, `execve`) of process `<PID>` and its children (`-f`), capturing up to 256 bytes of string arguments (`-s 256`). | Apply when reverse-engineering or debugging a live daemon to see what config files, sockets, or credentials it accesses in real time. | `procmon` / `procdump` |
| `systemctl list-units --type=service --state=running` | Lists all active `systemd` services and their descriptions (`[[commands/trained_cqc001_e050_m040_boot_init_login]]`). | Apply to inventory active daemons and identify custom or non-standard services. | `sc query state= active` |
| `systemctl status <service> --no-pager -l && systemctl cat <service>` | Shows service PID, recent journal logs, and the exact unit file path and `ExecStart=` command (`systemctl cat`). | Apply to inspect how a daemon is launched, which user it runs as (`User=`), and whether its unit file or script is writable. | `sc qc <ServiceName>` |
| `crontab -l; ls -la /etc/crontab /etc/cron.* /var/spool/cron/crontabs; systemctl list-timers --all` | Audits all user and system scheduled cron jobs and `systemd` timers. | Apply to detect scheduled persistence or periodic root scripts executing writable binaries. | `schtasks /query /fo LIST /v` |

---

## 7. Users, Permissions, SUID/SGID, Linux Capabilities, `sudo` & TTY Shell Upgrade (`Privilege_Escalation`)

| Linux Command | Description & Key Flags | When to Apply & Expected Output | Windows Equivalent |
| :--- | :--- | :--- | :--- |
| `sudo -l` | Lists commands the current user is permitted to run via `sudo` (including `NOPASSWD:` entries and `env_keep+=LD_PRELOAD`). | **First command to run for Linux Privilege Escalation** (`s_initial_shell_or_api_access -> s_interactive_tty_or_priv_escalated`). | `whoami /priv` |
| `find / -perm -4000 -type f -exec ls -la {} + 2>/dev/null` | Searches the entire filesystem for SUID (`-perm -4000`) binaries (use `-perm -2000` for SGID) and suppresses permission errors (`2>/dev/null`). | **Apply during privilege escalation survey** (`[[commands/trained_cqc001_e060_m010_users_and_permissions]]`): identifies custom or GTFOBins SUID binaries (`python3`, `find`, `vim`, `bash`, `nmap`, `cp`). | `accesschk -accepteula -uwcqv *` |
| `getcap -r / 2>/dev/null` | Recursively scans `/` for binaries granted POSIX Linux Capabilities (e.g., `cap_setuid+ep`, `cap_net_raw+ep`, `cap_dac_read_search+ep`). | **Critical modern Linux privesc check**: a binary with `cap_setuid+ep` (like `python3` or `perl`) grants instant root (`uid=0`) even without the SUID bit set! | `whoami /priv` |
| `find / -writable -type f \( -path "/etc/*" -o -path "/usr/*" -o -path "/opt/*" \) 2>/dev/null` | Finds world-writable or group-writable configuration files, scripts, or service units in `/etc`, `/usr`, and `/opt`. | Apply to discover writable `systemd` unit files, `/etc/passwd`, `/etc/sudoers.d/`, or cron scripts. | `icacls "C:\Program Files\*"` |
| `python3 -c 'import pty; pty.spawn("/bin/bash")'` or `script -qc /bin/bash /dev/null` | Spawns a pseudo-terminal (`PTY`) interactive `/bin/bash` shell inside a dumb netcat/reverse shell (`[[knowledge/trained_upgrading_shells_to_fully_interactive_ttys]]`). | **Apply whenever a shell lacks job control or rejects `su`/`sudo`/`ssh` with `must be run from a terminal`**. Follow with `Ctrl+Z`, `stty raw -echo; fg`, `export TERM=xterm-256color`. | `Enter-PSSession` |

---

## 8. Filesystems, Mounts, Forensic Search & Log Auditing (`Passive_Enum`)

| Linux Command | Description & Key Flags | When to Apply & Expected Output | Windows Equivalent |
| :--- | :--- | :--- | :--- |
| `df -hT && lsblk -f && findmnt` | Displays mounted filesystems, filesystem types (`ext4`, `xfs`, `tmpfs`, `nfs`), block device UUIDs, and mount options (`ro`, `noexec`, `nosuid`). | Apply when checking disk space, locating unmounted partitions, or verifying if `/tmp` or `/dev/shm` is mounted `noexec` (`[[knowledge/trained_cqc001_e050_m030_filesystems]]`). | `fsutil fsinfo drives && wmic logicaldisk get DeviceID,FileSystem,FreeSpace,Size` |
| `find / -xdev -mtime -2 -type f -ls 2>/dev/null` | Finds all files on the root filesystem (`-xdev`) modified within the last 48 hours (`-mtime -2`). | Apply during incident response to identify newly dropped web shells, configs, or staging files (`[[commands/trained_find]]`). | `forfiles /p C:\ /s /d -2` |
| `grep -rnI -iE "password\|passwd\|secret\|api_key\|bearer\|private_key" /etc /var/www /opt /home 2>/dev/null` | Recursive (`-r`), line-numbered (`-n`), non-binary (`-I`) regex search for credentials and tokens across config and web directories. | Apply during post-exploitation credential harvesting (`s_active_services_enumerated -> s_credentials_or_certs_acquired`). | `findstr /s /i /n "password secret" C:\*.config C:\*.ini` |
| `journalctl -xe --no-pager -n 100` / `journalctl -u <service> --since "1 hour ago" --no-pager` | Queries `systemd-journald` binary logs for recent system errors or service-specific output (`[[commands/trained_logging-cmds]]`). | Apply when troubleshooting daemon startup failures, authentication errors, or crash traces. | `wevtutil qe System /c:50 /rd:true /f:text` |
| `sudo grep -E "Accepted\|Failed\|Invalid\|sudo\|session opened" /var/log/auth.log /var/log/secure 2>/dev/null \| tail -n 50` | Extracts recent SSH logins, failed brute-force attempts, and `sudo` command executions on Debian/Ubuntu (`auth.log`) and RHEL/CentOS (`secure`). | Apply to audit authentication history and trace lateral movement (`[[knowledge/trained_cqc001_e060_m020_unix_logging]]`). | `wevtutil qe Security /q:"*[System[(EventID=4624 or EventID=4625)]]"` |

---

## 9. Packet Capture (`tcpdump`, `tshark`), BPF Syntax & Passive Fingerprinting (`p0f`)

| Linux Command | Description & Key Flags | When to Apply & Expected Output | Windows Equivalent |
| :--- | :--- | :--- | :--- |
| `sudo tcpdump -ni <IFACE> -c 50 -nn -e 'arp or icmp'` | Captures 50 packets (`-c 50`) on `<IFACE>` without DNS/port translation (`-nn`), printing L2 Ethernet MAC headers (`-e`) for ARP and ICMP traffic. | **Apply when diagnosing L2 ARP resolution or L3 ICMP blackholes** (`[[commands/trained_bpf_syntax]]`): proves whether replies arrive on the wire. | `pktmon start --capture --comp nics` |
| `sudo tcpdump -ni <IFACE> -nn 'tcp[tcpflags] & (tcp-syn\|tcp-rst) != 0 and host <TARGET_IP>'` | Uses Berkeley Packet Filter (`BPF`) byte-offset masking on the TCP flags byte (`tcp[13]`) to capture only `SYN`, `SYN-ACK`, and `RST` packets for `<TARGET_IP>`. | **Apply to distinguish silent firewall drops (`SYN` sent, 0 replies) from closed ports (`RST-ACK` received)** (`[[knowledge/trained_jstebelton_bpf-syntax]]`). | `tshark -i <IFACE> -f "host <TARGET_IP> and tcp[tcpflags] & (tcp-syn\|tcp-rst) != 0"` |
| `sudo tcpdump -ni <IFACE> -s0 -G 300 -W 1 -w /tmp/capture_%Y%m%d_%H%M%S.pcap` | Captures full-sized frames (`-s0`) for 300 seconds (`-G 300 -W 1`) into a standard `.pcap` file (`[[commands/trained_capture_sh]]`). | Apply to record raw network traffic for deep protocol analysis in `tshark` or `Wireshark`. | `netsh trace start capture=yes tracefile=C:\Temp\capture.etl` |
| `tshark -r /tmp/capture.pcap -Y "http.request or tls.handshake.type == 1 or dns.qry.name" -T fields -e ip.src -e ip.dst -e http.host -e tls.handshake.extensions_server_name -e dns.qry.name` | Extracts source IP, destination IP, HTTP `Host`, TLS SNI (`Server Name Indication`), and DNS query names from a `.pcap` file (`[[knowledge/trained_cqc001_e010_m030_wireshark_display_filters]]`). | Apply for fast CLI extraction of clear-text and TLS SNI metadata from packet captures. | `tshark.exe -r C:\Temp\capture.pcap -Y "http.request or tls.handshake.type == 1"` |
| `sudo p0f -i <IFACE>` / `p0f -r /tmp/capture.pcap` | Passively fingerprints remote OS, kernel family, uptime, and link MTU from TCP `SYN`/`SYN-ACK` window size, TTL, and TCP options ordering (`[[knowledge/trained_cqc001_e010_m040_p0f]]`). | **Apply in `WHITE`/`BLUE` stealth or passive monitoring scenarios** to identify remote OS types with zero active packets transmitted. | `p0f.exe -r capture.pcap` |

---

## 10. Active Reconnaissance (`nmap`), Web/API/mTLS Probing (`curl`) & Serial OOB (`tio`)

| Linux Command | Description & Key Flags | When to Apply & Expected Output | Windows Equivalent |
| :--- | :--- | :--- | :--- |
| `nmap -sn -PE -PP -PS22,80,443,445,3389,8080,8443 <SUBNET_CIDR>` | Performs fast host discovery sweep (`-sn`) combining ICMP Echo, Timestamp, and TCP SYN probes across common enterprise ports. | Apply to discover live hosts across a local or routed subnet (`s_l2_l3_verified -> s_active_services_enumerated`). | `nmap.exe -sn <SUBNET_CIDR>` |
| `nmap -sV -sC -Pn -T4 -p 22,80,443,445,3389,5985,8000,8080,8443,10443 <TARGET_IP>` | Probes key management/API ports skipping ping (`-Pn`), extracting service banners (`-sV`) and default NSE scripts (`-sC`, including TLS cert & HTTP title). | **Primary active service & appliance identification probe** (`Engine 4/15`). | `nmap.exe -sV -sC -Pn <TARGET_IP>` |
| `curl -sS -k -L -i --max-time 15 "https://<TARGET_IP>:8443/"` | Fetches HTTP response headers (`-i`) and body, following redirects (`-L`), allowing self-signed appliance certs (`-k`), with a 15s timeout (`[[commands/curl_playbook]]`). | **Apply when probing web servers, REST APIs, or firewall management GUIs** (e.g., FortiGate, pfSense, OpenWrt). | `curl.exe -sS -k -L -i --max-time 15 "https://<TARGET_IP>:8443/"` |
| `echo \| openssl s_client -connect <TARGET_IP>:443 -servername <TARGET_IP> 2>/dev/null \| openssl x509 -noout -subject -issuer -dates -serial -ext subjectAltName` | Extracts the X.509 TLS certificate `Subject` (`CN`, hardware serial number on Fortinet/Cisco appliances!), `Issuer`, validity dates, and `SAN` hostnames. | **High-signal appliance identification technique**: Fortinet FortiGate certificates embed the exact model and hardware serial number (e.g., `CN = FG100F...`) in the TLS certificate `Subject`! | `openssl.exe s_client -connect <TARGET_IP>:443` |
| `tio -b 115200 -o 15 -O 120 --mute --script-run once --script 'write("\r"); msleep(400); while read(4096, 600) > 0 do end; exit(0)' /dev/ttyUSB0` | Wakes and reads the out-of-band hardware UART console on `/dev/ttyUSB0` with anti-drop pacing (`-o 15 -O 120`) and exits cleanly (`[[commands/tio_serial_playbook]]`). | **Engine 1/4/6/15/19 Consensus OOB Pivot (`C1_OOB_SERIAL_LOOPBACK_APPLIANCE`)** when TCP/HTTP probes to `<TARGET_IP>` fail with `Connection refused (Exit 7)` or timeout (`Exit 28`). | `plink.exe -serial COM1 -sercfg 115200,8,n,1,N` |
