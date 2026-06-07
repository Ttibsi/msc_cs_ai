Run through both SAT algorithms by hand

```
1. (X v Y x Z)
2. (X v ¬Y x ¬Z)
3. (¬X v Y x Z)
4. (¬X v ¬Y x ¬Z)
5. (¬Y v Z)
6. (Y v ¬Z)
```

### DPLL Algorithm
model: X(true), Y(true), Z(true)
matches rules: 1, 2, 3, 5, 6

model: X(false), Y(true), Z(true)
matches rules: 1, 2, 3, 4, 5, 6

model: X(true), Y(false), Z(true)
matches rules: 1, 2, 3, 4, 5

model: X(true), Y(true), Z(false)
matches rules: 1, 2, 3, 4, 6

### WalkSAT
```
1. (X v Y x Z)
2. (X v ¬Y x ¬Z)
3. (¬X v Y x Z)
5. (¬Y v Z)
6. (Y v ¬Z)
```
(The instructions say to delete one clause with all three literals in it)

p=0.5
model: X(false), Y(false), Z(true)
matches rules: 1, 2, 3, 5
random value: 0.6
    greater than `p`, flip Y?

model: X(false), Y(true), Z(true)
matches rules: 1, 3, 5, 6
random value: 0.2
    less than `p`, flip Z

model: X(false), Y(true), Z(false)
matches rules: 1, 2, 3, 6
random value: 0.4
    less than `p`, flip X

model: X(true), Y(true), Z(false)
matches rules: 1, 2, 3, 6
random value: 0.7
    greater than `p`, flip Z

model: X(true), Y(true), Z(true)
matches rules: 1, 2, 3, 5, 6
