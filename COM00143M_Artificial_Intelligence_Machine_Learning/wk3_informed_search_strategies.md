# Week 3 - Informed Search Strategies

* Design heuristics for informed search algorithms.
* Implement informed search algorithms, including Greedy Best-First Search and A* Search
* Estimate the size and nature of the searches performed by informed search algorithms.

### Lesson 1 - Informed Search Strategies
These use additional information to help the algorithm to search the problem space more efficiently

Best-first search / greedy BFS.
A* search

Heuristic - a function that checks how close to a goal a particular node is.
- the heuristic function will be different for every algorithm as each algorithm works differently

GBFS - expands first the node with the lowest heuristic value (appears to be closest to the goal)
* It's called greedy because each iteration doesn't worry about the optimal cost, just travelling
    the first node in each layer it finds that gets the frontier closer to the goal
* The result solution may not be the most efficient
* Can be complete in finite search spaces but not infinite ones.
* worst case time/space is both O(V), but can be reduced to O(BM) in the best case

GBFS Algorithm pseudocode from wikipedia:
```
procedure GBS(start, target) is:
    mark start as visited
    add start to queue

    while queue is not empty do:
        current node <- vertex of queue with min distance to target
        remove current_node from queue

        for each neighbor n of current_node do:
            if n not in visited then:
                if n is target:
                    return n
                else:
                    mark n as visited
                    add n to queue
    return failure
```

If the heuristic has simple properties, then A* is guaranteed to find an optimal solution
A* takes cost into consideration as well as the heuristic. It is not required that the 
heuristic finds a goal state

`f(n) = g(n) + h(n)`
- g(n) is the path cost from the initial state to node n
- h(n) is the estimated cost of the shortest path from n to the goal

admissible heuristic - one that never overestimates the cost to reach a goal
    - an admissible heuristic is optimistic

A* properties
- It will always find a viable solution if one exists
- it will always find the optimal solution first
- It is optimally efficient

Contour - a boundary in the state space that encloses all states with a cost less or equal
to a set value

GBFS vs Iterative Deepening
    - GBFS does not regenerate nodes, Iterative Deepening does
    - the heuristic help GBFS select nodes close to the goal
