Hello, thank you for agreeing to meet with me to discuss the development of 
geltmSoft's new programming language. This presentation should last 25 
minutes, and is broken down into five sections

---

<TODO: WRITE ABOUT EACH SECTION>

---

Any conversation about how language development needs to begin with 
understanding how languages work. 

---

At it's most basic form, a computer only understands 1s and 0s. A CPU's 
instructions are stored in registers[1] in sets of bytes known as opcodes, or
operation codes. Any following parameters to that opcode are called it's 
operands. This example on screen shows the Add instruction, taking two addresses 
and adding the values at those locations into the first address. [3][4].

---

One big flaw in directly programming in raw bytes is that it's difficult to 
debug and tricky to understand. All other programming languages are abstractions 
over this idea. Here, you can see X86 assembly, the first level of abstraction, 
replacing raw bytes with three-letter instructions. Despite these languages 
allowing for precice control of the machine, even assembly doesn't completely 
solve the issues of machine code, and developers of the 1950s were discovering
another issue - portability.[5]

---

At the time, developers wanted to run their code on machines with different 
architectures that utilised varying instruction sets[6]. Starting with fortran 
in 1957 [7] and Algol in 1958 [8], compiled languages were developed. These use 
a program called a compiler to turn their source code into the correct machine 
code for the instruction set you're currently using. Some languages instead 
compile down to a virtual machine designed to run on any architecture.

Onscreen now is C, first released in the 70s [9]. However, these languages
aren't suited to the rapid development cycle that would benefit geltmSoft as 
further abstractions provide more powerful tools for modern developers.

---

Second generation high level languages start to add more powerful features 
around modelling the real world in your code. These languages make use of 
paradigms to categorise their features, and most modern languages implement
multiple paradigms. 

---

Procedural languages are a type of imperative langauge made up of 
statements run in a sequence. Procedural code tends to be simpler to implement,
perfect for prototyping, but doesn't often hold up to real world complexity.[10]
Modularity comes from procedures - also called functions - that the paradigm 
gets it's name from.[11]. This python code models this behaviour. 

---

Out of this grew object oriented programming, with its four pillars of 
Abstraction, Encapsulation, Inheritance, and Polymorphism[12] that allow for 
more powerful reuse of code and flexibility [13]. While first proposed in the 
'60s, this paradigm started to gain popularity in the '80s with languages like 
C++, modelled on this slide.[14]. Due to the nature of the products geltmSoft
wants to produce, I believe you would benefit from utilising powerful reusable 
components developed in this manner.

---

The environment around a language is also important. Some languages use a 
compiler and linker to compile down to machine code to be executed, whereas 
others use another program called an interpreter to execute each line. The 
former is usually faster than the latter, but has an extra build step that can 
be slow.[15] Debuggers also speed up the testing and debugging step[16], although
a number of compiled languages tend to insert DWARF debug symbols optionally
at compile time to make use of existing tooling.[17]
