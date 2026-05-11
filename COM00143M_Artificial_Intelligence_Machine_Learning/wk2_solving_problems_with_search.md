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
