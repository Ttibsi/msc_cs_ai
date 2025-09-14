# Data Type Abstractions in Python
* Define data type abstrctions and their types in programming languages
* Classify simple types used in programming languages like the integer and 
character data types
* Explain the abstractions of operators expressions and variables
* Classify composite types used in programming languages like the structure
and class data types

#### Lesson 1
* The smallest unit of data is usually a byte - 8 bits
* The unit processed by machine code is called a word - 32 or 64 bits
    * 4 or 8 bytes
* Most languages have data types that abstract over the control of these 
words, ex C has bool, int, float, double, but the size of these types are 
implementation defined
* There is a set of rules on how values of each type are used and manipulated
* Basic data types are just bool, char, ints (of varying sizes) and floating
point numbers.
* These constrain the possible values an expression (ex a variable) can hold
* Data types also define the operations that can be performed with that type

* Most languages allow the user to define their own types, usually by combining
multiple elements of other types and defining valid operations on that type.
* These can be classified over two dimension -- Declaration and Complexity
    * How they're declared in a program
    * The complexity of the data they abstract

* Data types can be declared as explicit or implicit
* Operators in simple types can be combined into compound operators
    * Ex `x = x + y` can be `x += y`

* High level languages can be strongly or weakly typed, but the exact definitions
of these terms aren't agreed on, and these can be fluid.
* Generally, strongly types langauges have stricter rules at compile time that
affect variabble assignment, function return values etc. 
    * Examples given: C#, Java, VB.NET
* Weakly typed languages have looser type checking rules and may produce
erroneous results or implicit type conversion at runtime, how ever they tend to 
be more flexible. 
    * Examples given: Python, Javascript

#### Lesson 2
* Numeric data types - Python supports 3 numeric data type
    * int, float, complex numbers
    * In general, integers can vary in size based on the number of bytes 
    assigned to that integer type
    * Python uses "bignum" integers, which allow for arbitrary precision

#### Lesson 3
* Operators are performed on "operands" 
    * ex `1 + 2` the two integers are operands

* An expression involving an operator is evaluated in some way, and the 
resulting value may be a whole value (r-value) on the right hand side of an
assignment, or an object allowing assignment (l-value)

#### Lesson 4 and 5
* Composite data types combine several values together and tread them as a 
single unit
    * Ex structs, arrays, strings, classe, tuples, dict, set
* Classes can perform tasks, report and change their state, and communicate
via method calling
    * Classes have both structural (attributes) and behavioural (method) 
    components
* Tuples are immutable lists of fixed size
* Dicts are also known as maps, associative arrays, and symbol tables
