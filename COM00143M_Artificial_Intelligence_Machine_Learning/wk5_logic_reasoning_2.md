# Week 5 - Representing and Reasoning with Logic 2

* Represent decision problems and logical entailment as propositional satisfiability
* Apply reasoning algorithms to solve the satisfiability problem in propositional logic.

# Lesson 1 - The Satisfiability problem in Propositional Logic
Satisfiability problem = SAT

Model - An assignment of each of the propositional symbols to True or False
Entailment - The idea of a sentence following logically from a KB
Inferrence - A computation that derives new entailed sentences from an existing KB
Conjunctive Normal Form - A standard form for logic formulas.

Satisfiability is used in planning, scheduling, resource allocation
Satisfiability - the problem of finding a model that satisfies a logic formula. A formula
is considered "satisfiable" if it has a model. This can be used if sentences can't be simplified
to CNF.

Satisfiability is an NP-complete problem and will take exponential time:
    n proposition symbols
    2^n models
    O(2^n) time to check

If we are looking for a formula F that proves a true ( `F |= a` ), then we can't look through
every model to check entailment (reminder `|=` is the entailment symbol) as this will take a long
time. We can instead check for `F ^ ¬a` instead, inverting it. If there are no models that 
match this, then `a` must be entailed.

Solving a decision problem with SAT:
1 - represent the decision problem as a formula
2 - Solve using a SAT algorithm
3 - if the SAT algorithm found a model, translate into a solution to the original problem

Soduku example:
* Taking one sub-square from a soduku board, each empty space can be a letter.
* We can write rules around what numbers each letter could be
* We can then write rules using `v` (or) to denote how only one letter can be a given number
* Write rules to denote that a square only has a single number in it
    ( No two numbers can be in the same letter using `¬` and `v` )

### Lesson 2 - A Complete Backtracking Algorithm for SAW
DPLL algorithm - Named after the four people who invented it
    - Dates back to the 1960s, but has been expanded on and "current versions are almost 
    unrecognisable"
    - "complete" = guarunteed to find a solution given enough time
        - note that this could be longer than the length of the universe
    - DPLL runs in exponential time
    - Based on DFS

* A partial model assigns some of the proposition symbols to true and false, and leaves others
unassigned
* DPLL starts with an empty partial model and attempts to find a way to extend it step-by-step
until the formula is satisfied
* DPLL is a binary-tree (every node has exactly 2 children) traversed in a depth-first search order

Time complexity: `O(2^n)` where `n` is the number of proposition symbols
Can be efficient, but not guaranteed to be

DPLL requires a formula to be in CNF
Usually implemented recursively
Frontier set usually not stored in memory at all

* DPLL features early termination, meaning if a part of the statement is true, then the whole
statement is true, and the algorithm can break out of it's calculations
* Pure symbol - a symbol that appears with the same sign in every clause (either `¬` for 
negation or not)
* Unit clause - a clause with just a single true/false literal

```
function DPLL_SATISFIABLE(s) returns true or false
    inputs: s, a sentence in propositional logic

    clauses <- a set of clauses in the CNF representation of s
    symbols <- a list of propositional symbols in s
    return DPLL(clauses, symbols, {})

function DPLL(clauses, symbols, model) return true or false
    if every clause in clauses is true in model
        return true

    if any clause in clauses is false in model 
        return false

    P, value <- FIND_PURE_SYMBOL(symbols, clauses, model)
    if P is non null
        model.add({P=value})
        return DPLL(clauses, symbols - P, model)

    P, value <- FIND_UNIT_SYMBOL(symbols, clauses, model)
    if P is non null
        model.add({P=value})
        return DPLL(clauses, symbols - P, model)

    P <- FIRST(symbols)
    rest <- REST(symbols)
    model.add({P=true}) or model.add({P=false})
    return DPLL(clauses, rest, model)
```

