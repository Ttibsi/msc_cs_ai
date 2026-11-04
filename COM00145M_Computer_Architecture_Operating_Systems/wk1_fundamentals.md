# Fundamentals of Computer Architecture

* Demonstrate understanding of a basic computer model and essential components capabilities, attributes, terminology,
    and relevance to performance, including the concept of binary, switching, and logic at a simple level that
    relates to low-level computing architecture, speed, and processor frequency.
* Understand what defines performance, how programs translate into instructions, in particular, speed versus complexity,
    memory versus core CPU tradeoffs, and apply this knowledge in reasoning about and comparing such components in a given context.
* Investigate and find data and specifications for processors from relevant sources, appreciating the key
    attributes defining processor desirability and being able to reason about how these attributes fulfil expectations
    of a target application.


### Lesson 1 - Fundamentals
Key elements of hardware
* Includes electronics, chips, circuit boards
* by definition, also includes peripherals - and some are "all but essential"
* All electronic devices consume electricity and generate heat
* operate on the level of binary numbers/signals
* Many performance limitations relate to the speed at whch circuits can manipulate those
    signals.

Key elements of software
* Applications you can install (in userspace)
* utilities that are part of the OS
* the OS itself and sxoftware embedded within peripherals, known as firmware
* Low level software that is part of the motherboard - the BIOS
    - Basic Input Output System
* Software that runs as part of a web page
* Compilers
* Interpreters
* pograms you write yourself then run on the system "user programs"
* software we do not want, such as viruses
* software that is installed to detect and prevent viruses

* Power - electricity measured in watts
* Frequency - how often a given activity happens per second. Measured in "Hertz"
* Data Capacity - measured in bytes or some increment of (ex megabyte, gigabyte)
* Data Rate - quantity of data that can be transferred in a given amount of time
    - usually bytes per second

Von Neumann Model - CPU, Memory, IO devices
* Also listed as Control Unit, Arithmetic Logic Unit (ALU), and memory
* Modules are connected via a "system bus"

Busses allow many devices to share one communication route for information.
Only one device can control the bus at a time, called a bus master
A bus is a combination of wires that designate an address, the data, and essential control signals

Cache is a type of memory that's much faster than normal memory

Von Neumann Bottleneck - multiple devices trying to use the same bus to access memory, slowing
down access as memory or the cache can only be accessed along the single system bus by one
device at a time

Harvard architecture - tries to alleviate the bottleneck by introducing two busses, one for
program memory and the other for data memory and IO

clocks - used to synchronise operations by generating a regular sequence of electrical pulses

---
History of computers
ENIAC - Electronic Numerican Integrator and Computer
    - Proposed in 1943 by the US for running calculations on ballistic missile targetting
    - Completed in 1946, too late for the war effort, but was used during project manhatten
    - Built using over 18000 vacuum tubes and weigh over 30 tons

Second generation computer - replacing vacuum tubes with transistors
    - The transistor was invented at bell labs in 1947 but were not fully available until the
        late 1950s
    - also introduced new more complex ALUs and control units, and the provision of system
        software to manage those
    - Digital Equipment Corporation (DEC) formed in 1957, creating the PDP-1
    - Another new architectural feature of 2nd generation computers is the "multiplexer", a
        chip that terminates all the data channels and schedules memory access

Third generation computer - integrated circuits
    - Invented in 1958
    - first used in the IBM System/360 and the DEC PDP-8
    - The System/360 was the first family of computers at different price ranges, starting
        from the model 30 at the lower end and the model 75 on the higher end
    - Meanwhile the PDP-8 was the first machine small and cheap enough to sit on a desk like
        a desktop of today.

Further changes are less defined as generations, but advances include:
* semiconductor memory
* microprocessor CPUs - all the components of a CPU on a single chip
    - developed with Intel's 4004 in 1971
