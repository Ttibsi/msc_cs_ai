# Week 4- Metaheuristics - Tabu Search and Simulated Annealing

* Design heuristics for Tabu search and Simulated Annealing. [MLO 2, MLO 3 & MLO 4]
* Implement search algorithms for Tabu search and Simulated Annealing. [MLO 3 & MLO 4]
* Identify some of the methods of current AI research and be able to give examples of their application in state-of-the-art AI systems. [MLO 4]

### Lesson 1 - Simulated Annealing
One method to escape local optima is to accept poor moves to try and reach a
better global result

Simulated Annealing is inspired by the annealing process in metalworking, where
a structure is heated and cooled to make it overall stronger.

The algorithm is given a "temperature" value, and the probability of a random
result being accepted is calculated as a function of the change in cost divided
by the temperature value. This is usually given as a decimal between 0 and 1.

Finding the right value for this temperature is part of the challenge.
If a temp is too high, there is a risk of this becoming a random walk algorithm.

The temperature can change during runtime, usually starting high and slowly
decreasing (not on every single iteration) to try and find a globally better
result.

Cooling factor - The temp is reduced gradually so that the final solution can
settle near the regions of the global optima. Normally alpha is kept between
0.5 and 0.99

### Lesson 2 - Simulated Annealing Algorithm
In this lesson, we run through an example of Simulated Annealing.
* Initial route - 364178253

Acceptance probability:
curr: 45, neighbourhood: 50, temp: 70, probability: 0.93
curr: 20, neighbourhood: 50, temp: 70, probability: (-)0.42
curr: 20, neighbourhood: 50, temp: 20, probability: 1.5?
curr: 45, neighbourhood: 50, temp: 10, probability: 0.5

High alpha can lead to not enough exploration and will converge on a locally
optimal solution. Low alpha will take too long to cool down.

SA can be stopped before them temp reaches 0, but probably manually by the
programmer.

### Lesson 2 Exercise - Paper analysis
The following notes concern the article "Simulated Annealing in Optimisation of Energy
Production in a water supply network" published in 2016 by Irene Samora, Mario J
Franca, Anton J Scheiss, and Helena M Ramos

In this paper, the authors were researching the best placement for turbines within the
water systems of Lausanne, Switzerland to usilise the existing flow and pressure for
hydropower generation. Their solution involved a much more complex version of the
simulated annealing algorithm, predominantly due to the number of variables involved
in the real-world that they needed to simulate. The neighbourhood operator was
defined so as to allow for a temporary minimum value of 0 due to the number of
variables involved in the simulation, and the implementors reran the simulation
for both 1 and 2 turbines involved, up to a maximum of 100 and 200 iterations.

Terminating conditions depended on the rate of water flow and the amount of power
a given turbine could generate at a given node. The implementors found that
with only a single turbine, the algorithm routinely found the optimal location
before it's 50th iteration, but when running the algoritm for two turbines, they
were finding that they had to "blacklist" a specific route as it wouldn't be
practical in the real world, but the algorithm continuously wanted to place
a turbine in that route.
