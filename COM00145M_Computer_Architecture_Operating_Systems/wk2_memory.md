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
