# Week 2 - Solving Problems with Search

* Represent search problems as states, actions, and goals.
* Implement the simplest search algorithms, including Depth-First Search, Breadth-First Search and Iterative Deepening
* Estimate the size and nature of the searches performed by uninformed search algorithms.

### Lesson 1 - Representing problems as AI search problems
How to represent real-world problems to be solved using AI search
* States, actions, goals

Route finding can be represented directly as an AI search problem
* states = set of locations
* actions = driving from one location to another
* step cost = length of each road

Some problems can have multiple states, and there is a benefit to finding the formulation that
reduces the number of states.
    - this is likely where something like genetic algorithms come in
    - One example is the 8-queens problem. I think you need to find the starting position of
    8 queen pieces on a chessboard that reduces the amount of moves that can be possible

Transition model: takes a state, applies an action, produces a new state
initial state of an incremental formulation: empty
There is (usually) only one goal state

English Peg Solitaire
States: A state description specifies which locations are populated with pegs
Initial State: All but the center hole is populated
Actions: Any movement that allows a peg to "jump" over another peg to populate an empty slot.
    The peg that was jumped over is removed from play
Transition Model: The state resulting from any legal move will have x-1 pegs remaining, two
    previously filled holes empty, and one previously empty hole filled
Goal state: Only one peg is remaining on the board
Action cost: Each action costs 1

### Lesson 2 - Tree Search and Graph Search
search algorithm - takes a search problem and returns a solution
state space != search tree
    - state space = set of states in the input tree (may be infinite),and the actions that
        allow transition from one to another
    - search tree - may have multiple paths to/multiple nodes for any given state, but each
        node has a unique path back to the root

Best-first search
- choose a node with some minimal value of an evaluation function
- also called greedy BFS (See AppliedAI wk 2)

search algorithms require a data structure to keep track of the search tree -a Node type
Nodes usually have 4 components:
- state
- parent
- action
- path_cost

Following the parent pointers back should always result in the root
We also need a data structure to store these queues to follow the "frontier". For this,
we can use a queue

frontier - the solution path currently being built

Handling redundancy in paths: three options
- remember every previously reached state (GBFS does this)
- don't worry about repeating the past - In some problems, it'd be very rare or impossible
- compromise and check for cycles but not redundant paths in general

Evaluate an algorithm in 4 ways
- completeness
- cost optimality
- time complexity
- space complexity

### Lesson 3 - Uninformed Search Strategies
Uninformed search algorithms are given the formulation of the problem ( the search space ) and
nothing else. They can't estimate how close they are to the goal.
These are sometimes called blind search.

informed search algorithms use functions called heuristics to calculate how good their selections
have been

Breadth-first search
    - Uses a queue

BFS pseudocode from "Artificial Intelligence: A Modern Approach" section 3.4 (fig 3.9)
```
function BREADTH-FIRST-SEARCH(problem) return a solution node or failure
    node <- NODE(problem.INITIAL)
    if problem.IS-GOAL(node.STATE) then return node

    frontier <- FIFO queue with node as an element
    reached <- problem.INITIAL

    while not IS-EMPTY(frontier) do
        node <- POP(frontier)

        for each child in EXPAND(problem, node) do
            s <- child.STATE
            if problem.IS-GOAL(s) then return child
            if s is not in reached then
                add s to reached
                add child to frontier
    return failure
```
Time and space complexity are both O(n^2) as every node remains in memory

Depth first Search
    - uses a stack / LIFO
    - two types of algorithm - one for trees, one for graphs

Depth-limited search is a limited form of DFS that will only search until it hits a specific
depth, considering any nodes below that depth as non-existant. This prevents an infinite loop
when traversing a graph as the algorithm will give up and try a different route instead.

Iterative Deepening search builds on this, this is an algorithm that checks every element in a
given depth before moving on to the next depth layer until a solution is found.

```
function ITERATIVE-DEEPENING-SEARCH(problem) returns a solution node or failure
    for depth = 0 to INF do
        result <- DEPTH-LIMITED-SEARCH(problem, depth)
        if result != cutoff then return result

function DEPTH-LIMITED-SEARCH(problem, l) returns a node or failure or cutoff
    frontier <- stack with NODE(problem.INITIAL) as an element
    result <- failure

    while not IS-EMPTY(frontier) do
        node <- POP(frontier)
        if problem.IS-GOAL(node.STATE) then return node

        if DEPTH(node) > l then
            result <- cutoff
        else if not IS-CYCLE(node) do
            for each child in EXPAND(problem, node) do
                add child to frontier
    return result
```
