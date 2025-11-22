# Wk 4 - Linear Data Structures

* Identify and describe abstract data types. [MLOs 1, 3]
* Describe the structure and operations of linear data structures such as stacks, queues and linked lists. [MLOs 2, 3]
* Use Object-Oriented programming concepts such as data encapsulation and information hiding.  [MLO 3]
* Compare and contrast different  Implementations of linear data structures in Python. [MLO3]

Abstract data type - ADTs -- ex stack, queue, linked list

Stacks
* Last in, first out
* ex undo functionality, call stack
* interface:
    * push
    * pop
    * top
    * is_empty
    * len/size
* Most operations are O(1) on a stack
    * I guess even len could be if the stack keeps track of it's length on each
    push/pop call

Queues
* first in, first out
* important for handling ordered sequences of items
    * A priority queue is a type of queue where each element has an assigned priority
    * higher priority items are handled first.
    * Often PQs are implemented with heaps, but they're conceptually different
* interface
    * enqueue - insertion at the rear of the queue
    * dequeue - pops an item from the start
    * first - like top
    * is_empty
    * len
* Each operation here is O(1)
* uses: task scheduling, customer service systems, data buffers

Deques - Double ended queue
* interface
    * add_first
    * add_last
    * delete_first
    * delete_last
    * first
    * last
    * is_empty
    * len
* Depending on implementation, these can all be O(1) operations
* uses: sliding window problems, palindrome checks, undo/redo
* flexible access, efficient

----
Task: Implement a simple Stack:
```py
class Stack:
    data: list[str] = []

    def push(self, str):
        self.data.append(str)

    def pop(self):
        return self.data.pop()

    def top(self) -> str | None:
        if self.data:
            return self.data[0]
        return None

    def is_empty(self) -> bool:
        return bool(len(self.data))

    def len(self) -> int:
        return len(self.data)
```

---
Linked lists
* dynamic memory allocation
* comprised of nodes including a pointer
* insertion - anywhere in the memory - O(1) 
* deletion - remove any element - O(1) 
* traversal - hopping from node to node to find a given node - O(n)
* circular linked list - an implementation where the last node's "next" pointer
points to to the first node
    * Is this not just a ring buffer?
    * Useful for round robin scheduling, or buffering systems

In python, a list is a dynamic array of addresses, with each address pointing
to the location of an element in the list. This is probably why it can store
values of different types, the size of an address doesn't change.

-----
browser history - stack
spell checker - list
task scheduler with propritised tasks - queue
traffic light system - circular list
