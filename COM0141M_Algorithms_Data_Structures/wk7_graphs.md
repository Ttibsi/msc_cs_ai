# Wk 7 - Graphs and Graph Traversal

* Implement graphs using adjacency lists and adjacency matrice. [MLO 1]
* Analyse the properties of graphs and graph representations. [MLOs 1,2]
* Write pseudocodes for several graph  algorithms and demonstrate how they work  [MLOs 1,2].
* Construct computer programs to implement graph  algorithms and analyse their performance  [MLOs 3,4].
* Implement and test a computer program against its specification. [MLO 4]

## Lesson 1 - Graphs and graph traversal
* Graphs can represent any form of relationships
* Not every vertex has to have edges
* Dense graphs - the number of edges is close to the maximum possible number of
    edges
* Sparce - opposite, has only a few edges in comparison to the number of vertices

* Complete graph - Each pair of vertices are joined by an edge
* Undirected - graph edges don't have a direction
* Directed - edges have a direction - (U->V) is not the same relation as (V->U)
    - also called a digraph
* Weighted graph - edges contain a weight, such as distance or cost
    - Edges could be represented like (U, V, W) where W is the weight
    - EX (U, V, 5) is a weighted, undirected node.
    - weighted graphs can be directed or undirected
    - Weights can be negative
    - Directed graphs can have different weights depending on the direction
* Path - a sequence of edges that are all distinct
* Connected graph - undirected graph where every vertex is connected in a path
* Disconnected graph - A graph that isn't connected

Representing Graphs
* Option 1 - Edge list
    - A list of triplets holding the source, dest, and weight
    - ex [(A, D, 1), (A, C, 3), (A, B 4)]
    - Main issue - lack of structure,
        - to get a list of all vertices, you must traverse the whole list
        - doesn't contain vertices with no edges
        - Could be solved with two lists, one of edges and one of vertices, but
        this takes up a lot of space in memory
* Option 2 - Adjacency matrix
    - A 2d array, where `matrix[u][v]` contains the weight of going from u to v
    - undirected graphs will repeat every value - `matrix[u][v]` will be the
    same as `matrix[v][u]`
    - if no edge exists, conventions to fill those space include filling those
    cells with infinity or zero, depending on the problem trying to be solved
    - Unweighted graphs can just use booleans, or 1 and 0
* Option 3 - Adjacency list
    - A map from vertices to their list of edges
    - ex `{A: [(D, 1), (B, 3)], B: [(D, 2)], D: []}`
    - The keys only store the source vertices

Edge list
    - Efficient for sparse graphs
    - O(E) lookup, linear with respect to the number of edges
    - Faster to iterate over every edge
Adjacency Matrix
    - efficient for dense graphs - O(v^2)
    - O(1) lookup
    - Slow to iterate over every edge - O(v^2)
        - note, this is a 2d array, same asymptotic time here
        - this is less of an issue when the graph is more dense
Adjacency List
    - Efficient for sparce graphs
    - Faster to iterate over every edge

A graph with both directed and undirected edges is called a Mixed Graph
    - EX map of roads, some go both way, some are one way roads

### Graph traversal
* Two main approaches -Depth first and breadth first search

* DFS - Can be used to see if a graph has a cycle or not
    - Mark a node as visited
    - Pick an edge that has not been used (at the start, all of them)
    - Mark a node as visited when you've gotten there
    - Recurse - keep exploring until you've hit everything
    - We also need a way to keep track of what we've already visited


pseudocode impl:
```
procedure dfs(g: graph, s: vertex, visited: list[bool]):
    if visited[s]:
        return

    visited[s] = True
    doThing(s) # could be a print or something

    # implicitly this recursion will also handle the backtracking
    for neighbor in s.neighbors():
        dfs(g, next, visited)
```

If there are nodes disconnected from the starting node, they won't be reached
by the DFS algorithm -- you will need to select a new node to start from once
the above algorithm finishes, if there are still unvisited nodes

Alternate approach using iteration, this uses a stack, emulating the callstack
of the recursive approach
- Post node to the stack
- pop the node off the top of the stack
- collect all it's unvisited adjacent nodes and push those on the stack
- if an adjacent node is marked as visited, don't add it back to the stack
- mark the popped node as visited, move on to next node in the stack

