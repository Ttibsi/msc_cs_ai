# Wk 3 - Algorithmic Analysis

* Construct pseudocodes to solve computational problems. [MLO1]
* Evaluate algorithm performances through asymptotic analysis using Big-O notation. [MLO2]
* Develop functions in Python to design modular programs [MLO3]
* Develop and apply test cases to evaluate the validity of programs [MLO4]

pseudocode - Designed to focus on the logic, not the technicalities of the 
implementation

- Useful for communicating algorithms to others, inc non programmers
- Useful for planning before you start programming
- Simple and clear, structured, abstract

Insertion sort
- initialise the sort starting from the second element
- compare it with the elements to its left
- swap if the current element is smaller
- move left until the correct position is found or the start of the list is reached
- repeat until all the elements are sorted

Algorithmic "big o" functions
- Constant time - O(1)
- Logarithmic time - O(log n)
    - binary search
- linear time - O(n)
    - linear search
- Log-linear time - O(n log n)
    - Merge sort
    - Quick sort
- Quadratic time - O(n^2)
    - Insertion/selection sort
- Cubic time - O(n^3)n^
    - matrix chain multiplication
- Exponential time - O(c^n)
    - A solution that examples all possible sublists of a list
- Factorial time - O(n!)
    - problems where all possible permutations need to be considered
