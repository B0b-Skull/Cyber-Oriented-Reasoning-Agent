---
title: "Trained Knowledge & Topology: CQC001_E020_M020_NTFS_Cheat_Sheets.pdf"
tags:
  - enumeration
  - http
  - mdp
  - pdf
  - post_exploitation_verification
  - serial
  - trained
source_file: CQC001_E020_M020_NTFS_Cheat_Sheets.pdf
doc_type: pdf
updated: 2026-10-25 00:57:31
---

# Trained Knowledge & Architecture: `CQC001_E020_M020_NTFS_Cheat_Sheets.pdf`

- **Source Path:** `~/Projects/CORA/Training/CQC001_E020_M020_NTFS_Cheat_Sheets.pdf` (`pdf`)
- **Extracted Technical Entities:** `http, serial`
- **Extracted IPs / Subnets:** `None`
- **Extracted Interfaces:** `None`
- **Linked Command Playbook:** [[commands/trained_cqc001_e020_m020_ntfs_cheat_sheets]] (`2` CEGAR-verified commands | `2` MDP transitions)

## Command & Tactic Coverage Summary
- **Total CEGAR-Verified Commands:** `2` (full executable list in [[commands/trained_cqc001_e020_m020_ntfs_cheat_sheets]])
- **Tactic Distribution:** `Enumeration` (1), `Post_Exploitation_Verification` (1)
- **Top Extracted CLI Tools:** `attrib` (2)

## LLM Distilled Operational Summary
### Operational Techniques & Decision Workflows

*   **MFT Recovery Strategy**: Prioritize reading the `$MFTMirr` (Record 1) before the primary `$MFT` (Record 0) to guarantee data access in case of a single-sector failure.
*   **Metadata Consistency Restoration**: Utilize the `$LogFile` (Record 2) to restore metadata consistency after a system failure, noting that its size can be adjusted via `Chkdsk`.
*   **Cluster State Analysis**: Interpret the `$Bitmap` (Record 6) to determine the state of free and unused clusters on the volume.
*   **Security Descriptor Extraction**: Focus on the `$Secure` file (Record 9) to retrieve unique security descriptors for all files within the volume.
*   **Attribute Parsing Workflow**: When analyzing a File Record Segment, first check the **Flags** field for compression (`0x00FF`), sparseness (`0x8000`), or encryption (`0x4000`) before processing content.

### Critical Command Patterns & Required Flags

*   **Volume Inspection**: Use `Chkdsk` to inspect and potentially increase the size of the `$LogFile`.
*   **Attribute Identification**:
    *   `0x10`: Standard Information (timestamps, link count).
    *   `0x30`: File Name (supports long/short names and hard links).
    *   `0x50`: Security Descriptor (ownership/access control).
    *   `0x80`: Data (file content; typically one unnamed attribute per file).
    *   `0xC0`: Reparse Point (junctions, mount points, filter drivers).
*   **Form Code Interpretation**:
    *   `0x00`: Resident attribute (data stored within the MFT record).
    *   `0x01`: Non-resident attribute (data stored on disk clusters).

### Network Topology & Service Relationships

*   **System File Hierarchy**: The volume boot process relies on the **Boot Code** (ending with `55 AA`) and the **BIOS Parameter Block (BPB)** within the `$Boot` file (Record 7) to mount the volume.
*   **Legacy Compatibility**: The **Media Descriptor** in the boot sector indicates disk type: `0xF8` for fixed disks and `0xF0` for 3.5-inch floppy drives.
*   **Character Encoding**: The `$Upcase` file (Record 10) manages Unicode uppercase conversions for case-insensitive MS-DOS compatibility.
*   **Extended Features**: The `$Extend` file (Record 11) handles optional extensions such as quotas, reparse point data, and object identifiers.

