---
title: "Trained Knowledge & Topology: us-15-Graeber-Abusing-Windows-Management-Instrumentation-WMI-To-Build-A-Persistent Asynchronous-And-Fileless-Backdoor-wp"
category: knowledge
domain_hub: "[[knowledge/04_windows_powershell_wmi_cim_and_active_directory]]"
os_platform: windows
primary_tactic: Active_Enum
summary: "Operational architecture, decision workflows & Windows/Linux command reference for us-15-Graeber-Abusing-Windows-Management-Instrumentation-WMI-To-Build-A-Persistent Asynchronous-And-Fileless-Backdoor-wp: PowerShell 2.0-7+ cmdlets, Get-CimInstance/Get-WmiObject/wmic queries, WinRM/PSRemoting (Invoke-Command, Enter-PSSession), Active "
when_to_apply: "Apply when working with us-15-Graeber-Abusing-Windows-Management-Instrumentation-WMI-To-Build-A-Persistent Asynchronous-And-Fileless-Backdoor-wp (windows): Apply when automating Windows enumeration with PowerShell or WMI/CIM (`Get-CimInstance`/`wmic`), executing commands remotely via WinRM/WMI, enumerating Active Directory users/groups/computers/trusts/GPOs (`dsquery`/`nltest`/`net`), or auditing Kerberos tickets (`klist`) and SPNs (`setspn`)."
tags: [credential_access, curl, enumeration, http, https, lateral_movement_routing_pivot, mdp, out-of-band_access, passive_enum, pdf, powershell, reconnaissance, sysinternals, trained, wmic, windows, get-ciminstance, winrm, invoke-command, dsquery, nltest, kerberos]
source_file: "us-15-Graeber-Abusing-Windows-Management-Instrumentation-WMI-To-Build-A-Persistent Asynchronous-And-Fileless-Backdoor-wp"
updated: 2026-10-30
---

# Trained Knowledge & Architecture: `us-15-Graeber-Abusing-Windows-Management-Instrumentation-WMI-To-Build-A-Persistent Asynchronous-And-Fileless-Backdoor-wp.pdf`

- **Source Path:** `~/Projects/CORA/Training/us-15-Graeber-Abusing-Windows-Management-Instrumentation-WMI-To-Build-A-Persistent Asynchronous-And-Fileless-Backdoor-wp.pdf` (`pdf`)
- **Extracted Technical Entities:** `curl, http, https, powershell, sysinternals, wmic`
- **Extracted IPs / Subnets:** `172.24.72.131, 172.24.72.134, 172.24.72.135`
- **Extracted Interfaces:** `None`
- **Linked Command Playbook:** [[commands/trained_us-15-graeber-abusing-windows-management-instrumentation-wmi-to-]] (`47` CEGAR-verified commands | `47` MDP transitions)

## Command & Tactic Coverage Summary
- **Total CEGAR-Verified Commands:** `47` (full executable list in [[commands/trained_us-15-graeber-abusing-windows-management-instrumentation-wmi-to-]])
- **Tactic Distribution:** `Enumeration` (23), `Passive_Enum` (11), `Credential_Access` (6), `Lateral_Movement_Routing_Pivot` (5), `Out-of-Band_Access` (1), `Reconnaissance` (1)
- **Top Extracted CLI Tools:** `get-wmiobject` (11), `invoke-wmimethod` (6), `get-ciminstance` (3), `new-object` (3), `set-wmiinstance` (3), `get-wminamespace` (2), `new-cimsession` (2), `get-cimassociatedinstance` (1), `get-cimclass` (1), `get-cimsession` (1), `get-credential` (1), `invoke-cimmethod` (1), `ls` (1), `new-ciminstance` (1), `new-cimsessionoption` (1), `register-cimindicationevent` (1), `register-wmievent` (1), `remove-ciminstance` (1), `remove-cimsession` (1), `remove-wmiobject` (1), `set-ciminstance` (1), `set-itemproperty` (1), `test-wsman` (1), `wmic` (1)

