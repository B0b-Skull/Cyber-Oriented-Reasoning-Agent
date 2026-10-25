---
title: "Trained Knowledge & Topology: PowerSploit.pdf"
tags:
  - credential_access
  - enumeration
  - http
  - https
  - kerberos
  - mdp
  - mimikatz
  - nmap
  - passive_enum
  - pdf
  - powershell
  - privilege_escalation
  - trained
source_file: PowerSploit.pdf
doc_type: pdf
updated: 2026-10-25 01:00:07
---

# Trained Knowledge & Architecture: `PowerSploit.pdf`

- **Source Path:** `~/Projects/CORA/Training/PowerSploit.pdf` (`pdf`)
- **Extracted Technical Entities:** `http, https, kerberos, mimikatz, nmap, powershell`
- **Extracted IPs / Subnets:** `172.24.1.0/24`
- **Extracted Interfaces:** `None`
- **Linked Command Playbook:** [[commands/trained_powersploit]] (`13` CEGAR-verified commands | `13` MDP transitions)

## Command & Tactic Coverage Summary
- **Total CEGAR-Verified Commands:** `13` (full executable list in [[commands/trained_powersploit]])
- **Tactic Distribution:** `Credential_Access` (5), `Enumeration` (3), `Privilege_Escalation` (3), `Passive_Enum` (2)
- **Top Extracted CLI Tools:** `mimikatz` (2), `base64` (1), `defaults` (1), `get-process` (1), `hexdump` (1), `invoke-tokenmanipulation` (1), `invoke-wmicommand` (1), `new-elevatedpersistenceoption` (1), `new-userpersistenceoption` (1), `out-minidump` (1), `sekurlsa::logonpasswords` (1), `strings` (1)

## LLM Distilled Operational Summary
### Key Operational Techniques & Workflows

*   **Reflective Code Execution**: Use `Invoke-ReflectivePEInjection` to load DLLs/EXEs into PowerShell or remote processes without writing files to disk. Requires a byte array (`-PEBytes`) and optional target process details (`-ProcName`, `-ProcId`).
*   **Shellcode Injection**: Utilize `Invoke-Shellcode` for injecting raw shellcode (byte arrays) into processes. Supports remote execution via `-ComputerName` and forced execution with `-Force`.
*   **Remote Command Execution**: Execute PowerShell scripts on targets using `Invoke-WmiCommand` with a scriptblock payload (`-Payload`) and optional credentials (`-Credential`).
*   **Credential Harvesting & Exfiltration**:
    *   Decrypt GPP passwords via `Get-GPPPassword`.
    *   Log keystrokes (`Get-Keystrokes`) or capture screenshots (`Get-TimedScreenshot`) with configurable intervals and timeouts.
    *   Inject Mimikatz via `Invoke-Mimikatz` to extract hashes (`lsadump::cache`), Kerberos tickets (`kerberos::list /export`), or perform DCSync (`lsadump::dcsync`).
*   **Token Manipulation**: Use `Invoke-TokenManipulation` to enumerate tokens (`-Enumerate`), revert to self (`-RevToSelf`), or create alternate processes with specific tokens (`-CreateProcess`).
*   **Memory Forensics**: Generate full-memory dumps of processes using `Out-Minidump` (pipeline-compatible with `Get-Process`).
*   **File Exfiltration**: Use `Invoke-NinjaCopy` to access locked files (e.g., `NTDS.dit`, `SYSTEM` hives) via raw disk access and copy them locally or remotely.
*   **Persistence**: Build user-land (`New-UserPersistenceOption`) or elevated (`New-ElevatedPersistenceOption`) persistence sets via Registry keys, Scheduled Tasks, or Logon triggers, then apply with `Add-Persistence`.

### Critical Command Patterns & Flags

| Function | Key Flags/Parameters |
| :--- | :--- |
| `Invoke-ReflectivePEInjection` | `-PEBytes`, `-ComputerName`, `-ExeArgs`, `-ProcName`, `-ProcId` |
| `Invoke-Shellcode` | `-ProcessID`, `-Shellcode`, `-Force` |
| `Invoke-WmiCommand` | `-Payload`, `-ComputerName`, `-Credential` |
| `Invoke-Mimikatz` | `-ComputerName`, `-Command` (e.g., `"lsadump::dcsync /user:krbtgt..."`) |
| `Invoke-NinjaCopy` | `-Path`, `-LocalDestination`, `-RemoteDestination`, `-ComputerName` |
| `Invoke-TokenManipulation` | `-Enumerate`, `-RevToSelf`, `-CreateProcess`, `-Username`, `-ProcessId` |
| `Out-Minidump` | `-Process`, `-DumpFilePath` |
| `New-UserPersistenceOption` | `-Registry`, `-AtLogon`, `-ScheduledTask`, `-OnIdle`, `-Daily`, `-Hourly`, `-At` |

### Network Topology & Service Relationships

*   **Remote Execution Targets**: Most functions (`Invoke-ReflectivePEInjection`,

