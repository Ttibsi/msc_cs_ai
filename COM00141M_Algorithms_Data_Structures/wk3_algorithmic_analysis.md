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
- Cubic time - O(n^3)
    - matrix chain multiplication
- Exponential time - O(c^n)
    - A solution that examples all possible sublists of a list
- Factorial time - O(n!)
    - problems where all possible permutations need to be considered

The RAM model uses maths to represent the complexity and performance of an algorithm
for example bubblesort (pseudocode from required reading)

```
BubbleSort(A, n):
    for i = 0 to n-2:
        for j = 0 to n-2-i:
            if A[j] > A[j+1]:
                Swap(A[j], A[j+1])
```

when i == 0, inner loop runs n-1 times (not n-2 as it's exclusive, like a python loop)
when i == 1, inner loop runs n-2 times

total iterations = (n - 1) + (n - 2) ... 

worst case - O(n^2)
best case - Omega(n^2)
    * Could this be refactored to be Omega(n) with a check before the inner loop starts?

When considering best case on a sort, think about what if the array is already
sorted, what would the algorithm do then?

```
OptimisedBubbleSort(A, n):
    for i = 0 to n-2:
        swapped = false
        for j = 0 to n-2-i:
            if A[j] > A[j+1]:
                Swap(A[j], A[j+1])
                swapped = true
        if not swapped:
            break
```

In this improved algorithm, worst case is still O(n^2), but best case is
Omega(n) because the outer loop would only iterate the once and break out
in the if statement.

----
Pseudocode development and analysis

Develop Pseudocode: Write pseudocode for an algorithm that determines whether a 
given sequence contains only unique elements. The algorithm should return True 
if all elements are unique and False otherwise.
Identify Best and Worst Case Scenarios:
    Best Case Scenario: Describe the input sequence that would result in the 
    best-case performance for your algorithm. What is the time complexity of 
    the algorithm in the best case?

    Worst Case Scenario: Describe the input sequence that would result in the 
    worst-case performance for your algorithm. What is the time complexity of 
    the algorithm in the worst case?

```
ALGORITHM check_unique(A)
    if length(A) is less than 2
        return true

    let visited be an empty list
    for elem in A
        for item in visited
            if item is equal to elem
                return true
            
        visited.insert(elem)
END
```

---
Turning someone else's pseudocode into python code:
```
def all_unique(A: list[int]) -> bool:
    checked_list = set()
    for elem in A:
        if elem in checked_list:
            return False
        else:
            checked_list.add(elem)
    return True

assert all_unique([1,2,3,4,5]) == True
assert all_unique([1,1,1]) == False
assert all_unique([1]) == True
```

It was cleverly identified that you could just turn a list into a set
and compare their lengths: `return len(set(A)) == len(A)` as sets have O(1)
lookup whereas lists have O(n) lookup
