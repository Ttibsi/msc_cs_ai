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

### Lesson 4 - Graphical user interface design
wireframe designs - diagrams for modelling interfaces
Human-Computer Interaction is a key area for research in computing

- A UI can be contextual, changing its design based on the purpose required. One example of this is a
smartwatch that shows different "modes" or faces based on the activity at the time, but most often
we'd see this in our own lives on our phone screens, such as changing between light and dark themes
based on the time of day. However, this often doesn't go far enough, and the user is left to configure
their own contexts, such as the iPhone's "Do not disturb while driving" mode or Focus modes that can
toggle based on the device's location (IE: work, home, gym) and time of day to tweak their experience,
notifications, and app layouts for different scenarios.

While reading through the Web Accessibility guidelines, I can observe that there are those that can
choose to benefit from these changes even without being the primary focus. One example of this is
guideline 2.1, which suggests that everything on a webpage should be interactable from the keyboard.
While this is clearly there to support those that have motor issues that prevent them from comfortably
working with a mouse, there are also those that will benefit from this just due to their input
preference, such as those that are used to a terminal-based workflow such as Vim and Tmux. This
empowers users to customise their experience to their common preference and makes sites more user
friendly across the board.

Out of the seven factors that influece user experience as listed by the Interaction Design
Foundation, there appears to be a scale of how much different ones are followed. On one end
of the scale you have useful and credible, which would include websites such as wikipedia,
arxiv, and blogs, whereas on the other side you would have accessible and desirable, which
would include sites such as social media. This scale is highly influenced by the intention
of the webiste, and more importantly, how they get their funding. Wikipedia is funded through
donations and merch, and arxiv was supported by Cornel University up to a few days ago, so
their user experience won't have a massive impact on their funding. Wheras social media
thrives from the number of views, the number of users, so they have designed their pages to be
approachable by anyone, and to keep users eyes on the page for as long as possible, something that
currently is going through the courts as this has reached a dangerous height.

Interface Components
- labels
- buttons
- text boxes
- radio buttons
- check boxes
- tables
- scroll bar
- menus
- tabs

Wireframes are a way to quickly sketch out the interface before starting to code
wireframing tools include `pencil` and `lucidchart`
`Figma` is also a valid option

For programmers, GUI dev can be a source of difficulty from the design aspects

One of the best ways to understand how effective a GUI is can be to perform user testing
Tests can be of a variety of types: observing users, users completing evaluation forms
