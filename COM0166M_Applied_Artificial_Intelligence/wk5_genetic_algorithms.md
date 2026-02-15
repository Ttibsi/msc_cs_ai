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

### Lesson 2 - Operators and Parameters
Parameter tuning - the process of finding good values for parameters before running an algorithm
    - Changing the numbers and see which gives the best result
    - Dynamic process
Parameter control - parameters can be changed during runtime
Parameters may need tuning repeatedly at different stages of the run

Example of genetic programming: https://www.datacamp.com/tutorial/genetic-algorithm-python

uniform crossover - a mutation technique that has two chromasomes of the same length and
applies a mask over it of the same length.

* For Oa, we take the bit from Ia if it's 1 or Ib if it's 0. For Ob, we do the reverse

```
Ia - 1 0 1 1 0 0 0 1 1 1
Ib - 0 0 0 1 1 1 1 0 0 0

MASK 0 0 1 1 0 0 1 1 0 0

Oa - 0 0 1 1 1 1 0 1 0 0
Ob - 1 0 0 1 0 0 1 0 1 1
```

MLP - multilayer perceptron
* A modern neural network consisting of neurons with nonlinear activation functions
* Trained using backpropagation
* Also called "vanilla" networks
* basis of deep learning
* consists of 3+ layers
    - input layer (training data)
    - hidden layers ( all the inner nodes)
    - output layer
    - Each node in one layer connects with a certain weight to every node in the next layer

Chromosome - A permutation?

### Lesson 3 - Genetic Algorithm Constraints
Objective of any search algorithm is to stay within feasable solutions from the search space.
In a genetic algorithm, the crossover operator can be responsible for producing unfeasable
solutions

For example, in the travelling salesman, the crossover operator could result in
the same city being visited twice, or not at all. Ways to handle this include:
* remove unfeasable solutions from the population
    * This is inefficient, but easy
* Use some process to repair an unfeasable solution
* Use only operators that are guaranteed to produce feasable solutions
* Transform the search space (Decoding)

The most common approach to indirectly dealing with unfeasable solutions is to attach
a penalty function for their existing evaluation function

Order crossover - given two parents, take a range of genes from parent 1 then iterate
through parent 2 to find valid genes to insert in the offspring to fill the remaining
gaps, ensuring no repeats

NLP = Non Linear Programming

The numbver of real-world applications for genetic algorithms are vast.
* Roulette-wheel selection is designed to favour stronger individuals
* Examples of mutation: random, inverse, adjacent
* Tournament selection chooses the best individual from a random subset
