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

