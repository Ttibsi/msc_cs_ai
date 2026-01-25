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


