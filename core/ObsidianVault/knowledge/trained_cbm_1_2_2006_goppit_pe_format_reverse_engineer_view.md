---
title: "Trained Knowledge & Topology: CBM_1_2_2006_Goppit_PE_Format_Reverse_Engineer_View.pdf"
tags:
  - http
  - john
  - mdp
  - pdf
  - tls
  - trained
source_file: CBM_1_2_2006_Goppit_PE_Format_Reverse_Engineer_View.pdf
doc_type: pdf
updated: 2026-10-24 01:05:55
---

# Trained Knowledge & Architecture: `CBM_1_2_2006_Goppit_PE_Format_Reverse_Engineer_View.pdf`

- **Source Path:** `~/Projects/CORA/Training/CBM_1_2_2006_Goppit_PE_Format_Reverse_Engineer_View.pdf` (`pdf`)
- **Extracted Technical Entities:** `http, john, tls`
- **Extracted IPs / Subnets:** `None`
- **Extracted Interfaces:** `None`

## Document Structure & Key Topics
- The Section Table (p. 18)
- The PE File Sections (p. 20)
- The Import Section (p. 29)
- The Loader (p. 35)
- Navigating Imports on Disk (p. 39)
- Adding Code to a PE File (p. 46)
- Adding Import to an Executable (p. 53)
- Infection of PE Files by Viruses (p. 71)

## Extracted Operational Steps & Workflows
- 1. Read in the first page of the file with the DOS header, PE header, and section headers.
- 2. Determine whether the target area of the address space is available, if not allocate another area.
- 3. Using info in the section headers, map sections of the file to the appropriate places in the allocated
- 4. If the file is not loaded at its target address (ImageBase), apply relocation fix-ups.
- 5. Go through list of DLLs in the imports section and load any that aren't already loaded (recursive).
- 6. Resolve all the imported symbols in the imports section.
- 7. Create the initial stack and heap using values from the PE header.
- 8. Create the initial thread and start the process.
- 1. Check to see if the module is already loaded.
- 2. Map the module and supporting information into memory.
- 3. Walk the module's import descriptor table (find other modules this one is importing).
- 4. Update the module's load count as well as any others brought in by this DLL.
- 5. Initialize the module.
- 6. Clear some sort of flag, indicating that the load has finished.
- 1. Add to an existing section when there is enough space for your code.
- 2. Enlarge an existing section when there is not enough space.
- 3. Add an entirely new section.
- 1. If the section is followed by other sections then you will need to move the following sections up to make
- 2. There are various references within the file headers that will need to be adjusted if you change the file
- 3. References between various sections (such as references to data values from the code section) will all
- 1. Each DLL must be declared with an IMAGE_IMPORT_DESCRIPTOR (IID), remembering to close the
- 2. Each IID needs at least Name1 and FirstThunk fields, the rest can be set to 0 (setting OriginalFirstThunk
- 3. Each entry of the FirstThunk must be an RVA to an Image_Thunk_Data (the IAT) which in turn contains a
- 4. If IIDs have been added then the isize field of the Import Table in the Data Directory may need
- 1. select basecalc.exe in the box at the top (it should still be running in Olly.)
- 2. Next enter our OEP (2ADB4) in the appropriate box
- 3. Press the "IAT AutoSearch" button and click OK on the messagebox
- 4. Press the "Get Imports" button
- 5. Press "Show Invalid" - in this case there are none
- 6. Press "Fix Dump" and select basecalc_dmp.exe in the open dialogbox
- 7. Exit.
- 1. The virus moves the PE  header to the end of the host app and inserts its code into the space.
- 2. The virus appends the host app to itself.

## Extracted Reference Excerpt
--- [Page 1] ---
Volume 1, Issue 2, 2006 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
Portable Executable File Format – A Reverse Engineer View 
 
Goppit 
January 2006 
 
Abstract 
This tutorial aims to collate information from a variety of sources and present it in a way which is accessible 
to beginners. Although detailed in parts, it is oriented towards reverse code engineering and superfluous 
information has been omitted.

--- [Page 2] ---
PORTABLE EXECUTABLE FILE FORMAT – A REVERSE ENGINEER VIEW 
This disclaimer is not meant to sidestep the responsibility for the material we will share 
with you, but rather is designed to emphasize the purpose of this CodeBreakers Magazine 
feature, which is to provide information for your own purposes. The subjects presented 
have been chosen for their educational value. The information contained herein consists of 
Secure Software Engineering, Software Security Engineering, Software Management, 
Security Analysis, Algorithms, Virus-Research, Software-Protection and Reverse Code 
Engineering, Cryptanalysis, White Hat and Black Hat Content, and is derived from authors 
of academically institutions, commercials, organizations, as well as private persons. The 
information should not be considered to be completely error-free or to include all relevant 
information; nor should it be used as an exclusive basis for decision-making. The user 
understands and accepts that if CodeBreakers Magazine were to accept the risk of harm to 
the user from use of this information, it would not be able to make the information 
available because the cost to cover the risk of harms to all users would be too great. Thus, 
use of the information is strictly voluntary and at the users sole risk. 
  
The information contained herein is not a license, either expressly or impliedly, to any 
intellectual property owned or controlled by any of the authors or developers of 
CodeBreakers Magazine. The information contained herein is provided on an "AS IS" basis 
and to the maximum extent permitted by applicable law, this information is provided AS IS 
AND WITH ALL FAULTS, and the authors and developers of CodeBreakers Magazine hereby 
disclaim all other warranties and conditions, either express, implied or statutory, including, 
but not limited to, any (if any) implied warranties, duties or conditions of merchantability, 
of fitness for a particular purpose, of accuracy or completeness of responses, of results, of 
workmanlike effort, of lack of viruses, and of lack of negligence, all with regard to the 
contribution.  
ALSO, THERE IS NO WARRANTY OR CONDITION OF TITLE, QUIET ENJOYMENT, QUIET 
POSSESSION, CORRESPONDENCE TO DESCRIPTION OR NON-INFRINGEMENT WITH 
REGARD TO CODEBREAKERS MAGAZINE.  
IN NO EVENT WILL ANY AUTHOR OR DEVELOPER OF

