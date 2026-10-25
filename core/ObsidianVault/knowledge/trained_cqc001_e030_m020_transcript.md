---
title: "Trained Knowledge & Topology: CQC001_E030_M020_transcript.pdf"
tags:
  - active_enum
  - credential_access
  - dsquery
  - enumeration
  - mdp
  - passive_enum
  - pdf
  - privilege_escalation
  - trained
source_file: CQC001_E030_M020_transcript.pdf
doc_type: pdf
updated: 2026-10-25 00:57:35
---

# Trained Knowledge & Architecture: `CQC001_E030_M020_transcript.pdf`

- **Source Path:** `~/Projects/CORA/Training/CQC001_E030_M020_transcript.pdf` (`pdf`)
- **Extracted Technical Entities:** `dsquery`
- **Extracted IPs / Subnets:** `None`
- **Extracted Interfaces:** `None`
- **Linked Command Playbook:** [[commands/trained_cqc001_e030_m020_transcript]] (`38` CEGAR-verified commands | `38` MDP transitions)

## Command & Tactic Coverage Summary
- **Total CEGAR-Verified Commands:** `38` (full executable list in [[commands/trained_cqc001_e030_m020_transcript]])
- **Tactic Distribution:** `Active_Enum` (21), `Enumeration` (11), `Credential_Access` (4), `Passive_Enum` (1), `Privilege_Escalation` (1)
- **Top Extracted CLI Tools:** `dsquery` (11), `dsget` (10), `dsmod` (8), `dsadd` (6), `csvde` (2), `ldifde` (1)

## LLM Distilled Operational Summary
### Active Directory Logical Structure
*   **Domain**: The core logical unit; a namespace where resources (users, computers, printers) share a single AD database.
*   **Namespace**: Shared naming convention (e.g., `PC1.abccorp.com`) within a domain.
*   **Multi-Domain Environments**: Separate databases exist per domain, though resource sharing is possible across them.

### Active Directory Physical Structure
*   **Domain Controllers (DC)**: Servers running Active Directory Domain Services that hold a writable copy of the AD database.
*   **Replication Mechanism**:
    *   **Method**: Pull-based replication initiated by the DC after a change (15s delay in Windows 2003, 5min in Windows 2000).
    *   **Optimization**: Compresses data and optimizes for WAN links.
    *   **Model**: Multimaster (each DC is an authority; changes replicate to all).
*   **DC Roles**: Authentication, access determination, collision detection, fault tolerance, and session management.

### Active Directory Objects & Schema
*   **Objects**: Distinctly named sets of attributes representing network resources (users, groups, policies, printers, etc.).
    *   **GUID**: 128-bit unique identifier (guaranteed unique within a Forest, immutable even if DN changes).
    *   **DN (Distinguished Name)**: Unique LDAP identifier.
*   **Schema**: Defines object types and attributes; stored as objects themselves.
    *   **Schema Class Objects**: Templates defining possible AD objects; collections of attributes.
    *   **Schema Attribute Objects**: Define specific attributes for associated classes; defined once, used in multiple classes.

### Command Line & Interaction
*   **Toolset**: Module focuses on command-line tools for interacting with AD (specific tools like `dsquery`, `dsmod`, or `ldapsearch` are implied by the "Demonstrate the use of command line tools" learning objective, though specific syntax flags were not detailed in this chunk).

### Network Topology & Relationships
*   **Forest**: The highest-level container containing one or more domains; the scope of GUID uniqueness.
*   **Replication Topology**: Flexible Single-Master Operation (FSMO) roles exist (though not fully detailed in this chunk), meaning not all DCs are functionally equal despite being multimaster for data.

