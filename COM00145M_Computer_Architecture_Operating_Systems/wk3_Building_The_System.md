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

Host-bus interface - used to connect storage devices.
    - Two most popular interfaces are SATA and SCSI (Scuzzy)

When an IO device wants to become the bus master, it has to REQUEST control from the CPU
The CPU responds with an ACKLNOWLEDGE to agree
The IO device queries the row in memory
The IO device queries the column in memory
The IO device read's from the memory location
The IO device sends a RELEASE to the CPU to tell it that the IO device is finished.

The is considered 1 payload read and 5 overhead instructions.
Efficiency = 1 / 6
    1 payload cycle, 6 total cycles
    Payload cycle count can vary

Bus concurrency
* The system bus will have a certain amount of bandwidth per second
* multiple devices can make use of some of that bandwidth to transfer different data
    within the same second, but there's still only X amount of bandwidth
* IO devices could instead have a "bus bridge" between them and the system bus
    * This bus can connect to higher performance busses such as PCI for
    faster disk access

### Task 1 - Advanced Bus Exercises
bandwidth = frequency * multiplier * bus width

1 - calculate bandwidth performance
data bus = 32 bits = 4 bytes
freq = 50MHz
clock cycle = 20 nanoseconds
send data takes 1 clock cycle each
memory access time = 125ns

* Get address (20ns)
* read memory (125ns)
* send data (20ns)

total time = 20ns + 125 ns + 20ns = 165ns
bandwidth = 4 bytes / (165 * 10^-9) = 242424.24 bytes/s / 10^6 = 24.24Mb/s

2 - Asynchronous
data bus = 32 bits = 4 bytes
handshake = 40ns
memory access time 125ns
both busses can transfer 4 bytes of data

* request read (40ns)
* request address (40ns)
* send data (40ns)
* send ack (40ns)

total time =  40 * 4 = 160 + 125 memory read = 285ns
bandwisth = 4 / (285 * 10^-9) = 14035087.719298244 bytes/s * 10^6 = 14.03 MB/s

3 - How much bandwidth is needed to transmit 1024 butes of data
data bus/transfer speed = 64 bits = 8 bytes
freq = 250MHz
clock cycle = 4ns
1 data transfer = 1 clock cycle
2 cycles between bus operations
memory access time = 100ns per block
bus transfer overlaps with reading the next data
block size = 32 bytes

amount to transfer = 1024 bytes / 32 = 32 blocks
transfers per block = 32 blocks / 8 bytes per transfer = 4
time per transfer = 4 clock cycles (1 address, 1 data, 2 idle) * 4ns = 16ns
total bus time per block = 4 transfers * 16ns = 64 ns
overlap consideration = max(100ns memory time access, 64ns transfer time) = 100ns
total transfer time = 100ns * 32 blocks = 3200ns
bandwisth = 1024 bytes / (3200 * 10^-9) = 320MB/s

### Lesson 2 - Storage Technologies
Magnetic tape - uses a magnetic recording head to write to the tape
    - Data is serialised, written in serial to the tape, and it's location is not stored
    - Read time is broken into seek time and data transfer time
    - These can still be used today for long-form data storage

Hard Disc Drive (HDD) - uses multiple disks in a column, called a plate
    - smallest block that can be written is based on the sector size
        - sector size may be ex 512bytes
    - A file smaller than a sector will still "reserve" the whole sector, meaning
    average wasted space is 0.5sectors.
    - rotational speed of the disk (revolutions per minute) is how fast
    requested bits are read/written.

Data rate
---------
num of sectors = 100
size of sectors = 1kb
RPM = 7200
rotational latency = 60sec/7200RPM = 8.3ms

100 sectors can be read in 8.3ms
1 sector can be read in 83ms
1 byte can be read in 81ns (83ms * 10^-6 / 1024)

Data rate = 1 / 81*10^-9 = 12.3million bytes/s = 11.8Mb/s

