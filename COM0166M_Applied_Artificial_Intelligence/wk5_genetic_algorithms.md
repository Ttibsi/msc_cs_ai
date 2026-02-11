# Wk 5 - Genetic Algorithms

* Describe the biological basis and basic concept of genetic algorithms. [MLO 2 & MLO 4]
* Identify and apply the operators and parameters of genetic algorithms. [MLO 1]
* Apply the basics of genetic algorithms to well-known NP-complete problems. [MLO 1]
* Identify and discuss the constraints and applications of genetic algorithms. [MLO 1]
* Identify methods of current AI research and give examples of their application in state-of-the-art AI systems. [MLO 4]

### Lesson 1
Genetic algorithms originally are inspired by biological models -- selective
breeding of plants or animals. 

* rapidly generates multiple solutions for testing based on the initial 
solutions provided
* This works by generating every permutation of the input
* may arrive at a better solution than any of the input solutions
    * uses processes such as derivation or crossover

A genetic algorithm is a metaheuristic algorithm.
Uses biologically-inspired operators (selection, mutation, crossover) in an
iterative process of replacement.

Good parameter values in a genetic algorithm are essential, but these are mostly
down to the experience and knowledge of the programmer.

Stochastic sampling - random procedure plays an important part in selection and 
reproduction
solution memory - a population of individuals which allow for different individuals
to generate new individuals
    - Does this mean memoisation? Collection of better solutions similar to tabu search? :shrug:

