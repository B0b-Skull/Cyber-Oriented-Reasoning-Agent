---
title: "Trained Knowledge & Topology: CQC001_E030_M010_Well_Known_SIDs.pdf"
tags:
  - https
  - mdp
  - pdf
  - trained
source_file: CQC001_E030_M010_Well_Known_SIDs.pdf
doc_type: pdf
updated: 2026-10-25 00:57:35
---

# Trained Knowledge & Architecture: `CQC001_E030_M010_Well_Known_SIDs.pdf`

- **Source Path:** `~/Projects/CORA/Training/CQC001_E030_M010_Well_Known_SIDs.pdf` (`pdf`)
- **Extracted Technical Entities:** `https`
- **Extracted IPs / Subnets:** `None`
- **Extracted Interfaces:** `None`

## LLM Distilled Operational Summary
### 1. Key Operational Techniques & Decision Workflows
*   **SID Construction**: Combine a predefined **Identifier Authority** (e.g., `SECURITY_WORLD_SID_AUTHORITY`) with a **Relative Identifier (RID)** to construct a Well-Known SID.
*   **Runtime Verification**:
    1.  Call `AllocateAndInitializeSid` to build the target Well-Known SID using authority and RID constants.
    2.  Use `EqualSid` to compare the constructed SID against SIDs present in the user's access token.
    3.  Call `FreeSid` to release memory allocated by `AllocateAndInitializeSid`.
*   **Inheritable ACE Handling**: Utilize `CREATOR_OWNER` (S-1-3-0) or `CREATOR_GROUP_ID` (S-1-3-1) as placeholders in Access Control Entries (ACEs). The system dynamically replaces these with the actual creator's SID or primary group SID upon inheritance.

### 2. Critical Command Patterns and Required Flags
*   **Universal SIDs**:
    *   `S-1-0-0`: Null SID (empty group).
    *   `S-1-1-0`: World/Everyone (all users).
    *   `S-1-2-0`: Local (physically connected terminals).
    *   `S-1-3-0`: Creator Owner ID.
    *   `S-1-3-1`: Creator Group ID.
*   **Windows-Specific SIDs (Authority: S-1-5)**:
    *   `S-1-5-1`: Dial-up users.
    *   `S-1-5-2`: Network logon users.
    *   `S-1-5-3`: Batch job users.
    *   `S-1-5-4`: Interactive users.
    *   `S-1-5-6`: Service accounts.
    *   `S-1-5-7`: Anonymous/Null session logon.
    *   `S-1-5-8`: Proxy.
    *   `S-1-5-9`: Enterprise controllers.
    *   `S-1-5-10`: Principal Self.

### 3. Network Topology & Service Relationships
*   **Logon Type Mapping**: Specific SIDs correspond to distinct logon types:
    *   `S-1-5-2` maps to `LOGON32_LOGON_NETWORK`.
    *   `S-1-5-3` maps to `LOGON32_LOGON_BATCH`.
    *   `S-1-5-4` maps to `LOGON32_LOGON_INTERACTIVE`.
    *   `S-1-5-6` maps to `LOGON32_LOGON_SERVICE`.
*   **Session Isolation**: `SECURITY_LOGON_IDS_RID` (S-1-5-5-X-Y) ensures process isolation within a specific logon session, restricting access to window-station objects for that session only.
*   **Authority Hierarchy**:
    *   **Universal**: Authorities 0 (`S-1-0`), 1 (`S-1-1

