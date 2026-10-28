---
title: "Trained Command Playbook: PowerView.pdf"
tags:
  - covert_infil
  - credential_access
  - enumeration
  - http
  - https
  - john
  - kerberos
  - mdp
  - pdf
  - post_exploitation_verification
  - powershell
  - trained
source_file: PowerView.pdf
updated: 2026-10-24 01:00:09
---

# Trained Command Playbook: `PowerView.pdf`

- **Source Document:** `~/Projects/CORA/Training/PowerView.pdf`
- **CEGAR Verified Commands:** `24` (`0` malformed/unsafe snippets filtered)
- **MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`):** `24`
- **Discovered IPs/Subnets:** `None`
- **Discovered Interfaces:** `None`
- **Related Knowledge Note:** [[knowledge/trained_powerview]]

## Distilled MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`)
| Pre-State ($s$) | Tactic ($\tau$) | Technique ($k$) | Tool ($u$) | Post-State ($s'$) | Verified Command ($c$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `import-module` | `s_active_services_enumerated` | `Import-Module powerview.ps1` |
| `s_cross_subnet_pivot_routed` | **`Post_Exploitation_Verification`** | Post-Action Host Identity, Privilege & Objective Verification | `invoke-*` | `s_goal_verified_complete` | `Invoke-*` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `new-object` | `s_credentials_or_certs_acquired` | `$Cred = New-Object` |
| `s_protocol_chain_established` | **`Covert_Infil`** | Staged Artifact / Encapsulated Ingress Delivery | `get-domainou` | `s_covert_infil_channel_ready` | `Get-DomainOU` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `get-*` | `s_active_services_enumerated` | `Get-*` |
| `s_cross_subnet_pivot_routed` | **`Post_Exploitation_Verification`** | Post-Action Host Identity, Privilege & Objective Verification | `find` | `s_goal_verified_complete` | `Find groups w/` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `get-domainuser` | `s_credentials_or_certs_acquired` | `Get-DomainUser -Credential $Cred` |
| `s_protocol_chain_established` | **`Covert_Infil`** | Staged Artifact / Encapsulated Ingress Delivery | `get-domaingpo` | `s_covert_infil_channel_ready` | `Get-DomainGPO` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `find-*` | `s_active_services_enumerated` | `Find-*` |
| `s_active_services_enumerated` | **`Credential_Access`** | Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations | `get-domain` | `s_credentials_or_certs_acquired` | `Get-Domain` |
| `s_protocol_chain_established` | **`Covert_Infil`** | Staged Artifact / Encapsulated Ingress Delivery | `get-domainfileserver` | `s_covert_infil_channel_ready` | `Get-DomainFileServer` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `set-*` | `s_active_services_enumerated` | `Set-*` |
| `s_protocol_chain_established` | **`Covert_Infil`** | Staged Artifact / Encapsulated Ingress Delivery | `get-netshare` | `s_covert_infil_channel_ready` | `Get-NetShare <X>` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `get-forest` | `s_active_services_enumerated` | `Get-Forest` |
| `s_protocol_chain_established` | **`Covert_Infil`** | Staged Artifact / Encapsulated Ingress Delivery | `get-netsession` | `s_covert_infil_channel_ready` | `Get-NetSession <X>` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `get-forestdomain` | `s_active_services_enumerated` | `Get-ForestDomain` |
| `s_protocol_chain_established` | **`Covert_Infil`** | Staged Artifact / Encapsulated Ingress Delivery | `get-netrdpsession` | `s_covert_infil_channel_ready` | `Get-NetRDPSession <X>` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `get-foresttrust` | `s_active_services_enumerated` | `Get-ForestTrust` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `get-domaintrust` | `s_active_services_enumerated` | `Get-DomainTrust` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `get-domaintrustmapping` | `s_active_services_enumerated` | `Get-DomainTrustMapping` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `get-domainforeignuser` | `s_active_services_enumerated` | `Get-DomainForeignUser` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `get-` | `s_active_services_enumerated` | `Get-` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `find-domainuserlocation` | `s_active_services_enumerated` | `Find-DomainUserLocation (old Invoke-UserHunter) will` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `find-domainshare` | `s_active_services_enumerated` | `Find-DomainShare (old Invoke-ShareFinder) will use` |

## Verified Executable Commands (Grouped by Capability Layer)

### General_System (24 commands)
```bash
Import-Module powerview.ps1
Get-*
Find-*
Set-*
Invoke-*
$Cred = New-Object
Get-DomainUser -Credential $Cred
Get-Forest
Get-ForestDomain
Get-ForestTrust
Get-Domain
Get-DomainTrust
Get-DomainTrustMapping
Get-DomainForeignUser
Find groups w/
Get-
Find-DomainUserLocation (old Invoke-UserHunter) will
Find-DomainShare (old Invoke-ShareFinder) will use
Get-DomainOU
Get-DomainGPO
Get-DomainFileServer
Get-NetShare <X>
Get-NetSession <X>
Get-NetRDPSession <X>
```

