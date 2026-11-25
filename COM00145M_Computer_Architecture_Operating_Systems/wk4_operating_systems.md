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
