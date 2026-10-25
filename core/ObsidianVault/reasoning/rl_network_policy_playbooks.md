---
title: rl_network_policy_playbooks
category: reasoning
engine: rl_network_policy
summary: Engine 19 TD(lambda) RL Policy (5200 eps, Avg Return +40.1, 34.86 ms)
tags: [reasoning, rl_network_policy, reinforcement-learning, td-lambda, network-topology, next-step-policy]
updated: 2026-10-25 14:50:17
---
# rl_network_policy_playbooks

> **Engine:** `rl_network_policy` | **Summary:** Engine 19 TD(lambda) RL Policy (5200 eps, Avg Return +40.1, 34.86 ms)  
> **Backlink:** [[00_MEMORY_INDEX]] | **Updated:** `2026-10-25 14:50:17`

### Engine 19: Converged Trajectory RL (`TD(lambda)` + UCB1) & Live Network World-Model Playbooks
- **Total Digital-Twin RL Episodes Trained**: **`5200`** (`52` live CLI transitions | Avg Return = **`+40.08`**)
- **RL Hyperparameters**: Discount $\gamma = 0.92$, Eligibility Trace $\lambda = 0.85$, Learning Rate $\alpha = 0.18$, UCB1 $c = 1.45$
- **Live Host Network Snapshot (`[[targets/local_network_topology]]`)**: Primary NIC `eth0`, Local Subnets `['<LOCAL_SUBNET_A>', '<LOCAL_SUBNET_B>', '198.51.100.0/25', '192.0.2.0/24', '<CONTAINER_BRIDGE>', '198.51.100.128/25']`, Default GW `<LOCAL_SUBNET_A>`, Reachable L2 ARP Neighbors = `4`, IPv4 Forwarding = `True`

#### 1. Active State 3-Step Optimal Trajectory Rollout ($\pi^*(s_t)$)
| Step | Network Stage ($s_t$) | Optimal Action ($a_t^*$) | Learned $Q^*(s,a)$ | Concrete Next Command |
| :---: | :--- | :--- | :---: | :--- |
| **1** | `STAGE_4_BYPASS_ICMP_PORT_SCAN` | **Map Local Interfaces, Subnets, Routes & ARP Cache** (`L1_L2_Host_Discovery`) | `+20.91` | `ip -br addr show && ip route show && ip neigh show` |
| **2** | `STAGE_1_L2_NEIGHBOR_DISCOVERY` | **Verify Target L2 ARP Reachability & MAC Resolution** (`L2_DataLink_ARP`) | `+18.50` | `ip neigh show <TARGET_IP> && ping -c 2 -W 1 <TARGET_IP>` |

#### 2. Converged Policy Lookup Table Across All 7 Network Prerequisite Stages
| Prerequisite Stage | Highest-$Q^*(s,a)$ Action ID | Converged $Q^*(s,a)$ | Verified Command Template |
| :--- | :--- | :---: | :--- |
| `STAGE_0_UNMAPPED_LOCAL_NET` | `A0_ENUM_IFACES_AND_ARP` (Map Local Interfaces, Subnets, Routes & ARP Cache) | `+42.96` | `ip -br addr show && ip route show && ip neigh show` |
| `STAGE_1_L2_NEIGHBOR_DISCOVERY` | `A1_PROBE_L2_NEIGHBOR` (Verify Target L2 ARP Reachability & MAC Resolution) | `+36.90` | `ip neigh show <TARGET_IP> && ping -c 2 -W 1 <TARGET_IP>` |
| `STAGE_2_OOB_SERIAL_UNLOCK` | `A2_OOB_SERIAL_LUA_PROBE` (Out-of-Band Serial Console Daemon & Socket Inspection) | `+18.50` | `tio --script 'write("id\r\nip -br addr\r\nss -tulpn\r\n"); while read(4096, 600) > 0 do end; exit(0)' /dev/ttyUSB0` |
| `STAGE_3_CROSS_SUBNET_L3_ROUTE` | `A3_INJECT_STATIC_ROUTE_AND_FWD` (Inject Cross-Subnet Static Route via Gateway Pivot & Enable IP Forwarding) | `+18.50` | `sudo ip route replace <REMOTE_SUBNET> via <GATEWAY_IP> && sudo sysctl -w net.ipv4.ip_forward=1` |
| `STAGE_4_BYPASS_ICMP_PORT_SCAN` | `A4_NMAP_NOPING_TCP_SCAN` (No-Ping (-Pn) TCP Service Port Discovery Scan) | `+30.23` | `nmap -Pn -sT -p 22,80,443,8080,8443 <TARGET_IP>` |
| `STAGE_5_L7_AUTH_OR_HEADER_BYPASS` | `A5_HTTP_AUTH_HEADER_PROBE` (HTTP OPTIONS Method & Local-Trust Header Bypass Probe) | `+18.50` | `curl -sS -k -i -X OPTIONS http://<TARGET_IP>/ -H 'X-Forwarded-For: 127.0.0.1'` |
| `STAGE_6_L7_SERVICE_GOAL_VERIFY` | `A6_CURL_L7_ENDPOINT_VERIFY` (Execute Verified L7 HTTP/API Endpoint Request) | `+23.00` | `curl -sS -k -L -i --max-time 10 http://<TARGET_IP>/` |
