---
title: "Trained Knowledge & Topology: FORFILES.txt"
tags:
  - mdp
  - passive_enum
  - text
  - trained
source_file: FORFILES.txt
doc_type: text
updated: 2026-10-25 00:58:24
---

# Trained Knowledge & Architecture: `FORFILES.txt`

- **Source Path:** `~/Projects/CORA/Training/FORFILES.txt` (`text`)
- **Extracted Technical Entities:** `general`
- **Extracted IPs / Subnets:** `None`
- **Extracted Interfaces:** `None`
- **Linked Command Playbook:** [[commands/trained_forfiles]] (`5` CEGAR-verified commands | `5` MDP transitions)

## Command & Tactic Coverage Summary
- **Total CEGAR-Verified Commands:** `5` (full executable list in [[commands/trained_forfiles]])
- **Tactic Distribution:** `Passive_Enum` (5)
- **Top Extracted CLI Tools:** `forfiles` (5)

## Extracted Reference Excerpt
FORFILES
	To list all of the batch files on drive C, type:
		• forfiles /p c:\ /s /m *.bat /c "cmd /c echo @file is a batch file"
	To list all of the directories on drive C, type:
		• forfiles /p c:\ /s /m *.* /c "cmd /c if @isdir==true echo @file is a directory"
	To list all of the files in the current directory that are at least one year old, type:
		• forfiles /s /m *.* /d -365 /c "cmd /c echo @file is at least one year old."
	To display the text "File is outdated" for each of the files in the current directory that are older than January 1, 2007, type:
		• forfiles /s /m *.* /d -01/01/2007 /c "cmd /c echo @file is outdated." 
	To list the file name extensions of all the files in the current directory in column format, and add a tab before the extension, type:
		• forfiles /s /m *.* /c "cmd /c echo The extension of @file is 0x09@ext"

