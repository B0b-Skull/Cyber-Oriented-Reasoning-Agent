---
title: "Trained Knowledge & Topology: Mod_14.pdf"
tags:
  - mdp
  - pdf
  - trained
source_file: Mod_14.pdf
doc_type: pdf
updated: 2026-10-25 00:59:21
---

# Trained Knowledge & Architecture: `Mod_14.pdf`

- **Source Path:** `~/Projects/CORA/Training/Mod_14.pdf` (`pdf`)
- **Extracted Technical Entities:** `general`
- **Extracted IPs / Subnets:** `None`
- **Extracted Interfaces:** `None`

## LLM Distilled Operational Summary
### Key Operational Techniques & Decision Workflows

*   **Context Switching Workflow**: When the scheduler allocates a time slice (approx. 0.1s) or a hardware interrupt occurs, the CPU switches from User Mode to Kernel Mode. This involves saving the current process status, re-evaluating priority (usually lowering it), and selecting a new runnable process.
*   **System Call Execution Flow**: A user process requests a service (e.g., file I/O) by invoking a C function (e.g., `open`, `read`). This triggers a software trap, switching execution to the kernel. The kernel validates arguments, switches modes, executes the specific service routine via the syscall vector, and returns an integer status code to the user process.
*   **Process State Transitions**: Processes transition between states based on events:
    *   `idle` → `runnable` → `running` (Normal execution).
    *   `running` → `sleep` (Waiting for I/O or events).
    *   `running` → `suspended` (Via signal).
    *   `running` → `zombie` (Terminated but exit code not yet collected by parent).
    *   `sleep/suspended` → `runnable` (Event completion or signal handling).
*   **Kernel Privileges**: The kernel maintains critical data structures in main memory that are not swapped out. It can access the scheduler directly, manage disk cache synchronization, and issue kill signals to any process, whereas no other process can abort the kernel.

### Critical Command Patterns and Required Flags

*   **System Call Interface (C Functions)**:
    *   `open()`: Open a file.
    *   `close()`: Close a file.
    *   `read()` / `write()`: Perform I/O operations.
    *   `kill()`: Send signals to processes (e.g., terminate).
    *   `pipe()`: Create a pipe for inter-process communication.
    *   `socket()`: Create a socket for network communication.
    *   `fork()`: Duplicate a process.
    *   `exec()`: Overlay/replace the current process image.
    *   `exit()`: Terminate a process.

### Network Topology, IP/Subnet, and Service Relationships

*   **Hardware Interrupt Hierarchy**: The kernel handles interrupts in a specific priority order:
    1.  Hardware Errors
    2.  Clock Interrupts
    3.  Disk I/O
    4.  Keyboard
    5.  Software Traps/Interrupts
*   **Kernel-User Interaction**: The kernel acts as the intermediary (`via-media`) between user processes and hardware peripherals. User processes request peripheral transfers (e.g., keyboard input) by switching to kernel mode, often putting the process to "sleep" until data is ready.
*   **Memory Management**: The kernel manages swapping between memory and disk and maintains a disk cache buffer synchronized every 30 seconds to ensure file consistency, during which other processes are suspended.

## Extracted Operational Steps & Workflows
- 1. The scheduler allocates a user process a slice of time (about
- 2.
Services are provided by kernel by switching to the kernel
- 3.
Suppose a user process had sought a data and the peripheral
- 1. Arguments (if present) for the system call are determined.
- 2. Arguments (if present) for the system call are pushed in astack.
- 3. The state of calling process is saved in a user structure.
- 4. The process switches to kernel mode.
- 5. The syscall vector is used as an interface to the kernel routine.
- 6. The kernel initiates the services routine and a return value is
- 7. The return value is converted to a c version (usually an integer
- 1. The first major key difference between the kernel process and
- 2. Another way the kernel differs from the user processes is that it
- 3. Finally, kernel can also issue signals to kill any process (like a
- 1. The page mapping as a page frame number, i.e. which disk
- 2. The date page was created.
- 3. Page protection bit for read/write protections.
- 4. Bits to indicate if the page was modified following the last
- 5. The current page address validity (vis-a-vis the disk).
- 1. Usually a scheduler reevaluates the process priorities at 1
- 2. Every tenth of a second the scheduler selects the topmost
- 3. If a process is runnable at the end of its allocated time, it joins
- 4. If a process is put to sleep awaiting an event, then the
- 5. If a process awaiting an event returns from a system call within
- 6. Periodic clock interrupts occur at the rate of 100

