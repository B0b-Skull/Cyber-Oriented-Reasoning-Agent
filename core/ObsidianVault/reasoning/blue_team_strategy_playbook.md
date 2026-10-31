---
title: blue_team_strategy_playbook
category: reasoning
engine: team_strategy_arbiter
team_role: blue_team
os_platform: cross-platform
domain_hub: "[[knowledge/03_windows_security_acls_auditing_and_logs]]"
primary_tactic: Defense_Evasion_Firewall
summary: "Blue Team Defensive Strategy & Incident Containment Playbook: attack-surface hardening, firewall/ACL lockdown, audit policy enforcement, service/registry integrity verification, and host containment across Windows and Linux."
when_to_apply: "Apply when the operator or goal requires defensive security, system hardening, firewall rule enforcement, ACL/permission lockdown, audit policy configuration, vulnerability mitigation, or incident containment, eradication, and recovery on Windows or Linux."
tags: [reasoning, blue_team, blue-team, defensive-security, hardening, incident-response, containment, eradication, firewall, acl, auditpol, wevtutil, icacls, netsh, iptables, nftables, sysctl, windows, linux]
updated: 2026-10-30 23:42:00
---
# Blue Team Strategy & Defensive Operations Playbook (`blue_team_strategy_playbook`)

> **Team Role:** `BLUE_TEAM` (Defensive Security, Hardening & Incident Containment)  
> **Primary H-MDP Tactics:** `Passive_Enum` $\to$ `Defense_Evasion_Firewall` $\to$ `Post_Exploitation_Verification`  
> **Recommended Console Posture:** `BLUE` (Interface-Locked Isolation) or `WHITE` (Air-Gapped Namespace) | **Modes:** `Standard` / `Analyst`  
> **Backlinks:** [[00_MEMORY_INDEX]] | [[commands/windows_master_command_playbook]] | [[commands/linux_master_command_playbook]] | [[knowledge/03_windows_security_acls_auditing_and_logs]] | [[knowledge/05_windows_and_linux_networking_routing_and_firewalls]]

---

## 1. When Engines & LLM Must Activate This Playbook
Activate `[[reasoning/blue_team_strategy_playbook]]` whenever the query, goal, or system state involves:
- **System & Network Hardening:** Locking down exposed TCP/UDP listeners, restricting firewall rules (`netsh advfirewall`, `nft`, `iptables`), enforcing kernel network protections (`rp_filter`, `tcp_syncookies`), or disabling unnecessary services/protocols (SMBv1, LLMNR, NetBIOS, WDigest).
- **Access Control & Privilege Lockdown:** Fixing permissive file/directory/service ACLs (`icacls`, `takeown`, `accesschk64.exe`, `chmod`, `chown`, `setfacl`), auditing privileged groups (`Administrators`, `Domain Admins`, `sudo`/`wheel`), or removing unauthorized SUID/capabilities (`getcap`).
- **Telemetry & Audit Enforcement:** Enabling Windows Security Audit subcategories (`auditpol`), PowerShell ScriptBlock/Module logging, Sysmon, or Linux `auditd`/`journald` rules.
- **Incident Containment & Eradication:** Isolating compromised interfaces, blocking malicious IPs/subnets, terminating rogue processes, disabling malicious scheduled tasks/services/Run keys, and verifying system recovery.

---

## 2. 15-Engine Neuro-Symbolic Alignment for Blue Team Operations
| Engine Layer | Engine Name | Blue Team Strategic Role & Decision Rule |
| :--- | :--- | :--- |
| **Layer 0** | **Engine 1 (`associative`) & Engine 9 (`temporal_fluents`)** | Prioritize `[[knowledge/03_windows_security_acls_auditing_and_logs]]`, `[[knowledge/05_windows_and_linux_networking_routing_and_firewalls]]`, and track live baseline fluents (`listening_ports`, `firewall_profile_state`, `audit_policy_enabled`). |
| **Layer 1** | **Engine 2 (`geometric`) & Engine 12 (`cegar_verifier`)** | Verify that firewall CIDR blocks do not sever management interfaces (`BLUE` allowed NICs) and block any destructive command lacking explicit target scope. |
| **Layer 2** | **Engine 4 (`bayesian`), Engine 5 (`causal`) & Engine 10 (`dempster_shafer`)** | Rank root causes of exposure or service failure; use Pearl's `do(ChokePoint=0)` on Causal DAGs to identify the single-node cut-set (`TCP_SYN_ACK_Handshake`, `Target_Firewall_Allow`) that neutralizes an attack path with minimal collateral impact. |
| **Layer 3/4** | **Engine 15 (`mdp_tactical`) & Engine 19 (`rl_network_policy`)** | Prioritize `Passive_Enum` (baseline audit) $\to$ `Defense_Evasion_Firewall` (rule enforcement) $\to$ `Post_Exploitation_Verification` (confirm port closed / ACL enforced). |
| **Layer 5** | **Engine 17 (`meta_learner`) & Engine 20 (`spectral_manifold_pca`)** | Use Mahalanobis distance ($D_M$) to verify that post-remediation host telemetry returns to the `MANIFOLD_INLIER` baseline. |

