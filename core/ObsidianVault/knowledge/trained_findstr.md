---
title: "Trained Knowledge & Topology: Findstr.pdf"
tags:
  - https
  - mdp
  - passive_enum
  - pdf
  - trained
source_file: Findstr.pdf
doc_type: pdf
updated: 2026-10-25 00:58:23
---

# Trained Knowledge & Architecture: `Findstr.pdf`

- **Source Path:** `~/Projects/CORA/Training/Findstr.pdf` (`pdf`)
- **Extracted Technical Entities:** `https`
- **Extracted IPs / Subnets:** `None`
- **Extracted Interfaces:** `None`
- **Linked Command Playbook:** [[commands/trained_findstr]] (`9` CEGAR-verified commands | `9` MDP transitions)

## Command & Tactic Coverage Summary
- **Total CEGAR-Verified Commands:** `9` (full executable list in [[commands/trained_findstr]])
- **Tactic Distribution:** `Passive_Enum` (9)
- **Top Extracted CLI Tools:** `findstr` (9)

## LLM Distilled Operational Summary
### Operational Techniques & Decision Workflows

*   **Exact vs. Pattern Matching**: Decide between literal string search (`/l`) and regular expression search (`/r`). Use `/l` for fixed text (e.g., specific error codes) and `/r` for flexible pattern matching (e.g., finding all logs starting with "Error").
*   **Scope Definition**: Determine the search scope:
    *   **Single File**: Specify `FileName`.
    *   **Current Directory & Subdirectories**: Use `/s` to recurse.
    *   **Specific Directories**: Use `/d:dirlist` for a comma-delimited list.
*   **Case Sensitivity**: Default behavior is case-sensitive. Use `/i` to ignore case (e.g., finding "Windows" matches "windows").
*   **Output Filtering**:
    *   **Exact Matches Only**: Use `/x` to print only lines that match the entire string exactly.
    *   **Inverted Search**: Use `/v` to print lines that *do not* contain the match (useful for finding clean logs).
    *   **File-Only Output**: Use `/m` to list only filenames containing matches, or `/n` to include line numbers.
*   **Advanced Regex Construction**: Combine metacharacters for complex logic:
    *   `^` and `$` for line start/end.
    *   `.*` for any string between start and end.
    *   `[class]` and `[^class]` for character sets.
    *   `\<` and `\>` for word boundaries.
*   **Batch Processing**: Use `/g:file` to read search strings from a text file and `/f:file` to read target filenames from a list, piping output (`>`) to a results file.

### Critical Command Patterns & Required Flags

| Flag | Function | Example Pattern |
| :--- | :--- | :--- |
| `/b` | Match at **beginning** of line | `findstr /b "ERROR" logfile.txt` |
| `/e` | Match at **end** of line | `findstr /e ".txt" *.log` |
| `/l` | **Literal** search (no regex) | `findstr /l "C00D" file.txt` |
| `/r` | **Regex** search (default if `/l` absent) | `findstr /r "^[A-Z]" file.txt` |
| `/s` | Search **subdirectories** | `findstr /s "config" .` |
| `/i` | **Case-insensitive** | `findstr /i "admin" C:\Users\*` |
| `/x` | **Exact** line match | `findstr /x "User=Admin" config.ini` |
| `/v` | **Invert** (no match) | `findstr /v "Critical" audit.log` |
| `/n` | Show **line numbers** | `findstr /n "timeout" app.exe` |
| `/m` | Show **file names only** | `findstr /m "fail" *.log` |
| `/o` | Show **seek offset** (byte position) | `findstr /

