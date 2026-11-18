# Week 2 - Computer Memory Subsystem

* Demonstrate awareness of concepts of memory as a system component, including types of memory, technology & capability, performance issues, and solutions, including cache memory.
* Understand and evaluate given memory configurations for performance, cache memory and memory hierarchy, hit rates,  memory configurations for better performance, including the cost-performance tradeoff.
* Identify suitable components for a memory system with a given degree of performance (high, low) and cost (high, low).

### Lesson 1 - Making Memories
Mercury Delay Line - a system that used sound waves to represent 1s/0s
    - upside: could store more than 500 bits of data
    - downside: used 20kg of mercury per line

Magnetic core-store - uses magnetic rings in a matrix to form a grid of binary storage elements.
    - used in Apollo systems

Types of memory:
- Read-only memory, also called non-programmable memory
- One-time Progarammable memory
    - cheaper to manufacture
    - data content is never lost as it's written to hardware
    - also called PROM (Proogrammable ROM)
- Programmable non-volatile memory
    - can be erased and reprogrammed many times.
    - EPROM - erasable programmable ROM is erased using UV light
    - EEPROM - erased by an electrical signal
    - EAROM - Electicall alterable rom - reprogrammed using electrical signals
    - Flash memory - a variation of EEROM, has large capacity, cheap, fast to read/write

SRAM and DRAM - static and dynamic Random Access Memory.
An SRAM cell can be made up of only 6 transistors (6T).

Memory speed is usually slower than CPU speed.
Burst mode - DRAM feature that boosts memory performance
    - A DRAM can be instructed to read a number of concecutive memory contents onto the
    bus one after another.
    - Isn't used all the time as it will cause access issues

Within RAM, data is stored in a 2x2 grid of cells, these correlate to memory addresses, it's
the literal address of the cell row and column.
Fast Page Mode can send a row and then multiple column locations in any order within that row
for addressing, which is another performance improvement

Cycle time - the total time a memory module takes to complete a full read/write operation
    - this includes both access and reccovery time

* Different storage technologies have different price and performance trade-offs
* Price and performance properties of different technologies are changing at different rates
* DRAM and disk perf lags behind CPU perf

Programs with good Locality run faster than those without.
Locality - the concept of keeping data that's commonly accessed together nearby in memory
    to reduce the retrieval time.
Programs that repeatedly reference the same variables enjoy good temporal locality.
    - A C-style for loop is a good example of this, referencing the iteration variable
        regularly in a short period.

RAM comparison on userbenchmark.com
- highest performing device: G.Skill TZ/RJ/FX DDRa5 6000 C30 (£2809)
- highest cost device: G.Skill TZ/RJ/FX DDRa5 6000 C30 (£2809)

### Lesson 2 - Performance Challenge
Cache memory - a small but fast type of memoryued to reduce access time to
frequently used data

10% of program code is accessed 90% of the time. These often have spacial
or temporal locality - in adjacent locations or used multiple times
within a short time period

Working set - 10% of memoyry we wish to access frequently
Cache - small amount of fast SRAM alongside a large amount of slow DRAM
    - There may be a cache set built into the CPU, and it may be split in two
        for data and instructions

There can be multiple caches in a system, which can alleviate the Von Neumann
Bottleneck.

Cache replacement policies - what values should be stored in the cache instead
of being returned to the main memory
    - Least Recently Used (LRU)
    - Least Frequently Used (LFU)
    - First In First Out
    - Random Replacement

instruction-only cache is called an `i-cache`
    - often read-only, making them simpler
data-only cache is called a `d-cache`
unified cache = both

Separate caches allow for reading both instructions and data at the same time

On an intel i7 chip, each of the four cores have their own private L1 i-cache
and d-cache and L2 unified cache. There's also an on-chip L3 unified cache.

Writing code with good locality
- make the common case go fast
    - focus on optimising the main loops of the application
- minimise the number of cache misses in each inner loop

reads per sec = (clock rate / average read time)
Data transfer rate = reads per sec * bits per read

### Lesson 3 - Errors, Mapping, Coherency
ECC RAM - Error Correcting Code RAM
    - utilises various algorithms, including parity check or Hamming code
    - Hamming code invented by "Richard Hamming" at Bell Labs

Power On Self Test - POSTing, a check the computer does when it boots.
    - write test data patterns to every memory location and check the response

IO mapping - a part of memory that IO devices read and write to, ex when you press
a key on a keyboard, or stoing the caps lock toggle.
These are usually known as IO-addressable registers

Some OS's highlight parts of the memory to be non-cachable, such as IO registers,
to prevent different cores reading cached inputs

DDR = Double Data Rate.

Memory map - mapping out how much memory each part of cache takes up.
example:

ROM - 4k - addresses 0000 to 0FFF
DRAM - 32k - addresses 1000 to 8FFF
[ big empty space here ]
IO device 1 - F000 to F007
IO device 2 - F1000 to F107

Cache coherency
* In a realtime system such as a gas sensor with an alarm, the input level
likely shouldn't be read to the cache as the gas level may not be accurate

Memory errors
* hardware failures and software failures
* hardware failures usually mean there's a tansistor either stuck or switching
    between 0 and 1 eratically.

* An error correcting code is a value written with any value written to memory.
* When a value is read, it's ECC is read too to verify that it's not corrupted
* If the ECC is wrong, the value gets sent to a "corrector" on the die

Hamming code:
* 4-bit words are written as the ECC code. Half the bytes are the value you're
writing, the other half is parity bits. Each word has an even number of bits.
The parity is calculated using XOR against the "Hamming code"

One downside of this is that it will only correct a single error. If there are
multiple, it may not detect them.

### Task 1 - Memory Map Independant Practice
A system with 1 MByte of memory, 128K ROM, 512K RAM, and three IO devices with 8 registers each, mapped to the top area of memory.

memory total range - 0x00000-0xFFFFF

IO device 1 - 0x00000 - 0x00007
IO device 2 - 0x00008 - 0x0000F
IO device 3 - 0x00010 - 0x00017
ROM - 128k - 0x00018 - 0x20017
RAM - 512k - 0x20018 - 0x90017
Unused - 0x90017 - 0xFFFFF