---

## 3. Concise 5-Phase Blue Team Operational Playbook (Windows & Linux)

### Phase 1: Attack Surface & Listening Service Baseline (`Passive_Enum`)
| Objective | Windows Command (`CMD` / `PowerShell`) | Linux Command (`Bash`) | What to Verify |
| :--- | :--- | :--- | :--- |
| **Audit Listening Sockets & Owning PIDs** | `netstat -anob` *(or)* `powershell -NoProfile -Command "Get-NetTCPConnection -State Listen,Established \| Select-Object LocalAddress,LocalPort,RemoteAddress,RemotePort,State,OwningProcess"` | `ss -tulpn && ss -tanpi` | Identify unexpected listeners bound to `0.0.0.0` / `::` and map each socket to its binary and PID. |
| **Audit Running & Auto-Start Services** | `powershell -NoProfile -Command "Get-CimInstance Win32_Service \| Where-Object {$_.State -eq 'Running'} \| Select-Object Name,DisplayName,StartMode,StartName,PathName"` | `systemctl list-units --type=service --state=running --no-pager` | Detect non-standard service binaries, writable paths, or services running as `LocalSystem`/`root` unnecessarily. |
| **Verify Digital Signatures of Autostarts** | `autorunsc64.exe -a * -c -h -s -v -nobanner` | `rpm -Va` *(RHEL)* or `debsums -s` *(Debian/Ubuntu)* | Flag unsigned binaries, missing publisher certificates, or modified package binaries. |

### Phase 2: Firewall, Network Segmentation & Stack Hardening (`Defense_Evasion_Firewall`)
| Objective | Windows Command (`CMD` / `PowerShell`) | Linux Command (`Bash`) | What to Verify |
| :--- | :--- | :--- | :--- |
| **Inspect Active Firewall Posture** | `netsh advfirewall show allprofiles` | `sudo nft list ruleset` *(or)* `sudo iptables -L -n -v --line-numbers` | Confirm firewall is `ON` across Domain/Private/Public profiles and default inbound policy is restrictive. |
| **Block Unauthorized Inbound Port / IP** | `netsh advfirewall firewall add rule name="Block_Threat_IP" dir=in action=block remoteip=<ATTACKER_IP>` | `sudo nft add rule inet filter input ip saddr <ATTACKER_IP> drop` *(or)* `sudo iptables -I INPUT 1 -s <ATTACKER_IP> -j DROP` | Immediately drop inbound traffic from malicious source IP or to an unauthorized port. |
| **Audit & Remove Rogue Port Proxies / NAT** | `netsh interface portproxy show all` *(remove via `delete v4tov4 listenport=<PORT> listenaddress=<IP>`)* | `sudo iptables -t nat -L -n -v --line-numbers` | Detect and remove adversary `portproxy` or `MASQUERADE`/`DNAT` pivot rules. |
| **Harden Kernel Network Stack** | `powershell -NoProfile -Command "Set-SmbServerConfiguration -EnableSMB1Protocol $false -Force"` | `sudo sysctl -w net.ipv4.conf.all.rp_filter=1 net.ipv4.tcp_syncookies=1 net.ipv4.conf.all.accept_redirects=0` | Disable legacy SMBv1 on Windows; enforce reverse-path filtering, SYN cookies, and ICMP redirect rejection on Linux. |

