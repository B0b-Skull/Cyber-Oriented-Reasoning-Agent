---
title: "Trained Knowledge & Topology: credential_dumping.pdf"
tags:
  - covert_exfil
  - credential_access
  - defense_evasion_firewall
  - enumeration
  - http
  - https
  - impacket
  - john
  - kerberos
  - lateral_movement_routing_pivot
  - mdp
  - mimikatz
  - netsh
  - nmap
  - out-of-band_access
  - pdf
  - powershell
  - privilege_escalation
  - ssh
  - sysinternals
  - trained
source_file: credential_dumping.pdf
doc_type: pdf
updated: 2026-10-24 00:58:07
---

# Trained Knowledge & Architecture: `credential_dumping.pdf`

- **Source Path:** `~/Projects/CORA/Training/credential_dumping.pdf` (`pdf`)
- **Extracted Technical Entities:** `http, https, impacket, john, kerberos, mimikatz, netsh, nmap, powershell, ssh, sysinternals`
- **Extracted IPs / Subnets:** `172.24.0.102, 172.24.1.103, 172.24.1.105, 172.24.1.108, 172.24.1.112`
- **Extracted Interfaces:** `None`
- **Linked Command Playbook:** [[commands/trained_credential_dumping]] (`81` CEGAR-verified commands | `81` MDP transitions)

## Command & Tactic Coverage Summary
- **Total CEGAR-Verified Commands:** `81` (full executable list in [[commands/trained_credential_dumping]])
- **Tactic Distribution:** `Credential_Access` (58), `Covert_Exfil` (13), `Lateral_Movement_Routing_Pivot` (3), `Out-of-Band_Access` (3), `Privilege_Escalation` (2), `Defense_Evasion_Firewall` (1), `Enumeration` (1)
- **Top Extracted CLI Tools:** `reg` (9), `nmap` (8), `import-module` (6), `john` (4), `type` (4), `crackmapexec` (3), `python` (3), `sekurlsa::minidump` (3), `telnet` (3), `netsh` (2), `secretsdump.py` (2), `get-addbaccount` (1), `get-bootkey` (1), `get-gpppassword` (1), `get-process` (1), `invoke-credentialsphish` (1), `invoke-loginprompt.ps1` (1), `invoke-powerdump` (1), `invoke-wdigestdowngrade` (1), `ip` (1), `lockphish.sh` (1), `lsadump::cache` (1), `lsadump::dcsync` (1), `lsadump::lsa` (1), `lsadump::sam` (1)

### Visual & Network Diagram Intelligence (`credential_dumping.pdf#page1`)
- **Spatially Grouped Diagram Nodes (Box/Component Clusters):**
  1. `[iGnITE | Technologies]`
  2. `[8 | ④]`
  3. `[f11 | f12 | 书]`
  4. `[国]`
  5. `[3 | 机]`
  6. `[ctrl | 目]`
  7. `[無变换]`
  8. `[alt | 口-又字]`
  9. `[CREDENTIALDUMPING]`
  10. `[CHEATSHEET]`
  11. `[WWW.HACKINGARTICLES.IN]`

### Visual & Network Diagram Intelligence (`credential_dumping.pdf#page8`)
- **Spatially Grouped Diagram Nodes (Box/Component Clusters):**
  1. `[Credential | Dumping: Wireless]`
  2. `[iGnITE | Technologies]`
  3. `[www.hackingarticles.in]`
  4. `[Page I 8]`

### Visual & Network Diagram Intelligence (`credential_dumping.pdf#page17`)
- **Spatially Grouped Diagram Nodes (Box/Component Clusters):**
  1. `[Credential]`
  2. `[Dumping:]`
  3. `[Group | Preferences]`
  4. `[Policy]`
  5. `[(GPP)]`
  6. `[iGnITE | Technologies]`
  7. `[www.hackingarticles.in]`
  8. `[Page | 17]`

## LLM Distilled Operational Summary
### Operational Techniques & Decision Workflows
- **Tool Selection Strategy**: Choose tools based on the target environment and authentication protocol (e.g., `Mimikatz` for memory-based credentials, `SamDump2` for SAM database extraction, `LaZagne` for application credential harvesting).
- **Workflow Phases**:
  1.  **Reconnaissance**: Identify running services (e.g., `WDigest`, `SSP`) and authentication methods (LM/NTLM).
  2.  **Manual Dumping**: Use GUI tools like `WirelessKeyView` or `Credential Manager` for quick, non-intrusive access.
  3.  **Automated/Scripted Dumping**: Execute PowerShell scripts (`Invoke-Powerdump.ps1`, `Get-PassHashes.ps1`) or command-line utilities (`PwDump7`, `SamDump2`) for deeper memory or registry extraction.
  4.  **Framework Integration**: Leverage `Metasploit` modules (`credential_collector`, `load kiwi`) or `PowerShell Empire` (`mimilib.dll`) to automate the collection and decryption of hashes.
  5.  **Post-Extraction**: Decrypt hashes using `John the Ripper` or `Hashcat` and analyze `Group Policy Preferences (GPP)` for plaintext secrets.

### Critical Command Patterns & Required Flags
- **Mimikatz**:
    -   `sekurlsa::logonpasswords` (Extracts plaintext passwords from memory).
    -   `sekurlsa::pth /user:USERNAME /domain:DOMAIN /ntlm:HASH` (Privilege Escalation via hash).
    -   `lsadump::sam` (Extracts SAM database hashes).