## LLM Distilled Operational Summary
### Key Operational Techniques & Decision Workflows
*   **Architecture Exploitation**: Leverage the consistency of WMI across Windows NT 4.0 through modern versions to bypass deprecation cycles.
*   **Data Consumption**: Utilize PowerShell for rapid interaction and querying of managed components (e.g., `Win32_Process`, `Win32_Service`).
*   **Dynamic vs. Persistent Objects**:
    *   Use **Dynamic Objects** for on-the-fly reconnaissance (e.g., listing running processes).
    *   Use **Persistent Objects** stored in `%SystemRoot%\System32\wbem\Repository\OBJECTS.DATA` for long-term persistence and asynchronous execution.
*   **Schema Injection**: Create custom WMI objects directly via .NET code without requiring MOF files, allowing flexible payload definition.
*   **Event-Driven Execution**: Register event handlers on object creation/modification to trigger callbacks or maintain presence.
*   **Lateral Movement**: Execute remote commands using the `Win32_Process.Create` method.

### Critical Command Patterns & Required Flags
*   **Querying Data**: Use **WQL (WMI Query Language)** for fine-grained filtering of object instances.
*   **Remote Transmission**:
    *   **DCOM**: Default local/remote protocol for WMI traffic.
    *   **WinRM**: Alternative protocol for remote management.
*   **Payload Execution**: Invoke `Win32_Process.Create` methods within WMI classes to spawn processes remotely.
*   **Persistence Mechanism**: Inject custom class instances into the **CIM Repository** (`OBJECTS.DATA`) to ensure survival across reboots.

### Network Topology & Service Relationships
*   **Core Service**: `Winmgmt` (Windows Management Instrumentation) service handles data population and query resolution.
*   **Data Storage**: Persistent WMI objects reside in the **CIM Repository** located at `%SystemRoot%\System32\wbem\Repository\OBJECTS.DATA`.
*   **Schema Definition**: Managed Object Format (**MOF**) files define the structure of standard WMI objects, though custom objects can bypass these files.
*   **Standards Compliance**: Implements **WBEM** and **CIM** standards from the **DMTF**, enabling industry-agnostic data transmission.
*   **Interoperability**: Supports both **DCOM** and **WinRM** for remote data transmission, facilitating lateral movement across network segments.

## Document Structure & Key Topics
- Prep file to drop on remote system
- Establish remote WMI connection
- "Push" file contents
- The PowerShell payload that will drop the stored file contents
- Drop the file to the target filesystem
- Confirm successful file drop
- Create a remote registry key and value
- PowerShell payload that saves the serialized output of `Get-Process lsass` to
- Invoke PowerShell payload
- Pull the serialized results back
- Deserialize and display the result of the command executed on the remote system

## Extracted Operational Steps & Workflows
- 1. Instance queries – Query instances on WMI objects
- 2. Event queries – Equivalent to registering an alert upon creation, modification, or deletion of a
- 3. Meta queries – Metaqueries used to query information about WMI namespaces and class
- 1. An event filter – The event of interest
- 2. An event consumer – An action to perform upon triggering an event
- 3. A filter to consumer binding – The registration mechanism that binds a filter to a consumer
- 98. 

- 1. An attacker uses WMI as a persistence mechanism
- 2. The WMI Shell utility is used as a C2 channel
- 3. WMI classes are created to store attacker data
- 4. An attacker installs a malicious WMI provider
- 5. An attacker persists via the Start Menu or registry
- 6. An attacker persists via other additional registry values
- 7. An attacker installs a service
- 1. Consider disabling the WMI service. Consider your organizations need for remote WMI access.
- 2. Consider blocking the WMI protocol ports. If there is no legitimate need to use remote WMI,
- 3. WMI, DCOM, and WinRM events are logged to the following event logs:

<!-- CORA-MAXIMIZED-COMMANDS-START -->
## Maximized Windows & Linux Command Examples for `us-15-Graeber-Abusing-Windows-Management-Instrumentation-WMI-To-Build-A-Persistent Asynchronous-And-Fileless-Backdoor-wp`

