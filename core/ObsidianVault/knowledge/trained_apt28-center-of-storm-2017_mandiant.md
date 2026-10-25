---
title: "Trained Knowledge & Topology: APT28-Center-of-Storm-2017_MANDIANT.pdf"
tags:
  - cve-2015-1701
  - cve-2015-2424
  - cve-2015-2590
  - cve-2015-3043
  - cve-2015-5119
  - cve-2016-7255
  - cve-2016-7855
  - john
  - mdp
  - pdf
  - powershell
  - trained
source_file: APT28-Center-of-Storm-2017_MANDIANT.pdf
doc_type: pdf
updated: 2026-10-25 00:56:10
---

# Trained Knowledge & Architecture: `APT28-Center-of-Storm-2017_MANDIANT.pdf`

- **Source Path:** `~/Projects/CORA/Training/APT28-Center-of-Storm-2017_MANDIANT.pdf` (`pdf`)
- **Extracted Technical Entities:** `cve-2015-1701, cve-2015-2424, cve-2015-2590, cve-2015-3043, cve-2015-5119, cve-2016-7255, cve-2016-7855, john, powershell`
- **Extracted IPs / Subnets:** `None`
- **Extracted Interfaces:** `None`

## LLM Distilled Operational Summary
### Operational Techniques & Decision Workflows
*   **Strategic Espionage to Information Operations:** APT28 evolved from traditional intelligence collection (defense/geopolitics) to active information operations. The workflow involves compromising a target, stealing internal data, and selectively leaking it to advance specific Russian political narratives (e.g., Syria conflict, NATO-Ukraine relations, 2016 US election).
*   **Target Selection:** Primary targets include governments, militaries, defense attaches, media entities, and dissidents in the US, Europe, and former Soviet Union. Specific focus on regional security organizations like NATO and OSCE.
*   **Tool Development & Adaptation:** The group demonstrates a sophisticated development cycle, adapting malware and operational procedures to evade detection over time (e.g., using decoys).
*   **Long-Term Persistence:** Operations date back to at least 2007, indicating a capability for long-term access and continuous monitoring of target environments.

### Critical Command Patterns & Required Flags
*   **Malware Families:** While specific command strings aren't detailed in this chunk, the report references the **Pawn Storm** campaign (Trend Micro's alias for APT28 activity).
*   **Detection Context:** Operations are characterized by endpoint and network detections requiring continuous monitoring. Specific flags are implied through the use of "decoys" to evade detection, suggesting commands related to credential harvesting or lateral movement that mimic legitimate traffic.

### Network Topology & Relationships
*   **Attribution:** Confirmed by DHS/FBI (Dec 2016) and FireEye as being sponsored by the **Russian Government**.
*   **Key Targets & Events:**
    *   **OSCE:** Confirmed breach in November 2016.
    *   **German CDU:** Targeted in May 2016.
    *   **DNC:** June 2016 breach attributed to the Russian Government.
    *   **WADA:** Investigated in the context of the 2016 Olympic doping scandal.
*   **Geographic Scope:** US, Europe, and former Soviet Union nations.
*   **Organizational Focus:** Governments, militaries, defense attaches, media, and political parties (e.g., German Christian Democratic Union).