- **Metasploit**:
    -   `use post/windows/gather/credential_collector` (Automated credential gathering).
    -   `use post/windows/manage/load_kiwi` (Loads Mimikatz within Metasploit).
    -   `use auxiliary/scanner/sam/sam_info` (Scans for SAM database).
- **PowerShell**:
    -   `Invoke-PowerDump` (Custom script for hash extraction).
    -   `Get-PassHashes` (Retrieves password hashes from memory).
- **Specialized Tools**:
    -   `samdump2 <SAM_FILE> <NTDS_FILE>` (Command-line SAM extraction).
    -   `lazagne.exe runa` (Automated application credential dump).

### Network Topology & Service Relationships
- **Authentication Protocols**:
    -   **LM/NTLM**: Legacy Windows authentication; targets include `Windows 7` and `Windows 10`.
    -   **WDigest**: A legacy service often enabled by default in older configurations, storing credentials in memory.
    -   **Security Support Provider (SSP)**: Services like `mimilib.dll` facilitate credential dumping via the SSP interface.
- **Storage Locations**:
    -   **SAM Database**: Located in `%SystemRoot%\System32\config\SAM`; stores hashed passwords for local accounts.
    -   **Group Policy Preferences (GPP)**: Often stores plaintext passwords in registry keys under `HKLM\Software\Policies\Microsoft\Windows NT

## Document Structure & Key Topics
- Introduction (p. 7)
- Credential Dumping in Real Life (p. 7)
- Manual Credential Dumping (p. 9)
- Credential Dumping using netsh (p. 10)
- Credential Dumping using WirelessKeyView (p. 12)
- Credential Dumping using Wifi Network Properties (p. 13)
- Credential Dumping using LaZagne (p. 14)
- Credential Dumping using Mimikatz (p. 15)
- Credential Dumping using Metasploit Framework (p. 16)
- Create an Account in Domain Controller with GPP (p. 19)
- Exploiting Group Policy Preferences via Metasploit-I (p. 21)
- Exploiting Group Policy Preferences via Metasploit -II (p. 22)
- Gpp-Decrypt (p. 24)
- GP3finder (p. 26)
- PowerShell Empire (p. 26)
- Windows Powershell (p. 27)
- Accessing Credential Manager (p. 29)
- Metasploit (p. 32)
- Empire (p. 33)
- CredentialsFileView (p. 35)
- Windows PowerShell (p. 36)
- Introduction to Wdigest (p. 38)
- Working of WDigest.dll (p. 38)
- Manual (p. 39)
- PowerShell (p. 42)
- PowerShell via Meterpreter (p. 43)
- Metasploit Framework (p. 45)
- PowerShell Empire (p. 46)
- CrackMapExec (p. 47)
- Introduction to Security Support Provider (p. 49)
- Manual (p. 49)
- Mimikatz (p. 52)
- Metasploit Framework (p. 53)
- Koadic (p. 55)
- PowerShell Empire (p. 56)
- Introduction to SAM (p. 60)
- LM authentication (p. 60)
- NTLM authentication (p. 60)
- Windows 7 (p. 61)
- PwDump7 (p. 61)
- SamDump2 (p. 62)
- PowerShell (p. 63)
- Windows 10 (p. 64)
- Mimikatz (p. 64)
- Impacket (p. 65)
- Koadic (p. 67)
- LaZAgne (p. 69)
- CrackMapExec (p. 69)
- PowerShell Empire (p. 72)
- Introduction to NTDS (p. 82)
- FGDump (p. 83)
- DSInternals (p. 85)
- NTDSDump.exe (p. 86)
- Metasploit (NTDS_grabber) (p. 87)
- CrackMapExec (p. 89)
- Hash Cracking (p. 89)
- FakeLogonScreen (p. 93)
- SharpLocker (p. 95)
- Koadic (p. 98)
- Lockphish (p. 101)
- Windows 7 (lsass.exe) Credential Dump using Mimikatz (p. 105)
- Windows 10 (LSA) Credential Dump (p. 109)
- PowerShell Empire (p. 118)
- Koadic (p. 119)
- Metasploit (p. 120)
- CrackMapExec (p. 122)
- PowerShell Empire (p. 125)
- Meterpreter Framework (p. 126)
- Koadic (p. 127)
- What is DCSYNC Attack (p. 129)
- Mimikatz (p. 129)
- PowerShell Empire (p. 133)
- Metasploit (p. 135)
- Configuration (p. 138)
- Metasploit (p. 142)
- PowerShell Empire (p. 143)
- Domain Cache credential (DCC2) (p. 145)
- Metasploit (p. 145)
- Impacket (p. 146)
- Mimikatz (p. 147)
- PowerShell Empire (p. 148)
- Koadic (p. 149)
- Python Script (p. 150)
- Cracking DCC2 or MACHACHE2/MSCASH2 (p. 151)
- Introduction (p. 153)
- FTP (p. 153)
- Telnet (p. 155)
- VNC (p. 156)
- SMB (p. 157)
- POP3 (p. 162)
- SMTP (p. 163)
- PostgreSQL (p. 164)
- MsSQL (p. 165)
- MySQL (p. 167)
- Reference (p. 172)
- About Us (p. 174)
- Visual & Network Diagram Intelligence (`credential_dumping.pdf#page1`)
- Visual & Network Diagram Intelligence (`credential_dumping.pdf#page8`)
- Visual & Network Diagram Intelligence (`credential_dumping.pdf#page17`)

