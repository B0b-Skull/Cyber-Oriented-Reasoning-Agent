---
title: "Trained Knowledge & Topology: PolAdtEv_Structure_en_rev2.pdf"
tags:
  - kerberos
  - mdp
  - pdf
  - trained
source_file: PolAdtEv_Structure_en_rev2.pdf
doc_type: pdf
updated: 2026-10-25 01:00:01
---

# Trained Knowledge & Architecture: `PolAdtEv_Structure_en_rev2.pdf`

- **Source Path:** `~/Projects/CORA/Training/PolAdtEv_Structure_en_rev2.pdf` (`pdf`)
- **Extracted Technical Entities:** `kerberos`
- **Extracted IPs / Subnets:** `None`
- **Extracted Interfaces:** `None`

## LLM Distilled Operational Summary
### Operational Techniques & Decision Workflows

*   **Registry Path Identification**: Locate the Audit Policy structure at `HKLM\SECURITY\Policy\PolAdtEv`.
*   **Version-Specific Byte Mapping**:
    *   **Windows 7 / 2008 x64**: Use the "Default (Windows 7)" column for byte offsets.
    *   **Windows 2008 x86 / Vista**: Use the "Default (2008 x86)" or "Default (Vista)" columns.
*   **Audit Value Configuration**:
    *   `00 00`: No Auditing.
    *   `01 00`: Success only.
    *   `02 00`: Failure only.
    *   `03 00`: Success and Failure.
*   **Category/Subcategory Alignment**: Map specific hex offsets to logical categories (e.g., Offset `0x12` = Security State Change, Offset `0x22` = Logon).

### Critical Command Patterns & Required Flags

*   **Registry Modification**: Use `reg add` or `reg edit` targeting `HKLM\SECURITY\Policy\PolAdtEv`.
*   **Byte-Level Editing**: Modify the binary value at the specific offset (e.g., changing Offset `0x22` from `01 00` to `03 00`) to enable both Success and Failure auditing for Logon events.
*   **Verification**: Confirm changes by reading the hex value at the target offset; ensure it matches the desired state (e.g., `03 00`).

### Network Topology & Service Relationships

*   **Service Dependencies**:
    *   **IPsec Events**: Offsets `0x18` (Driver), `0x28` (Main Mode), `0x2A` (Quick Mode), and `0x2C` (Extended Mode) control IPsec auditing. Default is often `00 00` (No Auditing).
    *   **Directory Services**: Offsets `0x68` (Access), `0x6A` (Changes), and `0x6C` (Replication) manage AD-related auditing. Note differences between x86 and x64 defaults.
    *   **Kerberos**: Offsets `0x70` (Ticket Operations) and `0x72` (Auth Service) handle Kerberos event tracking.
*   **Platform Specifics**:
    *   **Windows 7/2008 x64**: Generally more permissive defaults (e.g., Logon `01 00`, Network Policy Server `03 00`).
    *   **Windows 2008 x86/Vista**: Often stricter or different defaults (e.g., Network Policy Server `03 00` vs `00 00` in x64; Logon `03 00` vs `01 00`).
*   **Detailed Tracking**: Offsets `0x78` through `0x86` cover Policy Changes and Detailed Tracking events, with defaults varying by OS version.

