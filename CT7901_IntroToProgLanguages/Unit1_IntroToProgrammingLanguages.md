# Unit 1 - Introduction to Programming Languages
* Describe the evolution of programming languages
* Classify the abstractions in programming languages
* Classify programming language paradigms
* Describe the environment of programming languages
* Explain how syntax and semantics define a programming langauge

#### Lesson 1
* A programming language is a set of notations and rules with which we can 
communicate and instruct computers to perform computations for us
* Computer instructions are in a series of 0s and 1s 
* Machine languages are harder for humans to understand - ineffective and 
inefficient
* Higher levels of abstraction was needed, as well as programs to translate the
higher level languages down to this machine code
* These translaters are known as compilers and interpreters


##### Steps In The Evolution of Programming Languages
* Machine language - the native language of computers
    * Made up of an opcode (operation code) and a series of operands (IE arguments)
    * Operands may be memory locations/addresses of other values
* Assembly languages - Using mnemonics for opcodes
    * The first assembly language was invented in the 1950s
    * Uses an assembler program to translate the assembly code into machine code
    * Tied to the specific hardware architecture
* First generation high level languages 
    * Closer to the way humans think, using extra layers of abstraction
    * The earliest high-level languages were Fortran, Cobol, Algol, and lisp
    * Uses a program called a compiler to translate directly into machine language
    * However, these languages aren't tied to a specific architecture
* Second generation high level languages 
    * Higher levels of abstraction over first generation languages
    * EX OOP langs like Java
* Interpreted languages
    * Doesn't need to be compiled, is turned into machine language as the code is
    executed
    * Very flexible and convenient
    * Translates one line at a time

#### Lesson 2
* Two types of abstractions
    * Data abstractions - such as integers or arrays/container types
    * Control flow abstractions - IE `if/else`.


* Data abstractions have a public interface that act as the "contract" between
 the user and the implementer, and as long as the interface doesn't change, the
 implementer can change any implementation details, up to and including changing
 an underlying data structure completely. 
 * One example of this is an associative array (or lookup table) which can be 
 a hashmap, a binary search tree, or even a linked list of KV pairs.

#### Lesson 3
* A programming paradigm is a pattern or a model of abstraction offered by a 
programming language. The most common paradigm in recent years is Object Oriented
Programming, offered by languages such as Java, C#, and C++
* Early paradigms were influenced by the architecture of the hardware and based
on the Von Neumann machine
* "Imperative" paradigm -- directly based on the Von Neumann machine
    * Grew into OOP paradigm
* Functional paradigm - uses a series of state-less function invocations (ex Lisp)
* Logic paradigm - abstracts computations as answers to questions about a system
of facts and rules EX Prolog

* Programming paradigms are influenced by 
    * The architecture we weant to program
    * The mathematical strategies we use to solve problems
* OOP languages are imperative in style (as opposed to declarative)
    * But added features to support objects

#### Lesson 4
* Compilers, assemblers, editors, linkers, loaders, debuggers, profilers.
* Collectively called the development environment - often grouped into an IDE

* Editors
    * Specifically designed to simplify and speed up the typing of source code
    * Structure editors - a type of editor that allows you to modify the AST
    directly
    * Source-code editor can (usually) check syntax and warn of problems
    * The Language Server Protocol was developed by Microsoft and allows an
    editor to read syntax information about any language with an LSP server. 

* Compilers
    * Transforms code from one language into another, usually machine code
    or assembly
    * cross-compilers produce code for different CPU architectures or operating
    systems 
    * A Decompiler in turn transforms code from a lower langague to a higher one
    * Phases of compilation
        * Preprocessing
        * Lexical analysis
        * parsing
        * semantic analysis 
        * conversion of input programs to an intermediate representation
        * code optimisation
        * code generation 

* Linkers
    * Each file in a program is compiled down to an object file
    * A Linker links together these object files and links them into an 
    executable

* Loaders
    * Part of the OS responsible for loading programs and libraries
    * This places programs into memory to be executed
    * Embedded systems tend not to have loaders, instead reading straight from
    ROM. 
    * To load the OS itself, a specialised "bootloader" is used as part of 
    system startup

* Debuggers
    * Used to test another program
    * Typically can halt program execution with breakpoints 
    * can display the contents of memory/registers
    * Can modify memory contents

#### Lesson 5
* Reasons for formal definitions of programming languages
    * Clear up ambiguities
    * Can prove the correctness of a program mathematically
    * Ensure portability across architectures and OS's
    * Common means to compare and contrast languages 

* syntax is the rules that define the combinations of symbols for correctly
structured statements or expressions in that language.
* Syntax is the form of the code, semantics is the meaning.
* syntactic grammer - the rules which tokens can be combined 

* Forms of semantics:
    * Natural language - description by human natural language
    * formal semantics - description by mathematics
    * reference implementation - description by computer program
    * test suites - description by examples and expected behaviours 
        * Very rare to start like this, but some languages have evolved
        based on their test suites (EX Ada) 
