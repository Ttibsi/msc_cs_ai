# Week 3 - Event Driven Programming and GUIs

* articulate the considerations required to develop event-driven programs
* demonstrate how closures and lambda expressions are used in Python
* utilise state diagrams to model simple interactions and explore approaches to event-driven design
* demonstrate the application of event-driven programming through the construction of GUIs in Python
* utilise a range of GUI components to design and construct effective interfaces.

### Lesson 1 - Event Driven Programming
GUIs uses events to handle interactions. This doesn't mean those events can't be represented
in an OOP fashion.

Event handlers - code that connects an event to some code that triggers on this event.
When an event occurs, a callback function is triggered to initialise the relevant action

Making a cup of tea - event driven process:
* Open cupboard
    * event: toggle state of cupboard: closed > open
* Remove mug from cupboard
    * event: Decrement count of mug in cupboard
* Add teabag to mug
    * event: decrement count of teabags
    * event: append teabag to contents of mug
* Add sugar to mug
    * event: decrement sugar remaining
    * event: append sugar to contents of mug
* Add hot water to mug
    * event: append water to contents of mug

### Lesson 2 - Formal tools
UML diagrams - a range of tools and frameworks to enable system analysis and specification.

State diagram
- Shows the state changes between each interaction
- larger systems can be broken down into multiple state diagrams.
- UML is more flexible by design

### Lesson 3 - Closures and Lambda expressions
Closure - a state that can be generated.
    - a stored function that has its initial environment stored within it.

To have a closure, a language must have first-class functions
The `nonlocal` keyword allows you to access a var from an outer function in an inner function

```py
def outer():
    x = 0
    def inner():
        # nonlocal x
        x += 1
        print(x)
    inner()
outer()
```

The above crashes if you don't have the `nonlocal` call where it's currently commented out

Lambdas are anonymous functions that can take any number of arguments
