---
title: "Trained Knowledge & Topology: CQC001_E030_M050_transcript.pdf"
tags:
  - auditpol
  - credential_access
  - kerberos
  - mdp
  - pdf
  - trained
source_file: CQC001_E030_M050_transcript.pdf
doc_type: pdf
updated: 2026-10-25 00:57:38
---

# Trained Knowledge & Architecture: `CQC001_E030_M050_transcript.pdf`

- **Source Path:** `~/Projects/CORA/Training/CQC001_E030_M050_transcript.pdf` (`pdf`)
- **Extracted Technical Entities:** `auditpol, kerberos`
- **Extracted IPs / Subnets:** `None`
- **Extracted Interfaces:** `None`
- **Linked Command Playbook:** [[commands/trained_cqc001_e030_m050_transcript]] (`1` CEGAR-verified commands | `1` MDP transitions)

## Command & Tactic Coverage Summary
- **Total CEGAR-Verified Commands:** `1` (full executable list in [[commands/trained_cqc001_e030_m050_transcript]])
- **Tactic Distribution:** `Credential_Access` (1)
- **Top Extracted CLI Tools:** `handle` (1)

## LLM Distilled Operational Summary
### Operational Techniques & Decision Workflows

*   **Enabling/Disabling Auditing**:
    *   To enable: `auditpol /enable`
    *   To disable: `auditpol /disable`
    *   *Note*: Windows 2003/Vista+ have auditing enabled by default; XP and earlier have it disabled by default.
*   **Audit Policy Configuration**:
    *   Managed via **Local Security Policy Editor** (GUI) or **Registry**.
    *   **LSASS** receives policies from the **Security Reference Monitor (SRM)**.
    *   **SRM** sends records to the **Event Logger**, which writes them to the **Security Log**.
    *   Records are queued and sent to the **Local Security Authority (LSA)** immediately upon receipt, not in batches.
*   **Data Transfer Mechanisms**:
    *   **< 256 bytes**: Sent as an **LPC (Local Procedure Call)** message.
    *   **> 256 bytes**: SRM uses **shared memory** and passes a pointer to the LPC message.
*   **Registry Inspection**:
    *   Administrators must adjust permissions on specific registry keys to view audit settings.
    *   Values indicate status: `1` (Success), `2` (Failure), `3` (Both). Bit `Z` indicates if the policy is enabled (`1`) or disabled (`0`).

### Critical Command Patterns

*   `auditpol /enable`
*   `auditpol /disable`

### Network Topology & Service Relationships

*   **Primary Log**: **Security Log** (where audit records are written).
*   **Key Services/Components**:
    *   **LSASS** (Local Security Authority Subsystem): Maintains Local Security Policy.
    *   **SRM** (Security Reference Monitor): Receives policy updates and manages record flow.
    *   **Event Logger**: Writes final records to the Security Log.
    *   **LSA** (Local Security Authority): Receives queued audit records.
*   **ACL Structure**:
    *   **DACL** (Direct Access Control List): Stores access permissions (e.g., Read/Write).
    *   **SACL** (System Access Control List): Stores auditing permissions (Success/Failure events).

## Extracted Operational Steps & Workflows
- 1. From a command prompt, enter auditpol /enable.
- 2. Use the graphical user interface (GUI) to choose the objects to audit.
- 1. When the system initializes (or when policy changes), the LSASS sends messages to the
- 2. The LSASS receives the audit records from the SRM, edits the records to add pertinent details,
- 3. The Event Logger writes the audit records to the Security Log.
- 1. If the audit record is smaller than 256 bytes, then it is sent as an LPC message.
- 2. If the audit record is larger than 256 bytes, then the SRM uses shared memory to make the

