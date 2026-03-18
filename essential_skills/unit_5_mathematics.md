# Unit 5 - Mathematics for Computer Science

* Define the concept of set, the use of set notation, concepts of the intersection and union, the complement of a set (MLO 5)
* Evaluate the probability of an event occurring, and the probability that an event does not occur (MLO 5)
* Define and identify logical connectives (such as AND, OR, NOT) (MLO 5)
* Demonstrate understanding of the Foundations: Logic and Proofs (MLO 5)
* Identify and describe the properties and characteristics of Series (Arithmetic and Geometric) (MLO 5)

### Lesson 1 - Arithmetic expressions
Arithmetic expressions - addition, subtraction, multiplication, division, power, brackets

Absolute value (drops negative sign)
    - uses two bars either side of the value/expression
    - ex |x|

factorial (!)
    - multiply by every value between that and 0
    - ex 3! = 3*2*1

modular arithmetic (%)
    - the remainder

BODMAS
- Brackets, Of, Division, Multiplication, Addition, Subtraction

factorisation of any composite number can be uniquely expressed as a product of prime numbers
prime numbers are any positive integer that "do not have any proper divisor except 1"

Reciprocal of x is 1/x
    - used to normalise events, scaling data uniformly
    - Reciprocal is a number that, when multiplied by the original number, makes 1
    - Reciprocal of a fraction is just to flip the fraction
    - Reciprocal of a negative is also negative

### Lesson 2 - Sets and Probability
A set is a group of values that share a property.
    - EG: engineers may study all components from a production run that fail to meet a certain tolerance

If a set is contained completely in another set, we say one set is a _subset_ of the other.
"element" symbol used when an element belongs to a set (funky E symbol)
An empty set is notated with an O with a strike through it
Sets with overlaps can be represented with a venn diagram

A' (A with an apostrophe) denotes all the elements not in set A that are in the "universal" set
    (universal set is sometimes denoted as S)

The intersection between two sets are denoted with an arch/'n' character, ex `AnB`
The union of two sets (two sets combined) are denoted with a 'u' character (upside down arch)
    ex `AuB`

Set difference (elements in A that aren't in B) is usually written as `A \ B`
    This can also be written as `A - B`

AuB = ABCDEFH
BnC = F
An(BuC) = ACDEF
AnBnC = F
Bu(AnC) = F

a = 0,1,2,3,4,8
b = 1,3,5,7,9
c = 0,1,2,3,4,5,7,8,9
d = 1,3
e = 0,2,4,5,6,7,8,9
f = 1,3
g = everything but 6
h = everything but 0,2,4,8
i = everything but 1,5,7,9

### Lesson 3 - Probability
Probability is the study of uncertainty, dealing with situations where chance is involved

Probability can be seen in:
- Algorithm Design - for sorting data, detecting problems, and predicting user behaviour
- Machine Learning - to model uncertainty, variability, and noise in ML algorithms.
- Probabilistic Programming Languages - PPLS allow programmers to work at a higher level of
    abstraction
- Probability Distributions - Can calculate confidence intervals for parameters and critical
    regions for hypothesis tests

Mutually exclusive events - events that can't happen at the same time
    ex tossing a coin: heads and tails are mutually exclusive

### Lesson 4 - Logic and Proofs
logic are the rules of mathematics, such as "There exists an integer that is not the sum of
two squares"

Proofs are used to verify that computer programs produce the correct output.
There are programming languages that can be used to design proofs.

A proposition is a sentence that declares a fact which is either true or false but not both

A truth table can be used to show the combination of two propositions P and Q.
This is called a conjunction, using the ^ symbol
ex an AND table

0 ^ 0 = 0
0 ^ 1 = 0
1 ^ 0 = 0
1 ^ 1 = 1

A disjunction is an "or", using the v symbol
0 v 0 = 0
0 v 1 = 1
1 v 0 = 1
1 v 1 = 1

Propositions use the format "if P then Q. Therefore if Q is false then P is false"
Some propositions can't be proven because we don't have enough information
    - ex it could be true some of the time but not all of the time.
    This is not a proposition

Implication smbol is `=>`. This is the denotion of "if P then Q"
    `p => q`

Biconditional statements are true with both sides carry the same truth value and are
false otherwise. Sometimes called "iff"
    ex - `p <=> q`
    or - `p iff q`
    or `(p => q) ^ (q => p)`

Exercise:
Smartphone B's ram > A or C's ram therefore A and C are both less than B
