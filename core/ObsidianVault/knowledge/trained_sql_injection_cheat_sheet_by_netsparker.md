---
title: "Trained Knowledge & Topology: SQL Injection Cheat Sheet by Netsparker.pdf"
tags:
  - covert_infil
  - enumeration
  - http
  - john
  - mdp
  - pdf
  - trained
source_file: SQL Injection Cheat Sheet by Netsparker.pdf
doc_type: pdf
updated: 2026-10-24 01:00:36
---

# Trained Knowledge & Architecture: `SQL Injection Cheat Sheet by Netsparker.pdf`

- **Source Path:** `~/Projects/CORA/Training/SQL Injection Cheat Sheet by Netsparker.pdf` (`pdf`)
- **Extracted Technical Entities:** `http, john`
- **Extracted IPs / Subnets:** `None`
- **Extracted Interfaces:** `None`
- **Linked Command Playbook:** [[commands/trained_sql_injection_cheat_sheet_by_netsparker]] (`6` CEGAR-verified commands | `6` MDP transitions)

## Command & Tactic Coverage Summary
- **Total CEGAR-Verified Commands:** `6` (full executable list in [[commands/trained_sql_injection_cheat_sheet_by_netsparker]])
- **Tactic Distribution:** `Enumeration` (5), `Covert_Infil` (1)
- **Top Extracted CLI Tools:** `mysql` (6)

## Document Structure & Key Topics
- (M)

## Extracted Operational Steps & Workflows
- 1. Syntax Reference, Sample Attacks and Dirty SQL Injection Tricks
- 1. Line Comments
- 2. Inline Comments
- 3. Stacking Queries
- 4. If Statements
- 5. Using Integers
- 6. String Operations
- 7. Strings without Quotes
- 8. String Modification & Related
- 9. Union Injections
- 10. Bypassing Login Screens
- 11. Enabling xp_cmdshell in SQL Server 2005
- 12. Finding Database Structure in SQL Server
- 13. Fast way to extract data from Error Based SQL Injections in SQL Server
- 14. Blind SQL Injections
- 15. Covering Your Tracks
- 16. Extra MySQL Notes
- 17. Second Order SQL Injections
- 18. Out of Band (OOB) Channel Attacks
- 1. Create table foo( line varchar(8000) )
- 2. bulk insert foo from 'c:\inetpub\wwwroot\login.asp'
- 3. Drop temp table, and repeat for another file.
- 1. Cmd Execute (xp_cmdshell)
- 2. Registry Stuff (xp_regread)
- 1. xp_regaddmultistring
- 2. xp_regdeletekey
- 3. xp_regdeletevalue
- 4. xp_regenumkeys
- 5. xp_regenumvalues
- 6. xp_regread
- 7. xp_regremovemultistring
- 8. xp_regwrite
- 3. Managing Services (xp_servicecontrol)
- 4. Medias (xp_availablemedia)
- 5. ODBC Resources (xp_enumdsn)
- 6. Login mode (xp_loginconfig)
- 7. Creating Cab Files (xp_makecab)
- 8. Domain Enumeration (xp_ntsec_enumdomains)
- 9. Process Killing (need PID) (xp_terminate_process)
- 10. Add new procedure (virtually you can execute whatever you want)
- 11. Write text file to a UNC or an internal path (sp_makewebtask)
- 1. product.asp?id=4 (SMO)
- 1. product.asp?id=5-1
- 2. product.asp?id=4 OR 1=1
- 2. product.asp?name=Book

## Extracted Reference Excerpt
--- [Page 1] ---
SQL Injection Cheat Sheet
Category: Web Security Readings ­ Tags: sql injection , cheat sheet , web security ­ Tue, 29 Mar 2016, by Ferruh Mavituna
What is an SQL Injection Cheat Sheet?
An SQL injection cheat sheet is a resource in which you can find detailed technical information about
the many different variants of the SQL Injection vulnerability. This cheat sheet is of good reference to
both seasoned penetration tester and also those who are just getting started in web application
security.
About the SQL Injection Cheat Sheet
This SQL injection cheat sheet was originally published in 2007 by Ferruh Mavituna on his blog. We
have updated it and moved it over from our CEO's blog. Currently this SQL Cheat Sheet only
contains information for MySQL, Microsoft SQL Server, and some limited information for
ORACLE and PostgreSQL SQL servers. Some of the samples in this sheet might not work in every
situation because real live environments may vary depending on the usage of parenthesis, different
code bases and unexpected, strange and complex SQL sentences. 
Samples are provided to allow you to get basic idea of a potential attack and almost every section
includes a brief information about itself.
M :MySQL
S :SQL Server
P :PostgreSQL
O :Oracle
+ :Possibly all other databases
Examples;
(MS) means : MySQL and SQL Server etc.
(M*S) means : Only in some versions of MySQL or special conditions see related note and SQL
Server
Table Of Contents
1. Syntax Reference, Sample Attacks and Dirty SQL Injection Tricks
1. Line Comments
SQL Injection Attack Samples
2. Inline Comments
Classical Inline Comment SQL Injection Attack Samples
MySQL Version Detection Sample Attacks
3. Stacking Queries
Language / Database Stacked Query Support Table
About MySQL and PHP
Stacked SQL Injection Attack Samples
4. If Statements
MySQL If Statement
SQL Server If Statement
If Statement SQL Injection Attack Samples
SUBSCRIBE
Follow us
 
 
 
 
Netsparker Web Application
Security Scanner
Download Demo
Online Scan
Case Studies
Netsparker Desktop
Netsparker Cloud
Categories
Web Security Readings
Releases
Product Docs & FAQS
News
Events
Subscribe by Email
Get notified via email when new
blog posts are published.
Enter your email...
Archive
Select Month
 
 
 
 
 
 
 
Search...

--- [Page 2] ---
5. Using Integers
6. String Operations
String Concatenation
7. Strings without Quotes
Hex based SQL Injection Samples
8. String Modification & Related
9. Union Injections
UNION – Fixing Language Issues
10. Bypassing Login Screens
11. Enabling xp_cmdshell in SQL Server 2005
12. Finding Database Structure in SQL Server
13. Fast way to extract data from Error Based SQL Injections in SQL Server
14. Blind SQL Injections
15. Covering Your Tracks
16. Extra MySQL Notes
17. Second Order SQL Injection

