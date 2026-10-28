---
title: "Trained Knowledge & Topology: BCF_Autopsy Configuration and Setup.pdf"
tags:
  - mdp
  - pdf
  - trained
source_file: BCF_Autopsy Configuration and Setup.pdf
doc_type: pdf
updated: 2026-10-24 00:56:18
---

# Trained Knowledge & Architecture: `BCF_Autopsy Configuration and Setup.pdf`

- **Source Path:** `~/Projects/CORA/Training/BCF_Autopsy Configuration and Setup.pdf` (`pdf`)
- **Extracted Technical Entities:** `general`
- **Extracted IPs / Subnets:** `None`
- **Extracted Interfaces:** `None`

### Visual & Network Diagram Intelligence (`BCF_Autopsy Configuration and Setup.pdf#page1`)
- **Spatially Grouped Diagram Nodes (Box/Component Clusters):**
  1. `[ICHIRON | TRAINING]`
  2. `[Basic Computer Forensics | 26-28Mar2018 | DISCOVERYANDCOUNTER-INFILTRATIONPROFESSIONALTM(DCIP)TM]`

### Visual & Network Diagram Intelligence (`BCF_Autopsy Configuration and Setup.pdf#page2`)
- **Spatially Grouped Diagram Nodes (Box/Component Clusters):**
  1. `[Autopsy | Intro and Features]`
  2. `[OVERVIEW]`
  3. `[Ingest Modules]`

## LLM Distilled Operational Summary
### Operational Workflows & Decision Logic

*   **Case Initialization**: Begin by creating a new case, defining the case name, base directory, and examiner identity.
*   **Data Source Ingestion**: Add a data source by selecting either a local device or an image file (supporting raw and EnCase E01 formats).
*   **Ingest Module Selection**: Configure automated analysis by selecting specific ingest modules. Note that increasing the number of selected modules extends the processing time.
*   **Rule-Based Filtering**: Utilize "Interesting Files Identifier" to define custom rules (e.g., Type: Directory, Name: Backup, Path: AppleComputer/MobileSync) to generate alerts for specific file patterns, particularly useful for iPhone backups.
*   **Post-Ingest Verification**: Run the E01 Verifier module to compute checksums against internal values, flagging only corrupted or mismatched images.

### Critical Command Patterns & Module Flags

*   **Recent Activity**: Enables extraction of user activity from web browsers, installed programs, and OS logs; automatically runs Regripper.
*   **Hash Lookup**: Calculates MD5 hashes and cross-references them against NIST NSRL or custom hashsets to identify "known bad" or "known" files.
*   **File Type Identification**: Uses the Tika library to detect internal file signatures, ignoring extensions. Essential prerequisite for the Extension Mismatch Detector.
*   **Embedded File Extraction**: Processes archives (ZIP, RAR) and Office documents (DOCX, XLSX, etc.) to feed contents back into the ingest pipeline for keyword searching.
*   **EXIF Parser**: Extracts metadata including geolocation, timestamps, and camera models from image files.
*   **Email Parser**: Identifies and extracts content/attachments from Thunderbird MBOX and PST formats.
*   **Extension Mismatch Detector**: Flags files where the detected internal type differs from the file extension.
*   **PhotoRec Carver**: Recovers files from unallocated space.
*   **Keyword Search**: Supports built-in or custom keyword lists to search file contents.

### Network Topology & Service Relationships

*   **Spatial Grouping**: The environment is organized into clusters labeled `[ICHIRON | TRAINING]` and `[Basic Computer Forensics | 26-28Mar2018 | DCIP]`.
*   **Module Dependencies**:
    *   `File Type Identification` (Tika) must run before `Extension Mismatch Detector`.
    *   `Embedded File Extraction` feeds results back into the main `Ingest Modules` pipeline.
    *   `Recent Activity` implicitly triggers `Regripper` execution.
*   **Data Source Formats**: Supports native raw images and EnCase `.E01` formats, with specific verification logic required for `.E01` files.

## Document Structure & Key Topics
- Visual & Network Diagram Intelligence (`BCF_Autopsy Configuration and Setup.pdf#page1`)
- Visual & Network Diagram Intelligence (`BCF_Autopsy Configuration and Setup.pdf#page2`)

