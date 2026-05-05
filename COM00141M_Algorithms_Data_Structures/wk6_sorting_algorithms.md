# Wk 6 - Sorting Algorithms, Divide and Conquer, Handling Errors

* Write sorting algorithms and demonstrate how they work [MLO1]
* Analyse and compare the performance of sorting algorithms [MLO2]
* Apply appropriate exception handling techniques to prevent program crashes [MLO 4]
* Design and implement a Python program that effectively handles various types of exceptions [MLO 4]

# Lesson 1 - Priority Queues
An ADT that is similar to a queue but with an added priority assigned to each
element. This is usually implemented with a data structure like a Heap, for
insertion/removal in logarithmic time. PQueues are used for task scheduling,
pathfinding algorithms, and simulations.

Priority Queue ADT:
* add()
* min()
* remove_min()
* is_empty()
* len()

Implementing with a sorted list has O(1) for all methods except `add()`, which
is O(n) -- using an unsorted list has O(1) for all methods except finding the
minimum element, which is O(n). This shows the tradeoff between implementations.

Binary Heaps are a specialised binary tree to implement a PQueue. These are 
perfect for use cases such as Dijkstra's shortest path and a minimum spanning
tree

"Complete" binary tree

(assuming a max-heap here)
Insertion - add to end, then bubble up
bubbling - swap with parent if parent is smaller (min-heap: larger) than new number

deletion - usually involves removing the root element as it's the element with
right amount of priority.
- swap with the last element in the tree to maintain the complete binary tree
- bubble down from the root by swapping with the larger (min-heap: smaller) child
node

A heap can be represented as an array - the two children of a given node are
found by doing the calculation `(idx * 2) + (1 if left_node else 2)` and 
conversely the parent value of a node is found at `(idx - 1) // 2`

Heap sort - two steps
- Building a heap ( this is called heapification)
    - start with the first non-leaf node and compare against it's children, then swap
    - next do the same with it's partner node
    - then continue the process layer by layer, comparing all the way down

- sorting the heap 
    - swap the root with the last element
    - remove the right-most node as it's already in the right position
    - go node by node and re-heapify and remove the right node
    - sorting is complete once the length is only 1.

heap sort speed
    - building a heap is O(n) due to heapification, less work is needed at 
    each level
    - sorting the heap, each removal takes O(log n)
    total - O(n log n) -- this is the same for best, worst, average case

No extra space needed alongside the heap itself.
binary heap has O(log n) insertion as you need to walk down the tree when 
re-heapify'ing

## Lesson 2 - Divide and Conquer methods for sorting
Merge sort
- dividing the list into smaller portions and sorting them back together
- guarunteed O(n log n) perf
- 3 steps
    - divide the list into 2 equal halves recursively 
    - sort each half that's been split recursively
    - merge them both back together

Quick sort
- select a pivot
- split on that point
- sort left
- sort right
- combine sorted subarrays

Best time - when the pivot divides the array in roughly equal halves each time
- the depth of the decision tree is logarithmic in this case
- O(n log n)

worst case - pivot has very uneven splits, such as when the largest number or 
smallest number is consistently chosen as the pivot, or if the array is almost
sorted already
- O(n)
    
space complexity - depends on recursion depth, worst case each recursive call
processes only one element at a time
- should be O(log n), but can decay to O(n^2) in the worst case

### Discussion topic
```
ALGORITHM is_unique(S):
    if length(S) is less than 2
        return True

    Let T be a binary search tree
    for elem in S:
        if elem in T:
            return False
        else:
            insert elem into T

    return True
```

Algorithmic analysis
Here we use a Binary Search Tree to utilise it's sorted behaviour for quick 
insertion and lookup, both on average O(log n). This means we don't have to 
rely on sequence S being alredy sorted when searching. Notably, a pre-sorted 
sequence would have a negative affect on searching, as every node would be 
inserted to the right of the preceeding parent, leading to a worst case of O(n)
lookup -- effectively making our tree just a linked list.

We then need to consider the fact that we're iterating through -- at worst -- 
every element in S, which is a linear operation. Therefore our worst case 
performance here overall is O(n^2). However, our asymptotic performance is 
O(n log n) assuming our tree takes a traditional tree shape.

We could alternatively utilise a self-balancing tree, such as a Red-Black tree.
While this wouldn't have any signficant impact on performance, the 
self-balancing property would prevent the previously mentioned scenario when 
using a pre-sorted sequence, turning the worst case scenario from O(n^2) into 
O(n log n) as the height of the tree will always be log n. However, this is 
likely an over-optimisation based on the given scenario and should only be 
revisited if the BST implementation runs into relevant edge case issues.

## Lesson 3 - Handling errors and working with text files in python
* Python executes at most 1 except block
* `else` and `finally` keywords can follow
* `else` will trigger if no except block is entered
* `finally` is always called whether there's an exception or not

```py
try:
    input = int(input("enter a num "))
    out = 10 / input
except ValueError:
    print("ValueError")
except ZeroDivisionError:
    print("ZeroDivisionError")
else:
    print(f"{out=}")
finally:
    print("And now we clean up...")
```

You can create custom error types by `raise`ing a custom type:
```
class FooError(Exception):
    pass

raise FooError
```

* We should also use docstrings for documentation
* You can have an except block hold two error types with: `except (FooError, BarError):`

### Text files
```py
# Write a script to save the contents of a string variable, a_word, into a file named exo1.txt.
with open("exo1.txt", "w") as f:
    f.write(a_word)

# Write a function called save_to_log(entry, log_file) that takes two 
# parameters: a string entry to be added to the end of a text file named 
# log_file (also a string). The function should ensure that the existing 
# content of the log_file is NOT overwritten.
def save_to_log(entry: str, log_file: str):
    with open(log_file, "a") as f:
        f.write(entry + "\n")
```

