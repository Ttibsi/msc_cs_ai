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
