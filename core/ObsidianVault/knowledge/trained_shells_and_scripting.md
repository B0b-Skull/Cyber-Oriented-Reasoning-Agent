---
title: "Trained Knowledge & Topology: Shells_and_Scripting.pdf"
tags:
  - credential_access
  - enumeration
  - http
  - https
  - mdp
  - passive_enum
  - pdf
  - trained
source_file: Shells_and_Scripting.pdf
doc_type: pdf
updated: 2026-10-24 01:00:25
---

# Trained Knowledge & Architecture: `Shells_and_Scripting.pdf`

- **Source Path:** `~/Projects/CORA/Training/Shells_and_Scripting.pdf` (`pdf`)
- **Extracted Technical Entities:** `http, https`
- **Extracted IPs / Subnets:** `None`
- **Extracted Interfaces:** `None`
- **Linked Command Playbook:** [[commands/trained_shells_and_scripting]] (`8` CEGAR-verified commands | `8` MDP transitions)

## Command & Tactic Coverage Summary
- **Total CEGAR-Verified Commands:** `8` (full executable list in [[commands/trained_shells_and_scripting]])
- **Tactic Distribution:** `Enumeration` (6), `Credential_Access` (1), `Passive_Enum` (1)
- **Top Extracted CLI Tools:** `echo` (5), `cat` (1), `erase` (1), `history` (1)

## LLM Distilled Operational Summary
### Operational Techniques & Decision Workflows

*   **File I/O & Redirection**: Use `>` for output redirection, `<` for input redirection, and `>>` for appending. Combine stdout and stderr using `>file 2>&1` or `>&file`.
*   **Process Management**: Launch background processes with `&`, resume them with `fg`, list active jobs via `jobs`, and terminate with `kill`. Use `bg` to resume a job in the background and `wait` to synchronize completion.
*   **Shell Execution & Environment**: Execute commands in a subshell using `( )`, run a new shell with `exec`, and source files using `. file` or `source file`. Manage environment variables with `export` and unset them with `unset`.
*   **Loop Control**: Terminate loops with `break` (bash/ksh) or `end` (tcsh), and skip iterations with `continue`.
*   **Conditional Logic**: Evaluate conditions using `[ expression ]` or the preferred `[[ expression ]]` syntax for grouping and operator precedence. Use `&&` and `||` for logical AND/OR operations.

### Critical Command Patterns & Required Flags

*   **Variable Expansion**:
    *   Simple: `$VAR` or `${VAR}`
    *   Indirection: `${!VAR}`
    *   Default/Alternate: `${VAR:-default}` or `${VAR+alt}`
    *   Error on Null: `${VAR:?msg}`
    *   Substring/Removal: `${VAR#pattern}`, `${VAR%pattern}`
*   **String Manipulation**:
    *   Length: `${#VAR}`
    *   Slice: `${VAR:offset:length}`
    *   Replace: `${VAR/pattern/replacement}` (single) or `${VAR//pattern/replacement}` (all).
    *   Case Change: `${VAR^}` (first char), `${VAR^^}` (all upper), `${VAR,}` (first lower), `${VAR,,}` (all lower).
*   **Bash Specifics**:
    *   Grouping: `( expr )`
    *   Logical Ops: `expr1 && expr2`, `expr1 || expr2`
    *   Pattern Matching: `STRING == PATTERN`, `STRING != PATTERN`, `STRING =~ ERE`

### Network Topology & Service Relationships

*   **Directory Navigation**: Switch directories using `cd`, `cd ~-` (previous), and `popd/pushd` (stack-based).
*   **Command History & Editing**: List history with `history`, redo last command with `!!` or `fc -s`, and edit/redo specific commands with `fc -s str` or `!str`.
*   **Alias & Hashing**: Define aliases with `alias x=y`, display hashed commands with `hash`, and reset locations with `hash -r` or `unhash`.
*   **Resource Limits**: Set limits using `ulimit` (bash/ksh) or `limit` (tcsh).
*   **Input/Interrupt Handling**: Read from stdin with `read`, ignore interrupts via `trap INTR`, and handle signals with `onintr` (tcsh).

## Document Structure & Key Topics
- Background execution
- write the string “1234567890” to file output.txt
- open “output.txt” and assign fd 3 to it
- read 4 characters from open file with file descriptor (fd) 3. File
- write a decimal point at the file pointer position
- close fd 3
- output on the screen will be: 1234.67890

