Hello, thank you for agreeing to meet with me to discuss the development of 
geltmSoft's new programming language. This presentation should last 25 
minutes, and is broken down into five sections

---

I want to start by taking a moment to look at the fundamentals of programming
languages, and the history that led to these developments.

---

At it's most basic form, a computer only understands 1s and 0s. A CPU's 
instructions are stored in registers[1] in sets of bytes known as opcodes, or
operation codes. Any following parameters to that opcode are called it's 
operands. This example on screen shows the Add instruction, taking two addresses 
and adding the values at those locations into the first address.[2][3].

---

One big flaw in directly programming in raw bytes is that it's difficult to 
debug and tricky to understand. All other programming languages are abstractions 
over this idea. Here, you can see X86 assembly, the first level of abstraction, 
replacing raw bytes with three-letter instructions. Despite these languages 
allowing for precice control of the machine, even assembly doesn't completely 
solve the issues of machine code, and developers of the 1950s were discovering
another issue - portability.[4]

---

At the time, developers wanted to run their code on machines with different 
architectures that utilised varying instruction sets[5]. Starting with fortran 
in 1957 [6] and Algol in 1958 [7], compiled languages were developed. These use 
a program called a compiler to turn their source code into the correct machine 
code for the instruction set you're currently using. Some languages instead 
compile down to a virtual machine designed to run on any architecture.

---

Onscreen now is C, first released in the 70s [9][10][11]. However, these 
languages aren't suited to the rapid development cycle that would benefit 
geltmSoft as further abstractions provide more powerful tools for modern 
developers.

---

Second generation high level languages start to add more powerful features 
around modelling the real world in your code. These languages make use of 
paradigms to categorise their features, and most modern languages implement
multiple paradigms. 

---

Procedural languages are a type of imperative langauge made up of 
statements run in a sequence. Procedural code tends to be simpler to implement,
perfect for prototyping, but doesn't often hold up to real world complexity.[12]
Modularity comes from procedures - also called functions - that the paradigm 
gets it's name from.[13]. This python code models this behaviour. 

---

Out of this grew object oriented programming, with its four pillars of 
Abstraction, Encapsulation, Inheritance, and Polymorphism[14] that allow for 
more powerful reuse of code and flexibility [15]. While first proposed in the 
'60s, this paradigm started to gain popularity in the '80s with languages like 
C++, modelled on this slide.[16]. Due to the nature of the products geltmSoft
wants to produce, I believe you would benefit from utilising powerful reusable 
components developed in this manner.[17]

---

The environment around a language is also important. Some languages use a 
compiler and linker to compile down to machine code to be executed, whereas 
others use another program called an interpreter to execute each line. The 
former is usually faster than the latter, but has an extra build step that can 
be slow.[18] Debuggers also speed up the testing and debugging step[19], although
a number of compiled languages tend to insert DWARF debug symbols optionally
at compile time to make use of existing tooling.[20]

-------------------------------------------------------------------------------
<TODO: WORK ON TRANSITION>

---

I want to start taking a look at the features of geltmsoftlang, starting with 
the data types we'll build into the language. 

---

Along with the basics - chars, integers, floats, booleans and null values, we 
want to design a lean language that reuses these two data types: the 
associative array and the union

---

Starting with an associative array[21], we've chosen this as a versatile data
structure that can fill many use cases. Taking some inspiration from Lua[22], we 
can ensure our standard library provides functions to help the user recreate
types from other languages

---

such as lists or arrays with implicit indexing, structs with default values

---

or even classes, if we combine them with first class functions, adding a touch
of functional programming to emulate object oriented programming.

---

Of course, tables can be nested as well. 

---

There are many uses of this data structure within the educational domain. For
example, you may store student data as a list of structs like so

---

or multiple test results for two students like so. An added benefit here is that
this data should easily export as JSON, a commonly used format that other 
applications or services may use.

---

It's worth noting that we're trading flexibility for conciseness. While some
languages will provide discrete data types of each of these examples, which make
reading code clearer as to what's going on, the flexibility of only one type 
will allow for more complex data types to be built with less experience. We've 
chosen to take this approach so that your team can be up and running quickly.

---

The second data type is a union[23], a data type that practically allows an 
option of multiple types in one field. Unlike the previously mentioned lua,
geltmsoftlang is intended to be a strictly typed language for correctness, so
we're introducing this type to allow developers to have some more control over
the types used. 

---

We believe the most common use case will be to emulate an optional, either a
value or a null. Do you ever have records prepared for future use, such as
exams that haven't been marked yet? An optional float field.

---

What about a student's attendance for the upcoming month? An optional bool.

--- 

Outside of optionals, unions could also be used in the educational domain when
designing quizzes - take this example history question, some possible answers 
are stored as integers, and others are strings. 

---

While a union is  more niche data type with a somewhat narrow use case, we do 
believe that the combination of a union and our associative array should cover
any use case that you can think of.
