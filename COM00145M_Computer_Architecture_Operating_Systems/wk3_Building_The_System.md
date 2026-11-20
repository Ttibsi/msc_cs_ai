# Week 3 - Building the System

* Show core knowledge of system integration concepts – motherboards, racks, servers, bus systems and standards, and how to estimate the performance of design choices.
* Demonstrate awareness of data storage systems, including magnetic disk options, capability, function, theory. SSD systems and trends, flash disks, USB sticks,
* Appreciate the principles of encryption, RAID systems and reliability, remote storage, servers.
* Have an overview of peripherals, and their main types, examples, capabilities, and methods of interfacing to systems.
* Select suitable storage components and estimate their performance characteristics.
* Select interfaces and components to achieve compatibility and evaluate the efficiency of given configurations.

### Lesson 1 - Building the System
Motherboard layout has to be carefully considered as signal will start to degrade
over even small distances on a motherboard.
    - One approach around this is to send signals at lower frequencies anyway

Bus master/bus slave - which side of a track controls the data transfer and where
it begins

CPU will often have a bus connecting directly to the GPU, passing over the system bus.
Multiple busses can run concurrently to decrease wait time on various separate operations.

There are multiple standards for manufacturing devices to attach to motherboards, such
as VESA and PCI. The former is mostly obsolete at this point.

Clock driver - a circuit that genertes the signals for the system clock.

Row-Address-Select and Column-Address-Select signals are used to select row and column
in the CPU

PCI bus standard
- 33MHz bus freq
- 32 bit data width
- 32 bit Address range
- Bus arbitration takes 5 clock cycles
- Bus turnaround takes 1 cycle

PCI sends address and data values down the same bus - this is a form of multiplexing
This means the 32 address lines are the same lines as the 32 data lines, but at different times

bus freq (33 million) * data width (32 bits/4 bytes) = 132 million bytes/sec
    - 126 Mb/s transfer rate

