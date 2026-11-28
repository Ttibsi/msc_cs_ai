# Week 4 - Exploring Operating Systems

* Demonstrate understanding of operating systems models and hierarchies, types and standards in brief- Linux, Dos, OSX, graphical O/S and specialised O/S, eg RTOS
* Show appreciation of how programs run, scheduling, and how their characteristics can be measured, including concepts of user/superuser, kernel, multitasking and multithreading, scheduling, priority,
* Show awareness of resource utilisation, virtual memory, memory management, interprocess communication, virtualisation, multiprocessor systems, performance issues – disk swapping
* Understand and recognise some key developments in processors and systems in recent years which directly support the increasing demands of modern operating systems.

### Lesson 1 - Operating System Concepts
Operating system (simplified definition) - A collection of software operating at different
levels to hide the hardware structure from programs and users

Bare-metal system
* Step 1 - reset the program counter to 0 and begin reading from memory
* If there is only DRAM or volatile SRAM, the values will be nonsense
    causing a crash
* Startup instructions are instead read from a non-volatile ROM chip
    * BIOS - Basic Input Output System
    * also called a bootloader
* Step 2 - Initialise any important registers and components
* Step 3 - check for RAM
    * if it exists, then perform a Power-On Self Test (POST) to ensure
    components are working as expected
* Step 4 - Read the disk unit's information, as currently the machine
doesn't know what type of storage is connected
    * This is stored in the drive's boot sector, and is what's executed next

Types of operating systems
* Command line OS (EX MS-DOS and Unix)
* Graphical operating system (Windows, mac, linux)

Kernal - control access to low-level hardware
    - Manages memory allocation
    - Manages allocation of CPU time
    - Manages fault conditions gracefully
    - Controls user access rights
    - Manages how IO devices communicate with the hardware

On top of the kernal are drivers for the hardware
Then utility programs for managing file access, system configuration, and other basic tools
    - GNU coreutils is the example here
Then user programs, such as a browser, terminal emulator, or slack

Concurrency
- Task switching allows the CPU to jump from task to task in microseconds to appear as
if multiple things are running at the same time
- A job can be split into threads running separately, performing differet tasks

RTOS - Real Time Operating System
    * Often found in embedded locations, such as a car's computer or on specific machinery

While a stream of instructions makes up a program, sometimes there are things that
can't wait, such as input from an IO device or packets from the network
adapter. These are called Exceptional Control Flow and need to be handled
right away.

ECF instructions interact with the system using traps or system calls.
Breakpoints are a form of this, as is exception handling

Exceptions are partially implemented in hardware, partially in software
    - Exceptions are usually implemented via jump instructions to a
    separate table of instructions
    - Each exception type is allocated an ID number.
    - On boot, the OS allocates and initialises an exception table
    - At runtime, if an exception is thrown, the processor makes an Indirect Procedure Call
        -  I think this is jumping to the instructions in the exception table

Different types of exceptions:
- Interrupts - Asynchronous, return to next instruction
    - Signal from IO device
- Trap - Synchronous, return to next instruction
    - Intentional exception
- Fault - Synchronous, return to next instruction
    - Partially recoverable error
- Abort - Synchronous, Never returns
    - nonrecoverable error

System calls appear to be the same as normal function calls, but they run
in kernal mode instead and allow for privileged instructions to run and
access a stack in the kernal

Aborts never apply to user code, only apply when DRAM or SRAM bits are corrupted

### Lesson 2 - Workload Management
Processes - programs that run unde control of the OS, the primary way a task is
run. It has it's own private memory buffer and instructions are run at regular
intervals of CPU time.

Thread - Within a process there can be many threads. These each perform a
specific task and execute concurrently within the process. Threads all use
the same OS memory resources allocated to their parent process

PID - Process Identifier
Process Control Block (PCB) contains:
    -  process state
    - Information about it's parent process
    - Task priority and privileges
    - IO attribute information
    - General info such as CPU state data

User-level threads - scheduled by the process code itself
    - the Kernal does not see this as separate entities
Kernal-level threads - requires processes to request that the kernal handles
the thread.
    - User software does not need to implement it's own scheduler

Scheduling algorithms
Simple Sched
    - has a list of currently running tasks
    - every time a new task starts, it's added to the lis
    - ierate through each task and run it for a small period of time
        - ex 1ms
    - When the next task is run, the previous one is suspended
    - A task may have to wait for IO from a disk, which may take longer than it's
    allotted time.

pre-emptive scheduler is the above concept but using a FIFO queue instead of
a list

repetitive-interupt timer is what manages the timing of a scheduler

voluntary yielding - if a thread is idle, it yields back control to the scheduler
to start the next task instead. However, this means we don't know how long the
average thread will run from, just the worst case

timeslice calculation
Each task requires 25ms
    5ms of switching time
100 task = 2500ms for all tasks to run once
A task recieving 20ms of CPU time each time recieves 20/2500 = 0.008 (0.8%)
    of the CPU time

Each inactive task yields after 5ms of switching time
(50*25) + (50*5) = 1500ms average total time
    (assuming 50% of the 100 tasks are inactive)

One way around wasting time is to use multiple queues.
    - One option: Ready queue and IO Wait queue
    - tasks waiting for IO are moved to the latter, which may have a larger
    run time for each thread

Interrupts - signals used to indicate that events have occured, driven by timers
or IO devices.

Priority
    - some tasks are more important than others, need to be executed more often
    or have more CPU time
    - In simple schedulers, tasks have no priority
    - Linux priority swings from -20 to +20, with 0 being the default

    - one approach is to stagger the amount of time allocated to different tasks
        - In practice, this is difficult to achieve
    - Another approach is to keep the time-slices the same but skip over tasks that
    don't need as much time.
        - This is achieved with a priority queue
        - Earliest Deadline First (EDF) priority - used in RTOS systems
    - Another approach is to have multiple queues

For running just a single program, you don't need an OS, you can use the single program
as the software for the instructions. This is how dedicated hardware works.

Job scheduling - given there being multiple programs to run, there is either an operator
or algorithm organising how to share resources between the programs.
    - usually running one at a time in small chunks.

One downside is that all running programs need to occupy memory, and when executing small
parts at a time, we need to move around where in memory we're reading from.
