---
title: "Trained Knowledge & Topology: l-linux-kernel-pdf.pdf"
tags:
  - mdp
  - pdf
  - serial
  - trained
source_file: l-linux-kernel-pdf.pdf
doc_type: pdf
updated: 2026-10-25 00:58:46
---

# Trained Knowledge & Architecture: `l-linux-kernel-pdf.pdf`

- **Source Path:** `~/Projects/CORA/Training/l-linux-kernel-pdf.pdf` (`pdf`)
- **Extracted Technical Entities:** `serial`
- **Extracted IPs / Subnets:** `None`
- **Extracted Interfaces:** `None`

## Extracted Reference Excerpt
--- [Page 1] ---
© Copyright IBM Corporation 2007
Trademarks
Anatomy of the Linux kernel
Page 1 of 8
Anatomy of the Linux kernel
History and architectural decomposition
M. Tim Jones
June 06, 2007
The Linux® kernel is the core of a large and complex operating system, and while it's huge,
it is well organized in terms of subsystems and layers. In this article, you explore the general
structure of the Linux kernel and get to know its major subsystems and core interfaces. Where
possible, you get links to other IBM articles to help you dig deeper.
Given that the goal of this article is to introduce you to the Linux kernel and explore its architecture
and major components, let's start with a short tour of Linux kernel history, then look at the Linux
kernel architecture from 30,000 feet, and, finally, examine its major subsystems. The Linux kernel
is over six million lines of code, so this introduction is not exhaustive. Use the pointers to more
content to dig in further.
A short tour of Linux history
Linux or GNU/Linux?
You've probably noticed that Linux as an operating system is referred to in some cases as
"Linux" and in others as "GNU/Linux." The reason behind this is that Linux is the kernel of
an operating system. The wide range of applications that make the operating system useful
are the GNU software. For example, the windowing system, compiler, variety of shells,
development tools, editors, utilities, and other applications exist outside of the kernel, many
of which are GNU software. For this reason, many consider "GNU/Linux" a more appropriate
name for the operating system, while "Linux" is appropriate when referring to just the kernel.
While Linux is arguably the most popular open source operating system, its history is actually quite
short considering the timeline of operating systems. In the early days of computing, programmers
developed on the bare hardware in the hardware's language. The lack of an operating system
meant that only one application (and one user) could use the large and expensive device at a
time. Early operating systems were developed in the 1950s to provide a simpler development
experience. Examples include the General Motors Operating System (GMOS) developed for the
IBM 701 and the FORTRAN Monitor System (FMS) developed by North American Aviation for the
IBM 709.
In the 1960s, Massachusetts Institute of Technology (MIT) and a host of companies developed an
experimental operating system called Multics (or Multiplexed Information and Computing Service)

--- [Page 2] ---
developerWorks®
ibm.com/developerWorks/
Anatomy of the Linux kernel
Page 2 of 8
for the GE-645. One of the developers of this operating system, AT&T, dropped out of Multics
and developed their own operating system in 1970 called Unics. Along with this operating

