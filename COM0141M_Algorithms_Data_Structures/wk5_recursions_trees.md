# Wk5 - Recursion and Trees

* Write pseudo-code for non-linear data structures and demonstrate how they work [MLO1].
* Analyse the properties of binary search trees[MLO2].
* Analyse the performance of non-linear data structures  in their application to search algorithms.[MLO1].
* Design and implement recursive algorithms in Python, and assess their limitations. [MLO 3].

Recursion - when a function calls itself
    - requires a "base case" to break out
    - pre and post conditions around the recursion call

Recursion is useful for nested data structures such as trees and graphs
or maths algorithms like fibonacci

- "In mathematical logic and computer science recursive definition or inductive definition is used to define an object in terms of itself."

```py
# factorial recursive func
def factorial(n: int) -> int:
    return n * factorial(n - 1) if n else 1
```

All recursive implementations can be implemented as iterative as well

* Recursion will not make your code more performant. It's benefit is simpler code
and may aid in calculating runtime easier

* Memoisation is the case in which we have something that stores our state
as we go. For example, the below fib implementation with an inner func that uses
a dict to store values.

```py
def fib(n: int) -> int:
    def fib_inner(n: int, mem: dict[int, int]) -> int:
        if n in mem.keys():
            return mem[n]
        elif n == 0 or n == 1:
            mem[n] = n
            return mem[n]
        else:
            mem[n] = fib_inner(n - 1, mem) + fib_inner(n - 2, mem)
            return mem[n]

    return fib_inner(n, {})
```
