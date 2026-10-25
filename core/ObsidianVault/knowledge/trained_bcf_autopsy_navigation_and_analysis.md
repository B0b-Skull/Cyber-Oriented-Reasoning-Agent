---
title: "Trained Knowledge & Topology: BCF_Autopsy Navigation and Analysis.pdf"
tags:
  - mdp
  - pdf
  - trained
source_file: BCF_Autopsy Navigation and Analysis.pdf
doc_type: pdf
updated: 2026-10-25 00:56:25
---

# Trained Knowledge & Architecture: `BCF_Autopsy Navigation and Analysis.pdf`

- **Source Path:** `~/Projects/CORA/Training/BCF_Autopsy Navigation and Analysis.pdf` (`pdf`)
- **Extracted Technical Entities:** `general`
- **Extracted IPs / Subnets:** `None`
- **Extracted Interfaces:** `None`

### Visual & Network Diagram Intelligence (`BCF_Autopsy Navigation and Analysis.pdf#page1`)
- **Spatially Grouped Diagram Nodes (Box/Component Clusters):**
  1. `[ICHIRON | TRAINING]`
  2. `[Basic Computer Forensics | 26-28Mar2018 | DISCOVERYANDCOUNTER-INFILTRATIONPROFESSIONALTM(DCIP)TM]`

### Visual & Network Diagram Intelligence (`BCF_Autopsy Navigation and Analysis.pdf#page2`)
- **Spatially Grouped Diagram Nodes (Box/Component Clusters):**
  1. `[Autopsy | Navigation]`
  2. `[OVERVIEW]`
  3. `[Analysis | Reporting]`

## LLM Distilled Operational Summary
### Operational Techniques & Decision Workflows
*   **Navigation Hierarchy:** Follow the strict flow: `Tree Viewer` (discovered folders/ingest results) → `Result Viewer` (file attributes/full path) → `Content Viewer` (context-aware data).
*   **Tree Viewer Actions:** Expand/contract discovered folders and ingest module results to drive the Result Viewer.
*   **Result Viewer Actions:** Select files from the Tree Viewer list to view attributes, full paths, or thumbnails.
*   **Content Viewer Actions:** Inspect images, video, hex, text, extracted strings, and metadata.
*   **Image Viewer Configuration:** Enable the "EXIF, File Type and Hash Sets" module and group results by category for child-exploitation cases.
*   **Tagging Workflow:** Right-click any file/object to create a reference. Use "Quick Tag" or "Tag and Comment" to annotate items.
*   **Reporting Workflow:** Navigate to `Tools` → `Generate Report`. Select scope (All or Tagged results) and format (HTML).

### Critical Command Patterns & Required Flags
*   **File Search by Attributes:** Utilize the built-in search tools filtering by:
    *   Name
    *   Size
    *   MIME Type
    *   Date Range
    *   Hash Set ID
*   **Report Generation Command:** `Tools` > `Generate Report` (Flags: Scope = All/Tagged, Format = HTML).

### Network Topology & Relationships
*   **Training Context:** `ICHIRON | TRAINING` and `DCIP` (Discovery and Counter-Infiltration Professional) associated with the `Basic Computer Forensics` course (26-28 Mar 2018).
*   **Module Dependencies:** The `Image Viewer` requires the `EXIF, File Type and Hash Sets` module to be explicitly enabled.
*   **Data Flow:** `Tree Viewer` results directly drive the `Result Viewer`; `Result Viewer` selections drive the `Content Viewer`.

## Document Structure & Key Topics
- Visual & Network Diagram Intelligence (`BCF_Autopsy Navigation and Analysis.pdf#page1`)
- Visual & Network Diagram Intelligence (`BCF_Autopsy Navigation and Analysis.pdf#page2`)

