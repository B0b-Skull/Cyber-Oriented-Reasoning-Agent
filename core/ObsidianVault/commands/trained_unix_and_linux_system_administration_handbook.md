---
title: "Trained Command Playbook: UNIX and Linux System Administration Handbook.pdf"
tags:
  - active_enum
  - arp
  - aws
  - covert_infil
  - credential_access
  - defense_evasion_firewall
  - enumeration
  - eth0
  - eth1
  - http
  - https
  - iptables
  - john
  - kerberos
  - lateral_movement_routing_pivot
  - mdp
  - netstat
  - nmap
  - out-of-band_access
  - passive_enum
  - pdf
  - responder
  - trained
source_file: UNIX and Linux System Administration Handbook.pdf
updated: 2026-10-25 01:01:02
---

# Trained Command Playbook: `UNIX and Linux System Administration Handbook.pdf`

- **Source Document:** `~/Projects/CORA/Training/UNIX and Linux System Administration Handbook.pdf`
- **CEGAR Verified Commands:** `636` (`0` malformed/unsafe snippets filtered)
- **MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`):** `636`
- **Discovered IPs/Subnets:** `0.0.0.0, 0.0.0.0/8, 0.0.0.255, 0.11.25.39, 0.5.0.1, 1.0.0.0/8, 1.174.2.19, 1.189.173.63, 1.2.3.0/24, 1.2.3.13, 1.2.3.25, 1.2.3.4, 1.2.30.40, 1.243.138.128, 1.3.6.1, 1.5.0.11, 1.7.3.4, 10.0.0.0, 10.0.0.0/24, 10.0.0.0/8, 10.0.0.1, 10.0.0.10, 10.1.1.0, 10.1.1.1, 10.1.1.2, 10.1.1.46, 10.1.2.255, 10.1.2.9, 10.114.163.26, 10.16.08.14, 10.2.5.0, 10.231.143.81, 10.231.157.131, 10.231.39.205, 10.231.5.143, 10.255.255.255, 12.2.209.183, 12.28.20.15, 127.0.0.0, 127.0.0.0/8, 127.0.0.1, 127.255.255.255, 128.138.0.0, 128.138.0.0/16, 128.138.101.4, 128.138.116.4, 128.138.129.0/24, 128.138.129.1, 128.138.129.12, 128.138.176.0/20, 128.138.192.192, 128.138.192.55, 128.138.192.64, 128.138.193.0, 128.138.193.32, 128.138.198.0, 128.138.198.0/26, 128.138.198.84, 128.138.2.0, 128.138.2.0/24, 128.138.2.1, 128.138.2.4, 128.138.202.0, 128.138.242.1, 128.138.243.0, 128.138.243.0/24, 128.138.243.0/26, 128.138.243.1, 128.138.243.100, 128.138.243.100/16, 128.138.243.100/24, 128.138.243.100/26, 128.138.243.127, 128.138.243.128, 128.138.243.128/26, 128.138.243.149, 128.138.243.150, 128.138.243.151, 128.138.243.16, 128.138.243.191, 128.138.243.192/26, 128.138.243.255, 128.138.243.64, 128.138.243.64/26, 128.138.255.255, 128.138.92.128/25, 128.9.160.27, 129.132.2.217, 130.225.204.48, 130.225.204.49, 132.236.212.0, 132.236.212.0/26, 132.236.212.1, 132.236.212.6, 132.236.220.64, 132.236.220.64/26, 132.236.227.0, 132.236.227.0/24, 132.236.227.1, 132.236.227.93, 134.122.0.0/16, 134.122.67.124, 137.164.24.174, 137.164.46.119, 137.164.46.7, 169.254.0.0/16, 170.65.3.4, 172.16.0.0, 172.16.0.0/12, 172.16.152.40, 172.16.220.139, 172.16.8.254, 172.29.0.0/24, 172.31.255.255, 174.129.219.225, 175.14.4.1, 187.10.167.249, 192.0.2.0/24, 192.108.21.0, 192.108.21.1, 192.108.21.200, 192.108.21.254, 192.108.21.255, 192.108.21.48, 192.108.21.99, 192.144.0.0, 192.144.0.0/21, 192.144.7.0, 172.24.0.0, 172.24.0.0/16, 172.24.0.1, 172.24.0.12, 172.24.0.2, 172.24.0.255, 172.24.0.3, 172.24.0.75, 172.24.1.0, 172.24.1.0/24, 172.24.1.1, 172.24.1.102, 172.24.1.13, 172.24.1.17, 172.24.1.200, 172.24.1.254, 172.24.1.255, 172.24.1.28, 172.24.1.3, 172.24.1.4/24, 172.24.1.5, 172.24.1.51, 172.24.1.60, 172.24.10.0, 172.24.10.0/24, 172.24.10.10, 172.24.10.10/32, 172.24.10.11, 172.24.10.123, 172.24.10.15, 172.24.10.254, 172.24.10.255, 172.24.123.0/24, 172.24.15.9, 172.24.2.1, 172.24.2.10, 172.24.2.100, 172.24.2.11, 172.24.2.12, 172.24.2.14, 172.24.2.8, 172.24.20.1, 172.24.20.16, 172.24.20.25, 172.24.20.35, 172.24.20.48, 172.24.20.5, 172.24.20.6, 172.24.20.7, 172.24.255.255, 172.24.3.10, 172.24.3.255, 172.24.45.128/25, 172.24.6.17, 172.24.69.1, 172.24.7.120, 172.24.74.3, 172.24.96.107, 172.24.96.108, 172.24.96.197, 172.24.96.198, 172.24.96.43, 172.24.96.88, 172.24.96.92, 172.24.97.203, 192.172.226.32/32, 192.172.226.36/32, 192.172.226.78, 192.172.226.78/32, 192.225.33.254, 192.225.33.5, 192.225.40.253, 192.38.8.0, 192.38.8.129, 198.17.46.56, 198.32.146.32, 198.32.4.0/24, 199.165.145.0, 199.165.145.17, 199.165.145.24, 199.165.145.4, 199.165.146.0, 199.165.146.1, 199.165.146.3, 199.165.146.4, 2.0.0.0, 2.0.0.0/8, 2.1.1.3, 2.6.28.18, 204.152.184.64, 204.152.188.234, 206.0.1.133, 206.0.1.255, 206.168.198.192/28, 206.168.198.209, 206.168.198.213, 207.126.144.0/20, 208.77.188.0/24, 208.77.188.100, 209.180.251.0, 209.198.168.206, 209.246.26.10, 209.246.26.24, 209.246.26.25, 209.246.26.36, 209.246.26.39, 209.246.26.40, 209.246.26.41, 209.246.26.53, 209.85.128.0/17, 209.85.171.100, 209.85.171.147, 213.144.138.193, 213.198.168.206, 216.117.131.52, 216.12.111.80, 216.239.32.0/19, 216.239.32.10, 224.0.0.0/3, 224.0.0.0/4, 224.0.0.1, 24.8.175.0/24, 24.8.175.1, 24.8.175.254, 24.8.175.255, 24.8.175.69, 255.0.0.0, 255.255.0.0, 255.255.248.0, 255.255.255.0, 255.255.255.128, 255.255.255.192, 255.255.255.224, 255.255.255.248, 255.255.255.252, 255.255.255.254, 255.255.255.255, 4.3.2.1, 5.6.7.8, 63.173.189.0/26, 63.173.189.1, 63.173.189.17, 63.173.189.194, 63.173.189.2, 63.211.143.38, 63.231.83.113, 63.243.138.128, 64.18.0.0/20, 64.233.160.0/19, 66.102.0.0/20, 66.249.80.0/20, 66.77.122.161, 66.77.123.1, 71.33.249.193, 72.14.192.0/18, 72.32.154.224/27, 74.125.0.0/16, 74.125.95.103, 74.125.95.104, 74.125.95.105, 74.125.95.106, 74.125.95.147, 74.125.95.99, 74.208.4.194, 75.119.201.185, 77.109.128.150, 77.109.128.154, 77.109.128.209, 77.109.128.250, 82.165.230.84, 82.197.168.69, 88.198.52.145`
- **Discovered Interfaces:** `eth0, eth1, lo`
- **Related Knowledge Note:** [[knowledge/trained_unix_and_linux_system_administration_handbook]]

## Distilled MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`)
| Pre-State ($s$) | Tactic ($\tau$) | Technique ($k$) | Tool ($u$) | Post-State ($s'$) | Verified Command ($c$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `head` | `s_passive_topology_mapped` | `head and tail: read the beginning or end of a file . . . . . . . . . . . . . . . . . . 36` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `type` | `s_credentials_or_certs_acquired` | `Type conversions in expressions . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 57` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `chown` | `s_interactive_tty_or_priv_escalated` | `chown and chgrp: change ownership and group . . . . . . . . . . . . . . . . . . . . . 157` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `crontab` | `s_active_services_enumerated` | `Crontab management . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .286` |
| `s_cross_subnet_pivot_routed` | **`Post_Exploitation_Verification`** | Post-Action Host Identity, Privilege & Objective Verification | `hostname` | `s_goal_verified_complete` | `Hostname "addressing" . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 456` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `iptables` | `s_firewall_or_acl_unlocked` | `iptables firewall setup . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .937` |
| `s_passive_topology_mapped` | **`Active_Enum`** | Active Network, Cloud, Directory Service & Endpoint Probing | `echo` | `s_active_services_enumerated` | `echo -n "Stopping sshd: sshd"` |
| `s_init_unknown` | **`Reconnaissance`** | Domain, DNS, OSINT & Target Footprint Reconnaissance | `mdadm` | `s_passive_topology_mapped` | `sudo mdadm -As /dev/md0` |
| `s_firewall_or_acl_unlocked` | **`Lateral_Movement_Routing_Pivot`** | Remote Host Execution, L2/L3 Route Injection & Subnet Pivot | `route` | `s_cross_subnet_pivot_routed` | `route add -net 132.236.220.64 netmask 255.255.255.192` |
| `s_l2_l3_verified` | **`Out-of-Band_Access`** | UART/Serial Console Out-of-Band Enumeration & Control | `hostname` | `s_oob_serial_enumerated` | `hostname [ttl] [IN] AAAA ipaddr` |
| `s_protocol_chain_established` | **`Covert_Infil`** | Staged Artifact / Encapsulated Ingress Delivery | `scp` | `s_covert_infil_channel_ready` | `scp command  926` |
| `s_credentials_or_certs_acquired` | **`Protocol_Chaining`** | Multi-Protocol Handshake & Tunnel Relay Chaining | `snort` | `s_protocol_chain_established` | `Snort network intrusion detec-` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `hostname` | `s_passive_topology_mapped` | `Hostname and IP address assignment. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .477` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `echo` | `s_credentials_or_certs_acquired` | `echo "==> Leaving localizer, a is '$a'"` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `chmod` | `s_interactive_tty_or_priv_escalated` | `chmod +x helloworld` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `apt-get` | `s_active_services_enumerated` | `apt-get configuration. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 388` |
| `s_cross_subnet_pivot_routed` | **`Post_Exploitation_Verification`** | Post-Action Host Identity, Privilege & Objective Verification | `cp` | `s_goal_verified_complete` | `cp --preserve --recursive /etc/* /spare/backup \|\| echo "Did NOT make backup"` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `iptables` | `s_firewall_or_acl_unlocked` | `iptables implements not only NAT but also packet filtering. In earlier versions of` |
| `s_passive_topology_mapped` | **`Active_Enum`** | Active Network, Cloud, Directory Service & Endpoint Probing | `ping` | `s_active_services_enumerated` | `ping -c 3 tables. Of course, the LVM has to store both the original image and` |
| `s_init_unknown` | **`Reconnaissance`** | Domain, DNS, OSINT & Target Footprint Reconnaissance | `mdadm` | `s_passive_topology_mapped` | `sudo mdadm -S /dev/md0` |
| `s_firewall_or_acl_unlocked` | **`Lateral_Movement_Routing_Pivot`** | Remote Host Execution, L2/L3 Route Injection & Subnet Pivot | `route` | `s_cross_subnet_pivot_routed` | `route add default gw 132.236.227.1 eth0` |
| `s_l2_l3_verified` | **`Out-of-Band_Access`** | UART/Serial Console Out-of-Band Enumeration & Control | `erase` | `s_oob_serial_enumerated` | `erase = ^H; eol = M-^?; eol2 = M-^?; swtch = <undef>;` |
| `s_credentials_or_certs_acquired` | **`Protocol_Chaining`** | Multi-Protocol Handshake & Tunnel Relay Chaining | `command` | `s_protocol_chain_established` | `sudo command  113–116` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `sed` | `s_passive_topology_mapped` | `sed and awk, termcap and terminfo, and the UUCP networking system. We` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `echo` | `s_credentials_or_certs_acquired` | `echo "Before calling localizer, a is '$a'"` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `chmod` | `s_interactive_tty_or_priv_escalated` | `chmod (change mode) command. Use ls -l (or ls -ld for a directory) to inspect the` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `apt-get` | `s_active_services_enumerated` | `apt-get automation. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 391` |
| `s_cross_subnet_pivot_routed` | **`Post_Exploitation_Verification`** | Post-Action Host Identity, Privilege & Objective Verification | `echo` | `s_goal_verified_complete` | `echo "You did not tell me your name!"` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `dig` | `s_firewall_or_acl_unlocked` | `dig rs.dns-oarc.net txt and see what comes back; see page 652 for more details` |
| `s_passive_topology_mapped` | **`Active_Enum`** | Active Network, Cloud, Directory Service & Endpoint Probing | `ping` | `s_active_services_enumerated` | `ping -c 3 their price. In 2002, Quantum acquired Super DLT, a technology by Bench-` |
| `s_init_unknown` | **`Reconnaissance`** | Domain, DNS, OSINT & Target Footprint Reconnaissance | `ssh` | `s_passive_topology_mapped` | `sudo ssh tapehost mt -f /dev/nst0 fsf 3` |
| `s_firewall_or_acl_unlocked` | **`Lateral_Movement_Routing_Pivot`** | Remote Host Execution, L2/L3 Route Injection & Subnet Pivot | `route` | `s_cross_subnet_pivot_routed` | `route add -net 172.24.45.128/25 zulu-gw.atrust.net` |
| `s_l2_l3_verified` | **`Out-of-Band_Access`** | UART/Serial Console Out-of-Band Enumeration & Control | `zypper` | `s_oob_serial_enumerated` | `zypper command  392` |
| `s_credentials_or_certs_acquired` | **`Protocol_Chaining`** | Multi-Protocol Handshake & Tunnel Relay Chaining | `strace` | `s_protocol_chain_established` | `strace command  136` |
| `s_init_unknown` | **`Passive_Enum`** | Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey | `grep` | `s_passive_topology_mapped` | `grep Admin /pub/phonelist` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `echo` | `s_credentials_or_certs_acquired` | `echo "After calling localizer, a is '$a'"` |
| `s_initial_shell_or_api_access` | **`Privilege_Escalation`** | ACL/Permission Modification, Service Abuse & Privilege Escalation | `chown` | `s_interactive_tty_or_priv_escalated` | `chown and chgrp: change ownership and group` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `zypper` | `s_active_services_enumerated` | `Zypper package management for SUSE: now with more ZYpp!. . . . . . . . . 392` |
| `s_cross_subnet_pivot_routed` | **`Post_Exploitation_Verification`** | Post-Action Host Identity, Privilege & Objective Verification | `echo` | `s_goal_verified_complete` | `echo 'Invalid source directory'` |
| `s_oob_serial_enumerated` | **`Defense_Evasion_Firewall`** | Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment | `iptables` | `s_firewall_or_acl_unlocked` | `iptables firewall setup` |

## Verified Executable Commands (Grouped by Capability Layer)

### General_System (532 commands)
```bash
head and tail: read the beginning or end of a file . . . . . . . . . . . . . . . . . . 36
Type conversions in expressions . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 57
chown and chgrp: change ownership and group . . . . . . . . . . . . . . . . . . . . . 157
Crontab management . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .286
apt-get configuration. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 388
apt-get automation. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 391
Zypper package management for SUSE: now with more ZYpp!. . . . . . . . . 392
Hostname "addressing" . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 456
Hostname and IP address assignment. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .477
Script security . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 960
sed and awk, termcap and terminfo, and the UUCP networking system. We
grep Admin /pub/phonelist
export MANPATH=/home/share/localman:/usr/share/man
echo "This is a test message." > /tmp/mymessage
find / -name core
find / -name core 2> /dev/null
find / -name core > /tmp/corefiles 2> /dev/null
ps -ef | grep httpd
cut -d: -f7 < /etc/passwd | sort -u
grep command to select lines that contain the word httpd. The output of grep is
cp --preserve --recursive /etc/* /spare/backup || echo "Did NOT make backup"
echo $etcdir
echo "Saved ${rev}th version of mdadm.conf."
echo "I speak ${mylang}."
echo 'I speak ${mylang}.'
echo "There are `wc -l /etc/passwd` lines in the passwd file."
sort -t: -k3,3 -n /etc/group1
sort -t: -k3,3 /etc/group
cut -d: -f7 /etc/passwd | sort | uniq -c
wc /etc/passwd
find / -name core | tee /dev/tty | wc -l
tee command so that output goes both to a file and to the terminal window for
Type <Control-C> to stop monitoring.
sudo grep -l mdadm /var/log/*
echo "Hello, world!"
chmod +x helloworld
./helloworld3
prompt as an interactive script development environment.
find . -name '*log '
find . -type f -name '*.log '
find . -type f -name '*.log ' | grep -v .do-not-touch
find . -type f -name '*.log ' | grep -v .do-not-touch | while read fname
mv foo.log foo.LOG
mv genius/spew.log genius/spew.LOG
find . -type f -name '*.log ' | grep -v .do-not-touch | while read fname; do
echo mv $fname ${fname/.log/.LOG/}; done | bash -x
echo "\taa\tbb\tcc\n"
printf "\taa\tbb\tcc\n"
echo -n "Enter your name: "
echo "Hello $user_name!"
echo "You did not tell me your name!"
script below accepts two arguments, validates that the arguments are both direc-
echo "Usage: $0 source_dir dest_dir"
echo 'Invalid source directory'
echo 'Invalid destination directory'
printf "Source directory is ${source_dir}\n"
printf "Destination directory is ${dest_dir}\n"
mkdir aaa bbb
echo "==> In function localizer, a starts as '$a'"
echo "==> After local declaration, a is '$a'"
echo "==> Leaving localizer, a is '$a'"
echo "Before calling localizer, a is '$a'"
echo "After calling localizer, a is '$a'"
echo '==> Installing nothing'
echo "${message_level_text}: $message_itself"
echo "Copying $script to $newname..."
echo "$counter: $line"
echo "$((counter++)): $line"
echo "$a + $b = $c \t(plus sign as string literal)"
echo "$a + $b = $d \t(plus sign as arithmetic addition)"
echo "example[@] = ${example[@]}"
echo "example array contains ${#example[@]} elements"
echo "  Element = $elt"
grep and vi. They are so common that the name is usually shortened to "regex."
./helloworld
printf "There are %d articles of clothing.\n", $#items + 1;
printf "$counter ";
prompt to be repeated up to three times, after which the script gives up.
printf "Whole name: $fname $lname\n";
sudo perl -MCPAN -e shell
mount -o rw,remount /
echo -n "Starting sshd: sshd"
echo "."
echo -n "Stopping sshd: sshd"
kill `cat /var/run/sshd.pid`
echo "Usage: /etc/init.d/sshd start|stop|restart"
ln -s /etc/init.d/cups /etc/rc2.d/S80cups
ln -s /etc/init.d/cups /etc/rc0.d/K80cups
update-rc.d service { start | stop } sequence runlevels .
sudo shutdown -h +15 "Going down for emergency disk repair."
sudo activity. This timeout serves as a modest protection against users with sudo
sudo keeps a log of the command lines that were executed, the hosts on which
sudo runs on all UNIX and Linux systems. You do not need to worry
sudo power (all commands allowed, but no shells or su).
kill [-signal] pid
kill -9 pid
sudo pkill -u ben
sudo renice -5 8829
sudo renice 5 -u boggs
pfiles [pid]
pwdx [pid]
find /home -type f -size +1M -print0 | xargs -0 ls -l
sudo mount /dev/sda4 /users
mount /usr. See page 260 for a discussion of the fstab file and its brethren.
umount -f force-unmounts a busy filesystem and is supported on all our example
fuser -c /usr
ps -fp "157 315 5049"
fuser with the -v flag. This option produces a more readable display that includes
fuser -cv /usr
ls output encodes the type. For example, the following command demonstrates
ls -ld /usr/include
rm -i foo*
ln -s
sudo ln -s archived/secure /var/log/secure
ls -l /var/log/secure
chmod (change mode) command. Use ls -l (or ls -ld for a directory) to inspect the
ls -l /bin/gzip
ls -l /dev/tty0
chown and chgrp: change ownership and group
chmod -R g+w mydir
sudo chown -R matt ~matt/restore
sudo chgrp -R staff ~matt/restore
sudo chown -R matt ~matt/.*
chown user:group file …
sudo chown -R matt:staff ~matt/restore
ls -l /tmp/example
chmod 640 /tmp/example
chmod 770 /tmp/example
ls -v shows ACL information for filesystem objects. As with -l, you must include
chmod [-R] acl_operation file …
mount filesystems with the grpid option. Both of these measures make newly cre-
sudo passwd newusername
sudo chown -R newuser:newgroup ~newuser
sudo chown newuser:newgroup ~newuser/.*
ls -la
sudo useradd hilbert
sudo useradd -c "David Hilbert" -d /home/math/hilbert -g faculty -G
sudo find filesystem -xdev -nouser
script file of the commands it executed on your behalf. This can be a good learn-
sudo pvcreate /dev/sdc1
sudo vgcreate vgname /dev/sdc1
sudo lvcreate -l 100%FREE -n volname vgname
sudo mkfs -t ext4 /dev/vgname/volname
sudo mkdir mountpoint
sudo vi /etc/fstab
sudo pvcreate /dev/rdisk/disk4
sudo vgcreate vgname /dev/disk/disk4
sudo lvcreate -l freespace -n volname vgname
sudo mkfs /dev/vgname/volname
sudo mkvg -y vgname hdisk1
sudo crfs -v jfs2 -g vgname -m mountpoint -a size=freespaceM
sudo mount mountpoint
handle thousands.
sudo ioscan -fNn -C disk
erase performs as many overwrites as are needed to eliminate these shadow sig-
sudo hdparm --user-master u --security-set-pass password /dev/sda 8
sudo hdparm --user-master u --security-erase password /dev/sda
sudo /sbin/hdparm -Tt /dev/hdb
sudo mdadm -As /dev/md0
sudo mdadm -S /dev/md0
sudo mdadm /dev/md0 -f /dev/sdc1
sudo tail /var/log/messages
cat /proc/mdstat
sudo mdadm /dev/md0 -r /dev/sdc1
sudo mdadm /dev/md0 -a /dev/sdc1
sudo pvcreate /dev/md0
sudo vgcreate DEMO /dev/md0
sudo vgdisplay DEMO
sudo lvcreate -L 100G -n web1 DEMO
sudo mkfs /dev/DEMO/web1
sudo mkdir /mnt/web1
sudo mount /dev/DEMO/web1 /mnt/web1
sudo lvcreate -L 100G -s -n web1-snap DEMO/web1
sudo umount /mnt/web1
sudo lvchange -an DEMO/web1
sudo lvresize -L +10G DEMO/web1
sudo lvchange -ay DEMO/web1
sudo resize2fs /dev/DEMO/web1
sudo e2fsck -f /dev/DEMO/web1
df -h /mnt/web1
sudo lvmadm -t -V 1.0
sudo vgcreate vg01 /dev/disk/disk4
sudo lvcreate -L 25000 -n web1 vg01
sudo mkvg -y webvg hdisk1
sudo crfs -v jfs2 -g webvg -m /mnt/web1 -a size=25G
sudo mount /mnt/web1
sudo /sbin/tune2fs -c 50 /dev/sda3
sudo mount /dev/sda1 /mnt/temp
mount point on the command line. For example, with the Linux fstab configura-
sudo mount /media/cdrom0
sudo mount -t udf -o user,noauto,exec,utf8 /dev/scd0 /media/cdrom0
sudo mount -at ext4
mount
echo The time is now `date` > /dev/console
at 2:30 a.m. An entry like this might be used to start a long compilation at a time
find /tmp -atime +3 -type f -exec rm -f { } ';'
crontab filename installs filename as your crontab, replacing any previous version.
crontab -r removes it, leaving you with no crontab file at all.
crontab -e jsmith edits it. Linux allows both a username and a filename argument
crontab entries that run the scripts in a set of well-known directories, thereby
find / -xdev -type f '(' -name core -o name 'core.[0-9]*' -o name '*.core' ')' -atime +7 -exec rm -f { } ';'
find / -xdev -atime +3 '(' -name '#*' -o -name '.#*' -o -name '*.CKP' -o -name '*~' -o -name '.nfs*' ')' -exec rm -f { } ';'
sudo dump -0u -f anchor:/dev/nst0 /spare
sudo mkdir /var/restore
sudo ssh tapehost mt -f /dev/nst0 fsf 3
sudo restore -i -f tapehost:/dev/nst0
ls ~janet
sudo cp -p janet/iamlost ~janet/iamlost.restored
sudo chown janet ~janet/iamlost.restored
sudo chgrp staff ~janet/iamlost.restored
sudo restore -x -f tapehost:/dev/nst0 ./janet/iamlost
sudo mkfs /dev/vg01/lvol5
sudo mount /dev/vg01/lvol5 /home
sudo restore -r
tar reads multiple files or directories and packages them into one file, often a tape
sudo tar -cf - fromdir | ( cd todir ; sudo tar -xpf - )
tar expands holes in files and is intolerant of tape errors.13
dd if=/dev/st0 of=/dev/st1 cbs=16b
dd if=/dev/st0 of=tfile cbs=16b
dd if=tfile of=/dev/st0 cbs=16b
MySQL to store the catalog. The grant_mysql_privileges script sets up the ap-
MySQL and use separate catalogs for different groups of clients.
sudo ./bconsole
defaults specified in our configuration files.
sudo ./bacula start -d100
dmesg
sudo logs to local2 - keep a copy here too
rpm alone for the purpose of this example.
apt-get configuration
rpm or rpm-src for RPMs
script from the var subdirectory of your mirror to clean out obsolete files.
ln -s /var/spool/apt-mirror/us.archive.ubuntu.com/ubuntu /var/www/ubuntu
apt-get automation
apt-get dist-upgrade downloads and installs new versions of any packages that
apt-get update
apt-get -yes dist-upgrade
yum does not match on partial package names unless you include shell globbing
Zypper package management for SUSE: now with more ZYpp!
Zypper configuration files, including software repository configuration, are found
zypper addrepo uri
zypper dist-upgrade
zypper info packages
zypper install packages
zypper list-updates
zypper modifyrepo uri
zypper refresh
zypper remove packages
zypper repos
zypper search string
zypper shell (or sh)
zypper update
file /usr/lib/sw/sys.defaults. Even more strangely, per-user defaults can be con-
install-sd
mv $1 $newname;
echo "Backed up $1 to $newname.";
cp -p $newname $1;
mkdir repositories
chmod 700 admin
vi foo.c
git config --global user.name "John Q. Ulsah"
git config --global user.email "ulsah@book.admin.com"
sudo git init
sudo git add .
sudo git commit -m "Initial commit"
sudo vi mdadm/mdadm.conf
sudo git commit mdadm/mdadm.conf -m "Added spare to svr4west array"
sudo git status
sudo git commit passwd -m "Checking in existing passwd changes"
sudo git rm --cached mtab
sudo sh -c "echo mtab >> .gitignore"10
sudo git commit -m "Installed foobard; added RAID spare"
find (or pretend not to find, as the case may be). In addition, the kernel prospects
Copy arch/i386/boot/System.map to /boot/System.map.
insmod that understands dependencies, options, and installation and removal
handle each individual module.
modprobe also understands the statements install and remove. These statements
Hostname "addressing"
ndd -set /dev/ip ip_ire_redirect_interval 1000
Hostname and IP address assignment
type and have little to do with TCP/IP per se. One common example of this is
hostname
defaults unmolested as reference information; they make a nice sanity check if
sudo iptables -t nat -A POSTROUTING -o eth1 -j SNAT --to 63.173.189.1
hostname and IP address on a machine running Solaris. A quick peek at the an-
ndd [-set] device ? | variable [value]
ndd -set /dev/e1000g0 adv_autoneg_cap 0
ndd -set /dev/e1000g0 adv_1000fdx_cap 0
ndd -set /dev/e1000g0 adv_100fdx_cap 1
ndd -set /dev/e1000g0 adv_100hdx_cap 0
ndd -set /dev/e1000g0 adv_10fdx_cap 0
ndd -set /dev/e1000g0 adv_10hdx_cap 0
defaults to 1.
ndd -h | grep source
ndd -h ip_forward_src_routed
ndd -get /dev/ip ip_forward_src_routed
sudo ndd -set /dev/ip ip_forward_src_routed 1
echo 'Hey! I set the network address!'
handle redirects differently. Some hold on to them indefinitely. Others remove
hostname acme-gw
sudo rndc reload forward-zone-name
sudo rndc reload reverse-zone-name
logger "named restart"
hostname [ttl] [IN] A ipaddr
new-fast-box.atrust.com.
strings that are individually quoted. Be sure the quotes are balanced—missing
hostname [ttl] [IN] AAAA ipaddr
dig parent-domain ns
dig @name-server.parent-domain child-domain ns
dig @server version.bind txt chaos
dig domain ns
dig @ns-ext.isc.org version.bind txt chaos
dig @mroe.cs.colorado.edu version.bind txt chaos
dig @k.root-servers.net version.bind txt chaos
dig @k.root-servers.net hostname.bind txt chaos
dig @k.root-servers.net id.server txt chaos
hostname "string";
dig command.
dig rs.dns-oarc.net txt and see what comes back; see page 652 for more details
dig @f.root-servers.net . ns > root.cache
dig . ns > root.cache
./rndc-confgen -b 256
./configure
sudo make install
ID variables
hostname when queried for the CHAOS class names id.server and version.server.
sudo nsdc rebuild
sudo nsdc start
hostname or IP address. Forgetting the reverse files leaves sneaky errors: some
update-policy clause. allow-update grants permission to update any records in
update-policy ( grant | deny ) identity nametype name [types] ;
update-policy { grant dhcp-key subdomain dhcp.cs.colorado.edu A } ;
update-policy {
update-policy
sudo named -u 53
dig +short rs.dns-oarc.net txt
sudo dnssec-signzone -o example.com -N increment
sudo ldns-signzone example.com Kexample.com.+005+00682
sudo nsdc rebuild followed by sudo nsdc restart.
sudo dnssec-signzone -l dlv.isc.org example.com
update-security
sudo rndc stop
sudo /usr/sbin/named …
update-policy clause in named.conf for this zone. This is a common
sudo named -d2
sudo rndc stats
nslookup and host are simple and have pretty output, but you need dig or drill to
type ANY is a bit sneaky: instead of returning all data associated with a name, it
dig and drill include the notation aa in the output flags if an answer is authorita-
dig @e.gtld-servers.net w3w3.com ns
dig @ns0.nameservices.net w3w3.com ns
dig @ns1.nameservices.net w3w3.com ns
mount for writing; all others must mount read-only.
mount command understands the notation hostname:directory to mean the path
mount completes, you access an NFS-mounted filesystem just like a local filesys-
showmount -e monk
sudo mount -o rw,hard,intr,bg monk:/home/ben /nfs/ben
sudo mount -t nfs4 -o rw,hard,intr,bg monk:/ /nfs/ben
df /nfs/ben
mount -t nfs4 hostname:directory when requesting a version 4 mount.
mount NFS filesystems with mount -v nfs -a.
ls /portal
ls /portal/photos
rsync -gopt --password-file=/etc/rsync.pwd /etc/passwd lollipop::sysfiles
rsync server how to behave. The main file is /etc/rsyncd.conf, which contains
perl -e "print crypt('password','salt');"
ldapsearch -h atlantic.atrust.com -p 389
sudo amavisd-nanny
sudo amavisd-agent
sudo kill -HUP 'head -1 sendmail.pid'
./Build myhost.cf
sudo makemap hash /etc/mail/access < /etc/mail/access
cat /etc/passwd
sudo chroot /jail /usr/sbin/sendmail -bd -q30m
echo command redirected to the proper variable in the /proc filesystem. Chapter
sudo mailq
sudo exim -d -oX 26 -bd
MySQL database
hostname ending in cs.colorado.edu.
sudo postmap hash:/etc/postfix/access
sudo qshape deferred
sudo tcpdump host bull
sudo tcpdump src net 172.24.1.0/24 and dst port 80
snmpwalk -c secret813community -v1 tuva
sudo chage -m 2 -M 90 -E 2026-10-25 -W 14 ben
sudo ./john /etc/shadow
tar -zxvf ossec-hids-latest.tar.gz
sudo ./install.sh
Script security
dig www.google.com a
./configure --prefix=/etc/httpd/
sudo ifconfig eth0:0 128.138.243.150 netmask 255.255.255.192 up
ls -l /etc/host*
Hostname files can contain either hostnames from the /etc/hosts file or IP ad-
cat /etc/hostname.hme0
cat /etc/hostname.hme0:1
grep overkill /etc/hosts
sudo ifconfig lan0:1 172.24.69.1 up
sudo ifconfig en0 172.24.1.3 netmask 255.255.255.0 alias
sudo chdev -l en0 -a alias4=172.24.1.3,255.255.255.0
chmod 400 server.key server.key.orig
export EC2_HOME=~/.ec2
export PATH=$PATH:$EC2_HOME/bin
export EC2_PRIVATE_KEY=$EC2_HOME/pk-<long string value>.pem
export EC2_CERT=$EC2_HOME/cert-<long string value>.pem
export JAVA_HOME=/path/to/java
script terminates right away and the user is logged out immediately after logging
hostname and a global variable, making it easy for you to store configuration files
locate backend | grep -i cups
export PRINTER=printer_name
sudo lpadmin -p groucho -E -v parallel:/dev/lp0 -m pxlcolor.ppd
sudo lpadmin -p fezmo -E -v socket://172.24.0.12 -m laserjet.ppd
sudo lpadmin -p riley -c haemer
sudo lpadmin -p gilly -c haemer
sudo lpadmin -p zoe -c haemer
sudo lpadmin -x fezmo
sudo lpadmin -x haemer
sudo cupsdisable groucho
sudo reject corbet
sudo lpadmin -pprinter -vdevice { -eprinter | -mmodel | -iinterface }
sudo /usr/sbin/lpadmin -p"howler-lw,ralphie-lw" -ceng-printers
sudo lpadmin -phowler-lw -v/dev/tty06 -mPostScript -cpr
sudo lpadmin -dpr
sudo lpadmin -phowler-lw -L"Conference room"
sudo lpadmin -phowler-lw -rpr -cfast
sudo lpadmin -xhowler-lw
sudo reject -r"howler-lw will be down until Tuesday" howler-lw
sudo disable -r"Being cleaned, back in 5 minutes" howler-lw
sudo enable howler-lw
sudo lpmove howler-lw-324 howler-lw-325 anchor-lj
sudo lpmove howler-lw anchor-lj
sudo lpshut
sudo lpadmin -xhoser
sudo find /usr/spool/lp -name hoser | xargs rm -rf
sudo lpsched
sudo lpstat -t
kill them off by hand. lpc is useless in this situation. Rebooting the system always
kill and restart the master copy of lpd and manually remove jobs from the spool
grep cupsFilter /usr/share/ppd/ghostscript/model/pxlmono.ppd
Script or you can live with what you get by default.
sudo stopsrc -s lpd
sudo startsrc -s lpd
head that physical systems do not. The additional layers of abstraction introduced
sudo sh -c 'echo 1 > /sys/devices/system/cpu/sched_mc_power_savings'
sudo sh -c 'echo 1 > /sys/devices/system/cpu/sched_smt_power_savings'
sudo mount -o remount,noatime   /
Handle 0x0004, DMI type 4, 32 bytes.
uptime
sudo smbpasswd -a tobi
sudo chmod u=rw,g=rws,o= /home/eng
sudo chgrp eng /home/eng
sudo chown eng /home/eng
sudo ln -s 'msdfs:serverX\shareX,serverY\shareY' jump
smbclient //phobos/c\$ -U BOULDER\\ben
sudo mount -t cifs -o username=joe //redmond/joes /home/joe/mnt
mount /home/joe/mnt
sudo useradd printadm
sudo smbpasswd -a printadm
sudo mkdir -p /var/lib/samba/printers
sudo cd /var/lib/samba/printers
sudo mkdir W32X86 WIN40 x64
sudo chown -R printadm .
smbclient -U printadm '//samba-server/print$' -c 'mput *.*'
sudo smbcontrol smbd debug "4 auth:10"
sudo smbstatus
erase = ^H; eol = M-^?; eol2 = M-^?; swtch = <undef>;
unset noglob
groups work on the same problem without coordination
find that the number of available project owners quickly dwindles. Your goal in
groups deal with computers and wires, whereas the help desk deals with people.
apt-get command  387–391
dd command  316
tar command  315–316
chgrp command  157–158
chkconfig command  91, 94
chmod command  152, 156–157,
chown command  157–158
crontab command  286–287
crontab files  284–287
cut command  34
dd command  316, 992
df command  260
dig command  597–598, 615, 677–
dpkg command  383
fdisk command  207, 235–237
fuser command  144–145, 902,
git command  401
grep command  36
groups
history
hostname command  478
insmod command  435–436
history  447
iostat command  1127
kill command  127, 1132
ldapsearch command  734
yum  391
Zypper  392
locate command  23
logger command  351
modinfo command  431, 436–437
modprobe command  435
MySQL  318, 320–321, 956, 1193
update-policy clause  641
ndd command  468, 498–499, 504–
nslookup command  677
pkgutil command  23
prtconf command  430, 1120
psrinfo command  1120
rmmod command  435
rpm command  382–383
rsync command  290, 335, 725–727
sudo command  113–116
showmount command  706
smbclient  1148
snmpwalk command  885
apt-get  387–391
dpkg  383
rpm  382–383
strace command  136
svcadm command  98
svcs command  97, 494
rsync  725–727
tee command  35
uniq command  35
update-policy clause, DNS  641
update-rc.d command  94
vi editor  6, 30
wc command  35
xargs command  143
yum command  24, 391
zypper command  392
Cut out and tape to individual server machines. See admin.com for  a PDF version of this form.
```

### L1_Serial_OOB (3 commands)
```bash
stty lets you directly change and query the various settings of the terminal driver.
stty operates on the file descriptor of its standard input, so you can set and query
stty command  1167, 1178, 1180
```

### L2_ARP_Link (2 commands)
```bash
dladm command to list interfaces regardless of whether they have been plumbed.
ethtool command  489–490
```

### L3_Routing_NAT (74 commands)
```bash
iptables firewall setup . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .937
ping -c 3 tables. Of course, the LVM has to store both the original image and
ping -c 3 their price. In 2002, Quantum acquired Super DLT, a technology by Bench-
IP address, and the Ignite-UX server will respond and begin the installation.
IP address
route add -net 132.236.220.64 netmask 255.255.255.192
route add default gw 132.236.227.1 eth0
ifconfig eth0 172.24.1.13 netmask 255.255.255.0 up
route add -net 172.24.45.128/25 zulu-gw.atrust.net
route add -net 130.225.204.48 netmask 255.255.255.248 gw 130.225.204.49 eth0
route add -net 192.38.8.0 netmask 255.255.255.224 gw 192.38.8.129 eth1
iptables implements not only NAT but also packet filtering. In earlier versions of
ip address 192.108.21.254 255.255.255.0
ip address 192.225.33.254 255.255.255.0
ip address 192.225.40.253 255.255.255.0
IP address 63.173.189.1. The MX record reroutes email addressed to this machine
ping -c 3 problem until the root and top-level domains are signed, because the DNS-
IP address of mail-relay.atrust.com.
ping -c 3 beast (10.1.1.46): 56 bytes of data.
ping -c 3 the intermediate gateways in sequence to discover which link is dropping
ping -c 3 -s 1500 cuinfo.cornell.edu
ping -c 3 cuinfo.cornell.edu 1500
ping -c 3 packets to a target host at regular intervals. It shows the history of each mon-
traceroute hostname
traceroute nubark
traceroute to nubark (172.24.2.10), 30 hops max, 38 byte packets
traceroute to caida.org (192.172.226.78), 30 hops max, 46 byte packets
traceroute needs root privileges to operate. To be available to normal users, it
IP address, sorted by flows. -n 10 limits the display to the top 10 items.
ip route-cache flow on every interface, so that you see "software switched" flows
iptables firewall setup
iptables generally include startup scripts to achieve this enabling and loading.
iptables -F chain-name
iptables -P chain-name target
iptables -A chain-name -i interface -j target
iptables -F
iptables -P INPUT DROP
iptables -P FORWARD DROP
iptables -A FORWARD -i eth0 -p ANY -j ACCEPT
iptables -A FORWARD -d 10.1.1.2 -p tcp --dport 22 -j ACCEPT
iptables -A FORWARD -d 10.1.1.2 -p tcp --dport 80 -j ACCEPT
iptables -A FORWARD -d 10.1.1.2 -p tcp --dport 443 -j ACCEPT
ping -c 3 their default route, so the third rule here allows ICMP ECHO_REQUEST
iptables -A INPUT -i eth0 -d 10.1.1.1 -p tcp --dport 22 -j ACCEPT
iptables -A INPUT -i lo -d 127.0.0.1 -p ANY -j ACCEPT
iptables -A INPUT -i eth0 -d 10.1.1.1 -p icmp --icmp-type 8 -j ACCEPT
iptables -A INPUT -p icmp --icmp-type 0 -j ACCEPT
iptables -A INPUT -p icmp --icmp-type 3 -j ACCEPT
iptables -A INPUT -p icmp --icmp-type 5 -j ACCEPT
iptables -A INPUT -p icmp --icmp-type 11 -j ACCEPT
iptables -A FORWARD -d 10.1.1.2 -p icmp --icmp-type 0 -j ACCEPT
iptables -A FORWARD -d 10.1.1.2 -p icmp --icmp-type 3 -j ACCEPT
iptables -A FORWARD -d 10.1.1.2 -p icmp --icmp-type 5 -j ACCEPT
iptables -A FORWARD -d 10.1.1.2 -p icmp --icmp-type 11 -j ACCEPT
iptables -t nat -A PREROUTING -i eth1 -s 10.0.0.0/8 -j DROP
iptables -t nat -A PREROUTING -i eth1 -s 172.16.0.0/12 -j DROP
iptables -t nat -A PREROUTING -i eth1 -s 172.24.0.0/16 -j DROP
iptables -t nat -A PREROUTING -i eth1 -s 127.0.0.0/8 -j DROP
iptables -t nat -A PREROUTING -i eth1 -s 224.0.0.0/4 -j DROP
iptables -A INPUT -i eth1 -j LOG
iptables -A FORWARD -i eth1 -j LOG
iptables -A FORWARD -m state --state ESTABLISHED,RELATED -j ACCEPT
iptables simply disallows those connections. Although stateful packet filters can
ifconfig -a
traceroute and  867
ping -c 3 and  861
ipf command  500, 942
ipf command  942
ipfstat command  500
iptables  935–939
iptables command  493
ping -c 3 and  861–863
ping -c 3 command  473, 861–863
traceroute command  865–867
```

### L4_Port_Service (15 commands)
```bash
netstat -i
netstat -nr
telnet acme-gw.acme.com 3
telnet localhost 25
netstat -a is primarily useful for debugging higher-level problems once you have
netstat -s dumps the contents of counters that are scattered throughout the net-
netstat -i 2
Snort (snort.org) is an open source network intrusion prevention and detection
Snort itself is distributed for free as an open source package. However, Sourcefire
ssh does not consult SSHFP records by default. Add the VerifyHostKeyDNS op-
telnet localhost 80
ssh to administer it, just as you would with a system in your own data center. Best
scp command  926
Snort network intrusion detec-
ssh client  926
```

### L7_HTTP_Web (10 commands)
```bash
openssl genrsa -out rsa.private 1024
openssl rsa -in rsa.private -out rsa.public -pubout -outform PEM
wget ftp://user:password@hostname/path/to/file
wget http://ossec.net/files/ossec-hids-latest.tar.gz
openssl genrsa -des3 -out server.key 1024
openssl rsa -noout -text -in server.key
openssl req -new -key server.key -out server.csr
openssl req -noout -text -in server.csr
openssl rsa -in server.key.orig -out server.key
wget command  23, 727
```

