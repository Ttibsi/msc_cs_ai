# Week 4 - Representing and Reasoning with Knowledge

* Represent scenarios in propositional logic, and be able to perform rearrangements of logic 
sentences into conjunctive normal form.
* Apply reasoning algorithms for propositional logic with Horn clauses: forward and backward 
chaining.

### Lesson 1 - Principles of Logic and Propositional Logic
knowlege-based agents use a process of reasoning over an internal representation of knowledge to
decide what actions to take
A knowledge base is represented as a set of sentences. (sentence is a technical term, not identical
to the english language understanding of sentences).
Axioms are sentences not derived from any other sentence

TELL informs the knowledge base
ASK queries the knowledge base

PEAS: Performance, environment, actuators, sensors
Possible World - a description of the state of the world we are representing in logic.
    - ex game state in a board game/card game
    - This isn't a formal/precice thing but must be complete

Logical entailment - the idea that a sentence logically follows from another sentence
    This is denoted as `a |= b`
    ex: `a |= b if and only if M(a) c M(b)` (c is the "subset-of" symbol in set theory)

stanford source on subset-of symbol:
https://web.stanford.edu/class/cs103a/handouts/Guide%20to%20Sets,%20Elements,%20and%20Subsets.pdf

propositional symbols are used to represent different logic statements that can be true or false
`¬`  means `not`
`^` means `and` -- A conjunction
`v` means `or` -- A disjunction
`=>` means "implies"
`<=>` means `if and only if` -- this is a biconditional, and can also be written as `iff`

### Lesson 2 - Inferrence in Propositional Logic
Conjunctive Normal Form (CNF) - a standard way of organising logical sentences so that inferrence 
algorithms can be applied effectively.

Two algorithms: Forward chaining and backward chaining

A formula in CNF only uses conjunctions (`^`) and disjunctions (`v`). 

`(A => B) ^ (¬A => ¬B)` is not normalised as it uses two implications `=>`
This can be normalised by applying a rule twice:
`(¬A v B) ^ (A v ¬B)`

It turns out that `A => B` has the same meaning as `¬A v B`. This is called implication elimination

Other rules:
`A <=> B` can be eliminated into `(A => B) ^ (B => A)`
`A => B` can be eliminated into `¬A v B`
`¬` can only appear in literals, so we need to "move ¬ inwards": 
    `¬(¬A)` is double negative elimination: `A`
    `¬(A ^ B)` becomes `(¬A v ¬B)`
    `¬(A v B)` becomes `(¬A ^ ¬B)`

Horn clause - a statement that looks like this:
`(A1 ^ A2 ... An) => B`
B could also be replaced with `false`

This is usually written in CNF as:
`(¬A1 v ¬A2 ... ¬An) v B`

* Horn clauses are CNF clauses where _at most one_ literal is positive.
* A more restrictive form is the "Definite clause", where exactly one literal is positive
* If you resolve two horn clauses, you get back a horn clause
* Inference with horn clauses is done through forward and backward chaining

Forward chaining checks if a proposition symbol's requisites are all already stored in the 
knowledge base. For example, if `L1 ^ Breeze => B1` is a rule in the knowledge base, and 
the values L1 and Breeze are known, then B1 can be added to the knowledge base.
This can happen for more complex queries until the whole query is added or no further inferrence
can be made. This runs in linear time

Backward chaining instead works back from the query. If the given proposition is already evaluated
in the KB, no works is needed. Otherwise, the required implications are calculated recursively 
until we can add the query and it's prerequisites, or can work backward no more. This also 
runs in linear time.