### Phase 3: Identity, Privilege, File ACL & Credential Hardening (`Enumeration` / `Defense_Evasion_Firewall`)
| Objective | Windows Command (`CMD` / `PowerShell`) | Linux Command (`Bash`) | What to Verify |
| :--- | :--- | :--- | :--- |
| **Audit Administrative Group Memberships** | `net localgroup administrators` | `getent group sudo wheel adm root` | Verify only authorized accounts hold local or domain administrative privileges. |
| **Audit & Lock Down Sensitive File ACLs** | `icacls "C:\ProgramData\App" /inheritance:d /remove:g "Users" "Everyone"` | `chmod 600 /etc/shadow /etc/ssh/sshd_config && chown root:root /etc/shadow` | Remove write/modify (`(M)`, `(F)`, `(W)`) permissions for `Everyone`/`Users`/`Authenticated Users` on service directories. |
| **Audit Service Permissions & SUID/Capabilities** | `accesschk64.exe -uwcqv "Authenticated Users" * /accepteula` | `find / -perm -4000 -type f 2>/dev/null && getcap -r / 2>/dev/null` | Ensure non-admin users cannot reconfigure services (`SERVICE_CHANGE_CONFIG`) or abuse SUID/capabilities. |
| **Enforce Credential Guard / LSA Protection** | `reg add "HKLM\SYSTEM\CurrentControlSet\Control\Lsa" /v RunAsPPL /t REG_DWORD /d 1 /f && reg add "HKLM\SYSTEM\CurrentControlSet\Control\SecurityProviders\WDigest" /v UseLogonCredential /t REG_DWORD /d 0 /f` | `sudo sshd -T \| grep -E "permitrootlogin\|passwordauthentication\|pubkeyauthentication"` | Protect `lsass.exe` as Protected Process Light (`RunAsPPL=1`), disable cleartext `WDigest` caching, and enforce key-based SSH. |

### Phase 4: Audit Policy & Security Telemetry Enforcement (`Passive_Enum`)
| Objective | Windows Command (`CMD` / `PowerShell`) | Linux Command (`Bash`) | What to Verify |
| :--- | :--- | :--- | :--- |
| **Inspect Active Audit Policy** | `auditpol /get /category:*` | `sudo auditctl -l && sudo auditctl -s` | Identify silent telemetry gaps where `No Auditing` is set on Logon, Process Creation, or Privilege Use. |
| **Enable Process Command-Line & Logon Auditing** | `auditpol /set /subcategory:"Process Creation" /success:enable /failure:enable && reg add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System\Audit" /v ProcessCreationIncludeCmdLine_Enabled /t REG_DWORD /d 1 /f` | `sudo auditctl -a always,exit -F arch=b64 -S execve -k proc_exec` | Ensure Event ID `4688` (with full command line) on Windows and `EXECVE` syscall logging on Linux are active. |
| **Verify Log Capacity & Integrity** | `wevtutil gl Security` | `journalctl --disk-usage && ls -lh /var/log/audit/audit.log` | Ensure Security/audit logs are not full, wrapped, or disabled. |

### Phase 5: Incident Containment, Eradication & Verification (`Post_Exploitation_Verification`)
| Objective | Windows Command (`CMD` / `PowerShell`) | Linux Command (`Bash`) | What to Verify |
| :--- | :--- | :--- | :--- |
| **Terminate Malicious Process Tree** | `taskkill /F /T /PID <MALICIOUS_PID>` | `sudo kill -9 <MALICIOUS_PID>` | Stop active C2 beacon or unauthorized child process tree immediately. |
| **Disable Rogue Service or Scheduled Task** | `sc.exe stop "<SVC>" && sc.exe config "<SVC>" start= disabled` *(or)* `schtasks /Change /TN "<TASK>" /Disable` | `sudo systemctl disable --now <rogue.service> && sudo rm -f /etc/systemd/system/<rogue.service> && sudo systemctl daemon-reload` | Prevent persistence mechanism from respawning after process termination. |
| **Verify Containment & Clean State** | `netstat -ano \| findstr <PORT_OR_IP>` | `ss -tanp \| grep <PORT_OR_IP>` | Confirm zero remaining active sockets to the threat actor endpoint (`s_goal_verified_complete`). |
