---
title: "Trained Knowledge & Topology: CQC001_E020_M040_Windows_Processes.pdf"
tags:
  - http
  - https
  - listdlls
  - mdp
  - passive_enum
  - pdf
  - pslist
  - sysinternals
  - trained
source_file: CQC001_E020_M040_Windows_Processes.pdf
doc_type: pdf
updated: 2026-10-24 00:57:32
---

# Trained Knowledge & Architecture: `CQC001_E020_M040_Windows_Processes.pdf`

- **Source Path:** `~/Projects/CORA/Training/CQC001_E020_M040_Windows_Processes.pdf` (`pdf`)
- **Extracted Technical Entities:** `http, https, listdlls, pslist, sysinternals`
- **Extracted IPs / Subnets:** `None`
- **Extracted Interfaces:** `None`
- **Linked Command Playbook:** [[commands/trained_cqc001_e020_m040_windows_processes]] (`1` CEGAR-verified commands | `1` MDP transitions)

## Command & Tactic Coverage Summary
- **Total CEGAR-Verified Commands:** `1` (full executable list in [[commands/trained_cqc001_e020_m040_windows_processes]])
- **Tactic Distribution:** `Passive_Enum` (1)
- **Top Extracted CLI Tools:** `tasklist` (1)

## LLM Distilled Operational Summary
### Key Operational Techniques & Decision Workflows

*   **Process Definition & Isolation**: Identify a process as an executing program instance acting as a container for thread resources. Recognize that each process maintains a private virtual address space, isolated from others unless explicitly shared.
*   **Memory Analysis Workflow**:
    *   **Working Set**: Check physical memory currently mapped to the process.
    *   **Paged Pool**: Identify memory eligible for transfer to the paging file (disk) when unused.
    *   **Non-Paged Pool**: Identify critical memory objects that must remain in physical RAM.
    *   **Pagefile**: Monitor system paging file usage allocated to the specific process.
*   **Inter-Process Communication (IPC) Verification**:
    *   **Anonymous Pipes**: Use for single-direction data transfer between related local processes (e.g., redirecting stdin/stdout).
    *   **Named Pipes**: Use for reliable, duplex communication between unrelated processes or across networks.
    *   **Mailslots**: Utilize for unreliable, one-way, connectionless messaging.
    *   **RPC**: Invoke for remote function execution on local or remote systems.
    *   **Sockets & Clipboard**: Leverage for protocol-dependent networking and application-level data sharing respectively.

### Critical Command Patterns & Required Flags

*   **Sysinternals Suite (Recommended for detailed analysis)**:
    *   `PsList`: Enumerate running processes (Local/Remote, 32/64-bit).
    *   `PsKill`: Terminate specific processes.
    *   `PsSuspend`: Suspend or resume process execution.
    *   `Handle`: List open file references for all processes.
    *   `ListDLLs`: Enumerate loaded Dynamic Link Libraries per process.
*   **Native Windows Utilities**:
    *   `TaskList`: Display currently running processes.
    *   `TaskKill`: Terminate running processes.

### Network Topology & Service Relationships

*   **Local vs. Remote Scope**:
    *   **Anonymous Pipes**: Restricted to local computer communication between related processes.
    *   **Named Pipes**: Support both local and network-based communication between unrelated processes.
    *   **RPC**: Functions across local or remote computers, executing code external to the calling application.
    *   **Sockets**: Enable communication with socket implementations on other systems via underlying network protocols.
*   **Service Interaction**:
    *   **Mailslots**: Operate as a pseudo-file where clients append messages to be read by a dedicated mailslot server.
    *   **Clipboard**: Acts as a central repository for inter-application data sharing during copy/paste operations.