> **Domain Hub:** [[knowledge/04_windows_powershell_wmi_cim_and_active_directory|Domain Hub 04: Windows PowerShell, WMI/CIM, WinRM Remoting, Active Directory (dsquery), Kerberos & Post-Exploitation]]  
> **Master Playbooks:** [[commands/windows_master_command_playbook]] | [[commands/linux_master_command_playbook]] | [[commands/curl_playbook]] | [[commands/tio_serial_playbook]]  
> **When to Apply:** Apply when automating Windows enumeration with PowerShell or WMI/CIM (`Get-CimInstance`/`wmic`), executing commands remotely via WinRM/WMI, enumerating Active Directory users/groups/computers/trusts/GPOs (`dsquery`/`nltest`/`net`), or auditing Kerberos tickets (`klist`) and SPNs (`setspn`).  
> **15-Engine H-MDP State Transition:** `s_active_services_enumerated` $\xrightarrow{\text{Active_Enum}}$ `s_credentials_or_certs_acquired` | **Bayesian Root-Cause Triggers:** `ad_domain_trust_or_spn_exposure, winrm_or_wmi_lateral_movement_path, kerberos_ticket_or_delegation_weakness, unquoted_service_or_gpo_misconfig` | **Isolation:** `RED, BLUE (Active Directory / WinRM network queries require allowed LAN interface; local CIM/WMI works in WHITE)`

| Primary Command (`Windows` / `Linux`) | OS / Shell | What It Does & Key Flags | When to Apply & Expected Output | Cross-Platform Equivalent |
| :--- | :--- | :--- | :--- | :--- |
| `powershell -NoProfile -Command "Get-CimInstance Win32_ComputerSystem \| Select-Object Name,Domain,Manufacturer,Model,UserName,TotalPhysicalMemory"` | **PowerShell** | Queries `Win32_ComputerSystem` via modern CIM (WS-Man/DCOM) for host domain membership, logged-on console user, and hardware model. | Apply in PowerShell 4.0+ as the fast, structured replacement for `wmic computersystem` (`[[knowledge/trained_ps_get-cim]]`). | `hostnamectl && lscpu && free -h` |
| `powershell -NoProfile -Command "Get-CimInstance Win32_Service \| Where-Object {$_.State -eq 'Running' -and $_.PathName -notmatch 'C:\\Windows'} \| Select-Object Name,DisplayName,StartName,PathName"` | **PowerShell** | Finds all running third-party/custom Windows services whose binary path is outside `C:\Windows`. | Apply to quickly isolate non-OS services and inspect their execution account (`StartName`) and binary path. | `systemctl list-units --type=service --state=running` |
| `powershell -NoProfile -Command "Get-CimInstance -Namespace root\subscription -ClassName __EventFilter; Get-CimInstance -Namespace root\subscription -ClassName CommandLineEventConsumer; Get-CimInstance -Namespace root\subscription -ClassName __FilterToConsumerBinding"` | **PowerShell** | Audits the `root\subscription` WMI repository for permanent WMI Event Filters, Consumers, and Bindings. | Apply to detect fileless WMI persistence (`[[knowledge/trained_us-15-graeber-abusing-windows-management-instrumentation-wmi-to-]]`). | `crontab -l && systemctl list-timers --all` |
| `wmic /node:"<TARGET_IP>" process call create "cmd.exe /c ipconfig /all > C:\Temp\out.txt"` | **Windows CMD** | Executes a command remotely on `<TARGET_IP>` over DCOM/RPC (`TCP 135` + dynamic high ports) using WMI `Win32_Process.Create`. | Apply for agentless remote execution across domain hosts when WinRM (`5985`) is closed but RPC (`135`) is open. | `ssh <USER>@<TARGET_IP> 'ip -4 -br addr'` |
| `winrm enumerate winrm/config/listener && powershell -NoProfile -Command "Test-WSMan -ComputerName <TARGET_IP>"` | **CMD / PS** | Enumerates local WinRM listeners (`5985` HTTP / `5986` HTTPS) and tests WS-Management reachability on `<TARGET_IP>`. | Apply before running `Invoke-Command` or `Enter-PSSession` (`[[commands/trained_powershell-remoting]]`). | `nc -zv <TARGET_IP> 22` |
| `powershell -NoProfile -Command "Invoke-Command -ComputerName <TARGET_IP> -ScriptBlock { hostname; whoami /all; Get-NetIPConfiguration }"` | **PowerShell** | Executes a PowerShell script block on remote host `<TARGET_IP>` over WinRM (`TCP 5985`/`5986`) and returns serialized objects. | Apply for multi-host administrative command execution and remote triage. | `ssh <USER>@<TARGET_IP> 'hostname; id; ip addr'` |
| `nltest /dclist: && nltest /domain_trusts /all_trusts` | **Windows CMD** | Discovers all Domain Controllers in the current domain and enumerates all forest/external/transitive domain trusts. | Apply first during Active Directory reconnaissance (`[[commands/trained_domain_service_tools]]`). | `dig _ldap._tcp.dc._msdcs.<DOMAIN> SRV` |
| `net user /domain && net group "Domain Admins" /domain && net group "Enterprise Admins" /domain` | **Windows CMD** | Queries the Domain Controller for all domain user accounts and members of high-privilege administrative groups. | Apply on any domain-joined workstation/server to map privileged accounts (`[[commands/trained_net_cmds_1]]`). | `ldapsearch -x -H ldap://<DC_IP> -b 'dc=domain,dc=local'` |
| `dsquery user -limit 0 \| dsget user -samid -sid -upn -pwdneverexpires -disabled && dsquery computer -limit 0` | **Windows CMD (AD)** | Queries Active Directory LDAP for all user accounts (with SAMID, SID, and password expiry flags) and all domain computers (`[[commands/trained_ds_cmds]]`). | Apply when RSAT or DC tools are present to export complete Active Directory object inventories. | `ldapsearch -LLL -H ldap://<DC_IP> '(objectClass=user)' sAMAccountName objectSid` |
| `setspn -Q */* && klist` | **Windows CMD** | Lists all Service Principal Names (`SPNs`) registered in Active Directory (`setspn -Q */*`) and inspects cached Kerberos tickets (`klist`). | Apply to locate SQL/HTTP/Exchange service accounts (`Kerberoasting` audit) and verify active TGT/TGS encryption types (`[[knowledge/trained_kerberos_attacks_cheatsheet]]`). | `klist && kvno <SPN>` |

