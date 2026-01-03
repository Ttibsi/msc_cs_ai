# Wk5 - Recursion and Trees

* Write pseudo-code for non-linear data structures and demonstrate how they work [MLO1].
* Analyse the properties of binary search trees[MLO2].
* Analyse the performance of non-linear data structures  in their application to search algorithms.[MLO1].
* Design and implement recursive algorithms in Python, and assess their limitations. [MLO 3].

### Lesson 1 - Recursion

Recursion - when a function calls itself
    - requires a "base case" to break out
    - pre and post conditions around the recursion call

Recursion is useful for nested data structures such as trees and graphs
or maths algorithms like fibonacci

- "In mathematical logic and computer science recursive definition or inductive definition is used to define an object in terms of itself."

```py
# factorial recursive func
def factorial(n: int) -> int:
    return n * factorial(n - 1) if n else 1
```

All recursive implementations can be implemented as iterative as well

* Recursion will not make your code more performant. It's benefit is simpler code
and may aid in calculating runtime easier

* Memoisation is the case in which we have something that stores our state
as we go. For example, the below fib implementation with an inner func that uses
a dict to store values.

```py
def fib(n: int) -> int:
    def fib_inner(n: int, mem: dict[int, int]) -> int:
        if n in mem.keys():
            return mem[n]
        elif n == 0 or n == 1:
            mem[n] = n
            return mem[n]
        else:
            mem[n] = fib_inner(n - 1, mem) + fib_inner(n - 2, mem)
            return mem[n]

    return fib_inner(n, {})
```

---
### Lesson 2 - Trees
* Represents hierarcical relationships
* Useful for org charts, file systems, domain name hierarchies

Binary tree - tree where each node has at max two children

perfect binary tree 
    - all leaf nodes are the same level
        - not a full binary tree
    - height is log(n + 1)

complete trees != full trees

A full tree - all nodes have either 0 or 2 children
complete tree - all levels are filled (except maybe the bottom)
    - This is made taking an array and filling each height from the data in the array
perfect - full tree in which all leaves are the same depth

complete tree
-------------
[1,2,3,4,5,6,7,8]
       1
     /   \
    2     3
  /  \  /  \
  4  5  6  7
 /
8   

in-order traversal will print the elements in ascending order

          15
        /    \
     10       20
    / \     /  \
  7    12  17  30
/  \
6  9

BFS = [15, 10, 20, 7, 12, 17, 30, 6, 9]
BFS is a row at a time 

inorder = [6,7,9,10,12,15,17,20,30]
in-order - does from left to right -- if the tree is sorted, so is the array

pre-order - parent, then go left, then go right
pre = [15,10,7,6,9,12,20,17,30]

post-orde - visit the left child before the parent
post = [6,9,7,12,10,17,30,20,15]

### Lesson 3 - search trees

binary search tree 
    - quick lookup, insertion, deletion (quick read/write)
    - maintains a sorted structure
Red Black tree
    - ensure balance, consistent performance even in worst cases
    - used for databases, file systems, memory management
    - used where performance is crucial

Properties of a Red Black Tree
    - The root is always black
    - The children of a red node are black
    - all nodes with 0-1 children have the same black depth, the number of 
    black ancestor nodes

RB trees don't have faster searching as they maintain the same shape as 
a BST
RB trees enforce their shape, ensuring that the max depth is always log(n) 
This is by the rules of the red-black colouration of the nodes

Rotating an RB tree - this represents a LEFT rotate
```
func LeftRotate(node x):
    node y = x.right
    x.right = y.left
    if (y.left != NULL):
        y.left.parent = x

    y.parent = x.parent
    if (x.parent == NULL):
        return y
    else if (x == x.parent.left):
        x.parent.left = y
    else if (x == x.parent.right):
        x.parent.right = y

    y.left = x
    x.parent = y
```


### Lesson 4 - Maps, Sets, Hash tables

```py
simple_cypher: dict[str, str] = {
    "a": "z", "b": "y", "c": "x", "d": "w", "e": "v", "f": "u", "g": "t",
    "h": "s", "i": "r", "j": "q", "k": "p", "l": "o", "m": "n", "n": "m",
    "o": "l", "p": "k", "q": "j", "r": "i", "s": "h", "t": "g", "u": "f",
    "v": "e", "w": "d", "x": "c", "y": "b", "z": "a"
}

def encrypt_message(message: str, cipher_dict: dict[str, str]) -> str:
    ret = ""
    for c in message:
        if not c.isalpha():
            ret += c
        else:
            lower = c.lower()
            ins = cipher_dict[lower]
            ret += ins if lower == c else ins.upper()

    return ret

def decrypt_message(message: str, cipher_dict: dict[str, str]) -> str:
    ret = ""
    for c in message:
        if not c.isalpha():
            ret += c
        else:
            lower = c.lower()
            ins = [k for k, v in cipher_dict.items() if lower == v][0]
            ret += ins if lower == c else ins.upper()

    return ret


assert encrypt_message("hello world", simple_cypher) == "svool dliow"
assert encrypt_message("Hello world", simple_cypher) == "Svool dliow"
assert decrypt_message("svool dliow", simple_cypher) == "hello world"
assert decrypt_message("Svool dliow", simple_cypher) == "Hello world"
```

Sets do not maintain order
Sets maintain uniqueness
Set values must be immutatable
Sets use hashing for lookup and insertion
In python, sets use more memory than a list, because they use a hash table 
under the hood
    
```py
def find_common_items(lists: list[list[str]]) -> set[str]:
    first_list: set[str] = set(lists[0])
    for lst in lists[1:]:
        first_list = first_list & set(lst)

    return first_list

shopping_lists = [
    ["milk", "bread", "eggs", "apples"],
    ["bread", "eggs", "bananas", "apples"],
    ["milk", "bread", "apples"]
]
```

Hashing and hash functions
--------------------------
* A mathematical formula that turns an input and maps it to a specific index in
a hash table
* Simple example just uses modulo
* Strings could use the sum of the ascii values of each character, then modulo

Separate chaining - used in hash tables to handle collision
    - This basically uses a linked list at each bucket

Load factor 
    - how full a hash table is
    - shown as n over s (n/s) 
    - where n is the number of elements and s is the size of the table

Perf
    - Adding - O(1)
    - searching - O(1)
        worst case O(n) where n is the size of the linked list bucket
    - deleting - O(1)
    - resizing - O(n)

Open addressing - A different technique used for handling collisions
    * If the hash of a number is already taken, we keep jumping forward to the
    next empty slot
    * Lookup now means that after checking the hash, we need to jump forward
    and check the actual value
        * This means that lookup could be O(s) where s is the size of the table
    * Removal now means that we need to populate slots with "tombstone" markers,
    so that searching will keep going until it finds an empty slot, not a 
    tombstone slot.
    * Tombstones can be replaced during insertion

