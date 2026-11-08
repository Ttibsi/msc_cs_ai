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
    - Also called main bus or host bus

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
* rising edge as it turns on, falling edge as it turns off
* This looks like a square wave
* One iteration of off-on-off is called a cycle or period
    * One cycle is a single on/off of a signal
* frequency = 1 / period

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

Binary - base 2
Hex - base 16

Adder circuit - digital circuit that adds two numbers together
* used in the ALU
* Usually operates on binary numbers
* tivial to modify into an adder-subtractor
* half adder has two outputs - the sum and the carry, used in te case of overflow
    in multidigit addition
* full adder accounts for values carried in as well as out
* The simplest half-adder incorporates the an XOR gate for the sum and
    an AND gate for the carry.
* An OR gate can be used to combine two half-adders into a full adder
* alternatively, a full-adder can be implemented with 9 NAND or NOR gates

half-adder truth table
----------------------
(a input, b input) = (carry, sum)
(0, 0) = (0, 0)
(0 ,1) = (0, 1)
(1, 0) = (0, 1)
(1, 1) = (1, 0)

The third input in a full-adder is the carried over bit from the previous execution

full-adder truth table
----------------------
(a in, b in, c in) = (carry, sum)
(0, 0, 0) = (0, 0)
(0, 0, 1) = (0, 1)
(0, 1, 0) = (0, 1)
(0, 1, 1) = (1, 0)
(1, 0, 0) = (0, 1)
(1, 0, 1) = (1, 0)
(1, 1, 0) = (1, 0)
(1, 1 ,1) = (1, 1)

RS flipflop - circuit or latch that retains it's state, either on or off.
RS stands for "reset set".

Alternatively is the D flipflop, short for data flipflop.
These capture the input at a given time in a clock signal, such as the rising edge, which
becomes it's output

A counter is a circuit that does as it states, usually a finite state machine.
Diagrams suggest this works in binary, storing a number of on/off states to represent each bit
in the number being stored and knowing how to increment. These can be implemented using
D flip-flops in one case, or other types of flip-flops

### Lesson 2 - Processors
CPU - a digital electronic circuit, usually built from millions of transistors.
It can hold a small amount of temporary data and perform mathematical operations upon
them.

Fetch-execute cycle
- The CPU fetches the next instruction from memory, then executes it.

MIPS = Million Instructions Per Second
peak mips - maximum possible mips a processor can achieve under the best conditions.
GOPS - giga-operations per second
GFLOPS - giga floating-point operations per second

Main concern is power. Clock speed can be scaled down for pwer saving purposes,
ex CPU Throttling, putting the CPU in a sleep state.

Dynamic power - consumed each operation, the more operations performed per second,
the more power used.  On this basis, setting the clock rate to zero ought to reduce
power consumption to zero too.

Static power - consumed continuously even if the CPU does nothing.

Clock frequency - how many cycles per second (measured in hertz)
pipelining - overlapping instruction execution
    - could also include SIMD? Not clear

branch prediction - static or dynamic
- static is hardwired into the circuitry
- dynamic uses a "branch history table" to store previously reached branches
    and then uses the up-to-date info in that table to decide if a branch should
    be taken or not
- Allows for the CPU to fetch the next instruction immediately for overlapping
execution.

Branch mis-prediction - needing to step-back and re-run a branch because the wrong
branch was taken.
As 1 in 6 instructions are often a branch, this is a risk worth taking.
