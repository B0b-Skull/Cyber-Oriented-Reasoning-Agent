---
title: "Trained Knowledge & Topology: HadoopMappingInfra_ReadMe.md"
tags:
  - active_enum
  - http
  - https
  - mdp
  - nmap
  - text
  - trained
source_file: HadoopMappingInfra_ReadMe.md
doc_type: text
updated: 2026-10-25 00:58:24
---

# Trained Knowledge & Architecture: `HadoopMappingInfra_ReadMe.md`

- **Source Path:** `~/Projects/CORA/Training/HadoopMappingInfra_ReadMe.md` (`text`)
- **Extracted Technical Entities:** `http, https, nmap`
- **Extracted IPs / Subnets:** `172.24.11.150, 2.7.1.2`
- **Extracted Interfaces:** `None`
- **Linked Command Playbook:** [[commands/trained_hadoopmappinginfra_readme]] (`1` CEGAR-verified commands | `1` MDP transitions)

## Command & Tactic Coverage Summary
- **Total CEGAR-Verified Commands:** `1` (full executable list in [[commands/trained_hadoopmappinginfra_readme]])
- **Tactic Distribution:** `Active_Enum` (1)
- **Top Extracted CLI Tools:** `nmap` (1)

## LLM Distilled Operational Summary
### Key Operational Techniques & Decision Workflows
*   **Role Identification**: Determine server roles (datanode, namenode, edgenode) and deployed technologies (HBase, Hive, Spark, Kafka, HUE, Ranger) by correlating discovered ports with known Hadoop ecosystem services.
*   **WebUI Discovery**: Prioritize scanning for standard Hadoop WebUI ports to map infrastructure topology:
    *   HDFS NameNode: 50070 (HTTP) / 50470 (HTTPS)
    *   HDFS DataNode: 50075 (HTTP) / 50475 (HTTPS)
    *   Secondary NameNode: 50090
    *   YARN ResourceManager: 8088 (HTTP) / 8090 (HTTPS)
    *   YARN NodeManager: 8042 (HTTP) / 8044 (HTTPS)
    *   MapReduce v2 JobHistory: 19888 (HTTP) / 19890 (HTTPS)
    *   MapReduce v1 JobTracker: 50030
    *   MapReduce v1 TaskTracker: 50060
*   **Nmap Scripting**: Utilize `http-enum` with the `-sV` flag to identify specific WebUIs (Ambari, Oozie, Ranger, HUE, Cloudera Manager, MapReduce v2, YARN) via fingerprinting.
*   **Advanced NSE Scripts**: Deploy specialized scripts for deeper component analysis:
    *   *MapReduce v1*: `hadoop-datanode-info.nse`, `hadoop-jobtracker-info.nse`, `hadoop-namenode-info.nse`, `hadoop-tasktracker-info.nse`, `hadoop-secondary-namenode-info.nse`.
    *   *HBase*: `hbase-region-info.nse`, `hbase-master-info.nse`.
    *   *Flume*: `flume-master-info.nse`.

### Critical Command Patterns
*   **Basic WebUI Discovery**:
    ```bash
    nmap -sV --script=http-enum -p- <TARGET_IP>
    ```
    *Note: `-sV` is mandatory for correct service version identification (e.g., distinguishing JobHistory).*
*   **Targeted Component Scanning**:
    ```bash
    nmap -sV --script=hadoop-namenode-info,hadoop-datanode-info <TARGET_IP>
    ```

### Network Topology & Service Relationships
*   **IP/Subnet**: Example sandbox target `172.24.11.150` uses ports 6080, 8042, 8080, 8088, and 19888.
*   **Service Relationships**:
    *   **Apache Tomcat**: Often hosts Apache Ranger WebUI (Port 6080).
    *   **Jetty**: Hosts YARN NodeManager, ResourceManager, MapReduce JobHistory, and Ambari.
*   **Authentication Constraints**: Nmap probes are currently inefficient against Kerberized clusters requiring authentication to access WebUI

