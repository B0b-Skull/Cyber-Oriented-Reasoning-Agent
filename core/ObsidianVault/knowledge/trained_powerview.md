---
title: "Trained Knowledge & Topology: PowerView.pdf"
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
doc_type: pdf
updated: 2026-10-24 01:00:09
---

# Trained Knowledge & Architecture: `PowerView.pdf`

- **Source Path:** `~/Projects/CORA/Training/PowerView.pdf` (`pdf`)
- **Extracted Technical Entities:** `http, https, john, kerberos, powershell`
- **Extracted IPs / Subnets:** `None`
- **Extracted Interfaces:** `None`
- **Linked Command Playbook:** [[commands/trained_powerview]] (`24` CEGAR-verified commands | `24` MDP transitions)

## Command & Tactic Coverage Summary
- **Total CEGAR-Verified Commands:** `24` (full executable list in [[commands/trained_powerview]])
- **Tactic Distribution:** `Enumeration` (13), `Covert_Infil` (6), `Credential_Access` (3), `Post_Exploitation_Verification` (2)
- **Top Extracted CLI Tools:** `find` (1), `find-*` (1), `find-domainshare` (1), `find-domainuserlocation` (1), `get-` (1), `get-*` (1), `get-domain` (1), `get-domainfileserver` (1), `get-domainforeignuser` (1), `get-domaingpo` (1), `get-domainou` (1), `get-domaintrust` (1), `get-domaintrustmapping` (1), `get-domainuser` (1), `get-forest` (1), `get-forestdomain` (1), `get-foresttrust` (1), `get-netrdpsession` (1), `get-netsession` (1), `get-netshare` (1), `import-module` (1), `invoke-*` (1), `new-object` (1), `set-*` (1)

## LLM Distilled Operational Summary
### Operational Techniques & Workflows

*   **Module Loading & Execution**:
    *   **Standard**: `Import-Module powerview.ps1` (requires PowerShell bypass on non-domain machines).
    *   **Cobalt Strike**: `beacon> powershell-import /local/path/to/PowerView.ps1`.
    *   **Remote Execution**: Use `runas /netonly` or configure DNS to point to the Domain Controller (DC).
*   **Data Retrieval Workflow**:
    *   **Full Objects**: Use `Get-*` commands (e.g., `Get-DomainUser`) for raw data.
    *   **Specific Entries**: Use `Find-*` commands for targeted enumeration.
    *   **Modification**: Use `Add-*` or `Set-*` verbs to alter AD objects.
    *   **ACL Resolution**: Use `Get-DomainObjectACL` with `-ResolveGUIDs` to map ACE GUIDs to display names.
*   **User Hunting Workflow**:
    *   **Location Discovery**: Use `Find-DomainUserLocation` (legacy: `Invoke-UserHunter`) to locate users via LDAP/API calls.
    *   **Targeting**: Specify `-UserIdentity` for specific users or `-UserGroupIdentity` for group-based hunting.
    *   **Stealth Mode**: Use `-Stealth` to limit queries to session information from file servers/DCs.
    *   **Local Admin Check**: Verify local admin access for the current user on target computers.

### Critical Command Patterns & Flags

*   **Common Query Flags**:
    *   `-Identity <X>`: The primary object to query (supports wildcards like `*john*`).
    *   `-Verbose`: Display debug/status information.
    *   `-Domain <X>`: Query a foreign domain (e.g., `foreign.com`).
    *   `-LDAPFilter '...'`: Utilize custom LDAP filters.
    *   `-Properties <prop1,prop2>`: Return only specified properties.
    *   `-SearchBase "..."`: Search within a specific OU or Global Catalog (`GC://domain.com`).
    *   `-Server "..."`: Bind to a specific server for the search.
    *   `-SecurityMasks [Dacl/Owner/Sacl]`: Filter returned security information.
    *   `-FindOne`: Return only a single result.
    *   `-Credential <PSCredential>`: Authenticate using alternate credentials.
*   **Output Handling**:
    *   **List View**: `… | fl`
    *   **Wrapped Table**: `… | ft -wrap`
    *   **CSV Export**: `… | Export-CSV -NoTypeInformation out.csv`
    *   **XML Object**: `… | Export-Clixml obj.xml` (Read via `Import-Clixml`).
    *   **File Output**: `… | Out-File -Encoding Ascii out.txt`.
    *   **Threaded Execution**: `… | %{…Invoke-Command $_ }`.
    *   **Field Filtering**: `… | ? {$_.Field –eq X}`.

### Network Topology & Relationships

*   **Domain Trusts**:
    *   **Forest Level**: `Get-Forest` (current forest info