## Extracted Operational Steps & Workflows
- 1. 	
Gauquelin, Blaise. “La Russie soupçonnée d’être responsable d’un piratage informatique contre l’OSCE.” Le Monde. 28 Dec. 2016. Web. 29 Dec. 2016.
- 2. 	
Trend Micro refers to activity corresponding to FireEye’s APT28 as “Pawn Storm.”
- 3. 	
Hacquebord Feike. “Pawn Storm Targets German Christian Democratic Union.” Trend Micro. 11 May 2016. Web. 29 Dec. 2016.
- 4. 	
Hacquebord Feike. “Pawn Storm’s Domestic Spying Campaign Revealed; Ukraine and US Top Global Targets.” TrendLabs Security Intelligence Blog, Trend Micro. 18 August 2015. Web. 29 Dec.  2016.
- 5. 	
“Neuer Hackerangriff auf Bundespolitiker / BSI warnt Parteien vor Cyberangriffen.” Westdeutscher Rundfunk. 20 Sept. 2016. Web. 29 Dec. 2016.
- 8.	 “WADA Confirms Attack by Russian Cyber Espionage Group.” World Anti-Doping Agency. 13 Sept. 2016. Web. 29 Dec. 2016.
- 9.	 Fancy Bears’ HT (fancybears). “@AnonPress Greetings. We hacked #WADA. We have Proof of American Athletes taking doping. Fancybear.net.” 12 Sept. 2016, 4:12 PM. Tweet.
- 10.	 CrowdStrike refers to activity corresponding to FireEye’s APT28 and APT29 as “Fancy Bear” and “Cozy Bear,” respectively.
- 11. 	 “Nakashima, Ellen. “Cyber Researchers Confirm Russian Government Hack of Democratic National Committee.” The Washington Post. 20 June 2016. Web. 29 Dec. 2016.
- 12. 	 “Rid, Thomas. “All Signs Point to Russia Being Behind the DNC Hack.” Motherboard, Vice. 25 July 2016. Web. 29 Dec. 2016.
- 13.  	 “Bennett, Cory. “Guccifer 2.0 Drops More DNC Docs.” Politico. 13 Sept. 2016. Web. 2 Jan. 2017. <>
- 14.	 Perlroth, Nicole. Shear, Michael D. “Private Security Group Says Russia was Behind John Podesta’s Email Hack.” The New York Times. 21 Oct. 2016. Web. 2 Jan. 2017.
- 15. 	 “Franceschi-Bicchierai, Lorenzo. “How Hackers Broke Into John Podesta and Colin Powell’s Gmail Accounts.” 20 Oct. 2016. Web. 2 Jan. 2017.
- 16.	 “Nakashima, Ellen. “FBI Probes Suspected Breach of Another Democratic Organization by Russian Hackers.” The Washington Post. 29 July 2016. Web. 29 Dec. 2016.
- 17. 	 “Pelosi, Nancy. “DCCC Cyber Breach.” 13 August 2016. Email. U.S. House of Representatives. Washington, DC. Politico. Web. 29 Dec. 2016.
- 18. 	 “Lipton, Eric. Shane, Scott. “Democratic House Candidates Were Also Targets of Russian Hacking.” The New York Times. 13 Dec. 2016. Web. 29 Dec. 2016.
- 19. 	 Ibid.
- 20.	 Gallagher, Sean. “Guccifer 2.0 Posts DCCC Docs, Says They’re From Clinton Foundation.” Ars Technica. 4 Oct. 2016. Web. 3 Jan. 2017.
- 21.	 “Russian Hackers Suspected in French TV Cyberattack.” Deutsche Welle. 6 Oct. 2015. Web. 29 Dec. 2016.
- 22.	 Joselow, Gabe. “Election Cyberattacks: Pro-Russia Hackers Have Been Accused in Past.” NBC News. 3 Nov. 2016. Web. 29 Dec. 2016.
- 23. 	Clayton, Mark. “Ukraine Election Narrowly Avoided ‘Wanton Destruction’ From Hackers (+Video).” The Christian Science Monitor. 17 June 2014. Web. 2 Jan. 2017.
- 24. “Foundation Board Media Release: WADA Strengthens Anti-Doping Worldwide.” World Anti-Doping Agency. 18 November 2015.
- 25. 	“Russia State-Sponsored Doping Across Majority of Olympic Sports, Claims Report.” The BBC. 18 July 2016. Web. 29 Dec. 2016.
- 26.	 Macguire, Eoghan. Almasy, Steve. “271 Russian Athletes Cleared for Rio Games.” CNN. 5 August 2016. Web. 29 Dec. 2016.
- 27. 	“Cyber Security Update: WADA’s Incident Response.” World Anti-Doping Agency. 5 Oct. 2016. Web. 3 Jan. 2017.
- 28. 	“WADA Confirms Attack by Russian Cyber Espionage Group.” World Anti-Doping Agency. 13 Sept. 2016.
- 29.	 “WADA Confirms Another Batch of Athlete Data Leaked by Russian Cyber Hackers ‘Fancy Bear.’” World Anti-Doping Agency. 14 Sept. 2016. Web. 29 Dec. 2016. <>
- 30.	 [OP PL]. “www.tas-cas.org.” Online video clip. YouTube. YouTube, 9 Aug. 2016. Web. 3 Jan. 2017.
- 31. 	 Anonymous Poland (@anpoland). “@Cryptomeorg @ben_rumsby @PogoWasRight @Jason_A_Murdock @Cyber_War_News @kevincollier Tomorrow will ddos WADA and publish some secret dosc.” 11 Aug 2016 10:10
- 32. 	Anonymous Poland (@anpoland). “@JoeUchill within a few days will be new attack on the WADA/Olimpic.” 5 Sept. 2016 5:19 AM. Tweet.
- 33.	 Fancy Bears’ HT (fancybears). “@AnonPress Greetings. We hacked #WADA. We have Proof of American Athletes taking doping. Fancybear.net.”
- 34.	 Ibid.
- 35. 	“WADA Confirms Attack by Russian Cyber Espionage Group.”World Anti-Doping Agency.13 Sept. 2016.
- 36.	 Russian Hackers Leak Simone Biles and Serena Williams Files.” The BBC. 13 Sept. 2016. Web. 29 Dec. 2016.
- 37.	 Rumsby, Ben. “US Superstars Serena and Venus Williams and Simone Biles Given Drugs Exemption, Russian Hackers Reveal.” The Telegraph. 14 Sept. 2016. Web. 29 Dec. 2016.
- 38.	 Luhn, Alec.”Fancy Bears Origins Unclear But Russia Seizes Chance to Put Boot into Wada.” 15 Sept. 2016. Web. 29 Dec. 2016.
- 39. 	Gibson, Owen. “Russian Sports Minister Vitaly Mutko Denies Link to Wada Hackers.” The Guardian. 14 Sept. 2016. Web. 29 Dec. 2016.

