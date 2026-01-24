
* Identify and understand basic difficulties in problem solving and the need for heuristic optimisation. [MLO 3 & 3]
* Apply the basic concepts of heuristics and design heuristics for search algorithms. [MLO 2 & 3]

# Lesson 1 - Uninformed Blind Searches
* Uninformed search, also called blind search.
* Used in environments where no info on the search environment is available
    * EX getting out a maze you cannot see 
* These tend to be valid but inefficient strategies
* This is DFS and BFS

Breadth first search
* Uses a Queue data structure

Depth first search
* Uses a stack data structure
* visits one node per depth at a time during iteration

Uninformed search variants extend BFS and DFS to address limitations
* Infinite paths
* unknown solution depth
* expensive actions

Examples
* Uniform Cost Search - Select and expand the node with the lowest cost path
    * equivalent to Dijkstras shortest path
    * time complexity: O(b ^ c + 1)
    * space complexity: O(b ^ c + 1)
* Depth-limited search (DLS)
    - a DFS variant with a fixed depth limit to prevent infinite descent
    * time complexity: O(b ^ L)
    * space complexity: O(b * L)
* Iterative deepening depth first search 
    - combines the space efficiency of DFS with the completeness of BFS
        - lower memory usage than BFS
    - repeatedly applied DLS with increasing depth limits until it succeeds or fails
    - particularly effective when the search space is large or solution depth is unknown
    * time complexity: O(b ^ d) 
    * space complexity: O(b * d)
* bidirectional search
    - Two searches at once - one forward from the start and one back from the goal
    -  meet in the middle, reducing the search space
    * time complexity: O(b ^ d/2)
    * space complexity: O(b ^ d/2)

big o notation key:
b - branching factor
c - constant
d - solution depth
L - depth limit

Common uses of uninformed searches
* grid-based problem solving
* pathfinding
* data structure traversal
* game AI, ex NPC routing
* web crawling
* automation of planning activities -- ex project management

### Lesson 2 - Informed Heuristic search
In an informed search, the algorithm will use information provided about the search space to guide the search
    * EX - distance of the current node from the goal state 
    * cost of traversing nodes
    * how to reach goal state

Heuristic - a cost function that is used to evaluate certain paths
    * Not guaranteed to provide the best solution, but will always provide a good solution

Greedy BFS
* Also called "best-first search" 
* Uses a heuristic to provide the estimated cost to the goal node
* expands the node that looks "closest" to the goal
* In this case, this means that it's taking the next node with the shortest distance in a weighted graph
* weaknesses - not the shortest path
    - can get stuck "in local optima", picking a node that appears to be close but leads to a longer route

Example pseudocode
```
Algorithm GBFS(graph, goal)
    N = add parent node in the data structure
    while N is not empty

        L = based on the heuristic select the best successor node of N
        if L is a goal state
            return success and exit
        N = L
    end while
```

A* Algorithm
This popoular algorithm considers the cost of travelling from node n to it's successor
and then the successor to the goal. This will always prioritise the node with the minimum
cost

* A* is better than GBFS as it will find the shortest path based on the heuristic
* It avoids unnessecary detours by balancing costs and estimates
* A* also uses more memory
* A* uses both the distance already travelled to a node and the straight line distance from n to the goal

Other variants of informed heuristic serarch algorithms
* Beam search - explores only the best K nodes at each level
    - sacrifices completeness for efficiency
    - time complexity: O(`b*d`)
    - space complexity: O(kd)
* Iterative Deepening A* (`IDA*`) - Combines A* with iterative deepening with a cost threshhold
    - memory efficient compared to `A*`, while more complete
    - nodes are re-expanded on each iteration
    - time complexity: exponential, but based on heuristic
    - space complexity: linear
* Recursive Best-first search - memory-bounded version of A*
    - recursively explores the best path and backtracks when it hits a cost limit
    - uses linear space, efficient for large problems
    - time complexity: Similar to A* but with pruning
    - space complexity: linear
* Bidirectional heuristic search
    - Expands bidirectional search by applying heuristics
    - time complexity: O(b ^ d/2) but with guidance
    - space complexity: O(b ^ d/2)

* A* search
    - time complexity: O(b^d)
    - space complexity: O(b^d)
* Greedy best-first
    - time complexity: O(b^m) worst case
    - space complexity: O(b^m)

Common uses of informed searches
    * initial pathfinding estimates
    * natural language processing
    * game AI
    * web crawling
    * image processing

Frontier - the next nodes to consider

### Lesson 3 - Search Scenarios

Travelling Salesman - We have n citieis and d is the distance matrix between
each pair of cities. The goal is to find the shortest route that visits each
city only once and returns to the starting city

Knapsack problem - There are a number of items n each with a specific weight
and value (w, v). The knapsack has a maximum weight limit. The goal is to find
the subset of items the knapsack can contain while keeping the weight under the
knapsack's total. In this problem there are two conflicting objectives: 
weight restriction and highest possible value

Vehicle Routing problem - There are a fleet of vehicles n with are stored at
a specific place, and a number of customers m spread out across various locations.
This algorithm optimises the route for the set of vehicles so that a subset of 
customers are served

Cutting Stock problem - There is a stock material of a predefined size, ex
sheet metal and the objective is to cut that stock into n specific sized pieces
while minimising weight

Job Shop problem - There are a number of machines m with varied processing 
power, and a number of jobs n with varied time processing requirements. The 
goal is to minimisae the overall processing time while executing all the jobs
on all the machines.


These are combinatorial problems, and it's hard to calulcate solutions for them.
Travelling salesman is a very popular example.
Real world examples include:
    * shortest path between a source and a destination
    * internet data package routing
    * supply chain optimisation
    * protein structure sequencing
    * pattern recognition
    * job scheduling and timetabling.

#### Travelling Salesman Task
                                A
      B                C                D                E
 C    D    E      B    D    E      B    C    E      B    C    D
D E  C E  C D    D E  B E  B D    C E  B E  B C    C D  B D  B C

A<>B = 07 
A<>C = 06
A<>D = 10
A<>E = 13
B<>C = 07
B<>D = 10
B<>E = 10
C<>D = 05
C<>E = 09
D<>E = 06

The tree takes O(n!) space and has O(n-1) height. Plus an extra O(n-1!) space for the edges
This tree has a branching factor of d - (n-1) where d is the depth of the node
From this point, we can DSP our way to the shortest path

Using DSP and then making sure we make it back to A, my path is:
A > C >  D >  E >  B >  A
  6   11   17   27   34

At a total cost of 34