```
Algorithm DFS(G, source):
    beingVisited = stack()
    beingVisited.push(source)

    visited = [False for elem in G]
    visited[source] = True

    while beingVisited is not empty:
        current = beingVisited.pop()
        process(current)

        for each adjacent node [V] to current:
            if not visited[V]:
                beingVisited.push(V)
                visited[V] = True
```

time complexity: O(V + E)

Breadth first search - uses a queue to store the discovered vertices
Otherwise, the algorithm is similar to above

```
Algorithm BFS(G, source):
    beingVisited = Queue()
    beingVisited.enqueue(source)

    visited = [False for elem in G]
    visited[source] = True

    while beingVisited is not empty:
        current = beingVisited.dequeue()
        process(current)

        for each adjacent node [V] to current:
            if not visited[V]:
                beingVisited.enqueue(V)
                visited[V] = true
```

time complexity: O(V + E)

DFS is useful when searching a maze, or scenarios where you will need to 
backtrack on your path, whereas BFS is more useful in cases when you need to 
know the distance between two points.

## Lesson 2 - Dijkstra's shortest path

* Find the shortest path from any one node to another
* We use a process called edge relaxation that uses a table to store the distance
of each node from the starting node. To start, each node is set to "infinity"
distance away.

```
Algorithm ShortestPath(G, source):
    distance = infinity for each element
    distance[source] = 0

    pq = PriorityQueue()
    insert every vertex in G into PQ

    while pq is not empty:
        u = pq.remove_min()
        for each adjacent node [V] to u:

            # This is the relaxation section
            if (distance[u] + weight(u, V)) < distance[V]:
                distance[V] = distance[u] + weight(u, V)
    return distance[V] for for each vertex V

```

* DSP may not work if there are any negative distances
* This is a greedy strategy

* The idea here is that we aren't popping off the PQ, we're just reading from it.
This lets us lean on the automatic reordering to know the shortest distance to
any node, I think.

## Lesson 3 - Prim-Jarnik's Minimum Spanning Tree
Spanning tree - a subgraph of an undirected graph that includes all the vertices
while forming a tree
    * is Connected
    * contains no cycles
    * V-1 edges for V vertices
    * uses the minimum number of edges to maintain connectivity

Useful for simplifying complex graphs for analysis and optimisation
    * easier to explore relationship, identify key pathways, solve practical
        problems
    * in network design - used to ensure all nodes are connected without
    redundancy

finding a subset of edges in a weighted, undirected graph that connects all
vertices with the least total edge weight

exclusion of the heaviest edge in any cycle
    - by removing the heaviest edge, you maintain connectivity while reducing
    weight
inclusion of the lightest edge

Primm-Jarnik uses a priority queue to select which edges to include
1 - initialise a tree with a single vertex, chosen arbitrarily
2 - grow by one edge, finding the smallest weight attached node
3 - repeat step 2 until all vertices completed

Unlike above, this pseudoecode comes from wiki, with added comments by myself
```
function Prim(vertices, edges):
    // step 1, setup
    for each vertex in vertices:
        cheapestCost[vertex] = inf
        cheapestEdge[vertex] = Null

    explored = set()
    unexplored = set(all vertices)
    start = any vertex
    cheapestCost[start] = 0

    // step 2 - iterate through all elements and find the min weight
    while unexplored is not empty:
        // select vertex in unexplored with min cost
        currVertex = vertex in unexplored with min cheapestCost
        unexplored.remove(currVertex)
        explored.add(currVertex)

        for each edge(currVertex, neighbor) in edges:
            if (
                neighbor in unexplored and
                weight(currVertex, neighbor) < cheapestCost[neighbor]
            ):
                cheapestCost[neighbor] = weight(currVertex, neighbor)
                cheapestEdge[neighbor] = (currVertex, neighbor)

    // step 3 - build the MST from the cheapest edges
    resultEdges = []
    for each vertex in vertices:
        if cheapestEdge[vertex] is not null:
            resultEdges.append(cheapestEdge[vertex])

    return resultEdges
```

Not that the set above could be implemented as an array or priority queue.
Using a PQ, each operation runs in O(log n) time, with a total of O(m log n)
for a connected graph
Using an unsorted list instead results in O(n^2)

Note, an MST doesn't have to be a BINARY tree
