# Notes

Data Cleaning
- if `age_of_casualty` is `-1`, remove row
    - There's a large enough dataset that we can afford to lose these entries and still
    have a large enough dataset to work with
    - Note that we're not explicitly doing the same for `age_band` as it will be
    reflected in the same action
- if `enhanced_casualty_severity` is -1, remove row
    - value is not yet, unknown how big the damage was

Casualty Severity Investigation
 - it appears that we can use Naive Bayes here a few times to group together different
    factors to check for question 1 - WRT identifying three variables


----
Q2 writeup on scaling
https://sqlite.org/faq.html#q5 - Can multiple applications or multiple instances of the same application access a single database file at the same time
(yes)

https://sqlite.org/wal.html
Atomic writes. SQLIte is also threadsafe to implement multiple logic at once

Otherwise, convert to mysql, you can `.dump` the schema and with minimal tweaks import it. 
Adding new columns and tables is feasable. 
https://sqlite.org/lang_altertable.html

SQLite is also pretty easy to "script" as you can use python to manipulate a sqlite db. 
DB updates only happen on a yearly cadence, so analysts can each have their own copy to query, treating it as read-only
    - this can be enforced in python scripts to only open in RO mode
    - https://docs.python.org/3/library/sqlite3.html#how-to-work-with-sqlite-uris
    (see the first code snippet under this link - use this as reference in essay)
    - ref 2: https://www.sqlite.org/uri.html
