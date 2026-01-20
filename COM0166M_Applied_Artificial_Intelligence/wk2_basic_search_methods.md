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
