---
title: "Trained Knowledge & Topology: CQC001_E030_M030_S040_I020_ModExam_X030_C010_transcript.txt"
tags:
  - credential_access
  - enumeration
  - icacls
  - mdp
  - privilege_escalation
  - text
  - trained
source_file: CQC001_E030_M030_S040_I020_ModExam_X030_C010_transcript.txt
doc_type: text
updated: 2026-10-25 00:57:38
---

# Trained Knowledge & Architecture: `CQC001_E030_M030_S040_I020_ModExam_X030_C010_transcript.txt`

- **Source Path:** `~/Projects/CORA/Training/CQC001_E030_M030_S040_I020_ModExam_X030_C010_transcript.txt` (`text`)
- **Extracted Technical Entities:** `icacls`
- **Extracted IPs / Subnets:** `None`
- **Extracted Interfaces:** `None`
- **Linked Command Playbook:** [[commands/trained_cqc001_e030_m030_s040_i020_modexam_x030_c010_transcript]] (`5` CEGAR-verified commands | `5` MDP transitions)

## Command & Tactic Coverage Summary
- **Total CEGAR-Verified Commands:** `5` (full executable list in [[commands/trained_cqc001_e030_m030_s040_i020_modexam_x030_c010_transcript]])
- **Tactic Distribution:** `Credential_Access` (2), `Enumeration` (2), `Privilege_Escalation` (1)
- **Top Extracted CLI Tools:** `net` (2), `icacls` (1), `rd` (1), `w` (1)

## LLM Distilled Operational Summary
### Key Operational Techniques & Decision Workflows
*   **User Verification**: Confirm account status, expiration, and group memberships using `net user` to validate identity before access attempts.
*   **Permission Inheritance Analysis**: Use `icacls` with the `/T` flag to recursively inspect file permissions across directories, identifying explicit vs. inherited Access Control Entries (ACEs).
*   **ACE Ordering Logic**: Apply the canonical ACE ordering rule: Explicit Denials → Explicit Grants → Inherited Denials → Inherited Grants. This determines effective permissions when conflicts arise.
*   **Inheritance Control**: Utilize flags like `(OI)` (Object Inherit), `(CI)` (Container Inherit), and `(NP)` (No Propagate) to manage how permissions flow from parent containers to child objects.

### Critical Command Patterns and Required Flags
*   **User Enumeration**:
    *   `net user <username>`: Retrieves detailed user properties including active status, password policies, and group memberships.
*   **Recursive Permission Inspection**:
    *   `icacls <path> /T`: Recursively displays Access Control Entries for all files and subdirectories within the specified path.
*   **Permission Masks**:
    *   `N`: No access.
    *   `F`: Full access.
    *   `M`: Modify access.
    *   `RX`: Read and execute.
    *   `R`: Read-only.
    *   `W`: Write-only.
    *   `D`: Delete.
*   **Specific Rights (Comma-List Format)**:
    *   `DE`: Delete.
    *   `RC`: Read control.
    *   `WDAC`: Write DAC.
    *   `WO`: Write owner.
    *   `S`: Synchronize.
    *   `AS`: Access system security.
    *   `MA`: Maximum allowed.
    *   `GR`/`GW`/`GE`/`GA`: Generic read/write/execute/all.
    *   `RD`/`WD`/`AD`: Read/Write/Append data.
    *   `REA`/`WEA`: Read/Write extended attributes.
    *   `X`: Execute/traverse.
    *   `DC`: Delete child.
    *   `RA`/`WA`: Read/Write attributes.

### Network Topology, IP/Subnet, Serial, or Service Relationships
*   **User-to-Group Mapping**:
    *   **Bojangles**: Member of Local Group `*Jellyfish`, `*Ramp`.
    *   **Lilith**: Member of Local Group `*Cheese`, `*Jellyfish`.
*   **File-to-User Permission Matrix**:
    *   **random/Paris.txt**: `myPC\Lilith` has No access (`N`); `myPC\Jellyfish` has Read/Execute (`RX`); `myPC\Cheese` has Inherited Deny Write (`I)(DENY)(W)`).
    *   **random/Reno.txt**: `myPC\Ramp` has Deny Read/Write (`DENY)(R,W)`); `myPC\Bojangles` has Read/Execute/Write (`RX

