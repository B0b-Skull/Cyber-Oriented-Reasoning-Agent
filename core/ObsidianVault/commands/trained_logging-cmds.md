---
title: "Trained Command Playbook: Logging-CMDs.txt"
tags:
  - defense_evasion_firewall
  - enumeration
  - mdp
  - netstat
  - passive_enum
  - post_exploitation_verification
  - reconnaissance
  - text
  - trained
source_file: Logging-CMDs.txt
updated: 2026-10-24 00:58:52
---

# Trained Command Playbook: `Logging-CMDs.txt`

- **Source Document:** `~/Projects/CORA/Training/Logging-CMDs.txt`
- **CEGAR Verified Commands:** `27` (`0` malformed/unsafe snippets filtered)
- **MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`):** `27`
- **Discovered IPs/Subnets:** `172.24.11.13`
- **Discovered Interfaces:** `None`
- **Related Knowledge Note:** [[knowledge/trained_logging-cmds]]

## Distilled MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`)
| Pre-State ($s$) | Tactic ($\tau$) | Technique ($k$) | Tool ($u$) | Post-State ($s'$) | Verified Command ($c$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `ps` | `s_passive_topology_mapped` | `ps -ef \| grep syslog` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `vi` | `s_active_services_enumerated` | `vi /etc/sysconfig/syslog` |
| `s_init_unknown` | **`Reconnaissance`** | Domain, DNS, OSINT & Target Footprint Reconnaissance | `echo` | `s_passive_topology_mapped` | `echo 172.24.11.13 linux.ops.local loghost >> /etc/hosts` |
| `s_cross_subnet_pivot_routed` | **`Post_Exploitation_Verification`** | Post-Action Host Identity, Privilege & Objective Verification | `id` | `s_goal_verified_complete` | `id daemon` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `auditctl` | `s_firewall_or_acl_unlocked` | `auditctl -l \| wc -l` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `ls` | `s_passive_topology_mapped` | `ls /etc/syslog*` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `service` | `s_active_services_enumerated` | `service syslog restart` |
| `s_init_unknown` | **`Reconnaissance`** | Domain, DNS, OSINT & Target Footprint Reconnaissance | `svcadm` | `s_passive_topology_mapped` | `svcadm restart system/system-log` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `ausearch` | `s_firewall_or_acl_unlocked` | `ausearch --just-one` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `netstat` | `s_passive_topology_mapped` | `netstat -ulnp` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `service` | `s_active_services_enumerated` | `service auditd restart` |
| `s_init_unknown` | **`Reconnaissance`** | Domain, DNS, OSINT & Target Footprint Reconnaissance | `logger` | `s_passive_topology_mapped` | `logger -p auth.notice tst msg` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `aureport` | `s_firewall_or_acl_unlocked` | `aureport` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `tail` | `s_passive_topology_mapped` | `tail /var/log/messages` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `auditctl` | `s_firewall_or_acl_unlocked` | `auditctl -l` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `svcs` | `s_passive_topology_mapped` | `svcs utmp` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `sestatus` | `s_firewall_or_acl_unlocked` | `sestatus` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `cat` | `s_passive_topology_mapped` | `cat /var/adm/messages \| grep Copyright` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `setenforce` | `s_firewall_or_acl_unlocked` | `setenforce [0:1]` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `cat` | `s_passive_topology_mapped` | `cat /var/log/authlog \| grep console` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `dmesg` | `s_passive_topology_mapped` | `dmesg` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `ps` | `s_passive_topology_mapped` | `ps -C auditd` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `ps` | `s_passive_topology_mapped` | `ps awx\|grep auditd` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `lsof` | `s_passive_topology_mapped` | `lsof -p <PID>` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `tail` | `s_passive_topology_mapped` | `tail -n2 /var/log/messages` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `sed` | `s_passive_topology_mapped` | `sed -i -e '/b64/ s/^/#/' /etc/audit/audit.rules` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `sed` | `s_passive_topology_mapped` | `sed -i -e '/b32/ s/^#//' /etc/audit/audit.rules` |

## Verified Executable Commands (Grouped by Capability Layer)

### General_System (26 commands)
```bash
ps -ef | grep syslog
ls /etc/syslog*
vi /etc/sysconfig/syslog
service syslog restart
echo 172.24.11.13 linux.ops.local loghost >> /etc/hosts
svcadm restart system/system-log
logger -p auth.notice tst msg
tail /var/log/messages
svcs utmp
cat /var/adm/messages | grep Copyright
cat /var/log/authlog | grep console
dmesg
ps -C auditd
id daemon
ps awx|grep auditd
lsof -p <PID>
tail -n2 /var/log/messages
sed -i -e '/b64/ s/^/#/' /etc/audit/audit.rules
sed -i -e '/b32/ s/^#//' /etc/audit/audit.rules
service auditd restart
auditctl -l | wc -l
ausearch --just-one
aureport
auditctl -l
sestatus
setenforce [0:1]
```

### L4_Port_Service (1 commands)
```bash
netstat -ulnp
```

