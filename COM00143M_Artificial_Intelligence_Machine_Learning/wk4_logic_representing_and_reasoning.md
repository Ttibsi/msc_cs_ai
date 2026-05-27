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
