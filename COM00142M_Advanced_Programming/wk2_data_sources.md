# Week 2 - Data Sources

* Identify different data sources and how they are formatted and encoded
* Pull data into a program from different sources
* Clean and reformat data into a structure required by your program.

### Lesson 1 - Data Encoding
All computers communicate using binary. Everything else is an abstraction on
top.

- binary (base 2)
- octal (base 8)
- hexadecimal (base 16)

format: the way strings of symbols are arranged within a file
encoding: the way each symbol is represented by the computer

ASCII - American Standard Code for Information Interchange
* First release 1963
* 7 bits (0-127)

Unicode
- "basic latin" occupies the range 0000-007F
- Each "plane" of unicode holds 65536 characters
- Not all are available for public use
- Unicode defines a number of encoding formats known as "Unicode Transformation Format"s
    - EX UTF8, UCS-2, UTF-16
- Only concerned with the mapping of symbols, has no additional attributes (ex font)

- In unicode, the first byte defines how big the symbol is (up to 4 bytes)
- Then the next byte starts with x amount of 1s marking the size
    - ex `11100000` for a 3-byte symbol
- Then every further byte starts with a 1 until the end so that unicode can ensure it's not
corrupted ex in transit during communication

- Example: greek letter sigma
codepoint: u+03A3
11001110 10100011
$$$^     $$

bits with $ underneath them are unicode encoding markers - as mentioned above
the bit with ^ underneath is padding to ensure the first byte fills a whole byte

### Lesson 2 - File Formats
Files are used for 3 reason
- Data backup - the program needs a way to store setings when it's closed (persistence)
- Data input - the quantity of data the user needs to enter is too vast to be entered by hand
- Data consumption - the result the program produces need to be made available for use elsewhere

txt and csv are unstructured data
XML, HTML, OWL are semi-structured data

Metadata - data about the data.
Could also be called markup

docx - based on XML for storage
XML can be validated with a "DTD" file (Data Type Definition file), or with an XML schema
DTD files will define the attributes and values in a tag

YAML
- Created in 2001

### Lesson 3 - File IO
Absolute path - the path to a file using the whole file structure, starting at the drive root.
Relative path - path to a file from the current position in the path

Reading from a file - use `open()` and `read()`/`readlines()`
Writing to a file - use `write()`

### Lesson 4 - Exception handling
Two types of errors
 - syntax
 - execution/runtime

Exceptions can be caught with `try...catch` blocks
You can also add an 'else' block that triggers if no exception is thrown
There's also a 'finally' keyword that runs for cleanup code, weather an error occurs or not

Exceptions can be reraised by the user.

User-defined exceptions can be added with a class that extends the `Exception` type
Assertions can throw exceptions as well, useful for checking the state of the code

### Lesson 5 - Regular Expressions
Regular expression (regex for short) are patterns of characters that describe how
to match any other pattern of characters within a string
Regex can be compiled to speed up the usage of the regex if it's used in multiple locations
