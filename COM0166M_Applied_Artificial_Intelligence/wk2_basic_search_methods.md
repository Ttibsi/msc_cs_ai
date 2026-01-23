# Wk 2 - Basic search methods

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
* Algorithm strength - fast and simple
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

