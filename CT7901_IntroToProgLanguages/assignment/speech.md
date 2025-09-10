Hello, thank you for all agreeing to meet with me to discuss the potential 
development of geltmSoft's new programming language. This presentation should
only take 25 minutes, and I've broken this down into five sections

---

<TODO: WRITE ABOUT EACH SECTION>

---

So, let's start with the history of programming languages to get a thorough 
understanding of what came before. 

---

As you may know, computers "think" in ones and zeroes, otherwise known as 
binary, or machine code. A CPU is made up of a series of registers that store 
these bits. 

---

The CPU knows what actions to perform using opcodes, or Operation Codes. The 
valid instructions that each sequence of 1s and 0s will perform is called the
Instruction Set [1] and they tend to make up what we may be more familiar with
nowadays as simple statements.

---

Most opcodes also come with a series of values that are passed to it. These
are called operands.[2] For example, take the "add" instruction. Commonly, the
next two sequences of bytes will represent the addresses in memory of the two
numbers to add together.[3]

---

Remembering every sequence of 1s and 0s made any development very complex very
quickly, leading to the development of our second layer of programming languages.
Assembly. Assembly uses mnemonics to represent these instructions, as well as
memory addresses. [4] 

This is what our add instruction looks like in Arm assembly, adding 1 to the
number stored in the x0 register and writing it into the x1 register for later
use [4]

---

While somewhat easier to read, Assembly is still programming the instructions
a given CPU archtecture is expecting, such as Arm or X86 instruction sets. By 
the late 50s and early 60s, the conversation was turning to portability - how
can the code I write on one machine run on a different machine with a different
architecture. 

---

This leads us on to our third layer of abstraction, high level languages. Starting
with the likes of fortran in 1957 [5] and Algol in 1958 [6], compiled languages
started to appear. These use a program called a compiler to turn their source
code into the correct machine code for the instruction set you're currently 
using. Eventually cross-compilers were developed to allow you to compile for
other instruction sets as well.

The code on screen currently is C, one of the most well renowned languages of
this era, developed by Dennis Richie and Brian Kernighan and first released to 
the public in the early 70s [7]

---

This brings us to the fourth level of abstraction, and the one most likely to
be of interest to yourselves. Object oriented code wrap our previous tier in 
further abstraction, allowing for more powerful data-driven concepts in 
programming languages to appear. While these concepts first started floating
around back in the 70s with smalltalk[8], they were popularised by the likes of
C++ and Java, two of the biggest languages still used today[9]

---

I want to take a moment to note that programming languages can be classified
in a number of ways. We have Imperative vs Declarative, where one side declares
the "what" a program should do and the other defines how the program should get
there.[10] But, more interestingly, we have different programming paradigms

---

<TODO: SOMETHING HERE ON DIFFERENT PARADIGMS -- I NEED TO SHORTEN WHATS ABOVE>

---

Object Oriented programming is the main paradigm we're going to look at. It's
four principles of Encapsulation, Inheritance, Abstraction, and Polymorphism[11]
give you powerful tools
