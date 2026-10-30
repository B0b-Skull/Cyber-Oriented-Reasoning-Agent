---
title: rl_network_policy_playbooks
category: reasoning
engine: rl_network_policy
summary: Engine 19 TD(lambda) RL Policy (1200 eps, Avg Return +40.2, 55.54 ms)
tags: [reasoning, rl_network_policy, reinforcement-learning, td-lambda, network-topology, next-step-policy]
updated: 2026-10-28 21:17:53
---
# rl_network_policy_playbooks

> **Engine:** `rl_network_policy` | **Summary:** Engine 19 TD(lambda) RL Policy (1200 eps, Avg Return +40.2, 55.54 ms)  
> **Backlink:** [[00_MEMORY_INDEX]] | **Updated:** `2026-10-28 21:17:53`

### Engine 19: Converged Trajectory RL (`TD(lambda)` + UCB1) & Live Network World-Model Playbooks
- **Total Digital-Twin RL Episodes Trained**: **`1200`** (`4` live CLI transitions | Avg Return = **`+40.24`**)
- **RL Hyperparameters**: Discount $\gamma = 0.92$, Eligibility Trace $\lambda = 0.85$, Learning Rate $\alpha = 0.18$, UCB1 $c = 1.45$
- **Live Host Network Snapshot (`[[targets/local_network_topology]]`)**: Primary NIC `<PRIMARY_NIC>`, Local Subnets `['<LOCAL_SUBNET>/24']`, Default GW `<GATEWAY_IP>`, Reachable L2 ARP Neighbors = `0`, IPv4 Forwarding = `False`

#### 1. Active State 3-Step Optimal Trajectory Rollout ($\pi^*(s_t)$)
| Step | Network Stage ($s_t$) | Optimal Action ($a_t^*$) | Learned $Q^*(s,a)$ | Concrete Next Command |
| :---: | :--- | :--- | :---: | :--- |
| **1** | `STAGE_4_BYPASS_ICMP_PORT_SCAN` | **No-Ping (-Pn) TCP Service Port Discovery Scan** (`L4_Transport_TCP`) | `+31.93` | `powershell -NoProfile -Command "22,80,443,8080 | ForEach-Object { Test-NetConnection -ComputerName <TARGET_IP> -Port $_ -WarningAction SilentlyContinue }"` |
| **2** | `STAGE_6_L7_SERVICE_GOAL_VERIFY` | **Execute Verified L7 HTTP/API Endpoint Request** (`L7_Application_Goal`) | `+23.00` | `curl.exe -sS -k -L -i --max-time 10 http://<TARGET_IP>/` |

#### 2. Converged Policy Lookup Table Across All 7 Network Prerequisite Stages
| Prerequisite Stage | Highest-$Q^*(s,a)$ Action ID | Converged $Q^*(s,a)$ | Verified Command Template |
| :--- | :--- | :---: | :--- |
| `STAGE_0_UNMAPPED_LOCAL_NET` | `A0_ENUM_IFACES_AND_ARP` (Map Local Interfaces, Subnets, Routes & ARP Cache) | `+44.46` | `ipconfig /all & route print -4 & arp -a` |
| `STAGE_1_L2_NEIGHBOR_DISCOVERY` | `A1_PROBE_L2_NEIGHBOR` (Verify Target L2 ARP Reachability & MAC Resolution) | `+40.18` | `ping -n 2 -w 1000 <TARGET_IP> & arp -a <TARGET_IP>` |
| `STAGE_2_OOB_SERIAL_UNLOCK` | `A2_OOB_SERIAL_LUA_PROBE` (Out-of-Band Serial Console Daemon & Socket Inspection) | `+18.50` | `powershell -NoProfile -Command "Get-WmiObject Win32_SerialPort | Select-Object DeviceID,Description"` |
| `STAGE_3_CROSS_SUBNET_L3_ROUTE` | `A3_INJECT_STATIC_ROUTE_AND_FWD` (Inject Cross-Subnet Static Route via Gateway Pivot & Enable IP Forwarding) | `+18.50` | `route add <REMOTE_SUBNET> <GATEWAY_IP>` |
| `STAGE_4_BYPASS_ICMP_PORT_SCAN` | `A4_NMAP_NOPING_TCP_SCAN` (No-Ping (-Pn) TCP Service Port Discovery Scan) | `+31.93` | `powershell -NoProfile -Command "22,80,443,8080 | ForEach-Object { Test-NetConnection -ComputerName <TARGET_IP> -Port $_ -WarningAction SilentlyContinue }"` |
| `STAGE_5_L7_AUTH_OR_HEADER_BYPASS` | `A5_HTTP_AUTH_HEADER_PROBE` (HTTP OPTIONS Method & Local-Trust Header Bypass Probe) | `+18.50` | `curl.exe -sS -k -i -X OPTIONS http://<TARGET_IP>/ -H "X-Forwarded-For: 127.0.0.1"` |
| `STAGE_6_L7_SERVICE_GOAL_VERIFY` | `A6_CURL_L7_ENDPOINT_VERIFY` (Execute Verified L7 HTTP/API Endpoint Request) | `+23.00` | `curl.exe -sS -k -L -i --max-time 10 http://<TARGET_IP>/` |