Zoned bit recording = number of sectors in outer tracks is higher than on
inner tracks

File access time
----------------
rotational speed = 5400RPM = 90 times a second
one rotation = 11.1ms
data read rate = 100Mb/s
sector size = 2KB

3Kb file spans 2 sectors
Needs to read 4Kb (total size of two sectors)

worst case: seek time 2ms + 1 full rotation 11.1ms
total access time = 13.1ms
read time 40us
total read time: 13.14ms
implies peak data transfer rate of 0.3mb/s

Fragmentation = File data stored in multiple non-concecutive sectors,
    often in the wrong order.
Contiguous file = file stored in sequential sectors

Fragmentated file access time
    num_of_segments * (2ms + 11.1ms + 0.02ms)

Defrag utilities rewrites the whole disk to make all files continuous to increase
performance

SSD - Solid State Drive
    - Uses flash memory, similar to how RAM works
    - Faster and more expensive than HDDs, but have become standard to use

wear-levelling - writing to different parts across the SSD to not overuse a single
cell, wearing out everything at the same speed to decrease the likelihood of
a drive failure
    - This only affects write cycles, not read cycles

Possible faults:
* mechanical failure - a HDD just stops working, making it's data unreadable
* File corruption - Could happen for a number of reasons and is generally unpredictable

Reundant storage arrays can be used to reduce data loss when drive failure occurs
RAID = Redundant Array of Independant Disks
RAID 0 - Just combining the disks into a big pool of storage (Data striping)
RAID 1 - Disk mirroring, 50% storage for data stored in two places in the pool

Remote storage - cloud storage - cloud computing

worst-case time for a sector to rotate into position:
7200RPM in seconds = 120RPS
1 full revolution / 120 RPS = 8.3ms

SSDs and RAID
-------------
* Flash memory built using semiconductors
* NOR memory and NAND memory.
* NOR - basic unit is a single bit
    - provides high-speed random access
    - used for phone OS's or BIOS chips
* NAND - basic unit is 16 or 32 bits
    - Uses small blocks
    - used in flash drives/memory cards/SSDs
    - has greater write speeds than NOR
    - has no external random access bus
* SSDs have higher input-output operations per second (IOPS)
* less susceptible to physical shock
* Runs quieter and cooler
* lower access times and latency rates
* SSDs have their own controller chips

RAID
* Invented at UC Berkeley
* 7 different levels
    * RAID 0 - nonredundant
    * RAID 1 - Mirrored
    * RAID 2 - Redundancy through Hamming code
    * RAID 3 - Bit-interleaved parity
    * RAID 4 - Block-level parity
    * RAID 5 - Block level distributed parity
    * RAID 6 - Dual redundancy

RAID 1 redundancy is achieved through data duplication, whereas other
RAID levels achieve redundancy through parity

RAID 2 and 3 - data striping is used, often only the size of a single
word or byte

RAID 3 has high data transfer rates, due to smaller stripes than other
levels.

RAID 6 is nweer, uses two different parity calculations stored on other
drives. A RAID 6 array of N drives requres N+2 drives

Dual actuator HDDs - twice the data throughput, more power efficient.
Likely means multiple playheads on the disks inside the HDD
- They don't improve latency though

### Task 1 - Storage price investigation
Best HDD based on performance: WD Velociraptor 1TB (2012)
Best SSD based on performance: WD Black SN8100 M.2 1TB (2025)

Most expensive 1TB drive: WD Black SN8100 M.2 1TB (2025) - 290GBP

As identified, hard drive costs are a lot cheaper than Solid State drives. 
This is currently at least partially driven by the ongoing data-center driven component crisis, 
and the timing of this task around Black Friday, as we can observe that the WD Black drive 
in question is currently listed on Amazon for 280, but has fluctuated massively 
in the last month, and an almost 100GBP increase at the end of last month.

Source: https://keepa.com/product/2-B0F3BMBQ75
