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
- 32 bit data width (4 bytes)
- 32 bit Address range
- Bus arbitration takes 5 clock cycles
- Bus turnaround takes 1 cycle

PCI sends address and data values down the same bus - this is a form of multiplexing
This means the 32 address lines are the same lines as the 32 data lines, but at different times

bus freq (33 million) * data width (32 bits/4 bytes) = 132 million bytes/sec
    - 126 Mb/s transfer rate

Calculating transfer rate:
bus width = 32 bits = 4 bytes
cycle per transaction = 5 arbitration + 1 turnarions = 6 cycles
byte per cycle = 4 bytes / 6 cycles = 0.66
clock rate = 33Mhz = 33_000_000 bits
data rate = 0.66 * 33 * 10^6 cycles * 10^6 bytes/s
data rate = 219.7

Calculating block transfer efficiency:
amount to transfer = 16 bytes
transfers = 16 bytes / 4 bytes
total cycles  6 overhead + 4 data = 10 cycles
bytes per cycle = 16 / 10 = 1.6
Ideal (no overhead) = 4 bytes per cycle
efficiency = 1.6 / 4 = 0.4 = 40%

Universal Serial bus (USB)
--------------------------
* Designed for peripherals over internal devices
* Requires very little power to run
* USB1.0 came out in 1996
    * Data rate of 12 Mb/s
    * up to 8192 bit data payload per transfer packet
* Every transmission starts with a SYNC signal (8 bits)
* transmission packet then includes an identifier (8 bits)
* 16 bit CRC error check
* finishes with a 3-bit End Of Packet sequence

* USB has no clock, so it uses another circuit to detect the data flow
from the device
* If too many 1s or 0s are sent concecutively, the clock recovery circuit will de-sync.
    * USB hardware will send another alternative bit to avoid this from happening
    * Data transfer may take 1/6 longer than expected  because of this

* Updated versions of the standard (USB 2, USB 3, USB 4) are faster.

I2C - Inter-integrated chip bus standard
* This can be used as a hub interface
* appears to be part of the CPU usually.
* Uses a simple protocol
    - Serial Clock Line provides syncronisation
    - Serial Data provides the means to transmit data bits
* any device on an I2C chip can become the master, so an algorithm exists to
prevent conflict - "Back off and retry"

CAN bus - Cotroller Area Network
* Designed by the automotive industry for the devices in a car to link together
via a two-wire interface
* Differencial signalling - two wires transmit signals with poosing pos and neg
voltages
    - Makes the system resiliant to noise disrupting the signals

* Direct Memory Access - allows an IO device to take over control of the system bus
    and transfer data to a destination without CPU involvement.
    - More efficient as it uses larger block transfers
    - One example: Used for smoother audio streaming
