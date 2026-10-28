---
title: "Trained Knowledge & Topology: Find.pdf"
tags:
  - enumeration
  - https
  - mdp
  - passive_enum
  - pdf
  - trained
source_file: Find.pdf
doc_type: pdf
updated: 2026-10-24 00:58:23
---

# Trained Knowledge & Architecture: `Find.pdf`

- **Source Path:** `~/Projects/CORA/Training/Find.pdf` (`pdf`)
- **Extracted Technical Entities:** `https`
- **Extracted IPs / Subnets:** `None`
- **Extracted Interfaces:** `None`
- **Linked Command Playbook:** [[commands/trained_find]] (`4` CEGAR-verified commands | `4` MDP transitions)

## Command & Tactic Coverage Summary
- **Total CEGAR-Verified Commands:** `4` (full executable list in [[commands/trained_find]])
- **Tactic Distribution:** `Enumeration` (3), `Passive_Enum` (1)
- **Top Extracted CLI Tools:** `find` (3), `dir` (1)

## LLM Distilled Operational Summary
### Key Operational Techniques & Decision Workflows
*   **Case Sensitivity Handling**: By default, `find` is case-sensitive. To treat "a" and "A" as identical, append the `/i` flag. Without `/i`, exact character matching is required.
*   **Handling Embedded Quotes**: When searching for strings containing literal quotation marks (e.g., `"String"`), wrap the entire search term in outer quotes and double-escape the inner quotes (e.g., `"He said ""Hello"""`).
*   **Filtering vs. File Search**: Omitting a file name allows `find` to act as a filter, reading from standard input (keyboard, pipe, or redirect) rather than specific files.
*   **Carriage Return Awareness**: The command does not recognize carriage returns. Search strings must be continuous text unlikely to be split by line breaks (e.g., avoid searching for "tax file" if a line break exists between them).
*   **Wildcard Usage**: Direct wildcards (`*`, `?`) in file names are unsupported. Use a `for` loop to iterate over wildcard patterns before piping to `find`.
*   **Parameter Ordering**: Command-line options (e.g., `/v`, `/c`, `/n`, `/i`) can be placed in any order relative to the string and file arguments.

### Critical Command Patterns and Required Flags
*   **Basic Search**: `find "string" [Drive:][Path]FileName`
*   **Case-Insensitive Search**: Append `/i` (e.g., `find /i "CPU" file.txt`).
*   **Count Matches**: Append `/c` to display the total count of matching lines.
*   **Invert Match (Negative Search)**: Append `/v` to display lines that *do not* contain the string.
*   **Line Numbering**: Append `/n` to prefix each matching line with its file line number.
    *   *Note*: Using `/c` and `/n` together causes `/n` to be ignored.
*   **Combined Count/Invert**: Using `/c` and `/v` together counts the lines that *do not* contain the string.

### Network Topology & Service Relationships
*   **Input Sources**: When used as a filter, `find` accepts input from:
    *   Standard Input (Keyboard)
    *   Pipes (`|`) from other commands (e.g., `dir | find`)
    *   Redirected files
*   **Directory Scanning**: To search an entire drive (e.g., `C:`), pipe the output of `dir` with the `/s` (subdirectories) and `/b` (bare names) flags into `find`.
    *   Example: `dir c:\ /s /b | find "CPU"`
*   **Batch File Iteration**: Use a `for` loop to apply `find` across multiple files matching a pattern (e.g., all `.bat` files).
    *   Example: `for %f in (*.bat) do find "PROMPT" %f`

