---
title: "Trained Knowledge & Topology: CQC001_E030_M050_Auditing_Policy_Settings.pdf"
tags:
  - https
  - mdp
  - pdf
  - trained
source_file: CQC001_E030_M050_Auditing_Policy_Settings.pdf
doc_type: pdf
updated: 2026-10-25 00:57:38
---

# Trained Knowledge & Architecture: `CQC001_E030_M050_Auditing_Policy_Settings.pdf`

- **Source Path:** `~/Projects/CORA/Training/CQC001_E030_M050_Auditing_Policy_Settings.pdf` (`pdf`)
- **Extracted Technical Entities:** `https`
- **Extracted IPs / Subnets:** `None`
- **Extracted Interfaces:** `None`

## LLM Distilled Operational Summary
### Key Operational Techniques & Decision Workflows
*   **Registry Inspection**: Determine audit settings by reading `HKEY_LOCAL_MACHINE\Security\Policy\PolAdtEv`.
*   **Permission Prerequisite**: Administrators must manually modify registry key permissions to access the audit policy string, as default access is restricted.
*   **Policy State Verification**: Check the `Z` value to confirm if the audit policy is globally enabled (`1`) or disabled (`0`).
*   **Event Category Decoding**: Parse the string of numbers where specific positions correspond to event categories (A–G).
*   **Success/Failure Logic**: Interpret category values: `1` = Success only, `2` = Failure only, `3` = Both.
*   **Edge Case Handling**: Recognize that a policy can be enabled but configured to audit nothing (all category values = `0`).

### Critical Command Patterns and Required Flags
*   **Registry Path**: `HKEY_LOCAL_MACHINE\Security\Policy\PolAdtEv`
*   **Data Format**: Hexadecimal string representing a bitmask structure.
*   **Category Mapping**:
    *   **A**: Restart, Shutdown, System
    *   **B**: Logons and Logoffs
    *   **C**: File and Object Access
    *   **D**: Use of User Rights
    *   **E**: Process Tracking
    *   **F**: Security Policy Management
    *   **G**: User and Group Management
*   **Value Interpretation**:
    *   `Z=1`: Policy Enabled
    *   `Z=0`: Policy Disabled
    *   `A-G=1`: Success Auditing Enabled
    *   `A-G=2`: Failure Auditing Enabled
    *   `A-G=3`: Success and Failure Auditing Enabled

### Network Topology & Service Relationships
*   **Storage Location**: Local Machine Registry (no network dependency for storage).
*   **Access Control**: Requires elevated privileges to read/write the specific registry key.
*   **Reference Resources**:
    *   Primary: `CQC001_E030_M050_Auditing_Policy_Settings.pdf`
    *   Secondary: `https://web.archive.org/web/20160306051121/https://www.kazamiya.net/files/PolAdtEv_Structure_en_rev2.pdf`

