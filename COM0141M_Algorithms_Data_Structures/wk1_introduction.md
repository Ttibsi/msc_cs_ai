# Wk 1 - Introduction to algorithms

* Explain what an algorithm is. [MLO1]
* Apply algorithms to develop step-by-step solutions for a given problem. [MLO1]
* Translate/Express algorithms in plain English.  [MLO1]
* Develop your first program in Python. [MLO3]

Algorithm - A step by step procedure or set of rules designed to solve a specific
problem or solve a task.

Algorithm Design Manual - Skiena, Steven S.
* It is considered important "and honourable" to narrow a set of allowable instances
until there is a correct and efficient algorithm ( page 12)

Algorithms are often written in 1) english, 2) pseudocode, then 3) a real
programming language

Correctness - ensuring the algorithm produces the right output no matter the input
Efficiency - how well the algorithm uses resources like memory or time

Finiteness - Any algorithm should always come to an end, not get stuck in an infinite loop
Unambiguity - 
Sequencing - Ensure the steps are in the right order
Feasability - Can be executed within the given resources


------
The below notes are more appropriate for a later week

Algorithm Design Manual - Skiena, Steven S.
Ram Model
* A simple operation takes exactly one time step
    - math symbols, if stmt, calls
* loops and subroutines are not considered simple
* Each memeory access takes exactly one time step

Big O Notation
* The exact time complexity for any algorithm is likely to be complicated by
real world details and will require too many details to specify exactly. 
Instead, we use big O, which ignores certain details that do not impact our 
comparison of different algorithms.

* Constant functions `f(n) = 1`
    - A constant action
* Logarithmic functions `f(n) = log n`
* Linear functions `f(n) = n`
    - Looking at every element in a set
* Superlinear functions `f(n) = n log n`
* Quadratic functions `f(n) = f^2`
    - Looking at every pair to be made of a given set 
* Cubic functions `f(n) = n^3`
* Exponential functions `f(n) = C^n`
    - when enumerating a subset of n items
* Factorial functions `f(n) = n!`
    - when generating all permutations of n items
