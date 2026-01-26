# Week 3 - Local Search and Metaheuristics - Hill climbing 

* Select and apply appropriate AI algorithms and methodologies, with consideration for optimisation and scale to meet business objectives and performance targets. [MLO2 & MLO3]
* Critically evaluate AI-methodologies through experimental design, exploratory modelling, and hypothesis testing. [MLO2 & MLO3]
* Identify and discuss appropriate application areas and problems for current AI techniques, such as: neural network, deep learning, genetic algorithms and local search approaches. [MLO2 & MLO3]

### Lesson 1 - Simple Hill Walking Algorithm
Starts with an initial solution to a problem and then continues until it
reaches a "local optimal" solution.

```
input: initial solution
final solution s = []
s = s[0]
while not termination criterion do
    generate a candidate solution s[t] by exploring neighborhood of s
    evaluate candidate solution (C(s[t]))
    if (C(s[t])) is better than C(s)
        assign s[t] to s (s = s[t])
end while
output final solution s (local optima)
```

* What is the initial solution?
* What is the termination condition?
* What is the candidate solution
* How can we evaluate the solutions

in TSP, we can randomly choose two cities to swap and see if it makes the 
route any faster

How to create an initial path 
The greedy nearest neighbor approach is to find the neighbor with the 
smallest distance to travel.

For a stopping/termination condition, we will need to define a number of
iterations to work through, and we halt either when we hit that or 
when there are no improvements over x iterations.

* Simple hill walking's main decision is to move to the first neighbor that 
improves the current solution
* Limitations
    - can get stck on plateaus
    - does not backtrack
    - may stop at local optima

### Lesson 2 - Steepest Ascent Hill Climbing
While the simple hill climbing only explores it's nearest neighbor, steepest
ascent evaluates all neighboring elements to find the most optimal candidate.

```
Input:initial solution s_0
Final solution s=[┤]
s= s_0
While not termination criterion Do
      Generate candidate solutions N(St ) by exploring partial or complete neighbourhood
      Evaluate candidate solutions (C(N(st ))
      Select a solution(s') from C(N(st )) to replace the final solution
      if C(s' )  is better than C(s)
            Assign s' to s  (s= s' )
     End if
End While 
Output: Final solution s (local optima) 
```

Main difference: Generating valid candidates - fron all candidates in the 
neighbourhood, not just the next unit

in TSP, we collect all possible options by swapping every pair. 
Ex for a list of 8 cities, iteration 1 would have 7 possible options, as we
swap each valid pair individually and calculate cost.

This can still get stuck in local optima. 
    - You could try running the algorithm multiple times
    - or trying different patterns for swapping
Generally is faster than simple hill walking


Steepest Ascent is better than Simple Hill Walking as it checks all possible
permutations of two adjacent elements being swapped instead of just a single swap.

Swapping strategies
* inversion operator - I don't really understand this, but from the diagram, it
    looks less like swapping and closer to when you change the pointers on two
    elements of a linked list, so if you swap 3 and 7, you instead break the 
    connection between 2 and 3 and have 2 point to 7, then have 3 point to 8 instead
    so following the chain of nodes results in a single loop
* 2-opt operator - select two non-adjacent edges and remove the edges and reconnect
    the open nodes in a different order. 
    * The same design can be used to design a 3-opt operator
