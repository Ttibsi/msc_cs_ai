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
- the depth of hte tree is logarithmic in this case
- O(n log n)

worst case - pivot has very uneven splits, such as when the largest number or 
smallest number is consistently chosen as the pivot, or if the array is almost
sorted already
- O(n)
    
space complexity - depends on recursion depth, worst case each recursive call
processes only one element at a time
- should be O(log n), but can decay to O(n^2) in the worst case