### Copy-Pasteable Execution Block (Windows & Linux)
```bash
# [PowerShell] Queries `Win32_ComputerSystem` via modern CIM (WS-Man/DCOM) for host domain membership, logged-on console user, and hardware model.
powershell -NoProfile -Command "Get-CimInstance Win32_ComputerSystem | Select-Object Name,Domain,Manufacturer,Model,UserName,TotalPhysicalMemory"
# [PowerShell] Finds all running third-party/custom Windows services whose binary path is outside `C:\Windows`.
powershell -NoProfile -Command "Get-CimInstance Win32_Service | Where-Object {$_.State -eq 'Running' -and $_.PathName -notmatch 'C:\\Windows'} | Select-Object Name,DisplayName,StartName,PathName"
# [PowerShell] Audits the `root\subscription` WMI repository for permanent WMI Event Filters, Consumers, and Bindings.
powershell -NoProfile -Command "Get-CimInstance -Namespace root\subscription -ClassName __EventFilter; Get-CimInstance -Namespace root\subscription -ClassName CommandLineEventConsumer; Get-CimInstance -Namespace root\subscription -ClassName __FilterToConsumerBinding"
# [Windows CMD] Executes a command remotely on `<TARGET_IP>` over DCOM/RPC (`TCP 135` + dynamic high ports) using WMI `Win32_Process.Create`.
wmic /node:"<TARGET_IP>" process call create "cmd.exe /c ipconfig /all > C:\Temp\out.txt"
# [CMD / PS] Enumerates local WinRM listeners (`5985` HTTP / `5986` HTTPS) and tests WS-Management reachability on `<TARGET_IP>`.
winrm enumerate winrm/config/listener && powershell -NoProfile -Command "Test-WSMan -ComputerName <TARGET_IP>"
# [PowerShell] Executes a PowerShell script block on remote host `<TARGET_IP>` over WinRM (`TCP 5985`/`5986`) and returns serialized objects.
powershell -NoProfile -Command "Invoke-Command -ComputerName <TARGET_IP> -ScriptBlock { hostname; whoami /all; Get-NetIPConfiguration }"
```
<!-- CORA-MAXIMIZED-COMMANDS-END -->
